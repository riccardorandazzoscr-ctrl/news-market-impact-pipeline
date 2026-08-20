# Scade la tregua USA-Iran con Hormuz ancora chiuso: Brent a 88,50$ dentro un evento binario

**Data analisi**: 2026-08-17
**Fonte**: Morning Briefing 2026-08-17 (intl 01 + intl 02 + fin 05 + One Thing to Watch)
**Slug**: iran-ceasefire-lapse-hormuz

---

## Testo notizia (originale)

> La tregua che inquadrava la guerra con l'Iran da giugno scade lunedi 17 agosto senza proroga annunciata e con il traffico delle petroliere attraverso lo Stretto di Hormuz ancora fermo. Teheran ha irrigidito la posizione nel weekend (il vice ministro degli esteri Gharibabadi: lo stretto 'sara' aperto e chiuso solo su comando iraniano'), mentre Washington prepara un pacchetto di 'isolamento economico'. In parallelo i raid israeliani di sabato nel distretto di Nabatieh (Libano) hanno portato a 11 le vittime e ucciso due comandanti di Hezbollah, restringendo lo spazio diplomatico. Il Brent tiene 88,50 dollari al barile dopo un +6% settimanale; il prezzo medio della benzina USA e' a 4,08 dollari/gallone, +29% su un anno.

---

## In breve (in parole semplici)

Da giugno c'è una tregua che tiene ferma — almeno formalmente — la guerra fra Stati Uniti e Iran. Quella tregua scade oggi, lunedì 17 agosto, e nessuno ha annunciato un rinnovo. Nel frattempo lo Stretto di Hormuz, il corridoio di mare largo poche decine di chilometri fra Iran e Oman da cui passa circa un quinto del petrolio mondiale, resta chiuso al traffico delle petroliere.

Perché conta per i mercati: il petrolio è l'unica variabile che oggi tiene "in equilibrio" due banche centrali. La Federal Reserve (la banca centrale americana) ha appena tolto dal prezzo il rialzo dei tassi di settembre perché l'inflazione sembrava sotto controllo — ma quella scommessa regge solo se l'energia si comporta bene. Il Brent è a 88,50 dollari al barile, la benzina alla pompa negli Stati Uniti è già +29% su un anno.

La domanda che ci poniamo: quando in passato è successo qualcosa di simile — cioè un'escalation su un collo di bottiglia marittimo per il trasporto di greggio — come si sono mossi petrolio, margini di raffinazione, oro, volatilità e indici azionari nei giorni successivi?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | commodity_energy |
| `sub_themes` | shipping_chokepoint, iran, hormuz |
| `sentiment` | risk-off |
| `confidence` | medium |
| `horizon` | 1-5 giorni di trading |

**Motivazione classificazione**: il canale di trasmissione dominante non è diplomatico ma fisico — un collo di bottiglia (*chokepoint*) marittimo chiuso al traffico di greggio. Per questo la notizia è classificata `commodity_energy` e non `geopolitical`: gli asset che reagiscono per primi sono petrolio e prodotti raffinati, non i beni rifugio generici. Il sentiment è `risk-off` perché la scadenza senza proroga sposta la distribuzione dei rischi verso l'alto sul prezzo dell'energia (che per un'economia importatrice è uno shock negativo). La `confidence` è **medium** e non **high** per una ragione precisa: l'evento è *binario e già noto al mercato* — la data di scadenza è pubblica, quindi una parte del rischio è già nei prezzi (il +6% settimanale del Brent), e l'esito può essere tanto un'escalation quanto un annuncio di proroga last-minute.

---

## Asset rilevanti

### Primary (canale diretto)
- **BZ=F** (futures sul petrolio Brent, il greggio di riferimento europeo) — è il prezzo direttamente esposto alla disponibilità fisica del greggio che passa da Hormuz.
- **CRACK_321** (margine di raffinazione 3-2-1, in dollari al barile: quanto guadagna una raffineria trasformando 3 barili di greggio in 2 di benzina e 1 di diesel) — è il canale che si muove quando il problema riguarda *approvvigionamento e logistica* dei prodotti, non solo il greggio.
- **HO=F** (futures sul gasolio/diesel da riscaldamento, il prodotto raffinato più esposto agli shock di offerta) — il diesel è il prodotto che nelle crisi energetiche si tende per primo.
- **GC=F** (futures sull'oro) — bene rifugio classico nelle escalation militari.

### Secondary (effetti indiretti)
- **^VIX** (indice di volatilità implicita sull'S&P 500, il cosiddetto "indice della paura") — misura quanto il mercato azionario si aspetta di muoversi; sale nelle fasi di risk-off.
- **^GSPC** (indice azionario S&P 500, le 500 maggiori società quotate USA) — canale di risk-off generale e, per gli USA, effetto ambiguo: il settore energia guadagna, il resto perde potere d'acquisto.
- **^STOXX50E** (indice azionario Euro Stoxx 50, le 50 blue chip dell'area euro) — l'eurozona è importatrice netta di energia, quindi più esposta al lato negativo di uno shock petrolifero rispetto agli Stati Uniti.

---

## Knowledge Base — research correlate

- [score=8] `iran_hormuz/compass_artifact_wf-57769786-924f-41b7-8c1e-36177b05bebd_text_markdown.md` — *Iran – Stretto di Hormuz e il premio geopolitico sul petrolio: regime ed episodi storici (1980–2026)*
  - Perché è rilevante: è la research che mappa esattamente questo canale — chiusure e minacce di chiusura di Hormuz — e definisce le fasi di regime, inclusa quella corrente (`hormuz_closure_mou_2026`).
- [score=1] `Russia-Ucraina attrito energetico e regime sanzioni .../...md` — *Russia-Ucraina: attrito energetico e regime sanzioni (2022–2026)*
  - Perché è rilevante: fornisce il precedente più recente di **sanzioni + interruzione fisica** che colpiscono i prodotti raffinati più del greggio, utile per leggere il comportamento del `CRACK_321`.

---

## Regime storico identificato

- **Regime**: `hormuz_closure_mou_2026` (2026-02-01 → oggi), dalla research Iran/Hormuz.
- **Caratterizzazione**: dal febbraio 2026 non siamo più nel regime di *minaccia* di chiusura (come nel 2011-2012 o nel 2019 della "massima pressione") ma in quello di **chiusura effettiva e prolungata**. È una differenza sostanziale: quando la chiusura è solo minacciata, il mercato prezza una probabilità; quando è già in atto, il prezzo incorpora già il danno e ciò che si muove è il *margine* di ulteriore escalation o di normalizzazione. Il pool di analoghi che usiamo mescola quindi due sotto-regimi (minaccia vs chiusura in atto) — un limite dichiarato più sotto nei caveat.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla **libreria di episodi** (Opzione B) con filtro forte a livello di etichette date-locali, direzione negativa e vincolo di no-look-ahead (`--before 2026-08-17`). Il tetto di recency della libreria ha tenuto i 30 episodi più recenti su 32 disponibili.

```bash
venv/bin/python analogues.py find --theme commodity_energy --subtheme shipping_chokepoint \
  --direction neg --before 2026-08-17
# [30 episodi · sotto-tema 'shipping_chokepoint' su etichette date-locali: 32 episodi]
```

Gli episodi coprono, in ordine di regime:
- `2012-01-04`, `2012-01-23` — minacce iraniane di chiusura dello stretto durante il round di sanzioni nucleari UE/USA: il precedente storico più vicino come *retorica*, ma senza chiusura effettiva.
- `2014-11-27`, `2015-07-14`, `2016-01-19` — riunioni OPEC e accordo nucleare iraniano (JCPOA): episodi di *offerta in aumento*, inclusi nel pool perché la libreria li marca come shock su chokepoint/flussi.
- `2019-05-12`, `2019-06-13`, `2019-07-01`, `2019-09-14`, `2020-01-08` — attacchi alle petroliere nel Golfo di Oman, attacco agli impianti di Abqaiq in Arabia Saudita, uccisione di Soleimani: la fase di *massima pressione*, il regime più simile per natura del rischio.
- `2022-02-24`, `2022-03-08`, `2022-08-15` — invasione russa dell'Ucraina ed embargo: shock di offerta su scala globale.
- `2023-11-01`, `2023-12-18`, `2024-01-12`, `2024-10-26` — attacchi Houthi nel Mar Rosso e deviazione del traffico dal Canale di Suez: l'analogia più stretta come *meccanica* (chokepoint marittimo, premio sui noli).
- `2025-06-13`, `2025-06-22`, `2026-02-01` → `2026-04-17` — la guerra Israele/USA-Iran corrente e la chiusura di Hormuz: stesso regime, ma con il rischio di sovrappesare un singolo episodio ripetuto.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'BZ=F,CRACK_321,HO=F,GC=F,^VIX,^GSPC,^STOXX50E' \
  --events 2012-01-04,2012-01-23,2014-11-27,2015-07-14,2016-01-19,2019-05-12,2019-05-13,2019-06-13,2019-07-01,2019-09-14,2020-01-08,2022-02-24,2022-03-08,2022-08-15,2023-03-10,2023-11-01,2023-12-18,2024-01-12,2024-10-26,2025-06-13,2025-06-22,2025-06-23,2026-02-01,2026-02-17,2026-02-27,2026-02-28,2026-03-08,2026-03-12,2026-04-11,2026-04-17 \
  --windows 1,3,5,10 \
  --markdown
```

(Due date — `2019-05-13` e `2025-06-23` — sono state scartate automaticamente perché adiacenti ad altre già presenti: N effettivo = 28.)

### Risultati

**`BZ=F` — Brent** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.88% | +1.44% | +2.32% | +3.90% |
| mediana | **-0.46%** | **+1.43%** | **+1.36%** | **+0.78%** |
| dev std | 4.67% | 5.99% | 10.28% | 12.72% |
| p25 | -2.94% | -1.14% | -2.81% | -4.36% |
| p75 | +1.89% | +3.35% | +5.12% | +9.28% |

**`CRACK_321` — margine di raffinazione** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.93% | +8.22% | +6.71% | +10.19% |
| mediana | **+0.56%** | **+5.65%** | **+3.73%** | **+7.65%** |
| dev std | 9.84% | 16.50% | 19.21% | 22.34% |
| p25 | -1.41% | +1.35% | -0.31% | -5.66% |
| p75 | +5.22% | +12.30% | +12.05% | +19.63% |

**`HO=F` — diesel/gasolio** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.57% | +2.95% | +3.20% | +5.77% |
| mediana | **-0.04%** | **+1.29%** | **+1.15%** | **+2.85%** |
| dev std | 5.69% | 9.11% | 12.09% | 14.19% |

**`GC=F` — oro** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.31% | -0.03% | -0.09% | -1.14% |
| mediana | **+0.10%** | **-0.22%** | **-0.29%** | **-1.20%** |
| dev std | 2.02% | 2.17% | 3.84% | 5.17% |

**`^VIX` — volatilità implicita S&P 500** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -1.02% | -1.53% | -0.73% | +0.73% |
| mediana | **-1.90%** | **-4.23%** | **-2.48%** | **-1.55%** |
| dev std | 6.73% | 12.29% | 13.85% | 19.73% |

**`^GSPC` — S&P 500** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.29% | +0.43% | +0.55% | +0.71% |
| mediana | **+0.17%** | **+0.37%** | **+0.70%** | **+1.15%** |
| dev std | 0.91% | 1.23% | 1.64% | 3.21% |

**`^STOXX50E` — Euro Stoxx 50** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.24% | -0.11% | -0.41% | -0.54% |
| mediana | **+0.24%** | **+0.27%** | **+0.03%** | **-0.86%** |
| dev std | 2.21% | 2.28% | 2.69% | 3.84% |

---

## Considerazioni qualitative

**Come si leggono queste tabelle.** T+1, T+3, T+5, T+10 sono i giorni di *borsa* dopo l'evento (non giorni di calendario). Ogni numero è il rendimento cumulato dall'evento a quel giorno. Usiamo la **mediana** più della media perché la media viene distorta da singoli episodi estremi (qui, per esempio, il +42% del Brent a T+10 dopo il 27 febbraio 2026); la mediana dice "nella metà dei casi il risultato è stato peggiore, nell'altra metà migliore". La **deviazione standard** e la distanza fra p25 e p75 (il rendimento che separa il quarto peggiore dal quarto migliore) misurano la dispersione: quando è enorme rispetto alla mediana, il segnale è debole anche se la mediana ha un segno chiaro.

**Il petrolio: mediana positiva ma dispersione che divora il segnale.** Nei 28 episodi analoghi il Brent ha mediana **−0,46% a T+1** e poi **+1,43% a T+3, +1,36% a T+5, +0,78% a T+10**. Il pattern è interessante: nel giorno immediatamente successivo il prezzo scende leggermente più spesso di quanto non salga, poi il premio geopolitico si riaffaccia. La spiegazione plausibile è che questi eventi arrivano quasi sempre *dopo* una corsa dei prezzi (come oggi: +6% nella settimana), quindi la prima reazione è spesso una presa di profitto — il classico "buy the rumour, sell the news". Ma la deviazione standard a T+10 è **12,7%** contro una mediana di **+0,8%**: in pratica il segnale direzionale è quasi nullo, la vera informazione è che *la varianza esplode*. Nel quarto peggiore dei casi il Brent perdeva più del 4% a 10 giorni; nel quarto migliore guadagnava più del 9%.

**Il margine di raffinazione è dove il segnale è più netto.** Il `CRACK_321` ha mediana **+5,65% a T+3** e **+7,65% a T+10**, con il p25 (il quarto peggiore) sopra lo zero a T+3. Il meccanismo è quello descritto nel CLAUDE.md del progetto: quando lo shock riguarda il *trasporto e la raffinazione* più che l'estrazione, il greggio può anche restare fermo mentre i prodotti finiti — benzina e soprattutto diesel — si tendono, perché la scarsità si manifesta a valle. Il diesel (`HO=F`) conferma con mediana **+2,85% a T+10**. Tradotto: se oggi si volesse guardare un solo prezzo per capire se l'escalation è reale, non sarebbe il Brent ma il margine di raffinazione e il gasolio. Ed è anche il canale che porta direttamente al dato che interessa alla Federal Reserve — i 4,08 dollari al gallone alla pompa sono, in ultima istanza, greggio *più* margine di raffinazione.

**L'oro: qui il segno storico non è utilizzabile.** La tabella dà mediane leggermente negative (−1,20% a T+10). Ma la scorecard settimanale corrente (2026-W33, sezione 5-bis) classifica `GC=F` come **❌ controproducente**: hit-rate 47%, IC (information coefficient, la correlazione fra ciò che gli analoghi prevedono e ciò che si realizza) **−0,09** su 270 previsioni mature. Un IC negativo con N grande non è rumore: significa che su questo asset la lettura storica è sistematicamente rovesciata. **Riportiamo la tabella ma non ne traiamo alcuna direzione attesa sull'oro.** Vale la pena notare anche che l'oro è a 4.381 dollari l'oncia dopo un +0,8% settimanale — cioè il rifugio è già stato comprato.

**Volatilità e azionario: la reazione "sbagliata" che si ripete.** Il `^VIX` ha mediana **negativa** a tutti gli orizzonti (−4,23% a T+3): dopo questi eventi la paura misurata sull'S&P 500 tipicamente *scende*. Non è un paradosso — è l'effetto di chiusura dell'incertezza: quando l'evento si materializza (o si scopre che non era la catastrofe temuta), il premio di volatilità comprato prima si sgonfia. Il `^VIX` è peraltro l'asset più affidabile della nostra scorecard (✅, IC +0,27, hit-rate 63% su 83 previsioni), quindi questo è il segnale a cui dare più peso. Coerentemente l'`^GSPC` mostra mediane positive e piccole (+1,15% a T+10, dispersione 3,2%) — l'azionario americano storicamente *non* si spaventa in modo persistente per uno shock su Hormuz, anche perché gli Stati Uniti sono oggi esportatori netti di greggio.

**La differenza fra Stati Uniti ed Europa è la lettura più utile.** L'`^STOXX50E` è l'unico indice con mediana che diventa **negativa a T+10 (−0,86%)** dove l'S&P 500 è positivo. Il motivo è strutturale: l'eurozona importa quasi tutta l'energia che consuma, quindi un rincaro del greggio è un trasferimento di reddito verso l'estero — un peggioramento delle ragioni di scambio. Gli Stati Uniti, che producono, hanno un effetto compensativo interno. L'Euro Stoxx 50 è inoltre marcato ✅ affidabile in scorecard (IC +0,16 su 157 previsioni), quindi questa asimmetria è la conclusione operativa con il supporto statistico migliore della scheda.

**Il collegamento con la politica monetaria.** Il briefing lo formula bene: il petrolio è "l'unica variabile che tiene in piedi due banche centrali". La Fed ha rinviato il rialzo di settembre (69% di probabilità di *hold*, vedi `news_04.md`) sulla base di inflazione benigna e consumi deboli. Se il margine di raffinazione si tende come suggeriscono gli analoghi, la benzina alla pompa sale ancora e la traiettoria d'inflazione che giustificava il rinvio smette di reggere. È il nodo che lega questa scheda alla scheda sulla Fed: non sono due notizie separate, sono due lati della stessa scommessa.

---

## Glossario — sigle e termini

- **Stretto di Hormuz** — braccio di mare fra Iran e Oman, largo circa 33 km nel punto più stretto, attraverso cui transita circa un quinto del petrolio scambiato via mare nel mondo.
- **BZ=F** — futures sul petrolio **Brent**, il greggio di riferimento per Europa, Africa e Medio Oriente.
- **HO=F** — futures sul *heating oil* (gasolio da riscaldamento), usato come proxy del diesel.
- **RB=F** — futures sulla benzina RBOB (il contratto di riferimento USA).
- **CRACK_321** — margine di raffinazione "3-2-1", in dollari al barile: `(2×benzina + 1×diesel) × 42 / 3 − Brent`. Misura quanto guadagna una raffineria; sale quando i prodotti scarseggiano più del greggio.
- **GC=F** — futures sull'oro (Comex), bene rifugio di riferimento.
- **^VIX** — indice CBOE della volatilità implicita a 30 giorni sull'S&P 500, comunemente "indice della paura".
- **^GSPC** — indice azionario S&P 500 (500 maggiori società quotate USA).
- **^STOXX50E** — indice azionario Euro Stoxx 50 (50 blue chip dell'area euro).
- **T+1 / T+3 / T+5 / T+10** — giorni di *borsa* successivi all'evento; il valore è il rendimento cumulato da T+0.
- **IC (Information Coefficient)** — correlazione fra la direzione prevista e quella realizzata; se negativo, la previsione è sistematicamente rovesciata.
- **Chokepoint** — collo di bottiglia geografico del commercio marittimo (Hormuz, Suez, Malacca, Panama).
- **Risk-off** — fase in cui gli investitori riducono l'esposizione ad attività rischiose e comprano beni rifugio.
- **JCPOA** — *Joint Comprehensive Plan of Action*, l'accordo sul nucleare iraniano del 2015.

---

## Caveat

- **Mixing di regimi, dichiarato.** Il pool di 28 episodi copre quattro fasi strutturalmente diverse: minaccia di chiusura senza chiusura (2012), attacchi a petroliere e impianti (2019-2020), shock di offerta russo (2022), premio Mar Rosso (2023-2024) e chiusura effettiva di Hormuz (2026). La capacità inutilizzata dell'OPEC, la posizione degli Stati Uniti come produttore e il livello dei tassi reali erano molto diversi in ciascuna. La mediana aggrega contesti che non sono intercambiabili.
- **Sovrappeso dell'episodio corrente.** Nove delle 28 date appartengono al 2026, cioè alla *stessa* crisi che stiamo analizzando. Questo gonfia artificialmente la coerenza del pool: non sono osservazioni indipendenti, sono capitoli dello stesso evento.
- **Dispersione superiore al segnale su BZ=F.** Con deviazione standard 12,7% contro mediana +0,8% a T+10, la direzione attesa sul Brent va considerata di fatto non informativa. La scorecard corrente marca `BZ=F` come ⚠️ debole (IC +0,10, copertura 24%).
- **`GC=F` (oro): segno storico inaffidabile** — asset marcato ❌ controproducente nella scorecard 2026-W33. Nessuna direzione attesa viene tratta.
- **`CRACK_321` e `HO=F` non compaiono nella scorecard** perché hanno meno di 50 previsioni mature: il loro segnale non è ancora stato validato out-of-sample. Trattarlo come ipotesi, non come regolarità confermata.
- **Evento binario e parzialmente prezzato.** La data di scadenza è pubblica: il +6% settimanale del Brent indica che una parte del rischio è già nei prezzi. Gli event study misurano la reazione a *sorprese*; qui la sorpresa non è l'evento in sé ma il suo esito (proroga vs escalation).
- Correlazione ≠ causazione: le date raccolgono ciò che accadeva *anche* per altre ragioni negli stessi giorni.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-16T19:11:12
- Scorecard consultata: `daily_analysis/_scorecard/2026-W33.md`, sezione 5-bis
