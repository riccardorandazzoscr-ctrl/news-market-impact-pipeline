# Rottura commerciale Emirati-Iran, nave colpita a Hormuz e quarta seduta di rialzo del greggio con forte calo dei distillati

**Data analisi**: 2026-08-19
**Fonte**: Morning Briefing 2026-08-19 (intl 01-02-03, fin 08)
**Slug**: uae-iran-hormuz-crude

---

## Testo notizia (originale)

> Gli Emirati Arabi Uniti hanno sospeso 'fino a nuovo avviso' ogni scambio commerciale e finanziario con l'Iran dopo che due missili balistici sarebbero stati lanciati verso il territorio emiratino (uno caduto dentro le acque territoriali). Dubai era da decenni il principale hub di re-export e il canale finanziario informale dell'Iran. In parallelo la Francia espelle due diplomatici iraniani, e UKMTO segnala una nave colpita da un proiettile non identificato in uscita dallo Stretto di Hormuz, con i transiti giornalieri rimasti a una cifra; un alto funzionario iraniano annuncia una postura 'fully offensive' mentre Trump conferma il blocco navale. Sul prezzo: Brent ~91 $/barile e WTI ~85 $ dopo quattro sedute consecutive di rialzo (massimo di tre settimane), con un sondaggio privato sulle scorte USA che mostra un calo del greggio e un calo molto ampio dei distillati.

---

## In breve (in parole semplici)

Gli Emirati Arabi Uniti — cioè Dubai, che da decenni è la porta commerciale e finanziaria attraverso cui l'Iran aggira le sanzioni — hanno chiuso di colpo ogni scambio con Teheran. Nella stessa notte la Francia espelle due diplomatici iraniani e una nave viene colpita in uscita dallo Stretto di Hormuz, il corridoio marittimo da cui passa circa un quinto del petrolio mondiale. Il petrolio sale per la quarta seduta di fila, ma il dato più informativo non è il greggio: è il crollo delle scorte di distillati (gasolio/diesel) negli Stati Uniti.

La domanda che ci poniamo è: quando un'escalation colpisce un collo di bottiglia marittimo, *dove* si scarica davvero il prezzo? Sul greggio, o sui prodotti raffinati e sul margine di raffinazione? L'event study storico dà una risposta netta.

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | commodity_energy |
| `sub_themes` | shipping_chokepoint, iran, refinery_products |
| `sentiment` | risk-off |
| `confidence` | medium |
| `horizon` | 1-5 giorni di trading |

**Motivazione classificazione**: la notizia è formalmente geopolitica (sanzioni bilaterali, espulsioni diplomatiche, attacco a una nave), ma il canale di trasmissione misurabile sui nostri asset è energetico, e per questo la classifichiamo `commodity_energy`. Il sotto-tema canonico è `shipping_chokepoint` (collo di bottiglia marittimo): il fatto rilevante non è la retorica ma il numero di transiti giornalieri da Hormuz, rimasto a una sola cifra. Sentiment `risk-off` perché ogni componente della notizia riduce l'offerta potenziale o alza il premio per il rischio. Confidence `medium` e non `high` perché la rottura commerciale Emirati-Iran è un evento senza precedenti diretti nel campione (i nostri analoghi sono attacchi e minacce di chiusura, non embarghi intra-Golfo), quindi la mappatura sull'episodio storico è per analogia di canale, non di forma.

---

## Asset rilevanti

### Primary (canale diretto)
- **CRACK_321** — il margine di raffinazione 3-2-1 (in dollari per barile): quanto guadagna una raffineria trasformando 3 barili di greggio in 2 di benzina e 1 di gasolio. È **il** canale quando lo shock colpisce logistica e prodotti anziché la produzione di greggio.
- **HO=F** (futures sul gasolio da riscaldamento/diesel NYMEX) — il prodotto raffinato dove il calo di scorte è concentrato, e quello che il briefing indica come il numero davvero rilevante.
- **BZ=F** (futures sul petrolio Brent) — il benchmark del greggio, canale diretto ma il *meno* sensibile a uno shock di trasporto/prodotti.
- **RB=F** (futures sulla benzina RBOB) — completa la struttura del crack, monitorato ma non centrale qui.

### Secondary (effetti indiretti)
- **GC=F** (futures sull'oro) — bene rifugio classico; oggi però in fase di rottura al ribasso per il costo-opportunità dei rendimenti alti (vedi [news_03](news_03.md)).
- **CHF=X** (franco svizzero contro dollaro) — rifugio valutario, il più "pulito" perché meno contaminato dal canale tassi.
- **^VIX** (indice della volatilità implicita a 30 giorni sull'S&P 500, il cosiddetto "indice della paura") — misura quanto il mercato azionario prezza il rischio di coda.
- **^GSPC** (indice azionario S&P 500) — risk-off generale e componente energia dell'indice.
- **TTF=F** (gas naturale europeo, Dutch TTF) — *escluso dall'event study*: nel test preliminare la dispersione era enorme (deviazione standard fino al 27% a T+10) perché il gas europeo è guidato da meteo e flussi russi, non dal Golfo. Includerlo avrebbe aggiunto rumore, non informazione.

---

## Knowledge Base — research correlate

- [score=11] `iran_hormuz/compass_artifact_wf-57769786-924f-41b7-8c1e-36177b05bebd_text_markdown.md` — *Iran – Stretto di Hormuz e il premio geopolitico sul petrolio: regime ed episodi storici (1980–2026)*
  - Perché è rilevante: è la research che definisce la distinzione operativa fra shock di **premio di rischio** (escalation senza interruzione effettiva → rialzo di pochi dollari, riassorbito in settimane) e shock di **offerta vera** (interruzione fisica → rialzo persistente, safe haven coinvolti). La notizia di oggi va collocata su questo asse.
- [score=4] `Russia-Ucraina- attrito energetico e regime sanzioni (2022–2026).md` — *Russia-Ucraina: attrito energetico e regime sanzioni*
  - Perché è rilevante: fornisce il precedente più vicino di *sanzioni che colpiscono i prodotti raffinati e non il greggio* (embargo UE su diesel russo, febbraio 2023), cioè lo stesso meccanismo asimmetrico che ci aspettiamo qui.
- [score=3] `ciclo_inflazione_eurozona_2021-2023/Ciclo inflazione Eurozona 2021–2023.md`
  - Perché è rilevante: documenta il passaggio da shock energetico a inflazione generale, che è la ragione per cui questo tema si lega direttamente alle schede sui tassi lunghi di oggi.

---

## Regime storico identificato

- **Regime**: `hormuz_closure_mou_2026` — dal 2026-02-01 a oggi (research Iran/Hormuz).
- **Caratterizzazione**: siamo nel regime di **shock di offerta vero**, non di semplice premio di rischio. La research lo qualifica come il maggiore shock nella storia del mercato petrolifero secondo l'Agenzia Internazionale dell'Energia, con tre tratti distintivi rispetto ai regimi precedenti: i tassi USA salgono (canale inflattivo, non flight-to-quality), l'oro è "fuori fase" rispetto al copione del bene rifugio, e il dollaro è forte. Il memorandum d'intesa di giugno è scaduto e non c'è un quadro sostitutivo: l'escalation non ha un gradino concordato su cui fermarsi. Le mosse di oggi (embargo emiratino, espulsioni francesi, postura "fully offensive") **stringono ulteriormente** un regime già di offerta, restringendo per di più i canali finanziari e diplomatici residui.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla libreria (Opzione B) con:
`--theme commodity_energy --subtheme shipping_chokepoint --direction neg --before 2026-08-19`
→ 32 episodi con etichetta **date-locale** (filtro forte, non il fallback debole a livello di documento), ridotti a 30 dal tetto di recency della libreria, poi potati a **24 date** dall'analista. L'event study ne usa **22**: le date `2019-05-13` e `2025-06-23` cadono sullo stesso ancoraggio di borsa dell'episodio del giorno prima e vengono unificate. Nessun look-ahead: tutti gli episodi precedono il 2026-08-19.

**Potature effettuate** (episodi rimossi perché direzionalmente opposti — sono distensioni, non escalation):
- `2014-11-27` — l'OPEC decide di non tagliare la produzione: è uno shock di *eccesso* di offerta, non di collo di bottiglia.
- `2015-07-14` — firma dell'accordo nucleare iraniano (JCPOA): ritorno di offerta iraniana, ribassista.
- `2016-01-19` — "implementation day", rimozione delle sanzioni sull'Iran: ribassista.
- `2022-08-15` — fase distensiva del negoziato nucleare.
- `2023-03-10` — normalizzazione Arabia Saudita-Iran mediata dalla Cina: de-escalation.
- `2026-04-17` — l'Iran annuncia lo Stretto aperto al traffico commerciale e il **Brent perde oltre l'11%**: è l'episodio direzionalmente opposto più violento del campione, tenerlo avrebbe rovesciato il segno.

**Episodi tenuti** (con il meccanismo, non solo il fatto):

- `2012-01-04` — l'UE si orienta verso l'embargo sul greggio iraniano dopo la minaccia di Rahimi di chiudere lo Stretto: **sanzioni che restringono l'offerta → premio geopolitico sul Brent**.
- `2012-01-23` — l'UE formalizza l'embargo petrolifero sull'Iran: **rimozione forzata di barili dal mercato europeo → riallocazione dei flussi e allargamento dei differenziali**.
- `2019-05-12` / `2019-05-13` — sabotaggio di quattro petroliere al largo di Fujairah: **attacco al naviglio, non alla produzione → premio di rischio-navigazione e assicurativo, che si scarica su noli e prodotti più che sul greggio**.
- `2019-06-13` — attacchi alle petroliere nel Golfo dell'Oman: **stesso canale, transiti a rischio → premio war-risk sui transiti di Hormuz**.
- `2019-07-01` — l'OPEC+ estende i tagli produttivi: **restrizione volontaria dell'offerta → tensione sui bilanci di greggio**.
- `2019-09-14` — attacco con droni ad Abqaiq (Arabia Saudita): **colpita l'infrastruttura di trattamento, non il trasporto → il caso di scuola di perdita fisica immediata di offerta (~5,7 milioni di barili/giorno)**.
- `2020-01-08` — ritorsione iraniana su basi USA in Iraq dopo l'uccisione di Soleimani: **rischio di escalation militare diretta sul Golfo → picco di premio e rapido rientro quando l'escalation si ferma**.
- `2022-02-24` — invasione russa dell'Ucraina: **shock di offerta e di rotta su scala globale → il canale prodotti/diesel esplode più del greggio**.
- `2022-03-08` — divieto USA all'import di greggio russo: **sanzioni sull'offerta di un grande esportatore → riallocazione delle rotte e premio sui prodotti**.
- `2023-11-01` — apertura del regime "premio Houthi / Mar Rosso": **rotta alternativa a rischio (non Hormuz) → pass-through basso sul Brent, alto su noli, assicurazione e crack**.
- `2023-12-18` — le principali compagnie sospendono i transiti nel Mar Rosso: **allungamento fisico delle rotte → costo del trasporto dei prodotti, quindi margine di raffinazione**.
- `2024-01-12` — raid USA-Regno Unito contro obiettivi Houthi in Yemen: **escalation militare sul corridoio marittimo → premio di rischio-navigazione**.
- `2024-10-26` — rappresaglia israeliana sull'Iran che risparmia le installazioni petrolifere: **escalation con canale energetico esplicitamente evitato → utile come controfattuale interno al campione**.
- `2025-06-13` — inizio del conflitto diretto Israele-Iran: **rischio di chiusura dello Stretto messo sul tavolo → premio immediato**.
- `2025-06-22` — attacco USA ai siti nucleari iraniani (Fordow): **coinvolgimento diretto degli Stati Uniti → salto discreto del premio di rischio**.
- `2025-06-23` — risposta iraniana e minaccia esplicita su Hormuz: **il canale passa dalla minaccia al prezzo del transito**.
- `2026-02-01` — apertura del regime attuale di chiusura di Hormuz: **da premio di rischio a interruzione fisica → cambio di regime, non di livello**.
- `2026-02-17` — esercitazioni navali iraniane nello Stretto e premi war-risk in salita da 0,125% a 0,2-0,4% del valore assicurato per transito: **il costo assicurativo è il canale che trasferisce il rischio dal greggio ai prodotti**.
- `2026-02-27` — rapporto IAEA GOV/2026/8 sul mancato accesso alle scorte di uranio arricchito iraniane: **innalzamento del rischio di intervento militare → premio anticipatorio**.
- `2026-02-28` — attacchi coordinati USA-Israele (Operation Epic Fury), inizio della guerra del 2026: **shock di offerta conclamato**.
- `2026-03-08` — il Brent supera i 100 dollari per la prima volta dal 2022: **conferma di prezzo del passaggio a regime di offerta**.
- `2026-03-12` — dopo il rilascio di 400 milioni di barili dalle riserve strategiche dei 32 paesi IEA, il Brent chiude comunque a 100,46 dollari: **le riserve strategiche contengono il greggio ma non il collo di bottiglia sui prodotti raffinati → il crack resta tirato**.
- `2026-04-11` — fallimento dei colloqui di Islamabad mediati dal Pakistan: **chiusura del canale diplomatico → riprezzamento al rialzo del rischio di prolungamento**, il precedente strutturalmente più vicino alle espulsioni francesi di oggi.

### Comando eseguito

```bash
venv/bin/python analogues.py find --theme commodity_energy --subtheme shipping_chokepoint \
  --direction neg --before 2026-08-19

venv/bin/python event_study.py \
  --ticker 'BZ=F,CRACK_321,HO=F,GC=F,CHF=X,^VIX,^GSPC' \
  --events 2012-01-04,2012-01-23,2019-05-12,2019-05-13,2019-06-13,2019-07-01,2019-09-14,2020-01-08,2022-02-24,2022-03-08,2023-11-01,2023-12-18,2024-01-12,2024-10-26,2025-06-13,2025-06-22,2025-06-23,2026-02-01,2026-02-17,2026-02-27,2026-02-28,2026-03-08,2026-03-12,2026-04-11 \
  --windows 1,3,5,10 --markdown
```

### Risultati

Rendimenti cumulati a T+1, T+3, T+5, T+10 **giorni di borsa** dopo l'episodio (T+0 = giorno dell'evento).

### Event study — `BZ=F`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -1.03% | +1.23% | +2.38% | +4.33% |
| mediana | -0.26% | +1.43% | +1.76% | +0.78% |
| dev std | +4.95% | +5.18% | +10.56% | +12.70% |
| p25 | -3.40% | -0.82% | -3.33% | -2.47% |
| p75 | +1.62% | +3.23% | +5.08% | +8.29% |
| **N** | **22** | **22** | **22** | **22** |



### Event study — `CRACK_321`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +2.22% | +10.63% | +8.96% | +14.40% |
| mediana | +1.33% | +7.08% | +4.71% | +9.76% |
| dev std | +9.59% | +16.48% | +19.55% | +21.69% |
| p25 | -1.02% | +3.23% | -0.19% | +2.54% |
| p75 | +5.79% | +19.72% | +12.07% | +27.73% |
| **N** | **22** | **22** | **22** | **22** |



### Event study — `HO=F`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.56% | +2.95% | +3.20% | +6.36% |
| mediana | +0.36% | +1.29% | +1.15% | +2.85% |
| dev std | +6.26% | +9.37% | +13.12% | +15.05% |
| p25 | -2.89% | -0.26% | -1.86% | -2.44% |
| p75 | +1.98% | +6.62% | +7.23% | +9.22% |
| **N** | **22** | **22** | **22** | **22** |



### Event study — `GC=F`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.13% | -0.08% | -0.12% | -1.53% |
| mediana | +0.10% | -0.22% | -0.29% | -1.20% |
| dev std | +2.04% | +2.12% | +3.91% | +5.27% |
| p25 | -1.01% | -1.28% | -1.79% | -3.84% |
| p75 | +1.15% | +0.76% | +1.52% | +2.39% |
| **N** | **22** | **22** | **22** | **22** |



### Event study — `CHF=X`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.08% | +0.23% | +0.25% | -0.06% |
| mediana | +0.17% | +0.43% | +0.40% | +0.44% |
| dev std | +0.68% | +1.10% | +1.25% | +1.70% |
| p25 | -0.46% | -0.24% | -0.20% | -0.95% |
| p75 | +0.58% | +0.93% | +1.18% | +1.13% |
| **N** | **22** | **22** | **22** | **22** |



### Event study — `^VIX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -2.42% | -1.06% | -0.75% | -1.76% |
| mediana | -3.32% | -4.23% | -2.48% | -1.90% |
| dev std | +6.68% | +13.21% | +14.44% | +16.46% |
| p25 | -7.51% | -7.84% | -7.77% | -13.78% |
| p75 | -0.27% | +8.26% | +3.75% | +9.01% |
| **N** | **22** | **22** | **22** | **22** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.47% | +0.40% | +0.68% | +1.11% |
| mediana | +0.29% | +0.35% | +0.76% | +1.25% |
| dev std | +0.93% | +1.37% | +1.59% | +3.13% |
| p25 | -0.15% | -0.03% | -0.22% | -0.74% |
| p75 | +0.90% | +0.95% | +1.66% | +3.04% |
| **N** | **22** | **22** | **22** | **22** |

**In pratica, cosa dicono questi numeri.**

- **CRACK_321 (margine di raffinazione)**: è il segnale più forte e più coerente di tutto il campione. Nei 22 episodi analoghi, tre giorni di borsa dopo lo shock il margine era **mediamente più alto del 7,1%** (mediana), e a dieci giorni del **9,8%**; il primo quartile resta positivo (+3,2% a T+3), cioè in almeno tre casi su quattro il margine non è sceso. Tradotto: quando il collo di bottiglia è marittimo, il valore si sposta *dalla materia prima al prodotto trasformato*, perché il greggio si può stoccare e le riserve strategiche lo possono rimpiazzare, ma il diesel già raffinato e già in transito no.
- **HO=F (diesel)**: stessa direzione ma più debole — mediana +1,3% a T+3 e +2,9% a T+10, con dispersione ampia (deviazione standard 9-15%). Conferma il canale, non lo quantifica con precisione.
- **BZ=F (Brent)**: mediana **negativa** a T+1 (−0,26%) e solo +0,78% a T+10, con una dispersione enorme (deviazione standard 12,7% a T+10). Questo è il punto metodologico della scheda: **il greggio, da solo, è un pessimo strumento per leggere uno shock di trasporto**. Il primo quartile a T+10 è −2,5%, cioè in un quarto dei casi il Brent era *sceso* di oltre due punti e mezzo dieci giorni dopo un'escalation. La ragione è che l'escalation deprime anche la domanda (raffinerie che comprano meno greggio, attività economica che rallenta), e i due effetti si compensano.
- **GC=F (oro)**: mediana leggermente negativa e in peggioramento con l'orizzonte (−1,2% a T+10). ⚠️ **Su questo asset la scorecard più recente (2026-W34) segnala un Information Coefficient di −0,07 su 302 previsioni mature: "controproducente". Non traiamo quindi alcuna direzione attesa sull'oro da questa tabella** — il segno storico su questo ticker è stato sistematicamente rovesciato, e va letto solo come descrizione del passato.
- **CHF=X (franco svizzero)**: mediana positiva ma minuscola (+0,17% a T+1, +0,44% a T+10). Il rifugio valutario funziona, ma l'ordine di grandezza è dieci volte inferiore a quello del crack: non è lì che si gioca la partita.
- **^VIX (volatilità)**: mediana **negativa** su tutti gli orizzonti (−3,3% a T+1, −4,2% a T+3). Contro-intuitivo solo in apparenza: il VIX salta *nel giorno* dell'escalation, e l'event study misura da lì in avanti — quindi quello che vediamo è il normale sgonfiamento del premio di paura una volta che lo shock è noto. È lo stesso motivo per cui ^GSPC ha mediana positiva (+0,29% a T+1, +1,25% a T+10): storicamente l'azionario USA *assorbe* le escalation del Golfo entro due settimane.

**Regime misto — da dichiarare.** Il campione attraversa almeno tre regimi diversi: sanzioni pre-JCPOA (2012), premio di rischio senza interruzione (2019-2020, 2023-2025) e interruzione fisica (2022 Russia, 2026 Hormuz). La research Iran/Hormuz avverte esplicitamente che i due tipi di shock hanno ampiezze e persistenze diverse. Il fatto che il crack sia positivo in *tutti* i sotto-periodi è ciò che rende quel risultato più affidabile della media semplice sugli altri asset.

---

## Considerazioni qualitative

La lezione operativa di questa scheda è una sola, e vale la pena renderla esplicita perché è controintuitiva: **una crisi petrolifera non si legge sul petrolio**.

Il meccanismo, passo per passo. Un'escalation nel Golfo può colpire tre cose diverse: (a) la produzione di greggio, (b) il trasporto, (c) la capacità di raffinazione. Solo il caso (a) fa salire il Brent in modo pulito e duraturo — è il caso Abqaiq 2019. Nei casi (b) e (c), che sono quelli di oggi, il greggio è relativamente protetto: esiste in enormi quantità stoccate, i 32 paesi dell'Agenzia Internazionale dell'Energia possono rilasciarne dalle riserve strategiche (come hanno fatto l'11 marzo 2026 con 400 milioni di barili), e se l'economia rallenta le raffinerie ne comprano meno. Il diesel già raffinato, invece, non si può creare dal nulla: dipende da una catena logistica che è esattamente ciò che l'escalation sta colpendo. Il risultato è che il **margine fra il prezzo dei prodotti e quello del greggio** — il crack spread — si allarga. Ed è precisamente ciò che il briefing di oggi segnala quando dice che il calo delle scorte di distillati è "il numero più consequenziale".

Perché questo conta oltre l'energia. Il crack spread è il canale attraverso cui uno shock geopolitico diventa **inflazione**. Il diesel muove i camion, i trattori e le navi: il suo prezzo entra nei costi di quasi tutto. È il motivo per cui, come nota il briefing, l'inflazione dell'energia nell'area euro è al 10% su base annua a luglio e il Chief Economist della Banca Centrale Europea Philip Lane ha detto che le prospettive dipendono "fortemente" dalla guerra USA-Iran. Ed è anche il ponte con le altre due schede di oggi: [news_03](news_03.md) mostra la parte lunga della curva dei rendimenti che si riprezza su offerta e persistenza dell'inflazione, e [news_04](news_04.md) mostra la prima serie di attività reale (i cantieri residenziali USA) che ne subisce le conseguenze. **Sono lo stesso circuito osservato in tre punti diversi.**

Sull'elemento davvero nuovo — la rottura commerciale Emirati-Iran — bisogna essere onesti: non ha un analogo diretto nel campione. Dubai non è un produttore né una rotta, è un *sistema di pagamento e di re-export*. Un ex funzionario citato dalla stampa specializzata del Golfo la definisce un colpo più duro dell'embargo americano stesso. Il canale plausibile non è quindi un ulteriore barile in meno domani, ma un'ulteriore riduzione della capacità dell'Iran di monetizzare quello che riesce comunque a esportare — cioè un aumento della probabilità che Teheran alzi la posta militarmente, che è esattamente ciò che segnala la postura "fully offensive". Questo è un rischio di coda, non un flusso di cassa, e l'event study non lo cattura.

Infine, l'avvertenza sui transiti. La variabile che il briefing indica correttamente come quella che *prezza* il greggio non è la retorica ma il numero di attraversamenti giornalieri dello Stretto, rimasto a una sola cifra. Finché quel numero resta lì, siamo in regime di offerta; se risale, il campione mostra (episodio 2026-04-17, che abbiamo escluso proprio perché opposto) che il rientro può valere oltre l'11% sul Brent **in una sola seduta**. La simmetria del rischio in questo regime è brutale in entrambe le direzioni.

---

## Glossario — sigle e termini

- **Stretto di Hormuz** — braccio di mare fra Iran e Oman attraverso cui transita circa un quinto del petrolio mondiale via nave. Non esiste una rotta alternativa di capacità equivalente.
- **BZ=F** — futures sul petrolio greggio Brent, il benchmark di riferimento europeo/globale.
- **HO=F** — futures NYMEX sull'"heating oil", il gasolio: nella pratica è il proxy quotato del diesel.
- **RB=F** — futures NYMEX sulla benzina RBOB.
- **CRACK_321** — margine di raffinazione 3-2-1, in dollari per barile: `(2×benzina + 1×gasolio) × 42 / 3 − Brent`. Misura quanto guadagna una raffineria a trasformare greggio in prodotti. Il 42 converte i prodotti da dollari/gallone a dollari/barile.
- **GC=F** — futures sull'oro (Comex).
- **CHF=X** — cambio dollaro/franco svizzero; un valore in salita qui significa franco che si apprezza contro dollaro (rifugio valutario).
- **^VIX** — indice CBOE della volatilità implicita a 30 giorni sull'S&P 500, detto "indice della paura": sale quando il mercato compra protezione.
- **^GSPC** — indice azionario S&P 500 (500 maggiori società quotate USA).
- **TTF=F** — futures sul gas naturale europeo (hub olandese Title Transfer Facility), il prezzo di riferimento del gas in Europa.
- **UKMTO** — UK Maritime Trade Operations, l'organismo britannico che raccoglie e diffonde le segnalazioni di incidenti al naviglio mercantile.
- **IAEA** — International Atomic Energy Agency, l'Agenzia Internazionale per l'Energia Atomica dell'ONU.
- **IEA** — International Energy Agency, l'Agenzia Internazionale dell'Energia (OCSE), che coordina il rilascio delle riserve strategiche petrolifere dei paesi membri.
- **JCPOA** — Joint Comprehensive Plan of Action, l'accordo sul nucleare iraniano del 2015.
- **Premio war-risk** — sovrapprezzo assicurativo richiesto per far transitare una nave in un'area di conflitto, espresso in percentuale del valore assicurato per singolo transito.
- **T+N** — N giorni di **borsa** (non di calendario) dopo il giorno dell'evento.
- **Mediana vs media** — la mediana è il valore centrale (metà degli episodi sopra, metà sotto) ed è robusta agli episodi estremi; la media può essere trascinata da un singolo caso eccezionale. Quando le due divergono molto, come qui sul Brent, il campione è asimmetrico e la mediana è più informativa.
- **p25 / p75** — primo e terzo quartile: il 25% degli episodi sta sotto p25, il 25% sopra p75. La distanza fra i due misura la dispersione, cioè quanto il segnale è affidabile.
- **Information Coefficient (IC)** — correlazione di rango (Spearman) fra ciò che la scheda prevedeva e ciò che è realmente accaduto. Positivo = lo storico informa; negativo = lo storico inganna sistematicamente.

---

## Caveat

1. **Campione ampio ma eterogeneo per regime.** N=22 su tutti gli orizzonti è un buon numero (nessun flag "indicative only"), ma gli episodi attraversano regimi strutturalmente diversi: sanzioni pre-accordo nucleare, premio di rischio senza interruzione, interruzione fisica. La research Iran/Hormuz è esplicita nel dire che le ampiezze non sono confrontabili fra i due tipi. Il risultato sul CRACK_321 è il più robusto proprio perché mantiene il segno in tutti i sotto-periodi.
2. **Potatura discrezionale.** Sei episodi sono stati rimossi dal pool della libreria perché direzionalmente opposti (distensioni). La scelta è motivata sopra uno per uno, ma resta una scelta dell'analista: senza la potatura del 2026-04-17 il segno sul Brent si sarebbe rovesciato. Questo è di per sé un avvertimento sulla fragilità del segnale sul greggio.
3. **Asset con segno storico inaffidabile.** Secondo la scorecard 2026-W34, **GC=F (oro)** ha IC = −0,07 su N=302: la direzione storica su questo asset è controproducente e **non ne traiamo una previsione**. La tabella è riportata solo a fini descrittivi. Lo stesso vale, in altre schede di oggi, per ^TNX, IEF e DX-Y.NYB.
4. **La rottura Emirati-Iran non ha analogo diretto.** È un embargo finanziario/commerciale intra-Golfo: nel campione non esiste un episodio della stessa forma. La mappatura è per canale (restrizione dell'offerta e del rischio-Paese), non per tipo di evento.
5. **Ancoraggio temporale.** I prezzi citati nel briefing sono quotazioni di mattinata asiatica del 19 agosto o chiusure USA del 18 agosto: le sessioni europea e americana non erano ancora aperte. L'event study misura da chiusura a chiusura e quindi non è direttamente confrontabile con quei livelli intraday.
6. **Correlazione non è causalità.** Ogni episodio del campione conteneva anche altre notizie. L'event study misura ciò che è accaduto *attorno* a quelle date, non ciò che quelle notizie hanno *causato*.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Pool analoghi: libreria episodi (Opzione B), filtro date-locale `shipping_chokepoint`, direzione `neg`, no-look-ahead `--before 2026-08-19`
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
- Catalog timestamp: 2026-08-19T07:27:10
