# Opdracht voor een scorende agent

Je scoort de kapregels voor bomen op **particulier terrein** van een paar Nederlandse gemeenten. Je werkt alleen met primaire bronteksten die je zelf leest.

## Lees eerst

1. `INTENT.md` helemaal. Belangrijkst: ZOEKSTRATEGIE, WAT JE PER GEMEENTE VASTLEGT (a tot en met i, inclusief f2 en f3), SCORINGSMODEL v2.3, ONZEKERHEID en WERKREGELS. Bij KALIBRATIEGEMEENTEN staan uitgewerkte voorbeelden.
2. De docstring bovenaan `bomen/scores.py`. Daarin staat het JSON-formaat dat je moet opleveren.

## Bronnen per gemeente

Map: `data/gemeenten/<provincie>/<GM-code>_<naam>/`

- `dossier.md` is het startpunt. Lees het helemaal. Het bevat letterlijk alle passages over kap: de kapartikelen met definities en strafbepalingen, beleidsregels, de legesrij, de omgevingsplanartikelen en de bekendmakingen.
- Citeer uit het dossier. Ga alleen naar `tekst/<id>.md` (met grep, niet helemaal lezen) als iets ontbreekt, bijvoorbeeld een strafbepaling die alleen artikelnummers noemt, of als een passage is afgekapt.
- `cvdr/*.xml` is de ongewijzigde primaire tekst; `regelingen.jsonl` bevat ook de vervallen versies.
- `volledig_gelezen` mag true zijn als de kapartikelen volledig in het dossier staan.

## Werkwijze

- Stel vast welke tekst vandaag de kap op particulier terrein regelt. Kijk ook of er een beleidsregel over herplant, compensatie of handhaving is (die telt mee voor H, zie v2.3).
- Bij een lijstsysteem: probeer kort (hooguit een paar curl-requests) de bomenlijst of -kaart op de gemeentelijke website te vinden. Stel vast of er particuliere bomen op staan. Lukt dat niet, raad dan niet.
- Gebruik geen kennis uit je trainingsdata als bewijs. Elke W- en H-score heeft een letterlijk citaat nodig met bestand en artikel.
- **Schrijf alle tekstvelden in het Nederlands.** Citaten blijven letterlijk.
- Reken I, strengheid, bereik, categorie en betrouwbaarheid **niet** zelf uit. Dat doet `python3 -m bomen csv`. Lever alleen D, W, H en S met punt, min en max.

## Oplevering

- Schrijf per gemeente één bestand: `output/rijen/<GM-code>.json`, met alle velden uit de docstring van scores.py.
- Controleer daarna vanuit de projectmap met `python3 -m bomen csv --provincie <provincie>`. Staat jouw bestand bij ONGELDIG, verbeter het dan.
- De bestanden in output/rijen/ worden openbaar. Neem geen namen, adressen of perceelnummers van particulieren op, ook niet uit bomenlijsten of bekendmakingen. Verwijs naar een besluit met het kenmerk (bijv. gmb-2026-142843) en tel bomen in plaats van ze op te sommen.
- Wijzig geen andere bestanden in het project.
- Geef in je eindbericht per gemeente één regel: D/W/H/S, de belangrijkste bron en de open punten. Noem ook modelsignalen.
