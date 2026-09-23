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
**esattamente** queste intestazioni, in quest'ordine (la pipeline la legge per nome
delle colonne):

`| Data | Asset | Verso | Meccanismo | Evento | Note |`

**Una riga per ogni coppia (data, asset).** Se lo stesso evento spinge due asset in
direzioni diverse, sono due righe con la stessa data. Regole delle colonne:

- `Asset`: **un solo** ticker, preso da questa lista e da nessun'altra: <lista asset in DB>.
  Uno strumento non in lista si nomina solo in `Note`.
- `Verso`: la pressione **attesa all'epoca** sul **prezzo del ticker**, con l'informazione
  disponibile quel giorno — `pos` (al rialzo), `neg` (al ribasso), `neutral`. Non è un
  giudizio sull'evento e **non è il movimento poi osservato**: se il mercato si aspettava
  una cosa ed è successa l'opposta, si scrive l'attesa. L'attesa è la **sorpresa rispetto a
  quanto il mercato aveva già prezzato**, non il meccanismo in astratto: un rialzo dei tassi
  interamente scontato, annunciato con una guidance accomodante, spinge la valuta al
  ribasso, non al rialzo. Se non sai ricostruire cosa era prezzato, scrivi `pos, neg`.
  Convenzioni del ticker, da non
  sbagliare: sulle valute è la quotazione così com'è (`JPY=X` è USD/JPY: yen forte =
  `neg`); `^TNX`, `^FVX`, `^TYX` quotano il **rendimento**, `IEF` e gli ETF obbligazionari il
  **prezzo**; uno spread (`BTP_BUND_SPREAD`) che si allarga è `pos`. Se l'attesa era
  genuinamente ambigua scrivi `pos, neg`: la riga resta documentata ma esce dai calcoli
  direzionali, ed è meglio così che un verso indovinato.
- `Meccanismo`: uno o più token fra questi, separati da virgola: <token canonici del tema,
  da `analogues.py labels --theme <tema>`>. Per una release dell'area euro o del Regno
  Unito aggiungi `eurozone_release` o `britain_release`.
- `Evento`: una riga, cosa è successo quel giorno.
- `Note`: fonte, incertezze, controlli no-look-ahead, strumenti non in lista.

La tabella è l'elenco **completo** degli episodi dello studio: le date scritte nel resto
del testo non vengono raccolte. Un episodio che non sta in tabella per la pipeline non
esiste.

Requisiti sulle date, **critici**:
- almeno **<N, tipicamente 15-25>** episodi;
- formato **YYYY-MM-DD** e nient'altro;
- la data è quella della **seduta di mercato in cui l'asset-proxy reagisce**, non
  quella dell'annuncio: se la notizia esce a mercato chiuso, a mercato locale
  disallineato dal proxy (ETF USA su sottostante asiatico/europeo) o in un
  festivo, usa la prima seduta utile del proxy e **spiegalo nella colonna Note**;
- se una data è incerta fra due fonti, **non metterla in tabella**: scrivi le due
  candidate in prosa e spiega perché — un episodio con la data sbagliata di un giorno
  misura la cosa sbagliata.

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
- [ ] `venv/bin/python build_catalog.py` → lo studio compare in `catalog.yaml`; un ERRORE
      sulla tabella episodi (ticker fuori lista, verso fuori vocabolario, data non ISO)
      blocca la pubblicazione e va corretto nel .md
- [ ] `venv/bin/python analogues.py build` → controllare il delta di episodi
- [ ] `venv/bin/python analogues.py labels --theme <tema>` → la copertura è migliorata?
- [ ] `venv/bin/python analogues.py find --theme <tema> --direction <verso> --direction-reference <ticker>`
      → le righe della tabella entrano nel pool direzionale
- [ ] `venv/bin/python pipeline_tools.py match "<notizia tipo>"` → lo studio esce primo
- [ ] questo prompt cancellato da `_prompts/`
