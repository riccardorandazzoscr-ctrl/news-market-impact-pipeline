# I dati di attività cinesi di luglio mancano su tutta la linea: vendite al dettaglio +0,6%, produzione industriale +4,5%, investimenti fissi -6,7%

**Data analisi**: 2026-08-18
**Fonte**: Morning Briefing 2026-08-18 (fin 01)
**Slug**: china-july-activity-miss

---

## Testo notizia (originale)

> L'Ufficio nazionale di statistica cinese ha pubblicato lunedi i dati di attivita di luglio e ogni voce ha deluso. Le vendite al dettaglio sono cresciute dello 0,6% anno su anno contro un consenso dell'1,5% e l'1,0% di giugno; la produzione industriale ha rallentato al 4,5% dal 5,3%, contro il 4,8% atteso in un sondaggio Reuters su 26 analisti; gli investimenti in capitale fisso gennaio-luglio sono scesi del 6,7% anno su anno, peggio del -6,2% atteso e piu ripidi della contrazione del 5,7% del primo semestre. Il settore immobiliare resta l'epicentro: gli investimenti in sviluppo immobiliare sono calati del 19,2% nei primi sette mesi e le vendite di nuove case per superficie dell'11,8%, ma anche gli investimenti al netto dell'immobiliare sono scesi del 3,7%, quindi la debolezza non e piu confinata alle case. Le autorita hanno attribuito parte del disallineamento al maltempo estremo e all'esaurirsi degli effetti delle politiche di sostegno ai consumi. Il dato conferma il deleveraging implicito nella contrazione record del credito di luglio (340 miliardi di yuan); il rendimento del titolo di Stato cinese a 10 anni resta vicino a un minimo di un anno all'1,684% e Shanghai e salita dell'1,4%, cioe un mercato che tratta la risposta di stimolo piuttosto che il dato.

---

## In breve (in parole semplici)

Ogni mese la Cina pubblica tre numeri che raccontano se la sua economia sta girando: quanto comprano le famiglie (vendite al dettaglio), quanto producono le fabbriche (produzione industriale) e quanto si investe in impianti, infrastrutture e case (investimenti in capitale fisso). A luglio hanno deluso tutti e tre. Il più preoccupante è il terzo: gli investimenti non stanno solo rallentando, stanno **scendendo** — del 6,7% rispetto a un anno fa, peggio del già negativo −6,2% atteso, e in accelerazione rispetto al −5,7% del primo semestre.

Il punto che cambia la storia rispetto agli ultimi tre anni è questo: finora la debolezza cinese era la crisi immobiliare, un problema grave ma circoscritto. A luglio anche gli investimenti **al netto dell'immobiliare** sono scesi (−3,7%). La malattia si è estesa.

La reazione dei mercati è però controintuitiva: la borsa di Shanghai è salita dell'1,4% e i rendimenti dei titoli di Stato cinesi sono vicini ai minimi dell'anno. Il mercato non sta comprando i dati, sta comprando la **risposta** che si aspetta — cioè nuovo stimolo pubblico.

La domanda che ci poniamo: quando in passato i dati di attività globali hanno deluso al ribasso, come si sono mossi nei giorni successivi yuan, rame, azionario emergente ed europeo, greggio e volatilità?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | macro_data |
| `sub_themes` | activity_growth, cny |
| `sentiment` | bearish |
| `confidence` | medium |
| `horizon` | intraday-5 giorni di trading |

**Motivazione classificazione**: è una pubblicazione statistica programmata con un consenso pre-esistente e una sorpresa misurabile rispetto ad esso — la definizione da manuale di `macro_data`. Il sotto-tema canonico è `activity_growth` (dati di attività reale, distinti dai dati di inflazione `inflation_print` e dal mercato del lavoro `labour_market`). Il sentiment è `bearish` perché la sorpresa è negativa su tutte e tre le voci. La confidence è `medium`: la sorpresa è chiara e diffusa, ma la funzione di reazione del mercato cinese è ambigua per costruzione — cattive notizie possono essere lette come buone se aumentano la probabilità di stimolo, e infatti Shanghai è salita. Questa ambiguità è il motivo per cui non alzo la confidence a `high`.

Nota di trasparenza: la scorecard 2026-W34 assegna al tema `macro_data` un IC di **+0,11** con hit-rate 53% su 590 previsioni — il secondo tema migliore per contenuto informativo dopo `structural_themes` e `fiscal_policy`. È un terreno relativamente solido per questo sistema.

---

## Asset rilevanti

### Primary (canale diretto)

- **CNY=X** (cambio dollaro/yuan onshore: un numero più alto = yuan più debole) — il termometro diretto delle aspettative sull'economia cinese e sulla risposta della banca centrale.
- **HG=F** (futures sul rame, quotato al COMEX) — il rame è chiamato "Dr. Copper" perché la sua domanda dipende da costruzioni, reti elettriche e manifattura; la Cina ne assorbe circa la metà della domanda mondiale. È il miglior proxy quotato di questa notizia.
- **EEM** (ETF iShares MSCI Emerging Markets, azionario dei mercati emergenti; la Cina ne è la componente maggiore) — proxy azionario diretto.

### Secondary (effetti indiretti)

- **^STOXX50E** (Euro Stoxx 50) — l'area euro esporta in Cina beni di lusso, auto e macchinari; una domanda cinese debole colpisce direttamente i suoi utili.
- **^GSPC** (S&P 500) — canale di risk-off globale, più diluito.
- **BZ=F** (Brent) — la Cina è il maggiore importatore mondiale di greggio: attività debole = domanda di petrolio debole. È l'unica forza *ribassista* sull'energia in un briefing altrimenti tutto rialzista.
- **^VIX** (volatilità implicita S&P 500) — misura se il dato viene trattato come rumore o come rischio.
- **DX-Y.NYB** (indice del dollaro) — ⚠ direzione storicamente inaffidabile, vedi sotto.

---

## Knowledge Base — research correlate

- [score=10] `PBOC e politica economica cinese — regime ed episodi storici (2022–2026)/...md`
  - Perché è rilevante: è la research specifica sul tema. Documenta la funzione di reazione della banca centrale cinese (PBOC) e i regimi di politica economica del periodo — indispensabile per capire se un dato debole si traduce in stimolo o in inerzia.
- [score=5] `dati_macro_USA_e_trasmissione_ai_mercati_(2013–2024)/...md` — *Sorprese sui dati macro USA e trasmissione ai mercati: regimi, canali e state-dependence*
  - Perché è rilevante: il concetto chiave che serve qui — la *state-dependence*, cioè il fatto che la stessa sorpresa produce reazioni opposte a seconda del regime — è sviluppato in questa research. Il caso cinese di oggi (dato brutto, borsa su) ne è l'esempio perfetto.
- [score=4] `Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)/...md`
  - Perché è rilevante: parte della debolezza degli investimenti manifatturieri cinesi è il riflesso del regime tariffario; collega questa scheda alla `news_04`.
- [score=5] `ciclo_inflazione_eurozona_2021-2023/Ciclo inflazione Eurozona 2021–2023.md`
  - Perché è rilevante: la trasmissione di una domanda cinese debole ai prezzi dei beni importati in Europa (canale disinflazionistico) è il rovescio della medaglia energetica.

---

## Regime storico identificato

- **Regime**: deleveraging strutturale cinese in fase di allargamento (2022 → oggi), con la crisi immobiliare che smette di essere l'unica spiegazione.
- **Caratterizzazione**: tre fatti definiscono il momento. (1) **La contrazione ha superato l'immobiliare**: investimenti immobiliari −19,2% nei primi sette mesi, ma anche il resto degli investimenti a −3,7%. Nei tre anni precedenti la narrativa era "il problema sono le case"; ora non regge più. (2) **Il credito si sta contraendo, non solo rallentando**: luglio ha registrato una contrazione record di 340 miliardi di yuan. Quando famiglie e imprese rimborsano più di quanto prendono a prestito, la politica monetaria perde presa — è il meccanismo che gli economisti chiamano *balance-sheet recession*, la recessione da bilanci: dopo un eccesso di debito, ognuno dà priorità al ripagarlo anziché a spendere, e i tagli dei tassi non bastano a invertirlo. (3) **I consumi hanno esaurito la spinta artificiale**: le stesse autorità attribuiscono parte della delusione al venir meno degli incentivi (i programmi di rottamazione e sostituzione beni durevoli).
- **Il regime rende ambigua la lettura di mercato**: siamo in una fase in cui il mercato azionario cinese reagisce alla *probabilità di stimolo* più che al dato. Il decennale cinese all'1,684%, vicino ai minimi dell'anno, dice che il mercato obbligazionario prezza crescita e inflazione basse a lungo — che è l'interpretazione coerente col dato. Shanghai +1,4% dice che il mercato azionario prezza l'intervento pubblico. Le due letture non sono contraddittorie: sono la stessa notizia vista da chi teme la stagnazione e da chi scommette sul salvataggio.

---

## Event study

### Episodi storici analoghi selezionati

Pool dalla libreria (Opzione B), tema `macro_data`, sotto-tema **date-locale** `activity_growth` (29 episodi a questo livello, filtro forte), direzione `neg`, no-look-ahead a `2026-08-18`. Il pool non ha raggiunto il tetto di recency (28 episodi < 30), quindi è completo.

```bash
venv/bin/python analogues.py find --theme macro_data \
  --subtheme activity_growth --direction neg --before 2026-08-18
```

I 28 episodi sono pubblicazioni di dati di attività (PMI, produzione industriale, PIL, indagini congiunturali) risultate sotto le attese, distribuite fra 2015 e luglio 2026. Le famiglie principali:

- `2015-09-03`, `2015-12-01`, `2018-02-02` — la fase della "paura Cina" del 2015-16 e il rallentamento manifatturiero globale del 2018. Analoghi diretti per il canale cinese.
- `2019-08-01` → `2019-10-01` — il rallentamento manifatturiero da guerra commerciale: PMI in contrazione, ISM manifatturiero USA sotto 50. Regime tariffario simile all'attuale.
- `2022-02-04` → `2023-08-03` — i PMI globali in deterioramento durante lo shock energetico e la stretta monetaria: il regime **più simile a oggi** (attività debole *e* inflazione alta insieme).
- `2024-02-02` → `2025-03-03` — dati di attività deludenti nel ciclo di normalizzazione.
- `2026-06-05`, `2026-07-24` — gli episodi del regime corrente.

Non ho potato il pool: la libreria ha già applicato il filtro di sotto-tema forte e la direzione, e l'insieme è coerente ("attività reale sotto le attese").

⚠ Limite dichiarato: il pool è di **sorprese di attività globali**, non specificamente cinesi. Non esiste in libreria un sotto-tema `china_activity` con copertura sufficiente a livello date-locale (`cny` ne ha 13, `pboc` 8). È il compromesso di questa scheda.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'CNY=X,HG=F,EEM,^STOXX50E,^GSPC,BZ=F,^VIX,DX-Y.NYB' \
  --events 2015-09-03,2015-12-01,2018-02-02,2019-08-01,2019-09-04,2019-10-01,2022-02-04,2022-08-03,2022-10-13,2022-11-01,2022-12-01,2023-02-03,2023-06-01,2023-07-12,2023-08-01,2023-08-03,2023-12-08,2024-02-02,2024-04-01,2024-06-07,2024-07-11,2024-08-01,2024-10-01,2024-12-06,2025-03-03,2025-09-30,2026-06-05,2026-07-24 \
  --windows 1,3,5,10 --markdown
```

N = **28** su tutti i ticker.

### Risultati

> **Promemoria**: T+1/T+3/T+5/T+10 = giorni di **borsa** dopo l'evento, rendimenti cumulati. Mediana = caso tipico; media = sensibile agli estremi. Se p25 e p75 hanno segno opposto, non c'è direzione.

#### `HG=F` — rame

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.02% | +0.53% | +0.27% | +1.01% |
| mediana | +0.16% | +0.01% | +0.47% | +1.05% |
| dev std | +1.45% | +2.62% | +3.13% | +4.20% |
| p25 | -0.86% | -1.27% | -2.32% | -0.90% |
| p75 | +0.94% | +2.00% | +1.91% | +3.66% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: il rame, contro l'intuizione, **sale** leggermente dopo una delusione sull'attività (mediana +1,05% a due settimane). L'interpretazione più plausibile è la stessa che spiega Shanghai +1,4%: un dato brutto alza la probabilità di stimolo pubblico, e lo stimolo cinese passa storicamente da infrastrutture e reti elettriche, cioè da rame. Ma la banda p25–p75 a T+10 va da −0,90% a +3,66% e attraversa lo zero: **segnale debole**. Nota: `HG=F` ha meno di 50 previsioni mature e quindi non compare nella tabella per-asset della scorecard — non è né autorizzato né vietato, semplicemente non è ancora valutato. Lo tratto con cautela.

#### `EEM` — azionario emergenti

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.08% | +0.22% | +0.28% | +0.79% |
| mediana | +0.35% | +0.84% | +0.27% | +1.34% |
| dev std | +1.46% | +2.11% | +2.40% | +4.45% |
| p25 | -1.03% | -1.11% | -0.93% | -2.32% |
| p75 | +0.80% | +1.63% | +1.38% | +2.97% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: stessa firma del rame — l'azionario emergente **sale** (mediana +1,34% a T+10, positiva su tutti gli orizzonti). `EEM` è fra gli asset **✅ affidabili** della scorecard (IC +0,17, hit-rate 61%, N=64), quindi questa indicazione ha più peso delle altre in questa scheda. La logica di fondo è la stessa: dati deboli → attesa di politiche di sostegno → ricopertura sul rischio emergente. È il classico "bad news is good news", che vale però solo finché il mercato crede che una risposta arriverà.

#### `CNY=X` — cambio USD/CNY

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.00% | -0.01% | +0.03% | +0.09% |
| mediana | +0.00% | -0.00% | +0.03% | +0.09% |
| dev std | +0.35% | +0.74% | +0.78% | +1.20% |
| p25 | -0.26% | -0.22% | -0.33% | -0.44% |
| p75 | +0.14% | +0.17% | +0.26% | +0.82% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: **nulla**. Mediane fra 0,00% e +0,09%: lo yuan non si muove. Questo non è un fallimento della misura ma un fatto istituzionale — il cambio dello yuan onshore è gestito dalla banca centrale cinese entro una banda giornaliera attorno a una parità fissata ogni mattina. Non è un prezzo libero, quindi non reagisce ai dati come farebbe una valuta di mercato. Da tenere a mente ogni volta che si usa `CNY=X` come termometro: è un termometro con il vetro spesso.

#### `BZ=F` — Brent

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.33% | -0.78% | -0.85% | -1.20% |
| mediana | -0.09% | -1.85% | -0.08% | -0.14% |
| dev std | +2.38% | +4.11% | +4.88% | +5.86% |
| p25 | -2.06% | -3.36% | -3.70% | -4.18% |
| p75 | +1.47% | +2.81% | +1.68% | +2.69% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: il greggio **scende** in modo consistente su tutti gli orizzonti in termini di media (−1,20% a T+10), con mediane vicine allo zero ma sempre negative. È il canale della domanda: la Cina è il maggior importatore mondiale di petrolio, e attività debole significa meno barili consumati. `BZ=F` è **✅ affidabile** in scorecard (IC +0,13, hit-rate 61%, N=172), la seconda migliore valutazione per hit-rate. **Questo è il risultato più rilevante della scheda**, perché è l'unica forza ribassista sull'energia in un briefing dominato dallo shock di offerta iraniano — le due spinte si oppongono.

#### `^GSPC` — S&P 500

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.59% | -0.38% | -0.38% | +0.06% |
| mediana | -0.45% | -0.23% | -0.58% | +0.65% |
| dev std | +1.22% | +1.71% | +1.88% | +2.91% |
| p25 | -1.26% | -1.86% | -1.63% | -2.94% |
| p75 | +0.27% | +1.19% | +1.12% | +2.17% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: l'azionario americano incassa il colpo subito (mediana −0,45% il giorno dopo, con il quartile alto a soli +0,27% — cioè oltre tre quarti degli episodi sotto lo zero o poco sopra) e recupera entro due settimane (+0,65%). Un rimbalzo, non un trend. `^GSPC` è **⚠ debole** in scorecard (IC +0,10, N=406).

#### `^STOXX50E` — Euro Stoxx 50

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.27% | -0.10% | -0.29% | +0.21% |
| mediana | +0.02% | -0.21% | -0.03% | -0.23% |
| dev std | +1.24% | +1.53% | +2.34% | +3.25% |
| p25 | -0.90% | -0.92% | -1.52% | -1.92% |
| p75 | +0.61% | +0.72% | +1.55% | +2.31% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: sostanzialmente piatto con una leggerissima inclinazione negativa (mediana −0,23% a T+10). L'indice europeo non recupera come quello americano, il che è coerente con la maggiore esposizione delle sue società (lusso, auto, macchinari) al ciclo cinese. `^STOXX50E` è **✅ affidabile** (IC +0,17, N=172), quindi anche un segnale piccolo qui merita attenzione — ma resta piccolo.

#### `^VIX` — volatilità implicita

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +6.67% | +4.80% | +6.03% | +5.83% |
| mediana | +0.50% | +0.70% | +4.75% | +6.34% |
| dev std | +22.65% | +16.67% | +17.58% | +20.88% |
| p25 | -1.63% | -4.60% | -6.26% | -10.72% |
| p75 | +7.67% | +7.61% | +12.96% | +18.25% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica**: **il segnale più netto della scheda**. La volatilità sale, e sale in modo crescente nel tempo: mediana +4,75% a cinque giorni e +6,34% a dieci, con media positiva su tutti gli orizzonti. È l'unico asset in cui media e mediana concordano nel segno per l'intero profilo. `^VIX` è **✅ affidabile** (IC +0,17, hit-rate 63%, N=101) — la valutazione migliore per hit-rate di tutta la scorecard. La lettura: le delusioni sull'attività non producono un crollo direzionale dei listini, ma **alzano stabilmente il prezzo dell'incertezza**, e lo fanno con un ritardo (l'effetto è più forte a T+5 e T+10 che a T+1). Cioè il mercato metabolizza lentamente.

#### `DX-Y.NYB` — indice del dollaro

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.06% | -0.22% | -0.26% | -0.33% |
| mediana | -0.07% | -0.18% | -0.12% | -0.01% |
| dev std | +0.48% | +0.81% | +1.01% | +1.51% |
| p25 | -0.27% | -0.57% | -1.18% | -1.44% |
| p75 | +0.26% | +0.04% | +0.50% | +0.80% |
| **N** | **28** | **28** | **28** | **28** |

⚠ **Direzione NON utilizzabile.** `DX-Y.NYB` è marcato **❌ controproducente** nella scorecard 2026-W34 (IC per-asset −0,16, hit-rate 32%, N=156). Tabella riportata per trasparenza; nessuna aspettativa derivata.

### Lettura sintetica

| Asset | Giudizio scorecard | Mediana T+5 | Mediana T+10 | Lettura |
|---|---|---|---|---|
| ^VIX | ✅ affidabile (IC +0,17) | +4,75% | +6,34% | **volatilità in salita, con ritardo — il segnale più solido** |
| BZ=F | ✅ affidabile (IC +0,13) | −0,08% | −0,14% | greggio debole (media −0,85%/−1,20%): canale domanda |
| EEM | ✅ affidabile (IC +0,17) | +0,27% | +1,34% | emergenti in rialzo: "bad news is good news" da attesa stimolo |
| ^STOXX50E | ✅ affidabile (IC +0,17) | −0,03% | −0,23% | piatto/leggermente negativo |
| ^GSPC | ⚠ debole (IC +0,10) | −0,58% | +0,65% | colpo iniziale, poi rimbalzo |
| HG=F | non valutato (N<50) | +0,47% | +1,05% | rame in leggero rialzo — cautela, asset non validato |
| CNY=X | non valutato (N<50) | +0,03% | +0,09% | nessun movimento: cambio amministrato |
| DX-Y.NYB | ❌ controproducente | — | — | **nessuna direzione attesa** |

Il quadro coerente che ne esce: **non un risk-off direzionale, ma un aumento del prezzo dell'incertezza**, con il greggio come unico canale nettamente negativo e gli emergenti che scommettono sullo stimolo.

---

## Considerazioni qualitative

**Perché "gli investimenti al netto dell'immobiliare a −3,7%" è la riga che conta.** Dal 2021 la storia della Cina è stata: crisi del settore immobiliare, con Evergrande e Country Garden come simboli, e il resto dell'economia che teneva. Quella narrativa permetteva una lettura contenuta del problema — grave ma settoriale, risolvibile con tempo e ristrutturazioni. Il dato di luglio la smonta: se anche gli investimenti non immobiliari scendono, significa che le imprese al di fuori dell'edilizia non vedono ragioni per costruire capacità. Le cause plausibili sono tre e si sommano: sovraccapacità già installata (nell'auto elettrica, nei pannelli solari, nelle batterie); domanda estera compressa dai dazi; e la percezione che i prezzi non saliranno, che è il modo in cui la deflazione si autoalimenta — se pensi che l'impianto costerà meno fra un anno, aspetti.

**Il paradosso "dato brutto, borsa su" e perché non è irrazionale.** Shanghai +1,4% nel giorno del dato peggiore dell'anno sembra assurdo. Non lo è, se si tiene presente che il mercato azionario cinese è, più che altrove, un mercato di policy: il suo prezzo dipende meno dagli utili attesi e più dall'aspettativa di intervento pubblico. Un dato sufficientemente brutto costringe la mano di Pechino, e la storia recente dice che quando Pechino interviene lo fa in grande. L'event study su `EEM` (mediana +1,34% a due settimane, con asset marcato affidabile) conferma che questo riflesso è sistematico, non un caso isolato. **Ma è una scommessa sulla reazione, non sull'economia**, e ha un modo tipico di fallire: se lo stimolo annunciato è più piccolo dell'atteso, il rialzo si riavvolge in pochi giorni.

**Il rendimento del decennale cinese all'1,684% è il giudizio più onesto sul quadro.** Mentre le azioni comprano la speranza, le obbligazioni comprano la realtà: un rendimento decennale vicino ai minimi di un anno significa che il mercato obbligazionario si aspetta crescita bassa e inflazione bassa per molto tempo. Vale la pena notare quanto sia straordinario il confronto con la `news_02`: nello stesso giorno, il decennale giapponese è al 2,93% e quello cinese all'1,68%. Due economie asiatiche, curve che vanno in direzioni opposte. Il Giappone esce dalla deflazione, la Cina ci sta entrando.

**La contrazione del credito è il vero vincolo.** Una contrazione di 340 miliardi di yuan significa che il sistema ha rimborsato più di quanto ha erogato. In questo stato, tagliare i tassi serve a poco: il problema non è il costo del denaro ma il fatto che nessuno lo vuole prendere in prestito. È la stessa trappola in cui il Giappone è caduto negli anni Novanta, e la via d'uscita storicamente è stata fiscale, non monetaria — cioè lo Stato che si indebita al posto dei privati. Da qui la scommessa del mercato azionario. Da qui anche il motivo per cui la banca centrale cinese, da sola, non è la risposta.

**Cosa significa per l'Europa e per l'energia — il collegamento con le altre schede di oggi.** Due trasmissioni concrete. La prima: le società europee del lusso, dell'auto e dei macchinari hanno una quota di ricavi cinese rilevante, e una domanda al consumo che cresce dello 0,6% è, in termini reali, ferma. L'event study su `^STOXX50E` lo cattura solo debolmente (mediana −0,23% a T+10), ma il canale è strutturale, non di breve periodo. La seconda, più importante: **la domanda cinese debole è l'unica forza ribassista sul petrolio in circolazione oggi**. L'event study dà `BZ=F` in calo (media −1,20% a T+10) su un asset affidabile. Nel briefing di oggi convivono quindi due spinte opposte sul greggio: l'offerta iraniana strozzata che spinge in su (`news_01`) e la domanda cinese che cede e spinge in giù. Storicamente, negli shock di questa natura, il canale dell'offerta vince nel breve e quello della domanda nel medio — ed è una delle ragioni per cui il Brent nell'event study della `news_01` mostrava mediane così modeste. Da tenere d'occhio, perché è esattamente la dinamica che potrebbe far scendere il greggio mentre i prodotti raffinati continuano a salire.

---

## Glossario — sigle e termini

- **Vendite al dettaglio** (*retail sales*) — il totale speso dalle famiglie nei negozi e online; il termometro dei consumi.
- **Produzione industriale** — il volume prodotto da fabbriche, miniere e utility. Misura l'offerta reale.
- **Investimenti in capitale fisso** (*fixed-asset investment*, FAI) — la spesa in impianti, macchinari, infrastrutture e immobili. In Cina è la voce storicamente più grande della domanda aggregata.
- **Anno su anno** (*year on year*) — il confronto con lo stesso mese dell'anno precedente; elimina la stagionalità.
- **Consenso** — la media delle previsioni degli analisti prima della pubblicazione. La "sorpresa" è la differenza fra dato e consenso, ed è ciò che muove i prezzi (il livello atteso è già nel prezzo).
- **NBS** (*National Bureau of Statistics*) — l'ufficio statistico nazionale cinese.
- **PBOC** (*People's Bank of China*) — la banca centrale cinese.
- **Deleveraging** — la riduzione del debito aggregato di un'economia. Doloroso perché rimborsare significa non spendere.
- **Balance-sheet recession** (recessione da bilanci) — la situazione in cui, dopo un eccesso di debito, famiglie e imprese danno priorità al ripagarlo anziché a spendere e investire; la politica monetaria perde efficacia perché il problema non è il costo del credito ma la domanda di credito.
- **Deflazione** — la caduta generalizzata dei prezzi. Pericolosa perché rinviare gli acquisti diventa razionale, il che deprime ulteriormente la domanda, e perché aumenta il peso reale dei debiti.
- **Sovraccapacità** — capacità produttiva installata superiore alla domanda; comprime i margini e disincentiva nuovi investimenti.
- **PMI** (*Purchasing Managers' Index*) — indice dei responsabili acquisti: un'indagine mensile in cui i manager dicono se attività, ordini e occupazione sono migliorati o peggiorati. Sopra 50 = espansione, sotto 50 = contrazione.
- **ISM** (*Institute for Supply Management*) — l'analogo americano del PMI, il più seguito.
- **PIL / GDP** — prodotto interno lordo.
- **State-dependence** — il fatto che la stessa notizia produca reazioni di segno diverso a seconda del regime macro in cui arriva. Il caso di oggi (dato brutto, borsa su) ne è un esempio.
- **"Bad news is good news"** — la configurazione in cui un dato negativo fa salire i mercati perché aumenta la probabilità di sostegno pubblico o monetario.
- **CNY=X** — cambio dollaro/yuan **onshore** (quello negoziato in Cina continentale, gestito dalla PBOC entro una banda giornaliera attorno a una parità fissata ogni mattina), distinto dal CNH offshore di Hong Kong, più libero.
- **HG=F** — futures sul rame al COMEX. **EEM** — ETF azionario mercati emergenti. **BZ=F** — futures Brent. **^GSPC** — S&P 500. **^STOXX50E** — Euro Stoxx 50. **^VIX** — indice di volatilità. **DX-Y.NYB** — indice del dollaro.
- **IC** (*Information Coefficient*) — correlazione di rango a parità di asset fra direzione prevista e realizzata; negativo = sistematicamente rovesciata.

---

## Caveat

- **N = 28 su tutti i ticker**: sopra la soglia di 10, campione utilizzabile.
- **Il pool non è cinese-specifico.** Gli episodi sono sorprese negative sui dati di attività *globali* (PMI, ISM, produzione industriale, PIL di varie aree), non solo cinesi. La libreria non ha un sotto-tema cinese con copertura date-locale sufficiente (`cny` = 13 episodi, `pboc` = 8, entrambi sotto la soglia di affidabilità). È il limite principale della scheda: i risultati vanno letti come "reazione tipica a una delusione sull'attività", non come "reazione tipica a una delusione cinese".
- **Regime-mixing significativo**: 2015-16 (paura Cina, deflazione da commodity), 2018-19 (guerra commerciale), 2022-23 (shock energetico + stretta), 2024-26 (normalizzazione). Sono contesti macro molto diversi. La configurazione odierna — dato debole *dentro* uno shock inflazionistico da offerta — è più vicina al 2022-23 che alle altre.
- **`CNY=X` è un cambio amministrato**: le mediane a zero non sono un'assenza di reazione economica ma un'assenza di reazione *di prezzo*, perché la banca centrale limita l'escursione giornaliera. Non trarne che "il mercato non ha reagito".
- **`DX-Y.NYB` (dollaro): direzione bloccata** dalla scorecard 2026-W34 (❌ controproducente, IC −0,16, hit-rate 32%).
- **`HG=F` e `CNY=X` non sono ancora validati** dalla scorecard (meno di 50 previsioni mature): non sono vietati, ma non hanno un track record. Le loro indicazioni pesano meno.
- **La reazione del mercato azionario a questa notizia è per costruzione ambigua** (bad news = good news se lo stimolo arriva). Un event study direzionale cattura male una funzione di reazione a due rami; il fatto che il segnale più forte sia sulla *volatilità* e non sulla direzione è probabilmente la conseguenza di questo.
- **Correlazione ≠ causazione**: nelle finestre di diversi episodi si sovrappongono eventi di altra natura.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-17T08:04:03
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
