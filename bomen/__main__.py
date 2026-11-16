"""Commandoregel: python -m bomen <commando>.

  gemeenten   CBS-gemeentelijst 2026 ophalen (stap 0)
  namen       controleer of elke gemeentenaam treffers geeft in CVDR en bekendmakingen
  ophalen     regelingen, extracten en bekendmakingen ophalen per gemeente/provincie
  csv         CSV en afwijkingenlijst uit de bevindingen in output/rijen/
  citaten     citaten uit de bevindingen terugzoeken in de brontekst
  dossier     compact dossier per gemeente voor de scorende agent
  kaart       kaarten (SVG en GeoJSON) uit de bevindingen
  status      overzicht van wat er per gemeente is opgehaald (data/status.csv)
  dso         omgevingsplan (nieuwe deel) uit het DSO doorzoeken op kapregels
  samenvatting cijfers voor het rapport (output/samenvatting.md)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import bekendmakingen as ob
from . import cvdr
from .cbs import fetch_gemeenten, load_gemeenten
from .http import DATA
from .pipeline import GEMEENTEN_DIR, Options, gemeente_dir, names_for, safe_process

KALIBRATIE = ["GM0363", "GM0200", "GM0060", "GM0981", "GM0512"]
VOLGORDE = ["Zeeland", "Flevoland", "Drenthe", "Groningen", "Fryslân", "Limburg", "Utrecht", "Overijssel",
            "Noord-Holland", "Gelderland", "Noord-Brabant", "Zuid-Holland"]


def _fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def select(gem: list[dict], args) -> list[dict]:
    out: list[dict] = []
    if args.kalibratie:
        out += [g for g in gem if g["gm_code"] in KALIBRATIE]
    for p in args.provincie or []:
        hit = [g for g in gem if _fold(g["provincie"]) == _fold(p)]
        if not hit:
            sys.exit(f"Onbekende provincie: {p}")
        out += hit
    for x in args.gemeente or []:
        hit = [g for g in gem if g["gm_code"].upper() == x.upper() or _fold(g["gemeente"]) == _fold(x)]
        if not hit:
            sys.exit(f"Onbekende gemeente: {x}")
        out += hit
    if args.alles:
        order = {_fold(p): i for i, p in enumerate(VOLGORDE)}
        out += sorted(gem, key=lambda g: (order.get(_fold(g["provincie"]), 99), g["gemeente"]))
    seen, uniq = set(), []
    for g in out:
        if g["gm_code"] not in seen:
            seen.add(g["gm_code"])
            uniq.append(g)
    return uniq


def cmd_gemeenten(args):
    fetch_gemeenten(refresh=args.refresh)


def cmd_namen(args):
    gem = load_gemeenten()
    rows = []

    def check(g):
        c_name, o_name = names_for(g)
        raw = gemeente_dir(g) / "raw"
        return {"gm_code": g["gm_code"], "gemeente": g["gemeente"], "zoeknaam_cvdr": c_name,
                "cvdr_totaal": cvdr.count(c_name, raw), "zoeknaam_bekendmakingen": o_name,
                "bekendmakingen_totaal": ob.count(o_name, raw)}

    with ThreadPoolExecutor(args.workers) as ex:
        for f in as_completed([ex.submit(check, g) for g in gem]):
            rows.append(f.result())
    rows.sort(key=lambda r: r["gemeente"].lower())
    path = DATA / "naamcontrole.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";")
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if not r["cvdr_totaal"] or not r["bekendmakingen_totaal"]]
    print(f"{len(rows)} gemeenten gecontroleerd → {path}")
    for r in bad:
        print(f"  GEEN TREFFERS: {r['gm_code']} {r['gemeente']} (cvdr={r['cvdr_totaal']}, "
              f"bekendmakingen={r['bekendmakingen_totaal']}) — voeg alias toe in config/aliassen.json")


def cmd_ophalen(args):
    gem = load_gemeenten()
    todo = select(gem, args)
    if not todo:
        sys.exit("Niets geselecteerd: gebruik --kalibratie, --provincie, --gemeente of --alles")
    opt = Options(refresh=args.refresh, bekendmakingen=not args.geen_bekendmakingen,
                  alle_documenten=args.alle_documenten, steekproef=args.steekproef)
    print(f"{len(todo)} gemeenten ophalen ({args.workers} tegelijk)...")
    with ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(safe_process, g, opt): g for g in todo}
        for i, f in enumerate(as_completed(futs), 1):
            s = f.result()
            err = f" — {len(s['fouten'])} fout(en)" if s.get("fouten") else ""
            print(f"[{i}/{len(todo)}] {s['gm_code']} {s['gemeente']}: "
                  f"{s.get('geldende_regelingen', '?')} geldend, "
                  f"{len(s.get('geldend_met_kapartikelen', []))} met kapartikelen, "
                  f"{s.get('bekendmakingen_totaal', '-')} bekendmakingen{err}", flush=True)
    cmd_status(args)


def cmd_status(args):
    rows = []
    for p in sorted(GEMEENTEN_DIR.glob("*/*/bronnen.json")):
        s = json.loads(p.read_text(encoding="utf-8"))
        rows.append({
            "gm_code": s["gm_code"], "gemeente": s["gemeente"], "provincie": s["provincie"],
            "opgehaald_op": s["opgehaald_op"], "cvdr_treffers": s.get("cvdr_treffers", ""),
            "geldende_regelingen": s.get("geldende_regelingen", ""),
            "geldend_met_kapartikelen": " ".join(s.get("geldend_met_kapartikelen", [])),
            "bekendmakingen_totaal": s.get("bekendmakingen_totaal", ""),
            "bekendmakingen_besluiten": s.get("bekendmakingen_besluiten", ""),
            "bekendmakingen_geweigerd": s.get("bekendmakingen_geweigerd", ""),
            "bekendmakingen_zoekmethode": s.get("bekendmakingen_zoekmethode", "").split(" ")[0],
            "fouten": len(s.get("fouten", [])),
            "map": str(p.parent.relative_to(DATA.parent)),
        })
    if not rows:
        print("Nog niets opgehaald.")
        return
    path = DATA / "status.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";")
        w.writeheader()
        w.writerows(rows)
    geen = [r for r in rows if not r["geldend_met_kapartikelen"]]
    print(f"Status: {len(rows)} gemeenten opgehaald → {path}")
    if geen:
        print(f"  {len(geen)} zonder geldende regeling met kapartikelen in CVDR "
              f"(controleer omgevingsplan/aliassen): " + ", ".join(r["gemeente"] for r in geen[:30]))


def cmd_csv(args):
    from . import scores
    from .pipeline import slug as _slug

    rows, problemen = scores.laad(args.provincie)
    for p in problemen:
        print(f"  ONGELDIG: {p}")
    if not rows:
        sys.exit("Geen geldige rijen gevonden in output/rijen/.")
    if args.provincie:
        for prov in args.provincie:
            sel = scores.sorteer([r for r in rows if _slug(r["provincie"]) == _slug(prov)])
            naam = sel[0]["provincie"] if sel else prov
            scores.schrijf_csv(sel, scores.OUTPUT / f"{_slug(naam)}.csv")
            scores.schrijf_afwijkingen(sel, naam, scores.OUTPUT / f"{_slug(naam)}_afwijkingen.md")
            print(f"{naam}: {len(sel)} rijen → output/{_slug(naam)}.csv en output/{_slug(naam)}_afwijkingen.md")
    else:
        sel = scores.sorteer(rows)
        scores.schrijf_csv(sel, scores.OUTPUT / "alle_gemeenten.csv")
        scores.schrijf_afwijkingen(sel, "alle gemeenten", scores.OUTPUT / "alle_afwijkingen.md")
        print(f"{len(sel)} rijen → output/alle_gemeenten.csv")
    for r in scores.sorteer(rows):
        print(f"  {r['_strengheid']:>3} {r['_categorie']:<14} {r['gemeente']:<28} D{r['_D']} W{r['_W']} H{r['_H']} "
              f"S{r['_S']} bereik {r['_bereik']} ({r['_betrouwbaarheid']})")


def cmd_dossier(args):
    from .dossier import schrijf

    gem = load_gemeenten()
    todo = select(gem, args)
    if not todo:
        sys.exit("Niets geselecteerd: gebruik --kalibratie, --provincie, --gemeente of --alles")
    tot_new = tot_old = 0
    for g in todo:
        gdir = gemeente_dir(g)
        if not (gdir / "bronnen.json").exists():
            print(f"  {g['gm_code']} {g['gemeente']}: nog niet opgehaald")
            continue
        s = schrijf(gdir)
        tot_new += s["tekens"]
        tot_old += s["extract_tekens_oud"]
        print(f"  {s['gm_code']} {s['gemeente']:<26} {s['tekens']:>7} tekens (extracten: {s['extract_tekens_oud']:>8}) "
              f"kern {s['kern']}, beleid {s['kapbeleid']}, leges {s['leges']}, omgevingsplan {s['omgevingsplan']}, "
              f"overig {s['overig']}, niet opgenomen {s['niet_opgenomen']}")
    if tot_old:
        print(f"Totaal {tot_new} tekens tegen {tot_old} in de extracten ({tot_new / tot_old:.0%}).")


def cmd_citaten(args):
    from .citaten import controleer
    from .scores import RIJEN

    gem = load_gemeenten()
    todo = select(gem, args)
    if not todo:
        sys.exit("Niets geselecteerd: gebruik --kalibratie, --provincie, --gemeente of --alles")
    tot = mis = 0
    for g in todo:
        if not (RIJEN / f"{g['gm_code']}.json").exists():
            continue
        n, missend = controleer(g["gm_code"], gemeente_dir(g))
        tot += n
        mis += len(missend)
        print(f"  {g['gm_code']} {g['gemeente']:<26} {n - len(missend)}/{n} citaatfragmenten gevonden")
        for veld, f in missend:
            print(f"      NIET GEVONDEN [{veld}] {f[:140]}")
    print(f"Totaal {tot - mis}/{tot} gevonden in tekst/*.md of dossier.md. "
          "Niet gevonden kan ook betekenen: andere bron (Bal, website, lijst) of ingekort citaat.")


def cmd_dso(args):
    from . import dso
    gem = select(load_gemeenten(), args)
    uit = DATA / "dso_omgevingsplan.jsonl"
    oud = {}
    if uit.exists():
        for line in uit.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            oud[r["gm_code"]] = r
    for i, g in enumerate(gem, 1):
        try:
            r = dso.omgevingsplan(g["gm_code"], gemeente_dir(g))
        except dso.DSOError as e:
            print(f"[{i}/{len(gem)}] {g['gm_code']} {g['gemeente']}: FOUT {e}; gestopt", flush=True)
            break
        oud[r["gm_code"]] = r
        sterk = [a["kop"] for a in r["kapartikelen"] if a.get("sterk") and not a.get("bruidsschat_aanvraag")]
        plan = "geen omgevingsplan" if not r["omgevingsplan"] else f"{len(r['kapartikelen'])} treffers, {len(sterk)} sterk buiten bruidsschat"
        print(f"[{i}/{len(gem)}] {g['gm_code']} {g['gemeente']}: {plan} {'; '.join(sterk)[:160]}", flush=True)
        uit.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in oud.values()), encoding="utf-8")


def cmd_samenvatting(args):
    from .samenvatting import schrijf
    schrijf()


def cmd_kaart(args):
    from .kaart import maak_kaarten

    for name in maak_kaarten():
        print(f"output/{name}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m bomen", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("gemeenten", help="CBS-gemeentelijst 2026 ophalen")
    p.add_argument("--refresh", action="store_true")
    p.set_defaults(func=cmd_gemeenten)

    p = sub.add_parser("namen", help="naamcontrole CVDR/bekendmakingen")
    p.add_argument("--workers", type=int, default=4)
    p.set_defaults(func=cmd_namen)

    p = sub.add_parser("ophalen", help="bronnen ophalen")
    p.add_argument("--kalibratie", action="store_true", help="de vijf kalibratiegemeenten")
    p.add_argument("--provincie", action="append", help="herhaalbaar, bijv. --provincie Zeeland")
    p.add_argument("--gemeente", action="append", help="GM-code of naam, herhaalbaar")
    p.add_argument("--alles", action="store_true", help="alle gemeenten in de batchvolgorde")
    p.add_argument("--refresh", action="store_true", help="opnieuw ophalen, ook als bestand al bestaat")
    p.add_argument("--geen-bekendmakingen", action="store_true")
    p.add_argument("--alle-documenten", action="store_true",
                   help="ook geldende regelingen downloaden waarvan de titel niet relevant lijkt")
    p.add_argument("--steekproef", type=int, default=10, help="aantal recente kapbesluiten volledig ophalen")
    p.add_argument("--workers", type=int, default=3)
    p.set_defaults(func=cmd_ophalen)

    p = sub.add_parser("csv", help="CSV en afwijkingenlijst uit output/rijen/*.json")
    p.add_argument("--provincie", action="append", help="per provincie; zonder: alle gemeenten samen")
    p.set_defaults(func=cmd_csv)

    p = sub.add_parser("citaten", help="zoek elk citaat uit output/rijen/*.json terug in de brontekst")
    p.add_argument("--kalibratie", action="store_true")
    p.add_argument("--provincie", action="append")
    p.add_argument("--gemeente", action="append")
    p.add_argument("--alles", action="store_true")
    p.set_defaults(func=cmd_citaten)

    p = sub.add_parser("dossier", help="compact dossier per gemeente (dossier.md) voor de scorende agent")
    p.add_argument("--kalibratie", action="store_true")
    p.add_argument("--provincie", action="append")
    p.add_argument("--gemeente", action="append")
    p.add_argument("--alles", action="store_true")
    p.set_defaults(func=cmd_dossier)

    p = sub.add_parser("kaart", help="kaarten (SVG en GeoJSON) uit output/rijen/*.json")
    p.set_defaults(func=cmd_kaart)

    p = sub.add_parser("dso", help="omgevingsplan uit het DSO doorzoeken op kapregels (1 verzoek per 3 s)")
    p.add_argument("--kalibratie", action="store_true")
    p.add_argument("--provincie", action="append")
    p.add_argument("--gemeente", action="append")
    p.add_argument("--alles", action="store_true")
    p.set_defaults(func=cmd_dso)

    p = sub.add_parser("samenvatting", help="cijfers voor het rapport (output/samenvatting.md)")
    p.set_defaults(func=cmd_samenvatting)

    p = sub.add_parser("status", help="overzicht van opgehaalde gemeenten")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
