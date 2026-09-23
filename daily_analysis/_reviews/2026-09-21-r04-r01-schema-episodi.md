# R04 + R01 — Schema comune degli episodi: progettazione

Run 5a del piano di revisione pipeline. **Solo design: nessun codice di produzione.**
L'implementazione è il Run 5b.

Origine: `2026-09-15-revisione-pipeline.md`, ID R01 (ingestione KB che non alimenta i
filtri direzionali) e R04 (validazione dei metadati incompleta, due parser divergenti).

---

## 1. Il problema, come si è rivelato sui dati

Il report descrive R01 come «l'ingestione KB non produce `directions_by_reference`». Vero,
ma l'ispezione dei file reali ha cambiato la forma del problema:

**Le research hanno già una tabella di episodi.** 18 studi su 29, con colonne quasi
identiche fra loro:

```
| Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead |
```

Le date non mancano: `harvest_kb` le pesca tutte, e ognuna è già in libreria. Manca che
**direzione e asset siano campi invece che prosa**. Il filtro di `cmd_find` scarta senza
appello un episodio privo di direzione dichiarata per l'asset richiesto
([analogues.py:682](../../news_impact_pipeline/analogues.py)):

```python
eps = [e for e in eps if set(e.get("directions_by_reference", {}).get(reference, [])) == {direction}]
```

Non è un degrado: è esclusione, contata nel messaggio come «esclusi N senza riferimento».
Quindi una research catalogata contribuisce date che nessun pool direzionale userà mai.

**Lo stesso difetto è nelle schede, ed è più grande.** Le schede di agosto compilano il
blocco dichiarato ma non il campo `direction_reference`; a settembre lo compilano solo
dal giorno 14 in poi. Le loro righe dichiarate sono inutilizzabili per la stessa ragione.

**Cosa distingue le righe che funzionano.** Non un'euristica: tre regole scritte nel
template della scheda nel momento in cui qualcuno scrive.

1. un solo asset di riferimento, dichiarato esplicitamente → «verso» non è mai ambiguo;
2. vocabolario chiuso `pos` / `neg` / `neutral`, non prosa;
3. la convenzione detta sul posto (bond = prezzo, FX = quotazione del ticker) e
   `pos, neg` che **esclude** invece di indovinare.

Le tabelle delle research falliscono su tutte e tre perché sono state scritte prima che
quel contratto esistesse. **Il disegno è portare quel contratto sulle research, non
inventarne un altro.**

---

## 2. Il record comune: una forma, tre superfici

Esiste un unico tipo di record di episodio dichiarato:

| campo | obbligatorio | valore |
|---|---|---|
| `date` | sì | ISO `YYYY-MM-DD`, non futura |
| `reference` | sì | un ticker presente in `assets` |
| `direction` | sì | `pos` \| `neg` \| `neutral`, oppure insieme ambiguo → esclusione |
| `mechanism` | sì | token canonici di `subtheme_taxonomy.yaml` |
| `description` | sì | testo libero, una riga |
| `source` | sì | provenienza: `card:<giorno>/<file>` oppure `kb:<percorso>` |
| `theme` | sì | ereditato dal documento (`primary_theme`), già normalizzato |

Tre superfici lo producono, e sono **già tutte e tre presenti nel progetto**:

- **scheda giornaliera** — blocco `| Data | Verso | Meccanismo | Descrizione |`,
  `reference` dal campo `direction_reference` di scheda. **Non cambia.**
- **research KB** — tabella a cinque colonne (§3). `reference` dalla colonna.
- **registro revisioni** — `knowledge_base/_direction_reviews.yaml`, righe
  `date / theme / reference / direction / source / reason`. **Ha già questa forma.**

Un solo parser produce il record dalle tre superfici. È così che si chiude la richiesta
«un solo parser YAML per catalogo ed episodi» del Run 5b senza toccare le schede.

> **Nota di riuso.** Il registro revisioni non è un meccanismo da costruire: esiste, è
> letto e validato da `cmd_build`, e alimenta già `directions_by_reference`. Il conteggio
> corrente si legge con il comando in §9.

---

## 3. Formato della tabella nelle research

```
| Data | Asset | Verso | Meccanismo | Evento |
|---|---|---|---|---|
| `2024-08-05` | `^VIX`  | pos | carry_unwind | unwind del carry sullo yen |
| `2024-08-05` | `JPY=X` | neg | carry_unwind | lo yen si rafforza contro dollaro |
```

**Una riga per coppia (data, asset).** Scelta del maintainer: è la traduzione diretta di
come le research già ragionano — `SOXX: neutral / XLU: pos` diventa due righe — e non
obbliga a riorganizzare la tabella per asset.

Regole, identiche alla scheda e per gli stessi motivi:

- `Verso` è la **pressione attesa sul prezzo del ticker**, con l'informazione disponibile
  all'epoca dell'evento. Non è un giudizio sull'evento, e non è il segno del rendimento
  misurato dopo.
- `pos, neg` sulla stessa coppia (data, asset) significa «genuinamente ambiguo» e la
  esclude dai pool direzionali. È una dichiarazione, non una mancanza.
- `Meccanismo` sono token canonici; la geografia resta un token (`eurozone_release`,
  `britain_release`), non una colonna.
- `Evento` **si conserva**. Oggi il parser legge tre colonne e butta la descrizione;
  `MEMORY.md` ha aperta la voce «persistere le descrizioni», misurata il 21/08 su 129
  righe riscritte a memoria dall'agente di cui 119 già in libreria.

La colonna `Note no-look-ahead` delle research **resta prosa e resta dov'è**: serve a chi
legge, non al motore.

---

## 4. Campi che NON entrano, e quando aggiungerli

R01 elenca nove attributi. Cinque diventano campi; gli altri no, con il motivo e
l'innesco che li farebbe entrare:

| attributo | decisione | innesco per aggiungerlo |
|---|---|---|
| geografia | già token di meccanismo dal 26/08 | un filtro geografico che i token non sappiano esprimere |
| incertezza | già espressa da `pos, neg` → esclusione | serve graduare l'incertezza, non solo dichiararla |
| istituzione | fuori | un filtro per istituzione emittente |
| data/ora dell'annuncio | fuori | prezzi infragiornalieri nel DB (oggi sono giornalieri: non calcolabile) |
| fonte per singola riga | fuori | una research che citi documenti eterogenei per riga |

Principio: un campo entra quando un filtro lo chiede, non perché il report lo elenca.

---

## 5. Schema validato

### 5.1 Metadati del documento (chiude R04)

| campo | tipo richiesto |
|---|---|
| `title` | stringa non vuota |
| `date_compiled` | data YAML, non futura |
| `primary_theme` | token dell'ontologia §6.1 |
| `sub_themes`, `keywords` | lista di stringhe |
| `relevant_assets` | lista di ticker |
| `time_window` | **mappa** `{start: data, end: data \| present}` |
| `regime_phases` | **lista** di mappe a chiave singola, valore `YYYY-MM-DD to (YYYY-MM-DD \| present)` |

`time_window` e `regime_phases` sono i due campi che oggi passano come stringa. È da lì
che `monthly_digest.kb_regimes` estrae il carattere `)` come fase corrente: la riga fa
`phases[-1]`, e su una stringa l'ultimo elemento è l'ultimo **carattere**. Tipizzare il
campo chiude il bug alla radice, senza toccare `kb_regimes`.

La forma canonica non va inventata: è già quella che la quasi totalità degli studi usa.
Il comando in §9 dice quanti file deviano oggi.

### 5.2 Righe dichiarate

- `date`: ISO, non futura. Una data non ISO **non è un errore**: è una riga non
  indicizzabile, segnalata e saltata (la convenzione editoriale «scrivi non-ISO le date
  da non indicizzare» resta valida come comodità, ma non è più la difesa del motore).
- `reference`: deve esistere in `assets`. Oggi è un warning nel catalogo: per una riga
  dichiarata diventa **errore**, perché una dichiarazione su un ticker inesistente non
  potrà mai produrre un event study.
- `direction`: solo i tre token ammessi; qualsiasi altra cosa rende la riga non
  dichiarata (com'è oggi in `declared_episodes`).
- `mechanism`: token normalizzati da `_norm_label`; nessun token nuovo viene creato in
  silenzio — un token fuori tassonomia è segnalato.

### 5.3 Pubblicazione atomica

Indici costruiti in un file temporaneo, validati, e pubblicati solo se interi. Un errore
**nomina il file e non pubblica niente**: mai un catalogo degradato in silenzio. La
scoperta dei file è condivisa fra scanner e builder (oggi `index_studies.sh` considera
indicizzata un'intera cartella se un qualsiasi Markdown contiene un fence YAML).

---

## 6. Precedenza fra tabella e prosa

- Research **con** tabella dichiarata → la tabella è l'autorità per quel file. La pesca
  euristica delle date in prosa **si spegne** per quel documento.
- Research **senza** tabella → comportamento attuale invariato.

È la stessa regola che vale già per le schede («se la scheda dichiara l'episodio, i suoi
campi vincono sull'euristica»), e chiude la parte di R03 sulle date spurie: il falso
episodio `structural_themes` nasce da una data citata in una nota tecnica, cioè prosa.

Misurato il 2026-09-21: la grande maggioranza delle date estratte è già in tabella, e le
date fuori tabella si concentrano nei due studi che una tabella non ce l'hanno
(`iran_hormuz`, `brexit`). Comando in §9 per rifare il conto.

---

## 7. Recupero delle righe già scritte

Il maintainer ha chiesto esplicitamente che il recupero copra **sia le research sia le
schede senza asset di riferimento**. Il contratto e le regole sono gli stessi per
entrambe.

> **Aggiornamento 2026-09-23 (Run 5d):** il maintainer ha deciso di **non** recuperare le
> schede. Il loro Verso non aveva un asset né distingueva attesa ed esito (template di agosto:
> «il verso di quell'episodio»); vedi la nota nel Run 5d del piano. Il recupero copre solo le research.

### 7.1 Chi scrive la dichiarazione

La conversione la fa **l'agente in sessione, leggendo**, non una regex. Motivo misurato:
su un campione delle righe reali solo una minoranza si converte in modo meccanico; la
maggioranza richiede di conoscere la convenzione del ticker, e un'euristica del tipo
«debole → neg» scriverebbe il segno **rovesciato** su tutta la colonna FX.

Questo è coerente col vincolo di CLAUDE.md, non un'eccezione: il classificatore è
l'agente nella sessione, Python espone solo tool deterministici. È lo stesso schema del
giornaliero.

### 7.2 La regola non negoziabile della conversione

**Quando si decide il verso non si apre il database dei prezzi.** Mai.

Il verso dichiarato è la pressione **attesa all'epoca**. Se si leggesse l'esito e lo si
scrivesse come attesa, la scorecard confronterebbe le previsioni con esiti copiati dentro
le previsioni stesse: misurerebbe la propria copiatura e riporterebbe un'accuratezza
priva di significato.

Caso reale che lo rende concreto — research Regno Unito:

```
| 2016-06-23 | Giorno del referendum (voto) | GBP ↑ se Remain (atteso) | `GBPUSD=X` |
  Note: alle 22:00 il mercato prezzava Remain (~$1.50); esito ignoto fino a notte
```

La sterlina crollò. La dichiarazione corretta è **`pos`**, cioè il contrario dell'esito.

Le research distinguono già le due cose da sole. Riga reale da «Sorprese macro»:
`equity su atteso, realizzato debole` → si prende `pos`, il resto della frase si ignora.

**Regola del verso (DECISA dal maintainer il 2026-09-23):** l'attesa è la **sorpresa
rispetto a quanto il mercato aveva già prezzato**, non il meccanismo in astratto. Emersa dal
pilota BoJ, dove research («un rialzo rafforza lo yen») e schede («il rialzo era scontato, la
guidance accomodante ha indebolito lo yen») dichiaravano versi opposti per lo stesso giorno.

### 7.3 I quattro gruppi

Ogni riga ricade in uno dei quattro, e il Run 5b deve trattarli diversamente.

**Gruppo 1 — traduzione diretta.** La research già scrive per asset:
`2024-09-20 · SOXX: neutral / XLU: pos / ^NDX: neutral` → tre righe, nessun giudizio.

**Gruppo 2 — applicazione della convenzione.** Il verso narrativo va tradotto nel verso
sul ticker. Tavola minima, da estendere in implementazione:

| forma narrativa | ticker | dichiarazione | perché |
|---|---|---|---|
| «JPY debole» | `JPY=X` | `pos` | `JPY=X` è USD/JPY: yen debole = quotazione in salita |
| «JPY forte» | `JPY=X` | `neg` | inverso del precedente |
| «rendimenti su» | `^TNX`, `^TYX`, `^FVX` | `pos` | questi ticker quotano il **rendimento** |
| «prezzo bond giù» | `IEF`, `IEAG.AS`, `1482.T` | `neg` | qui il ticker quota il **prezzo** |
| «risk-off» | `^VIX` | `pos` | volatilità attesa in salita |
| «risk-off» | `GC=F` | `pos` | domanda di rifugio |
| «risk-off» | `^GSPC`, `^GDAXI`, `^STOXX50E` | `neg` | pressione sull'azionario |
| «spread in allargamento» | `BTP_BUND_SPREAD` | `pos` | il ticker quota lo spread: sale anche se è cattiva notizia |

⚠ La tavola codifica la convenzione già scritta nel template della scheda («per i bond è
il prezzo, non il rendimento; per FX è la quotazione del ticker»). Non è nuova: è resa
esplicita perché è il punto dove un errore non si vede.

**Gruppo 3 — si chiede al maintainer.** La prosa non contiene la risposta che il
contratto richiede. Caso reale: `2016-06-24 · GBP ↓↓, risk-off` elenca fra gli asset
anche `EURUSD=X`, su cui il risk-off tira in due direzioni (dollaro rifugio contro euro
vittima del caos europeo) e **la riga non lo dice**. La coppia resta senza dichiarazione
— cioè si comporta come oggi — finché il maintainer non decide. Nessuna riga viene
riempita per completezza.

Rientrano qui: asset marcati `(ctrl)` (termine di paragone o canale?), celle che nominano
un canale anziché un asset (`Canale 1`), righe il cui verso riguarda uno strumento non
presente in `assets`.

**Gruppo 4 — esclusione con motivo.** Il contratto scopre righe non calcolabili a
prescindere dalla qualità della conversione: date anteriori alla copertura del DB prezzi
(le research lo annotano già, «Pre-2011, non calcolabile»), ticker non in `assets`. Queste
producono una riga di esclusione **con motivo scritto**, non una sparizione silenziosa.
Il registro revisioni ha già `status: excluded` con `reason` per questo.

### 7.4 Dove finiscono le dichiarazioni approvate

Nel registro esistente `knowledge_base/_direction_reviews.yaml`, estendendo il vincolo
di provenienza di [analogues.py:479-485](../../news_impact_pipeline/analogues.py) per
accettare come `source` anche una research, non solo una scheda giornaliera. Il controllo
di integrità si conserva nella forma equivalente: **la fonte deve dichiarare quella data
nella propria tabella**, altrimenti errore.

Motivazione: quel file ha già quasi tutti i campi del record comune, è già validato, è già
letto da `cmd_build`, e il maintainer lo ha già compilato a mano decine di volte.
Aggiungere un formato parallelo sarebbe un secondo meccanismo per lo stesso scopo.

⚠ **Due campi mancano e vanno aggiunti al registro**, altrimenti la conversione perde
informazione che la research aveva:

- `mechanism` — i token della colonna `Meccanismo`. Senza, la riga recuperata entra nei
  pool per tema ma non risponde ai filtri `--subtheme`, che sono il livello che discrimina.
- `description` — il testo della colonna `Evento`. Il campo `reason` esistente motiva la
  **decisione di revisione**, non descrive l'evento: sono due cose diverse e accorparle
  farebbe perdere l'una o l'altra.

Entrambi restano opzionali per le 71 righe già compilate a mano, che non li hanno: la
validazione non deve invalidare retroattivamente il lavoro già fatto.

Le **proposte non ancora approvate** stanno in un file separato che il builder non legge.
Vale la convenzione già attiva: un percorso con un componente che inizia per `_` è escluso
da catalogo e libreria, quindi una proposta non può entrare per sbaglio.

### 7.5 Stati e garanzia

Ogni riga proposta porta accanto la **citazione testuale della riga originale**, così la
revisione confronta senza riaprire la research. La coda di revisione è ordinata per
rischio: prima i gruppi 2 e 3, dove l'errore è probabile e invisibile.

**Garanzia:** una riga non approvata non viene usata. Il sistema in ogni momento
intermedio si comporta esattamente come oggi, mai peggio. Il recupero è incrementale e
può fermarsi in qualsiasi punto senza lasciare uno stato rotto.

---

## 8. Confini di questo disegno

- **Run 6 (`event_id`)** non è anticipato. La chiave della libreria resta `(date, theme)`
  e continua a fondere eventi diversi nello stesso giorno. Il record `(data, asset)` è
  però compatibile: il Run 6 aggiunge identità all'evento senza rifare questa migrazione.
- **Nessuna nuova research.** Il vincolo del piano resta: finché il Run 5b non è chiuso
  non si commissionano deep research, e Claude non le scrive né ne scrive i prompt.
- **Le conversioni non sono ricerca.** Riscrivono in forma di campo ciò che il maintainer
  ha già scritto in prosa; non aggiungono episodi, non aggiungono fonti, non aggiungono
  date.
- **Nessun indicatore persistito.** Le dichiarazioni sono input, non risultati.

---

## 9. Comandi per rifare le misure

I conteggi di questo documento sono la fotografia del 2026-09-21. Non fidarsi: rifare.

```bash
cd /Users/riccardo/Claude/mercati_finanza
V=news_impact_pipeline/venv/bin/python

# studi indicizzati, episodi in libreria, qualità della libreria
grep -m1 num_entries  knowledge_base/catalog.yaml
grep -m1 num_episodes knowledge_base/_episodes.yaml
$V news_impact_pipeline/analogues.py stats

# quanti episodi hanno una direzione per asset (il numero che questo lavoro muove)
$V -c "import yaml;e=yaml.safe_load(open('knowledge_base/_episodes.yaml'))['episodes'];\
print(sum(1 for x in e if x.get('directions_by_reference')),'/',len(e))"

# revisioni già compilate a mano
$V -c "import yaml;r=yaml.safe_load(open('knowledge_base/_direction_reviews.yaml'))['reviews'];\
print(len(r),'revisioni;',sum(1 for x in r if x.get('direction')),'con direzione')"

# metadati che deviano dallo schema (time_window / regime_phases non tipizzati)
$V -c "import yaml;c=yaml.safe_load(open('knowledge_base/catalog.yaml'));\
print([e['source_file'] for e in c['entries'] if not isinstance(e.get('time_window'),dict) \
or not isinstance(e.get('regime_phases'),list)])"

# schede che dichiarano episodi ma non l'asset di riferimento
$V -c "
import sys,re;sys.path.insert(0,'news_impact_pipeline')
from pathlib import Path
from analogues import declared_episodes,_field
n=m=0
for d in sorted(Path('daily_analysis').iterdir()):
    if not (d.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}',d.name)): continue
    for c in d.glob('news_*.md'):
        t=c.read_text(encoding='utf-8')
        if not declared_episodes(t): continue
        n+=1
        if not _field(t,'direction_reference').strip('\` '): m+=1
print(f'{m}/{n} schede con blocco ma senza direction_reference')"
```

---

## 10. Cosa deve decidere il Run 5b, non questo run

- Il formato esatto del file di proposta e il comando che lo produce.
- Come lo scanner rileva rimozioni e rinomine (manifest basato sui contenuti).
- ~~Se la tabella delle research debba essere riscritta nel `.md` oppure restare prosa~~
  **DECISO dal maintainer il 2026-09-21: la research resta com'è.** Le dichiarazioni
  vivono nel registro; nessuno script riscrive i `.md` delle research. Da non
  rinegoziare nel Run 5b.
- L'ordine di lavorazione fra research e schede di agosto.
