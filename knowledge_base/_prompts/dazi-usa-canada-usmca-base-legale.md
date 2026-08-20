# Prompt di deep research — Dazi USA-Canada/USMCA e la base legale delle tariffe dopo la sentenza della Corte Suprema

## Metadati della richiesta (per noi, NON parte del prompt)

- **Lacuna che chiude:** «La research esistente sui dazi è centrata sull'asse USA-Cina: il canale USA-Canada/USMCA (catene del valore nordamericane integrate, energia, auto, acciaio e alluminio) e la dimensione **giuridica** dei dazi dopo la sentenza della Corte Suprema del febbraio 2026 non sono coperti.»
- **Segnalata il:** 2026-08-17 (prima segnalazione); ricorrente il 2026-08-18 (dazi al 50% ex Section 338 in vigore il 19 agosto salvo intesa; il dossier auto blocca il negoziato a 15% contro 10% — il test della base legale e imminente, priorita in aumento)
- **Tema canonico di destinazione:** regulatory (con forte sovrapposizione a geopolitical)
- **Asset in DB che lo studio deve poter servire:** CAD=X, ^GSPC, ^NDX, ^VIX, DX-Y.NYB, HG=F, ^STOXX50E, CNY=X, EEM, GC=F, BZ=F
- **Asset citabili ma NON in DB:** TSX Composite e banche canadesi, ETF settoriale auto/componentistica USA, ferrovie nordamericane (CP/CNI), Western Canadian Select e differenziale WCS-WTI, alluminio LME, peso messicano (MXN=X)
- **Perché serve la research e non basta la tassonomia:** il tema `regulatory` ha **19 episodi in tutto** nella libreria, di cui 15 con il token `tariff_escalation`; il ramo `geopolitical` ne porta 39 date-locali ma **solo 2 riguardano Canada e Messico** (`2025-02-01`, `2025-03-04`). Per un cambio bilaterale come `CAD=X` — entrato nel DB il 2026-08-16 e mai validato in scorecard — il pool disponibile misura la reazione a eventi che non riguardavano il Canada. La dimensione giuridica (quale autorità legale sostiene i dazi dopo l'annullamento di febbraio 2026) non ha alcun precedente nel campione.

---

## PROMPT (da incollare)

Sei un ricercatore quantitativo. Produci uno studio storico in **italiano**, in Markdown, su:

**Dazi USA-Canada e commercio nordamericano: regime, base legale ed episodi storici (1987–2026)**

### Contesto d'uso (vincolante)

Lo studio alimenta una pipeline di *event study*: un sistema che, data una notizia odierna, cerca episodi storici analoghi e misura i rendimenti cumulati degli asset a T+1, T+3, T+5, T+10 giorni di trading. Quindi:

- il valore dello studio sta nelle **date puntuali** e nei **canali di trasmissione**, non nella narrativa;
- ogni affermazione quantitativa va accompagnata dalla fonte e, se incerta, dichiarata tale;
- niente raccomandazioni operative, niente previsioni: solo statistica descrittiva storica.

Lo studio ha **due assi**, entrambi obbligatori:

1. **L'asse bilaterale USA-Canada**: come si comportano dollaro canadese, azionario, materie prime e volatilità quando l'attrito commerciale riguarda un partner con catene del valore *integrate* (auto assemblate attraversando il confine più volte, energia via oleodotto, acciaio e alluminio) — situazione strutturalmente diversa dai dazi USA-Cina, dove i beni attraversano il confine una volta sola.
2. **L'asse giuridico**: la storia di *quale autorità legale* ha sostenuto i dazi americani (Sezione 232 sulla sicurezza nazionale, Sezione 301 sulle pratiche sleali, Sezione 201 di salvaguardia, IEEPA e i poteri emergenziali) e come i mercati hanno reagito a **decisioni giudiziarie** su di essi — non solo agli annunci politici. Questo è l'asse che oggi non esiste in nessuna nostra research ed è quello con maggiore valore informativo prospettico.

### Struttura richiesta (esattamente queste sei sezioni)

**§1 Sintesi esecutiva.** La tesi centrale in 3-5 punti. Dichiara esplicitamente **dove l'event study è affidabile e dove non lo è** su questo tema — in particolare se le reazioni si siano attenuate nel tempo man mano che il mercato imparava che molte scadenze slittano.

**§2 Tassonomia dei canali di trasmissione.** Un paragrafo per canale, in forma di **catena causale esplicita** (`evento → meccanismo → variabile → prezzo`), con gli asset-proxy da usare fra: CAD=X, ^GSPC, ^NDX, ^VIX, DX-Y.NYB, HG=F, ^STOXX50E, CNY=X, EEM, GC=F, BZ=F. Come minimo:

1. **Canale valutario**: dazio annunciato → attesa di export canadese più basso e di ragioni di scambio peggiori → dollaro canadese più debole. Ma va discusso perché la svalutazione funzioni anche come *ammortizzatore* (compensa in parte il dazio), il che rende il segno atteso meno ovvio di quanto sembri.
2. **Canale delle catene del valore integrate**: dazio su input intermedi → margini compressi anche per i produttori **americani** → effetto sull'azionario USA che è ambiguo, a differenza del caso cinese.
3. **Canale energetico**: dazi su greggio canadese, differenziale Western Canadian Select-WTI, esposizione delle raffinerie del Midwest americano.
4. **Canale dell'incertezza**: annunci ripetuti e scadenze mobili → indici di *trade policy uncertainty* → volatilità implicita e premio al rischio azionario, indipendentemente dall'esito.
5. **Canale giuridico**: sentenza o parere che conferma o annulla una base legale → cambia la *probabilità e la persistenza attesa* dell'intero impianto tariffario, non solo di quella misura → effetto sistemico su tutti i partner commerciali, Europa e Cina incluse.
6. **Canale di reindirizzamento**: dazi fra due blocchi → flussi che cercano percorsi alternativi → beneficio marginale per i terzi (proxy: ^STOXX50E, EEM).

Distingui i canali *direzionali* dai *redistributivi* (per esempio: acciaio americano guadagna, manifattura americana che compra acciaio perde) e dagli *amplificatori*.

**§3 Catalogo di episodi-ancora datati.** Il cuore dello studio. Tabella con colonne: `Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead`.

Copertura minima richiesta:
- **Dispute pre-2018**: le fasi acute della disputa sul legname di conifere (*softwood lumber*), la disputa sulla carne bovina e l'etichettatura d'origine, i round negoziali di NAFTA;
- **2018-2019**: dazi Sezione 232 su acciaio e alluminio applicati al Canada (giugno 2018), ritorsione canadese (luglio 2018), rimozione (maggio 2019), rinegoziazione e firma dell'USMCA;
- **2025-2026**: le date dei dazi su Canada e Messico (febbraio-marzo 2025), le successive proroghe ed esenzioni, l'annullamento della Corte Suprema del febbraio 2026 e ogni pronuncia intermedia (tribunali di primo grado, corti d'appello, sospensioni), e la ricostruzione dei dazi su base legale alternativa;
- **Controllo**: alcune date di dazi USA-Cina e USA-UE dello stesso periodo, da usare come confronto per isolare la componente specificamente canadese.

Requisiti sulle date, **critici**:
- almeno **20** episodi, di cui **almeno 12 specificamente Canada/USMCA**;
- ⚠ **almeno 8 episodi devono essere di DISTENSIONE** (proroga, sospensione, esenzione,
  revoca, accordo raggiunto, dazio annullato in tribunale), non di escalation. È il
  requisito più importante di tutta la richiesta e va soddisfatto anche a costo di
  allargare il perimetro a dazi USA non canadesi. Motivo, misurato il 2026-08-19 sulla
  libreria: sul sotto-tema `tariff_escalation` gli episodi con verso **distensivo** sono
  **2 in tutto**. Il sistema non ha praticamente mai visto un dazio essere *rimosso*,
  quindi ogni volta che una notizia commerciale è positiva è costretto a stimarne
  l'effetto su un campione di escalation — cioè col segno sbagliato. Un campione di
  distensione datato è il singolo contributo di questa research che vale di più;
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**, non quella dell'annuncio: molti annunci tariffari arrivano nel weekend o a mercato chiuso — usa la prima seduta utile e **spiegalo nella colonna Note**;
- distingui esplicitamente, nella colonna `Tipo`, fra **annuncio**, **entrata in vigore**, **proroga/sospensione**, **ritorsione**, **accordo** e **decisione giudiziaria**: sono sei tipi di evento con reazioni diverse e la pipeline li può filtrare solo se sono etichettati;
- se una data è incerta fra due fonti, riportale entrambe e dichiaralo;
- **una data che NON deve diventare un episodio** (inizio di una fase, riferimento generico) va scritta in forma **non-ISO** ("primavera 2018", "inizio 2025") — la pipeline raccoglie ogni YYYY-MM-DD che trova.

**§4 Statistiche indicative.** Cosa è successo mediamente agli asset dopo gli episodi del §3, **separando per tipo di evento** (annuncio vs entrata in vigore vs proroga vs decisione giudiziaria). Riporta **sempre N**; marca "INDICATIVE ONLY" ogni statistica con N < 10. Discuti se le reazioni si siano attenuate fra la prima e la seconda ondata tariffaria e, se sì, di quanto.

**§5 Fasi di regime.** 2-5 fasi con confini datati, nomi in `snake_case` inglese. Come minimo: l'era NAFTA, la prima guerra commerciale 2018-2019, l'era USMCA 2020-2024, la seconda ondata dal 2025 e — se i confini lo giustificano — la fase post-sentenza dal febbraio 2026. Per ciascuna dichiara **se gli analoghi siano usabili nel regime corrente**.

**§6 Caveat metodologici.** Come minimo: la fortissima asimmetria della distribuzione (molte scadenze non producono nulla, poche producono movimenti estremi — quindi la mediana è la statistica meno informativa e vanno riportati i quartili); il *learning effect* del mercato sulle proroghe; la co-movenza fra dollaro canadese e prezzo del petrolio, che confonde il canale valutario (indicare come controllarla, per esempio usando BZ=F come regressore o selezionando episodi a petrolio stabile); gli eventi multi-causa; l'assenza di precedenti per la dimensione giudiziaria; serie citate ma non disponibili; fonti e incertezze residue.

### Blocco di metadati finale (obbligatorio, in coda al file)

Chiudi con un blocco YAML delimitato da tre backtick e la parola `yaml`, in questo formato esatto:

    ---
    title: "<titolo completo>"
    date_compiled: <YYYY-MM-DD>
    primary_theme: regulatory
    sub_themes: [<snake_case, minuscolo>]
    relevant_assets: [<solo ticker della lista asset in DB>]
    external_assets_mentioned:
      - "<ticker o serie citata ma NON disponibile — con il motivo per cui conterebbe>"
    time_window:
      start: <YYYY-MM-DD>
      end: present
    regime_phases:
      - <nome_fase>: <YYYY-MM-DD> to <YYYY-MM-DD|present>
    keywords: [<termini italiani E inglesi con cui una notizia potrebbe pescare questo studio>]

Nelle `keywords` includi almeno: dazi, tariffs, canada, ottawa, usmca, nafta, softwood lumber, legname, acciaio, steel, alluminio, aluminum, section 232, section 301, section 201, ieepa, corte suprema, supreme court, legal authority, base legale, dollaro canadese, canadian dollar, loonie, cad, auto tariffs, componentistica, supply chain, retaliation, ritorsione, trade policy uncertainty, deadline, proroga, exemption.

### Vincoli di scrittura

- Italiano, prosa densa, niente elenchi puntati dove serve un ragionamento.
- Cifre puntuali sempre con fonte e data; se non verificabile, dillo.
- Nessuna data ISO inventata o approssimata: meglio una data in meno che una sbagliata.
- Sulla parte giuridica: descrivi cosa è stato deciso e con quale motivazione, senza esprimere valutazioni sul merito politico.

---

## Dopo l'esecuzione (checklist per Claude)

- [ ] research salvata in `knowledge_base/<Titolo>/<Titolo>.md`
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] `venv/bin/python analogues.py labels --theme regulatory` → il tema esce dai 19 episodi attuali?
- [ ] aggiungere i token nuovi (es. `usmca_canada`, `legal_authority`, `tariff_deadline`) a `subtheme_taxonomy.yaml` se assenti
- [ ] `venv/bin/python pipeline_tools.py match --theme regulatory --keyword canada --keyword tariff` → lo studio esce primo
- [ ] date spurie? (confini di regime, `date_compiled`, date in prosa) → correggere il .md
- [ ] questo prompt cancellato da `_prompts/`
