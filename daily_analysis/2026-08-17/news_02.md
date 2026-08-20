# PIL giapponese Q2 a +0,3% t/t contro +0,5% atteso: sorpresa negativa con composizione peggiore del titolo

**Data analisi**: 2026-08-17
**Fonte**: Morning Briefing 2026-08-17 (fin 01)
**Slug**: japan-q2-gdp-miss

---

## Testo notizia (originale)

> La stima preliminare del Cabinet Office giapponese per aprile-giugno 2026 mostra un PIL reale a +0,3% trimestre su trimestre contro un consenso di +0,5%, e +1,1% annualizzato contro circa +2,0% atteso. La composizione e' peggiore del dato principale: investimenti delle imprese -1,2% t/t e consumi privati piatti dove era atteso +0,5%. Le esportazioni salgono +0,5% mentre le importazioni calano -1,5%, quindi il commercio netto abbellisce il numero e il calo dell'import riflette le forniture di greggio interrotte dalla chiusura di fatto dello Stretto di Hormuz, non un miglioramento della domanda giapponese. Uno scivolone guidato dai consumi toglie la giustificazione domestica a un rialzo dei tassi della Bank of Japan; lo yen e' a 159,15 per dollaro.

---

## In breve (in parole semplici)

L'economia giapponese è cresciuta nel secondo trimestre 2026 meno di quanto ci si aspettasse: +0,3% invece di +0,5% rispetto al trimestre precedente. Ma il punto non è il decimale mancato — è *da dove* viene la crescita. Le famiglie non hanno consumato di più (zero, contro un +0,5% atteso) e le imprese hanno tagliato gli investimenti dell'1,2%. Il numero è stato salvato solo dal fatto che le importazioni sono crollate — e sono crollate perché il petrolio non arriva, dato che lo Stretto di Hormuz è chiuso.

Perché conta: nella contabilità nazionale il PIL si calcola come consumi + investimenti + spesa pubblica + (esportazioni − importazioni). Se le importazioni scendono, quella sottrazione si riduce e il PIL *sale* per pura aritmetica, anche quando la ragione è che il Paese non riesce a comprare l'energia che gli serve. È il caso da manuale di un dato che sembra meno brutto di quanto sia.

La domanda che ci poniamo: quando in passato è arrivata una sorpresa negativa sui dati di attività economica, come si sono mossi lo yen, l'indice azionario giapponese e i tassi americani nei giorni successivi?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | macro_data |
| `sub_themes` | activity_growth, boj, jpy |
| `sentiment` | bearish |
| `confidence` | medium |
| `horizon` | intraday-3 giorni |

**Motivazione classificazione**: è la pubblicazione di un dato macroeconomico con un consenso pubblicato e una sorpresa misurabile — il caso puro di `macro_data`. Il sentiment è `bearish` perché la sorpresa è al ribasso *e* la composizione (consumi piatti, investimenti in calo) peggiora ulteriormente la lettura. La `confidence` è **medium**: il canale sulla Bank of Japan è chiaro ma parzialmente neutralizzato dal fatto che, come nota il briefing, il Nikkei è salito nonostante il dato — cioè il mercato sta prezzando il *percorso dei tassi* più della crescita, il che rovescia il segno atteso sull'azionario.

---

## Asset rilevanti

### Primary (canale diretto)
- **JPY=X** (cambio dollaro/yen — quante unità di yen serve per un dollaro; se il numero *sale*, lo yen si indebolisce) — è l'asset più direttamente esposto: un PIL debole toglie la giustificazione domestica a un rialzo dei tassi della Bank of Japan, e un differenziale di tasso più ampio con gli Stati Uniti indebolisce lo yen.
- **^N225** (indice azionario Nikkei 225, le 225 principali società quotate a Tokyo) — l'equity domestico è il secondo canale, con il segno però ambiguo (vedi sotto).

### Secondary (effetti indiretti)
- **^TNX** (rendimento del titolo di Stato americano a 10 anni, il *Treasury* decennale) — la Bank of Japan e il carry trade in yen sono uno dei maggiori canali di domanda per i Treasury: se la BoJ non alza i tassi, il carry trade resta finanziabile e la domanda di titoli esteri regge.
- **^GSPC** (indice azionario S&P 500) e **^VIX** (indice di volatilità implicita sull'S&P 500) — via *carry trade*: quando lo yen si rafforza bruscamente le posizioni finanziate in yen vengono chiuse in fretta, e questo si scarica sull'azionario globale (è quello che accadde il 5 agosto 2024).

---

## Knowledge Base — research correlate

- [score=6] `dati_macro_USA_e_trasmissione_ai_mercati_(2013–2024)/dati macro USA e trasmissione ai mercati (2013–2024).md` — *Sorprese sui dati macro e trasmissione ai mercati: regimi, canali e state-dependence*
  - Perché è rilevante: fornisce la meccanica generale di come una sorpresa macro si trasmette ai prezzi e, soprattutto, il concetto di *state-dependence* — la stessa sorpresa ha effetti opposti a seconda del regime in cui arriva.
- [score=2] `Giappone : Bank of Japan/...carry trade, uscita YCC e interventi FX — regime ed episodi storici (1998–2026).md`
  - Perché è rilevante: è la research specifica sul Giappone, con la mappa dei regimi BoJ (uscita dal controllo della curva, interventi sul cambio) e gli episodi di *carry unwind* — il rischio di coda di questa notizia.

---

## Regime storico identificato

- **Regime**: `post_ycc_2024_2026` (2024-04-01 → oggi), dalla research Bank of Japan.
- **Caratterizzazione**: la BoJ ha abbandonato il controllo della curva dei rendimenti (*Yield Curve Control*, la politica con cui comprava titoli per tenere fermo il rendimento decennale) nel marzo 2024 ed è entrata in una fase di normalizzazione lenta. In questo regime lo yen non è più ancorato dalla politica monetaria ma dipende dal differenziale di tasso con gli Stati Uniti e — quando questo si allarga troppo — dall'intervento diretto del Ministero delle Finanze sul mercato dei cambi. Il briefing segnala esattamente questo: con lo yen a 159,15 e senza giustificazione domestica per un rialzo, la difesa del cambio poggia sull'intervento coordinato di inizio agosto e non sui fondamentali. È un equilibrio fragile.

---

## Event study

### Episodi storici analoghi selezionati

Pool dalla libreria (Opzione B), filtro forte su etichette date-locali, direzione negativa, no-look-ahead:

```bash
venv/bin/python analogues.py find --theme macro_data --subtheme activity_growth \
  --direction neg --before 2026-08-17
# [28 episodi · sotto-tema 'activity_growth' su etichette date-locali: 29 episodi]
```

Il pool è composto da pubblicazioni di dati di attività (PIL, produzione industriale, indagini PMI, vendite al dettaglio) risultate *sotto* le attese. Include episodi con forte componente giapponese/BoJ — `2024-07-11`, `2024-08-01` (la vigilia del *carry unwind* del 5 agosto 2024), `2026-06-05`, `2026-07-24` — e sorprese negative su area euro e Stati Uniti, che entrano perché il canale di trasmissione (dato debole → aspettative di tassi più basse → cambio e azionario) è lo stesso.

### Comando eseguito

```bash
venv/bin/python event_study.py \
  --ticker 'JPY=X,^N225,^TNX,^GSPC,^VIX' \
  --events 2015-09-03,2015-12-01,2018-02-02,2019-08-01,2019-09-04,2019-10-01,2022-02-04,2022-08-03,2022-10-13,2022-11-01,2022-12-01,2023-02-03,2023-06-01,2023-07-12,2023-08-01,2023-08-03,2023-12-08,2024-02-02,2024-04-01,2024-06-07,2024-07-11,2024-08-01,2024-10-01,2024-12-06,2025-03-03,2025-09-30,2026-06-05,2026-07-24 \
  --windows 1,3,5,10 \
  --markdown
```

### Risultati

**`JPY=X` — cambio USD/JPY** (N=28) — *un valore positivo = yen più debole*

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.10% | -0.08% | -0.02% | +0.06% |
| mediana | **-0.12%** | **+0.07%** | **+0.10%** | **+0.16%** |
| dev std | 0.91% | 1.27% | 1.64% | 2.66% |
| p25 | -0.46% | -0.97% | -0.95% | -1.56% |
| p75 | +0.44% | +0.91% | +1.22% | +2.09% |

**`^N225` — Nikkei 225** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.58% | -0.91% | -0.54% | +0.51% |
| mediana | **-0.21%** | **-0.09%** | **+0.21%** | **+0.64%** |
| dev std | 1.97% | 3.19% | 3.35% | 4.50% |
| p25 | -2.12% | -2.94% | -2.08% | -1.56% |
| p75 | +0.67% | +0.97% | +1.13% | +3.28% |

**`^TNX` — rendimento Treasury USA 10 anni** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.04% | +0.21% | +1.00% | +1.69% |
| mediana | **+0.04%** | **+0.04%** | **+0.74%** | **+1.15%** |
| dev std | 2.38% | 3.98% | 5.40% | 7.20% |

**`^GSPC` — S&P 500** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.59% | -0.38% | -0.38% | +0.06% |
| mediana | **-0.45%** | **-0.23%** | **-0.58%** | **+0.65%** |
| dev std | 1.22% | 1.71% | 1.88% | 2.91% |

**`^VIX` — volatilità implicita S&P 500** (N=28)

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +6.67% | +4.80% | +6.03% | +5.83% |
| mediana | **+0.50%** | **+0.70%** | **+4.75%** | **+6.34%** |
| dev std | 22.65% | 16.67% | 17.58% | 20.88% |

---

## Considerazioni qualitative

**Lo yen: nessun segnale.** Le mediane su `JPY=X` sono comprese fra −0,12% e +0,16% a fronte di una dispersione di 0,9–2,7%. In pratica: nei 28 episodi analoghi la sorpresa negativa sui dati di attività non ha prodotto una direzione riconoscibile sul cambio. Il motivo è che il segno dipende da *quale* economia delude. Se delude il Giappone, lo yen si indebolisce (meno probabilità di rialzo BoJ). Se deludono gli Stati Uniti, lo yen si rafforza (meno probabilità di rialzo Fed, differenziale che si comprime). Il pool le mescola entrambe, e i due effetti si annullano. La scorecard corrente classifica `JPY=X` come ⚠️ debole (IC +0,01, hit-rate 54% su 84 previsioni) — coerente con quello che si vede qui. **Nessuna direzione attesa sul cambio.**

**Il Nikkei: negativo nei primissimi giorni, poi recupera.** Mediana **−0,21% a T+1** e **−0,09% a T+3**, che diventa **+0,21% a T+5** e **+0,64% a T+10**. La forma è quella di una reazione istintiva negativa che si riassorbe. È esattamente ciò che il briefing osserva oggi in tempo reale: il Nikkei è salito dello 0,4% *nonostante* il dato. Il meccanismo è il seguente — se la crescita delude, la Bank of Japan non alza i tassi; se i tassi restano bassi, i profitti futuri delle imprese valgono di più una volta scontati (perché il tasso a cui li si sconta è più basso) e lo yen debole gonfia gli utili degli esportatori giapponesi convertiti in yen. La borsa sta comprando il percorso dei tassi, non la crescita. Attenzione però: la dispersione è alta (deviazione standard 4,5% a T+10 contro mediana +0,64%) e il quarto peggiore dei casi vedeva il Nikkei a −1,56% — la scorecard marca `^N225` ⚠️ debole (IC +0,02 su 72 previsioni). Segnale indicativo, non affidabile.

**I tassi americani: qui il segno non va usato.** La tabella su `^TNX` mostra mediane positive crescenti (+1,15% a T+10, cioè il *rendimento* sale). Ma `^TNX` è marcato **❌ controproducente** nella scorecard 2026-W33: IC **−0,20** su 189 previsioni mature, hit-rate 46%. Un IC così negativo con N grande significa che la mediana degli analoghi punta nella direzione sbagliata più spesso che no. **Riportiamo il numero ma dichiariamo esplicitamente che il segno storico su ^TNX è inaffidabile e non ne traiamo previsione.**

**La volatilità: l'unico segnale con supporto solido.** Il `^VIX` è l'asset più affidabile della scorecard (✅, IC +0,27, hit-rate 63%) e qui ha mediana **+4,75% a T+5** e **+6,34% a T+10**. Tradotto: dopo una sorpresa negativa sui dati di attività, la volatilità attesa sull'azionario americano tende a salire nell'arco di una-due settimane, anche quando i prezzi non crollano subito. Ha senso: un dato debole non produce una vendita immediata ma allarga il ventaglio degli esiti possibili — il mercato non sa più se sta guardando un rallentamento gestibile o l'inizio di una contrazione, e paga di più per proteggersi. Va detto che la media (+5,83%) e la mediana (+6,34%) qui sono vicine ma la deviazione standard è enorme (20,9%): la direzione è ragionevole, l'ampiezza no.

**Il rischio di coda che vale la pena nominare.** Due delle date del pool — `2024-07-11` e `2024-08-01` — sono la vigilia del *carry unwind* del 5 agosto 2024, quando il rafforzamento improvviso dello yen costrinse a chiudere in massa posizioni finanziate a debito in yen e il Nikkei perse oltre il 12% in una seduta. In quegli episodi il Nikkei fa −10,79% e −0,17% a T+10 e il VIX +42,88% e −18,07%. È il promemoria che questo canale non è simmetrico: la coda negativa dello yen (rafforzamento improvviso) è molto più violenta della coda positiva. Oggi lo yen è a 159,15 con la difesa affidata all'intervento coordinato di inizio agosto piuttosto che ai fondamentali — cioè esattamente la configurazione in cui un movimento disordinato è possibile.

**Il collegamento con il resto della sessione.** Il calo delle importazioni giapponesi non è un miglioramento: è petrolio che non arriva perché Hormuz è chiuso (vedi `news_01.md`). Il Giappone è il maggiore importatore netto di energia fra le economie avanzate, quindi la scheda sull'Iran e questa sono lo stesso shock visto da due lati. Se l'energia rincara ancora, il PIL del terzo trimestre peggiora per la via delle ragioni di scambio — e la BoJ resta bloccata fra un'inflazione importata che vorrebbe combattere e una domanda interna che non regge un rialzo.

---

## Glossario — sigle e termini

- **PIL / GDP** (*Gross Domestic Product*) — il valore di tutti i beni e servizi finali prodotti in un Paese in un periodo. "t/t" = variazione rispetto al trimestre precedente; "annualizzato" = quel tasso trimestrale proiettato su dodici mesi.
- **Cabinet Office** — l'ufficio del governo giapponese che pubblica i conti nazionali; la "stima preliminare" è la prima lettura, soggetta a revisione.
- **BoJ** (*Bank of Japan*) — la banca centrale giapponese.
- **YCC** (*Yield Curve Control*, controllo della curva dei rendimenti) — politica con cui la BoJ, dal 2016 al 2024, comprava titoli di Stato per tenere il rendimento decennale entro una banda prefissata.
- **Carry trade** — strategia in cui ci si indebita in una valuta a tasso basso (storicamente lo yen) per investire in attività a rendimento più alto. Funziona finché la valuta di finanziamento resta debole; quando si rafforza bruscamente, le posizioni vanno chiuse tutte insieme (*carry unwind*).
- **JPY=X** — cambio USD/JPY: quanti yen per un dollaro. Numero che **sale** = yen che si **indebolisce**.
- **^N225** — indice azionario Nikkei 225 (Tokyo).
- **^TNX** — rendimento del titolo di Stato USA a 10 anni.
- **^GSPC** — indice azionario S&P 500.
- **^VIX** — indice di volatilità implicita a 30 giorni sull'S&P 500.
- **Consenso** — la mediana delle previsioni degli economisti prima della pubblicazione; la "sorpresa" è la differenza fra dato e consenso, ed è ciò che muove i prezzi (il livello atteso è già nei prezzi).
- **State-dependence** — il fatto che la stessa notizia produca effetti diversi a seconda del regime macro in cui arriva.
- **Ragioni di scambio** (*terms of trade*) — il rapporto fra i prezzi di ciò che un Paese esporta e di ciò che importa; peggiorano quando l'energia importata rincara.

---

## Caveat

- **Il pool mescola geografie.** Le 28 date includono sorprese negative su dati di Stati Uniti, area euro e Giappone. Il canale è formalmente lo stesso ma il *segno* sul cambio yen dipende da chi delude — ed è la ragione più probabile per cui `JPY=X` non mostra alcun segnale. Un pool ristretto ai soli dati giapponesi sarebbe più pulito ma avrebbe N troppo piccolo.
- **`^TNX`: segno storico inaffidabile** — asset marcato ❌ controproducente nella scorecard 2026-W33 (IC −0,20, N=189). Nessuna direzione attesa viene tratta sui tassi americani.
- **`JPY=X` e `^N225` sono ⚠️ deboli in scorecard** (IC +0,01 e +0,02): le mediane vanno lette come indicazioni, non come previsioni.
- **Effetto già in parte realizzato.** Il dato è stato pubblicato prima dell'apertura europea e il Nikkei ha già reagito (+0,4%). L'event study misura la reazione *da* T+0: parte del movimento a un giorno è già avvenuto mentre scriviamo.
- **Rischio di coda asimmetrico non catturato dalla mediana.** Gli episodi di *carry unwind* sono rari ma estremi: la mediana li nasconde per costruzione. La deviazione standard e il p25 sono, in questo caso, più informativi della tendenza centrale.
- Correlazione ≠ causazione; gli episodi appartengono a regimi di tasso molto diversi (2015-2019 a tassi zero, 2022-2024 in stretta, 2026 con l'overhang energetico).

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Catalog timestamp: 2026-08-16T19:11:12
- Scorecard consultata: `daily_analysis/_scorecard/2026-W33.md`, sezione 5-bis
