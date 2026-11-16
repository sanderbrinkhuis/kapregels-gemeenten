"""Zet CVDR-XML om naar leesbare tekst en haal de voor kapregels relevante artikelen eruit.

Werkt op de ongewijzigde CVDR-XML; de XML zelf blijft altijd bewaard. De
extractie is een leeshulp, geen interpretatie: hij selecteert artikelen op
trefwoorden en geeft de volledige artikeltekst letterlijk weer.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from .xmlutil import local as _local, norm, text_of


def local(tag: str) -> str:
    """Tagnaam zonder namespace, in kleine letters (CVDR: <artikel>, STOP: <tekst:Artikel>)."""
    return _local(tag).lower()

# Artikelen waarvan de tekst een van deze termen bevat, worden geëxtraheerd.
KEY = re.compile(
    r"houtopstand|\bbomen|\bboom|\bvellen\b|\bvelling|herplant|kapvergunning|\bkappen\b|"
    r"boomwaarde|bomenlijst|bomenregister|bomenkaart|monumentale\s+bo|bebouwingscontour",
    re.I,
)
# Definitieartikelen met deze termen worden ook opgenomen (begrip bebouwde kom e.d.).
DEFINITION = re.compile(r"definit|begrip", re.I)
DEFINITION_KEY = re.compile(r"bebouwde\s+kom|bebouwingscontour|houtopstand", re.I)
# Hele hoofdstukken/afdelingen/paragrafen met een van deze termen in de titel.
SECTION = re.compile(r"houtopstand|bomen|\bboom|groen|\bkap|herplant", re.I)
# Artikelen over sancties (verwijzen vaak alleen naar artikelnummers).
SANCTION = re.compile(r"straf|boete|sanctie|economisch|delict", re.I)
# Documenten waarvan de titel hierop past, worden integraal opgenomen.
STRONG_TITLE = re.compile(r"bomen|\bboom|houtopstand|\bkap|herplant|groen|compensatie", re.I)

CONTAINERS = {"hoofdstuk", "afdeling", "paragraaf", "sub-paragraaf", "subparagraaf", "subsubparagraaf",
              "titeldeel", "divisie", "divisietekst", "deel", "boek", "titel-deel", "bijlage",
              "toelichting", "algemenetoelichting", "artikelgewijzetoelichting"}
NUMMERS = {"lidnr", "lidnummer", "linummer"}
BLOCK = {"al", "lid", "lijst", "li", "table", "artikel", "kop"} | CONTAINERS


def _kop(el: ET.Element) -> str:
    for c in el:
        if local(c.tag) == "kop":
            parts = [norm("".join(x.itertext())) for x in c if local(x.tag) in ("label", "nr", "nummer", "titel", "opschrift")]
            return " ".join(p for p in parts if p)
    return ""


def render(el: ET.Element, level: int = 2) -> list[str]:
    """Render een element als markdown-regels, met behoud van lid- en lijstnummers."""
    tag = local(el.tag)
    out: list[str] = []
    if tag == "kop" or tag in NUMMERS:
        return out
    if tag == "al":
        t = text_of(el)
        return [t] if t else []
    if tag == "lid":
        nr = next((text_of(c) for c in el if local(c.tag) in ("lidnr", "lidnummer")), "")
        body = [l for c in el for l in render(c, level)]
        if body:
            body[0] = f"{nr} {body[0]}".strip()
        elif nr:
            # Sommige gemeenten zetten lidtekst in <lidnr> (bijv. Nadere regels houtkap Hoogeveen).
            body = [nr]
        return body + [""]
    if tag == "lijst":
        for li in el:
            if local(li.tag) != "li":
                continue
            nr = li.get("nr") or next((text_of(c) for c in li if local(c.tag) == "linummer"), "-")
            body = [l for c in li for l in render(c, level)]
            body = [l for l in body if l]
            if body:
                out.append(f"  {nr} {body[0]}")
                out.extend(f"     {l}" for l in body[1:])
        return out
    if tag == "table":
        for row in el.iter():
            if local(row.tag) == "row":
                out.append("| " + " | ".join(text_of(e) for e in row if local(e.tag) == "entry") + " |")
        return out + [""]
    if tag == "artikel":
        out.append(f"{'#' * min(level, 6)} {_kop(el) or 'Artikel'}")
        out.append("")
        for c in el:
            out.extend(render(c, level + 1))
        return out + [""]
    if tag in CONTAINERS:
        k = _kop(el)
        if k:
            out += [f"{'#' * min(level, 6)} {k}", ""]
        for c in el:
            out.extend(render(c, level + 1))
        return out
    # Geen blokelementen eronder: inline inhoud (tekst met links, nadruk e.d.) als één regel.
    if not any(local(d.tag) in BLOCK for d in el.iter() if d is not el):
        t = text_of(el)
        return [t] if t else []
    lead = norm(el.text or "")
    if lead:
        out.append(lead)
    for c in el:
        out.extend(render(c, level))
        tail = norm(c.tail or "")
        if tail:
            out.append(tail)
    return out


def _render_unit(el: ET.Element) -> list[str]:
    if local(el.tag) == "artikel":
        return render(el, 4)
    out = [f"#### {_kop(el)}", ""]
    for c in el:
        out.extend(render(c, 5))
    return out + [""]


def _body(root: ET.Element) -> ET.Element:
    for e in root.iter():
        if local(e.tag) == "body":
            return e
    return root


def full_text(xml: bytes) -> str:
    root = ET.fromstring(xml)
    lines = render(_body(root))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def relevant_articles(xml: bytes, title: str = "") -> tuple[list[dict], bool]:
    """Geef (artikelen, integraal). Integraal = hele document is relevant (titel past)."""
    root = ET.fromstring(xml)
    body = _body(root)
    if STRONG_TITLE.search(title or ""):
        return [], True

    found: list[dict] = []

    def walk(el: ET.Element, path: list[str], in_section: bool):
        tag = local(el.tag)
        is_leaf_container = tag in CONTAINERS and not any(
            local(d.tag) in CONTAINERS | {"artikel"} for d in el.iter() if d is not el)
        if tag == "artikel" or is_leaf_container:
            # Sommige verordeningen (VFL) gebruiken paragrafen zonder <artikel> als kleinste eenheid.
            k = _kop(el)
            text = text_of(el)
            reason = None
            if in_section:
                reason = "sectie"
            elif KEY.search(text):
                reason = "trefwoord"
            elif SANCTION.search(k):
                reason = "sanctie"
            elif DEFINITION.search(k) and DEFINITION_KEY.search(text):
                reason = "definitie"
            if reason:
                found.append({"pad": " > ".join(path), "kop": k, "reden": reason,
                              "tekst": "\n".join(_render_unit(el))})
            return
        if tag in CONTAINERS:
            k = _kop(el)
            sub = path + [k] if k else path
            sec = in_section or bool(SECTION.search(k))
            for c in el:
                walk(c, sub, sec)
            return
        for c in el:
            walk(c, path, in_section)

    walk(body, [], False)

    # Geen artikelstructuur (bijv. beleidsregel in losse alinea's) maar wel trefwoorden: integraal.
    has_articles = any(local(e.tag) == "artikel" for e in body.iter())
    if not has_articles and KEY.search(text_of(body)):
        return [], True
    return found, False


def extract_markdown(meta: dict, xml: bytes) -> tuple[str, list[str], bool]:
    """Bouw het extractbestand. Geeft (markdown, artikelkoppen, integraal)."""
    arts, integral = relevant_articles(xml, meta.get("titel", ""))
    head = [
        f"# {meta.get('titel', '')}",
        "",
        f"- Identifier: {meta.get('id')}",
        f"- Gemeente (creator): {meta.get('creator')}",
        f"- Type: {meta.get('type')}",
        f"- Inwerkingtreding: {meta.get('inwerkingtreding') or '?'}; "
        f"uitwerkingtreding: {meta.get('uitwerkingtreding') or '— (geldend)'}",
        f"- Omgevingswet-regeling: {meta.get('omgevingswet') or '?'}",
        f"- URL: {meta.get('url')}",
        f"- XML: {meta.get('xml_url')}",
        "",
    ]
    if integral:
        return "\n".join(head + ["_Integraal opgenomen (titel of structuur wijst op een volledig relevante regeling)._", "",
                                 full_text(xml)]), [], True
    if not arts:
        return "\n".join(head + ["_Geen relevante artikelen gevonden op trefwoord._", ""]), [], False
    body = []
    for a in arts:
        body += [f"<!-- pad: {a['pad']} | reden: {a['reden']} -->", a["tekst"], ""]
    return "\n".join(head + body), [a["kop"] for a in arts], False
