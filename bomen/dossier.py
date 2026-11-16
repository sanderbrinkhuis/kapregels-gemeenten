"""Dossier per gemeente: één compact leesbestand voor de scorende agent.

Het dossier bundelt uit de al opgehaalde bronnen alleen wat voor het scoren nodig is:

- kernverordeningen (APV, VFL, bomenverordening): de kapartikelen, definities en
  strafbepalingen, letterlijk en volledig (uit de CVDR-XML);
- beleidsregels en beleidsplannen (herplant, compensatie, handhaving, bomenlijst):
  alleen de secties of alinea's over kap;
- legesverordening: alleen de tabelrijen en alinea's over kap (meestal art. 2.30);
- omgevingsplan: alleen de artikelen over kap (meestal art. 22.299);
- bekendmakingen: tellingen en alleen de grondslagcitaten die over kap gaan.

Het dossier is een leeshulp, geen interpretatie. Alle tekst is letterlijk overgenomen;
bij elk fragment staat het bestand met de volledige tekst, zodat de agent kan controleren.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .extract import CONTAINERS, KEY, _kop, _render_unit, local, relevant_articles
from .http import ROOT
from .scores import ADRES
from .xmlutil import text_of

# Strikte kaptermen: bepalen of een sectie of alinea buiten de kernverordening wordt opgenomen.
KAP = re.compile(
    r"houtopstand|\bvell(?:en|ing)\b|\bgeveld|\bkap(?:pen|vergunning(?:en)?|verbod|aanvra(?:ag|gen)|melding(?:en)?|beleid)\b|\bgekapt|"
    r"herplant|herbeplant|bomenlijst|bomenregister|bomenkaart|bomenverordening|monumentale\s+bo|bijzondere\s+bo|"
    r"waardevolle\s+bo|beschermwaardige\s+bo|boomwaarde|bomenfonds|herplantfonds|groencompensatie|compensatieplicht|bomencompensatie|"
    r"\b(?:verwijderen|rooien)\s+van\s+(?:\w+\s+){0,3}bomen\b",
    re.I,
)
LEGES_RIJ = re.compile(r"houtopstand|\bvell|\bkap(?:pen|vergunning)?\b|\bbomen\b|\bboom\b", re.I)
KERN_TITEL = re.compile(r"verordening|plaatselijke|\bapv\b|\bvfl\b", re.I)
KAP_TITEL = re.compile(r"bomen|\bboom|houtopstand|\bkap(?:pen|beleid|vergunning)?\b|herplant|compensatie", re.I)
LEGES_TITEL = re.compile(r"\bleges", re.I)
OMGEVINGSPLAN_TITEL = re.compile(r"^\s*omgevingsplan\b", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

# Maximale lengte per document (tekens) per soort; daarboven wordt afgekapt met verwijzing.
MAX = {"kern": 60000, "kapbeleid": 20000, "omgevingsplan": 12000, "leges": 4000, "overig": 4000}
SECTIE_HEEL = 2500  # secties tot deze lengte gaan heel mee, langere alleen de treffende alinea's


def soort(r: dict) -> str:
    t = r.get("titel", "")
    if LEGES_TITEL.search(t):
        return "leges"
    if OMGEVINGSPLAN_TITEL.search(t):
        return "omgevingsplan"
    if KERN_TITEL.search(t) and not re.search(r"beleid|subsidie|nadere regels", t, re.I):
        return "kern"
    if KAP_TITEL.search(t) or re.search(r"handhaving|sanctie|bestuurlijke boete|dwangsom|groen|beplanting|"
                                        r"landschap|beleidsregel", t, re.I):
        return "kapbeleid"
    return "overig"


# --- markdown in secties --------------------------------------------------------------------

def secties(md: str) -> list[tuple[list[str], str, str]]:
    """Splits markdown op koppen. Geeft (koppen van de bovenliggende secties, kop, body) per sectie."""
    out: list[tuple[list[str], str, str]] = []
    stack: list[tuple[int, str]] = []  # (niveau, kop) van de huidige sectie en haar ouders
    body: list[str] = []

    def emit():
        if stack or any(regel.strip() for regel in body):
            out.append(([k for _, k in stack[:-1]], stack[-1][1] if stack else "", "\n".join(body).strip()))

    for line in md.splitlines():
        m = HEADING.match(line)
        if not m:
            body.append(line)
            continue
        emit()
        lvl = len(m.group(1))
        while stack and stack[-1][0] >= lvl:
            stack.pop()
        stack.append((lvl, m.group(2).strip()))
        body = []
    emit()
    return out


# Algemene artikelen die bij een kernverordening altijd meegaan: nakomen van voorschriften (f3),
# strafbepaling, WED, bestuurlijke boete, begripsbepalingen.
KERN_KOP = re.compile(r"straf|sanctie|economisch|boete|begrip|definit", re.I)
# Algemene procedureartikelen van een APV/VFL: kort en vaak nodig voor W (weigeren) en g (procedure).
KERN_ALGEMEEN = re.compile(r"weigeringsgrond|beslistermijn|intrekking|vervallen van de vergunning|"
                           r"voorschriften en beperkingen", re.I)
KERN_TEKST = re.compile(r"voorschriften en beperkingen na te komen|daaraan verbonden voorschriften|"
                        r"economische delicten|hechtenis|geldboete|bestuurlijke boete", re.I)
# Hoofdstukken met algemene vergunningbepalingen (APV hfst. 1; VFL 'Bepalingen ten aanzien van vergunningen').
ALGEMEEN_HOOFDSTUK = re.compile(r"algeme(?:ne|en)\s+bepaling|bepalingen\s+(?:ten aanzien van|over|voor)\s+"
                                r"(?:de\s+)?vergunning", re.I)
VENSTER = 700  # lange alinea: alleen dit aantal tekens rond elke treffer


def _eenheden(body: str) -> list[str]:
    """Alinea's; een tabel wordt opgesplitst in losse rijen (de kopregel blijft als eerste rij herkenbaar)."""
    out: list[str] = []
    for al in re.split(r"\n\s*\n", body):
        lines = [l for l in al.splitlines() if l.strip()]  # noqa: E741
        if lines and all(l.lstrip().startswith("|") for l in lines):  # noqa: E741
            out += [f"{lines[0]}\n{r}" if i else r for i, r in enumerate(lines)]
        elif lines:
            out.append("\n".join(lines))
    return out


def _venster(al: str, rx: re.Pattern) -> str:
    if len(al) <= 2 * VENSTER:
        return al
    spans, parts = [], []
    for m in rx.finditer(al):
        a, b = max(0, m.start() - VENSTER // 2), min(len(al), m.end() + VENSTER // 2)
        if spans and a <= spans[-1][1]:
            spans[-1] = (spans[-1][0], b)
        else:
            spans.append((a, b))
    for a, b in spans:
        parts.append(("…" if a else "") + al[a:b] + ("…" if b < len(al) else ""))
    return " [...] ".join(parts)


def _treffers(body: str, rx: re.Pattern, context: bool) -> str:
    al = _eenheden(body)
    keep = set()
    for i, a in enumerate(al):
        if rx.search(a):
            keep.add(i)
            if context and not a.lstrip().startswith("|"):
                keep |= {j for j in (i - 1, i + 1) if 0 <= j < len(al) and len(al[j]) <= VENSTER
                         and not al[j].lstrip().startswith("|")}
    parts, last = [], -2
    for i in sorted(keep):
        if i > last + 1 and parts:
            parts.append("[…]")
        parts.append(_venster(al[i].strip(), rx) if i in keep and rx.search(al[i]) else al[i].strip())
        last = i
    return "\n\n".join(parts)


def filter_md(md: str, extra_kop: re.Pattern | None = None, extra_tekst: re.Pattern | None = None,
              compact: bool = False) -> str:
    """Alleen de secties (of alinea's) waarin een kapterm staat, met het koppad erbij.

    compact: korte secties niet meer heel opnemen en geen omliggende alinea's (voor lange documenten).
    """
    rx = KAP if extra_tekst is None else re.compile(f"{KAP.pattern}|{extra_tekst.pattern}", re.I)
    out = []
    for pad, kop, body in secties(md):
        hit_kop = bool(KAP.search(kop) or (extra_kop and extra_kop.search(kop)))
        if not (hit_kop or rx.search(body)):
            continue
        if not compact and (len(body) <= SECTIE_HEEL or hit_kop and len(body) <= 2 * SECTIE_HEEL):
            tekst = body
        elif hit_kop and len(body) <= SECTIE_HEEL:
            tekst = body
        else:
            tekst = _treffers(body, rx, context=not compact)
        context = " > ".join(p for p in pad if p)
        out.append(f"#### {kop or '(zonder kop)'}" + (f"  \n<sub>in: {context}</sub>" if context else ""))
        out.append("")
        out.append(tekst or "_(geen tekst onder deze kop)_")
        out.append("")
    return "\n".join(out).strip()


def filter_binnen(md: str, max_len: int, **kw) -> str:
    """filter_md, en als dat te lang wordt de compacte variant."""
    t = filter_md(md, **kw)
    return t if len(t) <= max_len else filter_md(md, compact=True, **kw)


def leges_md(md: str) -> str:
    lines = md.splitlines()
    rows, keep = [], set()
    for i, regel in enumerate(lines):
        if regel.lstrip().startswith("|") and LEGES_RIJ.search(regel):
            keep.add(i)
            # vervolgrijen (bedragen, maxima) tot de volgende genummerde post, hooguit 6
            for j in range(i + 1, min(i + 7, len(lines))):
                if not lines[j].lstrip().startswith("|") or re.match(r"\|\s*\d+(?:\.\d+)+\s*\|", lines[j].strip()):
                    break
                keep.add(j)
    rows = [lines[i].strip() for i in sorted(keep)]
    rest = "\n".join(l for l in md.splitlines() if not l.lstrip().startswith("|"))  # noqa: E741
    tekst = filter_binnen(rest, MAX["leges"])
    out = []
    if rows:
        out += ["Tabelrijen over kap:", ""] + rows + [""]
    if tekst:
        out += [tekst]
    return "\n".join(out).strip()


def kern_md(xml: bytes) -> str:
    """Kapartikelen plus algemene artikelen (nakomen voorschriften, straf, WED, begrippen), volledig."""
    # Titel bewust leeg: de titelregel 'integraal' (bijv. '\bkap' in 'Kapelle') niet gebruiken.
    arts, integraal = relevant_articles(xml, "")
    if integraal:
        return ""
    gezien = {a["tekst"] for a in arts}

    def walk(el: ET.Element, algemeen: bool):
        tag = local(el.tag)
        if tag == "artikel":
            k, t = _kop(el), text_of(el)
            if KERN_TEKST.search(t) or (KERN_KOP.search(k) and KEY.search(t)) or (algemeen and KERN_ALGEMEEN.search(k)):
                tekst = "\n".join(_render_unit(el))
                if tekst not in gezien:
                    gezien.add(tekst)
                    arts.append({"pad": "", "kop": k, "reden": "algemeen artikel (voorschriften/straf/procedure)",
                                 "tekst": tekst})
            return
        if tag in CONTAINERS:
            algemeen = algemeen or bool(ALGEMEEN_HOOFDSTUK.search(_kop(el)))
        for c in el:
            walk(c, algemeen)

    walk(ET.fromstring(xml), False)
    out = []
    for a in arts:
        out.append(f"<!-- pad: {a['pad']} | reden: {a['reden']} -->")
        out.append(a["tekst"].strip())
        out.append("")
    return "\n".join(out).strip()


def _afkappen(tekst: str, max_len: int, bron: str) -> str:
    if len(tekst) <= max_len:
        return tekst
    cut = tekst.rfind("\n\n", 0, max_len)
    return tekst[: cut if cut > max_len // 2 else max_len] + \
        f"\n\n**[Afgekapt na {max_len} tekens. Zoek verder met grep in `{bron}`.]**"


# --- dossier ---------------------------------------------------------------------------------

def bouw(gdir: Path) -> tuple[str, dict]:
    bronnen = json.loads((gdir / "bronnen.json").read_text(encoding="utf-8"))
    regels = (gdir / "regelingen.jsonl").read_text(encoding="utf-8").splitlines()
    recs = [json.loads(regel) for regel in regels if regel.strip()]
    geldend = [r for r in recs if r["status"] in ("geldend", "toekomstig")]
    rel = lambda p: str(p.relative_to(ROOT))  # noqa: E731

    blokken = {"kern": [], "kapbeleid": [], "leges": [], "omgevingsplan": [], "overig": []}
    niet_opgenomen = []
    for r in sorted(geldend, key=lambda r: r["titel"].lower()):
        if not r.get("gedownload"):
            niet_opgenomen.append((r, "niet gedownload (titel lijkt niet relevant)"))
            continue
        xml_p, txt_p = gdir / "cvdr" / f"{r['id']}.xml", gdir / "tekst" / f"{r['id']}.md"
        if not txt_p.exists():
            niet_opgenomen.append((r, "geen tekstbestand"))
            continue
        md = txt_p.read_text(encoding="utf-8")
        s = soort(r)
        if s == "kern":
            body = kern_md(xml_p.read_bytes()) if xml_p.exists() else ""
            if not body:  # geen artikelstructuur of geen kapartikelen: alinea-filter
                body = filter_binnen(md, MAX[s], extra_kop=KERN_KOP, extra_tekst=KERN_TEKST)
        elif s == "leges":
            body = leges_md(md)
        elif s == "kapbeleid" and KAP_TITEL.search(r["titel"]) and len(md) <= MAX["kapbeleid"]:
            body = md.strip()  # korte kapbeleidsregel: integraal
        else:
            body = filter_binnen(md, MAX[s])
        if not body:
            niet_opgenomen.append((r, "geen kaptermen in de tekst"))
            continue
        body = _afkappen(body, MAX[s], rel(txt_p))
        kop = [f"### {r['titel']}", "",
               f"{r['id']} · in werking {r.get('inwerkingtreding') or '?'} · status {r['status']} · "
               f"Omgevingswet-regeling: {r.get('omgevingswet') or '?'}  ",
               f"Bron: {r['url']} · volledige tekst: `{rel(txt_p)}` · XML: `{rel(xml_p)}`", ""]
        blokken[s].append("\n".join(kop) + body + "\n")

    g = bronnen
    L = [f"# Dossier {g['gemeente']} ({g['gm_code']}) — {g['provincie']}", "",
         f"Peildatum geldigheid: {g['peildatum']} · bronnen opgehaald: {g['opgehaald_op']} · "
         f"herkomst per bestand: data/manifest.jsonl", "",
         "Dit dossier bevat alleen de passages die over kap gaan, letterlijk overgenomen. "
         "Citeer uit dit dossier of uit het genoemde tekstbestand. Twijfel je of iets ontbreekt "
         "(bijv. een strafbepaling die alleen artikelnummers noemt, of een begrip), zoek dan met grep "
         "in het volledige tekstbestand.", "",
         f"CVDR: {g.get('cvdr_treffers', 0)} treffers (alle versies), {len(geldend)} geldend of toekomstig. "
         f"Vervallen versies: zie `{rel(gdir / 'regelingen.jsonl')}`.", ""]
    titels = {"kern": "Kernverordeningen (kapartikelen, definities, strafbepalingen)",
              "kapbeleid": "Beleidsregels en beleidsplannen (alleen passages over kap)",
              "leges": "Leges (alleen kap)", "omgevingsplan": "Omgevingsplan (alleen artikelen over kap)",
              "overig": "Overige geldende documenten met kaptermen (alleen passages)"}
    for s, titel in titels.items():
        if blokken[s]:
            L += [f"## {titel}", ""] + blokken[s]

    if not any(re.search(r"plaatselijke verordening|\bapv\b|fysieke leefomgeving|\bvfl\b", r["titel"], re.I)
               for r in geldend):
        L += ["## Let op: geen geldende APV of VFL in de treffers", "",
              "_De CVDR-zoekvraag vindt alleen regelingen met kaptermen. Haal de actuele APV (en VFL, als die er is) "
              "zelf op via de SRU-zoekvraag op creator en titel en stel vast of er een kapregel in staat._", ""]
    if not blokken["leges"]:
        L += ["## Leges", "", "_Geen legesverordening met een kaprij in de geldende CVDR-treffers. "
              "Leg de leges vast als 'niet gevonden in CVDR'._", ""]
    L += bekendmakingen_md(gdir, g)
    if niet_opgenomen:
        L += ["## Geldende documenten zonder kappassages (niet opgenomen)", ""]
        L += [f"- {r['titel']} ({r['id']}): {why}" for r, why in niet_opgenomen]
        L.append("")
    L += ["## Niet automatisch opgehaald — handmatig controleren", "",
          "- Omgevingsplan tijdelijk deel / regels in DSO (omgevingswet.overheid.nl)",
          "- Bomenlijst, bomenkaart of register: staan er particuliere bomen op?",
          "- Gemeentelijke website: beleidsregels herplant/compensatie, handhavingsbeleid", ""]
    tekst = "\n".join(L)
    stats = {"gm_code": g["gm_code"], "gemeente": g["gemeente"], "tekens": len(tekst),
             **{s: len(v) for s, v in blokken.items()}, "niet_opgenomen": len(niet_opgenomen)}
    return tekst, stats


def bekendmakingen_md(gdir: Path, g: dict) -> list[str]:
    p = gdir / "bekendmakingen.jsonl"
    if not p.exists():
        return []
    pubs = [json.loads(regel) for regel in p.read_text(encoding="utf-8").splitlines() if regel.strip()]
    L = ["## Bekendmakingen sinds 2025 (praktijkcontrole)", "",
         f"Zoekmethode: {g.get('bekendmakingen_zoekmethode', '?')}  ",
         f"Totaal: {g.get('bekendmakingen_totaal', 0)} · besluiten: {g.get('bekendmakingen_besluiten', 0)} · "
         f"aanvragen: {g.get('bekendmakingen_aanvragen', 0)} · geweigerd (volgens titel): "
         f"{g.get('bekendmakingen_geweigerd', 0)}", ""]
    dl = [x for x in pubs if x.get("gedownload")]
    if dl:
        L += [f"Steekproef: {len(dl)} recente besluiten opgehaald. Alleen grondslagcitaten met een kapterm "
              f"staan hieronder. Adressen in titels zijn gemaskeerd; neem titels niet over in de rij.", ""]
    for x in dl:
        cit = [c for c in x.get("grondslag_citaten") or [] if KAP.search(c)]
        titel = ADRES.sub("[adres]", x.get("titel", ""))[:160]
        L.append(f"- [{x['id']}]({x['url']}) — {x['datum']} — {titel} — "
                 + ("geen grondslagcitaat over kap" if not cit else ""))
        for c in cit:
            L.append(f"  > {c[:500]}{'…' if len(c) > 500 else ''}")
    besl = sorted((x for x in pubs if x.get("soort") == "besluit" and not x.get("gedownload")),
                  key=lambda x: x.get("datum", ""), reverse=True)
    if besl:
        L += ["", f"Overige besluiten ({len(besl)}), recentste 25, adressen gemaskeerd:", ""]
        L += [f"- {x['id']} — {x['datum']} — {ADRES.sub('[adres]', x.get('titel', ''))[:160]}" for x in besl[:25]]
    L.append("")
    return L


def schrijf(gdir: Path) -> dict:
    tekst, stats = bouw(gdir)
    (gdir / "dossier.md").write_text(tekst, encoding="utf-8")
    oud = sum(f.stat().st_size for f in (gdir / "extract").glob("*.md")) if (gdir / "extract").exists() else 0
    stats["extract_tekens_oud"] = oud
    return stats
