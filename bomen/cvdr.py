"""Regelingen uit de CVDR (lokaleregelgeving.overheid.nl) via de SRU-zoekdienst."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

from .http import build_url, fetch
from .xmlutil import first_text, iter_local, local, norm

SRU = "https://zoekservice.overheid.nl/sru/Search"
PAGE = 1000

KEYWORDS = ["houtopstand", "houtopstanden", "bomen", "herplant", "herplantplicht", "kapvergunning",
            "vellen", "bomenverordening", "boomwaarde", "bomenlijst", "bomenregister"]

# Geldende regelingen met zo'n titel worden gedownload; overige alleen als metadata bewaard.
DOWNLOAD_TITLE = re.compile(
    r"plaatselijke|\bapv\b|bomen|\bboom|houtopstand|\bkap|groen|fysieke leefomgeving|omgevingsplan|"
    r"herplant|compensatie|handhaving|sanctie|boete|leges|vellen|landschap|monument|omgevingsverordening|"
    # Toegevoegd na Drenthe: kernregelingen met afwijkende titels (Verordening Leefomgeving
    # Midden-Drenthe, Nadere regels houtkap Hoogeveen, Algemene verordening gemeente Leudal,
    # Verordening op de beplantingen Leiderdorp, Omgevings- en Bouwverordening Bronckhorst).
    r"leefomgeving|houtkap|houtsingel|houtwal|beplanting|"
    r"algemene verordening(?! ondergrond| kabels| inzake werkzaamheden)|omgevings- en bouw|"
    # Toegevoegd na Noord-Holland: Verordening fysiek domein gemeente Haarlemmermeer 2024.
    r"fysiek domein|"
    # Toegevoegd bij Noord-Brabant: Duinverordening Heusden/Waalwijk, Biesboschverordening Altena.
    r"\bduin|biesbosch",
    re.I,
)


def query_for(name: str) -> str:
    kw = " or ".join(f'keyword="{k}"' for k in KEYWORDS)
    return f'dcterms.creator=="{name}" and ({kw})'


def count(name: str, raw_dir: Path) -> int:
    url = build_url(SRU, {"version": "1.2", "operation": "searchRetrieve", "x-connection": "cvdr",
                          "query": f'dcterms.creator=="{name}"', "maximumRecords": "0"})
    body = fetch(url, raw_dir / "cvdr_count.xml", refresh=True, context="naamcontrole")
    return int(first_text(ET.fromstring(body), "numberOfRecords") or 0)


def _parse_record(rec: ET.Element) -> dict:
    g = lambda n: first_text(rec, n)  # noqa: E731
    ident = g("identifier")
    m = re.match(r"(CVDR\d+)_(\d+)", ident)
    return {
        "id": ident,
        "work": m.group(1) if m else ident,
        "versie": int(m.group(2)) if m else None,
        "titel": g("title"),
        "creator": g("creator"),
        "type": g("type"),
        "onderwerp": g("subject"),
        "vastgesteld_door": g("isRatifiedBy"),
        "issued": g("issued"),
        "modified": g("modified"),
        "inwerkingtreding": g("inwerkingtredingDatum"),
        "uitwerkingtreding": g("uitwerkingtredingDatum"),
        "betreft": g("betreft"),
        "kenmerk": g("kenmerk"),
        "omgevingswet": g("omgevingswet"),
        "redactionele_toevoeging": norm(re.sub(r"<[^>]+>", " ", g("redactioneleToevoeging"))),
        "bron_publicatie": g("isFormatOf"),
        "xml_url": g("publicatieurl_xml"),
        "url": g("preferred_url"),
        "work_url": g("preferred_work_url"),
    }


def search(name: str, raw_dir: Path, refresh: bool = False) -> tuple[str, list[dict]]:
    q = query_for(name)
    records: list[dict] = []
    start, page = 1, 1
    while True:
        url = build_url(SRU, {"version": "1.2", "operation": "searchRetrieve", "x-connection": "cvdr",
                              "query": q, "maximumRecords": str(PAGE), "startRecord": str(start)})
        body = fetch(url, raw_dir / f"cvdr_sru_p{page}.xml", refresh=refresh, context=f"cvdr-zoek {name}")
        root = ET.fromstring(body)
        total = int(first_text(root, "numberOfRecords") or 0)
        recs = [r for r in iter_local(root, "record")
                if any(local(c.tag) == "recordData" for c in r)]
        records += [_parse_record(r) for r in recs]
        start += PAGE
        page += 1
        if not recs or start > total:
            break
    return q, records


def status_of(rec: dict, today: date) -> str:
    inw, uitw = rec.get("inwerkingtreding"), rec.get("uitwerkingtreding")
    if inw and inw > today.isoformat():
        return "toekomstig"
    if not uitw or uitw > today.isoformat():
        return "geldend"
    return "vervallen"
