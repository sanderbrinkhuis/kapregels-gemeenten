# Samenvatting kapregels particuliere bomen, alle gemeenten

Gegenereerd met `python3 -m bomen samenvatting` uit 342 rijen in `output/rijen/` (peildata 14 t/m 16 november 2026). Tellingen in tekstvelden zijn op trefwoord en indicatief.

## Verdeling over de categorieën

| Categorie | Aantal |
|---|---|
| 1 Zeer soepel | 139 |
| 2 Soepel | 92 |
| 3 Gemiddeld | 78 |
| 4 Streng | 31 |
| 5 Zeer streng | 2 |

## Per provincie

| Provincie | Gemeenten | 1 Zeer soepel | 2 Soepel | 3 Gemiddeld | 4 Streng | 5 Zeer streng | Gem. score |
|---|---|---|---|---|---|---|---|
| Groningen | 10 | 1 | 4 | 4 | 1 | 0 | 42.7 |
| Fryslân | 18 | 6 | 5 | 7 | 0 | 0 | 31.7 |
| Drenthe | 12 | 3 | 7 | 2 | 0 | 0 | 30 |
| Overijssel | 25 | 3 | 11 | 5 | 6 | 0 | 42.8 |
| Flevoland | 6 | 4 | 0 | 2 | 0 | 0 | 22 |
| Gelderland | 51 | 19 | 15 | 12 | 4 | 1 | 33.4 |
| Utrecht | 26 | 11 | 6 | 6 | 3 | 0 | 30.4 |
| Noord-Holland | 44 | 25 | 4 | 9 | 5 | 1 | 30.7 |
| Zuid-Holland | 50 | 22 | 14 | 9 | 5 | 0 | 30.4 |
| Zeeland | 13 | 9 | 3 | 1 | 0 | 0 | 21.7 |
| Noord-Brabant | 56 | 19 | 18 | 13 | 6 | 0 | 32.9 |
| Limburg | 31 | 17 | 5 | 8 | 1 | 0 | 29 |

## Tien strengste gemeenten

| Gemeente | Provincie | Score | Bereik |
|---|---|---|---|
| Harderwijk | Gelderland | 80 | 73-80 |
| Amsterdam | Noord-Holland | 80 | 80-80 |
| 's-Gravenhage | Zuid-Holland | 73 | 73-80 |
| Eindhoven | Noord-Brabant | 73 | 73-80 |
| Utrecht | Utrecht | 73 | 73-73 |
| Haarlem | Noord-Holland | 73 | 73-80 |
| Hof van Twente | Overijssel | 73 | 73-73 |
| Gilze en Rijen | Noord-Brabant | 73 | 18-73 |
| Haaksbergen | Overijssel | 73 | 67-73 |
| Wormerland | Noord-Holland | 67 | 67-67 |

## Soepelste gemeenten

Score 0 (10): Albrandswaard, Almere, Bunschoten, Duiven, Hollands Kroon, IJsselstein, Koggenland, Molenlanden, Uitgeest, Zoeterwoude

| Gemeente | Provincie | Score | Bereik |
|---|---|---|---|
| Almere | Flevoland | 0 | 0-0 |
| Duiven | Gelderland | 0 | 0-0 |
| Bunschoten | Utrecht | 0 | 0-17 |
| IJsselstein | Utrecht | 0 | 0-10 |
| Uitgeest | Noord-Holland | 0 | 0-0 |
| Albrandswaard | Zuid-Holland | 0 | 0-0 |
| Zoeterwoude | Zuid-Holland | 0 | 0-40 |
| Koggenland | Noord-Holland | 0 | 0-17 |
| Hollands Kroon | Noord-Holland | 0 | 0-0 |
| Molenlanden | Zuid-Holland | 0 | 0-0 |

## Systemen

| Systeem | Aantal |
|---|---|
| hele kom of gemeente, met drempel | 149 |
| alleen bomen op een lijst of kaart | 146 |
| kaart met gebieden of structuren | 31 |
| geen vergunningplicht voor particuliere bomen | 10 |
| hele kom of gemeente, zonder drempel | 6 |

## Drempels (hele kom of gemeente, met drempel)

149 gemeenten. Laagste 30.0 cm, hoogste 361.0 cm, mediaan 80.0 cm, kwartielen [62.8, 80.0, 100.0].

| Klasse (stamomtrek) | Aantal |
|---|---|
| onder 60 cm | 29 |
| 60 tot 100 cm | 90 |
| boven 100 cm | 30 |

## Voorbeeldboom A (80 cm)

| Provincie | ja | melden | alleen als op lijst | nee | onbekend |
|---|---|---|---|---|---|
| Groningen | 4 | 0 | 2 | 4 | 0 |
| Fryslân | 1 | 0 | 7 | 10 | 0 |
| Drenthe | 0 | 0 | 4 | 7 | 1 |
| Overijssel | 3 | 0 | 5 | 16 | 1 |
| Flevoland | 0 | 1 | 3 | 2 | 0 |
| Gelderland | 8 | 0 | 26 | 15 | 2 |
| Utrecht | 7 | 0 | 15 | 3 | 1 |
| Noord-Holland | 9 | 0 | 22 | 12 | 1 |
| Zuid-Holland | 7 | 0 | 28 | 13 | 2 |
| Zeeland | 0 | 0 | 12 | 1 | 0 |
| Noord-Brabant | 5 | 0 | 38 | 11 | 2 |
| Limburg | 5 | 0 | 19 | 7 | 0 |
| Totaal | 49 | 1 | 181 | 101 | 10 |

## Voorbeeldboom B (40 cm)

| Provincie | ja | melden | alleen als op lijst | nee | onbekend |
|---|---|---|---|---|---|
| Groningen | 1 | 0 | 2 | 7 | 0 |
| Fryslân | 0 | 0 | 7 | 11 | 0 |
| Drenthe | 0 | 0 | 4 | 7 | 1 |
| Overijssel | 0 | 0 | 5 | 19 | 1 |
| Flevoland | 0 | 0 | 4 | 2 | 0 |
| Gelderland | 0 | 0 | 26 | 25 | 0 |
| Utrecht | 1 | 0 | 15 | 9 | 1 |
| Noord-Holland | 2 | 0 | 22 | 20 | 0 |
| Zuid-Holland | 3 | 0 | 28 | 19 | 0 |
| Zeeland | 0 | 0 | 9 | 4 | 0 |
| Noord-Brabant | 1 | 0 | 38 | 15 | 2 |
| Limburg | 0 | 0 | 18 | 13 | 0 |
| Totaal | 8 | 0 | 178 | 151 | 5 |

## Lijstsystemen

{"lijstsystemen": 181, "ingezien": 58, "niet_ingezien": 123, "met_aantal_particulier": 47}

| Gemeente | Provincie | Lijst totaal | Particulier | Lijst ingezien |
|---|---|---|---|---|
| Zwolle | Overijssel | 6947 | 1339 | True |
| Sint-Michielsgestel | Noord-Brabant | 2184 | 1107 | True |
| Nunspeet | Gelderland | 3037 | 1101 | True |
| Kaag en Braassem | Zuid-Holland | 4304 | 986 | True |
| Lingewaard | Gelderland | 929 | 911 | True |
| Leeuwarden | Fryslân | 2444 | 694 | True |
| Goes | Zeeland | 2292 | 676 | True |
| Alphen aan den Rijn | Zuid-Holland | 1478 | 637 | False |
| Medemblik | Noord-Holland | 630 | 630 | True |
| Nieuwkoop | Zuid-Holland | 1406 | 548 | True |
| Middelburg (Z.) | Zeeland | 588 | 533 | True |
| Helmond | Noord-Brabant | 1797 | 533 | True |
| Hulst | Zeeland | 608 | 527 | True |
| Hoeksche Waard | Zuid-Holland | None | 475 | True |
| Teylingen | Zuid-Holland | 1407 | 402 | True |
| Haarlemmermeer | Noord-Holland | 815 | 362 | False |
| De Ronde Venen | Utrecht | 579 | 358 | True |
| Dijk en Waard | Noord-Holland | 648 | 332 | True |
| Zaanstad | Noord-Holland | 331 | 331 | True |
| Oosterhout | Noord-Brabant | 542 | 287 | True |
| Loon op Zand | Noord-Brabant | 238 | 233 | True |
| Voorschoten | Zuid-Holland | 1059 | 227 | True |
| Oudewater | Utrecht | 1233 | 224 | True |
| Heemstede | Noord-Holland | 466 | 220 | True |
| Barendrecht | Zuid-Holland | 211 | 183 | False |
| Lisse | Zuid-Holland | 379 | 181 | True |
| Moerdijk | Noord-Brabant | 185 | 150 | True |
| Gorinchem | Zuid-Holland | 1014 | 148 | True |
| Opmeer | Noord-Holland | 176 | 143 | True |
| Gennep | Limburg | 240 | 127 | True |
| Geertruidenberg | Noord-Brabant | None | 126 | False |
| Oisterwijk | Noord-Brabant | 370 | 125 | True |
| Veere | Zeeland | 118 | 115 | True |
| Texel | Noord-Holland | 415 | 108 | True |
| Etten-Leur | Noord-Brabant | 324 | 99 | True |
| Woensdrecht | Noord-Brabant | 113 | 93 | True |
| Ridderkerk | Zuid-Holland | 145 | 47 | False |
| Wijchen | Gelderland | 437 | 45 | True |
| Vlieland | Fryslân | 215 | 33 | True |
| Westervoort | Gelderland | None | 16 | False |
| Krimpenerwaard | Zuid-Holland | 709 | 11 | True |
| Schouwen-Duiveland | Zeeland | 32 | 6 | True |
| Beesel | Limburg | 37 | 5 | True |
| Bunschoten | Utrecht | 64 | 0 | True |
| Albrandswaard | Zuid-Holland | None | 0 | False |
| Zoeterwoude | Zuid-Holland | 51 | 0 | True |
| Hollands Kroon | Noord-Holland | None | 0 | True |

## Herplant

### herplant_type

| Waarde | Aantal |
|---|---|
| kan | 254 |
| harde plicht | 39 |
| in beginsel/tenzij | 34 |
| geen grondslag | 15 |

### herplant_betalen_als_alternatief

| Waarde | Aantal |
|---|---|
| nee | 186 |
| kan | 108 |
| verplicht | 41 |
| onbekend | 7 |

### herplant_na_illegale_kap

| Waarde | Aantal |
|---|---|
| kan | 212 |
| nee | 66 |
| verplicht | 37 |
| onbekend | 27 |

### herplant_niet_nakomen_type

| Waarde | Aantal |
|---|---|
| strafbaar (rechter) | 149 |
| niets geregeld | 118 |
| meerdere | 40 |
| dwangsom/bestuursdwang | 25 |
| onbekend | 10 |

## Variabelen in het kapbeleid (gemeenten met een kapregel)

Basis: 332 gemeenten met D > 0. Trefwoordtelling, indicatief.

| Variabele | Totaal | Groningen | Fryslân | Drenthe | Overijssel | Flevoland | Gelderland | Utrecht | Noord-Holland | Zuid-Holland | Zeeland | Noord-Brabant | Limburg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omtrekdrempel (stamdikte) | 187 | 7 | 10 | 10 | 21 | 2 | 30 | 14 | 22 | 25 | 6 | 26 | 14 |
| lijst of kaart met aangewezen bomen | 177 | 2 | 8 | 5 | 2 | 3 | 23 | 14 | 25 | 27 | 11 | 38 | 19 |
| tuin- of perceeluitzondering | 110 | 5 | 7 | 4 | 8 | 1 | 19 | 13 | 12 | 14 | 1 | 17 | 9 |
| soortuitzondering (bijv. coniferen, populieren, fruitbomen) | 156 | 9 | 10 | 4 | 19 | 2 | 26 | 11 | 17 | 17 | 6 | 22 | 13 |
| weigeringsgrond natuur of ecologie | 257 | 7 | 13 | 10 | 22 | 3 | 36 | 19 | 33 | 36 | 11 | 43 | 24 |
| weigeringsgrond landschap | 242 | 7 | 13 | 10 | 23 | 2 | 37 | 15 | 31 | 29 | 11 | 42 | 22 |
| weigeringsgrond cultuurhistorie | 251 | 8 | 13 | 10 | 22 | 3 | 36 | 18 | 33 | 34 | 11 | 42 | 21 |
| weigeringsgrond beeld (stads- en dorpsschoon, beeldbepalend) | 242 | 8 | 13 | 10 | 21 | 2 | 34 | 16 | 30 | 33 | 11 | 41 | 23 |
| weigeringsgrond leefbaarheid of recreatie | 218 | 6 | 10 | 9 | 18 | 3 | 31 | 16 | 26 | 29 | 11 | 38 | 21 |
| weigeringsgrond boomwaarde of monumentaliteit | 137 | 2 | 10 | 7 | 7 | 0 | 12 | 8 | 23 | 25 | 3 | 23 | 17 |
| weigeringsgrond klimaat | 21 | 0 | 0 | 1 | 4 | 0 | 5 | 2 | 3 | 3 | 0 | 2 | 1 |
| herplant (kan of moet) | 322 | 10 | 18 | 12 | 25 | 5 | 50 | 23 | 40 | 43 | 12 | 54 | 30 |
| financiële compensatie of boomwaarde | 261 | 8 | 10 | 7 | 24 | 4 | 35 | 19 | 33 | 37 | 11 | 51 | 22 |
| bestuurlijke boete in de regeling | 11 | 0 | 3 | 1 | 3 | 0 | 1 | 1 | 0 | 0 | 0 | 2 | 0 |
| apart vastgesteld beleid naast de regeling | 123 | 5 | 4 | 2 | 6 | 2 | 15 | 17 | 18 | 15 | 2 | 27 | 10 |

## Methode

### Juridische plaats

| Plaats | Aantal |
|---|---|
| APV | 170 |
| losse bomen- of kapverordening | 78 |
| verordening fysieke leefomgeving (VFL) | 65 |
| omgevingsplan | 18 |
| geen vergunningplicht voor particuliere bomen | 10 |
| omgevingsplan (tijdelijk deel: bestemmingsplan) | 1 |

- Restant bruidsschat zonder vergunningplicht: 5 (Almere, Duiven, Koggenland, Molenlanden, Uitgeest)
- S = 1 via de Omgevingswet (omgevingsplanactiviteit) genoemd: 301
- Kapregel staat op de peildatum nog in de APV (na de start van de Omgevingswet op 1-1-2024): 170
- Volledige artikeltekst gelezen: 338 van 342
- Bereik over een categoriegrens: 129
- Betrouwbaarheid: {'middel': 33, 'hoog': 161, 'laag': 148}; status: {'ok': 292, 'onzeker': 50}

## Buurgemeenten met het grootste verschil

| Verschil | Gemeente | Score | Boom A | Drempel | Buurgemeente | Score | Boom A | Drempel |
|---|---|---|---|---|---|---|---|---|
| 73 | Utrecht | 73 | ja | 47 | IJsselstein | 0 | onbekend | None |
| 67 | Hoorn | 67 | nee | 47.1 | Koggenland | 0 | nee | None |
| 67 | Amersfoort | 67 | ja | 35 | Bunschoten | 0 | alleen als op lijst | None |
| 63 | Amsterdam | 80 | ja | 31 | Wijdemeren | 17 | alleen als op lijst | None |
| 63 | Amsterdam | 80 | ja | 31 | Landsmeer | 17 | alleen als op lijst | None |
| 63 | Amsterdam | 80 | ja | 31 | De Ronde Venen | 17 | alleen als op lijst | None |
| 63 | Amstelveen | 17 | alleen als op lijst | None | Amsterdam | 80 | ja | 31 |
| 62 | Zeewolde | 18 | alleen als op lijst | None | Harderwijk | 80 | alleen als op lijst | 30 |
| 62 | Harderwijk | 80 | alleen als op lijst | 30 | Nunspeet | 18 | alleen als op lijst | None |
| 62 | Amsterdam | 80 | ja | 31 | Waterland | 18 | alleen als op lijst | None |
| 62 | Amsterdam | 80 | ja | 31 | Haarlemmermeer | 18 | alleen als op lijst | None |
| 60 | Amsterdam | 80 | ja | 31 | Zaanstad | 20 | alleen als op lijst | 31 |
| 58 | Amsterdam | 80 | ja | 31 | Stichtse Vecht | 22 | alleen als op lijst | 31 |
| 56 | Montfoort | 17 | alleen als op lijst | None | Utrecht | 73 | ja | 47 |
| 56 | Gilze en Rijen | 73 | nee | 100.0 | Oosterhout | 17 | alleen als op lijst | None |
| 56 | Eindhoven | 73 | ja | 45 | Oirschot | 17 | alleen als op lijst | None |
| 56 | Eindhoven | 73 | ja | 45 | Nuenen, Gerwen en Nederwetten | 17 | alleen als op lijst | None |
| 56 | Almelo | 17 | alleen als op lijst | None | Hof van Twente | 73 | nee | 94.2 |
| 55 | Utrecht | 73 | ja | 47 | Woerden | 18 | alleen als op lijst | None |
| 55 | IJsselstein | 0 | onbekend | None | Nieuwegein | 55 | nee | 90 |

### Buren waar boom A in de ene wel en in de andere geen vergunning nodig heeft

| Verschil | Gemeente | Score | Boom A | Drempel | Buurgemeente | Score | Boom A | Drempel |
|---|---|---|---|---|---|---|---|---|
| 50 | Maassluis | 67 | ja | 31.4 | Rotterdam | 17 | nee | 361 |
| 50 | Alkmaar | 50 | ja | 63 | Uitgeest | 0 | nee | None |
| 50 | Alkmaar | 50 | ja | 63 | Koggenland | 0 | nee | None |
| 49 | Maastricht | 67 | ja | 47 | Valkenburg aan de Geul | 18 | nee | 126 |
| 43 | Delft | 60 | ja | 63 | Rotterdam | 17 | nee | 361 |
| 43 | Amsterdam | 80 | ja | 31 | Ouder-Amstel | 37 | nee | 62.8 |
| 38 | Wageningen | 55 | ja | 60 | Neder-Betuwe | 17 | nee | 125.6 |
| 38 | Rotterdam | 17 | nee | 361 | Pijnacker-Nootdorp | 55 | ja | 78.5 |
| 38 | Groningen | 55 | ja | 62.8 | Tynaarlo | 17 | nee | 126 |
| 37 | Heusden | 18 | nee | 150 | Tilburg | 55 | ja | 65 |
| 34 | Doesburg | 67 | ja | 45 | Bronckhorst | 33 | nee | 95 |
| 33 | Smallingerland | 50 | ja | 63 | Tytsjerksteradiel | 17 | nee | 150 |
| 33 | Rotterdam | 17 | nee | 361 | Vlaardingen | 50 | ja | 62.8 |
| 33 | Raalte | 17 | nee | 110 | Olst-Wijhe | 50 | ja | 65 |
| 33 | Deventer | 50 | ja | 75 | Raalte | 17 | nee | 110 |
| 32 | Meerssen | 50 | ja | 78.5 | Valkenburg aan de Geul | 18 | nee | 126 |
| 30 | Leeuwarden | 20 | nee | 63 | Smallingerland | 50 | ja | 63 |
| 30 | Amsterdam | 80 | ja | 31 | Oostzaan | 50 | nee | 94 |
| 27 | Pekela | 60 | ja | 62.8 | Westerwolde | 33 | nee | 125.6 |
| 24 | Leiden | 43 | nee | 157 | Wassenaar | 67 | ja | 31.4 |
