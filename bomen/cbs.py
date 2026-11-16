"""Stap 0: gemeentelijst per 1 januari 2026 uit CBS-tabel 86247NED."""

from __future__ import annotations

import csv
import json
import re

from .http import DATA, build_url, fetch

TABLE = "86247NED"
BASE = f"https://opendata.cbs.nl/ODataApi/odata/{TABLE}"
GEMEENTEN_CSV = DATA / "gemeenten_2026.csv"
EXPECTED = 342


def search_name(cbs_name: str) -> str:
    """CBS schrijft 'Bergen (NH.)', overheid.nl 'Bergen (NH)'."""
    return re.sub(r"\(([^)]*?)\.\)", r"(\1)", cbs_name).strip()


def fetch_gemeenten(refresh: bool = False) -> list[dict]:
    raw = DATA / "raw" / "cbs"
    fetch(f"{BASE}/TableInfos", raw / f"{TABLE}_TableInfos.json", refresh=refresh, context="cbs")
    url = build_url(f"{BASE}/TypedDataSet", {"$select": "RegioS,Naam_2,Code_28,Naam_29"})
    body = fetch(url, raw / f"{TABLE}_TypedDataSet.json", refresh=refresh, context="cbs")
    info = json.loads((raw / f"{TABLE}_TableInfos.json").read_text())["value"][0]

    rows = []
    for r in json.loads(body)["value"]:
        code = r["RegioS"].strip()
        if not code.startswith("GM"):
            continue
        naam = r["Naam_2"].strip()
        rows.append({
            "gm_code": code,
            "gemeente": naam,
            "zoeknaam": search_name(naam),
            "provincie_code": r["Code_28"].strip(),
            "provincie": r["Naam_29"].strip(),
        })
    rows.sort(key=lambda r: r["gemeente"].lower())

    GEMEENTEN_CSV.parent.mkdir(parents=True, exist_ok=True)
    with GEMEENTEN_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";")
        w.writeheader()
        w.writerows(rows)

    print(f"CBS {TABLE} '{info['Title']}', gewijzigd {info['Modified']}: {len(rows)} gemeenten "
          f"(verwacht {EXPECTED}{'' if len(rows) == EXPECTED else ' — AFWIJKING'})")
    return rows


def load_gemeenten() -> list[dict]:
    if not GEMEENTEN_CSV.exists():
        return fetch_gemeenten()
    with GEMEENTEN_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))
