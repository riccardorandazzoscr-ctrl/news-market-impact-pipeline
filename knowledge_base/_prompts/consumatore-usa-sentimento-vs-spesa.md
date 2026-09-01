# Prompt di deep research — Consumatore USA: sentimento dichiarato, spesa realizzata e anticipo sul mercato del lavoro

## Metadati della richiesta (per noi, NON parte del prompt)

- **Lacuna che chiude:** «Il divario fra sentimento dichiarato e spesa realizzata del consumatore USA. Fra il 2022 e il 2024 l'indice University of Michigan ha segnalato ripetutamente un consumatore in condizioni peggiori che nel 2008 mentre la spesa reale cresceva, per ragioni attribuite alla polarizzazione politica delle risposte e alla sensibilità del sondaggio ai prezzi più visibili. Con `XLY`/`XLP`/`XRT` in DB dal 2026-08-27 il canale è ora misurabile ma non documentato: sappiamo leggere il rapporto `XLY`/`XLP`, non sappiamo quanto pesare il sondaggio che lo dovrebbe muovere.» (29/08, lacuna 5) — unita alla formulazione del 26/08: «manca una research sul canale fiducia dei consumatori → mercato del lavoro … né sulla divergenza fra Present Situation e Expectations».
- **Segnalata il:** **quattro ricorrenze** — 2026-08-14 (lacuna 3, «nessuno studio KB sul ciclo del consumatore americano … la lacuna più rilevante da colmare»), 2026-08-26 (lacuna 4), 2026-08-28 (lacuna 3, «l'asset c'è ora, il pool no»), 2026-08-29 (lacuna 5). ⚠ L'analisi le ha marcate quasi tutte come "prima segnalazione": il campo ricorrenza è inaffidabile, questo conteggio viene da `grep` sugli `_index.md`.
- **Tema canonico di destinazione:** `macro_data`
- **Asset in DB che lo studio deve poter servire:** `XLY`, `XLP`, `XRT` (in DB dal 2026-08-27, sono il cuore dello studio), `^GSPC`, `^NDX`, `IWM` (small cap, in DB dal 2026-08-29), `^TNX`, `^FVX`, `^VIX`, `IEF`, `DX-Y.NYB`, `GC=F`, `HYG`, `IYT`, `XLV`, `^MOVE`
- **Asset citabili ma NON in DB:** `^IRX` (3 mesi), indici di traffico retail o dati di spesa con carta (Chase/BAC card spending) — la serie che misurerebbe *direttamente* il divario oggetto dello studio.
- **Perché serve la research e non basta la tassonomia:** `consumer` ha **8 episodi date-locali** su `macro_data` (misurato il 27/08) — sotto la soglia di 12, quindi `find --subtheme consumer` degrada al livello documento e restituisce un pool generico. `activity_growth` (47 locali) mescola indagini di sentimento, PMI e dati di occupazione, che hanno relazioni molto diverse con i consumi effettivi. Non mancano le etichette: mancano gli **episodi datati**. Verificato con `pipeline_tools.py match`: nessuno studio dedicato, vincono le due research macro USA generiche solo per `primary_theme` + asset, con **zero** hit di keyword.
- **Nota sul formato:** questo prompt chiede il verso in forma **canonica** (`pos`/`neg`/`neutral`) in una colonna dedicata. Motivo: la research sulle raffinerie (eseguita il 27/08) ha una colonna "Direzione attesa" in prosa (`CRACK_321 ↑ / HO=F ↑`) che `analogues.py` **non** sa leggere, quindi quei 21 episodi non alimentano il livello di filtro forte `directions_declared` e restano esposti all'euristica. Con la colonna canonica il problema non si pone.

---

## PROMPT (da incollare)

Sei un ricercatore quantitativo. Produci uno studio storico in **italiano**, in Markdown, su:

**Il consumatore statunitense: sentimento dichiarato, spesa realizzata e anticipo sul mercato del lavoro — regime ed episodi storici (2000–2026)**

### Contesto d'uso (vincolante)

Lo studio alimenta una pipeline di *event study*: un sistema che, data una notizia odierna, cerca episodi storici analoghi e misura i rendimenti cumulati degli asset a T+1, T+3, T+5, T+10 giorni di trading. Quindi:

- il valore dello studio sta nelle **date puntuali** e nei **canali di trasmissione**, non nella narrativa;
- ogni affermazione quantitativa va accompagnata dalla fonte e, se incerta, dichiarata tale;
- niente raccomandazioni operative, niente previsioni: solo statistica descrittiva storica.

### Le tre domande a cui lo studio deve rispondere

**(1) Quanto vale davvero un dato di fiducia, dato che il sondaggio e la spesa divergono?** È la domanda centrale. Fra il 2022 e il 2024 l'indice University of Michigan ha segnalato ripetutamente un consumatore in condizioni peggiori che nel 2008, mentre la spesa reale delle famiglie continuava a crescere. Le spiegazioni proposte in letteratura sono almeno tre — polarizzazione politica delle risposte (l'orientamento partitico dell'intervistato che predice il giudizio più della sua condizione economica), sensibilità sproporzionata ai prezzi più *visibili* (benzina, generi alimentari) rispetto al paniere effettivo, e cambiamenti metodologici nella rilevazione (il passaggio del Michigan da telefono a web nel 2024). Lo studio deve dire **quale peso dare al sondaggio oggi**, e soprattutto **se e quando la sua reazione di prezzo si è staccata dal suo contenuto informativo**: al sistema serve sapere se un crollo di fiducia muove i mercati anche quando non predice nulla.

**(2) L'Expectations Index anticipa le serie sul mercato del lavoro?** Con quale ritardo, con quale affidabilità, e in quali regimi la relazione si rompe. Va trattata come domanda empirica con risposta datata, non come luogo comune: l'indice ha prodotto falsi allarmi (2011, 2022) e va detto quali e perché. Il *labour differential* del Conference Board («jobs plentiful» meno «jobs hard to get») è la serie più direttamente confrontabile con i dati di occupazione: usalo come ponte.

**(3) Cosa fa il mercato quando i due sotto-indici DIVERGONO?** Il Conference Board pubblica un *Present Situation Index* e un *Expectations Index*; il Michigan ha una struttura analoga (*Current Conditions* / *Consumer Expectations*). Il caso di interesse è quello osservato il 2026-08-25: Present Situation **in salita** (+6,8 punti) ed Expectations **in caduta** (−5,8 punti, a 68,2). Questa configurazione a forbice è statisticamente distinta da un calo generalizzato, e va isolata.

Distingui esplicitamente il canale **Conference Board** da quello **Michigan**: escono in giorni diversi, hanno reazioni di prezzo diverse, e il secondo porta anche le *aspettative di inflazione* a 1 e 5-10 anni, che nel 2025-2026 sono diventate una variabile di policy a sé (il 2026-08-28 il preliminare di agosto è uscito a 51,0 contro 54,5 attesi con aspettative a un anno al 4,3%; la lettura finale del 2026-08-29 a 51,7 da 55,2). Se le due indagini danno segnali opposti nello stesso mese, è un episodio interessante: datalo.

### Struttura richiesta (esattamente queste sei sezioni)

**§1 Sintesi esecutiva.** La tesi centrale in 3-5 punti. Dichiara esplicitamente **dove l'event study è affidabile e dove non lo è**: la fiducia è un dato *soft*, e la sua reazione di prezzo è quasi sempre più piccola di quella di un dato *hard*. Dì quanto, con numeri.

**§2 Tassonomia dei canali di trasmissione.** Un paragrafo per canale, ciascuno come **catena causale esplicita** (`evento → meccanismo → variabile → prezzo`), indicando gli asset-proxy fra: `XLY`, `XLP`, `XRT`, `IWM`, `^GSPC`, `^NDX`, `^TNX`, `^FVX`, `^VIX`, `IEF`, `DX-Y.NYB`, `GC=F`, `HYG`, `IYT`, `XLV`, `^MOVE`. Copri come minimo:

- il canale **consumo discrezionale**, che è il cuore dello studio. Trattalo come **rapporto `XLY`/`XLP`**, non come livello: i livelli sono dominati dal beta di mercato e non distinguono un calo di fiducia da un calo dell'indice. Due avvertenze misurate: `XLY` è cap-weighted e dominato da Amazon e Tesla (correla **0,89** con `^GSPC`), quindi da solo non misura il consumatore; `XRT` ha pesi molto più distribuiti (correla 0,76 con `XLY`) ed è il proxy della spesa effettiva nei negozi. **Quando i due divergono dopo un dato di fiducia, quella divergenza è essa stessa il risultato interessante** — dillo e datalo;
- il canale **tassi** (aspettative deboli → attesa di tagli → `^TNX`/`^FVX` giù), e il caso in cui **non funziona** perché la Fed è vincolata dall'inflazione: è la configurazione del 2026, in cui la coda del ciclo è un rialzo e non un taglio;
- il canale **dimensionale** (`IWM` contro `^GSPC`): le piccole capitalizzazioni sono più esposte alla domanda interna e al debito a tasso variabile. Un dato di fiducia debole che *non* muove le attese sui tassi dovrebbe colpirle più dell'indice;
- il canale **credito** (`HYG`), quello **ciclico-reale** (`IYT`) e quello **difensivo** (`XLP`, `XLV`, `GC=F`) come contro-prova della rotazione.

Distingui i canali *direzionali* dai *redistributivi* (che muovono due asset in direzioni opposte) e dagli *amplificatori*. Segnala se un canale ha segno **condizionato al regime di politica monetaria**: è il punto su cui la pipeline sbaglia di più.

**§3 Catalogo di episodi-ancora datati.** Il cuore dello studio. Tabella con **esattamente** queste colonne, in quest'ordine:

`Data (ISO) | Verso | Tipo | Evento | Asset-canale | Note no-look-ahead`

⚠ La colonna **Verso** deve contenere **soltanto** uno di questi tre valori: `pos`, `neg`, `neutral` — nient'altro, nessuna freccia, nessuna prosa, nessun nome di asset. È il verso per l'**azionario di riferimento** (`^GSPC`): un dato di fiducia debole che affossa le azioni è `neg`. Se la giornata è genuinamente ambivalente scrivi `pos, neg`. Ogni sfumatura va nelle altre colonne. (Motivo: un parser legge questa colonna come campo; una direzione in prosa viene scartata e l'episodio perde il suo verso.)

La colonna `Tipo` usa uno di questi valori, che diventeranno le etichette della pipeline:

- `expectations_collapse` — crollo del solo sotto-indice delle attese;
- `divergence_present_up_expectations_down` — la configurazione a forbice;
- `confidence_broad_drop` — calo generalizzato di entrambi i sotto-indici;
- `confidence_rebound` — recupero (serve il verso opposto, altrimenti il pool è tutto negativo e le mediane non sono interpretabili);
- `labour_differential_break` — rottura del differenziale «jobs plentiful − jobs hard to get»;
- `michigan_inflation_expectations` — episodi guidati dalle aspettative di inflazione, non dalla fiducia;
- `sentiment_spending_divergence` — il caso della domanda (1): sondaggio in caduta e spesa che tiene, o viceversa.

Requisiti sulle date, **critici**:
- almeno **20** episodi, distribuiti su tutti e sette i tipi e su tutto l'arco 2000-2026 (non solo post-2020);
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**: le indagini del Conference Board escono alle 10:00 di New York, quindi la seduta è quella stessa; il Michigan preliminare esce alle 10:00 di venerdì. Se la release cade in un festivo o l'orario è cambiato nel periodo, usa la prima seduta utile e **spiegalo nelle Note**;
- **non scegliere date in cui la release di fiducia è stata sovrastata da un evento più grande** (una decisione FOMC, un CPI, il 2008-09-15, i giorni del marzo 2020): un episodio contaminato è peggio di un episodio mancante. Se lo includi comunque, dichiara nelle Note **quale asset usare come controllo**;
- se una data è incerta fra due fonti, riportale entrambe e dichiaralo;
- **una data che NON deve diventare un episodio** (picco di una serie, inizio di una fase) va scritta in forma **non-ISO** ("inizio 2018", "primavera 2022") — la pipeline raccoglie ogni YYYY-MM-DD che trova.

⚠ **Ogni riga deve essere autosufficiente**: la pipeline etichetta ciascun episodio leggendo **solo il testo attorno alla sua data**, non il paragrafo che la introduce. Non scrivere «come il precedente» o «stesso meccanismo»: ripeti tipo e meccanismo su ogni riga. Per lo stesso motivo **non citare due date ISO diverse nella stessa riga o nella stessa frase** se descrivono episodi distinti.

**§4 Statistiche indicative.** Cosa è successo mediamente agli asset dopo gli episodi del §3, **separatamente per ciascun `Tipo`**. Riporta **sempre N**; marca "INDICATIVE ONLY" ogni statistica con N < 10. Includi due confronti espliciti, affiancati in tabella:
- `divergence_present_up_expectations_down` **contro** `confidence_broad_drop` — la forbice è un segnale peggiore del calo generalizzato?
- episodi in cui il sondaggio è crollato **e la spesa successiva ha tenuto**, contro quelli in cui è stato confermato dai dati di spesa: la reazione di prezzo *immediata* sa già distinguerli, o no?

**§5 Fasi di regime.** 2-5 fasi con confini datati, ciascuna con: cosa cambia strutturalmente e **se gli analoghi di quella fase siano usabili nel regime corrente**. Nomi in `snake_case` inglese. Tieni conto almeno di: la rottura post-2020 nel livello assoluto degli indici (mai tornati ai valori pre-pandemia a parità di condizioni reali), la polarizzazione politica delle risposte, il passaggio del Michigan a rilevazione web nel 2024, e il regime 2025-2026 di inflazione persistente con Fed vincolata.

**§6 Caveat metodologici.** Come minimo: il livello assoluto non è confrontabile fra decenni (revisioni del Conference Board, incluso il cambio di base del 2011 e la revisione del campione del 2020 — datali); la fiducia è correlata al prezzo della benzina e all'S&P 500 stesso, quindi **l'indice riflette in parte l'asset che stiamo cercando di prevedere** (endogeneità: dì come si attenua); episodi multi-causa e quale asset usare come controllo; *drift* di fondo se il campione cade in un mercato direzionale; canali con N strutturalmente piccolo; serie citate ma non disponibili; fonti e incertezze residue.

### Blocco di metadati finale (obbligatorio, in coda al file)

Chiudi con un blocco YAML delimitato da tre backtick e la parola `yaml`, in questo formato esatto:

    ---
    title: "Il consumatore statunitense: sentimento dichiarato, spesa realizzata e anticipo sul mercato del lavoro — regime ed episodi storici (2000–2026)"
    date_compiled: <YYYY-MM-DD>
    primary_theme: macro_data
    sub_themes: [consumer, consumer_expectations, sentiment_spending_divergence, expectations_collapse, labour_differential_break, confidence_broad_drop, confidence_rebound, michigan_inflation_expectations, conference_board, soft_data]
    relevant_assets: [XLY, XLP, XRT, IWM, ^GSPC, ^NDX, ^TNX, ^FVX, ^VIX, IEF, DX-Y.NYB, GC=F, HYG, IYT, XLV, ^MOVE]
    external_assets_mentioned:
      - "^IRX — 3 mesi: il tratto di curva che si muove per primo su un dato di fiducia debole"
      - "dati di spesa con carta (Chase/BofA) — misurerebbero DIRETTAMENTE il divario sondaggio/spesa oggetto dello studio"
    time_window:
      start: 2000-01-01
      end: present
    regime_phases:
      - <nome_fase>: <YYYY-MM-DD> to <YYYY-MM-DD|present>
    keywords: [fiducia dei consumatori, consumer confidence, consumer sentiment, expectations index, present situation, aspettative dei consumatori, conference board, university of michigan, jobs plentiful, jobs hard to get, labour differential, soft data, hard data, spesa delle famiglie, consumer spending, retail sales, vendite al dettaglio, recessione, recession signal, aspettative di inflazione, inflation expectations, polarizzazione politica]

### Vincoli di scrittura

- Italiano, prosa densa, niente elenchi puntati dove serve un ragionamento.
- Cifre puntuali sempre con fonte e data; se non verificabile, dillo.
- Nessuna data ISO inventata o approssimata: meglio una data in meno che una sbagliata.

---

## Dopo l'esecuzione (checklist per Claude)

- [ ] research salvata in `knowledge_base/Il consumatore statunitense — sentimento, spesa e mercato del lavoro (2000–2026)/<stesso nome>.md`
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] `venv/bin/python analogues.py labels --theme macro_data` → `consumer` deve salire **sopra 12** episodi date-locali (era 8 il 27/08); i sette `Tipo` del §3 devono comparire come etichette
- [ ] **verificare che la colonna Verso sia stata letta**: `analogues.py stats` → il numero di episodi "con VERSO dichiarato" deve salire di ~20. Se non sale, il parser non ha riconosciuto la tabella (`DECLARED_ROW_RE` si aspetta il verso in **seconda** colonna) → controllare l'ordine delle colonne nel file prima di dare la colpa alla research
- [ ] `venv/bin/python pipeline_tools.py match --theme macro_data --sub-theme consumer --keyword "consumer confidence"` → lo studio esce **primo**
- [ ] event study di confronto: `sentiment_spending_divergence` contro `confidence_broad_drop` su `XLY`/`XLP` — la differenza deve essere visibile nei numeri, non solo nella prosa
- [ ] date spurie? (confini di regime, `date_compiled`, date in prosa) → correggere il .md
- [ ] questo prompt cancellato da `_prompts/`
