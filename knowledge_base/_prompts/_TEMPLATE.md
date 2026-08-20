# Template di prompt per deep research KB

> Copia questo file in `_prompts/<slug>.md` e riempi le parti fra `<...>`.
> Il testo dentro il blocco "PROMPT" è quello da incollare nello strumento di
> deep research: deve essere **autosufficiente**, perché chi lo esegue non ha
> accesso a questo repository.

---

## Metadati della richiesta (per noi, NON parte del prompt)

- **Lacuna che chiude:** <copiare la frase esatta dalla sezione "Lacune emerse">
- **Segnalata il:** <YYYY-MM-DD, e in quali altre date se ricorrente>
- **Tema canonico di destinazione:** <uno di: monetary_policy, fiscal_policy, geopolitical, macro_data, corporate_idiosyncratic, regulatory, commodity_energy, financial_stability, structural_themes>
- **Asset in DB che lo studio deve poter servire:** <ticker esistenti nell'universo>
- **Asset citabili ma NON in DB:** <ticker mancanti — vanno dichiarati, non usati>
- **Perché serve la research e non basta la tassonomia:** <es. "gli episodi datati non esistono in libreria: `analogues.py labels --theme X` dà N episodi, M con etichette locali">

---

## PROMPT (da incollare)

Sei un ricercatore quantitativo. Produci uno studio storico in **italiano**,
in Markdown, su:

**<TITOLO: tema — regime ed episodi storici (ANNO_INIZIO–ANNO_FINE)>**

### Contesto d'uso (vincolante)

Lo studio alimenta una pipeline di *event study*: un sistema che, data una notizia
odierna, cerca episodi storici analoghi e misura i rendimenti cumulati degli asset
a T+1, T+3, T+5, T+10 giorni di trading. Quindi:

- il valore dello studio sta nelle **date puntuali** e nei **canali di trasmissione**,
  non nella narrativa;
- ogni affermazione quantitativa va accompagnata dalla fonte e, se incerta, dichiarata tale;
- niente raccomandazioni operative, niente previsioni: solo statistica descrittiva storica.

### Struttura richiesta (esattamente queste sei sezioni)

**§1 Sintesi esecutiva.** La tesi centrale in 3-5 punti. Dichiara esplicitamente
**dove l'event study è affidabile e dove non lo è** su questo tema.

**§2 Tassonomia dei canali di trasmissione.** Un paragrafo per canale. Ogni canale
in forma di **catena causale esplicita** (`evento → meccanismo → variabile → prezzo`)
e con l'indicazione degli asset-proxy da usare fra questi: <lista asset in DB>.
Distingui i canali *direzionali* da quelli *redistributivi* (che muovono due asset
in direzioni opposte) e dagli *amplificatori* (che cambiano l'ampiezza ma non il segno).

**§3 Catalogo di episodi-ancora datati.** Il cuore dello studio. Una tabella con
colonne: `Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead`.

Requisiti sulle date, **critici**:
- almeno **<N, tipicamente 15-25>** episodi;
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**, non
  quella dell'annuncio: se la notizia esce a mercato chiuso, a mercato locale
  disallineato dal proxy (ETF USA su sottostante asiatico/europeo) o in un
  festivo, usa la prima seduta utile del proxy e **spiegalo nella colonna Note**;
- se una data è incerta fra due fonti, riportale entrambe e dichiaralo;
- **una data che NON deve diventare un episodio** (picco di una serie di prezzo,
  inizio di una fase, riferimento generico) va scritta in forma **non-ISO**
  ("inizio 2018", "primavera 2022") — la pipeline raccoglie ogni YYYY-MM-DD che trova.

**§4 Statistiche indicative.** Cosa è successo mediamente agli asset dopo gli
episodi del §3, per canale. Riporta **sempre N** accanto a ogni statistica;
marca "INDICATIVE ONLY" ogni statistica con N < 10.

**§5 Fasi di regime.** 2-5 fasi con confini datati, ciascuna con: cosa cambia
strutturalmente, e **se gli analoghi di quella fase siano usabili nel regime
corrente**. Nomi delle fasi in `snake_case` inglese.

**§6 Caveat metodologici.** Come minimo: disallineamenti di fuso/seduta fra proxy
e mercato sottostante; episodi multi-causa e come isolare la componente di interesse
(quale asset usare come controllo); *drift* di fondo se il campione cade tutto in
un mercato direzionale; canali con N strutturalmente piccolo; serie citate ma non
disponibili; fonti e incertezze residue.

### Blocco di metadati finale (obbligatorio, in coda al file)

Chiudi con un blocco YAML delimitato da tre backtick e la parola `yaml`, in questo
formato esatto:

    ---
    title: "<titolo completo>"
    date_compiled: <YYYY-MM-DD>
    primary_theme: <tema canonico>
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

### Vincoli di scrittura

- Italiano, prosa densa, niente elenchi puntati dove serve un ragionamento.
- Cifre puntuali sempre con fonte e data; se non verificabile, dillo.
- Nessuna data ISO inventata o approssimata: meglio una data in meno che una sbagliata.

---

## Dopo l'esecuzione (checklist per Claude)

- [ ] research salvata in `knowledge_base/<Titolo>/<Titolo>.md`
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] `venv/bin/python analogues.py labels --theme <tema>` → la copertura è migliorata?
- [ ] `venv/bin/python pipeline_tools.py match "<notizia tipo>"` → lo studio esce primo
- [ ] date spurie? (confini di regime, `date_compiled`, date in prosa) → correggere il .md
- [ ] questo prompt cancellato da `_prompts/`
