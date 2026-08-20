# Il rialzo Fed di settembre e' stato prezzato via: 69% di probabilita' di 'hold', biennale ai minimi da sette settimane

**Data analisi**: 2026-08-17
**Fonte**: Morning Briefing 2026-08-17 (fin 04)
**Slug**: fed-september-hike-priced-out

---

## Testo notizia (originale)

> Il CME FedWatch al 14 agosto assegna il 69% di probabilita' a un nulla di fatto del FOMC in settembre, ribaltando l'inizio del mese quando il rialzo era l'esito modale. La ri-prezzatura e' guidata dai payroll di luglio, da letture di inflazione benigne, dal -0,6% delle vendite al dettaglio e da una fiducia dei consumatori dell'Universita' del Michigan a 51,0 contro 54,5 attesi. Le probabilita' di almeno un rialzo entro fine anno restano vicine al 63%: il mercato ha rinviato, non cancellato. Il rendimento del Treasury biennale e' sceso di 2 punti base a 4,156% dopo aver toccato un minimo di sette settimane a 4,0977%; il decennale cede 1 punto base a 4,684%. Il dollaro si e' indebolito di conseguenza, con l'euro a 1,1578 poco sotto il picco di due mesi a 1,1585.

---

## In breve (in parole semplici)

Fino a due settimane fa il mercato dava per probabile che la banca centrale americana alzasse i tassi a settembre. Oggi non più: i contratti derivati sui tassi assegnano il 69% di probabilità a un "non fare nulla". Il cambio d'idea è arrivato da una serie di dati deboli — meno posti di lavoro creati, inflazione tranquilla, vendite al dettaglio in calo dello 0,6%, fiducia dei consumatori crollata a 51,0 contro 54,5 attesi.

Perché conta: quando il mercato smette di aspettarsi tassi più alti, i rendimenti dei titoli di Stato a breve scendono (il biennale ha toccato il minimo di sette settimane), il dollaro si indebolisce e le azioni — soprattutto quelle "growth", che valgono per gli utili lontani nel tempo — tendono a beneficiarne, perché quegli utili futuri vengono scontati a un tasso più basso e quindi valgono di più oggi.

Il dettaglio che il briefing sottolinea giustamente: il mercato ha **rinviato, non cancellato**. Le probabilità di almeno un rialzo entro fine anno restano al 63%. E tutta questa ri-prezzatura poggia sull'ipotesi che l'energia si comporti bene — proprio mentre la tregua con l'Iran scade (vedi `news_01.md`).

La domanda che ci poniamo: quando in passato la Fed ha dato un segnale accomodante o il mercato ha ri-prezzato al ribasso il percorso dei tassi, come si sono mossi azionario, tassi, dollaro e volatilità?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | monetary_policy |
| `sub_themes` | guidance_pivot, fed, rate_decision |
| `sentiment` | dovish |
| `confidence` | medium |
| `horizon` | 1-5 giorni di trading |

**Motivazione classificazione**: l'oggetto è il percorso atteso dei tassi ufficiali americani, quindi `monetary_policy`. Il sotto-tema è `guidance_pivot` (svolta nelle aspettative di policy) più che `rate_decision`, perché non c'è stata alcuna decisione: è il *mercato* ad aver spostato le probabilità, non il FOMC ad aver deliberato. Il sentiment è `dovish` (accomodante). La `confidence` è **medium** per due ragioni opposte che si compensano: da un lato la ri-prezzatura è già avvenuta e visibile nei prezzi (quindi poco resta da scontare), dall'altro è fragile perché condizionata al petrolio.

---

## Asset rilevanti

### Primary (canale diretto)
- **^TNX** (rendimento del titolo di Stato USA a 10 anni) e **IEF** (ETF iShares su Treasury a 7-10 anni, proxy della duration americana) — sono il canale diretto: meno rialzi attesi significa rendimenti più bassi e prezzi delle obbligazioni più alti.
- **DX-Y.NYB** (indice del dollaro, che misura il dollaro contro un paniere di sei valute) e **EURUSD=X** (cambio euro/dollaro) — un percorso di tassi più basso riduce l'attrattiva del dollaro.

### Secondary (effetti indiretti)
- **^GSPC** (indice azionario S&P 500) — reagisce al tasso privo di rischio: tassi più bassi = fattore di sconto più basso = valutazioni più alte.
- **^NDX** (indice azionario Nasdaq-100, le 100 maggiori società non finanziarie del Nasdaq, a forte peso tecnologico) — è il segmento *growth*, il più sensibile al tasso di sconto perché i suoi utili sono concentrati lontano nel tempo.
- **GC=F** (futures sull'oro) — l'oro non paga cedole, quindi soffre quando i tassi reali salgono e beneficia quando scendono.
- **^VIX** (indice di volatilità implicita sull'S&P 500) — la rimozione di un rischio di policy tende a comprimere la volatilità attesa.

---

## Knowledge Base — research correlate

- [score=7] `Fed_ reaction function, indipendenza e divergenza con la BCE (2023–2026)/...md` — *Fed: reaction function, indipendenza e divergenza con la BCE*
  - Perché è rilevante: è la research dedicata alla *funzione di reazione* della Fed — come traduce dati in decisioni — e contiene la fase di regime `oil_overhang_hawkish_repricing`, cioè esattamente il meccanismo (il petrolio che condiziona il percorso dei tassi) che è al centro della giornata.
- [score=5] `Giappone : Bank of Japan/...(1998–2026).md`
  - Perché è rilevante: il differenziale di tasso Fed-BoJ è il motore del carry trade in yen; un percorso Fed più basso lo comprime (vedi `news_02.md`).
- [score=1] `dati_macro_USA_e_trasmissione_ai_mercati_(2013–2024)/...md`
  - Perché è rilevante: i dati che hanno prodotto la ri-prezzatura (payroll, vendite al dettaglio, Michigan) sono proprio quelli mappati in questa research.

---

## Regime storico identificato

- **Regime**: transizione fra `oil_overhang_hawkish_repricing` (2025-07-01 → 2026-04-30) e `independence_pressure_and_transition` (2026-05-01 → 2026-12-31), dalla research sulla Fed.
- **Caratterizzazione**: siamo in un regime anomalo rispetto agli ultimi due decenni. Non è un ciclo di tagli (la Fed non sta allentando) e non è un ciclo di rialzi (l'ultimo rialzo è stato rinviato). È una **fase di attesa condizionata all'energia**: la banca centrale ha un'inflazione core sotto controllo ma un'inflazione headline esposta al petrolio, e una domanda interna che si sta indebolendo. Il briefing lo descrive perfettamente: "un growth scare, non un allentamento di policy, fa il lavoro di indebolire la valuta". Questa distinzione è cruciale — il dollaro si indebolisce perché l'economia americana rallenta, non perché la Fed sta tagliando. Sono due cause con implicazioni diverse per l'azionario.

---

## Event study

### Episodi storici analoghi selezionati

Pool dalla libreria (Opzione B), sotto-tema canonico `guidance_pivot`, direzione positiva (accomodante = favorevole al rischio), no-look-ahead:

```bash
venv/bin/python analogues.py find --theme monetary_policy --subtheme guidance_pivot \
  --direction pos --before 2026-08-17
# [25 episodi · sotto-tema 'guidance_pivot' su etichette date-locali: 44 episodi]
```

Le 25 date sono in larga maggioranza riunioni del FOMC o discorsi del presidente della Fed in cui il messaggio è stato letto come accomodante o meno restrittivo del previsto. Fra i più riconoscibili: `2018-12-19` (il rialzo con guidance addolcita che precedette il pivot del 2019), `2019-09-18` (taglio "assicurativo"), `2022-12-14` (rallentamento del passo dei rialzi), `2023-09-20` e `2023-10-31` (la svolta di fine 2023), `2024-08-07` e `2024-09-18` (l'avvio del ciclo di tagli), `2025-06-18`, `2025-08-25` (Jackson Hole), `2025-12-10`, e le tre più recenti `2026-04-30`, `2026-05-13`, `2026-06-11` — quest'ultima è la più vicina al regime attuale.

**Nota di scelta del token**: `labels --theme monetary_policy` mostra `rate_decision` con 49 episodi date-locali e `guidance_pivot` con 44. È stato scelto `guidance_pivot` perché la notizia di oggi è una ri-prezzatura di *aspettative* senza alcuna decisione deliberata — il token concettualmente corretto.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker '^GSPC,^NDX,^TNX,IEF,DX-Y.NYB,EURUSD=X,GC=F,^VIX' \
  --events 2014-03-19,2018-03-21,2018-06-13,2018-12-19,2019-09-18,2022-08-26,2022-09-21,2022-12-14,2023-06-15,2023-09-20,2023-10-31,2024-03-19,2024-03-20,2024-05-01,2024-06-12,2024-07-31,2024-08-07,2024-09-18,2024-12-18,2025-06-18,2025-08-25,2025-12-10,2026-04-30,2026-05-13,2026-06-11 \
  --windows 1,3,5,10 \
  --markdown
```

### Risultati

**`^GSPC` — S&P 500** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.05% | -0.38% | -0.10% | +0.95% |
| mediana | **+0.23%** | **-0.12%** | **-0.30%** | **+1.00%** |
| dev std | 1.18% | 2.66% | 2.67% | 3.15% |
| p25 | -0.67% | -1.47% | -1.87% | -1.21% |
| p75 | +0.60% | +1.58% | +1.78% | +1.62% |

**`^NDX` — Nasdaq-100** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.03% | -0.35% | -0.01% | +1.11% |
| mediana | **+0.30%** | **+0.20%** | **-0.24%** | **+0.55%** |
| dev std | 1.56% | 3.30% | 3.69% | 4.33% |
| p25 | -0.96% | -2.09% | -2.60% | -1.29% |
| p75 | +0.94% | +2.05% | +3.25% | +2.37% |

**`^TNX` — rendimento Treasury 10 anni** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.07% | -0.32% | -0.30% | -0.37% |
| mediana | **-0.40%** | **-0.78%** | **-0.95%** | **-0.58%** |
| dev std | 1.84% | 3.62% | 3.32% | 5.50% |

**`IEF` — Treasury 7-10 anni (ETF)** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.00% | +0.13% | +0.16% | +0.24% |
| mediana | **+0.02%** | **+0.23%** | **+0.30%** | **+0.23%** |
| dev std | 0.51% | 1.08% | 0.96% | 1.47% |

**`DX-Y.NYB` — indice del dollaro** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.12% | +0.06% | +0.22% | +0.05% |
| mediana | **+0.13%** | **-0.05%** | **+0.32%** | **+0.42%** |
| dev std | 0.43% | 0.96% | 0.82% | 1.18% |

**`EURUSD=X` — cambio euro/dollaro** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.00% | -0.16% | -0.04% | +0.03% |
| mediana | **+0.02%** | **-0.11%** | **+0.00%** | **+0.10%** |
| dev std | 0.63% | 0.83% | 1.12% | 1.21% |

**`GC=F` — oro** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.10% | +0.04% | +0.30% | +0.81% |
| mediana | **+0.07%** | **-0.92%** | **+0.27%** | **+0.32%** |
| dev std | 1.11% | 2.06% | 2.42% | 3.76% |

**`^VIX` — volatilità implicita S&P 500** (N=25)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.40% | +3.65% | +0.09% | -2.27% |
| mediana | **-2.29%** | **-0.20%** | **-1.26%** | **-1.04%** |
| dev std | 9.99% | 31.62% | 22.92% | 20.74% |

---

## Considerazioni qualitative

**L'azionario: reazione positiva iniziale, digestione, poi recupero.** L'`^GSPC` fa **+0,23% a T+1**, poi scende (**−0,12% a T+3**, **−0,30% a T+5**) e chiude **+1,00% a T+10**. La forma a "V" non è casuale: la prima reazione è il sollievo automatico (meno stretta = valutazioni più alte), i giorni successivi sono la fase in cui il mercato si chiede *perché* la banca centrale sia diventata accomodante, e se la risposta è "perché l'economia rallenta" il sollievo si sgonfia. Poi, nella maggior parte dei casi storici, il tasso di sconto più basso vince. La dispersione resta però significativa (deviazione standard 3,15% a T+10 contro mediana +1,00%) e il p25 è **−1,21%**: in un quarto dei casi a due settimane si era comunque sotto.

**Il Nasdaq: stesso segno, ampiezza maggiore, ma meno persistente.** `^NDX` fa **+0,30% a T+1** e **+0,55% a T+10**, con dispersione 4,33%. È l'asset teoricamente più sensibile — le società growth valgono per gli utili degli anni futuri, che un tasso di sconto più basso rivaluta di più — e infatti il p75 a T+5 è **+3,25%** contro il +1,78% dell'S&P 500. Il Nasdaq-100 è marcato **✅ affidabile** nella scorecard corrente (IC +0,16, hit-rate 53% su 110 previsioni), quindi questa è, insieme al VIX, la lettura direzionale con il supporto migliore della scheda: **modesto bias positivo sull'azionario growth**.

**I tassi e il dollaro: le tabelle ci sono, il segno non è utilizzabile.** `^TNX` mostra mediane negative (−0,95% a T+5, cioè il rendimento scende), `IEF` mediane positive (+0,30% a T+5, cioè il prezzo delle obbligazioni sale) e `DX-Y.NYB` mediane leggermente positive. Tutti e tre — insieme a `GC=F` — sono marcati **❌ controproducente** nella scorecard 2026-W33: IC −0,20 per `^TNX` (N=189), −0,33 per `IEF` (N=59), −0,11 per `DX-Y.NYB` (N=130), −0,09 per `GC=F` (N=270). **Su questi quattro asset il segno storico è sistematicamente rovesciato e non ne traiamo alcuna direzione attesa.** È un limite pesante proprio in questa scheda, perché tassi e dollaro sono il canale *primario* di una notizia di politica monetaria. Vale la pena notare che la coerenza interna dei numeri (rendimento giù, prezzo dei bond su, mediane piccole ma di segno atteso) non basta: la scorecard misura la capacità *out-of-sample* del nostro processo, non la plausibilità economica.

**Perché tassi e dollaro sono così poco prevedibili qui, in una riga.** Perché al momento in cui l'evento diventa pubblico il mercato obbligazionario ha già prezzato l'informazione — è il segmento più efficiente e più veloce. Ciò che si osserva a T+1 e oltre non è la reazione alla notizia ma il rumore successivo, spesso dominato dalla notizia *seguente*. Su questo asset la nostra mediana storica finisce per catturare il rimbalzo anziché il movimento.

**La volatilità: compressione, come da manuale.** `^VIX` ha mediana **−2,29% a T+1** e resta negativa a tutti gli orizzonti. La rimozione di un rischio di policy — il rialzo di settembre non c'è più — riduce meccanicamente il premio che il mercato paga per proteggersi. Il `^VIX` è l'asset più affidabile della scorecard (✅, IC +0,27), quindi questo è il segnale su cui poggiare di più. Attenzione però alla deviazione standard mostruosa a T+3 (**31,6%**): quel numero è gonfiato dagli episodi in cui, pochi giorni dopo un segnale accomodante, è arrivato uno shock indipendente. Ed è esattamente il rischio di oggi.

**La sintesi vera della giornata.** Questa scheda e `news_01.md` non vanno lette separatamente. La ri-prezzatura è avvenuta *sull'ipotesi che l'energia si comporti bene*: inflazione headline benigna, consumatore che regge. Ma la benzina alla pompa è già a 4,08 dollari al gallone (+29% su un anno), la tregua con l'Iran scade oggi e il margine di raffinazione — l'anello fra greggio e prezzo alla pompa — mostra negli analoghi una mediana di **+7,65% a T+10** dopo eventi simili. Se quel canale si attiva, la traiettoria di inflazione che giustificava il rinvio smette di reggere e la parte breve della curva dovrebbe ri-prezzare una seconda volta in tre settimane. Il mercato oggi sta comprando due cose incompatibili: un percorso di tassi più basso e un rischio energetico non risolto. La lezione degli event study qui non è tanto la direzione quanto **la fragilità**: il 63% di probabilità di almeno un rialzo entro fine anno è la misura di quanto poco sia stato davvero cancellato.

---

## Glossario — sigle e termini

- **Fed / Federal Reserve** — la banca centrale degli Stati Uniti.
- **FOMC** (*Federal Open Market Committee*) — il comitato della Fed che decide i tassi di interesse; si riunisce otto volte l'anno.
- **CME FedWatch** — strumento del Chicago Mercantile Exchange che traduce i prezzi dei futures sui Fed funds in probabilità implicite di ciascuna decisione di tasso.
- **Hold** — decisione di lasciare i tassi invariati.
- **Punto base (bp)** — un centesimo di punto percentuale: 2 punti base = 0,02%.
- **NFP / payroll** (*Non-Farm Payrolls*) — il numero di nuovi posti di lavoro creati negli Stati Uniti esclusa l'agricoltura, pubblicato mensilmente; il dato più seguito sul mercato del lavoro americano.
- **Vendite al dettaglio** (*retail sales*) — spesa dei consumatori nei negozi, pubblicata dal Census Bureau; termometro della domanda interna.
- **Indice di fiducia dei consumatori dell'Università del Michigan** — indagine mensile sulle aspettative delle famiglie americane.
- **Guidance / forward guidance** — la comunicazione con cui una banca centrale indica al mercato il percorso futuro dei tassi.
- **Growth (azioni growth)** — società i cui utili attesi sono concentrati lontano nel futuro (tipicamente tecnologia); sono le più sensibili al tasso di sconto.
- **Tasso di sconto** — il tasso a cui si attualizzano gli utili futuri per calcolare quanto valgono oggi. Più basso il tasso, più alto il valore attuale.
- **Duration** — la sensibilità del prezzo di un'obbligazione a una variazione dei tassi; più è alta, più il prezzo si muove.
- **^TNX** — rendimento del titolo di Stato USA a 10 anni. **IEF** — ETF su Treasury a 7-10 anni (il *prezzo*, che si muove in direzione opposta al rendimento).
- **DX-Y.NYB** — indice del dollaro (*Dollar Index*), il dollaro contro un paniere di sei valute.
- **EURUSD=X** — cambio euro/dollaro: quanti dollari per un euro.
- **^GSPC / ^NDX / ^VIX / GC=F** — S&P 500 / Nasdaq-100 / indice di volatilità implicita / futures sull'oro.
- **IC (Information Coefficient)** — correlazione fra direzione prevista e realizzata; negativo = previsione sistematicamente rovesciata.

---

## Caveat

- **Quattro degli otto asset in tabella hanno segno storico inaffidabile.** `^TNX`, `IEF`, `DX-Y.NYB` e `GC=F` sono tutti marcati ❌ controproducente nella scorecard 2026-W33. Su questi **non viene tratta alcuna direzione attesa**, pur riportando i numeri. È un limite particolarmente rilevante qui, perché tassi e dollaro sono il canale primario di una notizia di politica monetaria; la lettura direzionale della scheda poggia quindi su `^NDX`, `^GSPC` e `^VIX`.
- **Il pool mescola tre regimi di tasso**: ciclo di rialzi 2018, tagli assicurativi 2019, stretta 2022-2023, avvio dei tagli 2024, e il regime corrente di *oil overhang*. Il significato di "accomodante" non è lo stesso in una fase in cui i tassi sono a zero e in una in cui sono al 4,7%.
- **Nessuna decisione è stata presa.** La notizia è una ri-prezzatura di aspettative, mentre gran parte del pool è composta da riunioni FOMC effettive. Un evento programmato con un annuncio produce una reazione più concentrata di una deriva di probabilità su più sedute; la reazione a T+1 del pool sovrastima quindi ciò che ci si può attendere oggi.
- **Ri-prezzatura già avvenuta.** Il biennale ha già toccato il minimo di sette settimane e il dollaro si è già indebolito: buona parte del movimento è nei prezzi. Gli event study misurano la reazione a sorprese, e qui la sorpresa è passata.
- **Rischio di condizionamento esogeno.** La deviazione standard del `^VIX` a T+3 (31,6%) segnala che negli analoghi è frequente che uno shock indipendente arrivi entro pochi giorni. Con la scadenza della tregua Iran nella stessa giornata, la probabilità che ciò accada oggi è alta.
- Correlazione ≠ causazione.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-16T19:11:12
- Scorecard consultata: `daily_analysis/_scorecard/2026-W33.md`, sezione 5-bis
