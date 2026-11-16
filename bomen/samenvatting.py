"""Samenvatting en methodologische cijfers uit output/rijen/*.json (INTENT.md, OUTPUT punt 4 en 5).

Schrijft output/samenvatting.md en output/samenvatting.json. Alle getallen in het rapport komen hieruit,
zodat ze na te rekenen zijn. Tellingen van variabelen in de tekstvelden (weigeringsgronden, uitzonderingen)
gebeuren met trefwoorden en zijn daarom indicatief; dat staat ook in de uitvoer.
"""

from __future__ import annotations

import csv
import json
import re
import statistics
from collections import Counter, defaultdict

from .scores import OUTPUT, RIJEN

PROVINCIES = [
    "Groningen",
    "Fryslân",
    "Drenthe",
    "Overijssel",
    "Flevoland",
    "Gelderland",
    "Utrecht",
    "Noord-Holland",
    "Zuid-Holland",
    "Zeeland",
    "Noord-Brabant",
    "Limburg",
]
CATS = ["1 Zeer soepel", "2 Soepel", "3 Gemiddeld", "4 Streng", "5 Zeer streng"]


def _txt(v) -> str:
    if isinstance(v, list):
        return " ".join(str(x) for x in v)
    return str(v or "")


def systeem(x: dict) -> str:
    d = x["D"]["punt"]
    if d == 0:
        return "geen vergunningplicht voor particuliere bomen"
    if x.get("lijstsysteem") and d <= 1:
        return "alleen bomen op een lijst of kaart"
    if x.get("lijstsysteem"):
        return "kaart met gebieden of structuren"
    if x.get("omtrek_cm") is None:
        return "hele kom of gemeente, zonder drempel"
    return "hele kom of gemeente, met drempel"


VARIABELEN = {
    "omtrekdrempel (stamdikte)": lambda x, t: x.get("omtrek_cm") is not None,
    "lijst of kaart met aangewezen bomen": lambda x, t: bool(x.get("lijstsysteem")),
    "tuin- of perceeluitzondering": lambda x, t: bool(
        re.search(
            r"achtertuin|zijtuin|voortuin|niet zichtbaar|tuin\w* (tot|kleiner|van ten hoogste)|percel\w* (tot|kleiner|van ten hoogste)"
            r"|erven en tuinen|tuinen en erven|erf of tuin|van de gevel|uit de gevel|m2|m²",
            t["uitz"],
            re.I,
        )
    ),
    "soortuitzondering (bijv. coniferen, populieren, fruitbomen)": lambda x, t: bool(
        re.search(r"conifer|naaldbo|populier|wilg|fruitbo|vruchtbo|berk|cypres|thuja|leyland", t["uitz"], re.I)
    ),
    "weigeringsgrond natuur of ecologie": lambda x, t: bool(re.search(r"natuur|ecolog", t["weig"], re.I)),
    "weigeringsgrond landschap": lambda x, t: bool(re.search(r"landschap", t["weig"], re.I)),
    "weigeringsgrond cultuurhistorie": lambda x, t: bool(re.search(r"cultuurhistor", t["weig"], re.I)),
    "weigeringsgrond beeld (stads- en dorpsschoon, beeldbepalend)": lambda x, t: bool(
        re.search(r"stads- en dorpsschoon|dorpsschoon|beeldbepal|stedenbouw|esthetis|beeldkwaliteit", t["weig"], re.I)
    ),
    "weigeringsgrond leefbaarheid of recreatie": lambda x, t: bool(
        re.search(r"leefbaar|recreati|leefomgeving", t["weig"], re.I)
    ),
    "weigeringsgrond boomwaarde of monumentaliteit": lambda x, t: bool(
        re.search(r"boomwaarde|monumenta|dendrolog|zeldza|waardevol", t["weig"], re.I)
    ),
    "weigeringsgrond klimaat": lambda x, t: bool(re.search(r"klimaat|hitte|wateroverlast", t["weig"], re.I)),
    "herplant (kan of moet)": lambda x, t: x["H"]["punt"] >= 1,
    "financiële compensatie of boomwaarde": lambda x, t: (
        x.get("herplant_betalen_als_alternatief") in ("kan", "verplicht")
        or bool(re.search(r"boomwaarde|herplantfonds|bomenfonds|groenfonds|compensatiefonds|financi", t["herpl"], re.I))
    ),
    "bestuurlijke boete in de regeling": lambda x, t: x["S"]["punt"] >= 2,
    "apart vastgesteld beleid naast de regeling": lambda x, t: bool(
        re.search(
            r"beleidsregel|beleidsplan|bomenbeleid|beleidsnota|nota |programma|bomenplan|beleidsnotitie|beleidskader",
            t["bron"],
            re.I,
        )
    ),
}


def plaats(x: dict) -> str:
    t = _txt(x.get("juridische_plaats")).lower()
    if x["D"]["punt"] == 0:
        return "geen vergunningplicht voor particuliere bomen"
    if "bestemmingsplan" in t[:200] and (t.startswith("onzeker") or t.startswith("chw")):
        return "omgevingsplan (tijdelijk deel: bestemmingsplan)"
    if t.startswith("onzeker") or not t:
        return "onzeker"
    if t.startswith("omgevingsplan") or t.startswith("chw"):
        return "omgevingsplan"
    if t.startswith("vfl") or t.startswith("vlmd") or "fysieke leefomgeving" in t[:80] or "leefomgeving" in t[:60]:
        return "verordening fysieke leefomgeving (VFL)"
    if "apv" in t[:40] or "plaatselijke verordening" in t[:80]:
        return "APV"
    if "verordening" in t[:80]:
        return "losse bomen- of kapverordening"
    return "overig"


def buren() -> dict[str, set[str]]:
    from .kaart import grenzen

    gj = grenzen("wgs84")
    punten: dict[tuple, set[str]] = defaultdict(set)
    for f in gj["features"]:
        code = f["properties"].get("statcode") or f["properties"].get("code")
        geom = f["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for p in polys:
            for ring in p:
                for xy in ring:
                    punten[(round(xy[0], 5), round(xy[1], 5))].add(code)
    paren: Counter = Counter()
    for codes in punten.values():
        if 1 < len(codes) < 4:
            cs = sorted(codes)
            for i in range(len(cs)):
                for j in range(i + 1, len(cs)):
                    paren[(cs[i], cs[j])] += 1
    nb: dict[str, set[str]] = defaultdict(set)
    for (a, b), n in paren.items():
        if n >= 2:
            nb[a].add(b)
            nb[b].add(a)
    return nb


def maak() -> dict:
    rijen = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(RIJEN.glob("GM*.json"))]
    csvr = {
        r["CBS-code"]: r for r in csv.DictReader((OUTPUT / "alle_gemeenten.csv").open(encoding="utf-8"), delimiter=";")
    }
    for x in rijen:
        c = csvr[x["gm_code"]]
        x["_s"] = int(c["strengheid"])
        x["_cat"] = c["categorie"]
        x["_bereik"] = c["bereik"]
        x["_betr"] = c["betrouwbaarheid"]
        x["_grens"] = c.get("bereik over categoriegrens", "")
    n = len(rijen)
    S: dict = {"aantal": n}
    S["categorie"] = Counter(x["_cat"] for x in rijen)
    S["categorie_per_provincie"] = {p: Counter(x["_cat"] for x in rijen if x["provincie"] == p) for p in PROVINCIES}
    S["betrouwbaarheid"] = Counter(x["_betr"] for x in rijen)
    S["status"] = Counter(x["status"] for x in rijen)
    ordered = sorted(rijen, key=lambda x: (-x["_s"], -x["D"]["punt"], x.get("omtrek_cm") or 999))
    S["strengst"] = [(x["gemeente"], x["provincie"], x["_s"], x["_bereik"]) for x in ordered[:10]]
    S["soepelst"] = [
        (x["gemeente"], x["provincie"], x["_s"], x["_bereik"])
        for x in sorted(rijen, key=lambda x: (x["_s"], x["D"]["punt"]))[:10]
    ]
    S["score_nul"] = sorted(x["gemeente"] for x in rijen if x["_s"] == 0)
    S["gemiddelde_per_provincie"] = {
        p: round(statistics.mean(x["_s"] for x in rijen if x["provincie"] == p), 1) for p in PROVINCIES
    }
    S["systeem"] = Counter(systeem(x) for x in rijen)
    S["systeem_per_provincie"] = {p: Counter(systeem(x) for x in rijen if x["provincie"] == p) for p in PROVINCIES}
    breed = [x for x in rijen if systeem(x) == "hele kom of gemeente, met drempel"]
    om = sorted(float(x["omtrek_cm"]) for x in breed)
    S["drempel"] = {
        "aantal": len(om),
        "min": min(om),
        "max": max(om),
        "mediaan": statistics.median(om),
        "kwartielen": [round(q, 1) for q in statistics.quantiles(om, n=4)],
        "klassen": {
            "onder 60 cm": sum(o < 60 for o in om),
            "60 tot 100 cm": sum(60 <= o <= 100 for o in om),
            "boven 100 cm": sum(o > 100 for o in om),
        },
    }
    S["drempel_laagst"] = [(x["gemeente"], x["omtrek_cm"]) for x in sorted(breed, key=lambda x: x["omtrek_cm"])[:5]]
    S["drempel_hoogst"] = [(x["gemeente"], x["omtrek_cm"]) for x in sorted(breed, key=lambda x: -x["omtrek_cm"])[:5]]
    for boom in ("boom_a_80cm", "boom_b_40cm"):
        S[boom] = Counter(x[boom] for x in rijen)
        S[boom + "_per_provincie"] = {p: Counter(x[boom] for x in rijen if x["provincie"] == p) for p in PROVINCIES}
    lijst = [x for x in rijen if x.get("lijstsysteem")]
    S["lijst"] = {
        "lijstsystemen": len(lijst),
        "ingezien": sum(1 for x in lijst if x.get("lijst_ingezien")),
        "niet_ingezien": sum(1 for x in lijst if not x.get("lijst_ingezien")),
        "met_aantal_particulier": sum(1 for x in lijst if x.get("lijst_aantal_particulier") is not None),
    }
    S["lijst_aantallen"] = sorted(
        [
            (
                x["gemeente"],
                x["provincie"],
                x.get("lijst_aantal_totaal"),
                x["lijst_aantal_particulier"],
                bool(x.get("lijst_ingezien")),
            )
            for x in lijst
            if x.get("lijst_aantal_particulier") is not None
        ],
        key=lambda t: -t[3],
    )
    for k in (
        "herplant_type",
        "herplant_betalen_als_alternatief",
        "herplant_na_illegale_kap",
        "herplant_niet_nakomen_type",
    ):
        S[k] = Counter(x.get(k) for x in rijen)
    S["herplant_type_per_provincie"] = {
        p: Counter(x["herplant_type"] for x in rijen if x["provincie"] == p) for p in PROVINCIES
    }
    S["H"] = Counter(x["H"]["punt"] for x in rijen)
    S["W"] = Counter(x["W"]["punt"] for x in rijen)
    S["S"] = Counter(x["S"]["punt"] for x in rijen)
    S["D"] = Counter(x["D"]["punt"] for x in rijen)
    var = {}
    for naam, f in VARIABELEN.items():
        tel = Counter()
        for x in rijen:
            t = {
                "uitz": _txt(x.get("uitzonderingen")) + " " + _txt(x.get("reikwijdte")),
                "weig": _txt(x.get("weigeringsgronden")),
                "herpl": _txt(x.get("herplantplicht")),
                "bron": _txt(x.get("brondocument")),
            }
            if x["D"]["punt"] > 0 and f(x, t):
                tel[x["provincie"]] += 1
        var[naam] = {"totaal": sum(tel.values()), **{p: tel[p] for p in PROVINCIES}}
    S["variabelen"] = var
    S["met_kapregel"] = sum(1 for x in rijen if x["D"]["punt"] > 0)
    S["juridische_plaats"] = Counter(plaats(x) for x in rijen)
    S["restant_bruidsschat"] = sorted(
        x["gemeente"]
        for x in rijen
        if "bruidsschat" in _txt(x.get("juridische_plaats")).lower() and x["D"]["punt"] == 0
    )
    S["s_via_omgevingswet"] = sum(
        1
        for x in rijen
        if x["S"]["punt"] >= 1
        and re.search(r"via (de )?(Ow|Omgevingswet)|omgevingsplanactiviteit", _txt(x.get("sancties")), re.I)
    )
    S["apv_na_2024"] = sum(1 for x in rijen if plaats(x) == "APV")
    S["volledig_gelezen"] = Counter(bool(x.get("volledig_gelezen")) for x in rijen)
    S["grensoverschrijdend_bereik"] = sum(1 for x in rijen if x["_grens"] == "ja")
    # buurgemeenten met het grootste verschil in voorbeeldboom A of strengheid
    try:
        nb = buren()
    except Exception:  # noqa: BLE001 - kaartbestand niet beschikbaar
        nb = {}
    byc = {x["gm_code"]: x for x in rijen}
    paren = []
    for a, bs in nb.items():
        for b in bs:
            if a < b and a in byc and b in byc:
                xa, xb = byc[a], byc[b]
                paren.append(
                    (
                        abs(xa["_s"] - xb["_s"]),
                        xa["gemeente"],
                        xa["_s"],
                        xa["boom_a_80cm"],
                        xa.get("omtrek_cm"),
                        xb["gemeente"],
                        xb["_s"],
                        xb["boom_a_80cm"],
                        xb.get("omtrek_cm"),
                    )
                )
    paren.sort(reverse=True)
    S["buren_grootste_verschil"] = paren[:20]
    S["buren_boom_a_ja_nee"] = [p for p in paren if {p[3], p[7]} == {"ja", "nee"}][:20]
    return S


def schrijf() -> None:
    S = maak()
    (OUTPUT / "samenvatting.json").write_text(
        json.dumps(S, ensure_ascii=False, indent=1, default=list) + "\n", encoding="utf-8"
    )
    L = [
        "# Samenvatting kapregels particuliere bomen, alle gemeenten",
        "",
        f"Gegenereerd met `python3 -m bomen samenvatting` uit {S['aantal']} rijen in `output/rijen/` "
        "(peildata 14 t/m 16 november 2026). Tellingen in tekstvelden zijn op trefwoord en indicatief.",
        "",
    ]

    def tabel(kop, rijen):
        out = ["| " + " | ".join(kop) + " |", "|" + "---|" * len(kop)]
        out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rijen]
        return out + [""]

    L += ["## Verdeling over de categorieën", ""] + tabel(
        ["Categorie", "Aantal"], [(c, S["categorie"][c]) for c in CATS]
    )
    L += ["## Per provincie", ""] + tabel(
        ["Provincie", "Gemeenten", *CATS, "Gem. score"],
        [
            (
                p,
                sum(S["categorie_per_provincie"][p].values()),
                *[S["categorie_per_provincie"][p][c] for c in CATS],
                S["gemiddelde_per_provincie"][p],
            )
            for p in PROVINCIES
        ],
    )
    L += ["## Tien strengste gemeenten", ""] + tabel(["Gemeente", "Provincie", "Score", "Bereik"], S["strengst"])
    L += ["## Soepelste gemeenten", "", f"Score 0 ({len(S['score_nul'])}): " + ", ".join(S["score_nul"]), ""]
    L += tabel(["Gemeente", "Provincie", "Score", "Bereik"], S["soepelst"])
    L += ["## Systemen", ""] + tabel(["Systeem", "Aantal"], S["systeem"].most_common())
    d = S["drempel"]
    L += [
        "## Drempels (hele kom of gemeente, met drempel)",
        "",
        f"{d['aantal']} gemeenten. Laagste {d['min']} cm, hoogste {d['max']} cm, mediaan {d['mediaan']} cm, "
        f"kwartielen {d['kwartielen']}.",
        "",
    ] + tabel(["Klasse (stamomtrek)", "Aantal"], d["klassen"].items())
    for boom, naam in (("boom_a_80cm", "Voorbeeldboom A (80 cm)"), ("boom_b_40cm", "Voorbeeldboom B (40 cm)")):
        vals = ["ja", "melden", "alleen als op lijst", "nee", "onbekend"]
        L += [f"## {naam}", ""] + tabel(
            ["Provincie", *vals],
            [(p, *[S[boom + "_per_provincie"][p][v] for v in vals]) for p in PROVINCIES]
            + [("Totaal", *[S[boom][v] for v in vals])],
        )
    L += ["## Lijstsystemen", "", json.dumps(S["lijst"], ensure_ascii=False), ""]
    L += tabel(["Gemeente", "Provincie", "Lijst totaal", "Particulier", "Lijst ingezien"], S["lijst_aantallen"])
    L += ["## Herplant", ""]
    for k in (
        "herplant_type",
        "herplant_betalen_als_alternatief",
        "herplant_na_illegale_kap",
        "herplant_niet_nakomen_type",
    ):
        L += [f"### {k}", ""] + tabel(["Waarde", "Aantal"], S[k].most_common())
    L += [
        "## Variabelen in het kapbeleid (gemeenten met een kapregel)",
        "",
        f"Basis: {S['met_kapregel']} gemeenten met D > 0. Trefwoordtelling, indicatief.",
        "",
    ]
    L += tabel(
        ["Variabele", "Totaal", *PROVINCIES],
        [(k, v["totaal"], *[v[p] for p in PROVINCIES]) for k, v in S["variabelen"].items()],
    )
    L += ["## Methode", "", "### Juridische plaats", ""] + tabel(
        ["Plaats", "Aantal"], S["juridische_plaats"].most_common()
    )
    L += [
        f"- Restant bruidsschat zonder vergunningplicht: {len(S['restant_bruidsschat'])} ({', '.join(S['restant_bruidsschat'])})",
        f"- S = 1 via de Omgevingswet (omgevingsplanactiviteit) genoemd: {S['s_via_omgevingswet']}",
        f"- Kapregel staat op de peildatum nog in de APV (na de start van de Omgevingswet op 1-1-2024): {S['apv_na_2024']}",
        f"- Volledige artikeltekst gelezen: {S['volledig_gelezen'][True]} van {S['aantal']}",
        f"- Bereik over een categoriegrens: {S['grensoverschrijdend_bereik']}",
        f"- Betrouwbaarheid: {dict(S['betrouwbaarheid'])}; status: {dict(S['status'])}",
        "",
    ]
    L += ["## Buurgemeenten met het grootste verschil", ""] + tabel(
        ["Verschil", "Gemeente", "Score", "Boom A", "Drempel", "Buurgemeente", "Score", "Boom A", "Drempel"],
        S["buren_grootste_verschil"],
    )
    L += ["### Buren waar boom A in de ene wel en in de andere geen vergunning nodig heeft", ""] + tabel(
        ["Verschil", "Gemeente", "Score", "Boom A", "Drempel", "Buurgemeente", "Score", "Boom A", "Drempel"],
        S["buren_boom_a_ja_nee"],
    )
    (OUTPUT / "samenvatting.md").write_text("\n".join(L), encoding="utf-8")
    print("output/samenvatting.md en output/samenvatting.json geschreven")
