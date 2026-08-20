# Fase 5 — Runbook orchestrazione giornaliera

Procedura che l'agente Claude esegue (manualmente o via `/schedule`) per
processare il morning briefing del giorno e produrre le schede di analisi.

## Input

- Briefing HTML in `~/Claude/morning brief/YYYY-MM-DD-morning-briefing.html`
  (20 notizie: 10 International + 10 Economics & Finance, + 1 "One Thing to Watch").
- DB mercati in `~/Claude/market_data/market_data.db` (**46 asset**).
  ⚠ NON dare per scontato il numero: l'universo si estende nel tempo. L'elenco
  autorevole e aggiornato è `category_asset_map.yaml` / `pipeline_tools.py
  list-categories`. Oltre ai 17 storici, ora include: **^NDX e SOXX** (Nasdaq-100 e
  semiconduttori → tema AI/chip), **HG=F** (rame), **HYG** (credito high yield),
  **^VIX** (volatilità), **URA/LIT** (uranio/litio), **EEM** (emergenti),
  **DX-Y.NYB** (indice dollaro), **TTF=F** (gas naturale europeo), **EXH9.DE**
  (utility europee, proxy elettricità EU), **CNY=X** (yuan onshore, canale
  guerra commerciale/Cina), **EWZ/BRL=X** (Brasile) e i **7 ASEAN**
  (**THB=X/SGD=X/MYR=X/IDR=X** valute + **THD/EWS/EIDO** equity Thailandia/
  Singapore/Indonesia — usali al posto del solo EEM per shock del Sud-Est
  asiatico; la Cambogia non ha proxy quotato), **SHLD.L** (ETF difesa/sicurezza
  globale, forte esposizione NATO/Europa — non EU-only puro), **EWY** (Corea,
  Samsung/SK Hynix) ed **EWT** (Taiwan, TSMC — canale memoria/HBM e rischio
  geopolitico Taiwan/Cina), **CAD=X** (dollaro canadese — canale diretto per dazi
  e attriti commerciali USA-Canada, aggiunto il 2026-08-16), e i **prodotti
  raffinati**: **RB=F** (benzina),
  **HO=F** (diesel/gasolio) e **CRACK_321** (margine di raffinazione in $/barile).
  ⚠ Per attacchi/fermi di raffineria usa **CRACK_321 e HO=F, non BZ=F**: quegli
  shock colpiscono i prodotti e il margine, e il greggio può perfino *scendere*
  (meno domanda di input) mentre il diesel sale. Se vuoto, ricostruirlo (vedi
  `bootstrap_market_data.py`; lo spread BTP-Bund via `fetch_daily_spread.py`,
  il crack via `compute_crack_spread.py`).

## Output

- `~/Claude/daily_analysis/YYYY-MM-DD/_index.md` — digest di triage (tutte le 20
  notizie con decisione ✅/✖ + motivazione + link alle schede).
- `~/Claude/daily_analysis/YYYY-MM-DD/news_NN.md` — una scheda completa per ogni
  notizia tenuta (subset triato: tipicamente 3-6/giorno).

## Procedura (tutti i comandi dalla dir `news_impact_pipeline/`)

1. **Parse + scaffold triage.** Genera l'indice del giorno:
   ```bash
   venv/bin/python pipeline_tools.py digest --date YYYY-MM-DD
   ```
   (Senza `--date` usa oggi. Aggiungi `--force` per rigenerare.)

2. **Triage.** Leggi `_index.md`. Per ognuna delle 20 notizie decidi:
   - ✅ **tieni** se (a) mappa su uno degli asset dell'universo corrente in DB —
     **verifica nell'elenco aggiornato (`category_asset_map.yaml`), NON a memoria**:
     notizie su AI/semiconduttori (→ ^NDX/SOXX), rame (→ HG=F), credito/rischio
     (→ HYG/^VIX), emergenti (→ EEM) ORA sono mappabili — *e* (b) esiste un
     analogo storico plausibile (stesso theme/sub-theme, direzione sentiment,
     regime confrontabile).
   - ✖ **scarta** altrimenti (geopolitica senza trasmissione asset; corporate su
     ticker non in DB; structural_themes fuori finestra; movimento di mercato non
     riconducibile a uno shock-notizia discreto). Scrivi sempre 1 riga di motivo.
   - **Consolida** notizie sullo stesso tema in un'unica scheda (es. più item
     sull'energia → un solo `news_NN.md`), linkando tutte le righe a quella scheda.
   Compila le colonne Decisione / Motivazione / Scheda della tabella via Edit.

3. **Per ogni notizia tenuta**, esegui il flusso Fasi 3-4:
   ```bash
   # asset rilevanti per il theme
   venv/bin/python pipeline_tools.py assets <theme>
   # research KB correlate
   venv/bin/python pipeline_tools.py match --theme <theme> --keyword ... --asset ...
   # crea lo scaffold scheda (auto-numerato news_NN.md)
   venv/bin/python pipeline_tools.py new-card --date YYYY-MM-DD --slug ... --title ... \
     --source "Morning Briefing YYYY-MM-DD" --theme <theme> --sub-theme ... \
     --sentiment ... --confidence ... --horizon ... --text "..."
   ```
   Poi recupera gli **episodi storici analoghi dalla libreria** (Opzione B — pool
   ampio invece di 5 a mano), filtrando per sotto-tema, **direzione** e con il
   **no-look-ahead** (`--before` = la data della notizia):
   ```bash
   venv/bin/python analogues.py find --theme <theme> --subtheme <tok> \
     --direction <pos|neg|neutral> --before YYYY-MM-DD   # date CSV pronte per --events
   ```
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

   **Scegli il token guardando la copertura, non l'intuito:**
   ```bash
   venv/bin/python analogues.py labels --theme <theme>   # quanti episodi porta ogni token
   ```
   Stampa, per tema, quanti episodi ha ciascuna etichetta a livello date-locale
   (filtro forte) e a livello di documento (debole). Serve perché il token
   *concettualmente* ovvio non è sempre quello con copertura: su `monetary_policy`
   il canale primario è `rate_decision`, ma fino al 2026-08-16 quel token restituiva
   **0** episodi date-locali mentre `guidance_pivot` ne aveva 31. Se un token che ti
   serve ha copertura zero o quasi, il rimedio è aggiungere pattern in
   `subtheme_taxonomy.yaml` e rilanciare `build` — **ricalibrandoli sui contesti
   reali**, non a memoria: le schede scrivono in inglese tecnico (`FOMC`, `75bp`,
   `dot plot`), non in italiano.
   Usa quel pool come set di analoghi (puoi **potare** gli episodi palesemente non
   pertinenti). Se il pool è troppo piccolo, integra a mano (Opzione A). Poi calcola
   l'event study:
   ```bash
   venv/bin/python event_study.py --ticker 'T1,T2' \
     --events <date dalla libreria> --windows 1,3,5,10 --markdown
   ```
   Incolla l'output e **compila via Edit** le sezioni qualitative della scheda:
   motivazione classificazione, asset, regime, episodi+motivazione, lettura
   sintetica, caveat. Se min(N) < 10 → la scheda riporta già "INDICATIVE ONLY".

   **Leggi la riga diagnostica di `find`, anche per la direzione.** Da 2026-08-19
   `--direction` ha tre livelli come `--subtheme`: marcatori date-locali (forte) →
   direzione della scheda (**debole**, e lo dichiara) → mixed/sconosciuto. Se leggi
   «uso la direzione a livello di scheda» il segno del pool non descrive gli episodi
   ma l'orientamento delle schede che li avevano citati: va dichiarato nel caveat.

   **Compila il blocco episodi DICHIARATO** (tabella `Data | Verso | Meccanismo |
   Descrizione` in `news_card_template.md`). Da 2026-08-19 è da lì che la libreria
   legge verso e meccanismo di ogni episodio, invece di dedurli dalla prosa: i campi
   dichiarati **vincono** sull'euristica. È l'unico punto della scheda che alimenta
   direttamente la qualità dei pool di domani — compilarlo male è peggio che lasciarlo
   vuoto, perché una riga con verso illeggibile viene ignorata ma una sbagliata no.
   Verifica i token con `analogues.py labels --theme <t>` prima di sceglierli, e
   controlla l'adozione con `analogues.py stats`.

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
