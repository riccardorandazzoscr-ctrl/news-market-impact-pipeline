# Episodi da dichiarare nel verso — candidati

_Generato il 2026-10-15 da `candidati_verso.py` (scratchpad), libreria a 1310 episodi._

Ordine: notizie del periodo 2026-09-20 → 2026-10-15 che toccano il gruppo (righe di triage + lacune che nominano tema o asset di riferimento e una parola chiave del gruppo). È una misura grezza della domanda, non un conteggio esatto di schede perse.

Per ogni episodio: data, etichette date-locali, la fonte che una revisione in `_direction_reviews.yaml` dovrebbe citare, e la riga della fonte che contiene la data. Il verso NON è suggerito: va deciso leggendo la fonte (pressione sul prezzo del riferimento, non ritorno ex post; data con spinte opposte → `status: excluded`).

Nota: molte righe di contesto mostrano già un verso (`pos`/`neg`) scritto dalla scheda: la libreria non lo usa perché manca il `direction_reference`. Una revisione che conferma quel verso sull'asset giusto basta a renderlo utilizzabile.

| # | Gruppo | Riferimento | Menzioni (giorni) | Già dichiarati | Esclusi | Da rivedere |
|---|---|---|---:|---:|---:|---:|
| 1 | Inflazione USA | `IEF` | 27 (14) | 30 | 13 | 42 |
| 2 | Capex AI | `SOXX` | 21 (12) | 9 | 11 | 5 |
| 3 | Fed hawkish / term premium | `IEF` | 21 (12) | 28 | 40 | 1 |
| 4 | Tregue commerciali USA-Cina | `CNY=X` | 18 (8) | 0 | 0 | 19 |
| 5 | Dati area euro | `EURUSD=X` | 17 (10) | 6 | 7 | 24 |
| 6 | Crisi fiscali sovrane UE | `BTP_BUND_SPREAD` | 15 (8) | 0 | 0 | 40 |
| 7 | Fiducia e consumi USA | `^FVX` | 13 (8) | 25 | 7 | 18 |
| 8 | ISM / PMI USA | `^TNX` | 10 (6) | 3 | 1 | 23 |
| 9 | Dati macro cinesi | `CNY=X` | 10 (7) | 6 | 0 | 20 |
| 10 | Elezioni (Brasile) | `EWZ` | 8 (5) | 3 | 0 | 20 |
| 11 | Difesa / NATO | `SHLD.L` | 8 (6) | 19 | 0 | 14 |
| 12 | Lavoro USA | `IEF` | 7 (6) | 26 | 8 | 16 |
| 13 | BCE: decisioni e discorsi | `EURUSD=X` | 6 (3) | 0 | 0 | 17 |
| 14 | Aste del Tesoro / term premium | `IEF` | 6 (2) | 0 | 0 | 15 |
| 15 | Inflazione giapponese | `JPY=X` | 6 (4) | 5 | 1 | 2 |

## 1. Inflazione USA — riferimento `IEF`

tema `macro_data`, almeno uno di `inflation_print`. Menzioni: 27 in 14 giorni. Già dichiarati: 30, esclusi: 13, da rivedere: **42**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-07-24 | activity_growth, china_inflation, cny, commodity_demand, cpi, energy_passthrough, eurozone_release, inflation_print, pmi | `card:2026-09-12/news_03.md` | 2026-07-24 pos inflation_print, activity_growth Dati estivi 2026 con inflazione in risalita per la componente energetica. |
| 2026-06-11 | activity_growth, ecb, eurozone_release, guidance_pivot, hawkish, inflation_print, japan_release, labour_market, rate_decision, term_premium, us_cpi | `card:2026-09-12/news_03.md` | 2026-06-11 pos us_cpi, inflation_print CPI di maggio 2026: primo passaggio dell'energia nei prezzi al consumo di quest'anno. |
| 2025-08-21 | activity_growth, china_consumption, cny, eurozone_release, inflation_print, pmi | `card:2026-09-12/news_03.md` | 2025-08-21 pos activity_growth, inflation_print Dati di attività di agosto 2025. |
| 2025-07-31 | inflation_print | `card:2026-08-19/news_06.md` | - 2025-07-31 — riunione con revisione al rialzo delle proiezioni di inflazione: guidance restrittiva senza mossa sui tassi . |
| 2025-05-23 | inflation_print, inflation_upside, japan_cpi, japan_release | `kb:Giappone; i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente)/Giappone- i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente).md` | 2025-05-23 CPI nazionale aprile core +3,5% (massimo ~2 anni, atteso +3,4%) CPI nazionale giapponese / Japan CPI ~3,5 settimane (prima del 17/6) JPY pos; 1482.T neg JPY=X  |
| 2025-04-25 | inflation_print, inflation_upside, japan_release, tariff_escalation | `kb:Giappone; i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente)/Giappone- i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente).md` | 2025-04-25 Tokyo core CPI aprile +3,4% (massimo da 2 anni, atteso +3,2%) CPI Tokyo / Tokyo CPI ~5 giorni (prima del 1/5) JPY pos "atteso" ma realizzato neg JPY=X (aspetta |
| 2025-03-09 | inflation_print | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2025-03-09 CPI febbraio 2025 −0,7% a/a: primo calo da gen-2024, oltre attese Bloomberg −0,4%; core negativo deflation_print ribasso EXV7.DE Data del rilascio; distorsione |
| 2025-03-03 | activity_growth, china_gdp, china_inflation, cny, eurozone_release, inflation_print, ism, pmi, tariff_escalation, us_cpi | `card:2026-09-12/news_03.md` | 2025-03-03 pos activity_growth, ism Indagine ISM (Institute for Supply Management — il sondaggio mensile sui responsabili acquisti) manifatturiera con componente prezzi i |
| 2024-12-27 | inflation_print | `kb:Giappone; i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente)/Giappone- i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente).md` | 2024-12-27 Tokyo CPI dicembre +3,0% a/a (core-core +2,4%) CPI Tokyo / Tokyo CPI ~4 settimane (prima del 24/1/2025) JPY pos; 1482.T neg JPY=X (aspettative) Venerdì; yen si |
| 2024-11-29 | inflation_print, inflation_upside, japan_release | `kb:Giappone; i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente)/Giappone- i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente).md` | 2024-11-29 Tokyo CPI novembre core +2,2% (atteso +2,1%) CPI Tokyo / Tokyo CPI ~3 settimane (prima del 19/12) JPY pos; 1482.T neg JPY=X (aspettative) Venerdì; yen balzò ~1 |
| 2024-11-22 | inflation_print, inflation_upside, japan_cpi, japan_release | `kb:Giappone; i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente)/Giappone- i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente).md` | 2024-11-22 CPI nazionale ottobre core +2,3% (sopra attese) CPI nazionale giapponese / Japan CPI ~4 settimane (prima del 19/12) JPY pos; 1482.T neg JPY=X (aspettative) Usc |
| 2024-08-22 | activity_growth, cny, energy_supply_shock, eurozone_release, inflation_print, pboc, pmi | `card:2026-09-12/news_03.md` | 2024-08-22 pos activity_growth, inflation_print Revisioni e dati di attività di fine estate 2024. |
| 2024-06-06 | activity_growth, ecb, eurozone_release, inflation_print, labour_market, rate_decision | `card:2026-09-12/news_03.md` | 2024-06-06 pos labour_market, inflation_print Dati del lavoro di maggio 2024. |
| 2024-05-31 | inflation_print | `card:2026-08-14/news_05.md` | --events 2023-08-01,2023-08-03,2023-08-11,2023-11-14,2023-12-08,2023-12-31,2024-01-05,2024-01-19,2024-02-02,2024-04-01,2024-04-05,2024-04-10,2024-05-31,2024-06-07,2024-07 |
| 2024-04-10 | inflation, inflation_print, inflation_upside | `card:2026-08-14/news_05.md` | --events 2023-08-01,2023-08-03,2023-08-11,2023-11-14,2023-12-08,2023-12-31,2024-01-05,2024-01-19,2024-02-02,2024-04-01,2024-04-05,2024-04-10,2024-05-31,2024-06-07,2024-07 |
| 2024-03-22 | activity_growth, boj_normalization, inflation_print, japan_cpi, japan_release | `card:2026-09-12/news_03.md` | 2024-03-22 pos inflation_print, activity_growth Riaccelerazione dei prezzi nel primo trimestre 2024. |
| 2024-02-13 | inflation_print, inflation_upside | `card:2026-08-01/news_03.md` | 2024-01-05, 2024-01-19, 2024-02-02, 2024-02-13, 2024-04-01, 2024-04-05, |
| 2024-02-08 | inflation_print | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2024-02-08 CPI gennaio 2024 −0,8% a/a: calo più forte da settembre 2009, 4° mese negativo; PPI −2,5% (16° calo); oltre attese Reuters −0,5% deflation_print ribasso EXV7.D |
| 2024-01-19 | consumer, inflation_downside, inflation_print, retail, umich, us_cpi | `card:2026-08-14/news_05.md` | --events 2023-08-01,2023-08-03,2023-08-11,2023-11-14,2023-12-08,2023-12-31,2024-01-05,2024-01-19,2024-02-02,2024-04-01,2024-04-05,2024-04-10,2024-05-31,2024-06-07,2024-07 |
| 2023-09-13 | inflation_print | `card:2026-07-31/news_05.md` | 2023-08-11 , 2023-09-13 , 2023-11-14 , 2023-12-08 , 2023-12-31 , 2024-01-05 , |
| 2023-08-31 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2023-08-31 neg inflation_print, eurozone_release flash di agosto 2023 al 5,3% contro 5,1% atteso → ultimo rialzo BCE di settembre prezzato, prezzo bond giù |
| 2023-08-09 | inflation_print | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2023-08-09 CPI luglio 2023 −0,3% a/a: prima deflazione da febbraio 2021; PPI −4,4% deflation_print ribasso EXV7.DE, ^GDAXI Redistributivo : finestra T+1/T+10 coglie solo  |
| 2023-06-23 | activity_growth, cny, commodity_energy_oil, eurozone_release, inflation_print, pboc, pmi | `card:2026-09-12/news_03.md` | 2023-06-23 pos inflation_print, activity_growth Metà 2023, fase di "higher for longer". |
| 2023-06-21 | britain_release, inflation_print, inflation_upside | `card:2026-09-08/news_06.md` | 2023-06-21 neg britain_release, inflation_print Inflazione britannica di maggio 2023 sopra le attese, il giorno prima del rialzo di 50 punti base della BoE: episodio di s |
| 2023-06-02 | inflation_print, labour_market | `card:2026-08-05/news_03.md` | Tenuti (29): 2022-02-04 , 2022-06-03 , 2022-07-08 , 2022-08-05 , 2022-10-07 , 2022-12-01 , 2023-02-03 , 2023-06-01 , 2023-06-02 , 2023-07-31 , 2023-08-01 , 2023-12-08 , 2 |
| 2023-01-04 | energy_passthrough, eurozone_release, inflation_print | `card:2026-09-02/news_05.md` | 2023-01-04 neg inflation_print Dato di prezzo di inizio 2023 |
| 2022-10-31 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | - Regime: la fase più simile della research è energy_war_shock (2022-02-24 → 2022-10-31): inflazione trainata dall'energia per una guerra, BCE costretta a stringere mentr |
| 2022-09-29 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --subtheme eurozone_release --match-all --direction neg --direction-reference IEAG.AS |
| 2022-08-31 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-08-31 neg inflation_print, eurozone_release flash di agosto 2022 al 9,1%, sopra le attese, con il gas ai massimi → rialzo da 75 punti base prezzato, prezzo bond giù |
| 2022-07-13 | hot_surprise, inflation_print | `card:2026-07-22/news_05.md` | --events 2015-08-24,2015-09-03,2015-12-01,2018-02-02,2018-10-05,2019-08-01,2019-09-04,2019-10-01,2021-10-13,2021-10-14,2021-11-10,2021-12-09,2022-02-04,2022-04-01,2022-04 |
| 2022-05-31 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-05-31 neg inflation_print, eurozone_release flash di maggio 2022 all'8,1% contro 7,7% atteso → il mercato prezza rialzi più ampi a luglio, prezzo bond giù |
| 2022-05-30 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --subtheme eurozone_release --match-all --direction neg --direction-reference IEAG.AS |
| 2022-05-11 | inflation_print | `card:2026-07-22/news_05.md` | --events 2015-08-24,2015-09-03,2015-12-01,2018-02-02,2018-10-05,2019-08-01,2019-09-04,2019-10-01,2021-10-13,2021-10-14,2021-11-10,2021-12-09,2022-02-04,2022-04-01,2022-04 |
| 2022-03-30 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --subtheme eurozone_release --match-all --direction neg --direction-reference IEAG.AS |
| 2022-03-02 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-03-02 neg inflation_print, eurozone_release flash di febbraio 2022 al 5,8% contro 5,6% atteso, pochi giorni dopo l'invasione dell'Ucraina → inflazione energetica e r |
| 2022-02-10 | inflation_print | `card:2026-06-17/news_05.md` | - 2022-02-10 — CPI USA gennaio 2022: 7,5% vs 7,3% — upside surprise in un regime già hawkish. |
| 2021-11-29 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2021-11-29 neg inflation_print, eurozone_release CPI preliminari di Germania e Spagna di novembre 2021 ai massimi da decenni, vigilia della flash al 4,9% → più stretta pr |
| 2021-11-10 | inflation_print | `card:2026-07-22/news_05.md` | --events 2015-08-24,2015-09-03,2015-12-01,2018-02-02,2018-10-05,2019-08-01,2019-09-04,2019-10-01,2021-10-13,2021-10-14,2021-11-10,2021-12-09,2022-02-04,2022-04-01,2022-04 |
| 2021-10-29 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2021-10-29 neg inflation_print, eurozone_release flash di ottobre 2021 al 4,1% contro 3,7% atteso, trainata dall'energia → il mercato anticipa la fine dei tassi negativi, |
| 2021-10-14 | inflation_print | `card:2026-07-31/news_05.md` | 2023 ( 2019-10-01 , e la serie 2021-2022 da 2021-10-14 a 2022-12-01 ). Motivo: in |
| 2021-10-13 | inflation_print, inflation_upside | `card:2026-07-22/news_05.md` | --events 2015-08-24,2015-09-03,2015-12-01,2018-02-02,2018-10-05,2019-08-01,2019-09-04,2019-10-01,2021-10-13,2021-10-14,2021-11-10,2021-12-09,2022-02-04,2022-04-01,2022-04 |
| 2015-09-03 | activity_growth, china, cny, commodity_demand, ecb, eurozone_release, flash_cpi, global_pmi, inflation_print, ism, pboc, pmi | `card:2026-09-09/news_03.md` | 2015-09-03 pos cny, china, commodity_demand, activity_growth Coda della svalutazione dello yuan dell'agosto 2015: la PBOC riprende il controllo del fixing dopo lo shock. |

## 2. Capex AI — riferimento `SOXX`

tema `structural_themes`, almeno uno di `ai_capex`, `ai_capex_financing`, `hyperscaler_capex`. Menzioni: 21 in 12 giorni. Già dichiarati: 9, esclusi: 11, da rivedere: **5**.

> Pochi episodi e quasi tutti già decisi: la domanda è alta ma la libreria è corta. Qui serve research, non solo revisione.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2025-08-28 | ai_capex, ai_capex_spending, ai_semis, earnings_shock, hyperscaler_capex, tariff_escalation | `card:2026-09-12/news_05.md` | 2025-08-28 pos ai_capex, ai_semis Segnale di domanda di fine estate 2025 sulla componente semiconduttori. |
| 2025-01-30 | ai_capex, ai_capex_spending, hyperscaler, hyperscaler_capex | `kb:Ciclo semiconduttori & AI capex (2023–2026)/Ciclo semiconduttori & AI capex (2023–2026).md` |  |
| 2025-01-21 | ai_capex, ai_capex_spending, regulatory_anticipation | `kb:Regolazione anticipata dell'AI e pause di sicurezza dei modelli; trasmissione ai semiconduttori, al software e alle utility — regime ed episodi storici (2018–presente)/Regolazione anticipata dell'AI e pause di sicurezza dei modelli- trasmissione ai semiconduttori, al software e alle utility — regime ed episodi storici (2018–presente).md` | 2025-01-21 IGV neutral regulatory_anticipation Primo giorno di contrattazione dopo la revoca dell'EO 14110 da parte di Trump Revoca il 2025-01-20, giorno dell'insediament |
| 2024-02-22 | ai_capex, ai_capex_spending, ai_capex_super_cycle, ai_chip, ai_semis, earnings_shock, export_controls | `card:2026-09-12/news_05.md` | 2024-02-22 pos ai_capex, earnings_shock Trimestrale Nvidia molto oltre le attese in piena fase di espansione dei multipli. |
| 2022-12-31 | ai_capex | `card:2026-08-15/news_04.md` | --events 2018-12-26,2020-09-03,2021-11-30,2022-04-26,2022-10-07,2022-11-10,2022-12-31,2023-01-01,2023-05-25,2023-07-03,2023-11-14,2024-02-22,2024-05-23,2024-06-10,2024-06 |

## 3. Fed hawkish / term premium — riferimento `IEF`

tema `monetary_policy`, almeno uno di `hawkish`, `term_premium`. Menzioni: 21 in 12 giorni. Già dichiarati: 28, esclusi: 40, da rivedere: **1**.

> Già quasi tutto deciso (28 dichiarati, 40 esclusi): il pool corto viene dalle esclusioni per spinte opposte, non da versi mancanti.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2022-06-09 | ecb, guidance_pivot, hawkish, rate_decision, stagflation, yen | `card:2026-08-16/news_04.md` | --events 2014-09-17,2018-03-21,2018-06-13,2018-12-19,2022-02-03,2022-06-09,2022-07-21,2022-08-26,2022-09-08,2022-09-21,2022-12-14,2022-12-15,2022-12-20,2023-02-02,2023-03 |

## 4. Tregue commerciali USA-Cina — riferimento `CNY=X`

tema `regulatory`, almeno uno di `china_trade`, `negotiation_track`, `tariff_escalation`, `trade_war`. Menzioni: 18 in 8 giorni. Già dichiarati: 0, esclusi: 0, da rivedere: **19**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-08-18 | guidance_pivot, hawkish, legal_uncertainty, nafta_usmca, tariff_escalation | `card:2026-09-08/news_05.md` | - ^GSPTSE (indice azionario canadese S&P/TSX Composite) — l'asset più direttamente esposto, come documentato dall'estensione dell'universo del 2026-08-18. |
| 2025-07-07 | asean, border_dispute, emerging_markets, tariff_escalation | `card:2026-09-13/news_04.md` | 2025-07-07 neg tariff_escalation Lettera che conferma dazi al 36% alla Thailandia dal 1° agosto: dazio settoriale/per-paese annunciato formalmente — il precedente più vic |
| 2025-04-30 | negotiation_track, tariff_escalation | `card:2026-08-22/news_01.md` | 2025-04-30 pos negotiation_track Deroghe al settore auto: de-escalation selettiva, il modello di come questa amministrazione arretra senza dichiararlo. |
| 2025-04-04 | ai_export_controls, auction, china_trade, risk_off, tariff_escalation | `card:2026-09-22/news_02.md` | 2025-04-04 neg tariff_escalation, china_trade Ritorsione cinese al 34%: la seconda gamba dello stesso shock, le peggiori due sedute dal COVID. |
| 2025-04-02 | risk_off, tariff_escalation, tariffs, trade_war | `card:2026-09-22/news_02.md` | 2025-04-02 neg tariff_escalation, risk_off "Liberation Day": dazi reciproci generalizzati, l'episodio di ampiezza massima dell'intero campione — definisce la coda sinistr |
| 2025-02-27 | ai_export_controls, ai_semis, nafta_usmca, sec_232, tariff, tariff_escalation, trade_war | `card:2026-09-22/news_02.md` | 2025-02-27 neg tariff_escalation, trade_war Conferma delle date di entrata in vigore dei dazi su Canada e Messico dopo un rinvio, più un ulteriore 10% sulla Cina: analogo |
| 2025-01-14 | negotiation_track, tariff_escalation | `card:2026-08-22/news_01.md` | 2025-01-14 pos negotiation_track Indiscrezione su un'introduzione graduale dei dazi: sollievo, dollaro in calo. Secondo caso-controllo di escalation attenuata. |
| 2025-01-01 | cny, defense, energy_channel, nafta_usmca, tariff, tariff_escalation, trade_war | `card:2026-09-09/news_04.md` | 2025-01-01 neg tariff, energy_channel, defense, cny Apertura del ciclo 2025 di misure commerciali del regime corrente. |
| 2024-12-15 | china_trade, election_risk, nafta_usmca, tariff_escalation, trade_war | `card:2026-09-13/news_04.md` | 2024-12-15 neg tariff_escalation Fase pre-insediamento, minaccia di dazi al 25% su Canada e Messico: primo prezzamento di un rischio annunciato ma non ancora esercitabile |
| 2019-08-12 | china_trade, cny, commodity_supply_shock, copper, tariff_escalation, trade_war | `card:2026-09-22/news_02.md` | 2019-08-12 neg tariff_escalation, cny, trade_war Fase acuta dell'agosto 2019: nuovi dazi sui 300 miliardi residui, lo yuan supera quota 7 per dollaro e gli Stati Uniti de |
| 2019-05-13 | china_trade, cny, de_escalation, tariff_escalation, trade_war | `card:2026-09-22/news_02.md` | 2019-05-13 neg tariff_escalation, china_trade Ritorsione cinese su 60 miliardi dopo l'innalzamento americano dei dazi dal 10% al 25%: rottura del negoziato di maggio, il  |
| 2019-02-19 | negotiation_track, sec_232, tariff_escalation, trade_war | `card:2026-09-13/news_04.md` | 2019-02-19 neg tariff_escalation, negotiation_track Fase negoziale del 2019 con scadenze tariffarie ravvicinate ed esito incerto. |
| 2018-12-26 | risk_off, tariff_escalation, trade_war | `card:2026-09-08/news_05.md` | 2018-12-26 neg tariff_escalation, risk_off Minimo del selloff di fine 2018, in cui il tema commerciale si somma alla stretta monetaria: episodio di regime estremo. |
| 2018-10-29 | risk_off, tariff_escalation, trade, trade_war | `card:2026-09-22/news_02.md` | 2018-10-29 neg tariff_escalation, risk_off Minaccia verbale di estendere i dazi all'intero import cinese residuo in caso di fallimento del vertice del G20: escalation sol |
| 2018-10-10 | ai_export_controls, china_trade, risk_off, tariff_escalation, trade_war | `card:2026-09-13/news_04.md` | 2018-10-10 neg tariff_escalation, china_trade Forte ribasso azionario dell'ottobre 2018 con la guerra commerciale come driver dichiarato. |
| 2018-09-17 | tariff_escalation | `card:2026-08-22/news_01.md` | 2018-09-17 pos tariff_escalation Annuncio dei dazi su 200 miliardi ma con aliquota inferiore all'attesa: escalation nominale, sollievo effettivo → rimbalzo. Caso-controll |
| 2018-07-02 | canada, china_trade, cny, em_fx, tariff, tariff_escalation, trade_war | `card:2026-09-13/news_04.md` | 2018-07-02 neg tariff_escalation Seduta di avvicinamento all'entrata in vigore: il mercato prezza l'irreversibilità. |
| 2018-06-15 | china_trade, sec_301, tariff_escalation, trade_war | `card:2026-09-22/news_02.md` | 2018-06-15 neg tariff_escalation, china_trade Pubblicazione della lista definitiva dei dazi al 25% con ritorsione cinese immediata e simmetrica: il passaggio da minaccia  |
| 2018-03-22 | china_trade, sec_301, section_301, tariff, tariff_escalation, trade_war | `card:2026-09-22/news_02.md` | 2018-03-22 neg tariff_escalation, sec_301 Trump firma il memorandum della Sezione 301 sui dazi alla Cina (circa 50 miliardi): apertura formale della prima guerra commerci |

## 5. Dati area euro — riferimento `EURUSD=X`

tema `macro_data`, almeno uno di `activity_growth`, `consumer`, `inflation_print`, `labour_market`, `pmi`, obbligatori `eurozone_release`. Menzioni: 17 in 10 giorni. Già dichiarati: 6, esclusi: 7, da rivedere: **24**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-06-11 | activity_growth, ecb, eurozone_release, guidance_pivot, hawkish, inflation_print, japan_release, labour_market, rate_decision, term_premium, us_cpi | `card:2026-09-12/news_03.md` | 2026-06-11 pos us_cpi, inflation_print CPI di maggio 2026: primo passaggio dell'energia nei prezzi al consumo di quest'anno. |
| 2024-04-05 | activity_growth, eurozone_release, inflation_print, labour_market, nfp | `card:2026-10-02/news_03.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --direction neg --direction-reference IEF --before 2026-10-02 → 11 episodi. Il filtro |
| 2024-01-05 | eurozone_release, inflation_print, labour_market, nfp, state_dependence | `card:2026-09-12/news_03.md` | 2024-01-05 pos labour_market, nfp Non-Farm Payrolls (i nuovi posti di lavoro USA esclusa l'agricoltura) di dicembre 2023 sopra le attese. |
| 2023-08-31 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2023-08-31 neg inflation_print, eurozone_release flash di agosto 2023 al 5,3% contro 5,1% atteso → ultimo rialzo BCE di settembre prezzato, prezzo bond giù |
| 2023-06-01 | activity_growth, cny, eurozone_release, inflation_downside, inflation_print, ism, services | `card:2026-09-08/news_03.md` | 2023-06-01 neg cny, activity_growth Delusione della ripresa post-riapertura: il momento in cui il mercato capisce che il rimbalzo del 2023 non arriverà. |
| 2023-01-04 | energy_passthrough, eurozone_release, inflation_print | `card:2026-09-02/news_05.md` | 2023-01-04 neg inflation_print Dato di prezzo di inizio 2023 |
| 2022-12-01 | activity_growth, china, cny, consumer_sentiment, eurozone_release, inflation_print, ism, pmi | `card:2026-09-12/news_03.md` | 2022-12-01 pos inflation_print Prosecuzione del precedente. |
| 2022-10-31 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | - Regime: la fase più simile della research è energy_war_shock (2022-02-24 → 2022-10-31): inflazione trainata dall'energia per una guerra, BCE costretta a stringere mentr |
| 2022-09-30 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-09-30 neg inflation_print, eurozone_release flash di settembre 2022 al 10,0% contro 9,7% atteso, prima volta in doppia cifra → altri rialzi ampi prezzati, prezzo bon |
| 2022-09-29 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --subtheme eurozone_release --match-all --direction neg --direction-reference IEAG.AS |
| 2022-08-31 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-08-31 neg inflation_print, eurozone_release flash di agosto 2022 al 9,1%, sopra le attese, con il gas ai massimi → rialzo da 75 punti base prezzato, prezzo bond giù |
| 2022-07-29 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-07-29 neg inflation_print, eurozone_release flash di luglio 2022 all'8,9% contro 8,6% atteso, dopo il primo rialzo BCE → stretta più lunga prezzata, prezzo bond giù |
| 2022-07-08 | activity_growth, consumer, eurozone_release, inflation_print, labour_market, nfp, state_dependence | `card:2026-10-02/news_03.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --direction neg --direction-reference IEF --before 2026-10-02 → 11 episodi. Il filtro |
| 2022-06-30 | eurozone_release, inflation_print | `card:2026-09-02/news_05.md` | 2022-06-30 neg inflation_print, eurozone_release Flash dell'area euro all'8,6% a giugno 2022 |
| 2022-06-03 | activity_growth, eurozone_release, inflation_print, labour_market, nfp, risk_on | `card:2026-10-02/news_03.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --direction neg --direction-reference IEF --before 2026-10-02 → 11 episodi. Il filtro |
| 2022-05-31 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-05-31 neg inflation_print, eurozone_release flash di maggio 2022 all'8,1% contro 7,7% atteso → il mercato prezza rialzi più ampi a luglio, prezzo bond giù |
| 2022-05-30 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --subtheme eurozone_release --match-all --direction neg --direction-reference IEAG.AS |
| 2022-04-01 | energy_passthrough, eurozone_release, hicp, inflation_print, labour_market, nfp, us_cpi | `card:2026-10-03/news_02.md` | 2022-04-01 neg inflation_print, eurozone_release flash di marzo 2022 al 7,5% contro 6,6% atteso, energia oltre +40% → pressione per la prima stretta BCE, prezzo bond giù |
| 2022-03-30 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | Pool dalla libreria: analogues.py find --theme macro_data --subtheme inflation_print --subtheme eurozone_release --match-all --direction neg --direction-reference IEAG.AS |
| 2022-03-02 | energy_passthrough, eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2022-03-02 neg inflation_print, eurozone_release flash di febbraio 2022 al 5,8% contro 5,6% atteso, pochi giorni dopo l'invasione dell'Ucraina → inflazione energetica e r |
| 2022-02-04 | activity_growth, ecb, eurozone_release, inflation_print, ism, labour_market, nfp, pmi, services | `card:2026-09-07/news_04.md` | 2022-02-04 pos labour_market, nfp Payroll di gennaio 2022 enormemente sopra attese in piena accelerazione del ciclo di rialzi: analogo forte per meccanismo (crescita che  |
| 2021-11-29 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2021-11-29 neg inflation_print, eurozone_release CPI preliminari di Germania e Spagna di novembre 2021 ai massimi da decenni, vigilia della flash al 4,9% → più stretta pr |
| 2021-10-29 | eurozone_release, inflation_print | `card:2026-10-03/news_02.md` | 2021-10-29 neg inflation_print, eurozone_release flash di ottobre 2021 al 4,1% contro 3,7% atteso, trainata dall'energia → il mercato anticipa la fine dei tassi negativi, |
| 2015-09-03 | activity_growth, china, cny, commodity_demand, ecb, eurozone_release, flash_cpi, global_pmi, inflation_print, ism, pboc, pmi | `card:2026-09-09/news_03.md` | 2015-09-03 pos cny, china, commodity_demand, activity_growth Coda della svalutazione dello yuan dell'agosto 2015: la PBOC riprende il controllo del fixing dopo lo shock. |

## 6. Crisi fiscali sovrane UE — riferimento `BTP_BUND_SPREAD`

tema `fiscal_policy`, almeno uno di `fiscal_deadlock`, `sovereign_rating`. Menzioni: 15 in 8 giorni. Già dichiarati: 0, esclusi: 0, da rivedere: **40**.

> I token non hanno geografia: qui ci sono anche bilanci britannici e USA, che non vanno dichiarati su uno spread europeo. Per gli episodi francesi il riferimento giusto è `OAT_BUND_SPREAD`, per quelli italiani `BTP_BUND_SPREAD`.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-08-14 | budget_passage, fiscal_deadlock, fiscal_expansion, term_premium | `card:2026-09-10/news_05.md` | 2026-08-14 neg term_premium, fiscal_expansion Episodio di agosto 2026 nel regime attualmente in corso |
| 2026-05-29 | difesa, fiscal_expansion, sovereign_rating | `card:2026-08-24/news_05.md` | 2026-05-29 neg sovereign_rating Ciclo di revisioni di rating sovrano europee: outlook rivisti . |
| 2026-05-08 | difesa, fiscal_deadlock, fiscal_expansion | `card:2026-08-24/news_05.md` | 2026-05-08 neg fiscal_deadlock Tensione sui conti pubblici europei dentro il ciclo di revisione della spesa. |
| 2026-01-28 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2026-01-28 neg fiscal_deadlock Ripresa del negoziato fiscale europeo nel nuovo anno. |
| 2025-12-02 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2025-12-02 neg fiscal_deadlock Passaggio parlamentare del bilancio francese: voto di fiducia sul deficit . |
| 2025-11-26 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2025-11-26 neg fiscal_deadlock Budget britannico d'autunno: manovra correttiva e reazione dei gilt. |
| 2025-11-21 | fiscal_deadlock, fiscal_expansion | `card:2026-08-24/news_05.md` | 2025-11-21 neg fiscal_deadlock Bilancio francese in commissione: rischio di nuovo stallo . |
| 2025-11-12 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2025-11-12 neg fiscal_deadlock Fase finale del negoziato per la riapertura: rientro dello stallo . |
| 2025-10-06 | fiscal_deadlock | `card:2026-10-08/news_04.md` | 2025-10-06 neg fiscal_deadlock Lecornu si dimette poche ore dopo aver nominato il governo → stallo senza soluzione, spread su |
| 2025-10-01 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2025-10-01 neg fiscal_deadlock Shutdown del governo federale USA : stallo di bilancio con sospensione delle statistiche ufficiali. |
| 2025-09-15 | sovereign_rating | `card:2026-10-08/news_04.md` | 2025-09-15 neg sovereign_rating Prima seduta dopo il declassamento di Fitch ad A+ → costo del debito e premio di rischio su |
| 2025-09-03 | auction, credibility_shock, fiscal_deadlock, term_premium | `card:2026-09-10/news_05.md` | 2025-09-03 neg term_premium, fiscal_deadlock Nuovo massimo dei rendimenti lunghi su timori di sostenibilità fiscale |
| 2025-08-26 | fiscal_consolidation, fiscal_deadlock | `card:2026-10-08/news_04.md` | 2025-08-26 neg fiscal_deadlock, fiscal_consolidation Bayrou chiede la fiducia sul piano da 44 miliardi → rischio di caduta del governo e stop al consolidamento |
| 2025-05-28 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2025-05-28 neg fiscal_deadlock Sentenza sui dazi e implicazioni per il gettito federale: incertezza sulle entrate . |
| 2025-05-20 | auction, sovereign_rating, term_premium | `card:2026-09-10/news_05.md` | 2025-05-20 neg term_premium, sovereign_rating, auction Declassamento del rating USA e asta ventennale mal digerita: premio a termine e credibilità insieme |
| 2025-05-19 | sovereign_rating | `card:2026-08-24/news_05.md` | 2025-05-19 neg sovereign_rating Moody's declassa gli Stati Uniti , ultima delle tre grandi a togliere la tripla A: reazione della parte lunga. |
| 2025-04-04 | credibility_shock, fiscal_deadlock, risk_off, term_premium | `card:2026-09-10/news_05.md` | 2025-04-04 neg term_premium, fiscal_deadlock Selloff della parte lunga in cui i Treasury non hanno funzionato da rifugio: il segnale di stress sovrano |
| 2025-01-21 | fiscal_consolidation, fiscal_deadlock | `card:2026-08-24/news_05.md` | 2025-01-21 neg fiscal_deadlock Negoziato sul bilancio francese sotto Bayrou: stallo persistente . |
| 2024-12-10 | fiscal_consolidation, fiscal_deadlock, sovereign_rating | `card:2026-08-24/news_05.md` | 2024-12-10 neg sovereign_rating Revisione del rating francese nella scia della crisi di governo: downgrade/outlook negativo . |
| 2024-12-04 | budget_passage, fiscal_deadlock | `card:2026-08-24/news_05.md` | 2024-12-04 neg fiscal_deadlock Caduta del governo Barnier sulla legge di bilancio francese : primo governo sfiduciato su un bilancio nella Quinta Repubblica. Il precedent |
| 2024-12-02 | fiscal_deadlock | `card:2026-10-08/news_04.md` | 2024-12-02 neg fiscal_deadlock Barnier forza il bilancio della previdenza col 49.3 e arriva la sfiducia → stallo sul bilancio, spread OAT-Bund su |
| 2024-10-30 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2024-10-30 neg fiscal_deadlock Budget britannico di Reeves: espansione a debito e reazione della curva gilt. |
| 2024-07-03 | election_risk, fiscal_consolidation, fiscal_deadlock | `card:2026-08-24/news_05.md` | 2024-07-03 neg election_risk, fiscal_deadlock Fase acuta delle elezioni legislative francesi: rischio di stallo di bilancio → allargamento OAT-Bund. |
| 2024-06-10 | election_risk, fiscal_deadlock | `card:2026-10-08/news_04.md` | 2024-06-10 neg election_risk, fiscal_deadlock Macron scioglie l'Assemblea dopo le europee → rischio di un governo con spesa non finanziata → premio sul debito francese, a |
| 2023-10-19 | fiscal_deadlock, term_premium, term_premium_shock | `card:2026-09-10/news_05.md` | 2023-10-19 neg term_premium, fiscal_deadlock Il decennale americano tocca il 5% su preoccupazioni di offerta e disfunzione fiscale a Washington |
| 2023-08-02 | sovereign_rating | `card:2026-08-24/news_05.md` | 2023-08-02 neg sovereign_rating Fitch declassa gli Stati Uniti da AAA ad AA+: downgrade di un emittente core, forte reazione della parte lunga. Analogo diretto per strutt |
| 2023-06-05 | budget_passage, fiscal_deadlock | `card:2026-08-24/news_05.md` | 2023-06-05 neg fiscal_deadlock Negoziato europeo sulle nuove regole di bilancio: incertezza sul quadro di consolidamento . |
| 2023-06-03 | fiscal_deadlock | `card:2026-06-10/news_02.md` | - 2023-06-03 — Biden firma il Fiscal Responsibility Act (debt ceiling deal): non un'espansione, ma una risoluzione dell'impasse debt ceiling 2023. Analogo per simmetria : |
| 2022-09-28 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2022-09-28 neg fiscal_deadlock Intervento d'emergenza della Bank of England sui gilt lunghi per fermare la spirale dei fondi LDI: stress di liquidità da causa fiscale . |
| 2022-09-23 | fiscal_deadlock, fiscal_expansion | `card:2026-08-24/news_05.md` | 2022-09-23 neg fiscal_deadlock Mini-budget di Kwarteng nel Regno Unito : tagli fiscali non finanziati → crollo di gilt e sterlina, il caso di scuola di perdita di credibi |
| 2022-05-30 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2022-05-30 neg fiscal_deadlock Stress da inflazione sui conti pubblici europei: misure di sostegno energia a debito . |
| 2021-11-23 | difesa, fiscal_deadlock, fiscal_expansion | `card:2026-08-24/news_05.md` | 2021-11-23 neg fiscal_deadlock Negoziato sul bilancio europeo e patto di stabilità in un contesto di inflazione crescente. |
| 2019-10-01 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2019-10-01 neg fiscal_deadlock Avvio della sessione di bilancio italiana in un contesto di crescita nulla: pressione sullo spread . |
| 2019-01-25 | fiscal_deadlock | `card:2026-08-24/news_05.md` | 2019-01-25 neg fiscal_deadlock Italia in recessione tecnica con manovra appena negoziata con Bruxelles: rischio fiscale periferico . |
| 2018-12-24 | fiscal_deadlock | `kb:Fiscal_Pol_Brazil/Fiscal_Pol_Brazil.md` | 2018-12-24 USA Inizio shutdown (35 giorni) stallo neutro ^GSPC, ^VIX Shutdown dal sab. 22 dic.; reazione dominata dalla Fed, non dal fiscale |
| 2015-09-10 | sovereign_rating | `kb:Fiscal_Pol_Brazil/Fiscal_Pol_Brazil.md` | 2015-09-10 Brasile S&P declassa a junk (BB+) rating BRL giù, azioni giù BRL=X, EWZ Annuncio 9 set. dopo chiusura USA (EWZ −6,6% after‑hours); 10 set. real −1,34%, EWZ −1, |
| 2015-08-11 | sovereign_rating | `kb:Fiscal_Pol_Brazil/Fiscal_Pol_Brazil.md` | 2015-08-11 Brasile Moody’s taglia a un gradino sopra il junk rating BRL giù BRL=X, EWZ Outlook portato a stabile; anticipa il taglio S&P |
| 2013-10-01 | fiscal_deadlock | `kb:Fiscal_Pol_Brazil/Fiscal_Pol_Brazil.md` | 2013-10-01 USA Inizio shutdown (Affordable Care Act) stallo neutro ^GSPC, ^VIX Look‑through; S&P +3,1% sull’intero episodio di 16 giorni |
| 2011-08-08 | sovereign_rating | `kb:Fiscal_Pol_Brazil/Fiscal_Pol_Brazil.md` | 2011-08-08 USA Reazione al declassamento S&P AAA→AA+ rating negativo azionario / rendimenti giù ^GSPC, ^TNX, GC=F Annuncio ven. 5 ago. a mercati chiusi; prima seduta lun. |
| 2011-08-02 | fiscal_deadlock | `kb:Fiscal_Pol_Brazil/Fiscal_Pol_Brazil.md` | 2011-08-02 USA Budget Control Act firmato, tetto del debito alzato sblocco neutro/positivo ^GSPC, ^TNX Sblocco atteso; attenzione subito spostata sul rischio rating |

## 7. Fiducia e consumi USA — riferimento `^FVX`

tema `macro_data`, almeno uno di `conference_board`, `consumer`. Menzioni: 13 in 8 giorni. Già dichiarati: 25, esclusi: 7, da rivedere: **18**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-08-17 | activity_growth, consumer, japan_release, retail_sales | `card:2026-09-08/news_04.md` | 2026-08-17 neutral japan_release, activity_growth Release di attività giapponese del mese scorso: stesso regime, stessa vigilia di riunione. |
| 2026-05-18 | consumer, retail_sales | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2026-05-18 Vendite al dettaglio aprile 2026 +0,2%, minimo 40 mesi retail_sales ribasso ^GDAXI Contaminato : fallout guerra Iran sullo stesso periodo |
| 2026-01-19 | consumer, retail_sales | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2026-01-19 Vendite al dettaglio dic-2025 +0,9%, minimo triennale retail_sales ribasso ^GDAXI Stessa data prezzi case (contaminazione property) |
| 2025-09-15 | consumer, retail_sales | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2025-09-15 Vendite al dettaglio agosto 2025 +3,4%, sotto attese 3,8%, minimo da nov-2024 retail_sales ribasso ^GDAXI Uscita mattina Pechino |
| 2025-08-15 | activity_growth, consumer | `card:2026-09-15/news_05.md` | 2025-08-15 neg activity_growth, consumer Dati di luglio 2025: l'analogo più recente e più vicino per regime. |
| 2025-04-29 | conference_board, consumer, expectations_collapse, inflation_print, labour_market, tariff_escalation | `card:2026-10-03/news_01.md` | 2025-04-29 pos labour_market, consumer JOLTS in calo e crollo delle aspettative Conference Board in piena escalation dei dazi → attese di crescita e tassi più bassi, prez |
| 2025-03-25 | conference_board, consumer | `card:2026-09-30/news_02.md` | 2025-03-25 pos conference_board, consumer Aspettative del Conference Board al minimo da oltre un decennio, sotto la soglia storicamente associata alla recessione (integra |
| 2025-02-25 | conference_board, consumer | `card:2026-09-30/news_02.md` | 2025-02-25 pos conference_board, consumer Fiducia Conference Board con il calo più ampio da agosto 2021, sotto attese: timori su dazi e inflazione → domanda attesa più de |
| 2024-09-14 | consumer, retail_sales | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2024-09-14 Vendite al dettaglio agosto 2024 +2,1% mancano 2,5% retail_sales ribasso ^GDAXI Dato uscito sabato → prima seduta utile lunedì 2024-09-16 |
| 2024-08-15 | activity_growth, consumer, platform_earnings | `card:2026-09-15/news_05.md` | 2024-08-15 neg activity_growth, consumer Dati di luglio 2024: stessa configurazione, produzione che regge e consumo che delude. |
| 2024-07-15 | activity_growth, consumer | `card:2026-09-15/news_05.md` | 2024-07-15 neg activity_growth, consumer Dati del secondo trimestre 2024 con vendite al dettaglio +2,0% contro +3,3% atteso: domanda interna sotto attese, produzione in t |
| 2024-01-19 | consumer, inflation_downside, inflation_print, retail, umich, us_cpi | `card:2026-08-14/news_05.md` | --events 2023-08-01,2023-08-03,2023-08-11,2023-11-14,2023-12-08,2023-12-31,2024-01-05,2024-01-19,2024-02-02,2024-04-01,2024-04-05,2024-04-10,2024-05-31,2024-06-07,2024-07 |
| 2023-08-29 | conference_board, consumer, labour_market | `card:2026-10-03/news_01.md` | 2023-08-29 pos labour_market, consumer JOLTS sotto i 9 milioni e Conference Board in calo: il raffreddamento del lavoro fa prezzare la fine dei rialzi Fed → prezzo Treasu |
| 2023-08-15 | activity_growth, britain_release, china, china_stimulus, cny, consumer, labour_market, pboc, rate_decision | `card:2026-09-15/news_05.md` | 2023-08-15 neg activity_growth, consumer Dati di luglio 2023 deboli su tutta la linea, accompagnati da un taglio a sorpresa dei tassi della banca centrale cinese. |
| 2022-06-28 | conference_board, consumer | `card:2026-09-30/news_02.md` | 2022-06-28 pos conference_board, consumer Fiducia Conference Board in calo e componente aspettative al minimo dal 2013, trainata dall'inflazione: stesso mix di oggi (fami |
| 2022-05-16 | consumer, retail_sales | `kb:Il consumatore cinese, domanda interna, e-commerce e trasmissione ai mercati (2011–2026)/ Il consumatore cinese- domanda interna, e-commerce e trasmissione ai mercati (2011–2026).md` | 2022-05-16 Vendite al dettaglio aprile 2022 −11,1% a/a (lockdown Shanghai), catering −22,7% retail_sales ribasso ^GDAXI, EEM Uscita mattina Pechino → seduta europea stess |
| 2022-04-18 | activity_growth, consumer | `card:2026-09-15/news_05.md` | 2022-04-18 neg activity_growth, consumer Dati di marzo 2022 con vendite al dettaglio in contrazione per i confinamenti: divergenza estrema fra produzione e consumo. |
| 2021-08-16 | activity_growth, consumer | `card:2026-09-15/news_05.md` | 2021-08-16 neg consumer, activity_growth Dati di luglio 2021 nettamente sotto attese: vendite al dettaglio +8,5% contro +11,5% previsto — l'inizio dell'aggiustamento immo |

## 8. ISM / PMI USA — riferimento `^TNX`

tema `macro_data`, almeno uno di `ism`, `pmi`. Menzioni: 10 in 6 giorni. Già dichiarati: 3, esclusi: 1, da rivedere: **23**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-07-24 | activity_growth, china_inflation, cny, commodity_demand, cpi, energy_passthrough, eurozone_release, inflation_print, pmi | `card:2026-09-12/news_03.md` | 2026-07-24 pos inflation_print, activity_growth Dati estivi 2026 con inflazione in risalita per la componente energetica. |
| 2025-08-21 | activity_growth, china_consumption, cny, eurozone_release, inflation_print, pmi | `card:2026-09-12/news_03.md` | 2025-08-21 pos activity_growth, inflation_print Dati di attività di agosto 2025. |
| 2025-03-03 | activity_growth, china_gdp, china_inflation, cny, eurozone_release, inflation_print, ism, pmi, tariff_escalation, us_cpi | `card:2026-09-12/news_03.md` | 2025-03-03 pos activity_growth, ism Indagine ISM (Institute for Supply Management — il sondaggio mensile sui responsabili acquisti) manifatturiera con componente prezzi i |
| 2024-12-06 | activity_growth, boe, britain_release, china, cpi_downside, election_risk, inflation_print, ism, labour_market, nfp, us_cpi | `card:2026-09-12/news_03.md` | 2024-12-06 pos labour_market, nfp NFP di novembre 2024. |
| 2024-10-01 | activity_growth, china_gdp, cny, ism, labour_market, military_escalation, pmi | `card:2026-09-09/news_03.md` | 2024-10-01 pos cny, china_gdp, activity_growth Prosecuzione del riprezzamento post-stimolo. |
| 2024-09-23 | activity_growth, eurozone_release, pboc, pmi | `card:2026-09-07/news_03.md` | 2024-09-23 neg pmi, activity_growth, eurozone_release Indicatori anticipatori europei in rallentamento, con la componente tedesca la più debole del blocco : l'analogo più |
| 2024-08-22 | activity_growth, cny, energy_supply_shock, eurozone_release, inflation_print, pboc, pmi | `card:2026-09-12/news_03.md` | 2024-08-22 pos activity_growth, inflation_print Revisioni e dati di attività di fine estate 2024. |
| 2024-08-01 | activity_growth, boj, boj_normalization, china_gdp, cny, commodity_demand, global_pmi, ism, japan_release, labour_market, nfp, pmi, yen | `card:2026-10-03/news_01.md` | 2024-08-01 pos labour_market, ism sussidi di disoccupazione in salita e occupazione ISM manifatturiera in contrazione alla vigilia del payroll di agosto 2024 → tagli più  |
| 2024-06-07 | activity_growth, ism, labour_market, services | `card:2026-08-19/news_06.md` | --events 2015-09-03,2015-12-01,2018-02-02,2019-08-01,2019-09-04,2019-10-01,2022-02-04,2022-08-03,2022-10-13,2022-11-01,2022-12-01,2023-02-03,2023-06-01,2023-07-12,2023-08 |
| 2024-04-01 | activity_growth, ism, japan_release, labour_market, nfp, pmi, tankan | `card:2026-09-08/news_04.md` | 2024-04-01 neutral japan_release, activity_growth Indagine Tankan sul clima di fiducia delle imprese giapponesi: la release trimestrale più seguita del calendario nipponi |
| 2023-08-03 | activity_growth, global_pmi, ism, pmi, services | `card:2026-09-02/news_04.md` | 2023-08-03 neg ism, pmi Indagine sotto le attese nell'estate del selloff da premio a termine |
| 2023-06-23 | activity_growth, cny, commodity_energy_oil, eurozone_release, inflation_print, pboc, pmi | `card:2026-09-12/news_03.md` | 2023-06-23 pos inflation_print, activity_growth Metà 2023, fase di "higher for longer". |
| 2023-02-03 | activity_growth, ism, labour_market, nfp, pmi | `card:2026-09-07/news_04.md` | 2023-02-03 pos labour_market, nfp Payroll di gennaio 2023 a 517.000, la sorpresa al rialzo più grande del campione : cancella il "pivot trade" di inizio anno, rendimenti  |
| 2022-12-01 | activity_growth, china, cny, consumer_sentiment, eurozone_release, inflation_print, ism, pmi | `card:2026-09-12/news_03.md` | 2022-12-01 pos inflation_print Prosecuzione del precedente. |
| 2022-11-01 | activity_growth, china, china_consumption, china_gdp, cny, consumer_sentiment, ism, pmi | `card:2026-09-09/news_03.md` | 2022-11-01 pos china_consumption, cny, china_gdp, consumer_sentiment Dati cinesi in regime di restrizioni sanitarie: consumo debole, cambio sotto pressione. |
| 2022-08-03 | activity_growth, cny, energy_passthrough, global_pmi, ism, pmi, services | `card:2026-09-08/news_03.md` | 2022-08-03 neg cny, activity_growth Delusione dell'attività cinese nella fase delle chiusure sanitarie. |
| 2022-02-04 | activity_growth, ecb, eurozone_release, inflation_print, ism, labour_market, nfp, pmi, services | `card:2026-09-07/news_04.md` | 2022-02-04 pos labour_market, nfp Payroll di gennaio 2022 enormemente sopra attese in piena accelerazione del ciclo di rialzi: analogo forte per meccanismo (crescita che  |
| 2019-10-01 | activity_growth, ism, pmi | `card:2026-09-19/news_04.md` | 2019-10-01 pos activity_growth ISM manifatturiero a 47,8, minimo dal 2009: sorpresa molto negativa che innescò un forte calo azionario. |
| 2019-09-04 | activity_growth, china_gdp, china_stimulus, cny, global_pmi, ism, pmi, usa | `card:2026-09-09/news_03.md` | 2019-09-04 pos cny, activity_growth, china_gdp, china_stimulus Giornata di dati/stimolo cinesi con il cambio come canale dichiarato. |
| 2019-08-01 | activity_growth, china_oil_demand, cny, commodity_demand, guidance_pivot, ism, labour_market, nfp, pmi, tariff_escalation | `card:2026-09-09/news_03.md` | 2019-08-01 pos cny, china_oil_demand, commodity_demand Nuovi dazi americani annunciati: lo yuan rompe la soglia psicologica di 7 nei giorni successivi. |
| 2018-02-02 | activity_growth, inflation_print, ism, labour_market, nfp, nfp_surprise, pmi, services | `card:2026-09-07/news_04.md` | 2018-02-02 pos labour_market, nfp Payroll di gennaio con salari orari in accelerazione a +2,9% annuo: sorpresa di crescita che riprezza i tassi al rialzo e innesca il cro |
| 2015-12-01 | activity_growth, ism, pmi | `card:2026-09-19/news_04.md` | 2015-12-01 pos activity_growth Indice ISM manifatturiero sotto la soglia dei 50 punti (che separa espansione e contrazione) per la prima volta in tre anni, alla vigilia d |
| 2015-09-03 | activity_growth, china, cny, commodity_demand, ecb, eurozone_release, flash_cpi, global_pmi, inflation_print, ism, pboc, pmi | `card:2026-09-09/news_03.md` | 2015-09-03 pos cny, china, commodity_demand, activity_growth Coda della svalutazione dello yuan dell'agosto 2015: la PBOC riprende il controllo del fixing dopo lo shock. |

## 9. Dati macro cinesi — riferimento `CNY=X`

tema `macro_data`, almeno uno di `activity_growth`, `china`, `inflation_print`, obbligatori `china`. Menzioni: 10 in 7 giorni. Già dichiarati: 6, esclusi: 0, da rivedere: **20**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-01-14 | activity_growth, china | `card:2026-08-13/news_01.md` | --events 2024-10-01,2024-10-04,2024-10-21,2024-11-07,2024-12-06,2024-12-09,2024-12-11,2024-12-31,2025-01-10,2025-02-09,2025-03-03,2025-03-07,2025-05-07,2025-05-12,2025-05 |
| 2025-10-30 | administrative_retaliation, china, negotiation_track, tariff_escalation | `card:2026-08-21/news_04.md` | Potatura : nessuna. Gli episodi non elencati nel blocco ( 2023-07-12 , 2023-12-08 , 2024-08-01 , 2024-10-01 , 2025-02-09 , 2025-03-03 , 2025-04-04 , 2025-04-08 , 2025-05- |
| 2025-07-30 | china, politburo, tariff_escalation | `card:2026-08-13/news_01.md` | --events 2024-10-01,2024-10-04,2024-10-21,2024-11-07,2024-12-06,2024-12-09,2024-12-11,2024-12-31,2025-01-10,2025-02-09,2025-03-03,2025-03-07,2025-05-07,2025-05-12,2025-05 |
| 2025-05-12 | china, negotiation_track, tariff_escalation | `card:2026-08-21/news_04.md` | Potatura : nessuna. Gli episodi non elencati nel blocco ( 2023-07-12 , 2023-12-08 , 2024-08-01 , 2024-10-01 , 2025-02-09 , 2025-03-03 , 2025-04-04 , 2025-04-08 , 2025-05- |
| 2025-05-07 | activity_growth, china, china_inflation, china_stimulus, cny, deflation_risk, dovish_repricing, pboc | `card:2026-09-09/news_03.md` | 2025-05-07 pos china_inflation, cny, deflation_risk, dovish_repricing Dato deflattivo con riprezzamento in senso accomodante delle attese sulla PBOC. |
| 2024-12-09 | china, china_stimulus, politburo | `card:2026-08-13/news_01.md` | --events 2024-10-01,2024-10-04,2024-10-21,2024-11-07,2024-12-06,2024-12-09,2024-12-11,2024-12-31,2025-01-10,2025-02-09,2025-03-03,2025-03-07,2025-05-07,2025-05-12,2025-05 |
| 2024-12-06 | activity_growth, boe, britain_release, china, cpi_downside, election_risk, inflation_print, ism, labour_market, nfp, us_cpi | `card:2026-09-12/news_03.md` | 2024-12-06 pos labour_market, nfp NFP di novembre 2024. |
| 2024-09-26 | china, china_stimulus, politburo | `card:2026-08-04/news_03.md` | --events 2024-09-06,2024-09-24,2024-09-26,2024-10-01,2024-10-21,2024-11-07,2024-12-06,2024-12-09,2024-12-11,2024-12-31,2025-01-10,2025-02-09,2025-03-03,2025-03-07,2025-04 |
| 2024-09-24 | activity_growth, balance_sheet, capital_controls, china, china_stimulus, cny, pboc | `card:2026-09-09/news_03.md` | 2024-09-24 pos china_stimulus, cny, balance_sheet, capital_controls Il grande pacchetto di stimolo della PBOC : tagli coordinati di riserva obbligatoria e tassi con soste |
| 2024-07-30 | china, politburo | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2024-07-30 Politburo luglio: enfasi su consumi ma pochi dettagli readout Politburo deludente → EM giù EEM, ^NDX Citi: nessun major shift; sentiment negativo |
| 2024-05-17 | china, china_stimulus, property_wealth | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2024-05-17 Pacchetto "storico" property: 300 mld yuan relending SOE per invenduto, abolito floor mutui, giù acconti stimolo property coordinato easing property → HG=F, EE |
| 2024-02-20 | china, property_wealth, rate_decision | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2024-02-20 Taglio record LPR 5y (-25bp a 3.95%), 1y invariata taglio tassi easing mirato property → HG=F su HG=F, EEM Primo taglio 5y da giu 2023, il più grande dal 2019 |
| 2024-01-24 | china, china_stimulus, pboc | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2024-01-24 PBOC annuncia taglio RRR -50bp (dal 5 feb), ~1 trilione yuan liquidità stimolo monetario easing → risk-on EEM, HG=F Annuncio anticipato inusuale, in mezzo a ro |
| 2023-09-25 | china, credit_stress, property_wealth | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2023-09-25/26 Evergrande manca pagamento, sospende emissione note; indagine su Hengda crisi immobiliare risk-off → EM giù EEM, HG=F Azioni Evergrande -22% poi -7%; Hang S |
| 2023-08-30 | china, credit_stress, property_wealth | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2023-08-30 Country Garden riporta perdita netta H1 ~45 mld yuan crisi immobiliare risk-off property → HG=F giù HG=F, EEM Deterioramento del "better child" del settore |
| 2022-12-07 | china, confidence_rebound | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2022-12-07 "10 misure" National Health Commission: smantellamento zero-COVID pivot politico/riapertura riapertura → risk-on EM, HG=F su EEM, HG=F, EWZ Pivot improvviso po |
| 2022-12-01 | activity_growth, china, cny, consumer_sentiment, eurozone_release, inflation_print, ism, pmi | `card:2026-09-12/news_03.md` | 2022-12-01 pos inflation_print Prosecuzione del precedente. |
| 2022-11-01 | activity_growth, china, china_consumption, china_gdp, cny, consumer_sentiment, ism, pmi | `card:2026-09-09/news_03.md` | 2022-11-01 pos china_consumption, cny, china_gdp, consumer_sentiment Dati cinesi in regime di restrizioni sanitarie: consumo debole, cambio sotto pressione. |
| 2022-01-20 | china, china_stimulus, rate_decision | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2022-01-20 Taglio LPR 1y (-10bp) e 5y (-5bp) taglio tassi LPR easing → risk-on EM EEM, HG=F Serie di easing per property e crescita |
| 2015-09-03 | activity_growth, china, cny, commodity_demand, ecb, eurozone_release, flash_cpi, global_pmi, inflation_print, ism, pboc, pmi | `card:2026-09-09/news_03.md` | 2015-09-03 pos cny, china, commodity_demand, activity_growth Coda della svalutazione dello yuan dell'agosto 2015: la PBOC riprende il controllo del fixing dopo lo shock. |

## 10. Elezioni (Brasile) — riferimento `EWZ`

tema `geopolitical`, almeno uno di `election_risk`. Menzioni: 8 in 5 giorni. Già dichiarati: 3, esclusi: 0, da rivedere: **20**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-06-18 | britain_release, election_risk, gbp, hormuz, iran, military_escalation, sanctions | `card:2026-09-13/news_03.md` | 2026-06-18 neg election_risk, britain_release By-election di Makerfield e dimissioni di Starmer: incertezza sulla leadership , il canale più vicino allo scenario «parlame |
| 2026-05-07 | britain_release, election_risk, gbp | `card:2026-09-13/news_03.md` | 2026-05-07 neg election_risk, britain_release Elezioni locali britanniche con pressione sulla leadership Starmer: gilt decennale ai massimi dal 2008. |
| 2025-12-18 | boe, election_risk, gbp, taiwan | `card:2026-08-15/news_01.md` | --events 2025-11-10,2025-12-08,2025-12-18,2026-02-01,2026-02-17,2026-02-27,2026-02-28,2026-03-01,2026-03-02,2026-03-03,2026-03-04,2026-03-08,2026-03-11,2026-03-12,2026-03 |
| 2025-12-12 | election_risk, thailand | `kb:ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026).md` | 2025-12-12 Fighting Thailandia-Cambogia riesplode; scioglimento parlamento thailandese disputa confinaria + instabilità ambiguo THB, THD SET +0,37/+0,8% (modalità elezion |
| 2024-12-15 | election_risk, semis, tariff, tariff_escalation, tariffs | `card:2026-08-26/news_05.md` | 2024-12-15 pos tariff_escalation (episodio ereditato dalla libreria con etichette date-locali; contenuto non ricostruito in questa sessione — resta nel campione, vedi cav |
| 2024-08-01 | boe, election_risk, gbp | `card:2026-07-20/news_02.md` | - 2024-08-01 — post-election settling (secondo mese Labour). |
| 2024-07-04 | britain_release, election_risk, gbp | `card:2026-09-13/news_03.md` | 2024-07-04 neutral election_risk, britain_release Landslide laburista nel Regno Unito: ampiamente atteso dai sondaggi → reazione contenuta. Il contro-esempio metodologico |
| 2024-02-14 | election_risk, indonesia | `kb:ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026).md` | 2024-02-14 Elezione presidenziale Indonesia (voto), Prabowo vince al 1° turno elezione a rischio pos. equity IND / neutro IDR IDR, EIDO Quick count ~60%; JCI +1,3% il 15/ |
| 2024-01-19 | election_risk, taiwan | `card:2026-07-28/news_04.md` | --events 2023-06-23,2024-01-19,2024-01-22,2024-02-23,2024-03-12,2024-03-13,2024-04-02,2024-08-22,2024-08-26,2024-08-28,2024-09-12,2024-09-18,2024-12-16,2025-01-10,2025-01 |
| 2022-10-31 | black_sea, election_risk, military_escalation, supply_disruption | `card:2026-10-14/news_02.md` | Pool dalla libreria: analogues.py find --theme geopolitical --subtheme black_sea --direction pos --direction-reference ZW=F --before 2026-10-14 → 7 episodi , tutti tenuti |
| 2022-06-20 | election_risk | `card:2026-08-15/news_05.md` | --events 2018-01-01,2018-07-02,2018-10-10,2018-10-29,2018-12-26,2019-05-13,2019-08-12,2019-10-28,2021-06-07,2021-12-19,2021-12-20,2021-12-31,2022-01-01,2022-06-20,2022-10 |
| 2021-12-19 | election_risk | `card:2026-09-13/news_03.md` | 2021-12-19 neg election_risk Vittoria netta di Boric in Cile: il lunedì successivo il peso registra la peggiore perdita giornaliera in un decennio. |
| 2021-06-07 | election_risk | `card:2026-09-13/news_03.md` | 2021-06-07 neg election_risk Vittoria di Castillo in Perù (secondo produttore mondiale di rame) su un programma di prelievo fino al 70% dei profitti minerari: esito non p |
| 2019-12-12 | britain_release, election_risk, gbp | `card:2026-09-13/news_03.md` | 2019-12-12 pos election_risk, britain_release Elezioni britanniche, maggioranza netta di Johnson: exit poll → sterlina +2% a 1,3445, la riduzione dell'incertezza vale più |
| 2018-10-29 | election_risk | `card:2026-09-13/news_03.md` | 2018-10-29 pos election_risk Ballottaggio brasiliano vinto da Bolsonaro: esito pro-mercato dopo un rally pre-elettorale (ETF Brasile +18% in ottobre) → il caso in cui la  |
| 2017-06-08 | election_risk, gbp | `card:2026-07-20/news_02.md` | - 2017-06-08 — May perde la maggioranza assoluta nelle elezioni anticipate (hung parliament). |
| 2016-05-11 | election_risk | `kb:ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026).md` | 2016-05-11 Rally post-elezione Filippine (PSEi +3,09%, peso ai massimi) elezione a rischio pos. equity/PHP PHP, EEM(ctrl) Relief rally su elezione "pacifica e ordinata";  |
| 2016-05-09 | election_risk | `kb:ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026).md` | 2016-05-09 Elezione presidenziale Filippine (voto), vittoria di Duterte elezione a rischio pos. PHP/equity FIL al risultato PHP, EEM(ctrl) Pre-voto: PSEi −5% dal picco ma |
| 2014-07-22 | election_risk | `kb:ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026).md` | 2014-07-22 KPU annuncia ufficialmente la vittoria di Jokowi elezione a rischio pos. IDR/equity IND IDR, EIDO Rimozione dell'incertezza; relief rally |
| 2014-07-09 | election_risk, indonesia | `kb:ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026).md` | 2014-07-09 Elezione presidenziale Indonesia (voto), Jokowi favorito elezione a rischio pos. IDR/equity IND al risultato IDR, EIDO Conteggio ufficiale assente; Prabowo con |

## 11. Difesa / NATO — riferimento `SHLD.L`

tema `geopolitical`, almeno uno di `difesa`, `nato`. Menzioni: 8 in 6 giorni. Già dichiarati: 19, esclusi: 0, da rivedere: **14**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-08-10 | difesa, military_escalation, nato | `card:2026-09-12/news_06.md` | 2026-08-10 pos difesa, military_escalation Escalation sul fronte con risposta in forniture. |
| 2026-08-04 | difesa, nato | `card:2026-09-12/news_06.md` | 2026-08-04 pos difesa, nato Impegni di procurement europeo, estate 2026. |
| 2026-05-26 | difesa, hormuz, infrastructure_attack, iran, military_escalation, nato, sanctions, shipping_chokepoint | `card:2026-09-12/news_06.md` | 2026-05-26 pos difesa, nato Coordinamento NATO su difesa aerea e missilistica. |
| 2026-02-06 | difesa, nato | `card:2026-09-12/news_06.md` | 2026-02-06 pos difesa, nato Impegni europei di difesa nella fase di escalation di inizio 2026. |
| 2025-09-19 | difesa, military_escalation, nato, nato_airspace_breach | `card:2026-09-12/news_06.md` | 2025-09-19 pos nato, military_escalation Violazioni dello spazio aereo NATO e risposta dell'Alleanza. |
| 2025-08-18 | infrastructure_attack, military_escalation, nato, negotiation_track | `card:2026-09-07/news_06.md` | 2025-08-18 neg negotiation_track, military_escalation Stallo del negoziato Russia-Ucraina dopo il vertice: ritorno alle posizioni di partenza — l'analogo più stretto per  |
| 2025-03-18 | difesa, negotiation_track | `card:2026-08-14/news_06.md` | --events 2025-01-01,2025-01-10,2025-01-14,2025-02-12,2025-02-18,2025-02-24,2025-03-04,2025-03-11,2025-03-18,2025-05-16,2025-05-20,2025-06-13,2025-06-23,2025-06-24,2025-06 |
| 2025-02-24 | black_sea, de_escalation, defence, difesa, military_escalation, nato, negotiation_track, russia, sanctions | `card:2026-09-12/news_06.md` | 2025-02-24 pos difesa, nato Terzo anniversario dell'invasione con riposizionamento europeo sulla propria autonomia di difesa. |
| 2022-11-15 | article_4_risk, article_5, military_escalation, nato | `card:2026-09-14/news_02.md` | 2022-11-15 pos nato, article_5, military_escalation Un missile cade a Przewodów, in Polonia: nelle prime ore origine e possibilità di consultazioni alleate erano incerte. |
| 2022-06-03 | difesa, nato, sanctions | `card:2026-09-12/news_06.md` | 2022-06-03 pos difesa, nato Pacchetti di forniture militari e coordinamento NATO nella fase iniziale della guerra. |
| 2022-02-27 | difesa, nato, zeitenwende | `card:2026-09-12/news_06.md` | 2022-02-27 pos difesa, nato La Zeitenwende tedesca: 100 miliardi di fondo speciale per la Bundeswehr annunciati in un fine settimana. |
| 2022-02-21 | military_escalation, nato, risk_off | `card:2026-09-02/news_06.md` | 2022-02-21 neg military_escalation, nato Riconoscimento russo delle repubbliche del Donbass: ultimo passo prima dell'invasione |
| 2014-09-05 | difesa, nato | `card:2026-09-12/news_06.md` | Pool da analogues.py find (tema geopolitical , sotto-temi difesa e nato , direzione pos , no-look-ahead al 2026-09-12). Diagnostica: direzione 'pos' DICHIARATA dalle sche |
| 2014-03-18 | military_escalation, nato, riarmo, sanctions, sovereignty_claim | `card:2026-09-14/news_02.md` | 2014-03-18 pos military_escalation Putin firma il trattato di annessione: il rischio diventa un cambiamento territoriale formale. |

## 12. Lavoro USA — riferimento `IEF`

tema `macro_data`, almeno uno di `labour_market`, `nfp`. Menzioni: 7 in 6 giorni. Già dichiarati: 26, esclusi: 8, da rivedere: **16**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-09-04 | household_spending, labour_market | `kb:Giappone; i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente)/Giappone- i dati macroeconomici come canale distinto dalla politica della Bank of Japan — regime ed episodi storici (2013–presente).md` | 2026-09-04 Spesa famiglie luglio −3,6% a/a (atteso −1,6%), 8° calo di fila, il più profondo da gen 2024 spesa delle famiglie giapponese / household spending ~2 settimane  |
| 2026-06-11 | activity_growth, ecb, eurozone_release, guidance_pivot, hawkish, inflation_print, japan_release, labour_market, rate_decision, term_premium, us_cpi | `card:2026-09-12/news_03.md` | 2026-06-11 pos us_cpi, inflation_print CPI di maggio 2026: primo passaggio dell'energia nei prezzi al consumo di quest'anno. |
| 2026-02-17 | britain_release, labour_market | `kb:Sorprese macro e reaction function dei mercati: fase del ciclo di politica monetaria e ampiezza geografica — Stati Uniti, area euro, Regno Unito (2007–2026)/Sorprese macro e reaction function dei mercati: fase del ciclo di politica monetaria e ampiezza geografica — Stati Uniti, area euro, Regno Unito (2007–2026).md` | 2026-02-17 Retribuzioni UK deboli, disoccupazione 5,2% UK easing_prezzato gilt yields giù IGLT.L, GBPUSD=X Gilt 10Y <4,4% (min da 14-gen); taglio aprile prezzato pieno |
| 2025-11-11 | britain_release, labour_market | `card:2026-09-08/news_06.md` | 2025-11-11 neg britain_release, labour_market Release britannica sul mercato del lavoro, verso neg dichiarato dalla scheda di origine. |
| 2025-03-07 | labour_market | `card:2026-08-14/news_05.md` | --events 2023-08-01,2023-08-03,2023-08-11,2023-11-14,2023-12-08,2023-12-31,2024-01-05,2024-01-19,2024-02-02,2024-04-01,2024-04-05,2024-04-10,2024-05-31,2024-06-07,2024-07 |
| 2024-09-06 | labour_market | `card:2026-08-14/news_05.md` | --events 2023-08-01,2023-08-03,2023-08-11,2023-11-14,2023-12-08,2023-12-31,2024-01-05,2024-01-19,2024-02-02,2024-04-01,2024-04-05,2024-04-10,2024-05-31,2024-06-07,2024-07 |
| 2024-08-05 | japan_release, labour_market, risk_off, yen | `card:2026-09-04/news_06.md` | 2024-08-05 neg japan_release, yen, risk_off Il crollo del Nikkei del 12% nella liquidazione del carry trade: l'episodio estremo del campione. |
| 2024-06-07 | activity_growth, ism, labour_market, services | `card:2026-08-19/news_06.md` | --events 2015-09-03,2015-12-01,2018-02-02,2019-08-01,2019-09-04,2019-10-01,2022-02-04,2022-08-03,2022-10-13,2022-11-01,2022-12-01,2023-02-03,2023-06-01,2023-07-12,2023-08 |
| 2024-06-06 | activity_growth, ecb, eurozone_release, inflation_print, labour_market, rate_decision | `card:2026-09-12/news_03.md` | 2024-06-06 pos labour_market, inflation_print Dati del lavoro di maggio 2024. |
| 2023-08-15 | activity_growth, britain_release, china, china_stimulus, cny, consumer, labour_market, pboc, rate_decision | `card:2026-09-15/news_05.md` | 2023-08-15 neg activity_growth, consumer Dati di luglio 2023 deboli su tutta la linea, accompagnati da un taglio a sorpresa dei tassi della banca centrale cinese. |
| 2023-06-15 | labour_market | `kb:PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/PBOC e politica economica cinese — regime ed episodi storici (2022–2026).md` | 2023-06-15 Taglio MLF 1y (-10bp a 2.65%); disoccupazione giovanile record 20.8% taglio tassi + dato macro easing → EM misto EEM, EWZ Crescente preoccupazione policymaker |
| 2023-06-02 | inflation_print, labour_market | `card:2026-08-05/news_03.md` | Tenuti (29): 2022-02-04 , 2022-06-03 , 2022-07-08 , 2022-08-05 , 2022-10-07 , 2022-12-01 , 2023-02-03 , 2023-06-01 , 2023-06-02 , 2023-07-31 , 2023-08-01 , 2023-12-08 , 2 |
| 2022-10-07 | labour_market | `card:2026-08-05/news_03.md` | Tenuti (29): 2022-02-04 , 2022-06-03 , 2022-07-08 , 2022-08-05 , 2022-10-07 , 2022-12-01 , 2023-02-03 , 2023-06-01 , 2023-06-02 , 2023-07-31 , 2023-08-01 , 2023-12-08 , 2 |
| 2022-08-05 | labour_market | `card:2026-08-05/news_03.md` | Tenuti (29): 2022-02-04 , 2022-06-03 , 2022-07-08 , 2022-08-05 , 2022-10-07 , 2022-12-01 , 2023-02-03 , 2023-06-01 , 2023-06-02 , 2023-07-31 , 2023-08-01 , 2023-12-08 , 2 |
| 2021-05-07 | labour_market, nfp | `card:2026-08-05/news_03.md` | Potato (1), con motivo: 2021-05-07 — il rilascio dei payrolls di aprile 2021, che mancò il consenso di circa 750.000 unità. È l'anomalia statistica più estrema della seri |
| 2018-10-05 | labour_market | `card:2026-07-24/news_04.md` | - 2018-10-05 — NFP forte → sell-off obbligazionario ottobre 2018. |

## 13. BCE: decisioni e discorsi — riferimento `EURUSD=X`

tema `monetary_policy`, almeno uno di `ecb`. Menzioni: 6 in 3 giorni. Già dichiarati: 0, esclusi: 0, da rivedere: **17**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-06-11 | boj, dot_plot, ecb, eurozone_release, guidance_pivot, hawkish, jpy, rate_decision, scotus, term_premium | `card:2026-09-06/news_04.md` | la cui ancora è l'episodio 2026-06-11 (rialzo BCE di giugno 2026, descritto nella KB |
| 2026-04-30 | boj, cb_independence, dot_plot, ecb, forward_guidance, guidance_pivot, hawkish, rate_decision, warsh | `card:2026-10-14/news_04.md` | Pool dalla libreria: analogues.py find --theme monetary_policy --subtheme hawkish --subtheme guidance_pivot --direction pos --direction-reference ^FVX --before 2026-10-14 |
| 2025-06-18 | cb_independence, dot_plot, ecb, guidance_pivot, hawkish, hawkish_hold, rate_decision, tariff_escalation | `card:2026-09-06/news_04.md` | 2018-06-13 e 2024-12-18 sono riunioni FOMC, 2025-06-18 è documentato in KB come |
| 2024-12-18 | boj, cb_divergence, dot_plot, dovish_repricing, ecb, election_risk, eurozone_release, fed, guidance_pivot, hawkish, japan_release, jpy, rate_decision, term_premium, yen | `card:2026-10-14/news_04.md` | 2024-12-18 pos guidance_pivot, hawkish, dot_plot Powell guida a soli due tagli nel 2025: sorpresa hawkish sul percorso → ^FVX al rialzo |
| 2024-07-31 | balance_sheet, boj, boj_hike, carry_trade, carry_trade_unwind, ecb, eurozone_release, fed, fx_intervention, guidance_pivot, hawkish, japan_release, jpy, jpy_carry, rate_decision, tariff_escalation, yen | `card:2026-09-13/news_02.md` | 2024-07-31 pos boj, rate_decision, japan_release Rialzo a 0,25%: il caso da manuale dello smontamento del carry trade — USD/JPY −5% in pochi giorni, Nikkei −19,55%. È l'e |
| 2023-09-14 | ecb, eurozone_release, guidance_pivot, hawkish, projection, rate_decision | `card:2026-09-12/news_04.md` | 2023-09-14 pos rate_decision, ecb, eurozone_release Ultimo rialzo del ciclo BCE. |
| 2023-07-27 | boj, ecb, eurozone_release, fx_intervention, guidance_pivot, hawkish, rate_decision, term_premium | `card:2026-09-06/news_04.md` | 2023-07-27 neg rate_decision, ecb, eurozone_release +25 pb con apertura esplicita a una pausa: il punto in cui la guidance diventa condizionale |
| 2023-06-15 | china_stimulus, dot_plot, ecb, eurozone_release, fed, guidance_pivot, hawkish, pboc, rate_decision | `card:2026-10-14/news_04.md` | Pool dalla libreria: analogues.py find --theme monetary_policy --subtheme hawkish --subtheme guidance_pivot --direction pos --direction-reference ^FVX --before 2026-10-14 |
| 2023-05-04 | ecb, eurozone_release, guidance_pivot, hawkish, rate_decision | `card:2026-09-12/news_04.md` | 2023-05-04 pos rate_decision, ecb, eurozone_release BCE di maggio 2023. |
| 2023-03-16 | ecb, eurozone_release, fed, forward_guidance, guidance_pivot, hawkish, rate_decision | `card:2026-09-06/news_04.md` | 2023-03-16 neg rate_decision, ecb, eurozone_release, hawkish +50 pb nonostante il crollo di Credit Suisse iniziato due giorni prima: archetipo della BCE che resta restrit |
| 2023-02-02 | ecb, eurozone_release, guidance_pivot, hawkish, hawkish_guidance, rate_decision | `card:2026-09-12/news_04.md` | 2023-02-02 pos rate_decision, ecb, eurozone_release Riunioni BCE e BoE ravvicinate in fase di stretta. |
| 2022-12-15 | ecb, eurozone_release, guidance_pivot, hawkish, hawkish_guidance, rate_decision | `card:2026-09-12/news_04.md` | 2022-12-15 pos rate_decision, ecb, eurozone_release BCE del giorno dopo, comunicazione più dura del previsto. |
| 2022-10-27 | ecb, rate_decision | `card:2026-07-25/news_06.md` | --events 2022-09-21,2022-10-27,2022-12-14,2022-12-15,2022-12-20,2023-01-01,\ |
| 2022-09-08 | ecb, eurozone_release, guidance_pivot, hawkish, rate_decision | `card:2026-09-12/news_04.md` | 2022-09-08 pos rate_decision, ecb, eurozone_release Rialzo BCE da 75 punti base. |
| 2022-07-21 | boj, ecb, ecb_supply_shock_pivot, eurozone_release, guidance_pivot, japan_release, jpy, rate_decision, rate_hike, yen | `card:2026-09-13/news_02.md` | 2022-07-21 pos boj, guidance_pivot, jpy, japan_release BoJ ferma con yen in caduta libera: comincia il dibattito pubblico sull'uscita dallo YCC. |
| 2022-06-09 | ecb, guidance_pivot, hawkish, rate_decision, stagflation, yen | `card:2026-08-16/news_04.md` | --events 2014-09-17,2018-03-21,2018-06-13,2018-12-19,2022-02-03,2022-06-09,2022-07-21,2022-08-26,2022-09-08,2022-09-21,2022-12-14,2022-12-15,2022-12-20,2023-02-02,2023-03 |
| 2018-06-13 | balance_sheet, dot_plot, ecb, fed, guidance_pivot, projection, rate_decision | `card:2026-09-06/news_04.md` | 2018-06-13 e 2024-12-18 sono riunioni FOMC, 2025-06-18 è documentato in KB come |

## 14. Aste del Tesoro / term premium — riferimento `IEF`

tema `fiscal_policy`, almeno uno di `auction`, `term_premium`. Menzioni: 6 in 2 giorni. Già dichiarati: 0, esclusi: 0, da rivedere: **15**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-08-18 | fiscal_expansion, supply_shock_duration, term_premium | `card:2026-09-10/news_05.md` | 2026-08-18 neg term_premium, fiscal_expansion Prosecuzione dell'allargamento del premio a termine, stesso regime di oggi |
| 2026-08-14 | budget_passage, fiscal_deadlock, fiscal_expansion, term_premium | `card:2026-09-10/news_05.md` | 2026-08-14 neg term_premium, fiscal_expansion Episodio di agosto 2026 nel regime attualmente in corso |
| 2025-09-03 | auction, credibility_shock, fiscal_deadlock, term_premium | `card:2026-09-10/news_05.md` | 2025-09-03 neg term_premium, fiscal_deadlock Nuovo massimo dei rendimenti lunghi su timori di sostenibilità fiscale |
| 2025-05-20 | auction, sovereign_rating, term_premium | `card:2026-09-10/news_05.md` | 2025-05-20 neg term_premium, sovereign_rating, auction Declassamento del rating USA e asta ventennale mal digerita: premio a termine e credibilità insieme |
| 2025-04-04 | credibility_shock, fiscal_deadlock, risk_off, term_premium | `card:2026-09-10/news_05.md` | 2025-04-04 neg term_premium, fiscal_deadlock Selloff della parte lunga in cui i Treasury non hanno funzionato da rifugio: il segnale di stress sovrano |
| 2024-11-06 | election_risk, fiscal_expansion, rate_expectations_shock, term_premium | `card:2026-09-10/news_05.md` | 2024-11-06 neg term_premium, fiscal_expansion, election_risk Vittoria di Trump: prezzatura immediata di espansione fiscale e dazi → curva più inclinata |
| 2023-10-19 | fiscal_deadlock, term_premium, term_premium_shock | `card:2026-09-10/news_05.md` | 2023-10-19 neg term_premium, fiscal_deadlock Il decennale americano tocca il 5% su preoccupazioni di offerta e disfunzione fiscale a Washington |
| 2022-12-20 | boj, term_premium, term_premium_shock | `card:2026-09-10/news_05.md` | 2022-12-20 neg term_premium, boj La BoJ allarga la banda del controllo della curva: shock globale al premio a termine via rimpatrio di capitali giapponesi |
| 2021-03-11 | fiscal_expansion, term_premium | `card:2026-09-10/news_05.md` | 2021-03-11 neg term_premium, fiscal_expansion Firma dell'American Rescue Plan da 1.900 miliardi: nuova offerta di debito a pieno impiego atteso |
| 2021-02-25 | auction, term_premium, term_premium_shock | `card:2026-09-10/news_05.md` | 2021-02-25 neg term_premium, auction Asta del Treasury a 7 anni con la peggiore coda della storia recente: shock di domanda sulla parte lunga |
| 2018-06-13 | rate_decision, term_premium | `card:2026-09-10/news_05.md` | ( 2003-06-25 , 2014-03-19 , 2018-03-21 , 2018-06-13 ): il verso dichiarato era |
| 2018-03-21 | rate_decision, term_premium | `card:2026-09-10/news_05.md` | ( 2003-06-25 , 2014-03-19 , 2018-03-21 , 2018-06-13 ): il verso dichiarato era |
| 2017-12-22 | fiscal_expansion, term_premium | `card:2026-09-10/news_05.md` | 2017-12-22 neg term_premium, fiscal_expansion Trump firma il TCJA: espansione fiscale non finanziata da 1.500 miliardi in espansione economica → premio a termine |
| 2014-03-19 | guidance_pivot, rate_expectations_shock, term_premium | `card:2026-09-10/news_05.md` | ( 2003-06-25 , 2014-03-19 , 2018-03-21 , 2018-06-13 ): il verso dichiarato era |
| 2003-06-25 | guidance_pivot, term_premium | `card:2026-09-10/news_05.md` | ( 2003-06-25 , 2014-03-19 , 2018-03-21 , 2018-06-13 ): il verso dichiarato era |

## 15. Inflazione giapponese — riferimento `JPY=X`

tema `macro_data`, almeno uno di `inflation_print`, obbligatori `japan_release`. Menzioni: 6 in 4 giorni. Già dichiarati: 5, esclusi: 1, da rivedere: **2**.

| Data | Etichette date-locali | Fonte | Contesto nella fonte |
|---|---|---|---|
| 2026-06-11 | activity_growth, ecb, eurozone_release, guidance_pivot, hawkish, inflation_print, japan_release, labour_market, rate_decision, term_premium, us_cpi | `card:2026-09-12/news_03.md` | 2026-06-11 pos us_cpi, inflation_print CPI di maggio 2026: primo passaggio dell'energia nei prezzi al consumo di quest'anno. |
| 2026-04-30 | boj, hawkish, inflation_print, japan_release, rate_decision | `card:2026-09-08/news_04.md` | 2026-04-30 neutral japan_release Release giapponese della fase corrente. |
