# Il memorandum USA-Iran scade senza sostituto e il greggio sale per la terza seduta: Brent a 91,5 dollari, prodotti raffinati in fuga

**Data analisi**: 2026-08-18
**Fonte**: Morning Briefing 2026-08-18 (intl 01, intl 02, intl 07, fin 02)
**Slug**: iran-hormuz-memorandum-expiry

---

## Testo notizia (originale)

> Il memorandum d'intesa di 60 giorni firmato a giugno fra Stati Uniti e Iran e' scaduto lunedi senza accordo sostitutivo. Trump ha dichiarato di non essere interessato a estenderlo, ha invitato l'Iran ad 'alzare bandiera bianca' e ha detto di non avere 'alcun calendario' per il conflitto, giunto alla ventiquattresima settimana. Teheran sostiene di aver raggiunto un'intesa con l'Oman sulle rotte di navigazione attraverso lo Stretto di Hormuz, trattativa da cui Washington e' esclusa; Trump ha risposto minacciando di bombardare l'Oman. In parallelo, due droni kamikaze Hadid-110 lanciati da territorio iraniano hanno colpito l'ufficio privato del primo ministro del Kurdistan iracheno a Erbil e la residenza del capo dell'intelligence regionale, e il capo di stato maggiore iraniano ha annunciato una taglia da 30.000 dollari per l'uccisione o la cattura di militari americani. Sui mercati il greggio sale per la terza seduta consecutiva: WTI sopra 85 dollari (+0,90%), Brent vicino a 91,5. I transiti di Hormuz restano una frazione della norma (cinque navi commerciali sabato, zero domenica, contro 31 il fine settimana precedente), ma i produttori del Golfo riescono in parte a spostare i carichi in modo occulto, il che ha frenato il rally. La benzina e' su del 57% e il gasolio del 98% anno su anno: il pass-through passa dai prodotti raffinati piu' che dal benchmark del greggio.

---

## In breve (in parole semplici)

L'accordo temporaneo che teneva dentro un perimetro negoziale la guerra fra Stati Uniti e Iran è scaduto lunedì e il presidente americano ha detto di non volerlo rinnovare. Tradotto: il conflitto — arrivato alla ventiquattresima settimana — non ha più una data di scadenza né un tavolo condiviso, e il traffico di petroliere attraverso lo Stretto di Hormuz (il corridoio marittimo largo poche decine di chilometri da cui passa circa un quinto del petrolio mondiale) resta ridotto a una frazione della norma. Il petrolio sale per la terza seduta di fila, ma il dato più interessante non è il greggio: sono i **prodotti raffinati**. La benzina è su del 57% e il gasolio del 98% rispetto a un anno fa, mentre il greggio "solo" del 38%. Significa che la strozzatura non è tanto sul petrolio estratto quanto sulla capacità di trasformarlo e consegnarlo — ed è per questo che lo shock energetico si sta scaricando sulle aspettative di inflazione più in fretta di quanto suggerisca il prezzo del barile.

La domanda che ci poniamo: quando in passato è saltato un contenimento diplomatico su una rotta marittima strategica, come si sono mossi nei giorni successivi greggio, prodotti raffinati, margine di raffinazione, azionario e volatilità?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | commodity_energy |
| `sub_themes` | shipping_chokepoint, hormuz, iran |
| `sentiment` | bearish (per il rischio: rialzista sull'energia, ribassista sul risk appetite) |
| `confidence` | medium |
| `horizon` | 1-5 giorni di trading |

**Motivazione classificazione**: la notizia è formalmente diplomatica (scadenza di un memorandum), ma il canale di trasmissione ai mercati è interamente energetico — passaggio di navi attraverso Hormuz, premio di rischio sul greggio, prezzi dei prodotti raffinati. Per questo il tema primario è `commodity_energy` e non `geopolitical`: la geopolitica qui è la causa, l'energia è il meccanismo. Il sentiment è `bearish` nel senso di **risk-off con energia in rialzo** — non è una notizia che fa salire il mercato azionario. La confidence è `medium` e non `high` per una ragione precisa: il briefing segnala che i produttori del Golfo stanno riuscendo a spostare i carichi in modo occulto, cioè esiste una valvola di sfogo che ha già smorzato i rally precedenti; e la scadenza del memorandum era ampiamente attesa, quindi parte dell'informazione era già nel prezzo.

Le notizie 02 (droni iraniani su Erbil, contro l'ufficio del primo ministro del Kurdistan iracheno e la casa del capo dell'intelligence regionale) e 07 (taglia da 30.000 dollari annunciata dal capo di stato maggiore iraniano per l'uccisione o cattura di militari americani) sono consolidate qui: non hanno un canale asset proprio, ma sono la stessa escalation vista dal lato militare-retorico e servono a stabilire che il vuoto diplomatico non è una pausa tecnica.

---

## Asset rilevanti

### Primary (canale diretto)

- **BZ=F** (futures sul petrolio Brent, il benchmark di riferimento per il greggio europeo e mediorientale) — il premio di rischio geopolitico si forma qui per primo.
- **CRACK_321** (margine di raffinazione 3-2-1, in dollari al barile: quanto guadagna una raffineria trasformando 3 barili di greggio in 2 di benzina e 1 di gasolio) — è **l'asset più informativo di questa scheda**. Quando la strozzatura è sulla logistica e sulla trasformazione, il margine si allarga anche se il greggio si muove poco.
- **HO=F** (futures sul gasolio da riscaldamento / diesel) — il prodotto raffinato più esposto: +98% anno su anno.
- **RB=F** (futures sulla benzina RBOB) — +57% anno su anno.

### Secondary (effetti indiretti)

- **^GSPC** (indice azionario S&P 500, le 500 maggiori società quotate USA) — canale risk-off generale; nota che il settore energia dentro l'indice compensa in parte.
- **^STOXX50E** (indice azionario Euro Stoxx 50, le 50 blue chip dell'area euro) — l'eurozona è importatore netto di energia, quindi un rincaro del greggio è per lei un trasferimento di reddito verso l'estero.
- **^VIX** (indice di volatilità implicita dell'S&P 500, il cosiddetto "indice della paura": misura quanta oscillazione il mercato delle opzioni si aspetta nei 30 giorni successivi) — termometro del risk-off.
- **GC=F** (futures sull'oro) — bene rifugio classico. ⚠ Su questo asset la direzione storica è dichiarata inaffidabile dalla scorecard corrente: vedi il blocco `GC=F` nella sezione Event study.

---

## Knowledge Base — research correlate

- [score=10] `iran_hormuz/compass_artifact_wf-57769786-924f-41b7-8c1e-36177b05bebd_text_markdown.md` — *Iran – Stretto di Hormuz e il premio geopolitico sul petrolio: regime ed episodi storici (1980–2026)*
  - Perché è rilevante: è la research dedicata esattamente a questo canale — mappa i regimi del premio geopolitico su Hormuz e i loro episodi datati, che è la base della libreria di analoghi usata sotto.
- [score=3] `Russia-Ucraina attrito energetico e regime sanzioni .../Russia-Ucraina- attrito energetico e regime sanzioni ... (2022–2026).md`
  - Perché è rilevante: fornisce il precedente moderno di uno shock energetico da conflitto che si trasmette ai **prodotti** più che al greggio (la crisi del diesel del 2022), che è esattamente la configurazione di oggi.
- [score=3] `ciclo_inflazione_eurozona_2021-2023/Ciclo inflazione Eurozona 2021–2023.md`
  - Perché è rilevante: documenta come uno shock di offerta energetico si trasferisce all'inflazione europea e quindi alla risposta della banca centrale — il secondo anello della catena di oggi.

---

## Regime storico identificato

- **Regime**: conflitto USA-Iran aperto e senza contenitore diplomatico (dal ~marzo 2026 alla data odierna), innestato su un regime globale di **inflazione da offerta con banche centrali sulla difensiva** (aspettative di inflazione a un anno dell'Università del Michigan sopra il 4% per il quinto mese consecutivo).
- **Caratterizzazione**: siamo nella fase in cui il premio di rischio su Hormuz non è più un evento puntuale ma una condizione permanente del mercato — i transiti sono cronicamente bassi (5 navi sabato, 0 domenica, contro 31 il fine settimana precedente di un mese fa) e i produttori hanno sviluppato canali alternativi. Questo ha due implicazioni opposte: da un lato riduce l'ampiezza delle reazioni al singolo titolo (il mercato si è abituato), dall'altro sposta lo stress dal greggio, che ha rotte alternative, ai prodotti raffinati e alla capacità di raffinazione, che non le hanno. È un regime **diverso** dagli shock Hormuz "puri" del 2019 (attacchi alle petroliere a Fujairah, abbattimento del drone USA), in cui il conflitto era episodico e il mercato tornava rapidamente al livello precedente.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla libreria di episodi (Opzione B), filtrato per tema `commodity_energy`, sotto-tema **date-locale** `shipping_chokepoint` (32 episodi disponibili a questo livello, filtro forte) e direzione `neg`, con vincolo di no-look-ahead (`--before 2026-08-18`). Il tetto di recency della libreria ha tenuto i 30 più recenti.

```bash
venv/bin/python analogues.py find --theme commodity_energy \
  --subtheme shipping_chokepoint --direction neg --before 2026-08-18
```

I 30 episodi coprono quattro sotto-famiglie, tutte accomunate dal meccanismo "una rotta marittima o un flusso di greggio viene messo in discussione":

- `2012-01-04`, `2012-01-23` — minacce iraniane di chiusura di Hormuz e adozione dell'embargo europeo sul petrolio iraniano. Analoghi diretti: stesso attore, stessa rotta, stessa logica di braccio di ferro.
- `2014-11-27`, `2015-07-14`, `2016-01-19` — decisione OPEC di non tagliare, accordo nucleare iraniano (JCPOA), revoca delle sanzioni all'Iran. Analoghi "di segno opposto sul flusso" ma appartenenti allo stesso complesso Iran/offerta.
- `2019-05-12`, `2019-05-13`, `2019-06-13`, `2019-07-01`, `2019-09-14`, `2020-01-08` — la sequenza sabotaggi di Fujairah → petroliere nel Golfo dell'Oman → attacco ad Abqaiq → rappresaglia post-Soleimani. È il precedente più stretto per "escalation militare che minaccia il transito".
- `2022-02-24`, `2022-03-08`, `2022-08-15`, `2023-*`, `2024-01-12` (Mar Rosso/Houthi), `2024-10-26`, `2025-06-13`, `2025-06-22`, `2025-06-23`, e la serie `2026-02` → `2026-04` — invasione dell'Ucraina, embargo, attacchi Houthi sul Mar Rosso e la fase acuta della guerra USA-Iran in corso. Sono gli episodi di regime più vicino a oggi.

Non ho potato il pool: la dispersione fra sotto-famiglie è informativa proprio perché mostra quanto poco robusto sia il segno medio (vedi Caveat).

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'BZ=F,CRACK_321,HO=F,RB=F,GC=F,^GSPC,^STOXX50E,^VIX' \
  --events 2012-01-04,2012-01-23,2014-11-27,2015-07-14,2016-01-19,2019-05-12,2019-05-13,2019-06-13,2019-07-01,2019-09-14,2020-01-08,2022-02-24,2022-03-08,2022-08-15,2023-03-10,2023-11-01,2023-12-18,2024-01-12,2024-10-26,2025-06-13,2025-06-22,2025-06-23,2026-02-01,2026-02-17,2026-02-27,2026-02-28,2026-03-08,2026-03-12,2026-04-11,2026-04-17 \
  --windows 1,3,5,10 --markdown
```

Due date (2019-05-13 e 2025-06-23) sono state saltate perché non festive/non quotate o coincidenti con l'ancora di un'altra: N effettivo = **28** su tutti i ticker.

### Risultati

> **Come si leggono le tabelle.** T+1, T+3, T+5, T+10 sono i **giorni di borsa** trascorsi dall'evento (non giorni di calendario): T+10 è circa due settimane. I numeri sono rendimenti **cumulati** dall'evento a quel giorno. La **mediana** è il valore centrale dei 28 episodi (metà sopra, metà sotto) ed è più robusta della media, che si lascia trascinare dai singoli episodi estremi. **p25** e **p75** delimitano il 50% centrale dei casi: se sono di segno opposto, il segnale è debole.

#### `BZ=F` — Brent

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.88% | +1.44% | +2.32% | +3.90% |
| mediana | -0.46% | +1.43% | +1.36% | +0.78% |
| dev std | +4.67% | +5.99% | +10.28% | +12.72% |
| p25 | -2.94% | -1.14% | -2.81% | -4.36% |
| p75 | +1.89% | +3.35% | +5.12% | +9.28% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: nei 28 episodi simili il Brent nel primissimo giorno *scende* leggermente (mediana −0,46%) e poi risale, chiudendo a due settimane con una mediana di appena +0,78% ma una media di +3,90%. Lo scarto fra media e mediana dice che il rialzo dipende da pochi episodi molto violenti (Abqaiq 2019, invasione 2022): nel caso tipico il greggio non fa granché. La banda p25–p75 a T+10 va da −4,4% a +9,3%, cioè comprende comodamente lo zero — **segnale direzionale debole sul greggio**.

#### `CRACK_321` — margine di raffinazione 3-2-1 ($/barile)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.93% | +8.22% | +6.71% | +10.19% |
| mediana | +0.56% | +5.65% | +3.73% | +7.65% |
| dev std | +9.84% | +16.50% | +19.21% | +22.34% |
| p25 | -1.41% | +1.35% | -0.31% | -5.66% |
| p75 | +5.22% | +12.30% | +12.05% | +19.63% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: qui il segnale c'è. A T+3 il margine di raffinazione è salito nel caso tipico del +5,65% e a T+10 del +7,65%, con **media e mediana entrambe positive e concordi** — ed è raro. A T+3 perfino il quartile basso (p25 = +1,35%) è positivo: significa che in oltre tre quarti dei 28 episodi il margine si era allargato entro tre giorni. La lettura economica è pulita: uno shock su una rotta marittima colpisce la logistica e la disponibilità di prodotto finito prima e più del greggio, e chi raffina cattura la differenza. È esattamente la configurazione già visibile oggi (benzina +57%, gasolio +98%, greggio +38% anno su anno).

#### `HO=F` — gasolio/diesel

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.57% | +2.95% | +3.20% | +5.77% |
| mediana | -0.04% | +1.29% | +1.15% | +2.85% |
| dev std | +5.69% | +9.11% | +12.09% | +14.19% |
| p25 | -3.26% | -1.03% | -2.89% | -2.62% |
| p75 | +1.76% | +7.60% | +7.92% | +11.71% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: il diesel sale con più decisione del greggio (mediana +2,85% a due settimane contro +0,78% del Brent), coerente col fatto che è il prodotto in cui la scarsità morde per prima. Ma la banda resta ampia e attraversa lo zero: direzione plausibile, magnitudine incerta.

#### `RB=F` — benzina RBOB

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.35% | +2.58% | +2.80% | +4.34% |
| mediana | -0.54% | +2.39% | +1.04% | +0.35% |
| dev std | +4.32% | +6.41% | +9.49% | +13.24% |
| p25 | -2.16% | -0.07% | -1.10% | -2.63% |
| p75 | +2.08% | +5.09% | +5.50% | +7.46% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: profilo simile al diesel ma più smorzato oltre i 3 giorni (mediana T+10 quasi nulla, +0,35%). La benzina è più legata alla domanda stagionale americana che alla rotta di Hormuz, ed è probabilmente per questo che il segnale si esaurisce prima.

#### `^GSPC` — S&P 500

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.29% | +0.43% | +0.55% | +0.71% |
| mediana | +0.17% | +0.37% | +0.70% | +1.15% |
| dev std | +0.91% | +1.23% | +1.64% | +3.21% |
| p25 | -0.22% | +0.03% | -0.21% | -1.04% |
| p75 | +0.70% | +0.92% | +1.40% | +2.94% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: contro l'intuizione, l'azionario americano nei 28 episodi tende a **salire**, non a scendere (mediana +1,15% a T+10, positiva su tutti gli orizzonti). Questo è il classico effetto "vendi la paura, compra il fatto": lo shock geopolitico su una rotta petrolifera arriva quasi sempre dopo giorni di tensione già scontata, e l'S&P 500 contiene un settore energia che beneficia del rincaro. La dispersione resta bassa (deviazione standard sotto l'1% fino a T+5), il che rende questo uno dei risultati meno rumorosi della scheda.

#### `^STOXX50E` — Euro Stoxx 50

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.24% | -0.11% | -0.41% | -0.54% |
| mediana | +0.24% | +0.27% | +0.03% | -0.86% |
| dev std | +2.21% | +2.28% | +2.69% | +3.84% |
| p25 | -0.56% | -1.67% | -2.30% | -2.78% |
| p75 | +1.32% | +1.36% | +1.35% | +1.47% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: la divergenza con l'S&P 500 è il risultato più interessante della scheda. L'azionario europeo, a differenza di quello americano, tende a **cedere** man mano che passano i giorni (mediana −0,86% a T+10 contro +1,15% dell'S&P 500). Il meccanismo è economico, non finanziario: gli Stati Uniti sono esportatori netti di energia, l'area euro è importatrice netta, quindi lo stesso rincaro del barile è per l'una un trasferimento di reddito in entrata e per l'altra in uscita. L'Euro Stoxx 50 inoltre pesa poco sull'energia e molto su industria e lusso, i settori che il caro-energia penalizza.

#### `^VIX` — indice di volatilità

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -1.02% | -1.53% | -0.73% | +0.73% |
| mediana | -1.90% | -4.23% | -2.48% | -1.55% |
| dev std | +6.73% | +12.29% | +13.85% | +19.73% |
| p25 | -6.87% | -8.96% | -9.15% | -12.96% |
| p75 | +5.99% | +7.32% | +3.87% | +9.92% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: la volatilità implicita **scende** nei giorni successivi (mediana −4,23% a T+3), il che conferma la lettura "sell the fear, buy the fact": nel momento in cui l'evento si materializza, l'incertezza si risolve e il premio pagato per proteggersi si sgonfia. È coerente con l'S&P 500 in rialzo. La dispersione però è enorme (banda p25–p75 da −9% a +4% a T+5): quando la volatilità invece esplode, esplode davvero.

#### `GC=F` — oro

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.31% | -0.03% | -0.09% | -1.14% |
| mediana | +0.10% | -0.22% | -0.29% | -1.20% |
| dev std | +2.02% | +2.17% | +3.84% | +5.17% |
| p25 | -1.01% | -1.40% | -2.05% | -4.16% |
| p75 | +1.42% | +0.83% | +1.60% | +2.86% |
| **N** | **28** | **28** | **28** | **28** |

⚠ **Numeri riportati per completezza, ma NON usati per una direzione attesa.** La scorecard settimanale corrente (2026-W34, sezione "5-bis") classifica `GC=F` come **❌ controproducente**: su 302 previsioni mature l'Information Coefficient per-asset è **−0,07** e l'hit-rate è 47%, cioè la mediana storica ha indicato il segno sbagliato più spesso che giusto. Su questo asset il segno di questa tabella è **inaffidabile** e non ci costruisco sopra un'aspettativa.

---

## Considerazioni qualitative

**Cosa è cambiato davvero ieri.** Non il livello del rischio militare — quello era già alto — ma la sua *struttura temporale*. Un memorandum di 60 giorni è, per un mercato, un'opzione con scadenza: fissa una data entro cui qualcosa deve succedere e permette di prezzare la probabilità di rinnovo. Con la scadenza senza sostituto e l'esplicito disinteresse americano a estenderlo, quell'opzione è scaduta senza essere sostituita. Il conflitto passa da "negoziato con deadline" a "guerra a tempo indeterminato". Per gli asset energetici questo non alza necessariamente il prezzo *oggi*, ma alza il **premio a termine**: la parte lontana della curva dei futures, e con essa le aspettative di inflazione.

**Perché guardare il margine di raffinazione e non il barile.** È la lezione centrale di questa scheda ed è confermata sia dai numeri di oggi sia dall'event study. Il Brent è un prodotto fungibile con molte rotte alternative: se Hormuz si strozza, i produttori del Golfo instradano diversamente (è esattamente ciò che il briefing descrive con i "carichi spostati in modo occulto"), e il prezzo del greggio si assesta. Benzina e gasolio no: sono prodotti che richiedono una raffineria in un posto specifico e una nave adatta per arrivare al consumatore. Quando la logistica si inceppa, il divario fra il prezzo dei prodotti e quello del greggio — cioè il **margine di raffinazione** — si allarga. Il CRACK_321 dell'event study lo mostra con la firma statistica più netta di tutta la scheda: mediana +5,65% a tre giorni con anche il quartile basso positivo. E i dati odierni sono già in quella configurazione: benzina +57% e gasolio +98% anno su anno contro un greggio a +38%.

**La conseguenza macro che chiude il cerchio con la notizia del giorno sui tassi.** Il consumatore e l'impresa non comprano barili di Brent: comprano gasolio, benzina, kerosene ed elettricità. Se i prodotti raffinati corrono al doppio del greggio, l'inflazione percepita e misurata sale più di quanto il prezzo del barile lasci intendere — ed è probabilmente parte della spiegazione del dato che compare altrove nel briefing di oggi: le aspettative di inflazione a un anno dell'Università del Michigan sopra il 4% per il quinto mese consecutivo. Questo è il ponte fra questa scheda e la `news_02` sul selloff sincronizzato delle scadenze lunghe: **è lo stesso shock, visto due anelli più avanti nella catena**.

**La divergenza Europa-Stati Uniti come chiave di lettura operativa.** L'event study separa nettamente due azionari che di solito si muovono insieme: l'S&P 500 sale (mediana +1,15% a T+10), l'Euro Stoxx 50 scende (mediana −0,86%). Vale la pena tenerlo a mente perché è un risultato *strutturale*, non statistico: dipende dal fatto che gli USA sono esportatori netti di energia e l'area euro importatrice netta. In termini contabili semplici, un rincaro del petrolio sposta reddito dai consumatori europei ai produttori americani e mediorientali. Su questa coppia la scorecard corrente è anche relativamente incoraggiante: `^STOXX50E` è fra gli asset marcati **✅ affidabile** (IC +0,17 su 172 previsioni), `^GSPC` è **⚠ debole** (IC +0,10 su 406).

**Cosa smorza la lettura rialzista sull'energia.** Tre cose. Primo, la valvola dei carichi occulti: se il greggio iraniano e del Golfo continua a trovare strada, il premio di scarsità si scarica sui prodotti ma non sul barile — è precisamente ciò che l'event study mostra con Brent debole e crack forte. Secondo, il mercato ha già visto ventiquattro settimane di questa guerra: l'assuefazione riduce l'ampiezza delle reazioni, e infatti l'event study mostra il VIX in *calo* dopo l'evento. Terzo, la scadenza era attesa: le notizie annunciate si prezzano prima, e ciò che resta è il residuo di sorpresa, che qui è modesto.

---

## Glossario — sigle e termini

- **Stretto di Hormuz** — braccio di mare fra Iran e Oman largo circa 33 km nel punto più stretto; ci transita circa un quinto del petrolio consumato nel mondo. Non ha alternative marittime: le rotte via oleodotto (Arabia Saudita verso il Mar Rosso, Emirati verso Fujairah) hanno capacità molto inferiore.
- **CRACK_321** — margine di raffinazione "3-2-1": il ricavo teorico di una raffineria che trasforma 3 barili di greggio in 2 di benzina e 1 di gasolio, meno il costo del greggio. Formula usata nel progetto: `(2×RB=F + 1×HO=F) × 42 / 3 − BZ=F`, in dollari al barile (il 42 converte i prodotti da dollari/gallone a dollari/barile). Il greggio di riferimento è il **Brent**, non il WTI, perché il canale di interesse è europeo/mediorientale.
- **BZ=F** — futures sul petrolio Brent, il greggio di riferimento del Mare del Nord usato come benchmark per due terzi del petrolio scambiato al mondo.
- **HO=F** — futures sull'*heating oil*, il gasolio da riscaldamento, usato come proxy quotato del diesel.
- **RB=F** — futures sulla benzina RBOB (*Reformulated Blendstock for Oxygenate Blending*), il contratto benzina di riferimento americano.
- **^GSPC** — indice azionario S&P 500 (le 500 maggiori società quotate statunitensi).
- **^STOXX50E** — indice azionario Euro Stoxx 50 (le 50 principali società dell'area euro).
- **^VIX** — indice della volatilità implicita a 30 giorni sull'S&P 500, ricavato dai prezzi delle opzioni. Sale quando il mercato paga di più per proteggersi.
- **GC=F** — futures sull'oro.
- **WTI** — *West Texas Intermediate*, il greggio benchmark americano; tipicamente quota qualche dollaro sotto il Brent.
- **Pass-through** — la quota di un rincaro all'origine (il barile) che arriva effettivamente al prezzo finale pagato da famiglie e imprese.
- **Premio di rischio geopolitico** — la parte del prezzo di una materia prima che non riflette domanda e offerta correnti ma la probabilità che l'offerta futura venga interrotta.
- **T+1 / T+3 / T+5 / T+10** — giorni di **borsa** (non di calendario) trascorsi dalla data dell'evento; i rendimenti sono cumulati dall'evento a quel giorno.
- **Mediana vs media** — la mediana è il valore centrale del campione (metà episodi sopra, metà sotto) e resiste agli episodi estremi; la media li incorpora. Quando le due divergono molto, il risultato dipende da pochi casi.
- **p25 / p75** — primo e terzo quartile: fra loro sta il 50% centrale degli episodi. Se hanno segno opposto, il campione non indica una direzione.
- **IC (Information Coefficient)** — correlazione di rango fra la previsione della scheda e il movimento realizzato, calcolata a parità di asset. Sopra zero = lo storico contiene informazione; sotto zero = è sistematicamente rovesciato.

---

## Caveat

- **N = 28 su tutti i ticker**: sopra la soglia di 10 sotto la quale il progetto flagga "indicative only", quindi il campione è utilizzabile — ma resta piccolo in senso statistico assoluto.
- **Regime-mixing dichiarato.** I 28 episodi non appartengono a un unico regime: includono le minacce iraniane del 2012 (regime di sanzioni pre-JCPOA), la distensione del 2015–16, gli attacchi episodici del 2019, lo shock russo del 2022 e la guerra USA-Iran in corso. Il regime attuale — conflitto prolungato con rotte alternative già rodate — è **strutturalmente diverso** dagli shock puntuali del 2019, in cui il mercato tornava rapidamente al livello precedente. Questa eterogeneità è visibile nelle deviazioni standard molto ampie e va letta come un limite reale, non come rumore da ignorare.
- **`GC=F` (oro): direzione inaffidabile** per decisione della scorecard 2026-W34 (IC per-asset −0,07 su N=302, ❌ controproducente). Tabella riportata, nessuna aspettativa derivata.
- **Notizia parzialmente attesa.** La scadenza del memorandum era su calendario: parte dell'informazione era già nei prezzi prima dell'evento, il che comprime meccanicamente i rendimenti post-evento e può far apparire "debole" una reazione che in realtà è già avvenuta prima.
- **Correlazione ≠ causazione.** In diversi episodi del pool (2022-02-24, 2022-03-08) altre notizie di grande portata si sovrappongono nella stessa finestra: l'event study attribuisce all'evento anche ciò che è dovuto al contesto.
- **Il pool non è stato potato.** Ho scelto di non rimuovere gli episodi di segno "distensivo" (2015-07-14 JCPOA, 2016-01-19 revoca sanzioni) perché la libreria li classifica già come direzione `neg` per l'asset di riferimento e perché escluderli a posteriori avrebbe introdotto una selezione favorevole all'ipotesi. Chi rifà l'analisi con un pool più stretto otterrà quasi certamente segnali più forti — e più fragili.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-17T08:04:03
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
