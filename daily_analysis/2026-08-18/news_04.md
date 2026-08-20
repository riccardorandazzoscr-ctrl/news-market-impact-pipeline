# L'auto blocca l'intesa Canada-USA a 36 ore dai dazi al 50%: Washington ferma al 15% minimo, Ottawa chiede il 10%

**Data analisi**: 2026-08-18
**Fonte**: Morning Briefing 2026-08-18 (fin 07)
**Slug**: canada-us-tariff-deadline

---

## Testo notizia (originale)

> A circa 36 ore dalla scadenza del 19 agosto, Bloomberg riporta che il dossier automobilistico e' il principale ostacolo a un'intesa commerciale fra Canada e Stati Uniti. Il Canada ha spinto per portare al 10% l'aliquota sui veicoli o per allargare l'esenzione per la componentistica di origine americana montata nei veicoli; l'amministrazione Trump e' rimasta ferma su un minimo del 15%. Il pacchetto piu ampio prevedrebbe che Washington riduca i dazi su auto, acciaio, alluminio e prodotti forestali canadesi in cambio di concessioni canadesi su alcolici, latticini, appalti pubblici e quote di export di acciaio e alluminio. I funzionari canadesi dicono che il valore delle riduzioni offerte resta sotto le richieste di Ottawa; le due parti continuano a incontrarsi ogni giorno. I nuovi prelievi sono imposti in base alla Section 338, dopo che la Corte Suprema a febbraio ha annullato i dazi precedenti. Sui mercati: dollaro canadese a 1,387 contro il dollaro USA, equity bancario, ferroviario e della componentistica auto canadese, catene di fornitura nordamericane; il TSX si e' gia ritirato da un massimo storico. Mercoledi mette alla prova anche la nuova base giuridica, il che conta ben oltre il Canada.

---

## In breve (in parole semplici)

Mercoledì 19 agosto entrano in vigore dazi americani del 50% sulle merci canadesi, a meno che un accordo non li fermi. A 36 ore dalla scadenza le due delegazioni sono ancora ferme su un solo punto: l'auto. Washington non scende sotto il 15% di dazio sui veicoli, Ottawa non sale sopra il 10%. Cinque punti percentuali di distanza fra un accordo e un dazio del 50%.

Perché il settore auto e non l'acciaio o il legname: Stati Uniti e Canada non hanno due industrie automobilistiche, ne hanno **una sola distribuita su due paesi**. Un componente attraversa il confine più volte prima di diventare un'auto finita, e ogni attraversamento pagherebbe il dazio. È il settore in cui una tariffa fa più danni per punto percentuale, ed è quindi anche quello su cui nessuno dei due può cedere facilmente.

C'è un secondo livello, meno visibile e forse più importante. I dazi precedenti erano stati annullati dalla Corte Suprema a febbraio; questi si appoggiano a una base giuridica diversa, la Section 338. Mercoledì non si testa solo un accordo commerciale, si testa se il nuovo strumento regge — e la risposta vale per tutti gli altri partner commerciali degli Stati Uniti, non solo per il Canada.

La domanda che ci poniamo: quando in passato una escalation tariffaria si è materializzata, come si sono mossi nei giorni successivi dollaro canadese, azionario americano ed europeo, rame e volatilità?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | regulatory |
| `sub_themes` | tariff_escalation |
| `sentiment` | bearish |
| `confidence` | medium |
| `horizon` | 1-10 giorni di trading |

**Motivazione classificazione**: i dazi sono una misura amministrativa unilaterale, quindi `regulatory` e non `geopolitical` (che nel nostro schema copre conflitti e tensioni diplomatiche) né `macro_data`. Il sotto-tema canonico è `tariff_escalation`, che nella libreria ha 16 episodi a livello date-locale — il massimo disponibile per questo tema. Il sentiment è `bearish`: la notizia dice che la trattativa è bloccata a poche ore dalla scadenza, quindi la probabilità implicita di dazi al 50% è salita. La confidence è `medium` per un motivo strutturale del dossier tariffario: nel regime iniziato nel 2025 le scadenze sono state posticipate o annacquate più volte di quanto non siano state rispettate, e il mercato lo ha imparato — la reazione a un annuncio è quindi smorzata dall'aspettativa di una proroga dell'ultimo minuto.

Sull'affidabilità del tema: la scorecard 2026-W34 dà a `regulatory` una copertura del 66% (la migliore di tutti i temi, cioè bande ben tarate) con hit-rate 55% e IC **+0,05** su 84 previsioni. Contenuto informativo modesto ma positivo.

---

## Asset rilevanti

### Primary (canale diretto)

- **CAD=X** (cambio dollaro USA/dollaro canadese: un numero più alto = dollaro canadese più debole; oggi a 1,387) — il canale più diretto e pulito. Il Canada esporta circa tre quarti delle sue merci verso gli Stati Uniti: un dazio è, in prima approssimazione, uno shock sui termini di scambio canadesi. Ticker aggiunto al database il **2026-08-16**, due giorni fa, proprio perché questo canale mancava.
- **^GSPC** (S&P 500) — i dazi colpiscono anche i produttori americani che comprano componenti canadesi, e comprimono i margini.

### Secondary (effetti indiretti)

- **^STOXX50E** (Euro Stoxx 50) — il canale non è il commercio Canada-Europa ma il **precedente giuridico**: se la Section 338 regge, l'Unione Europea è il prossimo bersaglio plausibile.
- **^VIX** (volatilità implicita S&P 500) — misura se il mercato tratta la scadenza come un rischio o come teatro negoziale.
- **HG=F** (rame) — proxy della domanda industriale nordamericana e delle catene di fornitura manifatturiere.
- **CNY=X** (cambio dollaro/yuan onshore) — la Cina è stata il bersaglio originario del regime tariffario; lo yuan si muove sulle notizie di dazi anche quando non la riguardano direttamente, come termometro del regime commerciale globale.
- **DX-Y.NYB** (indice del dollaro) — ⚠ direzione storicamente inaffidabile, vedi sotto.

⚠ Manca il canale più specifico: **azionario canadese**. Il TSX (l'indice della borsa di Toronto) non è nell'universo di 46 asset del progetto, e il briefing segnala che si è già ritirato da un massimo storico. Questa è una lacuna reale — vedi Caveat.

---

## Knowledge Base — research correlate

- [score=1] `Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)/...md`
  - Perché è rilevante: è **la** research del tema, e da essa proviene la maggior parte degli episodi del pool. Documenta i due regimi tariffari (2018-19 Cina-centrico, 2025-26 universale) e la loro diversa trasmissione ai mercati.
- [score=1] `ASEAN : Sud-Est asiatico- shock geopolitici — regime ed episodi storici (2010–2026)/...md`
  - Perché è rilevante: marginalmente — copre il lato dei paesi terzi colpiti da riallineamenti tariffari.

Nota: il punteggio di match è basso (1) perché il catalogo non contiene una research su **USMCA / commercio nordamericano** né sull'architettura giuridica delle deleghe tariffarie americane (Section 232, 301, IEEPA, 338). È una lacuna già segnalata il 2026-08-17, con prompt di deep research pronto in `knowledge_base/_prompts/dazi-usa-canada-usmca-base-legale.md` (non ancora eseguito).

---

## Regime storico identificato

- **Regime**: dazi come strumento ordinario e ricorrente di politica estera economica (2025 → oggi), in una **fase di incertezza giuridica** apertasi con la sentenza della Corte Suprema di febbraio 2026.
- **Caratterizzazione**: questo regime differisce in tre modi da quello del 2018-19, ed è la ragione per cui gli episodi più vecchi del pool vanno pesati meno. (1) **Il bersaglio è universale, non cinese**: nel 2018-19 i dazi erano essenzialmente uno strumento contro la Cina, e il mercato poteva riallocare verso altri fornitori; oggi colpiscono alleati (Canada, Unione Europea) e le catene di fornitura non hanno una via di fuga geografica ovvia. (2) **L'aliquota è di un altro ordine di grandezza**: 50% contro il 10-25% del primo ciclo. (3) **La base giuridica è contestata**: la Corte Suprema ha annullato a febbraio i dazi imposti con lo strumento precedente, e la Section 338 — una norma del 1930 mai usata prima in modo sistematico — è il ripiego. Un dazio che potrebbe essere annullato da un tribunale ha un effetto economico diverso da uno stabile: le imprese esitano a riorganizzare le catene di fornitura per una misura che potrebbe sparire, il che *aumenta* il danno da incertezza pur riducendo quello da tariffa.
- **Un elemento di regime specifico a questa notizia**: la distanza fra le parti è di 5 punti percentuali (15% contro 10%) su un solo capitolo. È un divario piccolo in termini economici — abbastanza da rendere un accordo tecnicamente facile — ma è diventato una questione di principio per entrambi. Questa configurazione (gap piccolo, posta enorme) produce storicamente accordi all'ultimo minuto o proroghe, più che rotture.

---

## Event study

### Episodi storici analoghi selezionati

Pool dalla libreria (Opzione B), tema `regulatory`, sotto-tema **date-locale** `tariff_escalation` (16 episodi a questo livello — è la copertura massima del tema, filtro forte), direzione `neg`, no-look-ahead a `2026-08-18`. Il pool non raggiunge il tetto di recency, quindi è completo.

```bash
venv/bin/python analogues.py find --theme regulatory \
  --subtheme tariff_escalation --direction neg --before 2026-08-18
```

I 16 episodi si dividono in due blocchi nettamente diversi:

- **2018-03-22 → 2019-08-12 (10 episodi)** — il primo ciclo di guerra commerciale: annuncio dei dazi Section 301 sulla Cina (22 marzo 2018), dazi su acciaio e alluminio verso alleati inclusi Canada e Unione Europea (1° giugno 2018, i cui annunci gravitano attorno al 15 giugno), le tranche successive di ottobre e dicembre 2018, la rottura del negoziato del maggio 2019 e l'annuncio della tranche di settembre (agosto 2019). Analoghi buoni per il **meccanismo**, deboli per il **regime** (aliquote più basse, bersaglio cinese).
- **2024-12-15 → 2025-04-30 (6 episodi)** — la fase corrente: le prime minacce del 25% su Canada e Messico (dicembre 2024 - gennaio 2025), l'entrata in vigore di marzo, il "Liberation Day" del 2 aprile 2025 con la tariffa universale. **Analoghi molto più stretti**: stesso regime, stesso strumento, in parte stesso bersaglio (il Canada compare direttamente).

Non ho potato il pool: con N=16 già al limite, escludere il blocco 2018-19 lo porterebbe a 6, sotto la soglia di utilizzabilità. Il costo è il regime-mixing, che dichiaro esplicitamente nei Caveat.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'CAD=X,^GSPC,DX-Y.NYB,^STOXX50E,^VIX,CNY=X,HG=F' \
  --events 2018-03-22,2018-06-15,2018-07-02,2018-09-17,2018-10-10,2018-10-29,2018-12-26,2019-02-19,2019-05-13,2019-08-12,2024-12-15,2025-01-01,2025-01-14,2025-02-27,2025-04-02,2025-04-30 \
  --windows 1,3,5,10 --markdown
```

N = **16** su tutti i ticker.

### Risultati

> ⚠ **N = 16.** Sopra la soglia formale di 10 sotto cui il progetto flagga "indicative only", ma **appena sopra**. Con sedici osservazioni, un singolo episodio estremo sposta visibilmente media e quartili, e le mediane vanno lette come indicazioni qualitative, non come stime. Tutta questa scheda va letta con questo vincolo in mente.
>
> Promemoria: T+1/T+3/T+5/T+10 = giorni di **borsa** dopo l'evento, rendimenti cumulati.

#### `CAD=X` — cambio USD/CAD

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.17% | +0.26% | +0.04% | -0.07% |
| mediana | +0.18% | +0.12% | +0.02% | +0.22% |
| dev std | +0.37% | +0.68% | +0.59% | +1.19% |
| p25 | -0.08% | -0.11% | -0.38% | -0.53% |
| p75 | +0.28% | +0.67% | +0.20% | +0.75% |
| **N** | **16** | **16** | **16** | **16** |

**In pratica**: il dollaro canadese si **indebolisce leggermente** subito (USD/CAD in salita, mediana +0,18% a un giorno, con il quartile basso quasi in pari a −0,08%: cioè circa tre quarti degli episodi hanno visto un CAD più debole o invariato il giorno dopo), e poi il movimento si esaurisce. A cinque giorni la mediana è praticamente zero. È un impatto **immediato e piccolo**: nell'ordine di due decimi di punto percentuale, non di una svalutazione. La logica economica torna — un dazio riduce le esportazioni canadesi e quindi la domanda di dollari canadesi — ma la magnitudine dice che il mercato prezza in anticipo e con moderazione. Nota di cautela: `CAD=X` è stato aggiunto al database il 2026-08-16 e non ha nessuna previsione matura in scorecard, quindi non ha ancora un track record nel sistema.

#### `^GSPC` — S&P 500

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.04% | -0.26% | +0.39% | -0.02% |
| mediana | +0.58% | +0.58% | +0.68% | +0.10% |
| dev std | +1.77% | +3.34% | +2.07% | +3.82% |
| p25 | -0.41% | -1.23% | -0.82% | -2.45% |
| p75 | +1.32% | +1.49% | +1.19% | +3.08% |
| **N** | **16** | **16** | **16** | **16** |

**In pratica**: la mediana è **positiva** su tutti gli orizzonti (+0,58% già il giorno dopo), la media invece oscilla attorno allo zero. Lo scarto fra le due dice esattamente cosa succede: nel caso *tipico* il mercato americano si scrolla di dosso l'annuncio tariffario, ma il campione contiene alcuni episodi molto negativi (il 2 aprile 2025 e il dicembre 2018) che trascinano giù la media. Tradotto in una regola pratica: l'escalation tariffaria di solito non fa nulla all'S&P 500, tranne le poche volte in cui fa molto. La deviazione standard di 3,82% a T+10 con N=16 è il segnale di un campione a code grasse. `^GSPC` è **⚠ debole** in scorecard (IC +0,10, N=406).

#### `^STOXX50E` — Euro Stoxx 50

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.21% | +0.02% | +0.45% | +1.04% |
| mediana | +0.49% | +1.26% | +1.51% | +1.65% |
| dev std | +1.60% | +3.83% | +3.93% | +3.45% |
| p25 | -0.46% | -1.42% | +0.12% | -0.16% |
| p75 | +1.11% | +2.17% | +2.25% | +3.11% |
| **N** | **16** | **16** | **16** | **16** |

**In pratica**: risultato sorprendente e il più marcato della scheda — l'azionario europeo **sale** dopo un'escalation tariffaria, con mediana crescente fino a +1,65% a due settimane e, a T+5, perfino il quartile basso in positivo (+0,12%). La spiegazione più probabile non è che i dazi facciano bene all'Europa, ma che nei sedici episodi del pool **l'Europa non era il bersaglio**: in un mondo in cui gli Stati Uniti tassano il Canada e la Cina, l'esportatore europeo guadagna posizione relativa. È un vantaggio di sostituzione, e ha una data di scadenza precisa — il giorno in cui l'Europa diventa il bersaglio. `^STOXX50E` è **✅ affidabile** in scorecard (IC +0,17, N=172), il che rende questa indicazione fra le più credibili della scheda; ma va letta come "l'Europa finora è stata spettatrice", non come una legge.

#### `^VIX` — volatilità implicita

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.66% | +4.35% | -3.40% | -2.28% |
| mediana | -3.47% | -5.76% | -12.63% | -9.66% |
| dev std | +13.28% | +36.66% | +21.50% | +23.00% |
| p25 | -7.83% | -14.38% | -19.22% | -15.43% |
| p75 | +4.23% | +2.01% | +10.29% | +11.59% |
| **N** | **16** | **16** | **16** | **16** |

**In pratica**: la volatilità **crolla** nel caso tipico — mediana −12,63% a cinque giorni, cioè un VIX a 20 che scende verso 17,5. Ma la media a T+3 è **positiva** (+4,35%) con una deviazione standard del 36%: il campione contiene almeno un episodio in cui la volatilità è esplosa (il 2 aprile 2025, con ogni probabilità). Questa è la firma statistica classica del "sell the fear, buy the fact" applicato alle scadenze tariffarie: nei giorni prima della deadline il mercato compra protezione, e quando la deadline passa — con accordo, proroga o dazio che sia — la protezione viene liquidata. `^VIX` è **✅ affidabile** in scorecard (IC +0,17, hit-rate 63%), il che dà peso alla mediana; ma la divergenza media/mediana è un avvertimento serio sul rischio di coda.

#### `HG=F` — rame

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.23% | -1.09% | -0.57% | -0.33% |
| mediana | -0.34% | -0.13% | +0.24% | -1.09% |
| dev std | +1.87% | +4.89% | +5.58% | +4.85% |
| p25 | -1.30% | -2.97% | -3.04% | -2.75% |
| p75 | +1.17% | +1.32% | +1.47% | +1.52% |
| **N** | **16** | **16** | **16** | **16** |

**In pratica**: il rame tende a **scendere** (media negativa su tutti gli orizzonti, mediana −1,09% a due settimane), coerente con il canale "dazi = meno commercio = meno attività industriale". Ma le bande sono larghissime e attraversano lo zero ovunque: **segnale debole**, su un asset che la scorecard non ha ancora validato (meno di 50 previsioni mature).

#### `CNY=X` — cambio USD/CNY

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.15% | +0.07% | +0.03% | +0.24% |
| mediana | +0.02% | +0.06% | -0.14% | +0.21% |
| dev std | +0.27% | +0.53% | +0.72% | +1.09% |
| p25 | -0.01% | -0.28% | -0.33% | -0.38% |
| p75 | +0.26% | +0.34% | +0.32% | +0.50% |
| **N** | **16** | **16** | **16** | **16** |

**In pratica**: yuan marginalmente più debole (mediana +0,21% a T+10), movimento minuscolo. Come già osservato nella `news_03`, il cambio onshore è amministrato entro una banda: la sua mancata reazione non prova che il mercato non abbia reagito. Da notare comunque il segno: la svalutazione controllata è stata storicamente uno degli strumenti con cui Pechino ha assorbito i dazi.

#### `DX-Y.NYB` — indice del dollaro

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.11% | -0.19% | -0.29% | -0.17% |
| mediana | -0.06% | -0.39% | -0.25% | +0.31% |
| dev std | +0.57% | +0.74% | +0.96% | +1.64% |
| p25 | -0.42% | -0.67% | -0.77% | -0.59% |
| p75 | +0.25% | +0.30% | +0.19% | +0.87% |
| **N** | **16** | **16** | **16** | **16** |

⚠ **Direzione NON utilizzabile.** `DX-Y.NYB` è **❌ controproducente** nella scorecard 2026-W34 (IC per-asset −0,16, hit-rate **32%**, N=156). Tabella riportata per trasparenza, nessuna aspettativa derivata. È un peccato proprio qui, perché il dollaro è teoricamente uno dei canali più diretti di uno shock tariffario.

### Lettura sintetica

| Asset | Giudizio scorecard | Mediana T+1 | Mediana T+10 | Lettura |
|---|---|---|---|---|
| ^STOXX50E | ✅ affidabile (IC +0,17) | +0,49% | +1,65% | **l'Europa beneficia da spettatrice** (finché non è il bersaglio) |
| ^VIX | ✅ affidabile (IC +0,17) | −3,47% | −9,66% | *vol crush* post-scadenza, ma con coda di rischio pesante |
| ^GSPC | ⚠ debole (IC +0,10) | +0,58% | +0,10% | tipicamente indifferente, con rari episodi molto negativi |
| CAD=X | non valutato (aggiunto 2026-08-16) | +0,18% | +0,22% | CAD leggermente più debole, effetto immediato e piccolo |
| HG=F | non valutato (N<50) | −0,34% | −1,09% | rame debole, segnale non robusto |
| CNY=X | non valutato (N<50) | +0,02% | +0,21% | movimento minimo, cambio amministrato |
| DX-Y.NYB | ❌ controproducente | — | — | **nessuna direzione attesa** |

Il messaggio: storicamente, l'escalation tariffaria **non** è stata un evento di risk-off. Il pattern tipico è dollaro canadese un po' più debole, volatilità che si sgonfia dopo la scadenza, azionario che tiene o sale. Con due avvertenze pesanti: N=16, e la coda negativa esiste ed è grossa.

---

## Considerazioni qualitative

**Perché l'auto è il punto di rottura.** L'industria automobilistica nordamericana non è composta da un'industria canadese e una americana che commerciano fra loro: è **una sola catena produttiva integrata** costruita in trent'anni di libero scambio (prima NAFTA, poi USMCA). Un pezzo di lamiera può attraversare il confine cinque o sei volte — stampato in Ontario, assemblato in Michigan, il modulo rispedito in Ontario, il veicolo finito venduto negli Stati Uniti. Con un dazio, ogni attraversamento è un evento fiscale: l'aliquota nominale del 15% si traduce in un costo effettivo molto più alto sul valore finale, perché si applica ripetutamente su un valore che include già dazi precedenti. Ecco perché Ottawa non chiede solo un'aliquota più bassa ma anche "l'allargamento dell'esenzione per la componentistica di origine americana": la vera partita non è il numero, è **cosa conta come contenuto americano**. Cinque punti di differenza sono poca cosa; la definizione di origine può valere molto di più.

**Il precedente giuridico conta più del dazio.** Questo è il pezzo che il briefing segnala giustamente come rilevante "ben oltre il Canada". A febbraio la Corte Suprema ha annullato i dazi imposti con lo strumento legale precedente. L'amministrazione ha ripiegato sulla **Section 338**, una disposizione del Tariff Act del 1930 che consente al presidente di imporre dazi fino al 50% contro paesi che discriminano il commercio americano — una norma sostanzialmente mai usata in novant'anni. Mercoledì è il primo test operativo. Se regge senza essere immediatamente sospesa da un tribunale, gli Stati Uniti hanno riacquistato uno strumento tariffario funzionante contro **chiunque**, e il rischio si ripresenta identico su Unione Europea, Messico e altri. Se non regge, l'intero regime tariffario torna in sospensione giudiziaria. È un'opzione binaria su un pezzo di architettura, non su un accordo bilaterale, e i mercati non la stanno prezzando in modo visibile.

**Perché l'evento potrebbe passare senza scosse — e perché non è una buona notizia.** L'event study dice, con la cautela di N=16, che il pattern tipico è mite: volatilità che si sgonfia (mediana −12,63% a cinque giorni), S&P 500 stabile, dollaro canadese giù di due decimi. La ragione è che il mercato ha imparato che in questo regime le scadenze tariffarie si spostano: la reazione a un annuncio incorpora già la probabilità di una proroga. Il rovescio della medaglia è che questa assuefazione riduce la capacità del mercato di prezzare il caso in cui *non* ci sia proroga — e la media del VIX a T+3 (+4,35% contro una mediana di −5,76%) è la traccia statistica di quei pochi casi. Un mercato che si aspetta sistematicamente la proroga è un mercato mal posizionato per il giorno in cui non arriva.

**Il paradosso europeo, e perché ha una scadenza.** Il risultato più forte dell'event study è `^STOXX50E` in rialzo (mediana +1,65% a due settimane), su un asset che la scorecard classifica affidabile. Non è che i dazi facciano bene all'Europa: è che nei sedici episodi del pool l'Europa era quasi sempre lo spettatore, e chi resta fuori da una guerra commerciale guadagna quote relative. Questa lettura ha però una condizione al contorno che oggi è particolarmente fragile, ed è esattamente il punto precedente: se la Section 338 supera il test di mercoledì, lo strumento diventa disponibile contro l'Unione Europea. In quel caso il vantaggio da spettatore evapora, e gli episodi del pool smettono di essere analoghi. **Questo è il motivo per cui non tratterei il +1,65% come una previsione.**

**Il collegamento con le altre schede di oggi.** Un dazio è, dal punto di vista macroeconomico, uno shock di offerta: alza i prezzi dei beni importati e insieme deprime i volumi. È lo stesso *tipo* di shock dell'energia (`news_01`) e dell'interruzione logistica sul Reno (`news_05`), e si somma a essi nello stesso trimestre. È precisamente la configurazione che rende la vita difficile alle banche centrali della `news_02`: alzare i tassi non fa sparire un dazio, e non alzarli lascia che l'inflazione da costi si trasferisca alle aspettative. La frase del briefing — "un tariff shock che atterra su un mercato che già prezza un regime di inflazione è la combinazione senza una risposta pulita da parte delle banche centrali" — è precisa.

---

## Glossario — sigle e termini

- **Dazio / tariffa** — un'imposta sulle merci importate, pagata all'ingresso nel paese importatore. La paga formalmente l'importatore, e viene poi ripartita fra margine dell'esportatore, margine dell'importatore e prezzo al consumatore.
- **Section 338** — disposizione del *Tariff Act* statunitense del 1930 che autorizza il presidente a imporre dazi fino al 50% contro paesi che discriminano il commercio americano. Praticamente inutilizzata per novant'anni; è la base giuridica di ripiego dopo l'annullamento dei dazi precedenti da parte della Corte Suprema nel febbraio 2026.
- **Section 232** — clausola che consente dazi per motivi di sicurezza nazionale (usata su acciaio e alluminio nel 2018). **Section 301** — clausola contro pratiche commerciali sleali (usata contro la Cina dal 2018). **IEEPA** — legge sui poteri economici in caso di emergenza, base dei dazi 2025 poi contestata in giudizio.
- **USMCA** (*United States–Mexico–Canada Agreement*) — l'accordo di libero scambio nordamericano in vigore dal 2020, che ha sostituito il **NAFTA** (1994).
- **Regole di origine** — i criteri che stabiliscono in quale paese un prodotto è "nato", e quindi quale dazio paga. In una catena integrata sono la parte più contesa di ogni negoziato: definiscono quanta parte di un'auto deve essere prodotta in area per essere esente.
- **TSX** (*Toronto Stock Exchange*) — la borsa canadese; il suo indice principale è l'S&P/TSX Composite. **Non presente nel database del progetto.**
- **Termini di scambio** (*terms of trade*) — il rapporto fra i prezzi di ciò che un paese esporta e di ciò che importa. Un dazio estero li peggiora e tende a indebolire la valuta.
- **Vol crush** — il crollo della volatilità implicita subito dopo il passaggio di un evento programmato, quando la protezione comprata prima viene liquidata.
- **Code grasse** (*fat tails*) — la proprietà di una distribuzione di produrre eventi estremi più spesso di quanto una distribuzione normale prevederebbe. Si riconosce da media e mediana molto distanti e deviazione standard alta.
- **CAD=X** — cambio USD/CAD: quanti dollari canadesi per un dollaro USA. Sale = dollaro canadese più debole. **CNY=X** — cambio USD/yuan onshore. **^GSPC** — S&P 500. **^STOXX50E** — Euro Stoxx 50. **^VIX** — indice di volatilità implicita. **HG=F** — futures rame. **DX-Y.NYB** — indice del dollaro.
- **IC** (*Information Coefficient*) — correlazione di rango a parità di asset fra direzione prevista e realizzata; negativo = previsione sistematicamente rovesciata.
- **p25 / p75** — primo e terzo quartile; fra loro sta il 50% centrale degli episodi.

---

## Caveat

- **N = 16 — il campione più piccolo delle schede di oggi.** Supera la soglia formale di 10, ma di poco: con sedici osservazioni un singolo episodio estremo sposta media e quartili in modo visibile, ed è esattamente quello che si vede su `^VIX` (media +4,35% e mediana −5,76% a T+3). Le indicazioni di questa scheda sono **qualitative**.
- **Regime-mixing severo e dichiarato.** Dieci dei sedici episodi appartengono al ciclo 2018-19, con aliquote del 10-25% e bersaglio prevalentemente cinese; sei al regime corrente, con aliquote fino al 50%, bersagli alleati e base giuridica contestata. Sono due mondi diversi. Ho tenuto il blocco vecchio solo perché escluderlo avrebbe portato N a 6, sotto la soglia di utilizzabilità: è un compromesso, non una scelta metodologicamente pulita.
- **Manca l'asset più diretto.** Il **TSX** (azionario canadese) non è nell'universo del progetto, e il briefing segnala che si è già ritirato da un massimo storico — cioè il movimento più informativo su questa notizia è precisamente quello che non possiamo misurare. Analogamente mancano l'azionario settoriale auto e i produttori di componentistica. Lacuna registrata in `_index.md`.
- **`CAD=X` è nel database da due giorni** (aggiunto il 2026-08-16) e **non ha alcuna previsione matura in scorecard**: l'event study su di esso è tecnicamente valido (i dati storici del cambio ci sono) ma il sistema non ha ancora alcuna evidenza sulla propria capacità di prevederlo.
- **`DX-Y.NYB`: direzione bloccata** dalla scorecard 2026-W34 (❌ controproducente, IC −0,16, hit-rate 32%).
- **`HG=F` e `CNY=X` non validati** (meno di 50 previsioni mature in scorecard).
- **Rischio di condizione al contorno sul risultato europeo.** Il rialzo di `^STOXX50E` dipende dal fatto che nei sedici episodi l'Europa non era il bersaglio. Se la Section 338 supera il test di mercoledì, questa condizione può decadere rapidamente e il segnale invertirsi. Non è un limite statistico ma logico, ed è il più importante della scheda.
- **Evento non ancora avvenuto.** A differenza delle altre schede di oggi, questa analizza una scadenza **futura** (19 agosto): il pool descrive cosa è successo *dopo* escalation già materializzate, mentre qui l'esito è ancora aperto fra accordo, proroga e dazio. La reazione di mercato dipenderà da quale dei tre si realizza, e l'event study non li distingue.
- **Correlazione ≠ causazione**: nel dicembre 2018 e nell'aprile 2025 la finestra dell'evento si sovrappone ad altri shock rilevanti (rispettivamente la stretta della Fed e il riprezzamento generale del rischio), che l'event study attribuisce interamente al dazio.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-17T08:04:03
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
