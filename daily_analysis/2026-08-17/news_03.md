# Credito cinese in contrazione record (-340 mld yuan a luglio) mentre lo yuan offshore e' ai massimi da 3 anni e mezzo

**Data analisi**: 2026-08-17
**Fonte**: Morning Briefing 2026-08-17 (fin 02 + fin 03 + fin 08)
**Slug**: china-credit-contraction-activity

---

## Testo notizia (originale)

> I nuovi prestiti in yuan di luglio sono risultati -340 miliardi contro un consenso di +45 miliardi: sorpresa negativa di quasi 400 miliardi e contrazione piu' profonda mai registrata nella serie, cioe' rimborsi e scadenze superiori ai nuovi finanziamenti. Il credito alle famiglie (mutui inclusi) cala di 460,3 miliardi dopo +264,6 a giugno; quello alle imprese -130 miliardi dopo +1,5 trilioni. Il cumulato gennaio-luglio e' 10,38 trilioni contro 12,87 un anno prima e la crescita dello stock di prestiti rallenta al 5,1%, minimo storico. Oggi escono i dati di attivita' di luglio (consenso: vendite al dettaglio +1,5% a/a, produzione industriale +4,8%, investimenti fissi -5,9% da inizio anno). Nel frattempo lo yuan offshore e' vicino a 6,74 per dollaro, il livello piu' forte da febbraio 2023, e il rendimento del decennale cinese e' intorno a 1,68-1,70%, ai minimi da un anno.

---

## In breve (in parole semplici)

A luglio in Cina il credito bancario si è **ridotto**: famiglie e imprese hanno restituito più prestiti di quanti ne abbiano chiesti di nuovi, per 340 miliardi di yuan netti. Gli economisti si aspettavano un aumento di 45 miliardi. È la contrazione più profonda da quando esiste la serie, ed è la seconda del 2026 — quindi non è un'anomalia stagionale, è una tendenza.

Perché conta: quando famiglie e imprese *rimborsano* invece di indebitarsi, si dice che stanno riparando il bilancio (*balance-sheet repair*). È la condizione in cui la politica monetaria smette di funzionare: la banca centrale può abbassare i tassi quanto vuole, ma se nessuno vuole prendere a prestito, i tagli non si trasmettono all'economia reale. Il Giappone degli anni Novanta è il precedente da manuale. E infatti il rendimento del titolo di Stato cinese a dieci anni è all'1,68% — un livello che non riflette alcuna aspettativa di crescita.

Aggiungiamo il paradosso del giorno: lo yuan è al livello più forte da tre anni e mezzo. Una valuta forte con credito in contrazione e indagini sull'attività sotto la soglia di espansione è una combinazione inusuale, e rende la vita più difficile agli esportatori cinesi proprio quando la domanda interna si ferma.

La domanda che ci poniamo: come si sono mossi yuan, rame, azionario emergente ed europeo dopo shock analoghi sui dati macro cinesi?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | macro_data |
| `sub_themes` | cny, credit_channel, activity_growth |
| `sentiment` | bearish |
| `confidence` | medium |
| `horizon` | 1-5 giorni di trading |

**Motivazione classificazione**: tre notizie del briefing (fin 02, fin 03, fin 08) descrivono lo stesso oggetto — lo stato del ciclo del credito e della domanda in Cina — e sono state consolidate in un'unica scheda. Il tema è `macro_data` perché il fatto generatore è la pubblicazione di dati con consenso e sorpresa misurabili (i prestiti di luglio; i dati di attività attesi in giornata). Il sentiment è `bearish`: una contrazione record del credito è un segnale di domanda interna che si ferma. La `confidence` è **medium** perché una parte dell'informazione (i dati di attività di luglio) **non è ancora pubblicata** al momento della scheda — il briefing riporta il consenso, non il dato, e la sorpresa rispetto a quel consenso è ciò che muoverà i prezzi.

---

## Asset rilevanti

### Primary (canale diretto)
- **CNY=X** (cambio dollaro/yuan onshore — quanti yuan per un dollaro; se il numero *scende*, lo yuan si rafforza) — è il termometro diretto della politica economica cinese e delle aspettative su di essa.
- **HG=F** (futures sul rame, Comex) — il rame è il "termometro della crescita globale": è l'input industriale per eccellenza e la Cina ne assorbe circa metà della domanda mondiale.

### Secondary (effetti indiretti)
- **EEM** (ETF iShares MSCI Emerging Markets, azionario dei mercati emergenti) — la Cina pesa attorno a un quarto/terzo dell'indice, e il resto degli emergenti dipende dalla domanda cinese di materie prime.
- **^STOXX50E** (indice azionario Euro Stoxx 50) — il canale europeo è specifico: lusso e automobili quotate nell'area euro hanno una quota rilevante di ricavi in Cina, quindi un consumatore cinese che smette di comprare arriva direttamente agli utili europei.
- **^GSPC** (indice azionario S&P 500) — canale di risk-off globale, più diluito.

---

## Knowledge Base — research correlate

- [score=6] `PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/...md` — *PBOC e politica economica cinese*
  - Perché è rilevante: è la research dedicata proprio a questo canale — banca centrale cinese, crisi immobiliare, canale del credito, spillover su emergenti e materie prime — e definisce le fasi di regime usate sotto.
- [score=5] `dati_macro_USA_e_trasmissione_ai_mercati_(2013–2024)/...md` — *Sorprese sui dati macro e trasmissione ai mercati*
  - Perché è rilevante: fornisce la meccanica generale della trasmissione sorpresa → prezzo e il concetto di *state-dependence*.
- [score=1] `Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)/...md`
  - Perché è rilevante: il briefing segnala export +23,1% e import +26,4% con "front-running" dei dazi (cioè spedizioni anticipate per battere l'entrata in vigore delle tariffe) — un effetto che distorce i dati cinesi di commercio estero e va scontato nella lettura.

---

## Regime storico identificato

- **Regime**: `current_regime_2025_2026` (2025-07-01 → oggi), dalla research PBOC.
- **Caratterizzazione**: dopo la fase di stimolo aggressivo del settembre 2024, la Cina è entrata in un regime in cui le misure di allentamento diventano progressivamente meno efficaci. La crisi immobiliare ha lasciato famiglie con patrimonio immobiliare svalutato e imprese con debito da smaltire; entrambe rispondono ai tagli dei tassi rimborsando anziché indebitandosi. È la definizione operativa di *balance-sheet recession* — recessione da bilancio. Gli indicatori del giorno lo confermano tutti insieme: prestiti in contrazione, PMI manifatturiero a 49,2 (sotto 50 = attività in contrazione, prima volta da febbraio), PMI non manifatturiero a 49,0, rendimento decennale all'1,68%.

---

## Event study

### Episodi storici analoghi selezionati

Pool dalla libreria (Opzione B), filtro sul sotto-tema `cny`, direzione negativa, no-look-ahead:

```bash
venv/bin/python analogues.py find --theme macro_data --subtheme cny \
  --direction neg --before 2026-08-17
# [13 episodi · sotto-tema 'cny' su etichette date-locali: 13 episodi]
# [direzione 'neg' stretta dava solo 8 episodi (<12) → incluso mixed/sconosciuto]
```

Le 13 date coprono shock e svolte sul complesso cinese: lo stimolo e i tagli del gennaio 2022 (`2022-01-17`), la fase di yuan debole dell'estate-autunno 2022 (`2022-08-15`, `2022-09-28`), i tagli del 2023 (`2023-06-13`, `2023-08-15`), il pacchetto di stimolo aggressivo del settembre 2024 (`2024-09-24`), l'elezione americana e l'inizio della seconda ondata di dazi (`2024-11-07`, `2024-12-31`), l'escalation tariffaria dell'aprile-maggio 2025 (`2025-04-08`, `2025-05-07`) e le sedute di fine 2025 (`2025-10-20`, `2025-12-24`, `2025-12-30`).

**Nota sulla qualità del filtro**: la diagnostica avverte che la direzione "neg" stretta dava solo 8 episodi, sotto la soglia minima, quindi il filtro ha incluso anche episodi a direzione mista o non etichettata. Il pool contiene perciò sia shock negativi sia annunci di stimolo (che sono positivi per il rischio). È il limite principale di questa scheda ed è dichiarato nei caveat.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'CNY=X,HG=F,EEM,^STOXX50E,^GSPC' \
  --events 2022-01-17,2022-08-15,2022-09-28,2023-06-13,2023-08-15,2024-09-24,2024-11-07,2024-12-31,2025-04-08,2025-05-07,2025-10-20,2025-12-24,2025-12-30 \
  --windows 1,3,5,10 \
  --markdown
```

### Risultati

**`CNY=X` — cambio USD/CNY** (N=13) — *un valore positivo = yuan più debole*

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.06% | -0.03% | -0.07% | +0.23% |
| mediana | **+0.00%** | **-0.01%** | **-0.15%** | **-0.01%** |
| dev std | 0.29% | 0.43% | 0.56% | 0.75% |

**`HG=F` — rame** (N=13)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.28% | +1.96% | +2.38% | +2.77% |
| mediana | **+0.06%** | **+2.25%** | **+2.39%** | **+1.21%** |
| dev std | 1.96% | 3.51% | 4.23% | 5.92% |
| p25 | -1.20% | +1.02% | +1.42% | -0.07% |
| p75 | +1.16% | +3.44% | +2.85% | +4.91% |

**`EEM` — azionario emergenti** (N=13)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.04% | +0.87% | +0.86% | +1.27% |
| mediana | **-0.14%** | **+0.85%** | **+1.44%** | **+1.33%** |
| dev std | 2.30% | 3.17% | 3.87% | 4.49% |
| p25 | -1.05% | -1.00% | -1.31% | -2.18% |
| p75 | +0.43% | +2.37% | +3.34% | +3.47% |

**`^STOXX50E` — Euro Stoxx 50** (N=13)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.01% | +0.81% | +0.73% | +1.18% |
| mediana | **+0.10%** | **+0.28%** | **+0.53%** | **+0.17%** |
| dev std | 1.53% | 1.79% | 2.92% | 3.80% |

**`^GSPC` — S&P 500** (N=13)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.44% | +0.54% | +0.47% | +0.46% |
| mediana | **-0.03%** | **+0.08%** | **-0.08%** | **+0.44%** |
| dev std | 2.82% | 2.76% | 3.36% | 3.34% |

---

## Considerazioni qualitative

**Lo yuan non si muove, ed è il dato più informativo della tabella.** Le mediane su `CNY=X` sono praticamente zero a tutti gli orizzonti (fra −0,15% e +0,00%) con dispersione fra 0,3% e 0,75%. Non è un caso: il cambio onshore è gestito dalla banca centrale cinese attraverso il *fixing* giornaliero, la parità centrale attorno a cui il cambio può oscillare entro una banda. Il messaggio non è "lo yuan non reagisce ai fondamentali" ma "lo yuan riflette una decisione di policy, non un prezzo di mercato". Da qui la stranezza segnalata dal briefing: yuan ai massimi da tre anni e mezzo con credito in contrazione significa che il movimento viene dal lato dollaro (dollaro debole per la Fed che rinvia — vedi `news_04.md`) e dal conto capitale, non dalla forza dell'economia cinese. **Conseguenza operativa**: uno yuan forte tende le condizioni finanziarie degli esportatori cinesi — i loro prodotti costano di più in valuta estera — proprio quando la domanda interna sta deleveraggiando, e toglie a Pechino l'arma della svalutazione competitiva come compensazione se i dati di oggi deludono.

**Rame ed emergenti: mediane positive, ma il pool è contaminato.** `HG=F` mostra mediana **+2,25% a T+3** e **+2,39% a T+5**; `EEM` mediana **+1,44% a T+5** e **+1,33% a T+10**. Preso alla lettera, direbbe che dopo shock sul complesso cinese rame ed emergenti *salgono*. La spiegazione è però meccanica: il pool contiene annunci di stimolo (24 settembre 2024, quando la Cina annunciò il pacchetto più aggressivo dal 2020: rame +2,52% a T+3, EEM +2,37%) e la tregua tariffaria dell'aprile 2025 (`2025-04-08`: rame +9,21% a T+3, EEM +8,39%). Sono episodi *positivi* per il rischio, entrati perché il filtro di direzione stretta non aveva abbastanza osservazioni. Non si può quindi leggere queste mediane come "risposta a una cattiva notizia cinese": leggono piuttosto "risposta a una notizia rilevante sul complesso cinese, di segno misto".

**Ciò che il pool dice comunque.** Anche accettando la contaminazione, c'è un'informazione utile: il rame ha p25 **positivo a T+3 (+1,02%) e a T+5 (+1,42%)**, cioè persino nel quarto peggiore dei casi non è sceso in quella finestra. E EEM è marcato **✅ affidabile** nella scorecard corrente (IC +0,17, hit-rate 62% su 58 previsioni) — è uno degli asset su cui il nostro processo prevede meglio. La lettura prudente è: storicamente, quando la Cina finisce sulle prime pagine, la reazione tende a essere costruttiva sugli asset ciclici perché il mercato inizia subito a prezzare la *risposta di policy* invece del dato. In un regime di *balance-sheet repair*, però, quella scommessa è esattamente quella che ha smesso di pagare — ed è la tensione centrale della giornata.

**Il canale europeo è quello meno visibile nei numeri e più rilevante nella sostanza.** `^STOXX50E` ha mediane piccole e positive (+0,53% a T+5, +0,17% a T+10) con dispersione 3-4%: nessun segnale. Ma il meccanismo economico esiste ed è forte — lusso e automobili dell'area euro hanno una quota importante di ricavi in Cina, e un calo delle vendite al dettaglio cinesi arriva agli utili europei nel giro di uno o due trimestri. È un effetto che opera sull'orizzonte degli utili, non su quello di 1-10 giorni che l'event study misura. La scorecard marca `^STOXX50E` ✅ affidabile (IC +0,16), quindi l'assenza di segnale qui è informativa: davvero non c'è reazione di breve.

**Cosa guardare oggi.** I dati di attività di luglio escono in giornata. Il consenso è: vendite al dettaglio +1,5% anno su anno, produzione industriale +4,8% (in rallentamento dal +5,3% di giugno), investimenti fissi −5,9% da inizio anno. Le vendite al dettaglio sono la variabile chiave: se mancano il consenso, confermano che famiglie *e* imprese stanno deleveraggiando contemporaneamente, che è la configurazione da cui non si esce con la politica monetaria. E arriverebbe nel momento in cui la Fed ha smesso di prezzare un rialzo, rendendo la domanda cinese una **seconda fonte indipendente di disinflazione globale** — cioè, paradossalmente, una ragione in più perché la Fed non alzi. Da tenere presente anche la distorsione segnalata dal briefing: export +23,1% e import +26,4% sono gonfiati dal *front-running* dei dazi (spedizioni anticipate per battere le tariffe), quindi il commercio estero cinese oggi sovrastima la domanda sottostante.

---

## Glossario — sigle e termini

- **PBOC** (*People's Bank of China*) — la banca centrale cinese.
- **Nuovi prestiti in yuan** (*new yuan loans*) — flusso mensile netto di credito bancario: erogazioni meno rimborsi. Un valore negativo significa che si è rimborsato più di quanto si sia preso a prestito.
- **Balance-sheet recession / repair** — situazione in cui famiglie e imprese danno priorità alla riduzione del debito rispetto a nuovi investimenti e consumi; in questa fase i tagli dei tassi non si trasmettono all'economia reale.
- **PMI** (*Purchasing Managers' Index*, indice dei direttori acquisti) — indagine mensile fra i responsabili acquisti delle imprese. Sopra 50 = attività in espansione, sotto 50 = in contrazione.
- **Fixing** — la parità centrale giornaliera fissata dalla PBOC attorno a cui lo yuan onshore può oscillare entro una banda; rende il cambio uno strumento di policy più che un prezzo di mercato.
- **CNY=X** — cambio USD/CNY (yuan **onshore**, quello scambiato in Cina continentale). Numero che **scende** = yuan che si **rafforza**. NB: il briefing cita lo yuan *offshore* (CNH, scambiato a Hong Kong) a 6,74; il DB contiene l'onshore, che si muove in modo molto simile ma non identico.
- **HG=F** — futures sul rame (Comex), proxy della domanda industriale globale.
- **EEM** — ETF iShares MSCI Emerging Markets, azionario dei mercati emergenti.
- **^STOXX50E** — indice azionario Euro Stoxx 50.
- **^GSPC** — indice azionario S&P 500.
- **Investimenti fissi** (*fixed-asset investment*) — spesa in infrastrutture, immobili e impianti; in Cina è storicamente il principale motore della crescita.
- **Front-running dei dazi** — anticipare le spedizioni prima dell'entrata in vigore di una tariffa, che gonfia temporaneamente i dati di commercio estero e li sgonfia nei mesi successivi.
- **IC (Information Coefficient)** — correlazione fra direzione prevista e realizzata; negativo = previsione sistematicamente rovesciata.

---

## Caveat

- **Filtro di direzione degradato.** La diagnostica della libreria segnala esplicitamente che la direzione "neg" stretta dava solo 8 episodi (sotto la soglia di 12), quindi il pool include episodi a direzione mista o non etichettata — fra cui annunci di stimolo e tregue tariffarie, che sono *positivi* per il rischio. Le mediane positive su rame ed emergenti riflettono in buona parte questi, non una reazione a cattive notizie. È il limite più serio di questa scheda.
- **N=13**: sopra la soglia dei 10 episodi, quindi la scheda non è classificata "INDICATIVE ONLY", ma resta un campione piccolo: quartili e mediana sono determinati da poche osservazioni e un singolo episodio estremo (l'8 aprile 2025) sposta visibilmente le medie.
- **Parte dell'informazione non è ancora pubblicata.** I dati di attività di luglio escono in giornata: il briefing riporta il *consenso*, non il dato. L'event study è quindi condizionato a uno shock che potrebbe non materializzarsi (se il dato esce in linea) o essere di segno opposto (se sorprende al rialzo).
- **`CNY=X` è un prezzo amministrato.** Le mediane vicine a zero non misurano l'assenza di impatto economico ma la gestione del cambio da parte della PBOC. Inoltre il DB contiene lo yuan **onshore**, mentre il briefing cita l'**offshore** (CNH): sono due prezzi correlati ma distinti, e proprio il divario fra i due è uno degli indicatori di pressione più usati.
- **Distorsione da front-running dei dazi** sui dati di commercio estero cinesi: export +23,1% e import +26,4% non riflettono la domanda sottostante.
- **Regime non ripetuto.** La *balance-sheet recession* è per definizione un episodio raro e prolungato: gli analoghi degli ultimi quattro anni appartengono in gran parte a fasi in cui lo stimolo funzionava ancora. Il campione non contiene molti casi in cui la trasmissione monetaria era già rotta.
- Correlazione ≠ causazione.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-16T19:11:12
- Scorecard consultata: `daily_analysis/_scorecard/2026-W33.md`, sezione 5-bis
