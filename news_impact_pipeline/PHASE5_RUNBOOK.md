# Fase 5 — Runbook orchestrazione giornaliera

Procedura che l'agente Claude esegue (manualmente o via `/schedule`) per
processare il morning briefing del giorno e produrre le schede di analisi.

## Input

- Briefing HTML in `~/Claude/mercati_finanza/morning brief/YYYY-MM-DD-morning-briefing.html`
  (N notizie: fino a 10 International e fino a 10 Economics & Finance, + 1 "One Thing to Watch").
- DB mercati in `market_data/market_data.db`.
  ⚠ **L'elenco degli asset NON è scritto qui.** L'unica fonte autorevole è
  `category_asset_map.yaml` (o `pipeline_tools.py list-categories`), che cresce nel
  tempo. Duplicarlo nel runbook lo rendeva stale — questo file ha detto "46 asset"
  fino al 2026-08-21, quando erano 66 — e la copia stale costringeva a rileggere
  comunque lo YAML ogni mattina. Leggi lo YAML **una volta sola** a inizio run, in
  fase di triage, e tienilo a mente per il resto della sessione.

  Le uniche regole di scelta asset che NON si deducono dallo YAML, e che quindi
  stanno qui:
  - **Attacchi/fermi di raffineria e terminali → `CRACK_321` e `HO=F`, non `BZ=F`.**
    Quegli shock colpiscono prodotti e margine; il greggio può perfino *scendere*
    (meno domanda di input) mentre il diesel sale.
  - **Sud-Est asiatico → i 7 proxy ASEAN**, non il solo `EEM`, troppo diluito.
  - **Se il DB risulta vuoto**: `bootstrap_market_data.py`; spread BTP-Bund via
    `fetch_daily_spread.py`, crack via `compute_crack_spread.py`.

## Output

- `~/Claude/mercati_finanza/daily_analysis/YYYY-MM-DD/_index.md` — digest di triage (tutte le N
  notizie con decisione ✅/✖ + motivazione + link alle schede).
- `~/Claude/mercati_finanza/daily_analysis/YYYY-MM-DD/news_NN.md` — una scheda completa per ogni
  notizia tenuta (subset triato: tipicamente 3-6/giorno).

## Economia del run (VINCOLANTE — leggi prima di iniziare)

Il costo di un run cresce **col quadrato del numero di turni**: ogni chiamata di
tool rilegge l'intero contesto accumulato, e il cache-read è l'85% della spesa.
Non si risparmia scrivendo di meno o peggio, si risparmia **facendo meno giri**.
Misure, cronologia degli interventi e proposte aperte:
[references/economia_del_run.md](../references/economia_del_run.md).

Tre regole, in ordine di impatto:

1. **Il CONTENUTO di ogni file lo scrivi UNA VOLTA SOLA, in un unico passaggio.**
   Questo non vieta lo scaffold deterministico (`new-card` crea `news_NN.md`
   pre-popolato di placeholder in un proprio passaggio, separato): vieta di
   rigenerare il corpo a pezzi, sezione per sezione, turno dopo turno. Prima di
   scrivere una scheda, **raccogli tutto**: pool di episodi potato, event study,
   research KB, sezione 5-bis della scorecard. Poi riempi lo scaffold con un solo
   Edit che sostituisce tutti i placeholder in blocco. Se dopo devi correggere,
   altro Edit chirurgico sulla stringa da cambiare — mai un heredoc che rigenera
   il corpo.
2. **Non rileggere ciò che hai appena scritto per certificarla tu.** Niente
   `cat`/`sed -n` sulla scheda che hai appena generato: se la scrittura non fosse
   riuscita avresti avuto un errore. Questo non vuol dire "nessuna verifica di
   contenuto" — quella esiste, mai a carico dell'agente che scrive: i guardiani
   strutturali a valle (`run_daily_analysis.sh`, le sei fasi di `stato_giornata.py`)
   controllano corrispondenza con le notizie in ingresso, esistenza delle schede e
   link, dopo che il run è finito.
3. **Non lanciare `--help`.** I flag che servono sono documentati sotto.

Nessuna di queste regole tocca il contenuto delle schede: stesso output, meno giri.

## Riferimento comandi (per non lanciare `--help`)

```bash
# 1. digest di triage → scaffold _index.md
venv/bin/python pipeline_tools.py digest --date AAAA-MM-GG [--force]

# 2. asset per tema · research KB correlate
venv/bin/python pipeline_tools.py assets <theme> [--level primary|secondary]
venv/bin/python pipeline_tools.py match --theme <t> --keyword <k> --asset <ticker>
venv/bin/python pipeline_tools.py list-categories

# 3. scaffold scheda (auto-numera news_NN.md)
venv/bin/python pipeline_tools.py new-card --date AAAA-MM-GG --slug <slug> \
  --title "<titolo>" --source "Morning Briefing AAAA-MM-GG" --theme <theme> \
  --sub-theme <tok> --sentiment <hawkish|dovish|bullish|bearish|risk-on|risk-off|neutral> \
  --confidence <low|medium|high> --horizon "<es. 1-5 giorni>" --text "<testo notizia>"
#   --sub-theme è ripetibile.

# 4. pool di analoghi dalla libreria
venv/bin/python analogues.py find --theme <t> [--subtheme <tok>]... \
  [--direction pos|neg|neutral --direction-reference TICKER] \
  [--before AAAA-MM-GG] [--min-n N] [--max-pool N] \
  [--match-all]
#   --subtheme ripetibile · --max-pool default 30 (0 = nessun tetto)
#   --min-n = soglia sotto cui il filtro sotto-tema NON viene applicato
#   --match-all = più --subtheme in INTERSEZIONE (default: unione). Obbligatorio
#     quando uno dei token è GEOGRAFICO (eurozone_release, japan_release,
#     britain_release): in unione il token geografico non filtra nulla e il pool
#     si riempie di release di altre aree. Leggi sempre la nota su stderr: se
#     dichiara il degrado "a livello di documento", l'intersezione NON è garantita.
venv/bin/python analogues.py labels --theme <t>    # copertura per token
venv/bin/python analogues.py stats                 # adozione blocchi dichiarati

# 5. event study
venv/bin/python event_study.py --ticker 'T1,T2' --events <date CSV> \
  --windows 1,3,5,10 --markdown [--detail] [--no-adj]
#   --detail aggiunge la tabella per-episodio: pesa l'80% dell'output e nelle
#   schede non si incolla mai. Chiedilo SOLO per potare il pool o cacciare outlier.
```

## Procedura (tutti i comandi dalla dir `news_impact_pipeline/`)

1. **Parse + scaffold triage.** `pipeline_tools.py digest --date AAAA-MM-GG`
   (comandi e flag: sezione "Riferimento comandi" sopra).

2. **Triage.** Leggi `_index.md`. Per ognuna delle N notizie decidi:
   - ✅ **tieni** se (a) mappa su uno degli asset dell'universo corrente in DB —
     **verifica in `category_asset_map.yaml`, NON a memoria** (letto una volta sola,
     qui in fase di triage) — *e* (b) esiste un
     analogo storico plausibile (stesso theme/sub-theme, direzione sentiment,
     regime confrontabile).
   - ✖ **scarta** altrimenti (geopolitica senza trasmissione asset; corporate su
     ticker non in DB; structural_themes fuori finestra; movimento di mercato non
     riconducibile a uno shock-notizia discreto). Scrivi sempre 1 riga di motivo.
   - **Consolida** notizie sullo stesso tema in un'unica scheda (es. più item
     sull'energia → un solo `news_NN.md`), linkando tutte le righe a quella scheda.
   Compila le colonne Decisione / Motivazione / Scheda della tabella via Edit.

3. **Per ogni notizia tenuta**, esegui il flusso Fasi 3-4 nell'ordine
   `assets` → `match` → `new-card` → `analogues find` → `event_study` (sintassi
   nella sezione "Riferimento comandi").

   ⚠ **Raccogli PRIMA, scrivi DOPO.** Esegui tutti e cinque i comandi, decidi la
   potatura del pool, poi scrivi la scheda **in un solo passaggio**. Non scrivere
   una sezione per volta: è la causa n.1 del costo del run (vedi "Economia del run").

   Il `find` recupera gli **episodi storici analoghi dalla libreria** (Opzione B —
   pool ampio invece di 5 a mano), filtrando per sotto-tema, **direzione** e con il
   **no-look-ahead** (`--before` = la data della notizia).
   **Passa SEMPRE `--direction` e `--direction-reference TICKER`** e, sui temi a pool largo (`geopolitical`,
   `commodity_energy`), **anche `--subtheme`**: senza filtri il pool si gonfia e
   diluisce il segnale (scorecard W28→W30: IC eroso proprio su quei temi). La libreria
   applica già un **tetto di recency** (default: 30 episodi più recenti = regime
   corrente; regolabile con `--max-pool`), ma i filtri restano la prima difesa.

   I token di `--subtheme` da preferire sono quelli **canonici** di
   `subtheme_taxonomy.yaml` (es. `ai_capex_financing` vs `memory_cycle` vs
   `valuation_derisking`): il `find` li cerca prima nelle etichette **date-locali**
   — ricavate dal contesto in cui la data compare, non dall'intestazione del
   documento — e solo se restano <`--min-n` ricade sui sotto-temi di documento e
   poi sul tema. La riga di diagnostica dice sempre quale livello è stato usato:
   se leggi «uso i sotto-temi a livello di documento» il filtro è **debole** e va
   dichiarato nel caveat della scheda. Un token non in tassonomia funziona ancora
   (match per sottostringa), ma quasi sempre solo al livello debole.

   **Scegli il token guardando la copertura, non l'intuito**: `analogues.py labels
   --theme <theme>` stampa, per tema, quanti episodi ha ciascuna etichetta a livello date-locale
   (filtro forte) e a livello di documento (debole). Il token *concettualmente* ovvio
   non è sempre quello con copertura. Se un token che ti serve ha copertura zero o
   quasi, il rimedio è aggiungere pattern in `subtheme_taxonomy.yaml` e rilanciare
   `build` — **ricalibrandoli sui contesti reali**, non a memoria: le schede scrivono
   in inglese tecnico (`FOMC`, `75bp`, `dot plot`), non in italiano.

   ⚠ **Distingui «copertura assente» da «copertura sotto soglia»**: hanno rimedi
   diversi (dettaglio e caso reale: [references/etichette_date_locali.md](../references/etichette_date_locali.md)).
   Se la diagnostica dice «N episodi date-locali … <`--min-n`» con N>0, la
   tassonomia **funziona** e il pool stretto esiste — rilancia con `--min-n N` più
   basso e dichiara nel caveat che il campione è piccolo, invece di riclassificare
   la notizia sotto un altro tema. Aggiungere pattern in `subtheme_taxonomy.yaml`
   serve solo quando il conteggio date-locale è davvero **0**.
   Usa quel pool come set di analoghi (puoi **potare** gli episodi palesemente non
   pertinenti). Se il pool è troppo piccolo, integra a mano (Opzione A). Poi calcola
   l'event study (`event_study.py`, sintassi nel riferimento comandi).

   L'output di default è **compatto**: solo le tabelle di statistiche, che sono le
   uniche che finiscono nella scheda. Se devi potare il pool o capire un outlier,
   rilancia quella singola chiamata con `--detail`. Poi scrivi la scheda **completa
   in un passaggio** — tabelle e sezioni qualitative insieme (motivazione
   classificazione, asset, regime, episodi+motivazione, lettura sintetica, caveat).
   Se min(N) < 10 → la scheda riporta già "INDICATIVE ONLY".

   **Convenzione Verso dal 2026-09-13.** Passa `--direction-reference TICKER`
   insieme a `--direction`. Il verso indica la pressione sul prezzo dell'asset
   di riferimento (pos rialzo, neg ribasso, neutral nessuna pressione), basata sul
   meccanismo noto all'evento, mai sul rendimento successivo. Per bond: prezzo,
   non yield; per FX: quotazione del ticker. Non significa evento buono/cattivo.
   La scheda deve contenere nella classificazione la riga
   ``| `direction_reference` | BZ=F |`` con il ticker scelto per tutti i suoi episodi.
   Compila `Data | Verso | Meccanismo | Descrizione` come nel template.
   `find` usa esclusivamente dichiarazioni con quel riferimento; esclude versi
   conflittuali e dichiarazioni legacy prive di riferimento, conservando le fonti
   in libreria. Nessun fallback direzionale, neppure sotto `--min-n`.
   Senza riferimento il risultato è vuoto con diagnostica esplicita. Con campione
   insufficiente integra episodi verificati a mano e dichiara N; non reinterpretare
   automaticamente le etichette legacy. Il registro
   `knowledge_base/_direction_reviews.yaml` conserva scheda d'origine, asset e
   motivazione. Il `build` incorpora anche i veti: una data dubbia resta esclusa
   pur se una scheda recente le attribuiva un verso. Quali temi hanno già una
   revisione (cresce col recupero delle research): comando in
   [references/etichette_date_locali.md](../references/etichette_date_locali.md), non
   un elenco fisso qui — è già stato sbagliato una volta.
   Per confrontare altri asset puoi usare lo stesso evento, ma non attribuire loro
   il verso del riferimento senza una classificazione separata.

   ⚠ **Dichiara la geografia sulle release non americane**: se l'episodio è un dato
   o una decisione dell'**area euro** o del **Regno Unito**, metti
   `eurozone_release` / `britain_release` fra i meccanismi. L'euristica sul testo
   produce falsi positivi (dettaglio e caso reale:
   [references/etichette_date_locali.md](../references/etichette_date_locali.md)):
   **solo il campo dichiarato è affidabile**.

   **Nella prosa, nomina comunque il VERSO e il MECCANISMO, non solo il fatto.** La
   libreria costruisce le etichette date-locali dal testo *attorno alla data*: se
   la riga dice solo «2017-12-22 — Trump firma il TCJA», l'episodio nasce senza
   etichetta di canale. Scrivendo «…TCJA: espansione fiscale non finanziata →
   premio a termine» l'episodio diventa pescabile (caso reale — `term_premium`:
   [references/etichette_date_locali.md](../references/etichette_date_locali.md)).

   ⚠ **Segno misto sui bond.** `^TNX` e `^TYX` sono **rendimenti** (salgono nel
   selloff); `IGLT.L`, `1482.T`, `VGB.AX`, `EXX6.DE`, `IEF` sono **prezzi** (scendono
   nel selloff). In un selloff globale la tabella mostra i primi positivi e i secondi
   negativi: è coerenza, non divergenza — va detto esplicitamente nella scheda.

4. **Sintesi di sessione.** In coda a `_index.md`, compila la sezione "Sintesi di
   sessione": temi dominanti del giorno, letture trasversali, lacune KB emerse.

   **Se emerge una lacuna di Knowledge Base: descrivila in `_index.md` e basta.**
   Nel run giornaliero **non** si scrive la research e **non** si scrive nemmeno il
   prompt di deep research. La lacuna va solo annotata in "Lacune emerse", con
   abbastanza dettaglio da poterci tornare (tema canonico, asset coinvolti, perché
   il pool attuale non basta, quante volte è già ricorsa).

   Il prompt in `knowledge_base/_prompts/` si scrive **solo se il maintainer lo chiede
   esplicitamente**, in una sessione interattiva. Regola corretta il 2026-08-18:
   la versione precedente lo rendeva un passo automatico del run giornaliero e la
   cartella si riempiva da sola. Convenzioni: `_prompts/README.md`.

5. **Render HTML.** Genera la versione sfogliabile nel browser:
   ```bash
   venv/bin/python render_report.py --date YYYY-MM-DD
   ```
   Produce `daily_analysis/YYYY-MM-DD/report.html` (indice + tutte le schede +
   glossario comune in fondo, da `glossario.md`, in un'unica pagina). Nel job
   automatico questo passo è eseguito dal wrapper dopo Claude, quindi non serve
   farlo a mano lì.

## Note metodologiche (vincolanti — cfr. CLAUDE.md e Design Doc §7)

- Riporta SEMPRE N accanto alle statistiche; N<10 → "indicative only".
- **Asset su cui NON trarre una direzione attesa.** Prima di scrivere la lettura
  direzionale, apri la scorecard più recente (`daily_analysis/_scorecard/` — l'ultimo
  file per settimana ISO) e leggi la sezione **"5-bis. Su quali ASSET prevediamo
  meglio?"**. La tabella non dà più un giudizio automatico: hit-rate e IC sono
  metriche diverse (hit-rate = quota di segni corretti, IC = se l'ordine delle
  magnitudini rispecchia il realizzato) e possono divergere — un IC negativo NON
  implica da solo che la direzione sia sbagliata più spesso che no. Leggi i due
  numeri dell'asset che ti serve; se appaiono deboli o incoerenti fra loro, riporta
  pure la tabella dell'event study ma **dichiara esplicitamente che il segno
  storico è inaffidabile** su quell'asset invece di costruirci sopra una previsione.
  La stessa scelta va **marcata nel titolo di ogni tabella**: `[previsione]`,
  `[descrittiva]` o `[scenario: nome]` (dettagli nel template, sezione Risultati).
  Il ledger delle previsioni registra solo ciò che è dichiarato lì, non la prosa.
  ⚠ NON dare per scontato un elenco a memoria: cambia ogni settimana, i numeri vanno
  riletti dalla scorecard corrente.
- Selezione analoghi: solo info disponibile alla data dell'episodio (no look-ahead).
- La segmentazione per regime è la difesa principale contro il mixing di contesti
  macro strutturalmente diversi: dichiara sempre se gli analoghi appartengono a
  regimi differenti.
- Nessun indicatore (rendimenti, vol, medie) è persistito: tutto calcolato on-the-fly.

## Stile e chiarezza (VINCOLANTE — vale per le schede e per la sintesi)

Il lettore è competente di finanza ma **in apprendimento**: non dà per scontate le
sigle né i meccanismi (per le sigle, vedi la regola sul glossario comune sotto).
Meglio una scheda più lunga e limpida che una corta e criptica. La lunghezza non è
un problema; l'oscurità sì. Regole:

1. **Non ridefinire una sigla/ticker/termine dentro la scheda: linka il glossario
   comune.** Vale per dati macro, strumenti di policy e ticker (`CPI`, `NFP`, `TPI`,
   `^TNX`, `BTP_BUND_SPREAD`, ecc.). Ogni scheda chiude con
   `→ [Glossario di sigle e termini](#doc-glossario)`, reso una volta sola in fondo
   al report da `render_report.py`. **Se il termine che ti serve non c'è ancora nel
   glossario** (`glossario.md`), aggiungilo lì — una riga, nella sezione più adatta,
   ordine alfabetico — invece di spiegarlo inline: così la prossima scheda lo trova
   già pronto e non lo riscrive. Stessa regola già in `news_card_template.md`; tiene
   bassi i byte riscritti a ogni turno (vedi "Economia del run" sotto).

2. **Spiega il meccanismo, non solo l'esito.** Invece di "ECB hawkish → equity giù",
   scrivi *perché*: "se la banca centrale alza i tassi, indebitarsi costa di più,
   gli utili futuri delle aziende valgono meno se scontati a tassi più alti, e quindi
   i prezzi azionari tendono a scendere". Una frase di catena causale per ogni nesso
   non ovvio.

3. **Non dare per scontato il contesto.** Se citi un episodio storico (es. "l'errore
   di Trichet del 2011"), aggiungi mezza riga su cosa fu e perché è rilevante.

4. **Interpreta i numeri dell'event study a parole.** Dopo ogni tabella, una riga del
   tipo: "in pratica: nei 5 episodi simili, a 10 giorni l'indice era in calo nella
   maggioranza dei casi (mediana −2,4%), ma con forte dispersione → segnale debole".
   Ricorda sempre cosa significano T+1/T+5/T+10 (giorni di borsa dopo l'evento),
   mediana vs media, e perché N piccolo = indicativo.

5. **Tono**: didattico, non accademico. Frasi piane. Va benissimo una parentesi
   esplicativa in più. Evita il gergo non spiegato e le catene di sigle senza link
   al glossario.

## Prompt suggerito per la routine `/schedule`

> Processa il morning briefing di oggi seguendo
> `~/Claude/mercati_finanza/news_impact_pipeline/PHASE5_RUNBOOK.md`: genera il digest di triage,
> tria tutte le notizie presenti (subset triato), e produci una scheda di event study completa
> per ciascuna notizia tenuta in `~/Claude/mercati_finanza/daily_analysis/<oggi>/`. Se il DB mercati
> è vuoto, ricostruiscilo prima con bootstrap + spread daily (MAI fetch_fred_data.py,
> vedi `references/quando_si_rompe.md`). **Rispetta la sezione "Stile e chiarezza" del
> runbook: linka le sigle al glossario comune (aggiungendo lì quelle nuove), spiega i
> meccanismi causali, interpreta i numeri a parole — preferisci la chiarezza alla
> brevità.** Riporta in chat un riepilogo: quante notizie tenute/scartate e i temi
> delle schede prodotte.
