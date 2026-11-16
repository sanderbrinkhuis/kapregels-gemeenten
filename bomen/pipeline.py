"""Per gemeente: zoeken, downloaden, extraheren en de herkomst vastleggen."""

from __future__ import annotations

import json
import re
import traceback
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import bekendmakingen as ob
from . import cvdr
from .extract import extract_markdown, full_text
from .http import DATA, ROOT, FetchError, fetch, now_iso

ALIASES = ROOT / "config" / "aliassen.json"
GEMEENTEN_DIR = DATA / "gemeenten"


@dataclass
class Options:
    refresh: bool = False
    bekendmakingen: bool = True
    alle_documenten: bool = False
    steekproef: int = 10
    max_bekendmakingen: int = 5000


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def gemeente_dir(g: dict) -> Path:
    return GEMEENTEN_DIR / slug(g["provincie"]) / f"{g['gm_code']}_{slug(g['gemeente'])}"


def aliases() -> dict:
    if ALIASES.exists():
        return json.loads(ALIASES.read_text(encoding="utf-8"))
    return {}


def names_for(g: dict) -> tuple[str, str]:
    a = aliases().get(g["gm_code"], {})
    return a.get("cvdr", g["zoeknaam"]), a.get("bekendmakingen", g["zoeknaam"])


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def process(g: dict, opt: Options) -> dict:
    gdir = gemeente_dir(g)
    raw = gdir / "raw"
    today = date.today()
    cvdr_name, ob_name = names_for(g)
    summary: dict = {
        "gemeente": g["gemeente"], "gm_code": g["gm_code"], "provincie": g["provincie"],
        "zoeknaam_cvdr": cvdr_name, "zoeknaam_bekendmakingen": ob_name,
        "opgehaald_op": now_iso(), "peildatum": today.isoformat(), "fouten": [],
    }

    # --- CVDR-regelingen -------------------------------------------------------
    try:
        q, recs = cvdr.search(cvdr_name, raw, refresh=opt.refresh)
        summary["cvdr_query"] = q
        summary["cvdr_treffers"] = len(recs)
        for r in recs:
            r["status"] = cvdr.status_of(r, today)
            r["gedownload"] = False
            wanted = r["status"] != "vervallen" and (opt.alle_documenten or cvdr.DOWNLOAD_TITLE.search(r["titel"]))
            if not wanted or not r["xml_url"]:
                continue
            try:
                xml = fetch(r["xml_url"], gdir / "cvdr" / f"{r['id']}.xml", refresh=opt.refresh,
                            context=f"cvdr-doc {g['gm_code']}")
                r["gedownload"] = True
                r["xml_pad"] = str((gdir / "cvdr" / f"{r['id']}.xml").relative_to(ROOT))
                txt = gdir / "tekst" / f"{r['id']}.md"
                txt.parent.mkdir(parents=True, exist_ok=True)
                txt.write_text(full_text(xml), encoding="utf-8")
                md, koppen, integraal = extract_markdown(r, xml)
                ex = gdir / "extract" / f"{r['id']}.md"
                ex.parent.mkdir(parents=True, exist_ok=True)
                ex.write_text(md, encoding="utf-8")
                r["relevante_artikelen"] = koppen
                r["integraal_relevant"] = integraal
            except Exception as e:  # noqa: BLE001
                r["fout"] = str(e)
                summary["fouten"].append(f"cvdr {r['id']}: {e}")
        _write_jsonl(gdir / "regelingen.jsonl", recs)
    except (FetchError, Exception) as e:  # noqa: BLE001
        summary["fouten"].append(f"cvdr-zoek: {e}")
        recs = []

    # --- Bekendmakingen (praktijkcontrole) ------------------------------------------
    pubs: list[dict] = []
    if opt.bekendmakingen:
        try:
            q, total, pubs = ob.search(ob_name, raw, refresh=opt.refresh, max_records=opt.max_bekendmakingen)
            summary["bekendmakingen_zoekmethode"] = "titel"
            # Veel gemeenten publiceren kapbesluiten in verzamellijsten zonder kapterm in de titel.
            # Bij minder dan 5 titeltreffers ook de volledige tekst doorzoeken en de grootste uitkomst nemen
            # (besluit gebruiker 16-11-2026; eerder alleen bij 0 titeltreffers).
            if total < 5:
                q2, total2, pubs2 = ob.search(ob_name, raw, refresh=opt.refresh,
                                              max_records=opt.max_bekendmakingen, mode="tekst")
                if total2 > total:
                    q, total, pubs = q2, total2, pubs2
                    summary["bekendmakingen_zoekmethode"] = (
                        "volledige tekst (benadering: kan ook niet-kapbesluiten bevatten)")
            summary["bekendmakingen_query"] = q
            summary["bekendmakingen_totaal"] = total
            besluiten = sorted((p for p in pubs if p["soort"] == "besluit"), key=lambda p: p["datum"], reverse=True)
            for p in besluiten[: opt.steekproef]:
                if not p["xml_url"]:
                    continue
                try:
                    xml = fetch(p["xml_url"], gdir / "bekendmakingen" / f"{p['id']}.xml", refresh=opt.refresh,
                                context=f"bekendmaking {g['gm_code']}")
                    p["gedownload"] = True
                    p["grondslag_citaten"] = ob.grondslag_snippets(xml)
                except Exception as e:  # noqa: BLE001
                    p["fout"] = str(e)
                    summary["fouten"].append(f"bekendmaking {p['id']}: {e}")
            _write_jsonl(gdir / "bekendmakingen.jsonl", pubs)
        except Exception as e:  # noqa: BLE001
            summary["fouten"].append(f"bekendmakingen-zoek: {e}")

    # --- Samenvatting ---------------------------------------------------------------
    geldend = [r for r in recs if r["status"] in ("geldend", "toekomstig")]
    summary["geldende_regelingen"] = len(geldend)
    summary["geldend_met_kapartikelen"] = sorted(
        r["id"] for r in geldend if r.get("relevante_artikelen") or r.get("integraal_relevant"))
    summary["bekendmakingen_besluiten"] = sum(p["soort"] == "besluit" for p in pubs)
    summary["bekendmakingen_aanvragen"] = sum(p["soort"] == "aanvraag" for p in pubs)
    summary["bekendmakingen_geweigerd"] = sum(bool(ob.GEWEIGERD.search(p["titel"])) for p in pubs)
    summary["bekendmakingen_steekproef_met_grondslag"] = sum(bool(p.get("grondslag_citaten")) for p in pubs)
    (gdir / "bronnen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (gdir / "index.md").write_text(render_index(g, summary, recs, pubs, gdir), encoding="utf-8")
    return summary


def render_index(g: dict, s: dict, recs: list[dict], pubs: list[dict], gdir: Path) -> str:
    L = [f"# {g['gemeente']} ({g['gm_code']}) — {g['provincie']}", "",
         f"Verwerkt: {s['opgehaald_op']} · peildatum geldigheid: {s['peildatum']} · "
         f"ophaaltijd per bronbestand: data/manifest.jsonl", "",
         "## Geldende en toekomstige regelingen (CVDR)", "",
         f"Zoekvraag: `{s.get('cvdr_query', '-')}` → {s.get('cvdr_treffers', 0)} treffers (alle versies).", "",
         "| Status | Titel | Identifier | In werking | Omgevingswet | Kapartikelen | Extract |",
         "|---|---|---|---|---|---|---|"]
    for r in sorted((r for r in recs if r["status"] != "vervallen"), key=lambda r: r["titel"].lower()):
        if r.get("integraal_relevant"):
            art = "integraal"
        elif r.get("relevante_artikelen"):
            art = "; ".join(r["relevante_artikelen"])[:200]
        else:
            art = "—" if r["gedownload"] else "niet gedownload"
        ex = f"[extract](extract/{r['id']}.md)" if r["gedownload"] else ""
        L.append(f"| {r['status']} | [{r['titel']}]({r['url']}) | {r['id']} | {r['inwerkingtreding']} | "
                 f"{r['omgevingswet']} | {art} | {ex} |")
    verv = [r for r in recs if r["status"] == "vervallen"]
    L += ["", f"Vervallen versies in de treffers: {len(verv)} (zie regelingen.jsonl).", ""]

    if pubs or "bekendmakingen_query" in s:
        L += ["## Bekendmakingen sinds 2025 (praktijkcontrole)", "",
              f"Zoekvraag: `{s.get('bekendmakingen_query', '-')}`", "",
              f"Zoekmethode: {s.get('bekendmakingen_zoekmethode', 'titel')}", "",
              f"Totaal: {s.get('bekendmakingen_totaal', 0)} · besluiten: {s['bekendmakingen_besluiten']} · "
              f"aanvragen: {s['bekendmakingen_aanvragen']} · geweigerd (volgens titel): {s['bekendmakingen_geweigerd']}", "",
              f"Steekproef: {sum(1 for p in pubs if p.get('gedownload'))} recente besluiten volledig opgehaald, "
              f"waarvan {s['bekendmakingen_steekproef_met_grondslag']} met een grondslagverwijzing.", ""]
        for p in (p for p in pubs if p.get("gedownload")):
            # Titel bewust weggelaten: die bevat vaak een adres van een particulier.
            L.append(f"### [{p['id']}]({p['url']}) — {p['datum']} — {p['soort']}")
            L.append("")
            for c in p.get("grondslag_citaten") or ["_geen grondslagverwijzing gevonden in de tekst_"]:
                L.append(f"> {c}")
                L.append("")
    L += ["## Niet automatisch opgehaald — handmatig controleren", "",
          "- [ ] Omgevingsplan (tijdelijk deel / regels in DSO, omgevingswet.overheid.nl)",
          "- [ ] Bomenlijst / bomenkaart / register: staan er particuliere bomen op?",
          "- [ ] Gemeentelijke website: beleidsregels herplant/compensatie, handhavingsbeleid",
          ""]
    if s["fouten"]:
        L += ["## Fouten bij ophalen", ""] + [f"- {f}" for f in s["fouten"]] + [""]
    return "\n".join(L)


def safe_process(g: dict, opt: Options) -> dict:
    try:
        return process(g, opt)
    except Exception:  # noqa: BLE001
        return {"gm_code": g["gm_code"], "gemeente": g["gemeente"], "fouten": [traceback.format_exc()]}
