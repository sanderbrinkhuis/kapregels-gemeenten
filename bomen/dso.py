"""Omgevingsplan (nieuwe deel) uit het DSO: kapregels zoeken.

Per gemeente:
  1. POST /regelingen/_zoek met bevoegdGezag = gmXXXX (lijst van regelingen in het DSO)
  2. GET  /regelingen/{id}/documentstructuur van het omgevingsplan (volledige tekst, één verzoek)
  3. artikelen over kap (houtopstand, vellen, bomen, kappen, herplant) naar dso/omgevingsplan_kap.md

Bron: Omgevingsdocumenten Presenteren API v8 (productie). De sleutel staat in de omgevingsvariabele
DSO_API_KEY of in .env (nooit committen) en gaat mee als header x-api-key, niet in de URL.

Limieten: het DSO kent een fair use policy zonder gepubliceerd aantal. We houden ruim marge:
standaard één verzoek per 3 seconden (ca. 1200 per uur), terugvallen bij 429/5xx en stoppen
als het blijft. Ruwe antwoorden worden gezipt bewaard (data/gemeenten/*/*/dso/, niet in git).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from .http import ROOT, USER_AGENT, _record, now_iso

BASE = "https://service.omgevingswet.overheid.nl/publiek/omgevingsdocumenten/api/presenteren/v8"
INTERVAL = 3.0
KAP = re.compile(r"houtopstand|\bbomen\b|\bboom\b|\bvellen\b|\bkappen\b|\bkap\b|her ?plant|houtwal|houtsingel", re.I)
STERK = re.compile(r"houtopstand|\bvellen\b|\bkappen\b|kapvergunning|her ?plant|houtwal|houtsingel", re.I)
BRUIDSSCHAT = re.compile(r"\b22\.(29[0-9]|30[0-9])\b")
_last = [0.0]


class DSOError(RuntimeError):
    pass


def api_key() -> str:
    key = os.environ.get("DSO_API_KEY")
    if not key and (ROOT / ".env").exists():
        for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if line.startswith("DSO_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        raise DSOError("Geen DSO_API_KEY (omgevingsvariabele of .env).")
    return key


def _request(path: str, *, body: dict | None = None, context: str = "") -> bytes:
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    headers = {"x-api-key": api_key(), "Accept": "application/hal+json", "User-Agent": USER_AGENT}
    if data is not None:
        headers["Content-Type"] = "application/json"
    for attempt in range(4):
        wait = _last[0] + INTERVAL - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read()
                _record({"url": url, "method": req.get_method(), "body": body, "retrieved_at": now_iso(),
                         "status": resp.status, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                         "content_type": resp.headers.get("Content-Type", ""), "context": context})
                return raw
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                pauze = 60 * (attempt + 1)
                print(f"  HTTP {e.code}, wacht {pauze} s", flush=True)
                time.sleep(pauze)
                continue
            _record({"url": url, "method": req.get_method(), "body": body, "retrieved_at": now_iso(),
                     "status": e.code, "error": str(e), "context": context})
            raise DSOError(f"{url}: HTTP {e.code}") from e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f"  netwerkfout {e}, wacht 30 s", flush=True)
            time.sleep(30)
    raise DSOError(f"{url}: blijvende fout; gestopt om de limieten te respecteren")


def _text(xml: str | None) -> str:
    if not xml:
        return ""
    s = re.sub(r"<\?xml[^>]*\?>", "", xml)
    s = re.sub(r"</(Al|Li|Kop|Opschrift|Nummer|Label)>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _walk(node, pad: list[str], out: list[dict]):
    """Platte lijst artikelen (met leden) uit de documentstructuur."""
    for c in node.get("_embedded", {}).get("documentComponenten", []):
        kop = _text(c.get("kop"))
        t = c.get("type")
        if t == "ARTIKEL":
            leden = [c] + list(_iter(c))
            tekst = " ".join(_text(x.get("inhoud")) for x in leden if x.get("inhoud"))
            out.append({"pad": " > ".join(pad), "kop": kop, "tekst": tekst,
                        "vervallen": bool(c.get("vervallen")), "id": c.get("identificatie")})
        else:
            _walk(c, pad + ([kop] if kop else []), out)


def _iter(c):
    for k in c.get("_embedded", {}).get("documentComponenten", []):
        yield k
        yield from _iter(k)


def regelingen(gm: str, dest: Path) -> list[dict]:
    f = dest / "regelingen.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    raw = _request("/regelingen/_zoek?size=100", body={"bevoegdGezag": [gm.lower()]}, context=f"dso-zoek {gm}")
    lijst = [{"identificatie": r["identificatie"], "titel": r.get("officieleTitel") or r.get("citeerTitel"),
              "type": r.get("type", {}).get("waarde"), "expressionId": r.get("expressionId"),
              "beginGeldigheid": r.get("geregistreerdMet", {}).get("beginGeldigheid"),
              "self": r.get("_links", {}).get("self", {}).get("href")}
             for r in json.loads(raw).get("_embedded", {}).get("regelingen", [])]
    dest.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(lijst, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return lijst


def omgevingsplan(gm: str, gdir: Path) -> dict:
    dest = gdir / "dso"
    regs = regelingen(gm, dest)
    plan = [r for r in regs if r["type"] == "Omgevingsplan"]
    res = {"gm_code": gm.upper(), "regelingen_dso": len(regs), "omgevingsplan": None, "kapartikelen": []}
    if not plan:
        return res
    r = plan[0]
    res["omgevingsplan"] = {k: r[k] for k in ("identificatie", "titel", "expressionId", "beginGeldigheid")}
    gz = dest / "omgevingsplan_documentstructuur.json.gz"
    if gz.exists():
        raw = gzip.decompress(gz.read_bytes())
    else:
        uri = "/regelingen/" + urllib.parse.quote(r["identificatie"].replace("/", "_"), safe="_") + "/documentstructuur"
        raw = _request(uri, context=f"dso-omgevingsplan {gm}")
        gz.write_bytes(gzip.compress(raw))
    arts: list[dict] = []
    _walk(json.loads(raw), [], arts)
    hits = [a for a in arts if not a["vervallen"] and KAP.search(a["kop"] + " " + a["tekst"])]
    res["artikelen_totaal"] = len(arts)
    for a in hits:
        a["sterk"] = bool(STERK.search(a["kop"] + " " + a["tekst"]))
        a["bruidsschat_aanvraag"] = bool(BRUIDSSCHAT.search(a["kop"]))
    res["kapartikelen"] = [{"kop": a["kop"], "pad": a["pad"], "id": a["id"], "sterk": a["sterk"],
                            "bruidsschat_aanvraag": a["bruidsschat_aanvraag"]} for a in hits]
    res["sterk_buiten_bruidsschat"] = sum(1 for a in hits if a["sterk"] and not a["bruidsschat_aanvraag"])
    md = [f"# Omgevingsplan (DSO) – kapgerelateerde artikelen {gm.upper()}", "",
          f"Regeling: {r['titel']} ({r['identificatie']}), expressie {r.get('expressionId')}, "
          f"geldig vanaf {r.get('beginGeldigheid')}. Opgehaald {now_iso()} via DSO Presenteren v8.",
          f"Artikelen totaal: {len(arts)}; met kaptermen (niet vervallen): {len(hits)}.", ""]
    for a in hits:
        label = "aanvraagvereisten bruidsschat" if a["bruidsschat_aanvraag"] else ("sterk" if a["sterk"] else "zwak (alleen boom/bomen)")
        md += [f"## {a['kop']} [{label}]", f"_{a['pad']}_", "", a["tekst"], ""]
    (dest / "omgevingsplan_kap.md").write_text("\n".join(md), encoding="utf-8")
    return res
