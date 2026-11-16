"""Praktijkcontrole: kapbesluiten in de Gemeenteblad-publicaties (officielebekendmakingen.nl)."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .http import build_url, fetch
from .xmlutil import first_text, iter_local, local, norm, text_of

SRU = "https://repository.overheid.nl/sru"
PAGE = 1000
SINCE = "2025-01-01"
TITLE_TERMS = ["kappen", "vellen", "houtopstand", "houtopstanden", "kapvergunning", "bomenkap", "rooien"]

BESLUIT = re.compile(r"verleend|verleent|verlening|geweigerd|weiger|besluit|ingetrokken|ontheffing verleend", re.I)
GEWEIGERD = re.compile(r"geweigerd|weigering|weigert", re.I)
AANVRAAG = re.compile(r"aanvraag|ontvangen|ingediend", re.I)
GRONDSLAG = re.compile(r"(artikel|art\.)\s*[\d:.]+[a-z]?", re.I)
GRONDSLAG_CONTEXT = re.compile(
    r"apv|plaatselijke verordening|verordening|omgevingsplan|omgevingswet|houtopstand|bomen|vellen|bruidsschat|"
    r"tijdelijk deel|fysieke leefomgeving|bal\b|besluit activiteiten", re.I)


# Terugvaloptie als een gemeente de kapactiviteit niet in de titel zet: zoeken in de volledige tekst.
TEXT_TERMS = ["houtopstand", "houtopstanden", "vellen", "kapvergunning"]


def query_for(name: str, since: str = SINCE, mode: str = "titel") -> str:
    if mode == "titel":
        t = " or ".join(f'dt.title="{x}"' for x in TITLE_TERMS)
    else:
        t = " or ".join(f'cql.textAndIndexes="{x}"' for x in TEXT_TERMS)
    return f'c.product-area==officielepublicaties and dt.creator=="{name}" and dt.date>="{since}" and ({t})'


def count(name: str, raw_dir: Path) -> int:
    url = build_url(SRU, {"query": f'c.product-area==officielepublicaties and dt.creator=="{name}"',
                          "maximumRecords": "0"})
    body = fetch(url, raw_dir / "ob_count.xml", refresh=True, context="naamcontrole")
    return int(first_text(ET.fromstring(body), "numberOfRecords") or 0)


def _parse(rec: ET.Element) -> dict:
    urls = {e.get("manifestation"): norm(e.text or "") for e in iter_local(rec, "itemUrl")}
    types = [norm(e.text or "") for e in iter_local(rec, "type")]
    title = first_text(rec, "title")
    kind = "besluit" if BESLUIT.search(title) else "aanvraag" if AANVRAAG.search(title) else "overig"
    return {
        "id": first_text(rec, "identifier"),
        "titel": title,
        "soort": kind,
        "types": types,
        "datum": first_text(rec, "date"),
        "publicatie": first_text(rec, "publicatienaam"),
        "creator": first_text(rec, "creator"),
        "url": first_text(rec, "preferredUrl"),
        "xml_url": urls.get("xml") or first_text(rec, "url"),
        "html_url": urls.get("html"),
        "pdf_url": urls.get("pdf"),
    }


def search(name: str, raw_dir: Path, refresh: bool = False, max_records: int = 5000,
           mode: str = "titel") -> tuple[str, int, list[dict]]:
    q = query_for(name, mode=mode)
    prefix = "ob_sru" if mode == "titel" else "ob_tekst_sru"
    out: list[dict] = []
    start, page, total = 1, 1, 0
    while start <= max_records:
        url = build_url(SRU, {"query": q, "maximumRecords": str(PAGE), "startRecord": str(start)})
        body = fetch(url, raw_dir / f"{prefix}_p{page}.xml", refresh=refresh, context=f"bekendmakingen {name}")
        root = ET.fromstring(body)
        total = int(first_text(root, "numberOfRecords") or 0)
        recs = [r for r in iter_local(root, "record") if any(local(c.tag) == "recordData" for c in r)]
        out += [_parse(r) for r in recs]
        start += PAGE
        page += 1
        if not recs or start > total:
            break
    return q, total, out


def grondslag_snippets(xml: bytes, limit: int = 6) -> list[str]:
    """Zinnen met een artikelverwijzing in de context van kapregels (letterlijk)."""
    try:
        text = text_of(ET.fromstring(xml))
    except ET.ParseError:
        return []
    sentences = re.split(r"(?<=[.;])\s+(?=[A-Z0-9(])", text)
    hits, seen = [], set()
    for s in sentences:
        if GRONDSLAG.search(s) and GRONDSLAG_CONTEXT.search(s):
            s = s[:500]
            if s not in seen:
                seen.add(s)
                hits.append(s)
        if len(hits) >= limit:
            break
    return hits
