# Afwijkingen — Fryslân

18 gemeenten gescoord. Hieronder staan de gemeenten met status "niet gevonden" of "onzeker", of met betrouwbaarheid "laag".

## Lijstsystemen waarvan de lijst niet is ingezien

- **Ameland** (GM0060): Bomenlijst/register beeldbepalende en monumentale bomen niet gevonden; onbekend of er particuliere bomen op staan en hoeveel. Omgevingsplan in het DSO niet ingezien. Bezwaar en beroep niet apart gelezen.
- **De Fryske Marren** (GM1940): Bomenlijst niet ingezien en niet bekend of er particuliere bomen op staan; de lijst wordt in de Groenvisie 2023-2027 wel genoemd ("Monumentale bomen ... staan vermeld op de gemeentelijke bomenlijst"), maar die tekst zegt niets over eigendom.
- **Heerenveen** (GM0074): De Bomenlijst zelf (aantal bomen, hoeveel particulier) is niet ingezien; de lijst staat niet in CVDR308389_1 en kon op de gemeentelijke website niet worden gevonden.
- **Súdwest-Fryslân** (GM1900): Kernbron ontbreekt: het Bomenbeleidsplan (met bomenregister en begrenzing van groenclusters) zit niet in het dossier en is niet gevonden. Daardoor onbekend hoeveel particuliere bomen onder het regime vallen (D tussen 0 en 2) en of het bomenbeleidsplan herplant of handhaving verder regelt.
- **Terschelling** (GM0093): Bomenlijst (bijlagen 2 tot en met 4 bij CVDR84374_3, of lijst op de gemeentelijke website) niet ingezien; aantal en particulier aandeel onbekend. Omgevingsplan in het DSO niet ingezien. Bezwaar en beroep niet apart gelezen.

## Overige afwijkingen

- **Vlieland** (GM0096), status ok, betrouwbaarheid laag: Kaart van het gebied 'Wonen in het bos' (bijlage 5 verwijst naar een kaart) en de actuele jaarlijkse lijst op de gemeentelijke website niet ingezien, dus het aandeel van de gemeente dat onder categorie 2 valt is niet vast te stellen (D 1-2). Omgevingsplan in het DSO niet ingezien. Bezwaar en beroep niet apart gelezen.
- **Leeuwarden** (GM0080), status ok, betrouwbaarheid laag: De afzonderlijke bomenlijst op de gemeentelijke website is niet ingezien (aantallen komen uit het vaststellingsdocument). Het kapmeldingsartikel waarnaar de toelichting verwijst, staat niet in de APV-tekst.
- **Waadhoeke** (GM1949), status onzeker, betrouwbaarheid laag: Lijst ingezien (bijlage bij CVDR742333_1, 2.708 bomen), maar zonder eigendomsgegevens. Of er particuliere bomen op staan is niet vast te stellen; kaart of kadasterkoppeling niet gevonden. Daarom D 1 met bereik 0-1.
- **Dantumadiel** (GM1891), status ok, betrouwbaarheid laag: Bomenlijst met markante bomen niet ingezien (telt niet voor D). Omgevingsplan in het DSO niet ingezien.
- **Tytsjerksteradiel** (GM0737), status ok, betrouwbaarheid laag: -

## Bereik loopt over een categoriegrens

- Vlieland: 40 (3 Gemiddeld), bereik 18-43
- Ameland: 22 (2 Soepel), bereik 0-22
- Leeuwarden: 20 (2 Soepel), bereik 20-43
- De Fryske Marren: 20 (2 Soepel), bereik 0-20
- Waadhoeke: 18 (1 Zeer soepel), bereik 0-20
- Dantumadiel: 17 (1 Zeer soepel), bereik 17-33
- Tytsjerksteradiel: 17 (1 Zeer soepel), bereik 17-33
- Súdwest-Fryslân: 17 (1 Zeer soepel), bereik 0-37

## Modelsignalen

- Schiermonnikoog: De tuinuitzondering hangt af van zichtbaarheid vanaf de openbare weg; het model kent alleen 'achtertuin' of 'strook langs de weg'. Ik heb de correctie -1 toegepast als gelijkwaardig aan alleen voorerf. Zichtbare achtertuinen blijven beschermd, dus de dekking kan groter zijn dan D3 suggereert (D4 min 1 is een grove benadering).
- Harlingen: Uitzondering met een leeftijdsvoorwaarde (bomen van 49 jaar of jonger op percelen tot 300 m2). De D-correctie kent alleen 'alle percelen tot een oppervlakte'; hier is de uitzondering smaller, omdat oudere bomen beschermd blijven. Toegepast zoals opgedragen: D4 wordt D3.
- Harlingen: Drempel 15 cm diameter (47 cm omtrek) is zeer laag; de score D3 komt hier uitsluitend uit de correctie.
- Smallingerland: Omgevingsplanregel die de drempel als uitzondering formuleert ("minder dan 63 cm") terwijl de meethoogte alleen in de aanvraagvereisten (art. 10.8) staat.
- Noardeast-Fryslân: Drempel gegeven als diameter van 30 cm met in dezelfde definitie een verwijzing naar 'stamomtrek van de dikste stam'. Omgerekend 94,2 cm omtrek, vlak onder de grens van 100 cm van D2: bij een kleine afwijking in de omrekening of een lezing als omtrek verandert D.
- Weststellingwerf: Drempel precies op 100 cm: ligt op de grens tussen D2 (>100) en D3 (60-100); toegepast als D3.
- Achtkarspelen: Erf- en tuinuitzondering op afstand (20 m van de gevel) valt niet netjes onder 'achter- of zijtuinen' of 'alle erven'; ik heb de correctie -1 toegepast omdat het merendeel van de gewone tuinbomen binnen die afstand valt. Een model-kwestie: afstandsgrenzen (bijv. 20 m) en uitzonderingen op zichtbaarheid vanaf de weg zouden een vaste regel nodig hebben.
- Achtkarspelen: Een handhavingsleidraad met 'bestuurlijke boete' als tweede sanctie maar met alleen een dwangsombedrag telt niet als S2/S3; het model kent geen aparte plek voor beleid dat een boete noemt zonder wettelijke grondslag in de regeling.
- Vlieland: Lijstsysteem dat via een bijlage met gebiedscategorieen (hele kavels in een woonwijk in het bos) ook particuliere bomen buiten een individuele lijst beschermt: het model kent dan D1 (lijst) of D2 (gebieden), maar de omvang van het gebied bepaalt of D2 terecht is; zonder kaart blijft dat onzeker.
- Vlieland: Beleidsregel (beleidskaders) zegt 'zal ... verleend worden met herplantplicht', terwijl de APV 'kan' zegt; scoring volgt de besluitregel voor tegenstrijdige teksten (H2).
- Opsterland: Soortgebonden verbod (alleen eik/beuk): D-correctie noemt dit niet expliciet; toegepast als ruime uitzondering.
- Ooststellingwerf: Leeftijdscriterium (80 jaar) en omtrekdrempel naast elkaar: het model scoort alleen op omtrek.
- Ooststellingwerf: Aanlegvergunning voor alle houtopstanden in een bestemmingsfunctie (H21 Agrarisch) zonder drempel: valt onder 'aangewezen gebieden' D2, maar omvang onbekend.
- Ameland: Het model scoort de strengheid van een lijstsysteem met D1 even hoog als de opbouw van I (W2 H2 S3 = 7 van 9), terwijl de lijst mogelijk geen enkele particuliere boom bevat (dan D0 en strengheid 0). De puntschatting D1 bij niet-ingeziene lijst geeft hier een score 22 die niet op feiten rust.
- Leeuwarden: Een regel op aantal (vergunning pas bij 10 of meer bomen per jaar per gebied, hele gemeente) past niet in de D-schaal (omtrek of aangewezen bomen/gebieden). Voor een particulier met een paar bomen is het effect dat alleen lijstbomen beschermd zijn (D1); voor grote kap geldt een vergunning.
- Leeuwarden: H: de beleidsregel verplicht compensatie (€ 2000) voor lijstbomen, maar herplant 'kan' alleen; het model kent geen aparte score voor 'verplichte financiële compensatie zonder standaard herplant'.
- Waadhoeke: Lijst ingezien maar zonder eigendomsgegevens: particulier versus gemeentelijk niet vast te stellen. Het model kent geen tussenstand tussen 'lijst niet ingezien' en 'particuliere bomen aanwezig'; D1 met bereik 0-1 en betrouwbaarheid laag.
- Waadhoeke: Een boom wordt hier gedefinieerd met een omvangdrempel (10 cm omtrek) die in de praktijk geen werking heeft, omdat alleen lijstbomen beschermd zijn.
- Dantumadiel: Tuinen en erven bij woningen zijn volledig uitgezonderd, maar de rest van de gemeente (bijv. bomen buiten tuinen, op bedrijfsterreinen en in het buitengebied) is wel beschermd met een lage drempel. Het model geeft dan D3, terwijl de dekking voor gewone woningbezitters in feite nul is; het rapport moet dit als feit noemen.
- Tytsjerksteradiel: Tytsjerksteradiel combineert een hoge omtrekdrempel (150 cm, D2) met een soortuitzondering voor populier, wilg, els en berk (correctie -1). Het model telt beide; of dat dubbel tellen is, is niet bepaald. Resultaat D1 (17) tegenover D2 (33) verandert de categorie van Zeer soepel naar Soepel.
- Heerenveen: Lijstsysteem waarbij de lijst niet in de brontekst staat en niet online is gevonden; D blijft daardoor onzeker (betrouwbaarheid laag).
- Súdwest-Fryslân: Verbod gekoppeld aan 'groencluster' (begrensd gebied, begrenzing in beleidsplan) naast een register: past niet netjes in D1 (individuele bomen) of D2 (aangewezen gebieden) zolang de omvang niet bekend is.
- Súdwest-Fryslân: Regime verwijst voor de reikwijdte naar een beleidsplan (niet in CVDR-dossier): kernbron ontbreekt.
- Terschelling: Definitie 'monumentaal' (80 jaar en levensverwachting 10 jaar) bepaalt de lijst; de lijst zelf is hier niet ingezien, waardoor D en dus de score geen feitelijke basis heeft (bereik 0-17).
