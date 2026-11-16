# Afwijkingen — Groningen

10 gemeenten gescoord. Hieronder staan de gemeenten met status "niet gevonden" of "onzeker", of met betrouwbaarheid "laag".

## Lijstsystemen waarvan de lijst niet is ingezien

- **Veendam** (GM0047): Register/lijst van waardevolle en monumentale bomen en de bijbehorende groene kaart (art. 2) niet ingezien; onbekend hoeveel bomen en hoeveel particulier. Toelichting en bijlagen van de Bomenverordening ontbreken in het dossier. Omgevingsplan DSO niet ingezien.

## Overige afwijkingen

- **Stadskanaal** (GM0037), status onzeker, betrouwbaarheid laag: Inwerkingtreding van het Chw-bestemmingsplan (vs02, vastgesteld 2026-09-14; regelStatus in de API 'in ontwikkeling') is niet vastgesteld. De legesverordening 2026 (geldend vanaf 2026-01-01) verwijst al naar art. 108.2 en de gemeente verleende ook in 2025-2026 kapvergunningen, dus een eerdere versie of ander plan met dezelfde regel lijkt te gelden; die tekst is niet gelezen. Als het plan niet van kracht is, kan D lager zijn (minimum D1). Beleidsregels herplant/financiële compensatie (art. 108.8 sub b) en weigeringsbeleid (108.6) niet gevonden, dus H-maximum 3.

## Bereik loopt over een categoriegrens

- Groningen: 55 (3 Gemiddeld), bereik 55-60
- Het Hogeland: 55 (3 Gemiddeld), bereik 55-60
- Stadskanaal: 50 (3 Gemiddeld), bereik 17-87
- Eemsdelta: 37 (2 Soepel), bereik 37-40
- Veendam: 37 (2 Soepel), bereik 18-37

## Modelsignalen

- Pekela: Art. 2:9 lid 1 ('wordt bij het vellen van een houtopstand zonder vergunning van het college een geldboete opgelegd', hoogte volgens strafbepaling) is dubbelzinnig tussen strafrechtelijke en bestuurlijke boete; het model kent alleen het onderscheid S1 versus S2.
- Groningen: Drempel gegeven als diameter (20 cm) die precies op 62,8 cm omtrek uitkomt: vlak boven de ondergrens van D3 (60 cm); een kleine afwijking in de omrekening verandert D niet, maar illustreert de scherpe grens.
- Oldambt: Regeling die buiten de bebouwde kom alleen grotere eenheden beschermt: het model heeft hiervoor geen aparte regel; behandeld als gebiedsbeperking zonder D-correctie, omdat de bebouwde kom (incl. tuinen) volledig gedekt is.
- Stadskanaal: Kapregel in een Chw-bestemmingsplan (bruidsschat) dat niet als CVDR-regeling is gepubliceerd: de pipeline haalt het niet op en kan het dus niet scoren.
- Stadskanaal: Kapregel in een Chw-bestemmingsplan dat pas kort is vastgesteld, terwijl de API regelStatus 'in ontwikkeling' geeft en de leges er al naar verwijzen: het model kent geen manier om een onzekere inwerkingtreding te scoren anders dan met een breed D-bereik. Advies: peildatum-regel uitbreiden (bijv. 'verwijst de geldende legesverordening ernaar, scoor dan de tekst en noteer de onzekerheid').
- Stadskanaal: 108.5 combineert 'kunnen weigeren op grond van waarden' (W2) met 'in beginsel geen velvergunningen' en gesloten criteria (W3) in één artikel. Gescoord W3 met minimum 2; advies: vastleggen dat bij tegenstrijdige leden de strengste formulering telt, of het omgekeerde.
- Eemsdelta: Drempel op het beschermde 'potentieel monumentale' niveau (35 cm diameter) levert een omtrek van ca. 110 cm op, net boven de grens van 100 cm tussen D2 en D3; kleine verschillen in omrekening (35 cm x 3,14 = 109,9) veranderen D niet.
- Veendam: Algemene houtopstandenregel met een oppervlaktedrempel van 100 m² (geen stamomtrek): het model kent alleen omtrekdrempels, dus D2 is een inschatting van gelijkwaardigheid met een hoge omtrekdrempel.
- Veendam: Boetehoogte 'ter hoogte van de boomwaarde' in een strafbepaling lijkt op S3 maar is een strafrechtelijke boete via de rechter; het model scoort dat als S1.
- Westerkwartier: Houtsingel zonder diameterdrempel binnen een regime met hoge drempel: het model beschrijft een structuur wel (D = 2) maar niet hoe die zich verhoudt tot een gemeentebrede regel met uitzondering voor fruitbomen. Zonder houtsingel zou D = 1 zijn (D = 2 min 1 voor fruitbomen); met houtsingel D = 2.
- Westerkwartier: Beleidsregel (spelregels) met '100% compensatieplicht' geldt alleen voor een subtype (houtsingels) en wordt volgens 'grootste deel van de gedekte bomen' niet in H meegeteld.
- Midden-Groningen: Een beleidsnotitie met 'in beginsel een herplantplicht' waarvan de bijbehorende APV-bepaling is vervallen: model v2.3 geeft geen regel voor beleid zonder verordeningsgrondslag; H = 1 met bereik 0-2 gekozen.
- Midden-Groningen: Gemengde lijst (gemeentelijke en particuliere bomen, zonder eigenaarskolom): lijst_aantal_particulier is niet vast te stellen.
