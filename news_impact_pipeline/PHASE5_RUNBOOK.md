# Fase 5 — Runbook orchestrazione giornaliera

Procedura che l'agente Claude esegue (manualmente o via `/schedule`) per
processare il morning briefing del giorno e produrre le schede di analisi.

## Input

- Briefing HTML in `~/Claude/morning brief/YYYY-MM-DD-morning-briefing.html`
  (20 notizie: 10 International + 10 Economics & Finance, + 1 "One Thing to Watch").
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

- `~/Claude/daily_analysis/YYYY-MM-DD/_index.md` — digest di triage (tutte le 20
  notizie con decisione ✅/✖ + motivazione + link alle schede).
- `~/Claude/daily_analysis/YYYY-MM-DD/news_NN.md` — una scheda completa per ogni
  notizia tenuta (subset triato: tipicamente 3-6/giorno).

## Economia del run (VINCOLANTE — leggi prima di iniziare)

Misurato il 2026-08-21 sui transcript delle sessioni: **il costo di un run cresce
col quadrato del numero di turni**, perché a ogni chiamata di tool l'intero
contesto accumulato viene riletto. Un blocco da 20 KB scritto al turno 20 viene
ripagato su tutti i turni successivi. Dati reali: 55 turni → $23; 96 turni → $36;
115 turni → $44; 134 turni → $53. Il cache-read è l'85% della spesa.

Non si risparmia scrivendo di meno o peggio. Si risparmia **facendo meno giri**.
Tre regole, in ordine di impatto:

1. **Ogni file si scrive UNA VOLTA SOLA, in un unico passaggio.** Il 21/08 sono
   servite 43 chiamate di scrittura per 9 file (`_index.md` riscritto 7 volte,
   `news_01.md` 7 volte, `news_03.md` 7 volte), ognuna rigenerando il corpo intero
   via heredoc. Prima di scrivere una scheda, **raccogli tutto**: pool di episodi
   potato, event study, research KB, sezione 5-bis della scorecard. Poi scrivi il
   file completo in una volta. Se dopo devi correggere, usa **Edit chirurgico** sulla
   stringa da cambiare — mai un heredoc che rigenera il corpo.
2. **Non rileggere ciò che hai appena scritto.** Niente `cat`/`sed -n` sulla scheda
   che hai appena generato: se la scrittura non fosse riuscita avresti avuto un errore.
3. **Non lanciare `--help`.** I flag che servono sono documentati sotto. Il 21/08 se
   ne sono andati 10 KB di contesto in `--help` di comandi usati ogni giorno.

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
  [--direction pos|neg|neutral] [--before AAAA-MM-GG] [--min-n N] [--max-pool N]
#   --subtheme ripetibile · --max-pool default 30 (0 = nessun tetto)
#   --min-n = soglia sotto cui il filtro sotto-tema NON viene applicato
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

2. **Triage.** Leggi `_index.md`. Per ognuna delle 20 notizie decidi:
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
   **Passa SEMPRE `--direction`** e, sui temi a pool largo (`geopolitical`,
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
   (filtro forte) e a livello di documento (debole). Serve perché il token
   *concettualmente* ovvio non è sempre quello con copertura: su `monetary_policy`
   il canale primario è `rate_decision`, ma fino al 2026-08-16 quel token restituiva
   **0** episodi date-locali mentre `guidance_pivot` ne aveva 31. Se un token che ti
   serve ha copertura zero o quasi, il rimedio è aggiungere pattern in
   `subtheme_taxonomy.yaml` e rilanciare `build` — **ricalibrandoli sui contesti
   reali**, non a memoria: le schede scrivono in inglese tecnico (`FOMC`, `75bp`,
   `dot plot`), non in italiano.

   ⚠ **Distingui «copertura assente» da «copertura sotto soglia»** (regola aggiunta
   il 2026-08-27). Il degrado al pool del tema ha due cause diverse e il rimedio
   non è lo stesso. La riga di diagnostica ora stampa entrambi i conteggi: se dice
   «N episodi date-locali … <`--min-n`» con N>0, la tassonomia **funziona** e il
   pool stretto esiste — rilancia con `--min-n N` e dichiara nel caveat che il
   campione è piccolo, invece di riclassificare la notizia sotto un altro tema per
   trovare episodi. Il 26/08 `macro_data + tariff_escalation` aveva **11** episodi
   date-locali contro una soglia di 12: il vecchio messaggio mostrava solo lo zero
   del livello documento, la notizia sui dazi è finita sotto `geopolitical` e
   l'analisi ha registrato una lacuna di tassonomia inesistente. Aggiungere pattern
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

   **Leggi la riga diagnostica di `find`, anche per la direzione.** Dal 2026-08-29
   `--direction` ha **quattro** livelli: verso **DICHIARATO** dalle schede (forte,
   nessuna euristica) → marcatori date-locali da regex → direzione della scheda
   (**debole**, e lo dichiara) → mixed/sconosciuto. Se leggi «uso la direzione a
   livello di scheda» il segno del pool non descrive gli episodi ma l'orientamento
   delle schede che li avevano citati: va dichiarato nel caveat.

   ⚠ **Se la riga dice «N episodi l'avevano DICHIARATA: sotto la soglia», abbassa
   `--min-n` a quel numero invece di accettare il pool più largo.** È il singolo
   controllo che previene la classe di errore più costosa del sistema: un pool che
   contiene episodi **di verso opposto** a quello richiesto. Caso reale del 29/08:
   `commodity_energy + hormuz + --direction pos` restituiva 13 episodi, di cui 5
   erano escalation **dichiarate `neg`** — entrate perché il filtro era degradato al
   livello scheda. Con `--min-n 8` il pool scende a 8 episodi tutti dichiarati `pos`.
   Meglio N=8 pulito che N=13 con il 38% di segni rovesciati: un episodio con il
   verso sbagliato non diluisce la mediana, la **sposta dalla parte opposta**.

   **Compila il blocco episodi DICHIARATO** (tabella `Data | Verso | Meccanismo |
   Descrizione` in `news_card_template.md`). Da 2026-08-19 è da lì che la libreria
   legge verso e meccanismo di ogni episodio, invece di dedurli dalla prosa: i campi
   dichiarati **vincono** sull'euristica. È l'unico punto della scheda che alimenta
   direttamente la qualità dei pool di domani — compilarlo male è peggio che lasciarlo
   vuoto, perché una riga con verso illeggibile viene ignorata ma una sbagliata no.
   Dal 2026-08-29 la colonna **Verso** conta il doppio: alimenta un livello di filtro
   dedicato (`directions_declared`) che l'euristica non può più contaminare, ed è il
   solo modo di far crescere quel livello. Ogni riga che compili oggi è un episodio
   che domani filtra correttamente per verso — anche se un'altra scheda lo cita in
   prosa con parole di segno opposto.
   Verifica i token con `analogues.py labels --theme <t>` prima di sceglierli, e
   controlla l'adozione con `analogues.py stats`.

   ⚠ **Dichiara la geografia sulle release non americane** (dal 2026-08-26): se
   l'episodio è un dato o una decisione dell'**area euro** o del **Regno Unito**,
   metti `eurozone_release` / `britain_release` fra i meccanismi. I due token esistono in
   tassonomia, ma l'euristica sul testo produce falsi positivi (le righe corte
   assorbono le righe vicine, così un payroll USA che cita la reazione del cambio
   può risultare europeo): **solo il campo dichiarato è affidabile**. Il costo del
   non farlo è misurato: il 25/08 il pool `pmi` era in larga parte americano e su
   EURUSD=X dava il segno **sbagliato** dopo un dato europeo debole.

   **Nella prosa, nomina comunque il VERSO e il MECCANISMO, non solo il fatto.** La
   libreria costruisce le etichette date-locali dal testo *attorno alla data*: se
   la riga dice solo «2017-12-22 — Trump firma il TCJA», l'episodio nasce senza
   etichetta di canale. Scrivendo «…TCJA: espansione fiscale non finanziata →
   premio a termine» l'episodio diventa pescabile. Misurato il 2026-08-18: il
   vocabolario del premio a termine compare 144 volte nelle schede ma solo 5 volte
   vicino a una data, ed è il motivo per cui `term_premium` è inutilizzabile.

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
   Produce `daily_analysis/YYYY-MM-DD/report.html` (indice + tutte le schede in
   un'unica pagina). Nel job automatico questo passo è eseguito dal wrapper dopo
   Claude, quindi non serve farlo a mano lì.

## Note metodologiche (vincolanti — cfr. CLAUDE.md e Design Doc §7)

- Riporta SEMPRE N accanto alle statistiche; N<10 → "indicative only".
- **Asset su cui NON trarre una direzione attesa.** Prima di scrivere la lettura
  direzionale, apri la scorecard più recente (`daily_analysis/_scorecard/` — l'ultimo
  file per settimana ISO) e leggi la sezione **"5-bis. Su quali ASSET prevediamo
  meglio?"**. Gli asset marcati ❌ **controproducente** hanno IC storicamente
  *negativo*: su quelli la mediana degli analoghi punta nella direzione sbagliata più
  spesso che no. Riporta pure la tabella dell'event study, ma **dichiara esplicitamente
  che il segno storico è inaffidabile** su quell'asset invece di costruirci sopra una
  previsione. ⚠ NON dare per scontato l'elenco a memoria: cambia ogni settimana, va
  riletto dalla scorecard corrente (all'audit del 2026-08-10 erano DX-Y.NYB, GC=F,
  IEF, SOXX, ^TNX — cioè rifugio/tassi/dollaro; ^VIX, EEM, ^NDX, ^STOXX50E erano
  invece i più affidabili).
- Selezione analoghi: solo info disponibile alla data dell'episodio (no look-ahead).
- La segmentazione per regime è la difesa principale contro il mixing di contesti
  macro strutturalmente diversi: dichiara sempre se gli analoghi appartengono a
  regimi differenti.
- Nessun indicatore (rendimenti, vol, medie) è persistito: tutto calcolato on-the-fly.

## Stile e chiarezza (VINCOLANTE — vale per le schede e per la sintesi)

Il lettore è competente di finanza ma **in apprendimento**: non dà per scontate le
sigle né i meccanismi. Meglio una scheda più lunga e limpida che una corta e criptica.
La lunghezza non è un problema; l'oscurità sì. Regole:

1. **Espandi OGNI sigla/acronimo alla prima occorrenza**, poi puoi abbreviare. Vale
   per i dati macro, gli strumenti di policy e i ticker. Esempi:
   - `CPI` → "CPI (Consumer Price Index — l'indice dei prezzi al consumo, misura
     l'inflazione)"; `NFP` → "NFP (Non-Farm Payrolls — i nuovi posti di lavoro USA
     esclusa l'agricoltura)"; `PCE`, `ISM`, `JOLTS`, `PMI`, `GDP/PIL`, `HICP` idem.
   - Policy: `TPI` → "TPI (Transmission Protection Instrument — lo scudo anti-spread
     della BCE)"; `OMT`, `PEPP`, `APP`, `QT`, `forward guidance` idem.
   - Ticker: `^TNX` → "^TNX (rendimento del Treasury USA a 10 anni)"; `BZ=F` →
     "BZ=F (futures sul petrolio Brent)"; `^STOXX50E` → "^STOXX50E (indice azionario
     Euro Stoxx 50)"; `BTP_BUND_SPREAD` → "lo spread BTP-Bund (differenziale di
     rendimento tra titoli di Stato italiani e tedeschi a 10 anni, misura del rischio
     percepito sull'Italia)".

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
   esplicativa in più. Evita il gergo non spiegato e le catene di sigle.

## Prompt suggerito per la routine `/schedule`

> Processa il morning briefing di oggi seguendo
> `~/Claude/news_impact_pipeline/PHASE5_RUNBOOK.md`: genera il digest di triage,
> tria le 20 notizie (subset triato), e produci una scheda di event study completa
> per ciascuna notizia tenuta in `~/Claude/daily_analysis/<oggi>/`. Se il DB mercati
> è vuoto, ricostruiscilo prima con bootstrap + fetch_fred. **Rispetta la sezione
> "Stile e chiarezza" del runbook: espandi tutte le sigle alla prima occorrenza,
> spiega i meccanismi causali, interpreta i numeri a parole — preferisci la chiarezza
> alla brevità.** Riporta in chat un riepilogo: quante notizie tenute/scartate e i
> temi delle schede prodotte.
