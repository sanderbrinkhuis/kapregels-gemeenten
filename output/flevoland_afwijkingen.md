# Afwijkingen — Flevoland

6 gemeenten gescoord. Hieronder staan de gemeenten met status "niet gevonden" of "onzeker", of met betrouwbaarheid "laag".

## Lijstsystemen waarvan de lijst niet is ingezien

- **Lelystad** (GM0995): Kaart bijzondere bomen en bebouwingscontour houtkap niet ingezien (alleen in het DSO beschikbaar). Het Bomenbeleidsplan (CVDR672052_1) noemt wel 'gemeentelijk of particulier' bij bijzondere bomen, dus particuliere bomen op de kaart zijn aannemelijk, maar de kaart zelf is niet gezien. Regels van het tijdelijk deel (oude bestemmingsplannen) kunnen op locatie afwijken (art. 15.21 lid 2).

## Overige afwijkingen

- **Zeewolde** (GM0050), status onzeker, betrouwbaarheid laag: Lijst ingezien op zeewolde.nl/boom-kappen (10 posten); niet bevestigd dat dit de door het college vastgestelde Bomenlijst is. Alle posten staan in openbaar gebied (berm, park, speelplein); alleen de bomen bij een basisschool en een jongerencentrum kunnen op terrein van een ander dan de gemeente staan (eigendom niet vastgesteld). Daarom D1 met minimum 0. Boombeleidsplan Zeewolde 2019 niet ingezien (niet in CVDR; mogelijk herplantbeleid).

## Bereik loopt over een categoriegrens

Geen.

## Modelsignalen

- Urk: Melding met verbodsbevoegdheid van het college zonder genoemde criteria (art. 3.7.2 VFL Urk): het model kent W0 voor 'melding zonder weigeringsmogelijkheid' en W1-3 voor vergunningen, maar niet deze tussenvorm. Ook is onduidelijk of D een melding met verbodsbevoegdheid als 'toestemmingsplicht' meetelt. Daarom bereik D 1-3 en W 0-2. Opgelost in model v2.3 (melding met verbodsmogelijkheid telt voor D; zonder criteria W = 1; voorbeeldboom 'melden').
- Urk: Boom A/B-velden kennen alleen 'vergunning ja/nee'; een meldplicht (boom A in Urk) past daar niet in. Opgelost in model v2.3 (melding met verbodsmogelijkheid telt voor D; zonder criteria W = 1; voorbeeldboom 'melden').
- Noordoostpolder: Het model kent geen goede plaats voor een regime dat alleen erfsingels en wegbeplanting buiten de kom beschermt. D2 ('aangewezen structuren') is gekozen; in een polder met veel erven kan de dekking in het buitengebied groot zijn, terwijl de bebouwde kom vrij blijft.
- Noordoostpolder: Een beleidsregel die hoort bij een ingetrokken verordening (Bomenverordening 2005) blijft door een overgangsbepaling (VFL 12.1.2 lid 5) gelden.
- Noordoostpolder: Strengheid 40 valt precies op de categoriegrens; een kleine wijziging in W of H verandert de categorie.
- Zeewolde: Lijst met vrijwel alleen gemeentelijke bomen: het model heeft geen D-waarde voor 'regeling bestaat, maar bijna geen particuliere bomen'. Volgens D0 ('alleen gemeentelijke bomen') zou de score 0 zijn; hier is D1 met minimum 0 gekozen omdat het eigendom van twee posten niet vaststaat.
- Dronten: Kleinste lijst tot nu toe (5 bomen): D1 geeft voor 5 bomen in een gemeente van ca. 40.000 inwoners dezelfde dekkingsscore als een lijst van honderden bomen; het model meet geen aantal bomen. Besluit model v2.3: D blijft 1; het aantal staat in de kolommen 'bomenlijst totaal/particulier'.
- Lelystad: Buitengebied-regime met uitzondering voor alle particuliere kavels <= 5.000 m2: niet duidelijk onder te brengen bij 'aangewezen gebieden' (D2) of de correctie -1; bij Lelystad leidt dat tot D1 met bereik 1-2. Opgelost in model v2.3 (uitzondering voor particuliere percelen tot een oppervlakte valt onder de correctie -1).
- Lelystad: Bebouwingscontour houtkap als kaartobject in het omgevingsplan: de contour zelf is niet ingezien, dus de omvang van het 'buitengebied-regime' is niet te bepalen.
- Almere: Aanvraagvereisten voor vellen van houtopstand in het omgevingsplan (art. 22.299) zonder bijbehorende vergunningplicht: standaardtekst uit het tijdelijk deel; geen aanwijzing voor een kapregel, maar het model kan zo'n restant niet vangen. Geregeld in model v2.3: scoort niet, genoteerd als 'restant bruidsschat'.
