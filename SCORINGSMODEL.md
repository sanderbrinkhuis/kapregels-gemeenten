# Het scoringsmodel uitgelegd (v2.3)

Dit document legt uit hoe het model in [INTENT.md](INTENT.md) een gemeente een strengheidsscore geeft. INTENT.md blijft de bindende versie; dit is de toelichting.

## Wat meet het model?

Het model beantwoordt één vraag: **hoe streng zijn de regels voor iemand die een boom in de eigen tuin wil kappen?**

Daarvoor kijkt het naar twee dingen:

1. **Dekking (D):** voor hoeveel particuliere bomen geldt de regel überhaupt?
2. **Intensiteit (I):** als de regel geldt, hoe zwaar is die dan?

Een gemeente met zware regels voor maar vijf bomen op een lijst is voor de gemiddelde tuineigenaar niet streng. Daarom weegt dekking het zwaarst.

## Dekking: D (0 tot 4)

| D | Wanneer | Voorbeeld |
|---|---|---|
| 0 | Geen vergunning nodig voor particuliere bomen | Alleen gemeentebomen beschermd |
| 1 | Alleen bomen die op een lijst of kaart staan | Ameland, Vaals, Gorinchem |
| 2 | Aangewezen gebieden, of overal maar alleen dikke bomen (omtrek > 100 cm) | Alleen bomen in een beschermd dorpsgezicht |
| 3 | Overal, vanaf een middelmatige dikte (omtrek 60–100 cm) | Apeldoorn (65 cm) |
| 4 | Overal, ook dunne bomen (omtrek < 60 cm) of zonder ondergrens | Amsterdam (31 cm) |

**Stamomtrek** is de omtrek van de stam, meestal gemeten op 1,30 m hoogte. Noemt een gemeente een diameter, dan rekenen we die om: omtrek = diameter × 3,14. Een stam van 20 cm doorsnee heeft dus een omtrek van ongeveer 63 cm.

**Kleine gebieden tellen niet.** Geldt een kapregel maar voor één wijk of één beschermd gezicht, dan verandert D niet. Zo'n regel noemen we wel in de opmerkingen. Een gebiedsregel telt alleen als die een flink deel van de gemeente bestrijkt, bijvoorbeeld alle dorpskernen samen.

**Correctie voor grote uitzonderingen.** Zijn bijvoorbeeld alle achtertuinen of alle coniferen vrijgesteld, dan gaat D één punt omlaag, maar niet onder 1. Gewone uitzonderingen tellen niet mee, zoals een dode of gevaarlijke boom.

## Intensiteit: I = W + H + S (0 tot 9)

Intensiteit bestaat uit drie onderdelen van elk 0 tot 3.

### W — Hoe kritisch kijkt de gemeente naar een aanvraag?

| W | Betekenis | Typische formulering |
|---|---|---|
| 0 | Geen toets | Alleen melden, of vergunning van rechtswege |
| 1 | Ja, tenzij | "wordt verleend, tenzij…" |
| 2 | Afweging | "kan worden geweigerd op grond van natuurwaarde, landschap…" |
| 3 | Nee, tenzij | "slechts bij uitzondering", "in beginsel geen vergunning" |

De meeste gemeenten volgen de modeltekst van de VNG. Die tekst somt een vaste lijst weigeringsgronden op. Dat scoren we als W = 2.

### H — Moet je een nieuwe boom planten of betalen?

| H | Betekenis |
|---|---|
| 0 | Geen regel over herplant |
| 1 | De gemeente *kan* herplant eisen |
| 2 | Herplant is de standaard ("wordt", "in beginsel") |
| 3 | Standaard herplant én verplicht betalen, bijvoorbeeld de waarde van de boom in een herplantfonds |

Twee regels voor lastige gevallen:

- **De beleidsregel beslist.** Zegt de verordening "kan", maar staat in een beleidsregel van de gemeente "moet" of "wordt", dan telt de beleidsregel. Een **beleidsregel** is een vaste werkafspraak die de gemeente zelf heeft vastgesteld en waaraan ze zich moet houden. Voorbeeld: Amsterdam. De verordening zegt dat betalen in het herplantfonds "kan". De beleidsregel zegt dat wie niet kan herplanten "financieel moeten compenseren". Amsterdam krijgt daarom H = 3.
- **Een uitgangspunt is geen plicht.** Schrijft de gemeente in een nota dat herplant "het uitgangspunt" is, maar beslist ze per geval, dan telt de tekst van de regeling zelf. Voorbeeld: Apeldoorn. De nota noemt herplant het uitgangspunt, maar de APV zegt "kan". Apeldoorn krijgt H = 1.

**De uitweg bij herplant.** Naast de score leggen we per gemeente vast of de tekst een uitweg biedt. Denk aan "kan" (de gemeente mag het eisen, maar hoeft niet), "in beginsel", "tenzij zwaarwegende argumenten zich daartegen verzetten" of betalen in plaats van planten. Die uitweg verandert de score niet. Het rapport bespreekt wel hoe vaak elke uitweg voorkomt.

### S — Wat gebeurt er als je zonder vergunning kapt?

| S | Betekenis |
|---|---|
| 0 | Alleen de algemene middelen, zoals een dwangsom |
| 1 | Speciale regel voor kap, zoals een strafbaar feit (economisch delict) of verplichte herplant na illegale kap |
| 2 | Een **bestuurlijke boete** in de regeling: de gemeente legt zelf een geldboete op, zonder tussenkomst van de rechter |
| 3 | Bestuurlijke boete plus vastgelegd beleid, bijvoorbeeld een boete die direct volgt of die meestijgt met de waarde van de boom |

## Van D en I naar één score

**Strengheid = D/4 × (40 + 60 × I/9)**, afgerond op een heel getal.

Dit doet de formule:

- **Zonder dekking geen strengheid.** Bij D = 0 is de score altijd 0.
- **Dekking zet het plafond.** Een gemeente met alleen een bomenlijst (D = 1) haalt maximaal 25 punten, hoe zwaar de regels ook zijn.
- **Er is een basisscore van 40.** Het bestaan van een vergunningplicht telt al mee, ook zonder zware toets, herplant of sanctie. De intensiteit voegt daar maximaal 60 punten aan toe.

Mogelijke scores per dekkingsniveau:

| D | Minimaal (I = 0) | Maximaal (I = 9) |
|---|---|---|
| 1 | 10 | 25 |
| 2 | 20 | 50 |
| 3 | 30 | 75 |
| 4 | 40 | 100 |

### Categorieën

| Score | Categorie |
|---|---|
| 0–19 | 1 Zeer soepel |
| 20–39 | 2 Soepel |
| 40–59 | 3 Gemiddeld |
| 60–79 | 4 Streng |
| 80–100 | 5 Zeer streng |

### Rekenvoorbeeld: Apeldoorn

- Bomen vanaf 65 cm omtrek, in de hele gemeente → **D = 3**
- "Kan worden geweigerd" op natuur- en landschapswaarden → **W = 2**
- De gemeente *kan* herplant eisen → **H = 1**
- Kappen zonder vergunning is een economisch delict → **S = 1**

I = 2 + 1 + 1 = 4. Strengheid = 3/4 × (40 + 60 × 4/9) = 0,75 × 66,7 = **50 → Gemiddeld**.

## Onzekerheid

Niet alles is altijd vast te stellen. Een bomenlijst staat bijvoorbeeld niet online. Dan geven we:

- een **puntschatting**: we scoren alleen wat we gelezen hebben. Een onderdeel dat we niet hebben gelezen, krijgt de laagste waarde. Bij een lijst die we niet hebben gezien, gaan we uit van D = 1.
- een **bereik**: de laagste en hoogste score die mogelijk is.

**Betrouwbaarheid** is "hoog" als de volledige tekst is gelezen en het bereik binnen één categorie valt. Ze is "laag" als de dekking onzeker is. In alle andere gevallen is ze "middel".

## Wat is er veranderd ten opzichte van v2?

| Onderdeel | v2 | v2.1 |
|---|---|---|
| Diameter of omtrek | Twee sets grenzen die niet precies op elkaar aansloten | Altijd omrekenen naar omtrek; die bepaalt de score |
| Lijst plus breed regime | Niet geregeld | Het breedste regime bepaalt D |
| W1 tegenover W2 | Overlap bij een vaste lijst weigeringsgronden | Vaste lijst met waarden = W2; W1 alleen bij "wordt verleend, tenzij" |
| H3 | "plus financiële compensatie" | Betalen moet verplicht zijn; een *kan*-bepaling telt niet |
| S en het omgevingsplan | Niet geregeld | Eerst vaststellen of kap in het omgevingsplan automatisch een economisch delict is (stap 1a); de route altijd noteren |
| Puntschatting | Niet geregeld (kalibratie deed het verschillend) | Alleen gelezen tekst telt; bij een niet-ingeziene lijst D = 1 |
| Kalibratie Amsterdam | Bereik 73–80 | Bereik 73–93 (S onbekend), loopt over de grens naar Zeer streng |

Na de kalibratie (14-11-2026) kwamen daar in v2.2 vier besluiten bij:

| Onderdeel | v2.1 | v2.2 |
|---|---|---|
| Verordening "kan", beleidsregel "moet" | Niet geregeld | De beleidsregel telt, voor H2 en H3 |
| "Uitgangspunt herplant" per geval | Niet geregeld | Telt niet als vast voorschrift; de tekst van de regeling beslist |
| Gebiedsregel voor één wijk | Kon D verhogen ("breedste regime") | Telt niet mee voor D; alleen in de opmerkingen |
| Label "juridische plaats onzeker" | Bij elke wijziging na 2024 | Alleen als de twijfel een score kan veranderen |
| Uitweg bij herplant | Niet vastgelegd | Eigen kolom met de letterlijke formulering |

Gevolg voor de kalibratie: Amsterdam gaat van 73 (Streng) naar 80 (Zeer streng). De andere vier blijven gelijk: Apeldoorn 50, Ameland 22, Vaals 18 en Gorinchem 17.

Na Flevoland (14-11-2026) kwamen daar in v2.3 vier besluiten bij. Ze leggen vooral feiten vast en veranderen geen enkele score die al bestond:

| Onderdeel | v2.2 | v2.3 |
|---|---|---|
| Melding waarbij de gemeente de kap kan verbieden | Niet geregeld (W0 alleen voor melding zonder verbod) | Telt voor D als toestemmingsplicht; W volgt de criteria voor het verbod (geen criteria = W1). Voorbeeldboom krijgt het antwoord "melden" |
| Particuliere percelen tot een bepaalde oppervlakte uitgezonderd | Niet letterlijk genoemd | Valt onder de correctie "alle erven of bouwkavels" (−1) |
| Aantal bomen op de lijst | Niet vastgelegd | D blijft 1, ongeacht het aantal. Het aantal (totaal en particulier) wordt een eigen kolom |
| Aanvraagvereisten zonder vergunningplicht (art. 22.299) | Niet geregeld | Scoort niet; heet "restant bruidsschat" in de kolom juridische plaats |

Na Drenthe (14-11-2026) kwamen er twee verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Kapregel alleen in een strook langs de weg of alleen in het voorerf | Telt als uitzondering van achtertuinen: D op de drempel, min 1. Gevolg: De Wolden van 33 naar 17, Hoogeveen van 40 naar 20 |
| Peildatum | De regels zoals ze gelden op de dag van scoren. Een beleidsregel die al in werking is, telt mee |
| Uitzonderingen voor tuinen | Achtertuinen, niet zichtbaar vanaf de weg, tuinen tot een bepaalde oppervlakte of binnen een afstand van de gevel tellen als ruime uitzondering (−1), ook in combinatie. Gevolg: Het Hogeland (tuinen < 100 m²) van 55 naar 37; Borger-Odoorn (≤ 500 m² én niet zichtbaar) van 67 naar 50 |
| Andere regels binnen en buiten de bebouwde kom | D per deel bepalen, het hoogste telt. Een regel alleen buiten de kom én buiten tuinen telt als aangewezen gebied (hooguit D2). Gevolg: Opsterland D2 (33), Weststellingwerf D3 (50) |
| Compensatie alleen bij bouwprojecten of na illegale kap | Verhoogt H niet; H gaat over gewone kap met vergunning. Gevolg: Noardeast-Fryslân H1, Het Hogeland en Groningen H2 (bereik smaller) |

Na Limburg (14-11-2026) kwamen er vier verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Sanctie bij een losse verordening of een foute artikelverwijzing | Noemt de legesverordening of de regeling het vellen een omgevingsplanactiviteit, dan S = 1 zonder bereik. Gevolg: Brunssum, Roermond en Peel en Maas S1 zonder bereik |
| Particulier mag een aantal bomen per jaar zonder vergunning kappen | Telt als tuinuitzondering (−1). Gevolg: Roermond D3 zonder bereik |
| Drempel hangt af van de soort eigenaar | D volgt de drempel voor het perceel van een burger (natuurlijk persoon). Gevolg: Heerlen D2 zonder bereik |
| Voorbeeldbomen A en B | Staan in een achtertuin bij een woning op een perceel van ca. 300 m². Gevolg: boom A van "ja" naar "nee" in Harlingen (perceel tot 300 m²) en Borger-Odoorn (tot 500 m²) |

Na Utrecht (14-11-2026) kwamen er deze verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Welk beleid telt naast de verordening | Een beleidsnota, beleidsplan of besluit bij een bomenlijst telt voor W en H als het door college of raad is vastgesteld en in CVDR als geldend staat. Niet: een nota bij een ingetrokken verordening, een plan voor een toekomstig stelsel, of beleid alleen voor gemeentebomen. Gevolg: Rhenen W3 H2, Houten W3 H2, De Bilt H3, Zeist H3 (bereik 1-3), Goes W3 H3, Leudal W3 H2, Valkenburg aan de Geul H2 (allemaal zonder bereik, behalve Zeist); Leusden H1 en Meerssen H1 zonder bereik |
| Bestuurlijke boete | S2 alleen als de regeling zelf (of een boeteverordening) een bestuurlijke boete voor kappen mogelijk maakt, ook zonder bedrag. Alleen in handhavingsbeleid, alleen voor snoeien, of alleen "een boete" = S1. Gevolg: Stichtse Vecht, Vlieland en Midden-Drenthe S2; Oudewater, Woerden, Amersfoort en Pekela S1 (zonder bereik) |
| "Wordt alleen verleend/geweigerd als ... onevenredig" | W2 zonder bereik bij de gebruikelijke waarden. Gevolg: Middelburg, Noardeast-Fryslân en Eemnes W2 zonder bereik |
| "In beginsel" herplant "en/of" financiële bijdrage | H2, maximum 3 (staande lijn bevestigd) |
| Vergunning "wordt geacht te zijn verleend" na de beslistermijn | Procedureregel, geen W0 (staande lijn bevestigd) |
| "Houtopstand" zonder drempel naast "boom" met drempel | D op de drempel voor bomen (staande lijn bevestigd) |

Na Overijssel (14-11-2026) kwamen er deze verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Hoge D alleen door het buitengebied | De regel "D per deel, neem het hoogste" blijft. Dekt de regel buiten de kom ook tuinen en erven, dan telt dat deel gewoon (zonder drempel D4), ook als een tuinboom in de kom vrij is. Het rapport laat voorbeeldbomen A en B als feit voorgaan. Gevolg: Zwartewaterland D2 → D4, Rijssen-Holten D4 zonder bereik; Hof van Twente, Haaksbergen, Hellendoorn en Olst-Wijhe ongewijzigd |
| Ruime uitzondering die maar voor één deel geldt | Correctie −1 alleen op dat deel, daarna het hoogste deel. Gevolg: Kampen D2 → D3 (uitzondering alleen binnen de kom), Raalte D2 → D1 (uitzondering alleen buiten de kom). Eerdere provincies (Nieuwegein, Maastricht, Borger-Odoorn) ongewijzigd |
| "Als de locatie het toelaat wordt ... een herplantplicht meegenomen" | Herplant met voorwaarde: H1, maximum 2. Gevolg: Olst-Wijhe H2 → H1, Raalte H1 met maximum 2 |
| "Wordt geweigerd als de belangen van verlening niet opwegen tegen ... behoud" | W2 zonder bereik (zoals "onevenredig"). Hof van Twente, Deventer en Raalte ongewijzigd |
| "Wordt slechts verleend als ... geen afbreuk wordt gedaan aan" waarden | W2, maximum 3. Ommen ongewijzigd |

Een advies om bij Zeist de −1 voor populieren en wilgen te laten vallen is niet uitgevoerd: de correctieregel noemt "populieren of wilgen ongeacht locatie" uitdrukkelijk als ruime uitzondering. Zeist blijft D1. Een gebiedsregime dat bijna de hele kom dekt, blijft een open modelsignaal.

Na Noord-Holland (15-11-2026) kwamen er deze verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Tuin- of perceeluitzondering met een maatgrens | Alleen −1 als de uitzondering de voorbeeldtuin (perceel ca. 300 m²) vrijstelt. Een grens onder 300 m² geeft geen −1; dit vervangt "ongeacht hoe groot of klein". Gevolg: Haarlem D3 → D4, Utrecht D3 → D4, Zandvoort, Diemen, Alkmaar, Baarn, Soest, Kerkrade en Het Hogeland D2 → D3. Lopik, Gulpen-Wittem en Ouder-Amstel ongewijzigd (andere ruime uitzondering) |
| Achtertuin, tuin of perceel | Geen onderscheid: een maatgrens voor de achtertuin vergelijk je ook met de ca. 300 m² van de voorbeeldtuin. Gevolg: Diemen boom A "onbekend" → "ja" |
| Twee regelingen tegelijk geldend in CVDR | Scoor op de regeling die de gemeente zelf als geldend aanwijst (APV, leges of beleid); de andere telt alleen in het bereik als die strenger is. Ouder-Amstel, Wormerland, Schagen en Hilversum ongewijzigd |
| Artikel tegenover toelichting | Het artikel gaat voor. Oostzaan ongewijzigd (D3, boom A en B "nee") |
| "Doorgaans" of "in principe" herplant in beleid | H1, maximum 2. "Wordt altijd opgelegd" is H2; H3 alleen bij verplichte betaling als herplant niet kan. Blaricum, Laren en Hilversum ongewijzigd |
| Aantal lijstbomen uit een beleidsnota | Mag worden ingevuld met de nota als bron; de lijst blijft "niet ingezien" en het D-bereik blijft. Gevolg: Haarlemmermeer 815 bomen, waarvan 362 particulier |
| "D per deel, neem het hoogste" | Blijft (zie Na Overijssel). Hoorn blijft D4 (67) terwijl voorbeeldboom A en B vrij zijn; het rapport laat de voorbeeldbomen voorgaan |

Waarom geen drempel voor kleine lijsten? Een grens als "minder dan tien bomen telt als geen regeling" is willekeurig en makkelijk te betwisten. Het aantal zelf is een feit dat iedereen kan controleren.

Na Gelderland (15-11-2026) kwamen er deze verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| "Fruitbomen en windschermen om boomgaarden" | Gangbare uitzondering voor boomgaarden: geen −1 en geen bereik. Gevolg: Bergen (NH) D2 → D3 (33 → 50), Tubbergen en Dinkelland D1 → D2 (18 → 37); Hattem en Westerkwartier houden hun score, maar hun D-bereik vervalt |
| Uitzondering voor een deel van de fruitbomen (alleen appel en peer, alleen laagstam) | Is niet "alle fruitbomen": geen −1. Gevolg: Oude IJsselstreek D2 → D3 (40 → 60, Streng). Culemborg ongewijzigd |
| Positieve soortenlijst (de regel geldt alleen voor enkele soorten) | Altijd −1, zonder bereik. Gevolg: Bronckhorst D3 → D2 (50 → 33); Ermelo en Noord-Beveland houden hun score, maar hun D-bereik vervalt. Renkum ongewijzigd |
| Vrijstelling voor een smalle strook bij de gevel | Alleen −1 als de voorbeeldboom in de achtertuin daardoor vrij is. Gevolg: Putten D2 → D3 (33 → 50). Wageningen (3 m) en Achtkarspelen (20 m, wel −1) ongewijzigd |
| Hogere drempel in tuinen en op erven dan op ander terrein in de kom | Scoor op de drempel voor tuinen en erven, naar analogie van "drempel per soort eigenaar". Gevolg: Winterswijk D3 → D2 (50 → 33) |
| Vergunning alleen op een gesloten lijst van gronden ("kan alleen worden verleend als ...") | Weigeren-tenzij: W3 zonder bereik. Gevolg: het W-bereik vervalt bij Rheden, Ede, Scherpenzeel, Oldebroek, West Maas en Waal, Woudenberg, Wierden en Gooise Meren; de puntscores blijven gelijk |
| "Geldelijke boete" ter hoogte van de boomwaarde, opgelegd door het college volgens de regeling | S3 zonder bereik. Gevolg: Maasdriel S3 (was 1-3); de puntscore blijft 22 |
| Voorbeeldboom A of B hangt af van de soort | "Onbekend" laten staan en de soorten in de opmerkingen noemen. Rozendaal, Renkum, Ermelo en Brummen ongewijzigd |

Nieuwe verdeling Gelderland: 19 Zeer soepel, 15 Soepel, 12 Gemiddeld, 4 Streng, 1 Zeer streng.

Na Noord-Brabant (16-11-2026) kwamen er deze verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Kaart met gebieden of structuren die niet is ingezien | Beschermt de verbodstekst zelf een gebied of structuur met drempel: D2 met minimum 1. Wijst de kaart alleen losse objecten aan: D1 met maximum 2. Gevolg: Breda maximum 1 → 2; Maasgouw minimum 0 → 1. Puntscores gelijk |
| Lijst niet ingezien, maar regeling of vastgesteld beleid bevestigt particuliere bomen op de lijst | D-minimum 1 (een website alleen is niet genoeg). Gevolg: alleen de ondergrens verandert bij Westervoort, Houten, Aalsmeer, Haarlemmermeer, Heemskerk, Purmerend, Uithoorn, Geertruidenberg, Rucphen, Roosendaal, Geldrop-Mierlo, Land van Cuijk en Maasgouw. Wie nu D1 zonder bereik heeft, kan betrouwbaarheid "hoog" krijgen, maar blijft in de groep "lijst niet ingezien" |
| Geldbedrag na illegale kap | "Compensatie" of "vergoeding" is herstel: S1. Bestuurlijke boete in de regeling: S2. S3 alleen bij een verplichte boete naar boomwaarde. "Kan"-boete naar boomwaarde: S2, maximum 3. "Boete" alleen in titel of toelichting: maximum één hoger. Gevolg: Heeze-Leende S3 → S2 (60 → 55, Gemiddeld), Maashorst S3 → S1 (40 → 33, Soepel), Heusden S2 → S1 (20 → 18, Zeer soepel); Midden-Drenthe krijgt maximum 3 |
| Groen, oranje en rode redenen | Plicht bij "rode reden" telt voor H als rood ook gewone tuinkap omvat. Gevolg: Tilburg H1 → H2 (50 → 55); Eindhoven en Geldrop-Mierlo ongewijzigd |
| Verplichte vaste storting in plaats van herplant | H2, maximum 3. Gevolg: Bergeijk H3 → H2 (43 → 40) |
| Veel hogere drempel voor coniferen, populieren en wilgen | Telt als uitzondering voor die soorten (−1). Gevolg: Valkenswaard D3 → D2 (50 → 33) |
| Buiten de kom alleen "zelfstandige eenheden" tot 10 are | Is houtopstand ook "een of meer bomen" en is er geen tuinuitzondering: D op de drempel voor dat deel. Gevolg: Veldhoven D2 → D4 (33 → 67) en Altena D2 → D4 (33 → 67), beide Streng; voorbeeldbomen A en B ongewijzigd. Ede, Lochem, Voorst en Winterswijk ongewijzigd (daar geldt buiten de kom ook een drempel) |
| Gebiedsregels met ander doel (archeologie, waterkering, cultuurhistorie) | Tellen niet voor D, ook niet in het bereik. Gevolg: maximum 2 → 1 bij Someren, Arnhem en Terneuzen |
| Welk beleid telt | Nota bij ingetrokken verordening telt als de geldende verordening ernaar verwijst; omgevingsprogramma telt als nota; bij strijd met de regeling gaat de regeling voor. Geen scorewijzigingen |
| Velden herplant en drempelgrens | "Strafbaar (rechter)" alleen met een bepaling "is verplicht daaraan te voldoen" of een strafbepaling die het herplantartikel noemt (Hilvarenbeek → "niets geregeld"). "Vanaf/minimaal 100 cm" = D3, "meer dan 100 cm" = D2 (zo al gescoord) |

Nieuwe verdeling Noord-Brabant: 19 Zeer soepel, 18 Soepel, 13 Gemiddeld, 6 Streng. In de andere provincies verandert alleen het bereik, niet de categorie.

Na Zuid-Holland (16-11-2026) kwamen er deze verduidelijkingen bij. Het model zelf verandert niet:

| Onderdeel | Besluit |
|---|---|
| Herplant "kan", betalen verplicht als herplant niet kan | H2, maximum 3. Gevolg: Den Haag 67 → 73, Nieuwegein 50 → 55, Borsele 37 → 40 (Gemiddeld), Borne 33 → 37, Zuidplas 17 → 18 |
| Bijlage bij de verordening | Hoort bij de regeling en telt mee, ook als die strenger is dan het artikel. Gevolg: Delft H2 → H3 (55 → 60, Streng) |
| Beleid stelt particulieren vrij van herplant | H0, maximum 1. Gevolg: Alphen aan den Rijn 17 → 15, Barendrecht 18 → 17 |
| Zeer hoge drempel (250 cm omtrek of meer) | D1, maximum 2. Gevolg: Rotterdam 33 → 17 (Zeer soepel), Peel en Maas 30 → 15 (Zeer soepel). Nissewaard (220 cm) blijft D2 |
| Vrijstelling binnen een afstand van de gevel | Vanaf 10 m: −1 zonder bereik; onder 10 m geen correctie. Gevolg: Schiedam bereik 33-55 → 33-37; Achtkarspelen (20 m) en Wassenaar (2 m) ongewijzigd |
| Alle tuinen van woningen uitgezonderd | D volgt wat er in tuinen beschermd blijft; alleen lijstbomen: D1, maximum 2. Gevolg: Zwijndrecht 37 → 18, Dantumadiel 50 → 17 (beide Zeer soepel) |
| "Boetebedrag volgens" een strafbepaling | Geen bestuurlijke boete: S1, maximum 2. Gevolg: Kaag en Braassem 23 → 22 |
| Toetsing onbekend | W2 met bereik 1-3; bij verwijzing naar onvindbaar beleid scoor je W op de regeling. Gevolg: Leiderdorp 18 → 20 (Soepel) |
| Aantal lijstbomen uit een stuk bij een ingetrokken verordening | Niet invullen, wel noemen in de opmerkingen. Gevolg: Capelle aan den IJssel aantal leeg |
| Veld herplant niet nakomen | "Strafbaar (rechter)" alleen als een strafbepaling of WED-aanwijzing de herplantplicht dekt (noemt het artikel, of geldt "bij of krachtens" de afdeling of alle artikelen). "Is verplicht daaraan te voldoen" alleen is niet genoeg. Geen invloed op de score. Nagelopen: 202 rijen in alle provincies; type gewijzigd bij 14 (o.a. Ommen, Tiel, Drechterland, Stede Broec, Maassluis, Papendrecht, Vlaardingen, Midden-Delfland → "niets geregeld"; Tubbergen, Dinkelland, Midden-Drenthe, Blaricum, Laren → "dwangsom/bestuursdwang"). Lezing: een uitzondering "voor zover de WED (en de Omgevingswet) van toepassing is" haalt de strafbepaling alleen weg voor wat de WED zelf dekt (kap zonder vergunning), niet voor een opgelegd herplantvoorschrift |
| "In beginsel geen vergunning, anders dan na een belangenafweging" | Belangenafweging: W2, maximum 3. Gevolg: Stadskanaal W3 → W2 (55 → 50), Groningen W3 → W2 (zelfde zin) |
| Vastgesteld plan, inwerkingtreding onzeker | Scoor de tekst als de geldende leges ernaar verwijzen; onzekerheid in het D-bereik en de velden. Gevolg: Stadskanaal (Chw-bestemmingsplan art. 108) gescoord |

Nieuwe verdeling Zuid-Holland: 22 Zeer soepel, 14 Soepel, 9 Gemiddeld, 5 Streng. Totaal 342 gemeenten: 140 Zeer soepel, 92 Soepel, 76 Gemiddeld, 32 Streng, 2 Zeer streng.

## Bewuste keuzes en hun gevolgen

- **Lijstsystemen scoren altijd laag.** Ook een gemeente die lijstbomen zeer streng beschermt, komt niet boven 25 uit. Dat past bij de vraag (de particuliere tuin), maar het zegt niets over hoe goed monumentale bomen beschermd zijn.
- **Dekking over het hele grondgebied begint bij 40.** Een gemeente met een lage drempel komt dus nooit onder "Gemiddeld", ook zonder herplant of sanctie.
- **Sancties hangen deels af van de wet, niet van de gemeente.** Kappen zonder vergunning in strijd met het omgevingsplan is volgens de wet automatisch een economisch delict (Wet op de economische delicten, art. 1a onder 2°, via art. 5.1 Omgevingswet). Een **economisch delict** is een strafbaar feit waarvoor de rechter onder meer een hogere boete kan opleggen dan bij een gewone overtreding. Gemeenten met hun kapregels in het omgevingsplan krijgen daardoor S = 1. Een gemeente met dezelfde regels in een gewone APV-bepaling kan S = 0 krijgen. Dit is besloten op 14-11-2026 (stap 1a). Het rapport moet dit verschil benoemen.
