"""Citaatcontrole: staat elk letterlijk citaat uit output/rijen/<GM>.json in de brontekst?

Een citaat is tekst tussen enkele aanhalingstekens ('…' of ‘…’) in een tekstveld. Weglatingen
('...', '…' of '[...]') splitsen een citaat in fragmenten; elk fragment van minstens 20 tekens
wordt gezocht in de volledige teksten (tekst/*.md) en het dossier van die gemeente, na
normalisatie van witruimte, aanhalingstekens en hoofdletters.

Niet gevonden betekent niet automatisch fout: het citaat kan uit een andere bron komen
(Bal, website, bomenlijst) of licht zijn ingekort. Het is een lijst om na te lopen.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .scores import RIJEN

MIN_LEN = 20
# Openend aanhalingsteken na begin, spatie of haakje; sluitend vóór spatie, leesteken of einde.
QUOTE = re.compile(r"(?:^|(?<=[\s(\[:;,/]))'([^']{12,}?)'(?=[\s.,;:)\]/]|$)")
# Sommige agents citeren tussen dubbele aanhalingstekens (Limburg: Heerlen, Venlo e.a.).
DQUOTE = re.compile(r'(?:^|(?<=[\s(\[:;,/]))"([^"]{12,}?)"(?=[\s.,;:)\]/]|$)')
# Lijstnummers ('a.', '1.', '2°', 'iv)') staan wel in de brontekst, maar zelden in een citaat.
LIJSTNR = re.compile(r"(?:^|(?<=\s))(?:[a-z]|\d{1,2}|[ivx]{2,4})[.°)](?=\s)|(?:^|(?<=\s))[-•·▪–*](?=\s)")


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    s = LIJSTNR.sub(" ", s.lower())
    s = re.sub(r"\s+([,;:.])", r"\1", s)  # '3.2 , 4.9' in de bron
    return re.sub(r"\s+", " ", s).strip()


def fragmenten(rij: dict) -> list[tuple[str, str]]:
    out = []
    for veld, v in rij.items():
        teksten = v if isinstance(v, list) else [v]
        for t in teksten:
            if not isinstance(t, str):
                continue
            t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("„", '"')
            for q in QUOTE.findall(t) + DQUOTE.findall(t):
                for frag in re.split(r"\.\.\.|…|\[[^\]]*\]", q):
                    f = norm(frag).strip(" .,;:")
                    if len(f) >= MIN_LEN:
                        out.append((veld, f))
    return out


def controleer(gm_code: str, gdir: Path) -> tuple[int, list[tuple[str, str]]]:
    rij = json.loads((RIJEN / f"{gm_code}.json").read_text(encoding="utf-8"))
    bronnen = list((gdir / "tekst").glob("*.md")) + [gdir / "dossier.md"] + list((gdir / "dso").glob("*.md"))
    corpus = norm(" ".join(p.read_text(encoding="utf-8") for p in bronnen if p.exists()))
    frags = fragmenten(rij)
    return len(frags), [(veld, f) for veld, f in frags if f not in corpus]
