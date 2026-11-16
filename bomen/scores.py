"""Van bevindingen per gemeente (output/rijen/<GM-code>.json) naar CSV en afwijkingenlijst.

De onderzoeker (of een agent) legt per gemeente de bevindingen en de deelscores
D, W, H en S vast in JSON. Deze module rekent I, strengheid, bereik, categorie en
betrouwbaarheid uit volgens INTENT.md, zodat er geen rekenfouten in de CSV komen.

JSON-velden per gemeente (alle tekstvelden in het Nederlands):
  gm_code, gemeente, provincie,
  brondocument, url, datum_geldigheid, laatste_wijziging, juridische_plaats, praktijkcontrole,
  vergunningplicht, drempel, omtrek_cm (getal of null), meethoogte, reikwijdte, uitzonderingen,
  weigeringsgronden, herplantplicht, herplant_ontsnapping, sancties, procedure,
  herplant_type: "harde plicht" | "in beginsel/tenzij" | "kan" | "geen grondslag"
  herplant_betalen_als_alternatief: "verplicht" | "kan" | "nee" | "onbekend"
  herplant_na_illegale_kap: "verplicht" | "kan" | "nee" | "onbekend"
  herplant_niet_nakomen: tekst met letterlijk citaat (gevolg als een opgelegde herplantplicht niet wordt nagekomen)
  herplant_niet_nakomen_type: "strafbaar (rechter)" | "bestuurlijke boete" | "dwangsom/bestuursdwang" |
                              "meerdere" | "niets geregeld" | "onbekend"
  boom_a_80cm, boom_b_40cm: "ja" | "melden" | "nee" | "alleen als op lijst" | "onbekend"
      (vergunning nodig voor gezonde boom in particuliere achtertuin binnen de bebouwde kom,
       stamomtrek 80 resp. 40 cm op 1,30 m; geen fruitboom, conifeer, populier of wilg)
  D, W, H, S: {"punt": int, "min": int, "max": int}
  volledig_gelezen: bool       (volledige artikeltekst zelf gelezen)
  lijstsysteem: bool, lijst_ingezien: bool | null, particuliere_bomen_op_lijst: "ja" | "nee" | "onbekend" | null
  lijst_aantal_totaal, lijst_aantal_particulier: int | null  (alleen als de lijst is ingezien; anders null)
  lijst_telling: str  (eenheid en bron van de telling, bijv. "regels op de lijst (website, 2026)"; "ca." als benaderd)
  status: "ok" | "onzeker" | "niet gevonden", ontbrekend: str
  artikelnummers, opmerkingen, modelsignalen: [str]
"""

from __future__ import annotations

import csv
import re
import json
import math
from pathlib import Path

from .http import ROOT
from .pipeline import slug

OUTPUT = ROOT / "output"
RIJEN = OUTPUT / "rijen"

CATEGORIEEN = [(80, "5 Zeer streng"), (60, "4 Streng"), (40, "3 Gemiddeld"), (20, "2 Soepel"), (0, "1 Zeer soepel")]
HERPLANT_TYPES = {"harde plicht", "in beginsel/tenzij", "kan", "geen grondslag"}
DRIEWAARDEN = {"verplicht", "kan", "nee", "onbekend"}
# output/rijen/ wordt openbaar: geen adressen van particulieren (straat + huisnummer, postcode).
ADRES = re.compile(r"\b[A-Z][\w'.-]*(?:[ -][A-Za-z][\w'.-]*){0,3}?(?:straat|weg|laan|plein|dijk|pad|singel|kade|"
                   r"gracht|hof|dreef|steeg|veld|park|wei|baan|ring|markt|haven|polder|"
                   r"plaats|plantsoen|erf|akker|kamp|zoom|hoek|wal)\s+\d+[a-zA-Z]?(?:[-–]\d+)?\b"
                   r"|\b\d{4}\s?[A-Z]{2}\b")
VOORBEELDBOOM = {"ja", "melden", "nee", "alleen als op lijst", "onbekend"}
NIET_NAKOMEN = {"strafbaar (rechter)", "bestuurlijke boete", "dwangsom/bestuursdwang", "meerdere",
                "niets geregeld", "onbekend"}

KOLOMMEN = [
    ("gemeente", "gemeente"), ("provincie", "provincie"), ("CBS-code", "gm_code"),
    ("brondocument", "brondocument"), ("URL", "url"), ("datum geldigheid", "datum_geldigheid"),
    ("laatste wijziging", "laatste_wijziging"), ("juridische plaats", "juridische_plaats"),
    ("praktijkcontrole", "praktijkcontrole"), ("vergunningplicht", "vergunningplicht"),
    ("drempel", "drempel"), ("omtrek (cm)", "omtrek_cm"), ("meethoogte", "meethoogte"),
    ("reikwijdte", "reikwijdte"), ("uitzonderingen", "uitzonderingen"),
    ("vergunning boom A (80 cm)", "boom_a_80cm"), ("vergunning boom B (40 cm)", "boom_b_40cm"),
    ("bomenlijst totaal", "lijst_aantal_totaal"), ("bomenlijst particulier", "lijst_aantal_particulier"),
    ("bomenlijst telling", "lijst_telling"),
    ("weigeringsgronden", "weigeringsgronden"), ("herplantplicht", "herplantplicht"),
    ("herplant ontsnapping", "herplant_ontsnapping"), ("herplant niet nakomen", "herplant_niet_nakomen"),
    ("sancties", "sancties"), ("procedure", "procedure"),
    ("D", "_D"), ("W", "_W"), ("H", "_H"), ("S", "_S"), ("I", "_I"), ("strengheid", "_strengheid"),
    ("bereik", "_bereik"), ("categorie", "_categorie"), ("bereik over categoriegrens", "_grens"),
    ("betrouwbaarheid", "_betrouwbaarheid"), ("artikelnummers", "artikelnummers"),
    ("opmerkingen", "opmerkingen"),
]


def strengheid(d: int, i: int) -> int:
    v = d / 4 * (40 + 60 * i / 9)
    return int(math.floor(v + 0.5))  # gewoon afronden (0,5 omhoog), niet bankiers-afronding


def categorie(score: int) -> str:
    return next(naam for grens, naam in CATEGORIEEN if score >= grens)


def _check(r: dict) -> list[str]:
    fout = []
    for k, (lo, hi) in {"D": (0, 4), "W": (0, 3), "H": (0, 3), "S": (0, 3)}.items():
        v = r.get(k)
        if not isinstance(v, dict) or not all(isinstance(v.get(x), int) for x in ("punt", "min", "max")):
            fout.append(f"{k} ontbreekt of is geen {{punt,min,max}}")
            continue
        if not (lo <= v["min"] <= v["punt"] <= v["max"] <= hi):
            fout.append(f"{k} ongeldig: {v}")
    if r.get("herplant_type") not in HERPLANT_TYPES:
        fout.append(f"herplant_type ongeldig: {r.get('herplant_type')!r}")
    for k in ("herplant_betalen_als_alternatief", "herplant_na_illegale_kap"):
        if r.get(k) not in DRIEWAARDEN:
            fout.append(f"{k} ongeldig: {r.get(k)!r}")
    if r.get("herplant_niet_nakomen_type") not in NIET_NAKOMEN:
        fout.append(f"herplant_niet_nakomen_type ongeldig: {r.get('herplant_niet_nakomen_type')!r}")
    for k in ("boom_a_80cm", "boom_b_40cm"):
        if r.get(k) not in VOORBEELDBOOM:
            fout.append(f"{k} ongeldig: {r.get(k)!r}")
    for k in ("lijst_aantal_totaal", "lijst_aantal_particulier"):
        v = r.get(k)
        if v is not None and (not isinstance(v, int) or isinstance(v, bool) or v < 0):
            fout.append(f"{k} moet een geheel getal of null zijn: {v!r}")
    if isinstance(r.get("lijst_aantal_totaal"), int) and isinstance(r.get("lijst_aantal_particulier"), int) \
            and r["lijst_aantal_particulier"] > r["lijst_aantal_totaal"]:
        fout.append("lijst_aantal_particulier is groter dan lijst_aantal_totaal")
    for k, v in r.items():
        if k != "url" and isinstance(v, str) and ADRES.search(v):
            fout.append(f"{k} bevat mogelijk een adres ({ADRES.search(v).group(0)!r}); vervang door [adres]")
    if r.get("status") not in ("ok", "onzeker", "niet gevonden"):
        fout.append(f"status ongeldig: {r.get('status')!r}")
    return fout


def bereken(r: dict) -> dict:
    p = {k: r[k]["punt"] for k in "DWHS"}
    lo = {k: r[k]["min"] for k in "DWHS"}
    hi = {k: r[k]["max"] for k in "DWHS"}
    i_p, i_lo, i_hi = (x["W"] + x["H"] + x["S"] for x in (p, lo, hi))
    s_p, s_lo, s_hi = strengheid(p["D"], i_p), strengheid(lo["D"], i_lo), strengheid(hi["D"], i_hi)
    grens = categorie(s_lo) != categorie(s_hi)
    if lo["D"] != hi["D"]:
        betr = "laag"
    elif r.get("volledig_gelezen") and not grens:
        betr = "hoog"
    else:
        betr = "middel"
    fmt = lambda k: str(p[k]) if lo[k] == hi[k] else f"{p[k]} ({lo[k]}-{hi[k]})"  # noqa: E731
    out = dict(r)
    out.update({
        "_D": fmt("D"), "_W": fmt("W"), "_H": fmt("H"), "_S": fmt("S"),
        "_I": str(i_p) if i_lo == i_hi else f"{i_p} ({i_lo}-{i_hi})",
        "_strengheid": s_p, "_strengheid_min": s_lo, "_strengheid_max": s_hi,
        "_bereik": f"{s_lo}-{s_hi}", "_categorie": categorie(s_p),
        "_grens": "ja" if grens else "nee", "_betrouwbaarheid": betr,
    })
    return out


def laad(provincies: list[str] | None = None) -> tuple[list[dict], list[str]]:
    rows, problemen = [], []
    for f in sorted(RIJEN.glob("GM*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        if provincies and slug(r.get("provincie", "")) not in {slug(p) for p in provincies}:
            continue
        fout = _check(r)
        if fout:
            problemen.append(f"{f.name}: " + "; ".join(fout))
            continue
        rows.append(bereken(r))
    return rows, problemen


def sorteer(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (-r["_strengheid"], -r["D"]["punt"],
                                       r.get("omtrek_cm") if isinstance(r.get("omtrek_cm"), (int, float)) else 9999,
                                       r["gemeente"].lower()))


def schrijf_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
        w.writerow([k for k, _ in KOLOMMEN])
        for r in rows:
            w.writerow(["" if r.get(v) is None else r.get(v) for _, v in KOLOMMEN])


def schrijf_afwijkingen(rows: list[dict], titel: str, path: Path) -> None:
    lijst_niet = [r for r in rows if r.get("lijstsysteem") and not r.get("lijst_ingezien")]
    overig = [r for r in rows if r not in lijst_niet
              and (r["status"] != "ok" or r["_betrouwbaarheid"] == "laag")]
    grens = [r for r in rows if r["_grens"] == "ja"]
    L = [f"# Afwijkingen — {titel}", "",
         f"{len(rows)} gemeenten gescoord. Hieronder staan de gemeenten met status \"niet gevonden\" of "
         f"\"onzeker\", of met betrouwbaarheid \"laag\".", ""]
    L += ["## Lijstsystemen waarvan de lijst niet is ingezien", ""]
    L += [f"- **{r['gemeente']}** ({r['gm_code']}): {r.get('ontbrekend') or 'lijst niet ingezien'}" for r in lijst_niet] or ["Geen."]
    L += ["", "## Overige afwijkingen", ""]
    L += [f"- **{r['gemeente']}** ({r['gm_code']}), status {r['status']}, betrouwbaarheid "
          f"{r['_betrouwbaarheid']}: {r.get('ontbrekend') or '-'}" for r in overig] or ["Geen."]
    L += ["", "## Bereik loopt over een categoriegrens", ""]
    L += [f"- {r['gemeente']}: {r['_strengheid']} ({r['_categorie']}), bereik {r['_bereik']}" for r in grens] or ["Geen."]
    sig = [(r["gemeente"], s) for r in rows for s in r.get("modelsignalen") or []]
    L += ["", "## Modelsignalen", ""]
    L += [f"- {g}: {s}" for g, s in sig] or ["Geen."]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
