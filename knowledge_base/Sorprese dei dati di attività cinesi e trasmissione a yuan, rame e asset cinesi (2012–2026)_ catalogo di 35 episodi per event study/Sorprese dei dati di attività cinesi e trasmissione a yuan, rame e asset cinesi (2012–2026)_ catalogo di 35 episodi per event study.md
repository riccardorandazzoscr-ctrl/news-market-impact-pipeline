# Sorprese dei dati di attività cinesi e trasmissione a yuan, rame e asset cinesi (2012–2026): catalogo di 35 episodi per event study

Le release cinesi di attività che si discostano nettamente dal consenso trasmettono una pressione direzionale coerente soprattutto su rame (`HG=F`), dollaro australiano (`AUD=X`) e internet cinese (`KWEB`). Su `CNY=X` la trasmissione è più debole e meno affidabile, perché il fixing della PBOC filtra la reazione e c'è il rischio di *sell the news*. Il catalogo raccoglie 35 date verificate: 19 sorprese al rialzo, 14 al ribasso e 2 a verso ambiguo, con 33 release «pulite» e 2 contaminate da stimolo.

## §1 Sintesi esecutiva

**TL;DR**
- Le sorprese ampie (PMI ufficiale/Caixin oltre circa 0,5 punti, PIL oltre 0,2 punti, produzione industriale e vendite al dettaglio oltre circa 1 punto) generano un'attesa direzionale chiara. Rialzo: rame `pos`, `KWEB` `pos`, `AUD=X` `neg`, `CNY=X` `neg`. Ribasso: segni opposti. Tutte e 35 le date hanno una riga su `CNY=X` e una su `HG=F`.
- L'event study è **affidabile** per `HG=F` e `AUD=X` sulle release di giorni feriali senza mosse PBOC (33 episodi su 35). È **debole** su `CNY=X`: nel regime pre-agosto 2015 il cambio era quasi agganciato, mentre dopo il 2015 il fixing e i *sell the news* compaiono anche nei casi documentati, per esempio il 2023-01-17. Le reazioni effettive documentate dalla stampa sui ticker in lista vanno nel senso atteso in 4 casi su 5 (N=5, INDICATIVE ONLY).
- È **inaffidabile** quando la release coincide con shock esogeni: 2013-04-15 (crollo dell'oro), 2016-01-04 (circuit breaker), 2020-03-02 (COVID e taglio d'emergenza Fed il giorno dopo), 2022-10-24 (esito politico del XX Congresso). Lo è anche quando la PBOC agisce lo stesso giorno (2024-10-18). Il catalogo marca questi casi; la pipeline dovrebbe escluderli dai calcoli direzionali o trattarli a parte.

La tesi centrale è che il canale dominante non è il PIL in sé ma la **sorpresa sulla domanda di materie prime e sul ciclo industriale**. Per questo il PMI manifatturiero (ufficiale NBS e Caixin/RatingDog) e la produzione industriale hanno una trasmissione più pulita del PIL trimestrale, che spesso esce insieme ai dati mensili di segno opposto (2024-04-16, 2026-04-16). La seconda tesi è che il regime conta più del segno. Nel 2012–2015 lo yuan quasi agganciato rende `CNY=X` poco informativo. Nel 2020–2022 lo shock pandemico domina i dati. Dal 2024 in poi il «policy put» di Pechino rende le sorprese negative parzialmente autolimitanti, perché il mercato le legge come preludio di stimolo. La terza tesi è operativa per la pipeline. Le release di sabato o domenica (PMI ufficiale NBS il 31 del mese) vanno mappate alla prima seduta del lunedì, e la sovrapposizione delle finestre T+10 fra PMI ufficiale e Caixin (due o tre giorni di distanza) obbliga a tenere una sola data per ciclo mensile, come è stato fatto qui.

## §2 Tassonomia dei canali di trasmissione

**Canale 1, domanda di metalli industriali (direzionale).** Catena: `sorpresa PMI/produzione industriale/investimenti fissi → revisione della domanda cinese di rame (la Cina ne è il primo consumatore) → prezzo atteso del rame → HG=F`.\[1\] È il canale più diretto e il meno contaminato dalla politica valutaria. Il verso è `pos` per le sorprese al rialzo e `neg` per quelle al ribasso. Il token è `commodity_demand`, l'asset principale `HG=F`; `BZ=F` è un proxy secondario e più rumoroso, perché il petrolio risponde soprattutto all'OPEC+ e alla geopolitica (nel 2026 alla guerra con l'Iran).

**Canale 2, valuta delle materie prime (direzionale).** Catena: `sorpresa di attività cinese → ragioni di scambio australiane (minerale di ferro, carbone, rame) → flussi verso AUD → USD/AUD`. Su `AUD=X`, quotato USD/AUD, una sorpresa al rialzo è `neg` (AUD forte) e una al ribasso è `pos`. La stampa di cronaca valutaria lo documenta in modo esplicito, per esempio con «Aussie dollar tanks with China Flash PMI» (MacroBusiness, 24 luglio 2015) e «AUD/USD rebounds toward 0.6750 on China's PMIs big beat» (FXStreet, 1 marzo 2023).\[2\]\[3\] Il minerale di ferro SGX/DCE sarebbe il proxy più puro, ma non è nel DB.

**Canale 3, yuan (direzionale ma smorzato).** Catena: `sorpresa di attività → aspettative su crescita e tassi PBOC → flussi di portafoglio e fixing → USD/CNY onshore`. Su `CNY=X` una sorpresa al rialzo è `neg` (yuan forte) e una al ribasso è `pos`. Il canale è smorzato dalla banda di oscillazione attorno al fixing e da due effetti di segno opposto. Il primo: una sorpresa negativa alza la probabilità di allentamento PBOC (`pboc`, `china_stimulus`), che indebolisce lo yuan nella stessa direzione. Il secondo: una sorpresa positiva già prezzata produce prese di profitto, come il 2023-01-17, quando Bloomberg riportava che lo yuan onshore e offshore «extended drops to 0.4%» nonostante il PIL sopra le attese.\[4\] Il CNH offshore reagisce prima e meglio, ma non è in DB.

**Canale 4, equity cinese ed EM (direzionale, con amplificatore).** Catena: `sorpresa di attività → revisione degli utili e del premio al rischio Cina → ADR/ETF cinesi → KWEB, EEM, EWY`. `KWEB` (dall'agosto 2013) ha la reattività più alta ma è fortemente esposto a fattori regolatori (2021) e politici (2022-10-24). `EEM` ed `EWY` sono proxy diluiti: la Corea è sensibile tramite l'export verso la Cina. Le borse locali (CSI 300, Hang Seng, HSCEI) non sono in DB.

**Canale 5, consumo interno (direzionale, con N ridotto).** Catena: `sorpresa sulle vendite al dettaglio → aspettative su piattaforme e consumi → KWEB`. Il token è `china_consumption`. È rilevante soprattutto dopo il 2022, quando le vendite al dettaglio diventano la variabile più seguita (2022-05-16, 2023-01-17, 2026-05-18, 2026-10-19).

**Canale redistributivo, stimolo contro crescita.** Catena: `sorpresa negativa → attesa di taglio RRR/LPR o pacchetto fiscale → yuan più debole (CNY=X pos) ma rame ed equity sostenuti dall'attesa di stimolo`. È redistributivo perché muove `CNY=X` e `HG=F`/`KWEB` in direzioni non speculari rispetto al canale di crescita puro. Quando la PBOC agisce lo stesso giorno (token `china_stimulus`, `pboc`), il segno su `CNY=X` diventa ambiguo e va scritto `pos, neg`, come per il 2024-10-18.

**Amplificatori (cambiano l'ampiezza, non il segno).** Gli amplificatori principali sono quattro. Il primo è la distanza dalla soglia 50 del PMI: un passaggio da sopra a sotto 50 viene titolato «unexpectedly contracts». Il secondo è lo stato di stress del mercato: agosto 2015, gennaio 2016, marzo 2020. Il terzo è la coincidenza con l'escalation tariffaria USA-Cina (`tariff_escalation`: 2019, aprile 2025), che rende i mercati più sensibili alle sorprese. Il quarto è la liquidità ridotta prima delle festività cinesi (30 settembre, 31 dicembre, 30 aprile).

## §3 Catalogo di episodi-ancora datati

Convenzioni di data. Le release NBS e Caixin escono alle 09:30–10:00 di Pechino (01:30–02:00 UTC). In un giorno feriale cadono quindi dentro la seduta onshore di `CNY=X`, dentro la seduta Globex di `HG=F` con data di contrattazione D, prima dell'apertura USA di `KWEB` (seduta D) e dentro la seduta asiatica di `AUD=X` (D). Per le release di sabato o domenica la prima seduta di **tutti** i proxy è il lunedì: Globex riapre la domenica alle 18:00 ET con data di contrattazione lunedì, e onshore, ETF USA e FX seguono il lunedì. Questa regola è applicata senza eccezioni.

| Data | Asset | Verso | Meccanismo | Evento | Note |
|---|---|---|---|---|---|
| 2012-05-11 | CNY=X | pos | china, activity_growth, cny | Produzione industriale di aprile +9,3% a/a, 2,6 punti sotto marzo, «sharper than expected» | Comunicato NBS «Industrial Production Operation in April 2012»: «up 9.3 percent year-on-year… 2.6 percentage points lower than that in March»; secondo China Briefing è stata «the slowest growth in the past three years». Al Jazeera 11/05/2012: «sharper than expected declines in investment and industrial production». Consenso numerico Reuters NON verificato (sorpresa ampiamente commentata). Taglio RRR di 50 pb annunciato nel weekend (China Briefing, 14/05/2012: «The People's Bank of China announced on May 13 that it would cut the amount of cash that banks must hold as reserves by 0.5 percentage points», in vigore dal 18/05; China Briefing indica il 13 maggio): contamina T+1 in poi. Venerdì feriale, release 02:00 UTC. |
| 2012-05-11 | HG=F | neg | china, activity_growth, commodity_demand | Produzione industriale di aprile +9,3%, sotto le attese | Fonte come riga CNY=X. Seduta Globex con data di contrattazione 2012-05-11. Taglio RRR annunciato nel weekend (China Briefing): misurare T+1 con cautela. |
| 2013-04-15 | CNY=X | pos | china, activity_growth, china_gdp, cny | PIL 1T13 +7,7% contro 8,0% atteso; produzione industriale di marzo 8,9% contro 10,1%\[5\]\[6\] | Bloomberg 15/04/2013 (survey 8,0%); Benzinga/Credit Suisse (produzione industriale 8,9% contro 10,1%, vendite al dettaglio 12,4% contro 12,6%).\[5\]\[6\] Regime di cambio quasi agganciato: reazione di CNY=X attesa minima. |
| 2013-04-15 | HG=F | neg | china, activity_growth, china_gdp, commodity_demand | PIL 1T13 sotto il consenso | Confondente forte: crollo dell'oro e dei metalli nella stessa seduta, che amplifica il movimento. Usare BZ=F/^GSPC come controllo. |
| 2013-04-15 | AUD=X | pos | china, activity_growth, china_gdp, commodity_demand | PIL 1T13 sotto il consenso, AUD atteso più debole | Lunedì feriale. Stesso confondente sulle materie prime. |
| 2013-10-24 | CNY=X | neg | china, activity_growth, pmi, cny | HSBC flash PMI di ottobre 50,9 contro 50,4\[7\] | Reuters via Yahoo; FXStreet 24/10/2013: «beats expectations and hits 7-month highs (50.9 v 50.4e)».\[7\]\[8\] Nessuna mossa PBOC. Giovedì. |
| 2013-10-24 | HG=F | pos | china, activity_growth, pmi, commodity_demand | HSBC flash PMI sopra le attese | Fonte come riga CNY=X. Release pulita. |
| 2013-10-24 | KWEB | pos | china, activity_growth, pmi | HSBC flash PMI sopra le attese | KWEB quotato da agosto 2013; seduta USA dello stesso giorno (release prima dell'apertura). |
| 2014-07-24 | CNY=X | neg | china, activity_growth, pmi, cny | HSBC flash PMI di luglio 52,0 contro 51,0 (massimo a 18 mesi)\[9\] | Reuters via Business Standard 24/07/2014: «beating a forecast of 51 in a Reuters poll». Misure del Consiglio di Stato annunciate il giorno prima (23/07):\[9\] nessuna mossa PBOC lo stesso giorno. |
| 2014-07-24 | HG=F | pos | china, activity_growth, pmi, commodity_demand | HSBC flash PMI sopra le attese | Fonte come riga CNY=X. |
| 2014-07-24 | KWEB | pos | china, activity_growth, pmi | HSBC flash PMI sopra le attese | Seduta USA del 2014-07-24. |
| 2015-02-26 | CNY=X | neg | china, activity_growth, pmi, cny | HSBC flash PMI di febbraio 50,1 contro 49,5\[10\] | Gulf News 26/02/2015: «Economists polled by Reuters had forecast a reading of 49.5».\[10\] Taglio dei tassi PBOC sabato 2015-02-28 (CNBC 28/02/2015: «China's central bank said on Saturday it would cut benchmark interest rates by 25 basis points to 5.35 percent», in vigore dal 01/03): contamina T+1 in poi. |
| 2015-02-26 | HG=F | pos | china, activity_growth, pmi, commodity_demand | HSBC flash PMI sopra le attese | Come riga CNY=X; finestre T+3/T+10 contaminate dallo stimolo successivo. |
| 2015-07-24 | CNY=X | pos | china, activity_growth, pmi, cny | Caixin flash PMI di luglio 48,2 contro 49,7 atteso (minimo a 15 mesi)\[2\] | MacroBusiness 24/07/2015: «Expected was 49.7»; comunicato Caixin/Markit (embargo 09:45 Pechino).\[2\]\[11\] Yuan ancora agganciato prima dell'11 agosto: reazione minima. Contesto: crash azionario cinese. |
| 2015-07-24 | HG=F | neg | china, activity_growth, pmi, commodity_demand | Caixin flash PMI sotto le attese | Fonte come riga CNY=X. Venerdì. |
| 2015-07-24 | KWEB | neg | china, activity_growth, pmi | Caixin flash PMI sotto le attese | Seduta USA del 2015-07-24. |
| 2015-07-24 | AUD=X | pos | china, activity_growth, pmi, commodity_demand | Caixin flash PMI sotto le attese, AUD atteso più debole | MacroBusiness: «Aussie dollar tanks with China Flash PMI» (reazione osservata coerente).\[2\] |
| 2015-08-21 | CNY=X | pos | china, activity_growth, pmi, cny | Caixin flash PMI di agosto 47,1 contro 47,7 (minimo a 77 mesi)\[12\]\[13\] | CNBC 20/08/2015 (ora USA) e Caixin Global 21/08: «below a Reuters forecast of 47.7». Release venerdì 09:45 Pechino.\[12\]\[13\] Multi-causa: svalutazione dell'11 agosto e «Black Monday» del 2015-08-24 (T+1). |
| 2015-08-21 | HG=F | neg | china, activity_growth, pmi, commodity_demand | Caixin flash PMI sotto le attese | Episodio dominato dal contagio di mercato nelle finestre T+1 e oltre. |
| 2015-08-21 | KWEB | neg | china, activity_growth, pmi | Caixin flash PMI sotto le attese | Seduta USA del 2015-08-21; T+1 è il crollo del 24 agosto. |
| 2015-08-21 | AUD=X | pos | china, activity_growth, pmi, commodity_demand | Caixin flash PMI sotto le attese | Amplificatore: stress di mercato. |
| 2016-01-04 | CNY=X | pos | china, activity_growth, pmi, cny | Caixin PMI di dicembre 48,2 contro 49,0 (Reuters)\[14\] | CNBC 03-04/01/2016: «below a Reuters poll forecast for 49.0» (altre fonti 48,9).\[14\]\[15\] PMI ufficiale 49,7 in linea, uscito venerdì 2016-01-01 (festivo): prima seduta per entrambi il 2016-01-04.\[16\] Multi-causa: circuit breaker CSI 300 (-7%, chiusura), tensioni Arabia Saudita-Iran.\[15\]\[17\]\[18\] |
| 2016-01-04 | HG=F | neg | china, activity_growth, pmi, commodity_demand | Caixin PMI sotto le attese | Episodio contaminato dal circuit breaker.\[18\] |
| 2016-01-04 | KWEB | neg | china, activity_growth, pmi | Caixin PMI sotto le attese | Seduta USA del 2016-01-04. |
| 2016-01-04 | AUD=X | pos | china, activity_growth, pmi, commodity_demand | Caixin PMI sotto le attese | Come sopra. |
| 2016-04-15 | CNY=X | neg | china, activity_growth, china_gdp, cny | Produzione industriale di marzo +6,8% contro 5,9%; investimenti fissi 10,7% contro 10,3%; PIL 6,7% in linea\[19\]\[20\] | CNBC (datato 14/04 ora USA) e Trading Economics 15/04/2016.\[19\]\[20\] Release venerdì 15/04 a Pechino. Sorpresa trainata dai dati mensili, non dal PIL.\[21\] |
| 2016-04-15 | HG=F | pos | china, activity_growth, commodity_demand | Produzione industriale e investimenti fissi sopra le attese | Fonte come riga CNY=X. Release pulita. |
| 2016-11-01 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di ottobre 51,2 contro 50,4 (Reuters, 26 analisti)\[22\] | CNBC (datato 31/10 ora USA): «a Reuters poll of 26 analysts had forecast 50.4». Release martedì 01/11 a Pechino; Caixin 51,2 lo stesso giorno (consenso non trovato).\[22\] Elezioni USA dell'8/11 in T+5. |
| 2016-11-01 | HG=F | pos | china, activity_growth, pmi, commodity_demand | PMI ufficiale sopra le attese | Fonte come riga CNY=X. |
| 2016-11-01 | KWEB | pos | china, activity_growth, pmi | PMI ufficiale sopra le attese | Seduta USA del 2016-11-01. |
| 2016-12-01 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di novembre 51,7 contro 51,0\[23\] | CNBC (datato 30/11 ora USA): «beat Reuters analyst predictions of a 51.0 reading». Giovedì 01/12 a Pechino; Caixin 50,9 contro 50,8, non rilevante.\[23\] |
| 2016-12-01 | HG=F | pos | china, activity_growth, pmi, commodity_demand | PMI ufficiale sopra le attese | Release pulita. |
| 2017-06-30 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di giugno 51,7 contro 51,0\[24\] | CNBC 02/07/2017 (sul Caixin) cita il PMI ufficiale; venerdì 30/06. Il Caixin del 2017-07-03 (50,4 contro 49,5) rafforza in T+1\[24\] ma non ha riga propria, per evitare finestre sovrapposte. |
| 2017-06-30 | HG=F | pos | china, activity_growth, pmi, commodity_demand | PMI ufficiale sopra le attese | Release pulita. |
| 2019-04-01 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di marzo 50,5 contro 49,6 (domenica 31/03) e Caixin 50,8 contro 49,9/50,0 (lunedì)\[25\]\[26\] | ForexLive 01/04/2019: «Manufacturing 50.5 (vs. expected 49.6)»; Investing.com: Caixin «higher than the expected 49.9».\[25\]\[26\] Prima seduta di tutti i proxy: lunedì 2019-04-01. Shanghai +2,3%, Hang Seng +1,8% (Investing.com).\[26\] |
| 2019-04-01 | HG=F | pos | china, activity_growth, pmi, commodity_demand | Doppio PMI sopra le attese | Release domenicale: data di contrattazione Globex lunedì. Pulita. |
| 2019-04-01 | KWEB | pos | china, activity_growth, pmi | Doppio PMI sopra le attese | Seduta USA del 2019-04-01. |
| 2019-04-01 | AUD=X | neg | china, activity_growth, pmi, commodity_demand | Doppio PMI sopra le attese, AUD atteso più forte | ForexLive: «risk boosted».\[25\] |
| 2019-04-30 | CNY=X | pos | china, activity_growth, pmi, cny | PMI ufficiale di aprile 50,1 contro 50,5; Caixin 50,2 contro 51,0\[27\] | CNBC 30/04/2019; FXStreet: «Caixin manufacturing PMI unexpectedly drops to 50.2 in April (Aussie weaker)».\[27\]\[28\] Martedì. Mercato onshore chiuso per il Primo maggio subito dopo: la T+1 di CNY=X va verificata sul calendario. Escalation tariffaria USA di inizio maggio in T+3/T+5. |
| 2019-04-30 | HG=F | neg | china, activity_growth, pmi, commodity_demand, tariff_escalation | Doppio PMI sotto le attese | Finestre T+5/T+10 contaminate da `tariff_escalation`. |
| 2019-04-30 | KWEB | neg | china, activity_growth, pmi, tariff_escalation | Doppio PMI sotto le attese | Come sopra. |
| 2019-04-30 | AUD=X | pos | china, activity_growth, pmi, commodity_demand | Doppio PMI sotto le attese | FXStreet: «Aussie weaker» (reazione osservata coerente).\[28\] |
| 2019-09-30 | CNY=X | neg | china, activity_growth, pmi, cny | Caixin PMI di settembre 51,4 contro 50,2 (Reuters)\[29\] | CNBC 30/09/2019 (via sub-ricerca). Lunedì; il PMI ufficiale esce lo stesso giorno\[29\] (valore non verificato qui). Onshore chiuso dal 1° al 7 ottobre: T+1 di CNY=X slitta all'8/10, dato Yahoo nella festività da verificare. |
| 2019-09-30 | HG=F | pos | china, activity_growth, pmi, commodity_demand | Caixin PMI sopra le attese | Release pulita; liquidità pre-festiva. |
| 2020-03-02 | CNY=X | pos | china, activity_growth, pmi, cny | PMI ufficiale di febbraio 35,7 contro 46,0 (sabato 29/02); Caixin 40,3 contro 45,7 (lunedì)\[30\]\[31\] | CNBC 29/02/2020: «Analysts polled by Reuters expected the February PMI to come in at 46.0»; CNBC 02/03/2020 (Caixin).\[30\]\[31\] Prima seduta per tutti: lunedì 2020-03-02. Multi-causa: COVID globale, taglio d'emergenza Fed del 2020-03-03 (T+1). |
| 2020-03-02 | HG=F | neg | china, activity_growth, pmi, commodity_demand | PMI ai minimi storici | Le finestre oltre T+0 sono dominate dalle politiche globali. |
| 2020-03-02 | KWEB | neg | china, activity_growth, pmi | PMI ai minimi storici | Seduta USA del 2020-03-02 (rimbalzo di Wall Street quel giorno: confondente). |
| 2020-03-02 | AUD=X | pos | china, activity_growth, pmi, commodity_demand | PMI ai minimi storici | Riunione RBA del 2020-03-03 in T+1. |
| 2020-03-31 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di marzo 52,0 contro 45 atteso\[32\] | CNBC 31/03/2020: «Analysts polled by Reuters had expected the official PMI to come in at 45». Martedì. L'NBS stessa avverte dell'effetto base.\[32\] Il giorno prima (lunedì 2020-03-30) la PBOC ha tagliato a sorpresa il reverse repo a 7 giorni di 20 pb, dal 2,40% al 2,20% (CNBC 30/03/2020; confermato da Xinhua): non lo stesso giorno. |
| 2020-03-31 | HG=F | pos | china, activity_growth, pmi, commodity_demand | PMI ufficiale molto sopra le attese | Sorpresa enorme ma di «qualità» bassa (effetto base): ampiezza attesa ridotta.\[32\] |
| 2020-03-31 | KWEB | pos | china, activity_growth, pmi | PMI ufficiale sopra le attese | Seduta USA del 2020-03-31. |
| 2020-07-16 | CNY=X | neg | china, activity_growth, china_gdp, cny | PIL 2T20 +3,2% a/a contro 2,5% (Reuters)\[33\] | Reuters via Yahoo 16/07/2020: «faster than the 2.5% forecast by analysts in a Reuters poll».\[33\] Giovedì. Altri dati mensili dello stesso rilascio non verificati qui. |
| 2020-07-16 | HG=F | pos | china, activity_growth, china_gdp, commodity_demand | PIL 2T20 sopra le attese | Release pulita. |
| 2022-05-16 | CNY=X | pos | china, activity_growth, china_consumption, cny, china_stimulus | Vendite al dettaglio di aprile -11,1% contro -6,1%; produzione industriale -2,9% contro +0,4%\[34\]\[35\] | ForexLive 16/05/2022; CNBC: «more than the 6.1% decline predicted in a Reuters poll».\[34\]\[35\] Lunedì. `china_stimulus`: domenica 2022-05-15 PBOC e CBIRC hanno consentito alle banche di abbassare di 20 pb il limite minimo dei tassi sui mutui per chi compra la prima casa, portandolo a 20 pb sotto il loan prime rate (SCMP 15/05/2022). Domina il dato. |
| 2022-05-16 | HG=F | neg | china, activity_growth, commodity_demand, china_stimulus | Crollo dei dati di aprile (lockdown di Shanghai)\[35\]\[36\] | Lo stimolo immobiliare del weekend agisce in senso opposto sul rame: possibile attenuazione. |
| 2022-05-16 | KWEB | neg | china, activity_growth, china_consumption, china_stimulus | Vendite al dettaglio molto sotto le attese | Seduta USA del 2022-05-16. |
| 2022-05-16 | AUD=X | pos | china, activity_growth, commodity_demand | Dati di aprile molto sotto le attese | Fonte come riga CNY=X. |
| 2022-10-24 | CNY=X | pos, neg | china, activity_growth, china_gdp, cny | PIL 3T22 +3,9% contro 3,4% (rilascio rinviato dal 18/10), nel lunedì post-Congresso\[37\]\[38\] | Rappler/Reuters 24/10/2022: «outstripping the 3.4% pace forecast»; «onshore yuan fell to its weakest level in 15 years».\[37\] La sorpresa positiva del dato è sovrastata dall'esito politico del XX Congresso (weekend 22-23/10): attesa genuinamente ambigua. Data di rilascio certa (24/10), non quella programmata (18/10).\[38\] |
| 2022-10-24 | HG=F | pos, neg | china, activity_growth, china_gdp, commodity_demand | PIL sopra le attese contro shock politico | Esclusa dai calcoli direzionali. |
| 2022-10-24 | KWEB | pos, neg | china, activity_growth, china_gdp | PIL sopra le attese contro shock politico | Hang Seng ai minimi da 13 anni (Reuters): reazione osservata dominata dalla politica.\[37\] |
| 2023-01-17 | CNY=X | neg | china, activity_growth, china_gdp, china_consumption, cny | PIL 4T22 +2,9% contro 1,8%; vendite al dettaglio di dicembre -1,8% contro -8,6%\[39\]\[40\] | CNBC 17/01/2023 (Reuters poll). Martedì. Reazione osservata opposta all'attesa: Bloomberg, «onshore and offshore yuan extended drops to 0.4%» (*sell the news* dopo il rally da riapertura).\[4\] |
| 2023-01-17 | HG=F | pos | china, activity_growth, china_gdp, commodity_demand | PIL e dati di dicembre sopra le attese | Release pulita. |
| 2023-01-17 | KWEB | pos | china, activity_growth, china_gdp, china_consumption | Dati sopra le attese | Hang Seng -0,78% (Business Standard): prese di profitto.\[41\] |
| 2023-03-01 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di febbraio 52,6 contro 50,5 (massimo a 11 anni); Caixin 51,6 contro 50,2\[3\]\[42\] | Global Times: «beating a forecast of 50.5 issued by Reuters»; FXStreet: Caixin «vs. 50.2 expected».\[3\]\[42\] Entrambi mercoledì 01/03. |
| 2023-03-01 | HG=F | pos | china, activity_growth, pmi, commodity_demand | Doppio PMI molto sopra le attese | Release pulita. |
| 2023-03-01 | KWEB | pos | china, activity_growth, pmi | Doppio PMI sopra le attese | Seduta USA del 2023-03-01. |
| 2023-03-01 | AUD=X | neg | china, activity_growth, pmi, commodity_demand | Doppio PMI sopra le attese | FXStreet: «AUD/USD rebounds toward 0.6750 on China's PMIs big beat». Confondente: PIL australiano lo stesso giorno.\[3\] |
| 2023-07-17 | CNY=X | pos | china, activity_growth, china_gdp, cny | PIL 2T23 +6,3% contro 7,3% (Reuters) / 7,1% (Bloomberg)\[43\]\[44\] | CNBC 17/07/2023; Bloomberg: «The onshore yuan weakened 0.4% at 7.17 per dollar» (coerente).\[43\] Rinnovo MLF a tasso invariato (2,65%):\[45\] nessuna mossa, release considerata pulita. |
| 2023-07-17 | HG=F | neg | china, activity_growth, china_gdp, commodity_demand | PIL 2T23 sotto le attese | Lunedì. |
| 2023-07-17 | KWEB | neg | china, activity_growth, china_gdp | PIL 2T23 sotto le attese | Seduta USA del 2023-07-17. |
| 2023-07-17 | AUD=X | pos | china, activity_growth, china_gdp, commodity_demand | PIL 2T23 sotto le attese | Fonte come riga CNY=X. |
| 2024-04-16 | CNY=X | pos, neg | china, activity_growth, china_gdp, cny | PIL 1T24 +5,3% contro 4,6%, ma produzione industriale di marzo 4,5% contro 6,0%\[46\]\[47\] | Reuters via Yahoo: «expected first-quarter GDP to expand 4.6%»; CNBC: produzione industriale «missing expectations of 6%».\[46\]\[47\] Segnali opposti: attesa ambigua. |
| 2024-04-16 | HG=F | pos, neg | china, activity_growth, china_gdp, commodity_demand | PIL sopra e produzione industriale sotto le attese | Il dato mensile più rilevante per il rame (produzione industriale) è negativo: escluso dai calcoli direzionali. |
| 2024-04-16 | KWEB | pos, neg | china, activity_growth, china_gdp | Release mista | Seduta USA del 2024-04-16. |
| 2024-10-18 | CNY=X | pos, neg | china, activity_growth, china_gdp, cny, china_stimulus, pboc | Settembre: vendite al dettaglio 3,2% contro 2,5%, produzione industriale 5,4% contro 4,5%; PIL 3T 4,6% contro 4,5%; lo stesso giorno la PBOC lancia gli strumenti per l'azionario\[48\]\[49\]\[50\] | CNBC/LSEG; China Daily: «PBOC will further cut the RRR … by 0.25 to 0.5 percentage points».\[48\]\[51\] Domina lo stimolo PBOC. Su CNY=X allentamento e crescita hanno segni opposti. |
| 2024-10-18 | HG=F | pos | china, activity_growth, commodity_demand, china_stimulus, pboc | Dati sopra le attese e stimolo nello stesso giorno | Stessa direzione dai due eventi; dominante lo stimolo. Da trattare a parte. |
| 2024-11-01 | CNY=X | neg | china, activity_growth, pmi, cny | Caixin PMI di ottobre 50,3 contro 49,7 (Reuters)\[52\] | CNBC 01/11/2024: «beating the median estimate of 49.7 in a Reuters poll». Venerdì.\[52\] Confondenti: payroll USA lo stesso giorno, elezioni USA del 5/11 in T+2. |
| 2024-11-01 | HG=F | pos | china, activity_growth, pmi, commodity_demand | Caixin PMI sopra le attese | Nessuna mossa PBOC lo stesso giorno. |
| 2024-11-01 | AUD=X | neg | china, activity_growth, pmi, commodity_demand | Caixin PMI sopra le attese | Riunione RBA del 5/11 nella finestra. |
| 2025-04-16 | CNY=X | neg | china, activity_growth, china_gdp, cny, tariff_escalation | PIL 1T25 +5,4% contro 5,1% (Reuters); t/t 1,2% contro 1,4%\[53\]\[54\] | CNBC 16/04/2025: «topped Reuters poll expectations for a 5.1% growth». Mercoledì.\[53\] Contesto di escalation tariffaria USA-Cina: il dato era considerato «pre-dazi».\[55\] |
| 2025-04-16 | HG=F | pos | china, activity_growth, china_gdp, commodity_demand, tariff_escalation | PIL 1T25 sopra le attese | Dominanza dei titoli sui dazi nelle finestre successive. |
| 2025-04-16 | KWEB | pos | china, activity_growth, china_gdp, tariff_escalation | PIL 1T25 sopra le attese | Seduta USA del 2025-04-16. |
| 2025-12-31 | CNY=X | neg | china, activity_growth, pmi, cny | PMI ufficiale di dicembre 50,1 contro 49,2\[56\] | Trading Economics (via sub-ricerca); ING conferma il 50,1.\[56\]\[57\] Mercoledì; il mercato onshore chiude il 1° gennaio, liquidità di fine anno ridotta. |
| 2025-12-31 | HG=F | pos | china, activity_growth, pmi, commodity_demand | PMI ufficiale sopra le attese | Release pulita, liquidità ridotta. |
| 2026-02-02 | CNY=X | pos | china, activity_growth, pmi, cny | PMI ufficiale di gennaio 49,3 contro 50,0 (Reuters), uscito sabato 31/01\[58\]\[59\] | Trading Economics: «missing market estimates of 50»; Reuters/MarketScreener (via sub-ricerca): «Reuters poll 50.0».\[59\]\[60\] Prima seduta per tutti: lunedì 2026-02-02. RatingDog di gennaio 50,3 in linea (02/02).\[61\] |
| 2026-02-02 | HG=F | neg | china, activity_growth, pmi, commodity_demand | PMI ufficiale sotto le attese | Release pulita. |
| 2026-04-16 | CNY=X | neg | china, activity_growth, china_gdp, cny | PIL 1T26 +5,0% contro 4,8% (Reuters, 50 economisti)\[62\]\[63\] | CNBC 16/04/2026: «exceeding economists' forecast for a 4.8% growth in a Reuters poll»; investimenti fissi 1,7% contro 1,9% (lieve mancato). Giovedì. Contesto di shock petrolifero (guerra con l'Iran).\[63\] |
| 2026-04-16 | HG=F | pos | china, activity_growth, china_gdp, commodity_demand | PIL sopra le attese | Release pulita. |
| 2026-04-16 | AUD=X | neg | china, activity_growth, china_gdp, commodity_demand | PIL sopra le attese | Fonte come riga CNY=X. |
| 2026-05-18 | CNY=X | pos | china, activity_growth, china_consumption, cny | Produzione industriale di aprile 4,1% contro 5,9%; vendite al dettaglio 0,2% contro 2,0%\[64\]\[65\] | Reuters via Investing.com 18/05/2026: «missed expectations for a 5.9% increase in a Reuters poll».\[65\] Lunedì.\[66\] Nessuna mossa PBOC. |
| 2026-05-18 | HG=F | neg | china, activity_growth, commodity_demand | Produzione industriale molto sotto le attese | Release pulita. |
| 2026-05-18 | KWEB | neg | china, activity_growth, china_consumption | Vendite al dettaglio ai minimi da dicembre 2022\[64\] | Seduta USA del 2026-05-18. |
| 2026-07-15 | CNY=X | pos | china, activity_growth, china_gdp, cny | PIL 2T26 +4,3% contro 4,5% (Reuters, 54 economisti), il più debole dal 4T22\[67\]\[68\] | Reuters via Investing.com 15/07/2026: «Q2 GDP +4.3% y/y (f'cast +4.5%)»; t/t 0,9% in linea. Mercoledì.\[67\] Dati mensili di giugno nello stesso rilascio (non verificati qui). |
| 2026-07-15 | HG=F | neg | china, activity_growth, china_gdp, commodity_demand | PIL sotto le attese | Attesa di stimolo (Politburo di fine luglio) come possibile attenuante.\[67\] |
| 2026-07-15 | KWEB | neg | china, activity_growth, china_gdp | PIL sotto le attese | Seduta USA del 2026-07-15. |
| 2026-07-15 | AUD=X | pos | china, activity_growth, china_gdp, commodity_demand | PIL sotto le attese | Fonte come riga CNY=X. |
| 2026-07-31 | CNY=X | pos | china, activity_growth, pmi, cny | PMI ufficiale di luglio 49,2 contro 50,0 (Reuters, 31 economisti); non manifatturiero 49,0 contro 50,0\[69\]\[70\] | IndexBox/Reuters (poll 50,0); Investing.com: «missing economists' expectations of 50.1»; uscito venerdì 31/07 (pubblicato giovedì sera ora USA).\[69\]\[70\] |
| 2026-07-31 | HG=F | neg | china, activity_growth, pmi, commodity_demand | PMI ufficiale di nuovo sotto 50 | Release pulita. |
| 2026-10-19 | CNY=X | neg | china, activity_growth, china_gdp, china_consumption, cny | PIL 3T26 +4,5% contro 4,4%; vendite al dettaglio di settembre 1,1% contro 0,6%\[71\]\[72\] | Reuters via US News 19/10/2026: «beat the forecast for 4.4% growth in a Reuters poll».\[71\]\[72\] Lunedì. La sorpresa sul PIL è piccola (0,1): l'episodio regge sulle vendite al dettaglio, commentate da ANZ («reduce the urgency for immediate broad-based easing»).\[71\] |
| 2026-10-19 | HG=F | pos | china, activity_growth, china_gdp, commodity_demand | PIL e vendite al dettaglio sopra le attese | Produzione industriale 5,5% in linea: ampiezza attesa modesta.\[72\]\[73\] |
| 2026-11-02 | CNY=X | pos | china, activity_growth, pmi, cny | PMI ufficiale di ottobre 49,3 contro 49,9–50,0, uscito sabato 31/10\[74\]\[75\] | TradingView/Trading Economics: «missing market expectations of 50.0»; Xinhua (31/10) conferma la data.\[75\]\[76\] Prima seduta per tutti: lunedì 2026-11-02. RatingDog di ottobre atteso lo stesso lunedì (valore non verificato). |
| 2026-11-02 | HG=F | neg | china, activity_growth, pmi, commodity_demand | PMI ufficiale sotto le attese | Release pulita a livello PBOC. |
| 2026-11-02 | AUD=X | pos | china, activity_growth, pmi, commodity_demand | PMI ufficiale sotto le attese | Verificare il calendario RBA di inizio novembre come confondente. |

Date candidate escluse o risolte. Il PMI ufficiale di ottobre 2016 è datato 31 ottobre da CNBC (ora USA) ma uscito il 1° novembre a Pechino: in tabella c'è il 2016-11-01.\[22\] Analogamente, il PMI di ottobre 2026 è datato 1° novembre da UPI e 31 ottobre (sabato) da Xinhua: la prima seduta è comunque il 2026-11-02.\[76\]\[77\] Il PIL del 3T22 era programmato per il 2022-10-18 ed è stato rinviato senza spiegazioni: è uscito il 2022-10-24, la data usata in tabella.\[38\] Il PMI ufficiale di ottobre 2024 (50,1 contro 49,9) è escluso perché la sorpresa è di soli 0,2 punti, sotto soglia;\[78\] il Caixin di giugno 2017 (2017-07-03) è escluso per sovrapposizione con il 2017-06-30. Per la produzione industriale di aprile 2012 il valore (9,3%) è certo, mentre il consenso Reuters (circa 12,2% secondo la memoria della sub-ricerca) non è verificato: la riga resta solo come sorpresa «ampiamente commentata».

## §4 Statistiche indicative

Questo studio **non dispone delle serie di prezzo** dei ticker e quindi **non riporta rendimenti cumulati T+1/T+3/T+5/T+10**, che la pipeline dovrà calcolare sulle date del §3. Inventarli violerebbe il vincolo no-look-ahead e di veridicità. Si riportano invece la composizione del campione per canale, che fissa gli N su cui la pipeline lavorerà, e la frequenza con cui le reazioni effettive **documentate dalla stampa dell'epoca** coincidono con il verso atteso.

Composizione per asset. `HG=F`: 35 date, di cui 33 direzionali (19 `pos`, 14 `neg`) e 2 `pos, neg` (2022-10-24, 2024-04-16). `CNY=X`: 35 date, di cui 32 direzionali (18 `neg` su sorprese al rialzo, 14 `pos` su sorprese al ribasso) e 3 ambigue (2022-10-24, 2024-04-16, 2024-10-18). `KWEB`: 19 date, di cui 17 direzionali (9 `pos`, 8 `neg`). `AUD=X`: 14 date, tutte direzionali (5 `neg`, 9 `pos`).

Composizione per canale-dato. PMI (ufficiale, Caixin, flash HSBC/Caixin): N=21 date. PIL trimestrale (`china_gdp`): N=12. Produzione industriale/vendite al dettaglio/investimenti fissi come driver principale: N=4 (2012-05-11, 2016-04-15, 2022-05-16, 2026-05-18), **INDICATIVE ONLY**. Consumo (`china_consumption`) come canale esplicito: N=4, **INDICATIVE ONLY**. Release con stimolo lo stesso giorno (`china_stimulus`): N=2 (2022-05-16, 2024-10-18), **INDICATIVE ONLY**, da escludere dalle medie del canale «dato». Release pulite: N=33.

Coerenza segno atteso/segno osservato sulle reazioni documentate dei ticker in lista: AUD più debole il 2015-07-24 (MacroBusiness) e il 2019-04-30 (FXStreet), AUD più forte il 2023-03-01 (FXStreet), yuan onshore più debole dello 0,4% a 7,17 il 2023-07-17 (Bloomberg), tutti coerenti.\[2\]\[3\]\[28\]\[43\] Lo yuan più debole dello 0,4% il 2023-01-17 (Bloomberg), nonostante la sorpresa positiva, è invece incoerente.\[4\] Risultato: 4 coerenti su 5, N=5, **INDICATIVE ONLY**. L'unico errore è su `CNY=X`, coerentemente con la tesi che lo yuan sia il canale meno affidabile. Sui proxy non in DB la stampa documenta movimenti coerenti nel 2019-04-01 (Shanghai +2,3%, Hang Seng +1,8%)\[26\] e nel 2016-01-04 (CSI 300 -7%, con confondente), e un movimento dominato dalla politica nel 2022-10-24.\[17\]\[37\]

La pipeline dovrebbe produrre come minimo quattro statistiche: la media e la mediana del rendimento firmato (rendimento × segno atteso) per ticker e orizzonte sulle 33 release pulite; la stessa statistica separata per tipo di dato (PMI contro PIL); la stessa statistica separata per fase del §5; la percentuale di episodi con segno coerente, con l'intervallo di confidenza binomiale. Con N=14 su `AUD=X` e N=17 su `KWEB` le statistiche per fase scendono sotto 10 e vanno marcate INDICATIVE ONLY.

## §5 Fasi di regime

**`managed_peg_credit_slowdown` (2012-01-01 → 2015-08-10).** Lo yuan si muove in una banda stretta attorno a un fixing amministrato e la crescita rallenta dall'8% verso il 7%; il PMI flash HSBC è la release più seguita dal mercato. `CNY=X` è quasi insensibile ai dati, mentre `HG=F` e `AUD=X` sono molto reattivi (picco della domanda cinese di metalli). Gli analoghi di rame e AUD sono usabili con cautela nel regime corrente: l'intensità di materie prime della crescita cinese era più alta. Quelli su `CNY=X` non sono usabili.

**`post_devaluation_two_way_fx` (2015-08-11 → 2019-12-31).** Dopo la riforma del fixing dell'11 agosto 2015 lo yuan diventa bidirezionale; le paure di *hard landing* (agosto 2015-gennaio 2016) amplificano le sorprese negative, poi la reflazione 2016-2017 e la guerra commerciale 2018-2019 aggiungono `tariff_escalation`. Gli analoghi sono **parzialmente usabili**: la struttura valutaria è simile a quella attuale, ma gli episodi di stress 2015-2016 hanno ampiezze non replicabili.

**`covid_shock_and_zero_covid` (2020-01-01 → 2022-12-07).** I dati sono dominati da chiusure ed effetti base: sorprese di 10 punti di PMI (2020-03-02, 2020-03-31) e di 5 punti sulle vendite al dettaglio (2022-05-16). Gli analoghi **non sono usabili** per stimare ampiezze; il segno resta informativo. La fase si chiude con l'allentamento delle restrizioni di dicembre 2022.

**`reopening_and_deflation` (2022-12-08 → 2024-09-23).** Riapertura, delusione post-riapertura (2023-07-17), crisi immobiliare e deflazione; il mercato vende spesso le buone notizie (2023-01-17). Gli analoghi sono **usabili** per il regime corrente, con l'avvertenza della minore credibilità percepita dei dati.

**`policy_put_export_boom` (2024-09-24 → present).** Inizia con il pacchetto PBOC di fine settembre 2024 e prosegue con la crescita trainata dall'export (componentistica per l'AI), lo shock petrolifero della guerra con l'Iran nel 2026 e un target di crescita del 4,5–5,0%.\[63\]\[67\]\[70\]\[72\]\[79\] Le sorprese negative sono lette anche come anticipo di stimolo (canale redistributivo), il che attenua il segno su `HG=F` e `KWEB`. È la fase **più rappresentativa del presente**, ma con N piccolo: 9 date nel catalogo.

## §6 Caveat metodologici

**Fusi orari e sedute.** Le release escono alle 01:30–02:00 UTC. In un giorno feriale `CNY=X`, `HG=F` (Globex) e `AUD=X` reagiscono nella stessa data, mentre `KWEB`, `EEM` ed `EWY` reagiscono all'apertura USA della stessa data, dopo circa 12 ore in cui il segnale è già stato prezzato in Asia e in Europa. Per gli ETF USA il rendimento T+0 open-to-close sottostima l'effetto: va usato close(D-1)→close(D). Il PMI ufficiale NBS esce spesso di sabato o domenica (2019-03-31, 2020-02-29, 2026-01-31, 2026-10-31): la data in tabella è il lunedì per tutti i proxy. Le festività cinesi (1–7 ottobre, Primo maggio, Capodanno lunare) interrompono `CNY=X` onshore ma non `HG=F` né `AUD=X`: per il 2019-04-30 e il 2019-09-30 la T+1 di `CNY=X` cade dopo la festività, e i dati Yahoo in quei giorni possono riflettere quotazioni anomale.

**Episodi multi-causa e controlli.** Per isolare la componente cinese del rame conviene usare come controllo `^GSPC` (rischio globale) e `BZ=F` (componente energetica/geopolitica), oppure il rendimento di `HG=F` meno beta × `^GSPC`. Per `KWEB` si usa `EEM` o `^GSPC`; per `AUD=X` il differenziale con la mossa del dollaro (assente un indice DXY in DB, `^N225`/`EWY` come controllo regionale). Gli episodi più contaminati sono 2013-04-15 (crollo dei metalli preziosi), 2015-08-21 e 2016-01-04 (stress dei mercati cinesi), 2020-03-02 (COVID, Fed), 2022-10-24 (politica), 2024-10-18 (PBOC) e 2024-11-01 (payroll USA ed elezioni USA). Le finestre T+5/T+10 di 2012-05-11, 2015-02-26 e 2019-04-30 contengono mosse di policy o tariffarie successive.

**Drift di fondo.** Il rame ha attraversato un mercato ribassista nel 2012–2015 e un forte rialzo nel 2020–2021 e nel 2024–2026. Il campione ha 14 sorprese negative concentrate nel 2012–2016 e nel 2026, e 19 positive distribuite nel periodo: senza sottrarre il drift di periodo (per esempio il rendimento medio di 10 giorni nei 60 giorni precedenti) le medie per segno sono distorte. Lo stesso vale per `CNY=X`, che ha un trend di deprezzamento nel 2015–2016 e nel 2018–2019.

**Canali con N strutturalmente piccolo.** Il consumo (`china_consumption`) e lo stimolo nello stesso giorno (`china_stimulus`) hanno N≤4; il PIL è trimestrale (massimo 4 release l'anno) e spesso la sorpresa è inferiore a 0,2 punti, quindi pochi episodi superano la soglia. L'investimento fisso compare quasi sempre come dato secondario. Le fasi `covid_shock_and_zero_covid` e `policy_put_export_boom` hanno meno di 10 date ciascuna.

**Serie citate ma non disponibili.** CNH offshore (reazione più pulita dello yuan, 24 ore su 24), Hang Seng e Hang Seng China Enterprises (equity cinesi nello stesso fuso), CSI 300 (mercato onshore), minerale di ferro SGX/DCE (canale acciaio-costruzioni, il più puro per `AUD=X`), il Caixin/RatingDog PMI come serie, e il consenso Bloomberg/Reuters come serie. Quest'ultimo è necessario per standardizzare la sorpresa (z-score); qui è ricostruito episodio per episodio dalla stampa.

**Fonti e incertezze residue.** I consensi provengono da sondaggi Reuters (riportati da CNBC, Investing.com, Yahoo, Business Standard), Bloomberg, ForexLive, FXStreet e Trading Economics; per lo stesso dato possono differire di 0,1–0,2 punti (per esempio luglio 2026: 50,0 secondo Reuters/IndexBox, 50,1 secondo Investing.com).\[69\]\[70\] Le mosse di policy adiacenti sono state verificate. Il taglio RRR di 50 pb del maggio 2012 è annunciato nel weekend dopo il 2012-05-11 (China Briefing lo data 13 maggio). Il taglio dei tassi di 25 pb è di sabato 2015-02-28 (CNBC). Il taglio del reverse repo a 7 giorni dal 2,40% al 2,20% è di lunedì 2020-03-30 (CNBC, Xinhua). La riduzione di 20 pb del limite minimo dei mutui per la prima casa è di domenica 2022-05-15 (SCMP). Resta invece non verificato il consenso numerico di aprile 2012. Dal 2025 il PMI privato Caixin è pubblicato con il marchio RatingDog (S&P Global): le serie storiche vanno raccordate.\[80\]

```yaml
---
title: "Sorprese dei dati di attività cinesi e trasmissione a yuan, rame e asset cinesi (2012–2026): catalogo di 35 episodi per event study"
date_compiled: 2026-11-10
primary_theme: macro_data
sub_themes: [china, activity_growth, china_gdp, pmi, cny, china_stimulus, china_consumption, commodity_demand, pboc, tariff_escalation]
relevant_assets: [CNY=X, HG=F, KWEB, AUD=X, EEM, EWY, ^N225, BZ=F, ^GSPC]
external_assets_mentioned:
  - "CNH (USD/CNH offshore) — reagisce 24h e senza vincolo di fixing, misura più pulita del canale yuan"
  - "Hang Seng / Hang Seng China Enterprises — equity cinesi nello stesso fuso della release, evitano il disallineamento di KWEB"
  - "CSI 300 — mercato onshore, rilevante per 2016-01-04 (circuit breaker) e 2019-04-01"
  - "Minerale di ferro SGX/DCE — canale acciaio-costruzioni, driver più diretto di AUD"
  - "Caixin/RatingDog PMI come serie — necessario per ricostruire la storia completa delle sorprese PMI private"
  - "Consenso Bloomberg/Reuters come serie — necessario per standardizzare la sorpresa in z-score"
time_window:
  start: 2012-01-01
  end: present
regime_phases:
  - managed_peg_credit_slowdown: 2012-01-01 to 2015-08-10
  - post_devaluation_two_way_fx: 2015-08-11 to 2019-12-31
  - covid_shock_and_zero_covid: 2020-01-01 to 2022-12-07
  - reopening_and_deflation: 2022-12-08 to 2024-09-23
  - policy_put_export_boom: 2024-09-24 to present
keywords: [Cina, PIL cinese, PMI, Caixin, NBS, produzione industriale, vendite al dettaglio, investimenti fissi, yuan, rame, consenso, sorpresa, China GDP, China PMI, Caixin PMI, industrial production, retail sales, data surprise, hard landing]
```

## Sources

1. [Copper falls on weak China data and QE outlook](https://www.tradingpedia.com/2013/07/04/copper-falls-on-weak-china-data-and-qe-outlook/)
2. [Aussie dollar tanks with China Flash PMI - MacroBusiness](https://www.macrobusiness.com.au/2015/07/aussie-dollar-smashed-on-china-flash-pmi-tank/)
3. [China's Caixin Manufacturing PMI expands to 51.6 in February vs. 50.2 expected](https://www.fxstreet.com/news/chinas-caixin-manufacturing-pmi-expands-to-516-in-february-vs-502-expected-202303010148)
4. [china fourth quarter gdp key data](https://www.bloomberg.com/news/live-blog/2023-01-17/china-fourth-quarter-gdp-key-data)
5. [China's GDP Report Delivers Disappointing News](https://www.bloomberg.com/news/articles/2013-04-15/chinas-gdp-report-delivers-disappointing-news)
6. [www.benzinga.com](https://www.benzinga.com/article/3496809)
7. [Strong new orders lift China HSBC flash PMI to seven-month high in October](https://www.yahoo.com/news/china-october-hsbc-flash-pmi-020342929.html)
8. [www.fxstreet.com](https://www.fxstreet.com/analysis/european-market-update/2013/10/24)
9. [China July HSBC flash PMI at 18-month high as stimulus revs up economy](https://www.business-standard.com/amp/article/reuters/china-july-hsbc-flash-pmi-at-18-month-high-as-stimulus-revs-up-economy-114072400612_1.html)
10. [China February HSBC PMI inches up](https://www.pressreader.com/uae/gulf-news/20150226/282570196559573)
11. [Caixin Flash China General Manufacturing PMI](https://download.caixin.com/upload/caixinpmien.pdf)
12. [Flash China Caixin PMI falls to 47.1 in August](https://www.cnbc.com/2015/08/20/flash-china-caixin-pmi-falls-to-471-in-august.html)
13. [77-Month Low for August's Early Caixin Manufacturing PMI - Caixin Global](http://english.caixin.com/2015-08-21/100842078.html)
14. [Caixin PMI falls to 48.2 in December, below expectations](https://www.cnbc.com/2016/01/03/caixin-pmi-falls-to-482-in-december-below-expectations.html)
15. [Happy New Year: Global Stocks Crash After China Is Halted Limit Down In Worst Start To Year In History](https://infiniteunknown.net/2016/01/04/happy-new-year-global-stocks-crash-after-china-is-halted-limit-down-in-worst-start-to-year-in-history/)
16. [Asian markets set for cautious open; China Caixin PMI due](https://www.cnbc.com/2016/01/03/asian-markets-set-for-cautious-open-china-caixin-pmi-due.html)
17. [Asia ETF Roundup (Market)](<https://my.morningstar.com/my/news/146969/asia-etf-roundup-(market)-%E2%80%93-december-2015-and-january-2016.aspx>)
18. [China's new circuit breaker may have worsened drop](https://www.cnbc.com/2016/01/04/chinas-new-circuit-breaker-may-have-worsened-drop.html)
19. [China's economy expanded 6.7% on-year in Q1, versus 6.8% in Q4: Reuters](https://www.cnbc.com/2016/04/14/chinas-economy-expanded-67-on-year-in-q1-versus-68-in-q4-reuters.html)
20. [China GDP Growth Slows to 6.7% in Q1](https://tradingeconomics.com/articles/04152016033628.htm)
21. [Expert Views: China Q1 GDP growth eases to 6.7 percent, meets view; other indicators beat forecast](https://www.business-standard.com/amp/article/reuters/expert-views-china-q1-gdp-growth-eases-to-6-7-percent-meets-view-other-indicators-beat-forecast-116041500136_1.html)
22. [China official manufacturing PMI at 51.2 in October, beating forecasts](https://www.cnbc.com/2016/10/31/china-official-manufacturing-pmi-at-512-in-october-beating-forecasts.html)
23. [China Caixin manufacturing November PMI above expectations; Reuters](https://www.cnbc.com/2016/11/30/china-official-november-pmi-above-expectations-reuters.html)
24. [Caixin PMI for June comes in at three-month high, beating forecast](https://www.cnbc.com/2017/07/02/caixin-pmi-for-june-comes-in-at-three-month-high-beating-forecast.html)
25. [ForexLive Asia FX news wrap: China PMIs improve to expansion, risk boosted](https://investinglive.com/news/!/forexlive-asia-fx-news-1-apr-20190401)
26. [Chinese Manufacturing Activity Unexpectedly Rebounds in March](https://investing.com/news/economic-indicators/economic-activities-in-china-unexpectedly-recovers-in-march-1823337)
27. [China economy: Official and Caixin manufacturing PMI for April](https://www.cnbc.com/2019/04/30/china-economy-official-and-caixin-manufacturing-pmi-for-april.html)
28. [China's Caixin manufacturing PMI unexpectedly drops to 50.2 in April (Aussie weaker)](https://www.fxstreet.com/news/chinas-caixin-manufacturing-pmi-unexpectedly-drops-to-502-in-april-aussie-weaker-201904300148)
29. [China economy: Official, Caixin manufacturing PMI for September](https://www.cnbc.com/2019/09/30/china-economy-official-caixin-manufacturing-pmi-for-september.html)
30. [China Economy: Caixin/Markit February manufacturing PMI amid coronavirus](https://www.cnbc.com/2020/03/02/china-economy-caixinmarkit-february-manufacturing-pmi-amid-coronavirus.html)
31. [China PMI: Factory activity shrank at fastest rate on record in February](https://www.cnbc.com/2020/02/29/china-pmi-factory-activity-shrank-at-fastest-rate-on-record-in-february.html)
32. [China says manufacturing activity expanded in March, defying expectations of a contraction](https://www.cnbc.com/2020/03/31/china-reports-march-manufacturing-pmi-amid-coronavirus-outbreak.html)
33. [China's second-quarter GDP grows 3.2% year-on-year, beats expectations](https://news.yahoo.com/chinas-second-quarter-gdp-grows-022355137.html)
34. [China data April Retail sales & Industrial production both plunge](https://investinglive.com/news/china-data-april-retail-sales-industrial-production-both-plunge-20220516/)
35. [China’s economic data disappoint in April as Covid controls weigh - Market Trading Essentials](https://www.markettradingessentials.com/2022/05/chinas-economic-data-disappoint-in-april-as-covid-controls-weigh/)
36. [China counts cost of lockdowns](https://www.pressreader.com/thailand/bangkok-post/20220517/282024740863384)
37. [China Q3 GDP growth tops forecasts but meaningful rebound elusive](https://www.rappler.com/business/gross-domestic-product-china-q3-2022/)
38. [China GDP beats with a bounce in the third quarter, delayed data shows](https://www.cnbc.com/2022/10/24/china-third-quarter-gdp.html)
39. [China reports 3% GDP growth for 2022 as December retail sales, industrial production beat estimates](https://www.nbcnews.com/news/world/china-reports-3-gdp-growth-2022-december-retail-sales-industrial-produ-rcna66034)
40. [China reports 3% GDP growth for 2022 as December retail sales, industrial production beat estimates](https://www.cnbc.com/2023/01/17/china-reports-3percent-gdp-growth-for-2022.html)
41. [Wednesday, December 17, 2025 | 02:09 PM ISTहिंदी में पढें](https://www.business-standard.com/article/news-cm/hong-kong-hang-seng-falls-from-6-month-high-123011701008_1.html)
42. [China’s PMI beats forecast to hit 11-year high in Feb, pointing to fast economic recovery - Global Times](https://www.globaltimes.cn/page/202303/1286420.shtml)
43. [China GDP Grows 6.3% in Second Quarter Missing Estimates - Bloomberg](https://www.bloomberg.com/news/live-blog/2023-07-17/china-second-quarter-gdp-key-data-liquidity-operations)
44. [China reports second-quarter GDP miss, another record high in youth unemployment](https://www.cnbc.com/2023/07/17/china-reports-q2-gdp-miss-another-record-high-in-youth-unemployment.html)
45. [China's economy grew 6.3% in Q2, lower than expected as momentum slows](https://www.business-standard.com/amp/world-news/china-s-economy-grew-6-3-in-q2-lower-than-expected-as-momentum-slows-123071700078_1.html)
46. [China's Q1 GDP grows 5.3% y/y, well above forecast](https://finance.yahoo.com/news/chinas-q1-gdp-grows-5-021132705.html)
47. [China beats expectations for Q1 GDP growth but March activity data comes in below forecasts](https://www.cnbc.com/video/2024/04/16/china-beats-expectations-for-q1-gdp-growth-but-march-activity-data-comes-in-below-forecasts.html)
48. [China reports better-than-expected retail sales and industrial production data](https://www.cnbc.com/2024/10/18/china-retail-sales-urban-investment-september.html)
49. [China Economy: PBOC Starts Share Buyback, Equity Swap Programs to Boost Markets - Bloomberg](https://www.bloomberg.com/news/articles/2024-10-18/pboc-starts-share-buyback-equity-swap-programs-to-boost-markets)
50. [China reports third-quarter GDP growth of 4.6%, slightly beating expectations](https://www.nbcnews.com/news/world/china-reports-third-quarter-gdp-growth-46-slightly-beating-expectation-rcna176047)
51. [PBOC to implement third RRR cut for 2024, lifting Chinese shares - Chinadaily.com.cn](https://global.chinadaily.com.cn/a/202410/18/WS6711ee8ba310f1265a1c853f.html)
52. [China’s Caixin manufacturing PMI for October](https://www.cnbc.com/2024/11/01/chinas-caixin-manufacturing-pmi-for-october.html)
53. [China's first-quarter GDP tops estimates at 5.4% as growth momentum continues amid tariff worries](https://www.cnbc.com/2025/04/16/chinas-first-quarter-gdp-growth-at-as-trade-war-heats-up.html)
54. [China Q1 GDP Growth Beats Expectations - Economic Outlook](https://www.globalbankingandfinance.com/CHINA-ECONOMY-GDP-464518a1-c971-4138-b83a-dc94b6c5f0f4/)
55. [Q1 2025 GDP: China posts unexpectedly strong 5.4% economic growth before tariffs bite](https://www.cnn.com/2025/04/15/business/china-economy-growth-q1-hnk-intl)
56. [China NBS Manufacturing PMI Falls to 4-Month Low](https://tradingeconomics.com/china/business-confidence/news/530347)
57. [China’s soft PMI data suggests domestic challenges carried over into 2026](https://think.ing.com/snaps/chinas-mixed-pmi-data-suggests-domestic-challenges-remain-to-start-2026/)
58. [China January official manufacturing PMI drops to 49.3 By Reuters](https://www.investing.com/news/economy-news/china-january-official-manufacturing-pmi-drops-to-493-4477612)
59. [China January official manufacturing PMI at 49.3 (Reuters poll 50.0, prev month 50.1)](https://www.marketscreener.com/news/china-january-official-manufacturing-pmi-at-49-3-reuters-poll-50-0-prev-month-50-1-ce7e5bdcd080f123)
60. [China Manufacturing PMI Below Forecasts](https://tradingeconomics.com/china/business-confidence/news/521821)
61. [China's factory activity grows at fastest pace since October, private survey shows, beating official reading](https://www.cnbc.com/2026/02/02/china-factory-activity-private-survey-official-reading-pmi-january-lunar-new-year-ratingdog.html)
62. [China poised for Q1 GDP growth rebound but Iran war dims 2026 outlook: Reuters poll](https://ca.finance.yahoo.com/news/china-poised-q1-gdp-growth-083204862.html)
63. [China economic growth accelerates to 5% in first quarter — but Iran war clouds outlook](https://www.cnbc.com/2026/04/16/china-gdp-growth-first-quarter-exports-property-retail-sales-iran-war.html)
64. [China’s economy slows in April as output, retail sales sharply undershoot forecasts By Reuters](https://www.investing.com/news/economy-news/chinas-economy-slows-in-april-as-output-retail-sales-sharply-undershoot-forecasts-4694608)
65. [China’s April industrial output, retail sales growth miss expectations By Reuters](https://www.investing.com/news/economy-news/chinas-april-industrial-output-retail-sales-growth-miss-expectations-4694603)
66. [China's April industrial output, retail sales growth miss expectations](https://finance.yahoo.com/economy/articles/chinas-april-industrial-output-retail-020150348.html)
67. [China’s second-quarter economic growth misses market forecast By Reuters](https://www.investing.com/news/economy-news/chinas-secondquarter-economic-growth-misses-market-forecast-4792126)
68. [China’s GDP growth set to slow, raising expectations for more stimulus By Reuters](https://www.investing.com/news/economy-news/chinas-gdp-growth-set-to-slow-raising-expectations-for-more-stimulus-4787575)
69. [China manufacturing PMI unexpectedly slips into contraction in July By Investing.com](https://www.investing.com/news/economic-indicators/china-manufacturing-pmi-unexpectedly-slips-into-contraction-in-july-4826676)
70. [China Manufacturing PMI Forecast to Hit 50.0 in July 2026 - News and Statistics - IndexBox](https://www.indexbox.io/blog/chinas-factory-activity-expected-to-stall-in-july-2026/)
71. [China's Economic Growth Accelerates to 4.5% in Third Quarter](https://money.usnews.com/investing/news/articles/2026-10-18/chinas-economic-growth-accelerates-to-4-5-in-third-quarter)
72. [China's Economic Growth Picks up in Third Quarter, Beating Expectations](https://money.usnews.com/investing/news/articles/2026-10-18/chinas-economic-growth-picks-up-in-third-quarter-beating-expectations)
73. [China industrial output, retail sales beat forecasts in September](https://finance.yahoo.com/economy/articles/china-industrial-output-retail-sales-025938695.html)
74. [China’s factory and services PMI gauges both drop below 50 as fourth quarter starts on a weak note](https://investinglive.com/news/china-s-factory-and-services-pmi-gauges-both-drop-below-50-as-fourth-quarter-starts-on-a-weak-note/)
75. [China Manufacturing Unexpectedly Weakens — TradingView News](https://www.tradingview.com/news/te_news:596971:0-china-manufacturing-unexpectedly-weakens/)
76. [China's manufacturing PMI softens, high-tech sector maintains expansion - People's Daily Online](http://en.people.cn/n3/2026/1031/c90000-20514322.html)
77. [China's manufacturing contracts as deflation fears deepen - UPI.com](https://www.upi.com/amp/Top_News/World-News/2026/11/01/manufacturing-index-pmi-deflation/6761793586387/)
78. [China's factory activity expands for the first time since April, official survey shows](https://www.cnbc.com/2024/10/31/pmi-chinas-factory-activity-expands-for-the-first-time-since-april.html)
79. [China Exceeds Growth Expectations Amid AI-Boosted Exports - ChinaRetailNews.com](https://www.chinaretailnews.com/2026/10/19/29712-china-exceeds-growth-expectations-amid-ai-boosted-exports/)
80. [China's factory activity slows down in October, missing expectations, private survey shows](https://www.cnbc.com/2025/11/03/china-factory-activity-october-pmi-ratingdog-private-survey-shows.html)
