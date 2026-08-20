# Selloff sincronizzato sulle scadenze lunghe: JGB decennale al 2,93% (massimo dal 1996), trentennale USA al top da 19 anni, gilt oltre il 5,05%

**Data analisi**: 2026-08-18
**Fonte**: Morning Briefing 2026-08-18 (fin 03, fin 04, fin 05, fin 06, fin 09, One Thing to Watch)
**Slug**: synchronised-long-end-selloff

---

## Testo notizia (originale)

> Quattro mercati obbligazionari maggiori sono simultaneamente su massimi pluridecennali. Il rendimento del titolo di Stato giapponese a 10 anni ha toccato il 2,930% lunedi e viaggia vicino al 2,95%, massimo da circa 29 anni e 10 mesi; il biennale all'1,650% (massimo dal 1995) e il quinquennale al 2,135% (record assoluto), su attese consolidate di rialzo della Bank of Japan alla riunione del 17-18 settembre (MUFG stima 1,25% dall'1,0% attuale). Il trentennale USA e' al massimo da 19 anni e il decennale intorno al 4,71-4,73%, con le aspettative di inflazione a un anno dell'Universita del Michigan sopra il 4% per il quinto mese consecutivo e segnali dal presidente della Fed Kevin Warsh che un rialzo dei tassi potrebbe non essere il suo strumento preferito contro l'inflazione; il mercato prezza ora circa 67% di probabilita che il FOMC resti fermo a settembre (sotto il 50% un mese fa), con target dei fed funds a 3,50-3,75%. Il decennale australiano supera il 5,04% e il trentennale il 5,60% dopo che la Reserve Bank of Australia ha tenuto fermo al 4,35% l'11 agosto pur avendo considerato un rialzo, con inflazione headline al 3,8% e ritorno al target non atteso prima dell'inizio 2028. Il gilt britannico decennale e' intorno al 5,06%, il tasso lungo piu' alto del G7, in attesa del dato di inflazione di luglio del 19 agosto, con un mercato del lavoro che si allenta (disoccupazione 4,9%, crescita salariale regolare 3,4%). Il driver comune e' un'aspettativa di inflazione, non una previsione di crescita. Il fattore offerta pesa: le societa dell'intelligenza artificiale hanno collocato circa 1.500 miliardi di dollari di obbligazioni quest'anno. Lunedi l'azionario USA e' sceso con Meta -3,5% e Microsoft -3,0%, cioe i nomi a duration lunga. L'oro sta sopra i 4.400 dollari (circa 4.430, +10,5% in un mese, +33,5% anno su anno) mentre i rendimenti nominali lunghi sono ai massimi: combinazione che non e un trade sui tassi reali ma un repricing della credibilita della risposta di politica economica.

---

## In breve (in parole semplici)

Quando un governo si indebita emette titoli di Stato; il "rendimento" di quei titoli è quanto il mercato pretende per prestargli denaro. Oggi quattro grandi mercati — Giappone, Stati Uniti, Australia, Regno Unito — chiedono contemporaneamente il rendimento più alto da decenni sulle scadenze lunghe. Il caso giapponese è il più clamoroso: il decennale al 2,93% non si vedeva dall'ottobre 1996.

La cosa insolita non è il livello, è la **sincronia**. Quattro banche centrali diverse, quattro cicli economici diversi, un unico movimento. E il motore comune non è l'aspettativa di più crescita (che di solito alza i tassi per buone ragioni) ma l'aspettativa di più **inflazione** insieme al dubbio che le banche centrali reagiscano. Due indizi lo confermano: l'oro è ai massimi *insieme* ai rendimenti — cosa che normalmente non accade, perché rendimenti alti rendono l'oro (che non paga cedole) meno attraente — e a Wall Street lunedì hanno sofferto proprio le società tecnologiche a "duration lunga", cioè quelle il cui valore dipende da utili molto in là nel tempo.

La domanda che ci poniamo: quando in passato il mercato ha ricalibrato al rialzo la traiettoria dei tassi per un pivot di comunicazione delle banche centrali, come si sono mossi nei giorni successivi tassi, azionario, yen, oro e volatilità?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | monetary_policy |
| `sub_themes` | guidance_pivot, boj, rate_decision |
| `sentiment` | hawkish |
| `confidence` | medium |
| `horizon` | 1-10 giorni di trading |

**Motivazione classificazione**: il tema è `monetary_policy` perché ciò che si muove è il prezzo del denaro a lunga scadenza, e ciò che lo muove è l'aspettativa su cosa faranno quattro banche centrali (BoJ a settembre, Fed che secondo il mercato terrà fermo, RBA che tiene la porta aperta a un rialzo, BoE stretta fra inflazione e lavoro debole). Il sotto-tema canonico è `guidance_pivot` — cioè un cambiamento nella *comunicazione* e nella funzione di reazione attesa, non una decisione già presa: nessuna delle quattro banche ha mosso i tassi in questi giorni. Il sentiment è `hawkish` perché la direzione del ricalcolo è "tassi più alti più a lungo". La confidence è `medium`: il fenomeno è nitido e ben documentato, ma è un movimento *già in corso da giorni* più che uno shock-notizia discreto, il che rende il momento zero dell'event study meno definito del solito.

Sono consolidate qui le notizie finanziarie 03 (JGB), 04 (Treasury USA e Michigan), 05 (Australia), 06 (gilt UK) e 09 (oro sopra 4.400 dollari), oltre alla "One Thing to Watch" del giorno, che è la stessa lettura. L'oro non ha una scheda propria: da solo è un movimento di prezzo senza uno shock-notizia discreto, ma come *co-movimento anomalo* con i rendimenti è un pezzo essenziale di questa storia.

---

## Asset rilevanti

### Primary (canale diretto)

- **^TNX** (rendimento del titolo di Stato USA a 10 anni, il Treasury — è il "tasso privo di rischio" di riferimento per la finanza mondiale) — l'asset centrale del fenomeno. ⚠ direzione storicamente inaffidabile, vedi sotto.
- **IEF** (ETF iShares che detiene Treasury USA con scadenza 7-10 anni; si muove **al contrario** del rendimento: se i tassi salgono, il prezzo delle obbligazioni già emesse scende) — proxy della duration americana. ⚠ direzione storicamente inaffidabile.
- **JPY=X** (cambio dollaro/yen: un numero più alto significa yen più debole) — la BoJ è l'epicentro; il differenziale di tasso fra Giappone e Stati Uniti è il canale.

### Secondary (effetti indiretti)

- **^NDX** (indice Nasdaq-100, le 100 maggiori società non finanziarie quotate al Nasdaq, fortemente tecnologiche) — il segmento più sensibile ai tassi lunghi, ed è dove il colpo è arrivato lunedì (Meta −3,5%, Microsoft −3,0%).
- **^GSPC** (S&P 500) — il mercato azionario USA nel suo complesso.
- **^STOXX50E** (Euro Stoxx 50) — l'area euro subisce il rialzo dei tassi globali senza esserne l'origine.
- **^N225** (indice Nikkei 225, la borsa di Tokyo) — canale diretto della normalizzazione BoJ.
- **^VIX** (indice di volatilità implicita dell'S&P 500) — misura se il mercato tratta il fenomeno come stress o come riprezzamento ordinato.
- **GC=F** (oro) — protagonista del co-movimento anomalo. ⚠ direzione storicamente inaffidabile.
- **DX-Y.NYB** (indice del dollaro contro un paniere di valute; a 99,5) — il differenziale di tasso dovrebbe rafforzarlo. ⚠ direzione storicamente inaffidabile.

---

## Knowledge Base — research correlate

- [score=9] `Fed_ reaction function, indipendenza e divergenza con la BCE (2023–2026)/...md` — *Fed: reaction function, indipendenza e divergenza con la BCE (2023–2026)*
  - Perché è rilevante: la notizia centrale non è un livello di tasso ma un dubbio sulla **funzione di reazione** della Fed (Warsh che segnala di non voler usare i rialzi contro l'inflazione). È esattamente l'oggetto di questa research.
- [score=8] `Giappone : Bank of Japan/... carry trade, uscita YCC e interventi FX ... (1998–2026).md` — *Giappone / Bank of Japan: carry trade, uscita YCC e interventi FX*
  - Perché è rilevante: il canale giapponese — uscita dal controllo della curva, rimpatrio dei capitali istituzionali, effetti sul carry trade — è il meccanismo che collega il JGB al resto delle curve mondiali.
- [score=4] `Regno Unito, shock politici e monetari — regime ed episodi storici (2016–2026)/...md`
  - Perché è rilevante: il gilt al 5,06% con inflazione al 2,6% e disoccupazione in salita è un premio a termine che i fondamentali domestici non giustificano — la research documenta i precedenti di questo scollamento (Truss 2022 in primis).
- [score=4] `ciclo_inflazione_eurozona_2021-2023/Ciclo inflazione Eurozona 2021–2023.md`
  - Perché è rilevante: il caso di scuola di come uno shock di offerta energetico si trasmetta alle aspettative di inflazione e poi alla reazione della banca centrale — la catena che collega la `news_01` a questa.

⚠ **Lacuna**: il catalogo ha uno studio *per ciascuna banca centrale* ma nessuno sul **premio a termine come fenomeno cross-mercato** — cioè esattamente il canale che collega le quattro curve di oggi, inclusa la fine del Giappone come esportatore netto di risparmio. Ho redatto il prompt di deep research in `knowledge_base/_prompts/premio-a-termine-globale-selloff-sincronizzati.md`; l'esecuzione spetta al maintainer (regola del 2026-08-16).

---

## Regime storico identificato

- **Regime**: normalizzazione tardiva globale con **credibilità sotto esame** (2025-2026). Non è il regime di stretta 2022-23 (in cui le banche centrali alzavano aggressivamente e il mercato le seguiva), né il regime di allentamento 2024 (tagli attesi). È una terza fase: inflazione riaccesa da uno shock di offerta, banche centrali che *non* stringono con decisione, e mercato che chiede un premio per tenersi il rischio.
- **Caratterizzazione**: tre elementi distinguono questo momento. (1) **Il Giappone esce definitivamente dal ruolo di ancora**: per trent'anni le istituzioni giapponesi hanno esportato risparmio comprando Treasury e titoli europei perché in patria rendevano zero; con il decennale nazionale vicino al 3% quel flusso si inverte, e con esso sparisce un compratore strutturale del debito altrui. (2) **Il premio a termine torna a essere il driver**, non l'aspettativa sui tassi a breve: negli Stati Uniti il mercato prezza il 67% di probabilità che la Fed *non* muova a settembre, eppure la parte lunga sale — il segno tipico di chi dubita della reazione, non della previsione. (3) **L'offerta di carta è enorme**: circa 1.500 miliardi di dollari di obbligazioni emesse quest'anno dalle sole società dell'intelligenza artificiale, in aggiunta alle emissioni sovrane.
- **Regime dell'oro**: la combinazione oro ai massimi + rendimenti nominali ai massimi è la firma di un repricing di credibilità fiscale/monetaria, non di un flight-to-quality (in una fuga verso la sicurezza i titoli di Stato salirebbero, cioè i rendimenti scenderebbero — sta succedendo l'opposto).

---

## Event study

### Episodi storici analoghi selezionati

Pool dalla libreria (Opzione B), tema `monetary_policy`, sotto-tema **date-locale** `guidance_pivot` (44 episodi disponibili a questo livello — filtro forte), direzione `neg`, no-look-ahead a `2026-08-18`; tetto di recency della libreria = 30 più recenti.

```bash
venv/bin/python analogues.py find --theme monetary_policy \
  --subtheme guidance_pivot --direction neg --before 2026-08-18
```

Il pool copre un arco temporale coerente (settembre 2022 → giugno 2026), cioè interamente dentro il ciclo inflazione-stretta-normalizzazione post-Covid, che è una buona notizia per l'omogeneità di regime. Le famiglie di episodi:

- `2022-09-08` → `2022-12-20` — il cuore della stretta: rialzi da 75 punti base di BCE e Fed, e il pivot della BoJ del 20 dicembre 2022 sull'ampliamento della banda di controllo della curva (che fece saltare in un giorno l'intero mercato JGB). Quest'ultimo è **l'analogo singolo più stretto** al canale giapponese di oggi.
- `2023-02-02` → `2023-10-19` — la fase "higher for longer": riunioni in cui la mossa sui tassi contava meno della revisione al rialzo del sentiero atteso.
- `2024-03-19`, `2024-03-20` — la BoJ esce dai tassi negativi e abbandona formalmente il controllo della curva; il giorno dopo la Fed conferma tre tagli nel *dot plot*. Coppia molto informativa: divergenza di comunicazione fra le due banche.
- `2024-05-01` → `2024-12-18` — riunioni FOMC con revisioni di guidance, incluso il 18 dicembre 2024 (taglio "hawkish").
- `2025-06-18` → `2026-06-11` — il regime corrente, quello più vicino per contesto (inflazione da offerta, banche centrali riluttanti).

Non ho potato: l'omogeneità di regime è già buona e ogni esclusione discrezionale avrebbe ridotto N sotto la soglia di comfort.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker '^TNX,IEF,JPY=X,^N225,^GSPC,^NDX,^STOXX50E,GC=F,^VIX,DX-Y.NYB' \
  --events 2022-09-08,2022-09-21,2022-12-14,2022-12-15,2022-12-20,2023-02-02,2023-03-16,2023-05-04,2023-06-15,2023-07-27,2023-08-01,2023-09-14,2023-09-20,2023-10-19,2024-03-19,2024-03-20,2024-05-01,2024-06-12,2024-07-31,2024-08-07,2024-09-18,2024-12-18,2025-06-18,2025-08-25,2025-10-01,2025-12-10,2026-01-21,2026-04-30,2026-05-13,2026-06-11 \
  --windows 1,3,5,10 --markdown
```

N = **30** su tutti i ticker.

### Risultati

> **Promemoria di lettura**: T+1/T+3/T+5/T+10 sono giorni di **borsa** dopo l'evento; i rendimenti sono cumulati. La mediana è il caso tipico, la media risente degli estremi. Se p25 e p75 hanno segno opposto, il campione non indica una direzione. Su `^TNX` il "rendimento" percentuale è la variazione **del rendimento stesso**, non del prezzo: +2% a T+10 significa che un rendimento del 4,50% è passato a circa 4,59%.

#### `^TNX` — rendimento Treasury USA 10 anni

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.23% | +1.09% | +1.14% | +2.11% |
| mediana | -0.07% | +0.59% | +0.17% | +1.16% |
| dev std | +2.04% | +3.59% | +3.55% | +5.63% |
| p25 | -0.54% | -0.90% | -1.34% | -1.07% |
| p75 | +0.92% | +2.31% | +4.46% | +6.37% |
| **N** | **30** | **30** | **30** | **30** |

⚠ **Direzione NON utilizzabile.** La scorecard corrente (2026-W34, sezione 5-bis) marca `^TNX` come **❌ controproducente**: Information Coefficient per-asset **−0,20** su 208 previsioni mature, hit-rate 45%. È il peggior risultato dopo IEF. Riporto la tabella per trasparenza, ma **il segno storico su questo asset è inaffidabile** e non ne traggo un'aspettativa: la mediana leggermente positiva a T+10 non è un argomento per attendersi rendimenti in salita.

#### `IEF` — ETF Treasury 7-10 anni

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.05% | -0.21% | -0.19% | -0.37% |
| mediana | +0.01% | -0.14% | -0.05% | -0.05% |
| dev std | +0.52% | +1.03% | +1.04% | +1.59% |
| p25 | -0.29% | -0.74% | -1.08% | -1.65% |
| p75 | +0.22% | +0.36% | +0.62% | +0.54% |
| **N** | **30** | **30** | **30** | **30** |

⚠ **Direzione NON utilizzabile.** `IEF` è l'asset con l'IC per-asset peggiore dell'intero sistema: **−0,29** su N=66, hit-rate 38% (scorecard 2026-W34, ❌ controproducente). Tabella riportata, nessuna previsione derivata. (È coerente che IEF e ^TNX siano entrambi rovesciati: sono lo stesso rischio visto da prezzo e da rendimento.)

#### `JPY=X` — cambio USD/JPY

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.16% | +0.04% | -0.22% | +0.46% |
| mediana | +0.07% | +0.24% | +0.19% | +0.64% |
| dev std | +1.05% | +1.65% | +1.90% | +1.92% |
| p25 | -0.29% | -0.51% | -1.32% | -0.69% |
| p75 | +0.41% | +1.18% | +0.88% | +1.64% |
| **N** | **30** | **30** | **30** | **30** |

**In pratica**: il caso tipico è uno yen che si **indebolisce** leggermente (USD/JPY in salita, mediana +0,64% a due settimane), ma con banda p25–p75 che a T+10 va da −0,69% a +1,64%, cioè attraversa lo zero. Segnale debole. Il dato è però contro-intuitivo e vale la pena spiegarlo: se la BoJ alza i tassi, in teoria lo yen dovrebbe rafforzarsi. Storicamente non è andata così, perché i rialzi giapponesi sono arrivati sempre più lentamente di quanto il mercato prezzasse e perché il differenziale con gli Stati Uniti restava enorme. Oggi il briefing conferma il fenomeno: yen a 159,4 nonostante il decennale giapponese al 2,93%. La scorecard classifica `JPY=X` come **⚠ debole** (IC +0,04, N=93): affidabilità modesta ma non rovesciata.

#### `^N225` — Nikkei 225

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.05% | -0.35% | -0.26% | +0.55% |
| mediana | -0.39% | -0.24% | -0.67% | +1.21% |
| dev std | +1.29% | +4.79% | +4.34% | +5.02% |
| p25 | -0.86% | -1.34% | -2.29% | -2.75% |
| p75 | +0.81% | +1.52% | +1.32% | +2.69% |
| **N** | **30** | **30** | **30** | **30** |

**In pratica**: la borsa di Tokyo scende nella prima settimana (mediana −0,67% a T+5) e recupera oltre (mediana +1,21% a T+10). È un profilo a V poco robusto — banda molto ampia, `^N225` marcato **⚠ debole** dalla scorecard (IC +0,00, N=79). Non ci costruirei sopra nulla.

#### `^GSPC` — S&P 500

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.03% | -0.16% | -0.38% | +0.27% |
| mediana | +0.22% | +0.52% | -0.33% | +0.33% |
| dev std | +1.18% | +2.10% | +2.43% | +3.06% |
| p25 | -1.09% | -1.36% | -2.23% | -1.47% |
| p75 | +0.86% | +1.08% | +1.48% | +1.50% |
| **N** | **30** | **30** | **30** | **30** |

**In pratica**: sostanzialmente **piatto**. Mediane fra −0,33% e +0,52%, con la banda centrale sempre a cavallo dello zero. La lettura onesta è che un pivot di comunicazione hawkish, storicamente, *non* ha spostato l'indice americano nell'arco di due settimane. Il danno, se c'è, si distribuisce dentro l'indice fra settori, non sull'indice.

#### `^NDX` — Nasdaq-100

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.04% | -0.15% | -0.38% | +0.28% |
| mediana | +0.40% | +0.46% | -0.48% | -0.35% |
| dev std | +1.60% | +2.71% | +3.46% | +4.21% |
| p25 | -1.10% | -2.03% | -3.27% | -2.13% |
| p75 | +1.10% | +1.70% | +2.72% | +2.22% |
| **N** | **30** | **30** | **30** | **30** |

**In pratica**: profilo simile all'S&P 500 ma con **il doppio della dispersione** (deviazione standard 4,21% a T+10 contro 3,06%) e mediana che vira in negativo dopo la prima settimana (−0,48% a T+5, −0,35% a T+10). Tradotto: il Nasdaq non scende *sistematicamente* dopo un pivot hawkish, ma sbanda molto di più. Ed è esattamente il rischio odierno, perché il meccanismo di trasmissione è pulito — il valore di una società tecnologica sta quasi tutto negli utili attesi fra cinque, dieci, quindici anni; per calcolare quanto valgono oggi si dividono per un tasso di sconto; se il tasso a lunga scadenza sale, il divisore cresce e il valore attuale scende, e scende **di più** quanto più lontani sono quegli utili. Meta −3,5% e Microsoft −3,0% lunedì sono la manifestazione manuale del fenomeno. `^NDX` è fra gli asset **✅ affidabili** della scorecard (IC +0,17, N=126), quindi qui il debole segnale negativo va preso più sul serio che altrove.

#### `^STOXX50E` — Euro Stoxx 50

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.30% | -0.39% | -0.22% | +0.44% |
| mediana | -0.07% | -0.07% | -0.06% | +0.60% |
| dev std | +1.67% | +2.16% | +2.16% | +2.45% |
| p25 | -1.44% | -0.87% | -1.53% | -1.32% |
| p75 | +0.98% | +0.87% | +1.20% | +2.38% |
| **N** | **30** | **30** | **30** | **30** |

**In pratica**: leggerissima flessione nella prima settimana, poi recupero (mediana +0,60% a T+10). Anche qui la banda attraversa sempre lo zero. `^STOXX50E` è **✅ affidabile** secondo la scorecard (IC +0,17, N=172), il che rende credibile l'indicazione — ma l'indicazione è "poco succede".

#### `^VIX` — volatilità implicita

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -1.42% | +1.63% | +0.77% | -1.03% |
| mediana | -2.21% | -2.64% | -1.82% | +1.68% |
| dev std | +8.24% | +28.24% | +21.32% | +18.53% |
| p25 | -6.61% | -10.76% | -6.75% | -13.15% |
| p75 | +1.93% | +5.58% | +10.55% | +9.42% |
| **N** | **30** | **30** | **30** | **30** |

**In pratica**: la volatilità **si sgonfia** nei primi giorni (mediana −2,64% a T+3) e poi risale (+1,68% a T+10). Il primo pezzo ha una spiegazione semplice: le riunioni di banca centrale sono eventi programmati, prima dei quali il mercato compra protezione; quando l'evento passa, quella protezione viene liquidata (il fenomeno noto come *vol crush*). Il secondo pezzo, la risalita, è più rumoroso: la deviazione standard a T+3 è del 28%, il che significa che il campione contiene sia episodi in cui non è successo nulla sia episodi in cui la volatilità è raddoppiata. `^VIX` è **✅ affidabile** in scorecard (IC +0,17, hit-rate 63%, N=101), ma qui il segnale che produce è "prima calma, poi incertezza", non una direzione netta.

#### `GC=F` — oro

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.16% | +0.28% | +0.80% | +0.92% |
| mediana | +0.34% | -0.12% | +0.52% | +0.77% |
| dev std | +1.30% | +2.08% | +2.96% | +3.87% |
| p25 | -0.58% | -1.10% | -1.33% | -1.94% |
| p75 | +0.72% | +1.58% | +2.00% | +3.14% |
| **N** | **30** | **30** | **30** | **30** |

⚠ **Direzione NON utilizzabile** — `GC=F` è **❌ controproducente** nella scorecard 2026-W34 (IC per-asset −0,07, hit-rate 47%, N=302). Tabella riportata per completezza; non deduco che l'oro debba salire.

#### `DX-Y.NYB` — indice del dollaro

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.06% | +0.09% | +0.17% | +0.26% |
| mediana | +0.07% | +0.06% | +0.32% | +0.71% |
| dev std | +0.42% | +0.93% | +0.94% | +1.23% |
| p25 | -0.20% | -0.49% | -0.11% | -0.78% |
| p75 | +0.30% | +0.51% | +0.73% | +1.06% |
| **N** | **30** | **30** | **30** | **30** |

⚠ **Direzione NON utilizzabile** — `DX-Y.NYB` è **❌ controproducente** (IC per-asset −0,16, hit-rate **32%**, N=156: il peggior hit-rate della tabella per-asset). Tabella riportata, nessuna aspettativa derivata.

### Lettura sintetica

Riassumendo per orizzonte, **usando solo gli asset su cui la scorecard corrente autorizza una lettura direzionale**:

| Asset | Giudizio scorecard | Mediana T+5 | Mediana T+10 | Cosa dice |
|---|---|---|---|---|
| ^NDX | ✅ affidabile (IC +0,17) | −0,48% | −0,35% | flessione lieve ma con dispersione doppia rispetto all'S&P 500 |
| ^STOXX50E | ✅ affidabile (IC +0,17) | −0,06% | +0,60% | sostanzialmente neutro |
| ^VIX | ✅ affidabile (IC +0,17) | −1,82% | +1,68% | *vol crush* iniziale, poi risalita |
| ^GSPC | ⚠ debole (IC +0,10) | −0,33% | +0,33% | piatto |
| JPY=X | ⚠ debole (IC +0,04) | +0,19% | +0,64% | yen leggermente più debole, segnale non robusto |
| ^N225 | ⚠ debole (IC 0,00) | −0,67% | +1,21% | profilo a V, non interpretabile |
| ^TNX, IEF, GC=F, DX-Y.NYB | ❌ controproducente | — | — | **nessuna direzione attesa: segno storico inaffidabile** |

Il messaggio complessivo è di **basso contenuto direzionale**: nessun asset con lettura autorizzata mostra un segnale forte. Questo è già un risultato utile — dice che, storicamente, un ricalcolo hawkish delle aspettative non ha prodotto nell'arco di due settimane il crollo azionario che l'intuizione suggerirebbe. L'unica indicazione con un po' di sostanza è la maggiore fragilità relativa del Nasdaq-100 rispetto all'S&P 500.

---

## Considerazioni qualitative

**Perché la sincronia conta più del livello.** Se un solo paese avesse rendimenti record, si cercherebbe una causa locale: un deficit, un'elezione, una sorpresa sull'inflazione. Quattro insieme, con cicli economici scollegati, indicano un fattore comune globale. Il briefing lo identifica correttamente: non è la crescita (nessuno prevede un boom), è l'inflazione attesa unita al dubbio sulla reazione. La prova è nella forma della curva americana: il mercato dà il 67% di probabilità che la Fed *stia ferma* a settembre e contemporaneamente vende la parte lunga. Chi si aspetta che la banca centrale non intervenga contro l'inflazione chiede più rendimento per tenersi il rischio di un'inflazione che dura — quello che i tecnici chiamano **premio a termine**.

**Il pezzo giapponese è quello strutturale.** Per trent'anni il Giappone ha avuto tassi a zero o negativi, e le sue istituzioni — fondi pensione, assicurazioni, banche — hanno esportato risparmio comprando Treasury americani e Bund tedeschi, perché in patria non rendevano nulla. Con il decennale giapponese vicino al 3% quella convenienza sparisce: conviene tenere i soldi in casa, e i capitali cominciano a rientrare. È un compratore strutturale di debito estero che si ritira, e la sua uscita alza i rendimenti *ovunque*, non solo a Tokyo. L'analogo storico più utile nel pool è il **20 dicembre 2022**, quando la BoJ ampliò a sorpresa la banda del controllo della curva dei rendimenti: quel giorno il decennale giapponese saltò, lo yen si rafforzò bruscamente e la scossa attraversò tutte le curve mondiali. La differenza fra allora e oggi è che quello fu uno shock puntuale a sorpresa, mentre questo è un processo annunciato e graduale — motivo in più per cui l'event study restituisce reazioni contenute.

**L'oro come indicatore, non come posizione.** L'oro non paga cedole. Quando i rendimenti nominali salgono, detenerlo costa di più in termini di rendimento rinunciato, e di norma il prezzo scende. Che stia salendo del 10,5% in un mese *mentre* quattro mercati obbligazionari toccano massimi pluridecennali è la parte veramente anomala del quadro. La lettura standard è che il compratore marginale non stia comprando "protezione dai tassi reali" ma **protezione dalla credibilità**: non si fida né della risposta della banca centrale all'inflazione né della sostenibilità delle traiettorie fiscali. È lo stesso segnale che dà l'obbligazionario, letto da un'altra finestra. Vale la pena ripeterlo: questa è una lettura *interpretativa*, non una previsione — sull'oro la scorecard ci vieta di trarre una direzione.

**Il collegamento con la scheda energia.** L'inflazione che sta alimentando questo movimento non è generica: le aspettative del Michigan sopra il 4% per cinque mesi consecutivi si formano su ciò che le famiglie pagano davvero, cioè benzina e gasolio — su del 57% e del 98% anno su anno secondo la `news_01`. È lo stesso shock, due anelli dopo. E qui sta la trappola per le banche centrali: uno shock di offerta energetica alza i prezzi *e* deprime la crescita insieme. Alzare i tassi non fa arrivare più petrolio; tenerli fermi lascia disancorare le aspettative. È precisamente la situazione in cui Warsh sembra dire che il rialzo dei tassi non è il suo strumento preferito — e in cui il mercato risponde alzandoglieli da solo sulla parte lunga della curva.

**Il caso britannico come test di rottura.** Il gilt decennale al 5,06% è il tasso lungo più alto del G7 in un'economia con inflazione al 2,6% (in calo dal 2,8%), disoccupazione al 4,9% (in salita di 0,2 punti in un anno), crescita dei salari al 3,4% (la più lenta dall'ottobre 2020) e posti vacanti scesi a 712.000. Questi fondamentali giustificherebbero tassi *più bassi*. Il fatto che il mercato ne pretenda di più altissimi significa che sta prezzando altro: l'offerta di titoli legata al deficit e il passaggio dei costi energetici. Se il dato di inflazione di luglio del 19 agosto sorprende al rialzo per la componente energia, la Bank of England si trova stretta fra un lavoro che si indebolisce e prezzi che accelerano — e il gilt è l'asset più esposto perché porta già un premio che i fondamentali non spiegano. ⚠ Nota di copertura: il progetto **non ha in database né il gilt né il JGB né il titolo australiano**; li discuto qualitativamente ma non possono entrare nell'event study. È la principale lacuna di questa scheda (vedi Caveat e "Lacune emerse" in `_index.md`).

---

## Glossario — sigle e termini

- **JGB** (*Japanese Government Bond*) — titolo di Stato giapponese.
- **Gilt** — titolo di Stato del Regno Unito.
- **BoJ** (*Bank of Japan*) — la banca centrale giapponese. **RBA** (*Reserve Bank of Australia*), **BoE** (*Bank of England*), **Fed** (*Federal Reserve*) — le rispettive di Australia, Regno Unito, Stati Uniti.
- **FOMC** (*Federal Open Market Committee*) — il comitato della Federal Reserve che decide i tassi USA; si riunisce otto volte l'anno.
- **Fed funds** — il tasso di riferimento americano, oggi in un intervallo di 3,50–3,75%.
- **Punto base (bp)** — un centesimo di punto percentuale: 75 bp = 0,75%.
- **Parte lunga / scadenze lunghe della curva** — i titoli di Stato a 10, 20, 30 anni. La "curva dei rendimenti" mette in grafico il rendimento per ogni scadenza; se le scadenze lunghe salgono più delle brevi la curva si "irripidisce" (*steepening*).
- **Premio a termine** (*term premium*) — il rendimento extra che un investitore pretende per prestare a lungo invece che rinnovare continuamente prestiti brevi. Compensa il rischio che inflazione e tassi futuri sorprendano al rialzo.
- **Duration** — la sensibilità del prezzo di un'obbligazione (o del valore di un'azione growth) a una variazione dei tassi. "Duration lunga" = molto sensibile.
- **YCC** (*Yield Curve Control*, controllo della curva dei rendimenti) — la politica con cui la BoJ fissava per decreto un tetto al rendimento del decennale giapponese comprando titoli senza limite. Abbandonata nel marzo 2024.
- **Carry trade** — prendere a prestito in una valuta a tasso basso (storicamente lo yen) per investire in una a tasso alto. Si smonta bruscamente quando il differenziale si riduce o la valuta di finanziamento si rafforza.
- **Dot plot** — il grafico in cui ogni membro del FOMC indica anonimamente dove vede i tassi negli anni successivi; è il principale strumento di *forward guidance* della Fed.
- **Forward guidance** — la comunicazione con cui una banca centrale orienta le aspettative sui tassi futuri, senza muovere il tasso oggi.
- **Funzione di reazione** (*reaction function*) — la regola implicita con cui una banca centrale risponde ai dati. Quando il mercato dubita della funzione di reazione, dubita non di *cosa* succederà all'inflazione ma di *cosa farà la banca centrale* al riguardo.
- **Michigan inflation expectations** — l'indagine mensile dell'Università del Michigan sulle aspettative di inflazione delle famiglie americane a un anno e a 5-10 anni; molto seguita perché le aspettative "disancorate" tendono a diventare inflazione reale via salari e prezzi.
- **CPI** (*Consumer Price Index*) — l'indice dei prezzi al consumo, la misura standard dell'inflazione.
- **PIL / GDP** — il prodotto interno lordo, il valore di tutto ciò che un'economia produce.
- **G7** — il gruppo delle sette maggiori economie avanzate (USA, Giappone, Germania, Regno Unito, Francia, Italia, Canada).
- **Tassi reali** — il tasso nominale meno l'inflazione attesa: quanto rende davvero un investimento in termini di potere d'acquisto.
- **Flight-to-quality** — la corsa verso gli attivi più sicuri (tipicamente titoli di Stato) durante uno stress; fa *scendere* i loro rendimenti. Il fatto che oggi i rendimenti salgano dice che non è questo che sta accadendo.
- **Vol crush** — il crollo della volatilità implicita subito dopo un evento programmato, quando la protezione comprata in anticipo viene liquidata.
- **^TNX** — rendimento del Treasury USA a 10 anni. **IEF** — ETF su Treasury 7-10 anni. **^NDX** — Nasdaq-100. **^GSPC** — S&P 500. **^STOXX50E** — Euro Stoxx 50. **^N225** — Nikkei 225. **^VIX** — indice di volatilità. **GC=F** — oro. **JPY=X** — cambio USD/JPY. **DX-Y.NYB** — indice del dollaro.
- **IC** (*Information Coefficient*) — correlazione di rango, calcolata a parità di asset, fra la direzione prevista dalla scheda e quella realizzata. Negativo = previsione sistematicamente rovesciata.

---

## Caveat

- **N = 30 su tutti i ticker**: campione utilizzabile (sopra la soglia di 10), regime relativamente omogeneo (tutti gli episodi fra settembre 2022 e giugno 2026).
- **Quattro asset su dieci hanno la direzione bloccata dalla scorecard.** `^TNX`, `IEF`, `GC=F` e `DX-Y.NYB` sono tutti marcati **❌ controproducente** in `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis. È una limitazione severa e ironica per questa scheda in particolare, perché sono proprio gli asset al centro della notizia: il sistema, storicamente, prevede male i tassi, il dollaro e l'oro. Le tabelle sono riportate; le direzioni non sono usate. Le uniche letture direzionali che mi permetto sono su `^NDX`, `^STOXX50E`, `^VIX` (✅ affidabili) e, con cautela, `^GSPC`.
- **Lacuna di knowledge base**: nessuna research copre il premio a termine cross-mercato. Prompt redatto oggi in `knowledge_base/_prompts/premio-a-termine-globale-selloff-sincronizzati.md`.
- **Copertura di mercato incompleta.** Tre dei quattro mercati protagonisti — gilt britannico, JGB giapponese, titolo australiano — **non sono nell'universo di 46 asset del progetto**. L'event study copre solo il canale americano più i riflessi su azionario, yen e volatilità. Questa è una lacuna strutturale, non un dettaglio: la scheda parla di un fenomeno obbligazionario globale con una sola curva misurabile.
- **Momento zero mal definito.** A differenza di una decisione di banca centrale, qui non c'è un istante preciso in cui l'informazione arriva: il selloff è in corso da giorni. L'event study assume un evento discreto, e questa assunzione qui è debole. Va letto come "cosa succede *tipicamente* attorno a un ricalcolo hawkish", non come "cosa succederà da questo esatto punto".
- **Il co-movimento oro/rendimenti è raro** e quindi poco rappresentato nel pool: gli episodi selezionati sono pivot di comunicazione generici, non specificamente casi di repricing di credibilità. Il campione potrebbe sottostimare la coda negativa.
- **Correlazione ≠ causazione**, e in diversi episodi del pool si sovrappongono eventi di natura diversa nella stessa finestra (per esempio marzo 2023, in piena crisi delle banche regionali americane).

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-17T08:04:03
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
