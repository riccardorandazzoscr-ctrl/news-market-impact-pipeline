# Il Kospi scatta il sidecar e perde 5,2%, Nikkei -2,6%: l'unwind del complesso AI in Asia dopo l'apertura cinese all'H200 di Nvidia

**Data analisi**: 2026-08-19
**Fonte**: Morning Briefing 2026-08-19 (fin 02)
**Slug**: asia-ai-memory-unwind

---

## Testo notizia (originale)

> Il Kospi ha aperto a -5%, allargando a -6% in pochi minuti e facendo scattare il meccanismo 'sidecar' della borsa coreana (sospensione per cinque minuti delle vendite guidate da programmi automatici), per poi chiudere la mattina a -5,2% intorno a 6.516; Samsung Electronics e SK Hynix hanno perso circa il 7% ciascuna. Il Nikkei 225 ha ceduto il 2,6% a circa 65.704, con Tokyo Electron -4% e il produttore di memorie Kioxia -9%; anche le borse cinesi hanno aperto in calo. L'innesco e' stato il selloff dei semiconduttori USA di martedi', amplificato da un articolo del Financial Times secondo cui Pechino sta autorizzando spedizioni limitate dei processori H200 di Nvidia, con ByteDance e Tencent destinatarie di circa 10.000 unita' ciascuna: un fatto positivo per la domanda di Nvidia ma competitivamente negativo per i fornitori di memoria coreani e giapponesi, le cui valutazioni assumono che gli acquirenti cinesi restino vincolati dall'offerta. E' il terzo drawdown distinto legato all'AI da fine luglio.

---

## In breve (in parole semplici)

La borsa coreana ha perso il 5,2% in una mattinata, facendo scattare un meccanismo automatico di sospensione, e i due giganti mondiali della memoria — Samsung Electronics e SK Hynix — hanno lasciato sul terreno circa il 7% ciascuno. Il Giappone ha seguito, con il produttore di memorie Kioxia a −9%.

Il motivo è un'apparente buona notizia letta al contrario: Pechino sta autorizzando l'ingresso di un numero limitato di processori H200 di Nvidia. Bene per Nvidia, male per chi vende memoria ai cinesi — perché il prezzo alto delle memorie si regge sull'ipotesi che i compratori cinesi restino a secco.

Ci chiediamo: dopo uno shock che colpisce il *ciclo della memoria*, cosa è successo storicamente nei dieci giorni di borsa successivi a semiconduttori, Corea e Taiwan?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | structural_themes |
| `sub_themes` | memory_cycle, valuation_derisking, kospi |
| `sentiment` | risk-off |
| `confidence` | medium |
| `horizon` | 1-5 giorni di trading (il tema è strutturale: la finestra breve va letta come indicativa) |

**Motivazione classificazione**: `structural_themes` perché l'oggetto è il ciclo di investimento nell'intelligenza artificiale e nella memoria, non un singolo risultato aziendale né un dato macro. Il sotto-tema canonico primario è `memory_cycle`, che nella libreria ha 13 episodi con **etichetta date-locale** (filtro forte): è esattamente il canale colpito, cioè le aspettative sui prezzi di DRAM e HBM. Sentiment `risk-off` con una precisazione: la notizia è *positiva* per Nvidia e *negativa* per i fornitori di memoria coreani e giapponesi — il segno dipende da dove si sta nella catena del valore, ed è il motivo per cui la scheda separa SOXX/^NDX (indici che contengono Nvidia) da EWY/EWT (esposti ai fornitori). Confidence `medium`: la meccanica è chiara, ma il briefing stesso osserva che il vincolo operativo è il **posizionamento**, non i fondamentali, e il posizionamento è la variabile che i nostri analoghi catturano peggio.

⚠ **Nota metodologica sul tema.** `structural_themes` copre fenomeni di orizzonte pluriennale, e la mappa asset lo dice esplicitamente: l'event study a 1-10 giorni è *meno* informativo qui. Lo eseguiamo perché lo shock di oggi è un evento di prezzo discreto e databile, ma la lettura resta tattica, non una previsione sul ciclo.

---

## Asset rilevanti

### Primary (canale diretto)
- **SOXX** (ETF iShares sui semiconduttori, proxy dell'indice di Filadelfia) — il complesso semiconduttori: contiene sia i beneficiari (Nvidia) sia i penalizzati.
- **^NDX** (indice Nasdaq-100, le 100 maggiori società non finanziarie del Nasdaq) — proxy diretto del capex sull'intelligenza artificiale e delle mega-cap tecnologiche.

### Secondary (effetti indiretti)
- **EWY** (ETF iShares MSCI South Korea) — proxy quotato del Kospi: Samsung Electronics e SK Hynix ne dominano il peso. È l'asset **più direttamente** colpito dalla notizia di oggi, benché la mappa lo classifichi secondary.
- **EWT** (ETF iShares MSCI Taiwan) — proxy di TSMC e della catena dei semiconduttori avanzati.
- **^N225** (indice Nikkei 225, Tokyo) — Tokyo Electron e Kioxia; il canale giapponese della stessa catena.
- **EEM** (ETF iShares MSCI Emerging Markets) — Corea e Taiwan pesano molto nell'indice: canale aggregato emergenti.
- **^VIX** (indice della volatilità implicita a 30 giorni sull'S&P 500) — misura se lo shock asiatico si traduce in domanda di protezione negli Stati Uniti.
- **^GSPC** (indice S&P 500) — controllo: quanto dello shock è idiosincratico al complesso AI e quanto è mercato generale.

---

## Knowledge Base — research correlate

- [score=14] `Ciclo della memoria DRAM-NAND-HBM e mercato azionario coreano (2016–2026)/…md` — *Ciclo della memoria (DRAM/NAND/HBM) e mercato azionario coreano: regime ed episodi storici (2016–2026)*
  - Perché è rilevante: è la research dedicata esattamente a questo meccanismo — come i cicli di prezzo delle memorie si trasmettono al mercato azionario coreano — e copre sia SOXX sia EWY.
- [score=7] `Ciclo semiconduttori & AI capex (2023–2026)/…md` — *Ciclo semiconduttori & AI capex: catalizzatori discreti e trasmissione*
  - Perché è rilevante: fornisce la tassonomia dei catalizzatori discreti (controlli all'export, annunci di capex, risultati trimestrali) di cui l'apertura cinese all'H200 è un caso.
- [score=5] `Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)/…md`
  - Perché è rilevante: i controlli all'export sui chip verso la Cina sono uno strumento di politica commerciale, e la loro parziale rimozione va letta in quel quadro.

---

## Regime storico identificato

- **Regime**: fase avanzata del ciclo di capex sull'intelligenza artificiale, con **de-risking delle valutazioni** in corso da fine luglio 2026.
- **Caratterizzazione**: il briefing lo dice in modo netto — questo è il **terzo drawdown distinto legato all'AI da fine luglio**, e il fatto che si propaghi attraverso i circuit breaker (i meccanismi automatici di sospensione delle contrattazioni) anziché tramite un riprezzamento ordinato indica che il vincolo attivo è il posizionamento, non i fondamentali. Il contesto lo conferma: il Fund Manager Survey di Bank America di agosto (notizia fin 10 del briefing, scartata dal triage come non event-studiabile) riporta liquidità al 3,5% degli attivi, la sesta lettura più bassa dal 1998, e allocazione azionaria ai massimi da novembre 2021, con "scarsa preoccupazione" dichiarata proprio sul capex AI. **Complacency registrata e drawdown in corso sono lo stesso fenomeno osservato in due momenti diversi.** In un regime così, l'ampiezza dei movimenti dipende da quanto c'è da liquidare, non da quanto la notizia sia grave.
- Ulteriore elemento di regime, specifico di oggi: il vincolo che sosteneva i prezzi della memoria era **regolamentare** (i compratori cinesi non potevano accedere ai chip avanzati). Se quel vincolo si allenta, cambia la struttura del mercato, non solo il livello dei prezzi.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla libreria (Opzione B) con:
`--theme structural_themes --subtheme memory_cycle --direction neg --before 2026-08-19`
→ 13 episodi con etichetta **date-locale** (filtro forte), potati a **12** dall'analista.

**Potatura effettuata:**
- `2023-05-25` — reazione ai risultati trimestrali di Nvidia con la guidance che aprì il ciclo AI: è lo shock **positivo** più grande del campione sui semiconduttori. Tenerlo in un pool di shock negativi avrebbe drogato al rialzo tutte le mediane.

**Episodi tenuti** (con il meccanismo, non solo il fatto):

- `2019-06-25` — fase di taglio della domanda di memoria durante la guerra commerciale USA-Cina: **restrizioni all'export che colpiscono i volumi dei fornitori asiatici → compressione dei multipli su Corea e semiconduttori**.
- `2021-11-30` — svolta della Federal Reserve sul "transitorio" e shock Omicron: **rialzo del tasso di sconto sui flussi di cassa lontani → de-rating delle valutazioni growth, di cui i semiconduttori sono la parte più sensibile**.
- `2023-04-06` — Samsung annuncia un taglio significativo della produzione di memoria: **risposta dell'offerta a un eccesso di scorte → punto di svolta del ciclo dei prezzi DRAM**.
- `2023-05-22` — riprezzamento della catena memoria alla vigilia del ciclo AI: **rotazione fra fornitori di memoria e produttori di acceleratori**.
- `2023-07-27` — stretta finanziaria che colpisce il complesso growth: **canale tasso di sconto sulle valutazioni AI**.
- `2023-11-09` — de-risking delle valutazioni dopo un rally sui semiconduttori: **presa di profitto su posizionamento affollato, non su cambio di fondamentali**.
- `2025-01-27` — shock DeepSeek: **un modello cinese a costo dichiarato molto inferiore mette in discussione la necessità del capex → il caso di scuola di "shock di capacità del modello" che riprezza l'intera catena in una seduta**.
- `2025-02-27` — reazione negativa ai risultati di Nvidia nonostante il superamento delle stime: **quando l'asticella implicita è più alta della guidance, il beat non basta → compressione dei multipli**.
- `2025-09-19` — episodio di derisking sul complesso AI: **rotazione di posizionamento**.
- `2026-07-02` — primo dei drawdown AI dell'estate 2026: **avvio del ciclo di riduzione dell'esposizione**.
- `2026-07-29` — secondo drawdown AI: **conferma che si tratta di una sequenza, non di un episodio isolato**.
- `2026-08-14` — terzo episodio recente della stessa sequenza, cinque giorni di borsa fa: **è l'analogo più prossimo per regime e posizionamento**; ha però meno storia realizzata (vedi caveat sull'N).

### Comando eseguito

```bash
venv/bin/python analogues.py find --theme structural_themes --subtheme memory_cycle \
  --direction neg --before 2026-08-19

venv/bin/python event_study.py \
  --ticker 'SOXX,^NDX,EWY,EWT,^N225,^VIX,EEM,^GSPC' \
  --events 2019-06-25,2021-11-30,2023-04-06,2023-05-22,2023-07-27,2023-11-09,2025-01-27,2025-02-27,2025-09-19,2026-07-02,2026-07-29,2026-08-14 \
  --windows 1,3,5,10 --markdown
```

### Risultati

Rendimenti cumulati a T+1, T+3, T+5, T+10 **giorni di borsa** dopo l'episodio (T+0 = giorno dell'evento, cioè il giorno in cui lo shock è già avvenuto).

### Event study — `SOXX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +2.12% | +2.49% | +3.78% | +2.63% |
| mediana | +1.68% | +2.67% | +2.65% | +3.36% |
| dev std | +2.52% | +3.45% | +5.30% | +7.46% |
| p25 | +1.23% | -0.69% | +0.41% | -2.92% |
| p75 | +2.82% | +4.16% | +6.91% | +7.07% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `^NDX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.82% | +0.83% | +1.75% | +1.32% |
| mediana | +0.90% | +0.64% | +1.18% | +0.65% |
| dev std | +1.45% | +2.48% | +2.97% | +4.51% |
| p25 | -0.11% | -0.73% | -0.18% | -1.77% |
| p75 | +1.68% | +1.72% | +3.20% | +4.61% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `EWY`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +2.15% | +2.15% | +2.77% | +2.29% |
| mediana | +1.83% | +1.43% | +0.52% | +2.67% |
| dev std | +3.64% | +3.61% | +5.79% | +7.96% |
| p25 | +0.42% | +0.55% | -1.39% | -2.34% |
| p75 | +2.37% | +3.52% | +5.26% | +4.43% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `EWT`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +1.18% | +1.69% | +2.32% | +2.09% |
| mediana | +1.04% | +0.59% | +1.27% | +1.99% |
| dev std | +1.54% | +2.93% | +4.47% | +6.78% |
| p25 | +0.24% | +0.28% | +0.22% | -2.23% |
| p75 | +1.60% | +2.08% | +3.42% | +4.07% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `^N225`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.17% | +0.48% | +0.88% | +1.98% |
| mediana | -0.04% | +0.39% | +0.47% | +2.20% |
| dev std | +1.11% | +1.65% | +3.12% | +4.53% |
| p25 | -0.44% | -0.53% | -1.81% | -1.60% |
| p75 | +0.53% | +1.61% | +2.44% | +3.98% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `^VIX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -1.17% | -0.84% | -4.22% | -8.08% |
| mediana | -1.27% | -0.12% | -1.92% | -11.68% |
| dev std | +8.82% | +11.12% | +13.03% | +15.17% |
| p25 | -7.37% | -7.38% | -13.36% | -19.19% |
| p75 | +4.80% | +7.97% | +2.74% | +5.68% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `EEM`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.91% | +1.01% | +1.51% | +1.42% |
| mediana | +0.72% | +0.81% | +0.89% | +1.48% |
| dev std | +1.62% | +2.17% | +2.56% | +3.35% |
| p25 | +0.30% | +0.08% | +0.00% | -0.52% |
| p75 | +1.40% | +1.99% | +2.50% | +2.99% |
| **N** | **12** | **11** | **11** | **11** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.42% | +0.57% | +1.15% | +1.07% |
| mediana | +0.58% | -0.01% | +0.79% | +0.90% |
| dev std | +1.00% | +1.71% | +2.19% | +3.13% |
| p25 | -0.22% | -0.51% | -0.30% | +0.18% |
| p75 | +1.13% | +0.92% | +2.26% | +2.39% |
| **N** | **12** | **11** | **11** | **11** |

**In pratica, cosa dicono questi numeri.**

Il risultato è coerente e va detto con chiarezza: **nei dodici episodi analoghi il mercato ha rimbalzato, non è affondato ulteriormente.**

- **SOXX (semiconduttori)**: mediana **+1,68% a T+1** e **+2,67% a T+3**, con il primo quartile positivo a T+1 (+1,23%) — cioè in oltre tre casi su quattro il giorno dopo lo shock il settore era già in guadagno. A T+10 la mediana è +3,36%, ma il primo quartile scende a −2,92%: il rimbalzo di breve è robusto, quello a due settimane no.
- **EWY (Corea)**: mediana +1,83% a T+1, +1,43% a T+3, +2,67% a T+10 — ma con dispersione crescente (deviazione standard dal 3,6% all'8,0%). Corea è l'asset più esposto e anche il più volatile.
- **EWT (Taiwan)**: profilo simile ma più contenuto (+1,04% / +0,59% / +1,99%): coerente con il fatto che TSMC produce, non vende memoria, e quindi è meno direttamente colpita dall'apertura cinese all'H200.
- **^NDX (Nasdaq-100)**: mediana +0,90% a T+1 e +0,65% a T+10 — un rimbalzo reale ma di un ordine di grandezza inferiore a quello dei semiconduttori. ✅ La scorecard 2026-W34 classifica ^NDX fra gli asset **affidabili** (IC +0,17 su N=126): è il ticker su cui la lettura direzionale di questa scheda poggia meglio.
- **^VIX (volatilità)**: mediana in discesa e sempre più negativa con l'orizzonte (−1,27% a T+1, −11,68% a T+10): il premio per la paura si sgonfia man mano che lo shock viene digerito. ✅ Anche ^VIX è fra gli asset affidabili in scorecard (IC +0,17, hit-rate 63%).
- **EEM (emergenti)**: mediana positiva e sorprendentemente stabile su tutti gli orizzonti (+0,72% → +1,48%), con primo quartile mai sotto zero fino a T+5. ✅ Affidabile in scorecard (IC +0,17). È la conferma che lo shock resta confinato al complesso tecnologico e non contamina l'universo emergenti nel suo insieme.
- **^N225 (Nikkei)**: l'unico con mediana negativa a T+1 (−0,04%), poi positiva. Il Giappone assorbe più lentamente perché ha sia i fornitori penalizzati sia una valuta che si muove in senso contrario.
- **^GSPC**: +0,58% a T+1, +0,90% a T+10 — l'S&P 500 fa quasi nulla. **Questo è il dato più importante di tutta la tabella**: lo shock è settoriale, non sistemico.

**Perché il rimbalzo, e perché diffidarne.** Il meccanismo del rimbalzo è meccanico: l'event study parte dalla chiusura del giorno dello shock, quando il ribasso è già avvenuto. Se la vendita è guidata da liquidazione di posizioni (margin call, stop automatici, sidecar) e non da un peggioramento dei fondamentali, l'eccesso rientra nelle sedute successive. Il campione lo conferma. **Il caveat è che il campione contiene sia rimbalzi che erano davvero il fondo, sia rimbalzi che precedevano nuove gambe di ribasso** — la dispersione crescente a T+10 (primo quartile SOXX a −2,92%) è esattamente questo.

**Regime misto — da dichiarare.** Il campione mescola tre regimi diversi: la guerra commerciale pre-AI (2019), il ciclo di scorte della memoria (2023), e il ciclo di capex AI (2025-2026). Solo gli ultimi tre episodi (luglio-agosto 2026) condividono il regime di posizionamento estremo che il Fund Manager Survey documenta oggi. Se si guardassero solo quelli, N=3 e la scheda sarebbe puramente aneddotica.

---

## Considerazioni qualitative

Vale la pena chiarire il meccanismo, perché la notizia è controintuitiva: *perché una buona notizia per Nvidia fa crollare Seul?*

Il prezzo delle memorie ad alta larghezza di banda (HBM, High Bandwidth Memory — la memoria specializzata che affianca i chip acceleratori nei data center per l'intelligenza artificiale) è alto per due ragioni distinte. La prima è la domanda: servono per addestrare e far girare i modelli. La seconda, meno ovvia, è **regolamentare**: i controlli USA all'export hanno tenuto i grandi compratori cinesi fuori dal mercato dei chip avanzati, e quindi anche fuori dal mercato della memoria che li accompagna. Samsung e SK Hynix hanno beneficiato di un mercato in cui una fetta enorme di domanda potenziale era congelata *ma* l'offerta era tarata su quel mondo.

Se Pechino ora autorizza l'ingresso degli H200 — anche solo 10.000 unità a testa per ByteDance e Tencent — succedono due cose in direzioni opposte. Nvidia guadagna un mercato. I fornitori di memoria coreani e giapponesi, invece, perdono la *scarsità artificiale*: se i cinesi possono comprare acceleratori Nvidia con memoria integrata nella catena Nvidia, la struttura della domanda cambia, e le valutazioni che scontavano un mercato permanentemente vincolato dall'offerta devono essere riviste. È un riprezzamento della **struttura**, non del ciclo.

Il secondo elemento è il modo in cui il ribasso si è propagato. Un "sidecar" è un meccanismo della borsa coreana che sospende per cinque minuti gli ordini generati da programmi automatici quando i future si muovono oltre una soglia. Che venga attivato significa che la vendita non stava arrivando da investitori che riconsiderano il valore delle aziende, ma da sistemi che vendono perché il prezzo scende. Questa distinzione — riprezzamento ordinato contro liquidazione forzata — è la ragione per cui l'event study mostra rimbalzi: **le liquidazioni forzate rientrano, i riprezzamenti fondamentali no.**

Il terzo elemento è il contesto di posizionamento, e qui va detta la cosa scomoda. Il Fund Manager Survey mostra liquidità ai minimi da quasi trent'anni e allocazione azionaria da record recente, con gli intervistati che dichiarano di non preoccuparsi né dei rialzi dei tassi né del capex AI. Quando la liquidità è quella, non esiste un ammortizzatore: ogni ondata di vendite deve trovare un compratore che, per definizione, è già investito. Il briefing coglie il nesso con la scheda [news_03](news_03.md): *"spiega perché un movimento di 5 punti base sul trentennale sta producendo movimenti del 5% sul Kospi"*. Cinque punti base sono un'inezia; il 5% no. La sproporzione è la misura della leva di posizionamento.

**Lettura direzionale.** Su ^NDX, ^VIX ed EEM — i tre asset che la scorecard 2026-W34 classifica come affidabili — il campione indica un **rimbalzo modesto e un rientro della volatilità nell'arco di 1-3 giorni di borsa**, con l'S&P 500 sostanzialmente fermo, cioè shock confinato al settore. Su SOXX la lettura direzionale va presa con più cautela: la scorecard lo marca ⚠️ **debole** (IC −0,03 su N=71, hit-rate 46%), quindi la mediana positiva di +2,67% a T+3 non è un'indicazione su cui costruire. Su EWY ed EWT la scorecard non fornisce ancora un giudizio (meno di 50 previsioni mature: sono in DB solo dal 2026-08-10), quindi vanno letti come descrittivi.

---

## Glossario — sigle e termini

- **AI (Artificial Intelligence)** — intelligenza artificiale; qui in particolare i modelli di grandi dimensioni che richiedono hardware specializzato.
- **DRAM** — Dynamic Random Access Memory, la memoria di lavoro standard dei computer.
- **NAND** — memoria flash non volatile (quella che conserva i dati a computer spento).
- **HBM (High Bandwidth Memory)** — memoria ad alta larghezza di banda, impilata in verticale e collocata accanto al chip acceleratore: è il collo di bottiglia fisico dei sistemi per l'intelligenza artificiale, e il prodotto a margine più alto di SK Hynix e Samsung.
- **H200** — acceleratore Nvidia per data center, generazione precedente ai modelli di punta ma soggetto a controlli all'export verso la Cina.
- **Capex** — capital expenditure, la spesa per investimenti in beni durevoli; qui la spesa dei grandi operatori cloud in data center e chip.
- **Sidecar** — meccanismo della borsa coreana che sospende per cinque minuti gli ordini generati da programmi automatici quando i future superano una soglia di variazione. Diverso dal "circuit breaker", che sospende l'intero mercato.
- **Kospi** — indice principale della borsa di Seul. Non è nel nostro DB: usiamo **EWY** come proxy quotato.
- **SOXX** — ETF iShares sui semiconduttori, proxy dell'indice di Filadelfia (PHLX Semiconductor).
- **^NDX** — indice Nasdaq-100: le 100 maggiori società non finanziarie quotate al Nasdaq.
- **EWY / EWT / EEM** — ETF iShares su Corea del Sud, Taiwan e mercati emergenti.
- **^N225** — indice Nikkei 225 della borsa di Tokyo.
- **^VIX** — indice CBOE della volatilità implicita a 30 giorni sull'S&P 500.
- **^GSPC** — indice azionario S&P 500.
- **De-rating / de-risking delle valutazioni** — compressione dei multipli (es. prezzo/utili) senza che gli utili attesi cambino: il mercato paga meno per lo stesso flusso di cassa, perché sconta a un tasso più alto o richiede più premio per il rischio.
- **Drawdown** — perdita dal massimo precedente.
- **T+N** — N giorni di **borsa** dopo il giorno dell'evento.
- **Mediana vs media** — la mediana è il valore centrale del campione ed è robusta agli episodi estremi; la media può essere trascinata da un singolo caso.
- **p25 / p75** — primo e terzo quartile; la loro distanza misura la dispersione, cioè quanto poco affidabile è il valore centrale.
- **Information Coefficient (IC)** — correlazione di rango fra previsione storica e risultato realizzato, calcolata nella scorecard settimanale. Positivo = utile; negativo = sistematicamente rovesciato.

---

## Caveat

1. **N al limite.** N=12 a T+1 ma **N=11 a T+3, T+5 e T+10**, perché l'episodio del 2026-08-14 non ha ancora dieci giorni di borsa realizzati. Il sistema non applica il flag "INDICATIVE ONLY" (che scatta sotto N=10), ma siamo a un episodio di distanza: trattare questi numeri come indicazioni di direzione, non come stime di ampiezza.
2. **Tema strutturale, finestra tattica.** `structural_themes` ha orizzonte pluriennale per costruzione. La mappa asset avverte esplicitamente di non usare questa categoria per inferire impatti di breve. L'abbiamo fatto perché lo shock è discreto e databile, ma il risultato descrive la dinamica di *posizionamento* nei giorni successivi, non l'esito del ciclo della memoria.
3. **Regime misto.** Il campione copre guerra commerciale pre-AI (2019), ciclo scorte memoria (2023) e ciclo capex AI (2025-2026). Solo tre episodi condividono l'attuale regime di posizionamento estremo.
4. **Il bias meccanico del rimbalzo.** L'event study misura dalla chiusura del giorno dello shock in poi: per costruzione cattura il rientro dell'eccesso, non la continuazione. Un campione di soli shock negativi tende a produrre mediane positive nei giorni successivi. È informazione utile (dice che le liquidazioni rientrano) ma **non è una previsione di rialzo**.
5. **Asset con lettura direzionale debole o non giudicata.** **SOXX** è ⚠️ debole in scorecard (IC −0,03, hit-rate 46%): non ne traiamo una direzione. **EWY** ed **EWT** non hanno ancora abbastanza previsioni mature per un giudizio (in DB dal 2026-08-10): descrittivi. Gli asset su cui la lettura poggia sono **^NDX, ^VIX ed EEM** (tutti ✅ affidabili, IC +0,17).
6. **Asimmetria del segno lungo la catena del valore.** La stessa notizia è positiva per Nvidia (dentro SOXX e ^NDX) e negativa per Samsung/SK Hynix (dentro EWY). Gli indici la mediano: nessuno dei nostri asset isola il lato penalizzato in modo puro.
7. **Potatura discrezionale.** Un episodio (2023-05-25) è stato rimosso dal pool della libreria perché direzionalmente opposto. La scelta è motivata sopra, ma resta una scelta dell'analista.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Pool analoghi: libreria episodi (Opzione B), filtro date-locale `memory_cycle`, direzione `neg`, no-look-ahead `--before 2026-08-19`
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
- Catalog timestamp: 2026-08-19T07:27:10
