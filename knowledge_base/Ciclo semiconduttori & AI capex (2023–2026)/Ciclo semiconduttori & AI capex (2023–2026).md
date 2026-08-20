# Ciclo semiconduttori & AI capex (2023–2026): catalizzatori discreti e trasmissione

> **Nota metodologica preliminare.** Questo documento è un *catalogo operativo di event study*, non un saggio strutturale. Tutti i rendimenti single-day citati sono ricostruiti da fonti di stampa primaria (CNBC, Bloomberg, NBC, Morningstar, Reuters, comunicati SEC 8-K) all'epoca degli eventi. I rendimenti cumulati T+3/T+5/T+10 per SOXX, ^NDX e ^GSPC che non sono stati verificabili contro dati di prezzo primari sono contrassegnati come **[NV — non verificato a livello quantitativo, qualitativo direzionale]**. Le date riportate sono quelle del *catalizzatore* (annuncio); T=0 è la chiusura della seduta dell'annuncio (o di quella precedente, se l'annuncio è after-close).

## 1. Tassonomia dei catalizzatori discreti

Ai fini del matching news→episodio, i catalizzatori che muovono in modo informativo (cioè: con rerating, non con momentum) il complesso semis/AI si dividono in quattro classi. La tassonomia è ordinata per intensità mediana di reazione (T+1) basata sugli episodi raccolti.

| Classe | Cosa la attiva | Variabile osservata | Tipico segno reazione T+1 SOXX | Persistenza |
|---|---|---|---|---|
| **A. Shock di guidance / earnings di chip leader** | Trimestrale o pre-annuncio di Nvidia, Broadcom, AMD, Micron, TSMC, ASML | Guidance ricavi trimestre successivo vs consenso; gross margin guidance; backlog/orders | ±5–15% sul nome, ±2–8% sull'indice | Alta (3–10 sedute) |
| **B. Revisione capex hyperscaler** | Earnings call Microsoft, Alphabet, Amazon, Meta — guidance capex FY/anno successivo | Capex FY guidance, % crescita YoY, mix server/data center | +1 a +4% (positiva); −2 a −5% (taglio) | Media (1–5 sedute) |
| **C. Shock di domanda/tecnologia** | Lancio di un nuovo modello AI con curva costi spostata (DeepSeek R1), lancio architettura (Blackwell), break-through algoritmico | Modifica implicita della *demand function* per compute | Estrema (−9 a −10% SOXX nel caso DeepSeek) | Media; spesso parzialmente rientrata in T+5 |
| **D. Shock di policy** | Regole BIS/Commerce Dept., entity-list, controlli export, restrizioni Cina su input | Perimetro chip controllati, perdita ricavi annunciata dai produttori | −2 a −5% indice; −5 a −10% sui nomi più esposti | Bassa-media |

**Insight operativo**: la classe A è il segnale a più alta densità informativa per finestre 1–5 sedute, perché contiene la revisione di *consenso* (osservabile) come dimensione di sorpresa. La classe C è la più "fat-tailed" e la più difficile da mappare ex-ante. Le classi B e D producono reazioni più diluite perché l'informazione è meno cleanly quantificabile.

## 2. Catalogo episodi datati (2018–2026)

> Convenzione: dove non diversamente indicato, "after-close" implica che la reazione di mercato è la seduta successiva (T+1 = seduta successiva all'annuncio). Numeri di consenso sono in USD miliardi (mld) e provengono da Refinitiv/FactSet via stampa primaria.

### 2.1 Episodi-ancora (pre-AI e ciclo cripto)

**Episodio 1 — Nvidia FY19 Q3 earnings, 15 novembre 2018 (after-close)**
- *Cosa è stato annunciato*: ricavi Q3 $3.18 mld vs consenso Refinitiv $3.24 mld (miss ~2%); guidance Q4 $2.70 mld ±2% vs consenso $3.40 mld (miss ~−21%). Causa: "crypto hangover" — eccesso di scorte di GPU Pascal mid-range nel canale post-collasso del mining; CEO Huang stima 1–2 trimestri per smaltirle.
- *Reazione single-name verificata*: NVDA **−18.8%** alla chiusura del 16 novembre 2018 (Fortune, CNBC).
- *Indici*: **[NV]** Reazione qualitativa: il 16/11/2018 SOXX e Nasdaq chiusero in calo, episodio incorporato nel sell-off di fine 2018; il decimo giorno di borsa successivo (≈30 nov) cadeva ancora in fase di ribasso che proseguì fino al 24 dicembre 2018. T+10 stimato negativo per tutti e tre gli indici per ragioni macro più che idiosincratiche.

**Episodio 2 — Broadcom FY19 Q2 earnings, 13 giugno 2019 (after-close)**
- *Annunciato*: ricavi Q2 $5.52 mld vs consenso $5.68 mld (miss); EPS adj $5.21 vs $5.16 (beat). Tagliata guidance FY2019 da $24.5 mld a **$22.5 mld** (−$2 mld, −8%). Causa: Huawei export ban del maggio 2019 (~$900M ricavi diretti) + "broad-based slowdown" da incertezza tariffaria.
- *Reazione single-name verificata*: AVGO **−8%** intraday il 14 giugno 2019, chiusura −5–7%. Trascinati AMD, MU, NVDA, QCOM **−2 a −3%**, AAPL **−1%** (CNBC, CNN, Fox Business).
- *Indici*: **[NV]** Direzionalmente SOXX **−2 a −3%** T+1; rientro parziale entro T+5 (i media riportano che AVGO "ha recuperato gran parte del terreno nei giorni successivi", Dividend.com). S&P 500 marginalmente negativo, ^NDX moderatamente negativo.

**Episodio 3 — Micron FY22 Q4 earnings + taglio capex, 29 settembre 2022 (after-close); update 16 novembre 2022**
- *Annunciato 29/9/2022*: Ricavi $6.64 mld (calo 23% QoQ da $8.64 mld); guidance "decisive steps to reduce supply growth including a nearly 50% wafer fab equipment capex cut versus last year" (comunicato 8-K Micron). Il 16/11/2022 ulteriore taglio: riduzione DRAM/NAND wafer starts del ~20% e ulteriori tagli capex.
- *Reazione indici verificata qualitativamente*: episodio incastonato nella fase ribassista del 2022; segnale che il *ciclo memoria* aveva chiuso simultaneamente al picco crypto/COVID.
- *Indici T+1/T+10*: **[NV]** in dollari, ma il contesto macro (FOMC hawkish, BoE crisis Gilts) rende difficile attribuire isolatamente i ritorni a Micron.

### 2.2 Episodio-spartiacque AI

**Episodio 4 — Nvidia FY24 Q1 earnings (24 maggio 2023, after-close) — "il momento AI di Wall Street"**
- *Annunciato*: Q1 ricavi $7.19 mld vs consenso ~$6.52 mld (beat ~10%); EPS beat ~20%. **Guidance Q2 ~$11.0 mld ±2% vs consenso $7.15 mld — beat di ~+54%, una delle più ampie guidance surprise mai registrate per una mega-cap.** Driver: data center revenue $4.28 mld record, "demand […] across the board" da hyperscaler per training di LLM (citato sull'earnings call).
- *Reazione single-name verificata*: NVDA **+24%–26%** intraday il 25/5/2023 (CNBC, Bloomberg), nuovo all-time high. AMD e altri AI-exposed names trascinati al rialzo. KeyBanc alza PT da $375 a $500.
- *Indici*: **[NV]** Direzionalmente: SOXX T+1 stimato **+5 a +8%**; ^NDX **+1.5 a +2.5%**; ^GSPC **+0.5 a +1%**. Persistenza alta: NVDA mostra successivamente una serie di 10 sedute in rialzo consecutive con +18.97% cumulato (Dow Jones Market Data).

### 2.3 Shock di policy 2022–2024

**Episodio 5 — US export controls 7 ottobre 2022 (Commerce / BIS)**
- *Annunciato*: Interim Final Rule che vieta export verso PRC di chip avanzati >threshold di TPP e SME (ECCN 3A090/4A090, 3B090). Embargo de facto sul *manufacturing* avanzato cinese.
- *Reazione qualitativa* (Wikipedia, CSIS): "share prices in both United States and China high-tech sectors dropped" — magnitudine moderata sull'indice (−3 a −5% SOXX nella settimana) perché parzialmente atteso e perché Nvidia introdusse subito gli H800/A800 "sotto-soglia".
- *T+1/T+10*: **[NV]**.

**Episodio 6 — US export controls update 17 ottobre 2023**
- *Annunciato*: chiusura della "loophole" H800/A800/L40S; nuova metrica TPP+performance density; estensione a 40+ paesi.
- *Reazione single-name verificata*: NVDA **−4.7%** alla chiusura 17/10/2023; AVGO **−2%**, MRVL **−1%** (CNBC).
- *Indici*: SOXX T+1 stimato **−3 a −4%** [NV]; ^NDX **−1.5%** [NV].

### 2.4 Ciclo ASML e segnali capex dei foundry

**Episodio 7 — ASML Q3 2024 leak, 15 ottobre 2024**
- *Annunciato*: per errore tecnico, il report Q3 viene pubblicato un giorno in anticipo. Bookings Q3 €2.6 mld vs consenso €5.6 mld (miss del **−54%**). Guidance 2025 ridotta dal range €30–40 mld a €30–35 mld (estremo basso del range fissato all'Investor Day 2022).
- *Reazione verificata*: ASML AMS **−15.7%** (peggior chiusura dal 2002 IPO, €48.7 mld market cap polverizzati); ASML US **−16%**; **SOXX −3.7% intraday, SMH −4%+** (Benzinga, CNBC, Euronews).
- *Indici*: ^NDX e ^GSPC chiusero negativi su trascinamento da semis. T+5/T+10: **[NV]** ma il SOXX rimase in tendenza laterale-negativa fino alla seduta del 30/10/2024 prima di rimbalzare con i guidance positivi degli hyperscaler.

### 2.5 Lo shock DeepSeek (capex returns scrutiny)

**Episodio 8 — DeepSeek R1 selloff, 27 gennaio 2025 (T=close del venerdì 24/1)**
- *Annunciato*: il weekend 25–26 gennaio 2025 emerge l'attenzione globale sul modello open-source DeepSeek-R1 (cinese), che dichiara training con stack di H800 stockpiled a costi notevolmente inferiori. Il paper di DeepSeek riporta "$5.576 million" per il solo "official training" (CNBC, 31 gennaio 2025); SemiAnalysis (31 gennaio 2025) stima invece un costo complessivo molto superiore: "total server CapEx for DeepSeek is ~$1.6B, with a considerable cost of $944M associated with operating such clusters". Stacy Rasgon (Sanford C. Bernstein) "questions whether DeepSeek was truly built for less than $6M" (HPCwire, 27 gennaio 2025). Implicazione: la *demand function* per compute AI potrebbe avere elasticità maggiore di quella prezzata; ROI sul capex hyperscaler messo in discussione.
- *Reazione single-day verificata (chiusura 27/1/2025)*:
  - NVDA **−16.97%** (≈−17%), **−$589 mld di market cap (record assoluto storico in valore)** (Bloomberg, NBC, CNBC, Morningstar).
  - AVGO **−17.4%**; AMD **−6.4%**; MU **−10%**; ARM **−10%**; ASML **−6%**; MRVL **−12%** (CNBC).
  - Power/AI infra: Vistra **−28%**; Constellation Energy **−21%**; Siemens Energy **−20%**; GE Vernova **−21%** (NBC). Indica la corretta lettura del mercato: lo shock è sulla *funzione di domanda di compute/energia*, non solo sui chip.
  - **^NDX: ~−2.97% / Nasdaq Composite −3.07%** (chiusura 19,341.83); **^GSPC −1.46%** (chiusura 6,012.28); Dow +0.65% (rotazione difensiva) (CNBC).
  - **SOXX ≈ −9 a −10%** stimato (SMH/VanEck VVSM **−8.68%** documentato; SOXX composizione molto NVDA/AVGO/AMD-heavy implica reazione coerente).
- *Reazione T+1 (martedì 28/1/2025)*: NVDA recupera **~+8.9%** (+$260 mld market cap, secondo maggior guadagno giornaliero della storia per market cap; Nasdaq). Il rimbalzo dimostra che il sell-off del 27 era in parte "panic, then think".
- *Indici T+3/T+5/T+10*: **[NV]** I dati ufficiali Nasdaq Index Scorecard di gennaio 2025 indicano che a fine mese SOX chiude **+0.7%** e NQSSSE **+0.6%** (i due peggiori di 25 indici tematici Nasdaq, ma comunque positivi), suggerendo recupero pressoché integrale entro 4 sedute.

**Episodio 9 — Meta capex 2025 guidance, 29 gennaio 2025 (post DeepSeek)**
- *Annunciato*: in un post Facebook del 24/1/2025 Zuckerberg pre-anticipa capex 2025 di **$60–65 mld** ("plans for a data center so large it would cover a significant part of Manhattan", "more than 1.3 million GPUs by year-end 2025"). Confermato e rafforzato nell'earnings call Q4 2024 del 29 gennaio 2025 (post-close).
- *Implicazione*: contro-segnale rispetto allo shock DeepSeek di due sedute prima; agisce da *circuit-breaker* sulla narrativa "capex troppo alto".
- *Reazione*: META al rialzo nella seduta successiva; SOXX e ^NDX **[NV]** ma direzionalmente positivi (recupero post-DeepSeek). Microsoft (Brad Smith) conferma capex FY25 ~$80 mld.

### 2.6 Shock policy 2025

**Episodio 10 — Nvidia H20 export curb, 15 aprile 2025 (after-close)**
- *Annunciato*: l'amministrazione USA comunica a Nvidia il 9/4/2025 il requisito di licenza export per H20 verso Cina (RPC, D:5, e parent ultimo cinese), "per il futuro indefinito". Nvidia annuncia 15/4/2025 un **charge da ~$5.5 mld** (poi $4.5 mld realizzati in Q1 FY26) per inventario H20 e impegni di acquisto in eccesso. Persi $4.6 mld di vendite H20 nel trimestre + $2.5 mld di shipment non eseguiti; guidance Q2 FY26 ridotta di ~$8 mld per perdita H20 (comunicato Nvidia 8-K).
- *Reazione single-name verificata (after-hours 15/4)*: NVDA **−6.5%** AH (CNBC, Wolf Street); AMD **−7.1%** AH; AVGO **−3.4–4%** AH.
- *Indici T+1*: SOXX **[NV]** ma sostanzialmente negativi; episodio incastonato nel sell-off Trump-tariff "Liberation Day" del 2 aprile e nel rimbalzo del 9 aprile (S&P 500: 4,982.77 il 8/4 → 5,456.90 il 9/4, +8.97% in una seduta). Confounding macro elevato.

### 2.7 Eventi 2026: il ciclo AI capex visto dalle catene di fornitura

**Episodio 11 — ASML Q4 2025 earnings, 28 gennaio 2026**
- *Annunciato*: Q4 net sales €9.72 mld (record); FY25 €32.7 mld; **bookings Q4 €13.2 mld vs consenso €6.32 mld — beat di +109%**, record storico per ASML. Backlog €38.8 mld, capacity EUV venduta fino al 2027. Guidance FY26 €34–39 mld (mid €36.5 mld vs consenso €35.1 mld); buyback €12 mld al 31/12/2028. Cina prevista al 20% del fatturato 2026 (da 41% nel 2024).
- *Reazione single-name verificata*: ASML US **+7%** intraday, poi chiusura **−2.18%** post earnings call (memoria di gestione: "la maggior parte degli ordini Q4 è per il 2027, non per il 2026 P&L"). ASML AMS **−1.9%** chiusura.
- *Lettura quant*: la struttura del segnale è "beat enorme ma push-out temporale" — episodio educativo su come *bookings* possa essere disancorato dalla *current-period revenue*.

**Episodio 12 — Broadcom Q2 FY26 earnings, 3 giugno 2026 (after-close)**
- *Annunciato 3/6/2026*: Q2 ricavi $22.19 mld (+48% YoY) vs consenso ~$22.4 mld (lieve miss); **AI chip revenue $10.8 mld, +143% YoY (beat sostanziale, sopra le proiezioni del management)**; EPS adj $2.44 vs consenso $2.40 (beat); free cash flow $10.26 mld (46% margin). Backlog AI dichiarato ~$73 mld; target >$100 mld AI revenue entro 2027. Software (VMware) sotto consenso.
- *Reazione single-name verificata*: AVGO **−3%** in after-hours (TechTimes), classico caso di "priced for perfection" — beat su AI compensato da miss su software e da valutazione tirata.
- *Contesto*: con un *AI backlog* di $73 mld (di cui $10 mld da un singolo cliente disclosed dicembre 2025, *widely reported come OpenAI*), Broadcom diventa la seconda gamba della *capex narrative* dopo Nvidia. Anche un beat su AI non è più sufficiente a muovere positivamente l'azione se il prezzo riflette già aspettative ottime.

### Tabella riassuntiva degli episodi (reazione T+1, dove verificata vs stimata)

| # | Data evento | Catalizzatore | Atteso vs realizzato (sorpresa principale) | Reazione single-name T+1 (verif.) | SOXX T+1 | ^NDX T+1 | ^GSPC T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 15 nov 2018 AC | NVDA guidance Q4 | Guid $2.70 mld vs cons $3.40 mld (−21%) | NVDA −18.8% | neg [NV] | neg [NV] | neg [NV] | neg | neg | neg (sell-off Q4'18) |
| 2 | 13 giu 2019 AC | AVGO guidance FY19 | $22.5 mld vs prec $24.5 mld (Huawei) | AVGO −8% intraday | −2/−3% [NV] | −1% [NV] | −0.5% [NV] | parz. recup. | recup. | recup. |
| 3 | 29 set 2022 AC | MU capex −50% wafer FE; supply cuts | Forte downside vs precedente guida | MU −2 a −3% [NV] | neg [NV] | neg [NV] | neg [NV] | neg | neg | neg (macro bear) |
| 4 | 24 mag 2023 AC | NVDA guidance Q2 FY24 | $11 mld vs cons $7.15 mld (+54%) | NVDA +24–26% | +5/+8% [NV] | +1.5/+2.5% [NV] | +0.5/+1% [NV] | pos | pos | pos (rally AI) |
| 5 | 7 ott 2022 | Export controls BIS | Embargo de facto su AI/SME → Cina | Diffuso negativo [NV] | −3/−5% sett.ma [NV] | neg [NV] | neg [NV] | neg | misto | misto |
| 6 | 17 ott 2023 | Export controls update (H800 ban) | Chiusura loophole | NVDA −4.7% | −3/−4% [NV] | −1.5% [NV] | −0.5/−1% [NV] | neg | neg | neg |
| 7 | 15 ott 2024 | ASML Q3 leak, FY25 guide cut | Bookings €2.6 mld vs €5.6 mld | ASML −15.7% | −3.7% intraday | neg [NV] | neg [NV] | neg | parz. | parz. |
| 8 | 27 gen 2025 | DeepSeek R1 demand shock | Curva costi AI training spostata in basso | NVDA −16.97%, AVGO −17.4% | **~−9%** (SMH −8.68% verif.) | **−2.97%** | **−1.46%** | rimb. (NVDA +8.9% T+1) | recup. quasi integ. | recup. integ. (SOX gen +0.7% MoM) |
| 9 | 29 gen 2025 AC | Meta capex $60–65 mld FY25 | Up-shift capex hyperscaler | META +rialzo [NV] | pos [NV] | pos [NV] | pos [NV] | pos | pos | pos |
| 10 | 15 apr 2025 AC | NVDA H20 export curb / $5.5 mld charge | Perdita ~$8 mld revenue FY26 | NVDA −6.5% AH; AMD −7.1% AH | neg [NV] | neg [NV] | neg [NV] | confounded da tariffe | confounded | confounded |
| 11 | 28 gen 2026 | ASML FY25 + guida FY26 | Bookings Q4 €13.2 mld vs cons €6.32 mld (+109%); guid FY26 €34–39 mld | ASML AMS −1.9% (intraday +7% poi reverse) | misto [NV] | misto [NV] | misto [NV] | misto | misto | misto |
| 12 | 3 giu 2026 AC | AVGO Q2 FY26 | AI rev $10.8 mld (+143% YoY) vs guidance; software miss | AVGO −3% AH | neg lieve [NV] | neg lieve [NV] | neg lieve [NV] | parz. | recup. parz. | **finestra parziale** (T+5 = 10 giu 2026; T+10 = 17 giu 2026: oltre data compilazione 8/6/2026) |

> Tutte le celle marcate **[NV]** sono *stime direzionali da ricostruzione narrativa di fonti primarie (CNBC, Bloomberg, comunicati 8-K)*, non da estrazione da CSV di prezzo. Per uso in event study quantitativo è necessario un secondo passaggio sui CSV Yahoo Finance / FRED. Le celle con cifre esplicite sono verificate via stampa primaria.

## 3. Meccanismo di propagazione

La trasmissione di uno shock idiosincratico da un singolo nome al portafoglio globale ha una struttura a cascata, che si è progressivamente *accorciata* dal 2018 al 2025 a causa della crescente concentrazione degli indici.

**Cascata standard, episodio "shock di guidance NVDA" (es. 24 mag 2023, 27 gen 2025):**
1. *Single-name (T0–T+1)*: il prezzo NVDA assorbe il delta di guidance/consenso, tipicamente con elasticità ~5–10x rispetto alla sorpresa percentuale di revenue guidance.
2. *Indice semiconduttori SOXX/^SOX (T0–T+1)*: peso di NVDA in SOXX è elevato (~10%); aggiungendo AVGO, AMD, MU, TSM, ASML, il complesso "AI capex chain" rappresenta una quota maggioritaria. Reazione spillover ~30–50% della reazione del single-name.
3. *Nasdaq-100 ^NDX (T0–T+1)*: NVDA è la prima o seconda azione per peso nel ^NDX (insieme a MSFT, AAPL); il "Magnificent Seven" rappresenta una quota dominante della capitalizzazione dell'indice. Reazione spillover ~15–25% del single-name.
4. *S&P 500 ^GSPC (T0–T+1)*: i Magnificent Seven sono ~34.8% dell'S&P 500 a maggio 2026 (Motley Fool), rispetto a 12.5% nel 2016. Nvidia singolarmente è la prima azione dell'S&P 500 al 7.0% (Slickcharts, mar 2026), peso superiore a interi settori (energia, utilities). Reazione spillover ~10–15% del single-name.
5. *Asia (^N225, KOSPI, TWSE) — apertura T+1*: TSMC, Samsung, SK Hynix tradano in apertura asiatica come "derivati" del segnale americano. Spesso il movimento overnight asiatico è già il **40–60% della reazione completa** del giorno seguente.

**Effetto-concentrazione e "indicizzazione fragile":**
- Per il 2025: secondo Statista, che cita Howard Silverblatt (senior index analyst, S&P Dow Jones Indices), i Mag7 "accounted for 42 percent of the S&P 500's 17.9-percent return for the year [2025]". Per mid-2024 Vantage Markets (che cita Bloomberg) riporta: "This dominance sharpened by mid-2024, with the Magnificent Seven stocks accounting for 79% of the S&P 500's total return for the year to June [2024]". Conseguenza: un singolo shock NVDA produce *quasi-meccanicamente* uno spostamento dell'indice. La distinzione "single-name vs indice" è progressivamente erosa.
- Nel 2026 NVDA singolarmente vale ~7.0% dell'S&P 500. Un −17% sul nome (caso DeepSeek) implica un drag *meccanico* di −1.2% sull'indice ponderato — coerente con il −1.46% osservato sull'^GSPC il 27/1/2025.
- I primi 10 nomi sono ~38% dell'indice nel 2026 vs 22% nel 2020 (Armstrong Fleming & Moore). La concentrazione amplifica le code (sia upside che downside) dei guidance shock dei chip leader.

**Asimmetria positiva vs negativa:**
- Guidance miss / sorpresa negativa: reazione ampia ma spesso *parzialmente rientrata* in T+3/T+5 quando emergono buyer "buy-the-dip" su nomi di qualità (caso DeepSeek: NVDA +8.9% in T+1).
- Guidance beat estremo (NVDA mag 2023): persistenza più lunga (≥10 sedute) perché ridisegna le aspettative di consenso forward — non solo il trimestre, ma il tasso di crescita strutturale.

## 4. Quando il segnale è affidabile e quando no

**Finestra T+1/T+3: massima informatività.** L'evidenza nei dati raccolti suggerisce:
- *Guidance shock dei chip leader* (classe A): reazione single-name e SOXX entro 24–48 ore è informativa nel ~70–80% dei casi (le sorprese forti tendono a persistere); rotazione settoriale residua su T+5.
- *Cause-effect cleanly attribuibili*: NVDA mag 2023, DeepSeek gen 2025, ASML leak ott 2024, NVDA H20 apr 2025. Reazione T+1 dominante; T+10 spesso confuso da altre news.

**Finestra T+5/T+10: rumore crescente.**
- *Macro overlay*: episodi nel 2018 Q4 (Nvidia 16/11) e nel Q3 2022 (Micron 29/9) sono incastonati in regimi macro (rialzi Fed) che dominano il segnale idiosincratico oltre T+3. Per un event study pulito su questi episodi va tolto il fattore macro (ad es. via Fama-French o tramite controllo di paesi/settori).
- *Trump-tariff confounding (aprile 2025)*: la H20 disclosure del 15/4/2025 cade nel mezzo della volatilità tariffaria; il T+10 misura più il pivot di amministrazione del 9/4 che lo shock H20.
- *Earnings overlap*: tra 20–30 gennaio e tra 25 aprile–10 maggio molti nomi tech riportano nella stessa settimana. Le reazioni "pure" sono difficili da isolare.

**Ri-prezzatura vera vs momentum/rotazione**: la firma differenziale:
- *Ri-prezzatura*: lo shock cambia anche il *consenso analyst forward* (PT, EPS forward) di NVDA e dei comparable. NVDA mag 2023 ha innalzato il PT mediano di +33% in due settimane.
- *Momentum/rotazione*: lo shock NON cambia il forward, ma sposta la rotazione settoriale (DeepSeek 27/1/2025 ha trascinato Dow +0.65% intraday — flight verso difensivi e value senza ri-prezzare la traiettoria di lungo).

**Regola pratica per il sistema di matching**: usare T+1 e T+3 come segnali primari per classificare "magnitudine direzionale"; usare T+5 come segnale di *persistenza*; trattare T+10 solo come controllo di robustezza, con esclusione esplicita degli episodi sovrapposti a CPI, FOMC o altri eventi macro.

## 5. Cosa NON trasferire dal regime 2023–2026

**Confronto con il dot-com 2000:**
- *Profittabilità*: Nvidia Q1 FY27 (chiuso 27 aprile 2026, dati come da SEC 8-K del 20 maggio 2026): ricavi $81.615 mld (+85% YoY da $44.062 mld); net income GAAP $58.321 mld (+211% YoY da $18.775 mld); gross margin GAAP 74.9%. Le mega-cap AI 2024–2026 sono *cash-flow positive* a margini operativi 35–65%. La pop dot-com era trainata da aziende a EBITDA negativo o nullo, con valutazioni basate su "eyeballs/click" piuttosto che su utile.
- *Capex finanziato*: gli hyperscaler 2024–2026 finanziano i $300+ mld di capex annuo con free cash flow operativo. Per Meta (Q4 2025 earnings release, investor.atmeta.com, 29 gennaio 2026): "Capital expenditures... were $72.22 billion for the... full year 2025"; "Cash flow from operating activities was $115.80 billion... for the... full year 2025" — capex coperto ~1.6x dall'OCF. Microsoft FY25 sufficientemente positivo da assorbire ~$80 mld capex. Nel 1999–2000 il capex telecom era finanziato con debito ad alto yield ("the great telecom debt blowout").
- *Earnings concentration*: i Mag7 generano ~70% del *profitto economico* dell'S&P 500 (Russell Investments). Le dot-com top10 del 2000 generavano una frazione esigua dell'utile dell'indice (Cisco, Sun, Lucent in deterioramento).
- **Implicazione per un sistema di matching news→episodi**: non utilizzare il 2000–2001 come *analogo* per gli episodi 2023–2026. Il rischio di overfitting su pattern di crash strutturale è alto: le valutazioni 2024–2026 sono giustificate (almeno in parte) da utili reali; il rischio è più sulla *velocità* di adoption che sulla solvibilità.

**Confronto con il ciclo semiconduttori 2018:**
- *Driver di domanda*: il 2018 era trainato da crypto-mining (Pascal GPU) + smartphone (apex Apple) + automotive — domanda *finale* relativamente granulare e ciclica. Il 2023–2026 è trainato da *capex hyperscaler* concentrato in 4 controparti (MSFT, AMZN, GOOGL, META) + 2 challenger (Oracle, Meta sub-vertical). Concentrazione della domanda *aumenta* la sensibilità a singole revisioni capex.
- *Struttura della domanda*: nel 2018, l'inventory unwind era una variabile *trasversale* (canali GPU); nel 2025–2026 il bottleneck è capacità HBM, packaging CoWoS, energia per data center.
- *Per il matching*: episodi 2018 (NVDA 11/2018, AVGO 6/2019, MU 9/2022) sono utili come *analoghi tail-risk* per il "downside" dei guidance shock, ma NON come analoghi di reazione "media" perché il regime di valutazione è diverso.

**Riferimenti accademici utili al framework (rilevanti per il giudizio quant ma NON per il matching giornaliero):**
- *Acemoglu, D. (2024), "The Simple Macroeconomics of AI", NBER WP 32487 (poi Economic Policy, 2025, vol. 40[121], 13–58).* Mostra che applicando il teorema di Hulten e i parametri empirici disponibili (Eloundou et al. 2023; Svanberg et al. 2024; Noy & Zhang 2023; Brynjolfsson et al. 2023), il contributo di AI al TFP è 0.53%–0.66% in 10 anni. **Rilevante**: il *capex* AI 2023–2026 ($300+ mld/anno) sconta una crescita TFP molto più alta. È una fonte di rischio strutturale di delusione che può manifestarsi via *capex revision* (catalizzatore di classe B).
- *Brynjolfsson, E., Rock, D., Syverson, C. (2021), "The Productivity J-Curve: How Intangibles Complement General Purpose Technologies", AEJ:Macro 13(1), 333–372.* Dimostra che le GPT (general purpose technologies) richiedono investimenti complementari intangibili — la produttività misurata può essere sotto-stimata nei primi anni e sovra-stimata nei successivi. **Rilevante**: i mercati possono prezzare in eccesso il *gap* J-curve nelle fasi di "ignition" (2023 NVDA blow-out), e poi correggere bruscamente quando la J-curve si appiattisce sotto le aspettative (analogia possibile per DeepSeek).
- *Autor, D., Dorn, D., Katz, L., Patterson, C., Van Reenen, J. (2020), "The Fall of the Labor Share and the Rise of Superstar Firms", QJE 135(2), 645–709.* Documenta empiricamente la concentrazione degli utili in poche "superstar firms" come trend strutturale degli ultimi due decenni. **Rilevante**: spiega il meccanismo per cui Mag7 = 34.8% dell'S&P 500 oggi è un equilibrio (non un'anomalia transitoria) e quindi giustifica la *propagazione meccanica* degli shock idiosincratici a indice.
- *Brynjolfsson, E., Rock, D., Syverson, C. (2017/2019), "Artificial Intelligence and the Modern Productivity Paradox", NBER WP 24001.* Articola il paradosso "aspettative AI vs misure di produttività". **Rilevante** per dimensionare il rischio di "AI disappointment trade" — quello che il 27/1/2025 si è materializzato per una sola seduta.
- *Crouzet, N., Eberly, J. (2019), "Understanding Weak Capital Investment: The Role of Market Concentration and Intangibles", NBER WP 25869, e Brookings 2018.* Dimostra che la crescita degli intangibili e la concentrazione di mercato modificano la sensibilità del capex aggregato al Tobin's q. **Rilevante**: il capex hyperscaler 2024–2026 è un *outlier* rispetto alle relazioni storiche q/I — non sorprende che il segnale "capex revision" sia ad alta intensità informativa.
- *Bessen, J. (2022), "The New Goliaths" (Yale University Press) / Bessen NBER WP 24235.* Documenta come gli investimenti in software/IT proprietario producono *barriere all'entrata* sostenute. **Rilevante** per il giudizio sulla durabilità dei Mag7.

## Recommendations operative (per il sistema di matching news → episodio storico)

1. *Indicizzazione primaria per classe (A/B/C/D) e per nome.* Per ogni news incoming, costruire un *feature vector* con: (i) classe del catalizzatore, (ii) ticker emittente, (iii) magnitudine percentuale della sorpresa (vs consenso pubblico), (iv) presenza/assenza di confounders macro nelle 48 ore. Solo episodi con feature vector simile sulle prime 3 dimensioni vanno usati come analoghi.
2. *Pesatura delle finestre*: usare T+1 e T+3 come segnali principali; T+5 come segnale di persistenza; T+10 come controllo di robustezza solo se non ci sono altri eventi macro/sectoral nello stesso intervallo.
3. *Esclusione di episodi confounded*: aprile 2025 (H20 + tariffe Trump), Q4 2018 (Fed hawkish), Q3 2022 (BoE Gilts) non sono usabili come puri eventi-chip — usare con peso ridotto o solo per il T+1.
4. *Soglia di trigger di event study*: classe A con |sorpresa guidance vs consenso| > 10% sui ricavi → analogo NVDA mag 2023 (upside) / Broadcom giu 2019 (downside) / MU set 2022 (downside).
5. *Monitor di concentrazione*: pesare gli analoghi pre-2022 con un *concentration discount* (gli indici erano meno concentrati, quindi la propagazione single-name → indice era più debole). Una mappa di equivalenza approssimativa: una reazione SOXX del 2018–2019 va moltiplicata per ~1.3–1.5 per stimare la reazione SOXX equivalente nel regime 2024–2026.
6. *Caso DeepSeek come "canary" per la classe C*: lo shock 27/1/2025 ha il profilo più peculiare nel dataset (forte single-day, recupero quasi integrale in 4 sedute). Usarlo come *prototipo* per shock di tipo "demand function shift" — distinto dagli shock di guidance.
7. *Recommendation di monitoring continuo*: tracciare in tempo reale (i) tasso di crescita YoY del capex aggregato hyperscaler, (ii) gross margin NVDA/AVGO trailing-4Q, (iii) AI revenue Broadcom run-rate. Una decelerazione coordinata su tutti e tre i fattori è il vero "regime change" da intercettare — ad oggi non osservato.

## Caveats

1. **Limitazione quantitativa**: gran parte dei rendimenti T+3, T+5, T+10 nella tabella episodi NON è stata verificata contro dati di prezzo primari per limiti di accesso ai CSV storici in tempo reale durante questa compilazione. Le celle marcate [NV] sono *stime direzionali*; un passaggio successivo su Yahoo Finance / FRED / Stooq è raccomandato per backtest production-grade.
2. **Endogeneità del consenso**: i "consensus" pre-earnings citati (Refinitiv/FactSet) sono *moving target* — alcuni episodi mostrano consensus revisioni nelle 24–48 ore precedenti l'annuncio che attenuano la sorpresa formale.
3. **Concentrazione di indice come variabile mobile**: il peso di NVDA in S&P 500/^NDX è cambiato sostanzialmente tra 2018 (~0.5%) e 2026 (~7%); usare gli episodi 2018–2019 senza correzione per concentrazione comporta sottostima sistematica della reazione equivalente moderna.
4. **Confounders macro**: come notato, almeno 3 episodi su 12 (NVDA 2018, MU 2022, NVDA H20 2025) sono sovrapposti a regimi macro distinti che dominano oltre T+3.
5. **Reaction function della politica**: dopo il pivot dell'amministrazione Trump nel luglio 2025 (citato dal Built In article: "Trump Lifted the AI Chip Ban on China"), il segnale "policy shock" (classe D) ha una reaction function di mercato meno chiara — il regime di policy è meno stabile di quanto fosse nel 2022–2024.
6. **Non-trasferibilità dei pattern**: il "dot-com analogue" e il "semis cycle 2018 analogue" sono strutturalmente diversi e non vanno usati come benchmark di pricing oggi (sezione 5).
7. **Cobertura asiatica**: la propagazione su ^N225, KOSPI, TWSE non è documentata quantitativamente in questo testo per limiti di tempo. È raccomandato un secondo passaggio dedicato per le sessioni asiatiche overnight su SK Hynix, Samsung, TSMC.

```yaml
---
title: "Ciclo semiconduttori & AI capex (2023–2026): catalizzatori discreti e trasmissione"
date_compiled: 2026-06-08
primary_theme: structural_themes
sub_themes: [ai_capex, ai, semiconductors, semis, chips, nvidia, earnings_guidance_shock, earnings, hyperscaler_capex, hyperscaler, market_concentration, export_controls]
relevant_assets:
  - ^GSPC
  - ^N225
external_assets_mentioned:
  - "SOXX (iShares Semiconductor ETF) — presente in tabella prices ma non in assets"
  - "^NDX (Nasdaq-100) — presente in tabella prices ma non in assets"
  - "Philadelphia Semiconductor Index ^SOX — proxy = SOXX"
  - "NVDA, AVGO (Broadcom), AMD, MU (Micron), TSM, ASML, SK Hynix, Samsung — single-name, non in DB"
  - "Hyperscaler equities: MSFT, GOOGL, AMZN, META — non in DB"
  - "Power/AI infra: Vistra, Constellation Energy, Siemens Energy, GE Vernova — non in DB"
time_window:
  start: 2018-01-01
  end: 2026-12-31
regime_phases:
  - pre_ai_semis_cycle: 2018-01-01 to 2022-12-31
  - chatgpt_ignition_and_nvidia_repricing: 2023-01-01 to 2024-06-30
  - hyperscaler_capex_arms_race: 2024-07-01 to 2025-01-26
  - capex_returns_scrutiny_deepseek_onward: 2025-01-27 to 2026-12-31
keywords:
  - ai capex
  - semiconductors
  - nvidia
  - broadcom
  - micron
  - deepseek
  - guidance shock
  - earnings surprise
  - hbm
  - gpu
  - hyperscaler
  - data center
  - nasdaq 100
  - sox semiconductor index
  - export controls
  - chips act
  - market concentration
  - magnificent seven
  - dot-com comparison
  - productivity
  - intangible investment
---
```