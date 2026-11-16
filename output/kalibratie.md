# Kalibratie stap 1b — scoringsmodel v2.1

Peildatum bronnen: 14-11-2026 (data/gemeenten/…). Gescoord zonder kennis van de referentiescores; doorslaggevende citaten handmatig gecontroleerd tegen tekst/*.md.

## Uitkomst

| Gemeente | Referentie (v2) | Nieuw (v2.1) | Score ref → nieuw | Bereik nieuw | Categorie | Betrouwbaarheid |
|---|---|---|---|---|---|---|
| Amsterdam GM0363 | D4 W2 H3 S0 | D4 W2 **H2 S1** | 73 → 73 | 73–80 (loopt tot grens Zeer streng) | 4 Streng | middel |
| Apeldoorn GM0200 | D3 W2 H1 S1 | D3 W2 H1 S1 | 50 → 50 | 50–55 | 3 Gemiddeld | hoog |
| Ameland GM0060 | D1 W2 H2 S3 | D1 W2 H2 S3 | 22 → 22 | 0–22 (over grens) | 2 Soepel | laag (lijst niet gevonden) |
| Vaals GM0981 | D1 W3 H1 S1 | D1 W3 H1 S1 | 18 → 18 | 0–20 (over grens) | 1 Zeer soepel | laag (lijst niet gevonden) |
| Gorinchem GM0512 | D1 W2 H1 S1 | D1 W2 H1 S1 | 17 → 17 | 17–33 (over grens) | 1 Zeer soepel | middel (lijst ingezien) |

## Verschillen per criterium

**Amsterdam H 3 → 2.** Bomenverordening 2014 art. 7 lid 1: "Het college verbindt aan de vergunning … het voorschrift dat … wordt herplant, tenzij zwaarwegende argumenten zich daartegen verzetten" (standaard herplant = H2). Lid 3: storting van de boomwaarde in het herplantfonds "kan" als herplant niet mogelijk is. Volgens v2.1 verhoogt een kan-storting H niet. Maar beleidsregel CVDR697591_2 zegt: "Vergunningaanvragers die niet fysiek kunnen herplanten en daarom financieel moeten compenseren, storten het verschuldigde geldbedrag …" → maximum H3.

**Amsterdam S 0 → 1.** Art. 9 lid 1: "Het college schrijft de zakelijk gerechtigde … die zonder vergunning … is geveld … aan om tot herplant over te gaan." Dat is herplantplicht na illegale kap = S1. Art. 9 was in de proefrun niet gelezen. Geen bestuurlijke boete voor kap (de boeteverordening dekt alleen iepziekte), dus S blijft 1.

**Gorinchem: bomenlijst ingezien.** Geoportaal-laag van de gemeente: 1.014 monumentale/beeldbepalende bomen, waarvan 148 met eigenaar "particulier". D = 0 valt daarmee af; het bereik begint bij 17. Het maximum 33 komt van een gebiedsregel in het omgevingsplan (hoofdstuk 20, Linge II Zuid) die volgens "breedste regime bepaalt D" tot D = 2 zou leiden.

**Vaals: bereik 0–18 → 0–20.** Het groenstructuurplan, waarnaar de toelichting verwijst voor herplant, is niet gelezen. Dat kan H op 2 brengen.

## Juridische plaats

Bij alle vijf staat de materiële kapregel in een gemeentelijke verordening (APV, bomenverordening of VFL). Het omgevingsplan in de CVDR bevat alleen aanvraagvereisten (art. 22.299). De legesverordeningen noemen kap overal een omgevingsplanactiviteit (Ow 5.1 lid 1 onder a, via art. 22.8 Ow). Amsterdam spreekt zichzelf tegen: de toelichting bij het omgevingsplan zegt dat "overige delen van verordeningen" geen deel uitmaken van het tijdelijk deel. S verandert daardoor bij geen van de vijf, omdat elk ook een eigen kapspecifieke sanctie heeft.

## Modelsignalen (besluit gebruiker nodig)

1. **H bij tegenstrijdige teksten.** De verordening zegt "kan", de beleidsregel "moeten" (Amsterdam). Telt de beleidsregel mee voor H3, net zoals een beleidsregel nu al meetelt voor H2? Zo ja: Amsterdam H3 → 80 → Zeer streng.
2. **"Uitgangspunt herplant" per geval** (Apeldoorn, Bomennota van de raad, ±40% in de praktijk): H1 of H2?
3. **Kleine gebiedsregels en D** (Gorinchem, Linge II Zuid): telt een gebiedsregel voor één wijk als "aangewezen gebied" (D2)?
4. **Label "juridische plaats onzeker".** Dit geldt bijna overal (APV of VFL na 2024 opnieuw vastgesteld). Alleen gebruiken als het een score verandert?
5. **Geldigheid van de bestuurlijke boete** (Ameland): de teksten noemen geen wettelijke grondslag. Het model scoort de tekst, niet de geldigheid.
6. **Strenge handhaving zonder boete** (Amsterdam: dwangsom €5.000 per boom, herplant in 100% afgedwongen) scoort gelijk aan alleen een herplantaanschrijving (S1).
7. **Bouwkavelvrijstelling bij lijstsysteem** (Vaals): de correctieregel werkt niet bij D = 1.

## Open punten

- Bomenlijsten Ameland en Vaals niet online gevonden (Vaals: Gemeenteblad 2019, 235553 gaf HTTP 504).
- Amsterdam: of de Bomenverordening 2014 in Weesp geldt, is niet vastgesteld (Verzamelbesluit herindeling niet gelezen).
- Niet gelezen: VTH-beleidsplan Vaals 2026-2030, groenstructuurplan Vaals, beslistermijnen onder de Ow.
