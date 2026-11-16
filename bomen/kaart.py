"""Kaarten van Nederland per gemeente.

Maakt uit output/rijen/*.json:
  output/kaart_boom_a.svg      vergunning nodig voor voorbeeldboom A (80 cm stamomtrek)?
  output/kaart_boom_b.svg      idem voor voorbeeldboom B (40 cm)
  output/kaart_strengheid.svg  strengheidscategorie
  output/kaart.geojson         alle gegevens samen (gekleurd naar boom A)
  output/kaart_*.geojson       per thema gekleurd; GitHub toont elk bestand als interactieve kaart

Gemeentegrenzen: CBS-gebiedsindeling 2026 via PDOK (gegeneraliseerd), in RD-coördinaten
(EPSG:28992) voor de SVG's en in WGS84 voor de GeoJSON.
"""

from __future__ import annotations

import json
from collections import Counter
from html import escape

from .http import DATA, ROOT, fetch
from .scores import laad

PDOK = ("https://service.pdok.nl/cbs/gebiedsindelingen/2026/wfs/v1_0?request=GetFeature&service=WFS"
        "&version=2.0.0&typeName=gebiedsindelingen:gemeente_gegeneraliseerd&outputFormat=application/json")
OUTPUT = ROOT / "output"

# Eén tint (blauw), licht → donker = minder → meer bescherming. Gevalideerd als ordinale reeks.
SURFACE = "#fcfcfb"
INK, INK2 = "#0b0b0b", "#52514e"
ONBEKEND = "#b9b8b3"      # met arcering, zodat het niet alleen op kleur leunt
NIET_GESCOORD = "#e9e7e1"

BOOM_KLASSEN = [  # (waarde, label, kleur)
    ("ja", "Vergunning nodig", "#184f95"),
    ("melden", "Melden (gemeente kan verbieden)", "#2a6bc0"),
    ("alleen als op lijst", "Alleen als de boom op de bomenlijst staat", "#3987e5"),
    ("nee", "Geen vergunning nodig", "#86b6ef"),
    ("onbekend", "Onbekend", ONBEKEND),
    (None, "Nog niet onderzocht", NIET_GESCOORD),
]
CAT_KLASSEN = [
    ("5 Zeer streng", "5 Zeer streng (80–100)", "#104281"),
    ("4 Streng", "4 Streng (60–79)", "#1c5cab"),
    ("3 Gemiddeld", "3 Gemiddeld (40–59)", "#2a78d6"),
    ("2 Soepel", "2 Soepel (20–39)", "#5598e7"),
    ("1 Zeer soepel", "1 Zeer soepel (0–19)", "#86b6ef"),
    (None, "Nog niet onderzocht", NIET_GESCOORD),
]


def grenzen(crs: str) -> dict:
    raw = DATA / "raw" / "pdok"
    if crs == "rd":
        body = fetch(PDOK, raw / "gemeenten_2026_rd.json", context="pdok")
    else:
        body = fetch(PDOK + "&srsName=EPSG:4326", raw / "gemeenten_2026_wgs84.json", context="pdok")
    return json.loads(body)


def _polygons(geom: dict):
    if geom["type"] == "Polygon":
        yield geom["coordinates"]
    else:
        yield from geom["coordinates"]


def _path(geom: dict, tx) -> str:
    parts = []
    for poly in _polygons(geom):
        for ring in poly:
            pts, last = [], None
            for x, y in ring:
                p = tx(x, y)
                if p != last:
                    pts.append(p)
                    last = p
            if len(pts) >= 3:
                parts.append("M" + "L".join(f"{a:g},{b:g}" for a, b in pts) + "Z")
    return "".join(parts)


def _svg(feats: list, waarde_van, klassen: list, titel: str, subtitel: str, tooltip) -> str:
    W, H_MAP, LEG_W = 520, 600, 300
    xs = [x for f in feats for poly in _polygons(f["geometry"]) for ring in poly for x, _ in ring]
    ys = [y for f in feats for poly in _polygons(f["geometry"]) for ring in poly for _, y in ring]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = min((W - 20) / (x1 - x0), (H_MAP - 20) / (y1 - y0))
    top = 70

    def tx(x, y):  # RD → pixels, noorden boven; afgerond op 0,5 px
        return (round((10 + (x - x0) * s) * 2) / 2, round((top + 10 + (y1 - y) * s) * 2) / 2)

    kleur = {k[0]: k[2] for k in klassen}
    tel = Counter(waarde_van(f) for f in feats)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + LEG_W} {top + H_MAP + 30}" '
           f'font-family="system-ui,-apple-system,Segoe UI,Roboto,sans-serif" role="img" aria-labelledby="t d">',
           f'<title id="t">{escape(titel)}</title><desc id="d">{escape(subtitel)}</desc>',
           '<defs><pattern id="arcering" width="6" height="6" patternUnits="userSpaceOnUse" '
           f'patternTransform="rotate(45)"><rect width="6" height="6" fill="{ONBEKEND}"/>'
           f'<line x1="0" y1="0" x2="0" y2="6" stroke="{SURFACE}" stroke-width="2"/></pattern></defs>',
           f'<rect width="100%" height="100%" fill="{SURFACE}"/>',
           f'<text x="10" y="28" font-size="20" font-weight="600" fill="{INK}">{escape(titel)}</text>',
           f'<text x="10" y="50" font-size="13" fill="{INK2}">{escape(subtitel)}</text>',
           f'<g stroke="{SURFACE}" stroke-width="0.6" stroke-linejoin="round">']
    for f in sorted(feats, key=lambda f: f["properties"]["statcode"]):
        v = waarde_van(f)
        fill = "url(#arcering)" if v == "onbekend" else kleur.get(v, NIET_GESCOORD)
        out.append(f'<path d="{_path(f["geometry"], tx)}" fill="{fill}">'
                   f'<title>{escape(tooltip(f))}</title></path>')
    out.append("</g>")
    ly = top + 20
    out.append(f'<text x="{W + 10}" y="{ly}" font-size="13" font-weight="600" fill="{INK}">Legenda (aantal gemeenten)</text>')
    for i, (v, label, c) in enumerate(klassen):
        y = ly + 18 + i * 26
        fill = "url(#arcering)" if v == "onbekend" else c
        out.append(f'<rect x="{W + 10}" y="{y}" width="16" height="16" rx="3" fill="{fill}"/>')
        out.append(f'<text x="{W + 34}" y="{y + 12.5}" font-size="12.5" fill="{INK}">{escape(label)} '
                   f'<tspan fill="{INK2}">({tel.get(v, 0)})</tspan></text>')
    out.append(f'<text x="10" y="{top + H_MAP + 20}" font-size="11" fill="{INK2}">Bron: eigen onderzoek naar '
               f'gemeentelijke regelgeving (CVDR); grenzen: CBS/PDOK gebiedsindeling 2026.</text>')
    out.append("</svg>")
    return "\n".join(out)


def maak_kaarten() -> list[str]:
    rows, problemen = laad()
    for p in problemen:
        print(f"  ONGELDIG (niet op kaart): {p}")
    per_gm = {r["gm_code"]: r for r in rows}
    rd = grenzen("rd")["features"]
    n = len(per_gm)
    peil = "peildatum regelgeving 14 t/m 16 november 2026"
    sub = f"{n} van {len(rd)} gemeenten onderzocht · {peil}"

    def boom(key):
        return lambda f: per_gm.get(f["properties"]["statcode"], {}).get(key)

    def tip(key, label):
        def t(f):
            r = per_gm.get(f["properties"]["statcode"])
            naam = f["properties"]["statnaam"]
            if not r:
                return f"{naam}: nog niet onderzocht"
            return f"{naam}: {label} {r.get(key)} (strengheid {r['_strengheid']}, {r['_categorie']})"
        return t

    files = {
        "kaart_boom_a.svg": _svg(rd, boom("boom_a_80cm"), BOOM_KLASSEN,
                                 "Vergunning nodig voor een tuinboom van 80 cm stamomtrek?",
                                 sub, tip("boom_a_80cm", "vergunning nodig:")),
        "kaart_boom_b.svg": _svg(rd, boom("boom_b_40cm"), BOOM_KLASSEN,
                                 "Vergunning nodig voor een tuinboom van 40 cm stamomtrek?",
                                 sub, tip("boom_b_40cm", "vergunning nodig:")),
        "kaart_strengheid.svg": _svg(rd, boom("_categorie"), CAT_KLASSEN,
                                     "Strengheid van de kapregels voor particulier terrein",
                                     sub, tip("_categorie", "categorie")),
    }
    OUTPUT.mkdir(exist_ok=True)
    for name, svg in files.items():
        (OUTPUT / name).write_text(svg, encoding="utf-8")

    # GeoJSON: GitHub toont dit als interactieve kaart; eigenschappen verschijnen bij klikken.
    # Kleuren volgen de simplestyle-spec (fill, stroke), die GitHub overneemt.
    kleur_a = {k[0]: k[2] for k in BOOM_KLASSEN}
    kleur_cat = {k[0]: k[2] for k in CAT_KLASSEN}
    thema = {
        "kaart.geojson": (lambda r: kleur_a.get(r["boom_a_80cm"] if r else None, NIET_GESCOORD), True),
        "kaart_boom_a.geojson": (lambda r: kleur_a.get(r["boom_a_80cm"] if r else None, NIET_GESCOORD), False),
        "kaart_boom_b.geojson": (lambda r: kleur_a.get(r["boom_b_40cm"] if r else None, NIET_GESCOORD), False),
        "kaart_strengheid.geojson": (lambda r: kleur_cat.get(r["_categorie"] if r else None, NIET_GESCOORD), False),
    }

    def kort(t, n=240):
        t = " ".join(t) if isinstance(t, list) else str(t or "")
        return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"

    wgs = grenzen("wgs84")["features"]
    geoms = {f["properties"]["statcode"]: json.loads(json.dumps(f["geometry"]),
                                                     parse_float=lambda s: round(float(s), 5)) for f in wgs}
    for naam, (kleur, volledig) in thema.items():
        feats = []
        for f in wgs:
            code = f["properties"]["statcode"]
            r = per_gm.get(code)
            props = {"gemeente": f["properties"]["statnaam"], "CBS-code": code}
            if r:
                props.update({
                    "provincie": r["provincie"],
                    "vergunning boom A (80 cm)": r["boom_a_80cm"],
                    "vergunning boom B (40 cm)": r["boom_b_40cm"],
                    "drempel": r.get("drempel") if volledig else kort(r.get("drempel")),
                    "herplant": r.get("herplant_type"),
                    "strengheid": r["_strengheid"], "bereik": r["_bereik"], "categorie": r["_categorie"],
                    "betrouwbaarheid": r["_betrouwbaarheid"],
                    "brondocument": r.get("brondocument") if volledig else kort(r.get("brondocument"), 160),
                    "bron": r.get("url"),
                })
                if volledig:
                    props["herplantplicht"] = r.get("herplantplicht")
            else:
                props["status"] = "nog niet onderzocht"
            props.update({"fill": kleur(r), "fill-opacity": 0.85, "stroke": "#ffffff", "stroke-width": 0.5})
            feats.append({"type": "Feature", "properties": props, "geometry": geoms[code]})
        (OUTPUT / naam).write_text(
            json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
    # Compacte data voor de interactieve kaartpagina (docs/index.html, GitHub Pages vanuit /docs).
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    feats = []
    for f in wgs:
        code = f["properties"]["statcode"]
        r = per_gm.get(code)
        geom = json.loads(json.dumps(f["geometry"]), parse_float=lambda s: round(float(s), 4))
        props = {"n": f["properties"]["statnaam"], "c": code}
        if r:
            props.update({"p": r["provincie"], "a": r["boom_a_80cm"], "b": r["boom_b_40cm"],
                          "s": r["_strengheid"], "r": r["_bereik"], "k": r["_categorie"],
                          "t": r["_betrouwbaarheid"], "d": kort(r.get("drempel"), 200),
                          "h": r.get("herplant_type"), "q": kort(r.get("brondocument"), 160),
                          "u": (r.get("url") or "").split(" ;")[0].strip()})
        feats.append({"type": "Feature", "properties": props, "geometry": geom})
    fc = json.dumps({"type": "FeatureCollection", "peildatum": "14 t/m 16 november 2026", "features": feats},
                    ensure_ascii=False, separators=(",", ":"))
    (docs / "gemeenten.geojson").write_text(fc, encoding="utf-8")
    # Zelfde data als script, zodat de pagina ook werkt als je index.html direct opent (file://).
    (docs / "gemeenten.js").write_text("window.GEMEENTEN = " + fc + ";\n", encoding="utf-8")
    return list(files) + list(thema)
