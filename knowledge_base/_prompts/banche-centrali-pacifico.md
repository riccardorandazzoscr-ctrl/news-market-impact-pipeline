# Prompt di deep research — Reserve Bank of Australia e Bank of Korea: regime ed episodi storici

## Metadati della richiesta (per noi, NON parte del prompt)

- **Lacuna che chiude:** «Nessuna research su Reserve Bank of Australia e Bank of Korea. `news_05.md` ha dovuto usare pool `activity_growth` e `inflation_print` composti quasi interamente da release americane ed europee. Il problema non è la scarsità di episodi (26 e 30, entrambi ben sopra soglia) ma la loro geografia: si misura come gli asset australiani e coreani reagiscono a dati americani, non a dati domestici.» (2026-09-02, lacuna 1) — preceduta dal 2026-08-27, lacuna 3: «Il match più alto per `news_03` è la research sul fixing della PBOC (score 8), che riguarda la gestione del cambio cinese — un altro paese e un altro strumento. […] Con la Corea che è il primo anello macro della catena AI, questa lacuna è destinata a ripresentarsi», e dal 2026-08-27, lacuna 4/5, dove la diagnosi iniziale («è un problema di tassonomia») è stata **ribaltata dalla misura**: aggiunti i token geografici, il conteggio resta zero perché mancano gli episodi datati, non le etichette.
- **Segnalata il:** 2026-08-20 (prima occorrenza, sull'assenza di asset — **chiusa** l'8-27 aggiungendo `AUD=X`/`^AXJO`/`VGB.AX`; `KRW=X`/`EWY` erano già in DB), 2026-08-26 (di nuovo sull'asset, stessa chiusura), 2026-08-27 (due segnalazioni distinte lo stesso giorno: mancanza di research su Bank of Korea, e diagnosi poi corretta sul token `australia_release`), 2026-08-31 (implicita: `news_06` tenuta con confidenza "low" per pool geograficamente non pertinente), 2026-09-02 (esplicita, questa citazione). **Ricorrenza: 4** occorrenze sulla research vera e propria, oltre alle 2 sull'asset ormai chiuse.
- **Tema canonico di destinazione:** `monetary_policy` (le decisioni RBA/BoK sono l'episodio-ancora più pulito); deve però popolare anche `macro_data` per i dati che le anticipano (CPI trimmed mean australiano, CPI coreano, PMI, occupazione) — stesso doppio ruolo già svolto da `eurozone_release`.
- **Asset in DB che lo studio deve poter servire:** `AUD=X` (USD/AUD, dal 2011-01), `^AXJO` (S&P/ASX 200, dal 2011-01), `VGB.AX` (ETF titoli di stato australiani, dal 2012-04), `KRW=X` (USD/KRW), `EWY` (iShares MSCI South Korea — dominato da Samsung/SK Hynix, quindi anche canale ciclo memoria/AI)
- **Asset citabili ma NON in DB:** un ETF/future sui titoli di stato coreani (KTB) — non risulta un equivalente liquido di `VGB.AX` per la Corea, se lo studio ne identifica uno dichiaralo per nome senza assumerlo in DB; il differenziale di rendimento AU-US e KR-US a 10 anni, se reperibile solo come livello e non come serie scaricabile.
- **Esplicitamente FUORI SCOPO:** Reserve Bank of New Zealand/`NZD=X` (token e asset già trattati altrove, nessuna lacuna aperta su questo) e PBOC/Cina (research dedicata già in KB, score 9). Non includerli per evitare di diluire il pool con un terzo o quarto paese.
- **Perché serve la research e non basta la tassonomia:** i quattro token geografici del 2026-08-27 sono stati misurati su 8.735 contesti date-locali reali PRIMA di scrivere i pattern — `australia_release` 0, `korea_release` 1, `canada_release` 1, `japan_release` 106. Rimisurato oggi (2026-09-03) con `analogues.py find --subtheme australia_release/korea_release` su entrambi i temi: **ancora 0 episodi date-locali su tutti e quattro gli incroci** (australia_release×monetary_policy, ×macro_data, korea_release×monetary_policy, ×macro_data). Il precedente che funziona è `japan_release`: stesso meccanismo, oggi **15 episodi date-locali su `macro_data`** (soglia 12) perché esiste una research dedicata (`knowledge_base/Giappone : Bank of Japan/…`) che nomina esplicitamente l'istituzione riga per riga. Le 140 menzioni di "RBA" e le 332 di "Corea" già presenti nelle schede vivono nella prosa dei commenti, non nelle righe attorno a una data — stessa dinamica già documentata per `term_premium` il 2026-08-18.
- **Vincolo tecnico non ovvio, critico per non ripetere l'errore:** l'etichettatura automatica (`local_labels` in `analogues.py`) cerca i pattern `\brba\b`, `reserve bank of australia`, `bank of korea`, `\bbok\b` **nel testo intorno alla data dell'episodio**, non nel documento nel suo complesso. Uno studio storicamente accurato ma che descrive gli eventi senza nominare esplicitamente l'istituzione riga per riga produrrà episodi che il `build` non etichetterà — la lacuna resterebbe aperta anche dopo aver caricato la research. Vedi il vincolo di scrittura dedicato più sotto.

---

## PROMPT (da incollare)

Sei un ricercatore quantitativo. Produci uno studio storico in **italiano**,
in Markdown, su:

**Reserve Bank of Australia e Bank of Korea: regime ed episodi storici (1999–presente)**

### Contesto d'uso (vincolante)

Lo studio alimenta una pipeline di *event study*: un sistema che, data una notizia
odierna, cerca episodi storici analoghi e misura i rendimenti cumulati degli asset
a T+1, T+3, T+5, T+10 giorni di trading. Quindi:

- il valore dello studio sta nelle **date puntuali** e nei **canali di trasmissione**,
  non nella narrativa;
- ogni affermazione quantitativa va accompagnata dalla fonte e, se incerta, dichiarata tale;
- niente raccomandazioni operative, niente previsioni: solo statistica descrittiva storica.

### Le due domande a cui lo studio deve rispondere

**(1) L'Australia come "prior" del ciclo dati settimanale americano.** L'universo `AUD=X`/`^AXJO`/`VGB.AX` è stato aggiunto il 2026-08-27 con la motivazione esplicita che le release RBA (in particolare CPI mensile e trimmed mean) arrivano tipicamente all'inizio della settimana di mercato, prima dei dati equivalenti americani, e ne costituiscono un prior regionale. Lo studio deve stabilire se questa relazione è misurabile: quando un dato australiano hawkish/dovish è stato seguito, nella stessa settimana, da un dato americano nella stessa direzione, e quando invece ha divergito. Non serve un modello formale — serve la cronologia datata che permetterebbe di costruirlo in futuro.

**(2) La Corea come primo anello macro del ciclo AI/memoria, separato dal canale di politica monetaria pura.** `EWY` è dominato da Samsung e SK Hynix: una decisione o una sorpresa macro della Bank of Korea lo muove per il canale valutario/tassi, ma l'export coreano di semiconduttori lo muove per il canale del ciclo tecnologico globale, spesso nella stessa settimana e talvolta in direzioni opposte. Lo studio deve trattare questi come **due canali distinti** e, dove possibile, includere episodi di controllo in cui il driver è dichiaratamente uno solo dei due (una decisione BoK senza notizie sui semiconduttori quella settimana; un dato export/memoria senza riunione BoK), in modo da poter isolare l'uno dall'altro.

### Struttura richiesta (esattamente queste sei sezioni)

**§1 Sintesi esecutiva.** La tesi centrale in 3-5 punti. Dichiara esplicitamente
**dove l'event study è affidabile e dove non lo è** — in particolare se il campione
di decisioni RBA/BoK pure (senza altri driver nella stessa finestra) è denso
abbastanza da distinguerle dal rumore del ciclo macro globale.

**§2 Tassonomia dei canali di trasmissione.** Un paragrafo per canale. Ogni canale
in forma di **catena causale esplicita** (`evento → meccanismo → variabile → prezzo`)
e con l'indicazione degli asset-proxy da usare fra questi: `AUD=X`, `^AXJO`, `VGB.AX`,
`KRW=X`, `EWY`. Distingui almeno questi canali:
- decisione di tasso RBA (hawkish/dovish/in linea) come canale diretto su `AUD=X` e `VGB.AX`, redistributivo rispetto a `^AXJO` (un rialzo può pesare sull'azionario e sostenere la valuta nello stesso episodio);
- sorpresa sui dati australiani (CPI mensile, trimmed mean, occupazione) come *prior* per il dato equivalente americano della stessa settimana — il canale della domanda (1);
- decisione di tasso Bank of Korea come canale diretto su `KRW=X`, con effetto **amplificatore o attenuante** su `EWY` a seconda che converga o diverga dal canale (4);
- ciclo export/memoria coreano (dati export dei primi 10-20 giorni del mese, risultati Samsung/SK Hynix) come canale separato su `EWY`, distinto dalla politica monetaria — il canale della domanda (2);
- intervento valutario o verbale (jawboning) della Bank of Korea sul won, se distinguibile dalla decisione di tasso ordinaria.
Segnala esplicitamente quali canali sono redistributivi, quali amplificatori, e quali invece **in conflitto** fra loro nella stessa finestra temporale.

**§3 Catalogo di episodi-ancora datati.** Il cuore dello studio. Una tabella con
colonne: `Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead`.

La colonna "Evento" deve **nominare esplicitamente l'istituzione** per ogni episodio di politica monetaria o dato ufficiale — "RBA", "Reserve Bank of Australia", "Bank of Korea" o "BOK" per esteso nel testo della riga, non solo il nome del dato (es. "La RBA alza i tassi di 25pb…", non solo "Rialzo dei tassi in Australia…"). È un vincolo tecnico, non stilistico: la pipeline etichetta automaticamente un episodio come "release australiana/coreana" cercando questi pattern nel testo intorno alla data, e un episodio corretto ma senza questi termini non verrà etichettato — la lacuna che questo studio deve chiudere resterebbe aperta anche dopo il caricamento.

La colonna "Direzione attesa" va in forma **canonica** (`pos`/`neg`/`neutral`), riferita esplicitamente a **ciascun** asset quando il verso diverge fra loro (es. `AUD=X: neg / ^AXJO: pos`). **Attenzione al verso**: `AUD=X` e `KRW=X` sono quotati come dollaro-per-valuta-locale inversa (USD/AUD, USD/KRW): salgono quando la valuta locale si **indebolisce**. Una decisione RBA o BoK **hawkish** fa tipicamente **scendere** `AUD=X`/`KRW=X` (valuta locale più forte) — è l'errore di segno già commesso e corretto su questo stesso asset il 2026-08-27, non ripeterlo.

Requisiti sulle date, **critici**:
- almeno **20-30** episodi, con un minimo di 8-10 per ciascuna delle due banche centrali (per evitare che uno dei due pool resti sotto soglia);
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**, non
  quella dell'annuncio: le riunioni RBA sono in orario asiatico e i dati BoK escono
  spesso a mercato locale chiuso rispetto a `EWY` (ETF USA) — se il disallineamento
  si applica, usa la prima seduta utile del proxy e **spiegalo nella colonna Note**;
- se una data è incerta fra due fonti, riportale entrambe e dichiaralo;
- includi, quando databili con fonte, anche i casi di **divergenza dichiarata** fra il canale di politica monetaria e il canale export/memoria coreano (per servire la domanda 2), e i casi in cui un dato australiano ha anticipato o contraddetto il dato americano della stessa settimana (per servire la domanda 1);
- **una data che NON deve diventare un episodio** (picco di una serie di prezzo,
  inizio di una fase, riferimento generico) va scritta in forma **non-ISO**
  ("inizio 2019", "metà 2023") — la pipeline raccoglie ogni YYYY-MM-DD che trova.

**§4 Statistiche indicative.** Cosa è successo mediamente a `AUD=X`, `^AXJO`,
`VGB.AX`, `KRW=X`, `EWY` dopo gli episodi del §3, separando **sempre** i due paesi
e, per la Corea, i due canali (politica monetaria vs export/memoria). Riporta
**sempre N** accanto a ogni statistica; marca "INDICATIVE ONLY" ogni statistica
con N < 10 — probabile per più di una sotto-categoria, dichiaralo senza forzare
il pool ad aggregare cose diverse pur di salire sopra soglia.

**§5 Fasi di regime.** 2-5 fasi con confini datati (es. la Corea pre/post crisi
finanziaria asiatica se rilevante per l'inflation targeting; l'Australia nel ciclo
delle materie prime cinesi; l'ingresso della Corea nel ciclo di export dei
semiconduttori AI dal 2023 in avanti), ciascuna con: cosa cambia strutturalmente, e
**se gli analoghi di quella fase siano usabili nel regime corrente**. Nomi delle
fasi in `snake_case` inglese.

**§6 Caveat metodologici.** Come minimo: il disallineamento di fuso fra le
riunioni RBA/BoK (orario asiatico) e la seduta `EWY`/`^AXJO`-proxy quando rilevante;
la difficoltà di isolare un episodio "puramente RBA" o "puramente BoK" da uno
guidato dal ciclo cinese delle materie prime (Australia) o dal ciclo tech globale
(Corea) — dichiara quanti episodi del §3 sono "puri" contro quanti multi-causa;
l'assenza di un proxy obbligazionario coreano paragonabile a `VGB.AX`; *drift* di
fondo se il campione cade in una fase di mercato direzionale; fonti e incertezze
residue.

### Blocco di metadati finale (obbligatorio, in coda al file)

Chiudi con un blocco YAML delimitato da tre backtick e la parola `yaml`, in questo
formato esatto:

    ---
    title: "<titolo completo>"
    date_compiled: <YYYY-MM-DD>
    primary_theme: monetary_policy
    sub_themes: [australia_release, korea_release, rba, boj_divergence, memory_cycle, fx_intervention]
    relevant_assets: [AUD=X, ^AXJO, VGB.AX, KRW=X, EWY]
    external_assets_mentioned:
      - "<eventuale ETF/future su titoli di stato coreani, se identificato — con motivo per cui conterebbe>"
    time_window:
      start: 1999-01-01
      end: present
    regime_phases:
      - <nome_fase>: <YYYY-MM-DD> to <YYYY-MM-DD|present>
    keywords: [RBA, Reserve Bank of Australia, Bank of Korea, BOK, banca centrale australiana, banca centrale coreana, dollaro australiano, won coreano, trimmed mean, CPI australiano, CPI coreano, ASX 200, Samsung, SK Hynix, ciclo memoria, export semiconduttori Corea, prior settimanale]

### Vincoli di scrittura

- Italiano, prosa densa, niente elenchi puntati dove serve un ragionamento.
- Cifre puntuali sempre con fonte e data; se non verificabile, dillo.
- Nessuna data ISO inventata o approssimata: meglio una data in meno che una sbagliata.
- **Nomina sempre l'istituzione per esteso o in sigla (RBA/Reserve Bank of Australia, Bank of Korea/BOK) nella riga della tabella §3**, non solo nella prosa circostante: è un requisito tecnico della pipeline, non una preferenza stilistica (vedi sopra).

---

## Dopo l'esecuzione (checklist per Claude)

- [ ] research salvata in `knowledge_base/<Titolo>/<Titolo>.md`
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] `venv/bin/python analogues.py find --theme monetary_policy --subtheme australia_release --max-pool 0 --min-n 1` e lo stesso per `korea_release` su `monetary_policy` e `macro_data` → conferma che il conteggio è salito da 0
- [ ] `venv/bin/python analogues.py labels --theme monetary_policy` e `--theme macro_data` → la copertura è migliorata rispetto a oggi (2026-09-03: entrambi i token a 0 su entrambi i temi)?
- [ ] `venv/bin/python pipeline_tools.py match "<notizia tipo su una decisione RBA o BoK>"` → lo studio esce primo
- [ ] verificare a campione 3-4 righe della tabella §3: contengono "RBA"/"Bank of Korea" nel testo, non solo il nome del dato?
- [ ] date spurie? (confini di regime, `date_compiled`, date in prosa) → correggere il .md
- [ ] questo prompt cancellato da `_prompts/`
