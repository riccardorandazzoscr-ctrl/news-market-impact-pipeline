# Il vincolo elettrico del capex AI: potenza, reti e turbine come collo di bottiglia — regime ed episodi storici (2021–presente)

## §1 Sintesi esecutiva

1. **Il mercato ha iniziato a prezzare la potenza elettrica come vincolo marginale del capex AI in modo discreto e databile a partire dal 20 settembre 2024**, giorno in cui l'accordo Constellation–Microsoft per il riavvio di Three Mile Island (Crane Clean Energy Center) fece chiudere Constellation (CEG) a $254,98, +22% in una singola seduta (circa +15 miliardi di dollari di capitalizzazione; CNBC: "Constellation stock jumped about 22% on Friday to close at $254.98 per share"). Prima di quella data la spesa AI era prezzata quasi interamente attraverso il canale-chip (Nvidia, SOXX, ^NDX); dopo, il canale "domanda elettrica" (utility, IPP nucleari) diventa un tema autonomo. La confessione di Satya Nadella diventa poi il punto in cui il vincolo elettrico è esplicitato come guidance: al BG2 Pod (con Sam Altman, Brad Gerstner e Bill Gurley), verbatim, "you may actually have a bunch of chips sitting in inventory that I can't plug in. In fact, that is my problem today. It's not a supply issue of chips; it's actually the fact that I don't have warm shells to plug into" (via Tom's Hardware/DCD, ottobre-novembre 2025).

2. **La divergenza SOXX/XLU è misurabile ma il campione pulito è sottile.** Gli episodi in cui il verso diverge davvero (XLU su, SOXX giù, o viceversa) sono pochi: il grosso degli eventi di capex AI muove SOXX e XLU nella *stessa* direzione per sentiment, non per canale. I casi realmente redistributivi identificati sono dell'ordine di 4-6, non abbastanza per una statistica robusta: vanno trattati come indicativi.

3. **Il vincolo elettrico si manifesta su tre canali strutturalmente diversi** — capacità di generazione dedicata (nucleare/gas/solare), backlog dei produttori di turbine e trasformatori, code di interconnessione alla rete — che hanno firme di prezzo differenti. Solo il primo è chiaramente redistributivo; il secondo e il terzo sono amplificatori dei tempi, non della cancellazione della spesa.

4. **Dove l'event study è affidabile:** eventi discreti e ad alta salienza mediatica con reazione intraday chiara su singoli nomi (CEG, VST, GEV, OKLO) e, per riflesso, su XLU. **Dove NON lo è:** distinguere un evento "puramente elettrico" da un generico shock di sentiment sul capex AI; il campione cade quasi interamente in una fase rialzista sul tema AI (drift di fondo positivo), e la maggior parte degli episodi è post-settembre 2024, quindi l'inferenza sul regime 2021–2023 è debolissima.

5. **Non esiste oggi un proxy quotato pulito per l'equipaggiamento di rete/turbine.** `GRID` è scartato (correla 0,80 con SOXX). Il candidato migliore identificato è `VOLT` (Tema Electrification ETF, quotato NASDAQ dal 3 dicembre 2024), che detiene GE Vernova ed Eaton ma resta un paniere di elettrificazione diversificato, non nel database: da dichiarare, non da assumere.

## §2 Tassonomia dei canali di trasmissione

**Canale A — Capacità di generazione dedicata (nucleare/SMR, gas, solare) [REDISTRIBUTIVO].**
Catena causale: *evento* (hyperscaler firma PPA nucleare, riavvio impianto, ordine SMR) → *meccanismo* (la scarsità di MWh disponibili sposta valore verso chi possiede o costruisce generazione firm; segnala che il collo di bottiglia è a valle del chip) → *variabile* (ricavi contrattualizzati pluriennali per IPP/utility; premio di scarsità sul prezzo dell'energia) → *prezzo* (rialzo di CEG, VST, TLN, OKLO e, per aggregazione, di XLU; effetto neutro o marginalmente positivo su SOXX). Asset-proxy: **XLU (pos)**, con **SOXX** e **^NDX** neutrali o marginalmente positivi. Questo è l'unico canale che può muovere SOXX e XLU in direzioni opposte, soprattutto quando l'evento è un *rifiuto* regolatorio (FERC) che colpisce le utility senza toccare i chip. **TAN** entra quando l'evento riguarda generazione solare dedicata.

**Canale B — Backlog di turbine e trasformatori [AMPLIFICATORE].**
Catena causale: *evento* (GE Vernova/Siemens Energy dichiara backlog record, slot sold-out fino al 2028-2030, lead time trasformatori >2 anni) → *meccanismo* (l'equipaggiamento diventa il percorso critico: allunga i tempi di realizzazione dei data center ma non li cancella; ridistribuisce valore verso i costruttori di equipaggiamento) → *variabile* (order backlog in GW e in dollari; lead time in settimane) → *prezzo* (rialzo di GE Vernova/Siemens Energy; effetto sul tema più che sul canale). Poiché non c'è ETF pulito, il segnale ricade su nomi singoli (GEV) e in parte su XLU. Questo canale è **amplificatore**: in un contesto rialzista muove SOXX e XLU nella stessa direzione, con ampiezza diversa; solo in eventi negativi molto specifici (es. DeepSeek) si vede un movimento comune al ribasso. Proxy imperfetto: **XLU** parziale; nessun proxy diretto nel database (vedi §6 e VOLT).

**Canale C — Code di interconnessione alla rete (interconnection queue) [STRUTTURALE/LENTO].**
Catena causale: *evento* (report LBNL "Queued Up" — edizione 2024, dati a fine 2023, autori Rand et al.: "nearly 2,600 gigawatts (GW) of total generation and storage capacity now seeking connection", scesi a ~2.290 GW nell'edizione 2025 su dati fine 2024, −12%; asta di capacità PJM a prezzo record trainata dai data center; regole di fast-track PJM per grandi carichi) → *meccanismo* (il collo di bottiglia è amministrativo e fisico, lento a risolversi, diverso per natura da uno shock di offerta di chip che si esaurisce in trimestri) → *variabile* (GW in coda; durata mediana dalla richiesta alla messa in servizio raddoppiata da <2 anni nel 2000–2007 a oltre 4 anni nel 2018–2024, con mediana di 5 anni per i progetti completati nel 2023 e solo il 13% della capacità 2000–2019 realizzata, per LBNL Queued Up 2025 Edition; prezzo $/MW-day dell'asta di capacità) → *prezzo* (rialzo strutturale delle utility/IPP nella zona interessata; impatto diffuso e lento su XLU). Proxy: **XLU (pos, lento)**. Questo canale raramente produce una reazione intraday netta salvo l'annuncio dell'asta PJM.

**Canale D — Cancellazione/ritardo di progetti vs. sola maggiorazione di costo [DIAGNOSTICO].**
Catena causale: *evento* (un vincolo elettrico blocca o rinvia un progetto annunciato — es. FERC che boccia la co-location Talen–Amazon il 1° novembre 2024 — distinto da eventi in cui il progetto procede ma più caro/lento) → *meccanismo* (il rifiuto regolatorio segnala che la via "behind-the-meter" diretta è ostruita) → *variabile* (MW autorizzati vs richiesti: la richiesta PJM di alzare la fornitura da 300 a 480 MW fu respinta 2-1) → *prezzo* (caduta acuta degli IPP esposti: CEG −12,5%, VST, TLN giù nella seduta del 4 novembre 2024). Questo è l'unico caso in cui il canale elettrico produce un segnale **negativo** su XLU/IPP mentre i chip restano piatti: prezioso per la validazione, perché mostra che XLU e SOXX possono divergere.

**Riepilogo direzionale.** Canale A e Canale D sono **redistributivi** (possono muovere SOXX e XLU in direzioni opposte). Canale B e Canale C sono **amplificatori/strutturali** (tendono a muovere entrambi nella stessa direzione con ampiezza diversa, salvo eventi negativi idiosincratici).

## §3 Catalogo di episodi-ancora datati

Le date sono la seduta di reazione del proxy. "Direzione attesa" è in forma canonica per ciascun asset quando i versi divergono.

| Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead |
|---|---|---|---|---|---|
| 2024-09-20 | Constellation–Microsoft: riavvio Three Mile Island/Crane per data center; CEG chiude +22% a $254,98 | A | SOXX: neutral / XLU: pos / ^NDX: neutral | XLU, ^NDX | Venerdì (quad-witching). Primo episodio "potenza" ad alta salienza; annuncio a mercato aperto. |
| 2024-10-14 | Google–Kairos Power: primo PPA aziendale su SMR (500 MW, 6-7 reattori) | A | SOXX: neutral / XLU: pos | XLU | Lunedì. Reazione concentrata su nomi nucleari/SMR. |
| 2024-10-16 | Amazon–X-energy: investimento ~$500M, >5 GW SMR al 2039 | A | SOXX: neutral / XLU: pos | XLU, TAN | Mercoledì. Conferma il pattern SMR degli hyperscaler. |
| 2024-11-04 | FERC boccia (2-1) l'espansione co-location Talen–Amazon (300→480 MW) | D | SOXX: neutral / XLU: neg | XLU | Lunedì (vigilia elezioni USA). CEG −12,5%, VST ~−3%, TLN ~−2%. Segnale negativo puro sul canale elettrico. |
| 2024-12-03 | Meta lancia RFP nucleare 1–4 GW (SMR o grandi reattori, dai primi anni 2030) | A | SOXX: neutral / XLU: pos | XLU | Martedì. Annuncio a mercato aperto. |
| 2025-01-21 | Annuncio Stargate ($500 mld su 4 anni, 10 GW) alla Casa Bianca | A/C | SOXX: pos / XLU: pos | ^NDX, XLU | Martedì (conferenza stampa serale). Evento "capex totale": muove entrambi i canali nella stessa direzione (sentiment). |
| 2025-01-27 | Selloff DeepSeek: dubbi sull'intensità di potenza dell'AI | Controllo (chip-efficiency) | SOXX: neg / XLU: neg | SOXX, XLU, ^NDX | Lunedì. Nvidia −16,9% (−$593 mld, record Wall Street); Philadelphia Semiconductor Index −9,2%; Nasdaq −3,1%; Vistra −28,3%, Constellation −20,8%, NRG −13,2%, GE Vernova −21%, Siemens Energy −20%. Shock che colpisce ENTRAMBI i canali. |
| 2025-04-16 | Reazione al charge Nvidia di $5,5 mld su H20 (export control, disclosure 15/4) | Controllo (chip) | SOXX: neg / XLU: pos | SOXX, ^NDX | Disclosure 15/4 a mercato chiuso → reazione 16/4. ^NDX −3,04% (Barchart); SOXX ~−4/−5%; utility difensive in rotazione. Canale-chip negativo con XLU che sovraperforma. |
| 2025-06-03 | Constellation–Meta: PPA nucleare ventennale (Clinton) | A | SOXX: neutral / XLU: pos | XLU | Martedì. CEG sale in apertura (~+7/+15% intraday) poi ripiega: usare la seduta 03/06. |
| 2025-06-11 | Talen–Amazon: PPA ampliato a 1.920 MW fino al 2042 | A | SOXX: neutral / XLU: pos | XLU | Mercoledì. Comunicato aziendale ore 06:00 ET. |
| 2025-07-15 | USA autorizza ripresa vendite H20 in Cina | Controllo (chip) | SOXX: pos / XLU: neutral | SOXX, EWT | Martedì. Nvidia e AMD +>4%. Evento chip-positivo: verso opposto rispetto al canale elettrico. |
| 2025-07-22 | Asta capacità PJM 2026/2027 al cap FERC $329,17/MW-day (da $269,92, +22%), 134.311 MW procurati | C | SOXX: neutral / XLU: pos | XLU | Risultati diffusi ~22/7 (report 23/7). Per Introl la domanda data center ha determinato il 63% dell'aumento. |
| 2025-10-16 | TSMC Q3: ricavi +40% a $33,1 mld, N2 in volume entro fine 2025 | Controllo (chip) | SOXX: pos / EWT: pos / XLU: neutral | SOXX, EWT | Giovedì (earnings call). Progresso lato fonderia: canale chip positivo. |
| 2025-10-31 | Nadella (BG2): "GPU in inventario che non posso collegare, mancano warm shells" | B/C | SOXX: neutral / XLU: pos | XLU | Episodio pubblicato ~31/10. Non un mover di mercato netto: valore semantico, marca il vincolo come guidance. |
| 2025-12-09 | GE Vernova investor update: backlog gas ~80 GW a fine 2025, slot sold-out verso il 2030 | B | SOXX: neutral / XLU: pos | XLU | Martedì. Segnale di amplificatore (turbine come percorso critico). |
| 2025-12-17 | Asta capacità PJM 2027/2028 al cap FERC $333,44/MW-day (terzo record consecutivo); 145.777 MW; deficit di 6.625 MW sotto il target di riserva del 20% | C | SOXX: neutral / XLU: pos | XLU | Mercoledì; report market monitor successivo (data center ~40% dei costi). Prima volta sotto il target di riserva. |
| 2026-05-06 | NRC approva i Principal Design Criteria dell'Aurora di Oklo; OKLO +12% | A | SOXX: neutral / XLU: pos | XLU, TAN | Mercoledì. Nome SMR; proxy XLU imperfetto. |
| 2026-07-22 | GE Vernova Q2: backlog $176 mld, ordini Power +134%, ≥125 GW gas sotto contratto al 2026 | B | SOXX: neutral / XLU: pos | XLU | Mercoledì (8-K). Conferma strutturale del canale turbine. |
| 2026-08-24 | Aggreko deposita F-1 per IPO NYSE (valutazione riportata ~$15 mld) trainata dai data center | A/B | SOXX: neutral / XLU: pos | XLU | Lunedì. Evento-ancora della tesi: potenza modulare/bridge come collo di bottiglia (data center ~19% dei ricavi). |

Date **non-ISO** (da non trattare come episodi): riavvio di Three Mile Island atteso "nel 2027" (revisione da 2028); groundbreaking Fab 21 Phase 3 di TSMC "aprile 2025"; dichiarazione GE Vernova "sold-out fino al 2028" di "marzo 2025"; picco delle utility come miglior settore "fine 2024"; pledge di triplicazione del nucleare al CERAWeek di "inizio-metà marzo 2026" (data incerta fra due fonti, 5 e 12 marzo 2026: non usata come ISO); lead time trasformatori a ~120 settimane "nel 2024".

## §4 Statistiche indicative

Tutte le statistiche sotto sono **INDICATIVE ONLY** (campione N < 10 in ogni sotto-categoria). I valori di prezzo a un giorno provengono da fonti secondarie; per l'uso nella pipeline vanno ricalcolati sui proxy esatti (Yahoo/Barchart historical).

**Canale A (generazione dedicata), reazione a 1 giorno — N = 7 episodi (INDICATIVE ONLY).**
Su singoli nomi la reazione mediana è nettamente positiva (CEG +22% il 20/09/2024; OKLO +12% il 06/05/2026). Su **XLU** l'impatto è positivo ma attenuato (XLU è cap-weighted su 30+ utility, CEG pesa ~6%): il segnale netto atteso su XLU è dell'ordine di +0,5/+1,5% nella seduta, contro reazioni a doppia cifra sui singoli IPP. **SOXX** resta sostanzialmente neutrale. Spread SOXX−XLU: **negativo** (XLU sovraperforma).

**Canale B (turbine/trasformatori), reazione a 1 giorno — N = 3 (INDICATIVE ONLY).**
Nessun proxy pulito; il segnale è su GEV (non nel database). Su XLU l'effetto è debole e nella stessa direzione del tema. Spread SOXX−XLU: **prossimo a zero o lievemente negativo**.

**Canale C (interconnection/PJM), reazione a 1 giorno — N = 3 (INDICATIVE ONLY).**
Reazione intraday debole salvo l'asta; effetto strutturale che si accumula su XLU su orizzonti più lunghi di T+10. Spread SOXX−XLU: **debolmente negativo**.

**Controlli chip — N = 4 (INDICATIVE ONLY).**
- 2025-01-27 (DeepSeek): SOXX ~−9% (proxy Philadelphia Semiconductor Index −9,2%), XLU −2,3% (Morningstar), ^NDX ~−3,0/−3,1% (il −3,1% documentato è il Nasdaq Composite; NDX comparabile). Spread SOXX−XLU ≈ **−6,7 pp**: *entrambi* giù, ma i chip molto più dei power. È uno shock di efficienza che colpisce i due canali insieme → verso concorde, non divergente.
- 2025-04-16 (H20 charge): SOXX ~−4/−5%, ^NDX −3,04%, XLU in rialzo (rotazione difensiva). Spread SOXX−XLU: **fortemente negativo con verso opposto** (chip giù, utility su) → caso redistributivo "da lato chip".
- 2025-07-15 (ripresa H20): SOXX pos (Nvidia/AMD +>4%), XLU neutrale → spread **positivo**.
- 2025-10-16 (TSMC N2): SOXX/EWT pos, XLU neutrale → spread **positivo**.

**Lettura d'insieme dello spread SOXX/XLU come serie derivata.** Il segno dello spread è informativo *condizionatamente al tipo di evento*: negativo (XLU>SOXX) sugli eventi di generazione dedicata e sugli shock negativi lato chip; positivo (SOXX>XLU) sui progressi lato fonderia/allentamento export. Sugli eventi di "capex totale" (Stargate) e sugli shock di sentiment (DeepSeek) il segno non separa i canali. Con N così bassi per cella, nessuna media è statisticamente affidabile: la serie va usata come filtro qualitativo, non come stima puntuale.

## §5 Fasi di regime

**`chip_scarcity_regime` — 2021-01-01 → 2024-09-19.** Il collo di bottiglia percepito è il silicio (allocazione GPU Nvidia, capacità CoWoS di TSMC). La potenza è un tema di sostenibilità, non un vincolo di prezzo. Divergenza SOXX/XLU non informativa sul canale elettrico. **Usabilità nel regime corrente: bassa.** Gli analoghi pre-settembre 2024 non servono a distinguere il vincolo di potenza.

**`power_repricing_onset` — 2024-09-20 → 2025-01-26.** Innescato dal deal Constellation–Microsoft. Il mercato inizia a prezzare la generazione firm (nucleare/SMR) come tema autonomo; Vistra (+257,9% nel 2024) e Constellation fra i migliori titoli S&P 500 dell'anno. Il vincolo è percepito come opportunità (PPA, riavvii), non ancora come freno alla crescita. **Usabilità: media-alta** per episodi di tipo A; la reazione delle utility è genuina e ripetibile.

**`efficiency_shock_interlude` — 2025-01-27 → 2025-02-28.** Fase breve ma diagnostica: DeepSeek mette in dubbio l'intensità di potenza dell'AI, colpendo *insieme* chip e power. Dimostra che uno shock di domanda percepita muove i due canali nello stesso verso. **Usabilità: alta come controllo**, bassa come analogo di vincolo-di-potenza.

**`power_as_binding_constraint` — 2025-03-01 → presente.** Il vincolo elettrico diventa guidance ricorrente: backlog turbine sold-out (GE Vernova), lead time trasformatori pluriennali (NERC: ~120 settimane nel 2024, in ulteriore aumento), aste PJM a record consecutivi, e la formulazione esplicita di Nadella ("warm shells"). La potenza è ora il fattore limitante dichiarato, non i chip. L'IPO Aggreko (agosto 2026) è il coronamento della tesi. **Usabilità: alta** — è il regime corrente; gli episodi qui sono i più rappresentativi per la pipeline.

## §6 Caveat metodologici

**Isolare l'evento "puramente elettrico".** Il limite principale è che la maggior parte degli eventi di capex AI muove SOXX e XLU nella stessa direzione per sentiment condiviso, non per canale. Solo gli eventi di tipo A (generazione dedicata) e di tipo D (rifiuto regolatorio) producono divergenza affidabile; gli eventi di tipo B e C spesso si confondono con il tema AI generale. Un evento come Stargate (21/01/2025) è "capex totale" e non separa i canali. Il ricercatore deve etichettare a mano ogni episodio per tipo prima di aggregare.

**Assenza di un proxy pulito per equipaggiamento di rete/turbine.** `GRID` (First Trust NASDAQ Clean Edge Smart Grid) è stato valutato e **scartato**: correla 0,80 con SOXX, quindi confonde i canali invece di separarli — non va riproposto. Il miglior candidato identificato è **`VOLT` (Tema Electrification ETF, NASDAQ, inception 3 dicembre 2024)**, che detiene esplicitamente GE Vernova, Eaton, Quanta Services, Powell Industries e ha un tilt industrials/equipaggiamento (Industrials ~41%, Utilities ~30%) più marcato di GRID; conterebbe perché cattura i costruttori di turbine/trasformatori che sono il cuore del Canale B. **Limiti:** VOLT resta un paniere di elettrificazione diversificato (include utility e pipeline come Energy Transfer), ha storia cortissima (dal dicembre 2024, quindi nessun dato pre-regime), e non è nel database — va dichiarato, non assunto. Nessun ETF USA pure-play su turbine/trasformatori (GEV + Siemens Energy) risulta esistere; Siemens Energy è quotata a Francoforte (ENR.DE), fuori portata per un ETF USA. In alternativa, il segnale del Canale B va misurato sul singolo nome GEV.

**Drift di fondo rialzista.** Quasi tutti gli episodi cadono in una fase di mercato euforica sul tema AI (2024-2026). Le reazioni positive delle utility possono riflettere il beta del tema più che il canale elettrico: senza aggiustamento per il rendimento di mercato e per il beta settoriale, le medie a T+1…T+10 sono contaminate da drift positivo. Il residuo XLU al netto del mercato (−0,21 indicato dal database) suggerisce che il segnale di canale, una volta tolto il beta, è debole e va misurato su spread e non su livelli.

**Campione denso solo nel regime corrente.** Con l'onset a settembre 2024 e la fase vincolante da marzo 2025, gli episodi datati sono concentrati in ~24 mesi. L'inferenza sul comportamento del canale in un eventuale regime di *disinflazione* del tema (analogo a DeepSeek ma prolungato) è priva di analoghi: il 27 gennaio 2025 è l'unico vero campione di shock al ribasso, e va usato con cautela.

**Incertezze residue sulle date.** Le reazioni intraday sono documentate su singoli nomi (CEG, VST, GEV, OKLO) da fonti giornalistiche; i valori esatti su SOXX/XLU/^NDX per ciascuna data vanno ricalcolati dai listini storici prima dell'uso quantitativo (le fonti più pulite reperite sono: XLU −2,3% il 27/01/2025 da Morningstar; ^NDX −0,21% il 20/09/2024 e −3,04% il 16/04/2025 da Barchart). Le date con annuncio a mercato chiuso o in festivo (es. H20 il 15/04 → 16/04) sono spostate alla prima seduta utile e annotate. Il pledge nucleare del CERAWeek di marzo 2026 ha data incerta fra due fonti e non è stato promosso a episodio ISO.

```yaml
---
title: "Il vincolo elettrico del capex AI: potenza, reti e turbine come collo di bottiglia — regime ed episodi storici (2021–presente)"
date_compiled: 2026-09-03
primary_theme: structural_themes
sub_themes: [power_bottleneck, grid_capacity, ai_capex]
relevant_assets: [SOXX, XLU, ^NDX, ^GSPC, EWT, IGV, TAN, REMX]
external_assets_mentioned:
  - "GRID: valutato e scartato — correla 0,80 con SOXX, non separa i canali"
  - "VOLT (Tema Electrification ETF, NASDAQ, inception 2024-12-03): candidato migliore per il canale turbine/trasformatori — detiene GE Vernova, Eaton, Quanta, Powell Industries; tilt industrials ~41% / utilities ~30%; ma paniere diversificato, storia cortissima, non nel database"
  - "GEV (GE Vernova): singolo nome, non ETF — proxy diretto del backlog turbine/trasformatori"
time_window:
  start: 2021-01-01
  end: present
regime_phases:
  - chip_scarcity_regime: 2021-01-01 to 2024-09-19
  - power_repricing_onset: 2024-09-20 to 2025-01-26
  - efficiency_shock_interlude: 2025-01-27 to 2025-02-28
  - power_as_binding_constraint: 2025-03-01 to present
keywords: [vincolo elettrico, power bottleneck, grid, rete elettrica, turbine, data center, interconnection queue, capex AI, hyperscaler, SMR, power purchase agreement]
```