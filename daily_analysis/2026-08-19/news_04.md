# Housing starts USA in calo del 12,4% a 1,239 milioni contro 1,350 attesi: la prima serie di attivita' reale a registrare il repricing dei tassi lunghi

**Data analisi**: 2026-08-19
**Fonte**: Morning Briefing 2026-08-19 (fin 04)
**Slug**: us-housing-starts-july

---

## Testo notizia (originale)

> Il Census Bureau ha riportato nuovi cantieri residenziali privati a un tasso annualizzato destagionalizzato di 1,239 milioni a luglio, in calo del 12,4% sul mese e ampiamente sotto il consenso Reuters di 1,35 milioni. I cantieri unifamiliari, che assorbono la maggior parte dell'occupazione edilizia e della domanda di materiali, sono scesi del 9,9% a 808.000 unita'. Le cause prossime sono i tassi sui mutui piu' alti, conseguenza diretta del repricing della parte lunga della curva, e un accumulo di case nuove invendute. E' il canale di trasmissione dal mercato obbligazionario all'economia reale che opera in tempo reale, ed e' la prima serie di attivita' 'hard' a mostrarlo con chiarezza: un calo del 12,4% dei cantieri accanto a un trentennale ai massimi da 19 anni e' la combinazione stagflazionaria che lascia la banca centrale senza uno strumento pulito.

---

## In breve (in parole semplici)

Negli Stati Uniti a luglio sono partiti molti meno cantieri residenziali del previsto: 1,239 milioni in ritmo annualizzato contro 1,35 milioni attesi, cioè un calo del 12,4% in un solo mese. La componente più importante — le case unifamiliari, quelle che generano occupazione edilizia e domanda di materiali — è scesa del 9,9%.

Perché conta: il mutuo trentennale americano è agganciato al rendimento del titolo di Stato a lungo termine. Quando quel rendimento sale (ed è al massimo da 19 anni, vedi [news_03](news_03.md)), comprare casa a rate diventa più caro e i costruttori smettono di costruire. **Questa è la prima serie di dati "duri" — non di sondaggio — che mostra il mercato obbligazionario che frena l'economia reale.**

Ci chiediamo: come hanno reagito storicamente gli asset a una sorpresa negativa ampia sui dati di attività USA?

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | macro_data |
| `sub_themes` | activity_growth, housing |
| `sentiment` | bearish |
| `confidence` | medium |
| `horizon` | intraday-1 giorno (con coda a 5-10 giorni sul canale tassi) |

**Motivazione classificazione**: `macro_data` perché è una release statistica ufficiale (US Census Bureau) con un consenso di mercato pubblicato, quindi con una **sorpresa** misurabile: 1,239 contro 1,350 milioni attesi, uno scarto di circa l'8% sul consenso. Il sotto-tema canonico è `activity_growth`, che nella libreria ha 30 episodi con etichetta date-locale (filtro forte). Sentiment `bearish`: la sorpresa è al ribasso e su una componente ciclica sensibile. Confidence `medium`: il dato è netto, ma i dati sull'edilizia residenziale sono notoriamente volatili mese su mese e soggetti a revisioni ampie, il che riduce il contenuto informativo del singolo mese.

---

## Asset rilevanti

### Primary (canale diretto)
- **^TNX** (rendimento del Treasury USA a 10 anni) — canale diretto: dati di attività deboli riducono le aspettative di crescita e quindi il tasso richiesto. È anche il tasso su cui è ancorato il mutuo trentennale, quindi il *responsabile* del dato oltre che il suo destinatario.
- **^GSPC** (indice azionario S&P 500) — l'azionario USA reagisce direttamente alle release americane.
- **EURUSD=X** (cambio euro/dollaro) — driver primario del cambio sui dati macro.

### Secondary (effetti indiretti)
- **IEF** (ETF iShares Treasury USA 7-10 anni) — proxy di **prezzo** della duration: sale quando ^TNX scende. ⚠ Segno opposto a ^TNX per costruzione.
- **^NDX** (indice Nasdaq-100) — molto reattivo ai dati che spostano le aspettative sui tassi.
- **DX-Y.NYB** (indice del dollaro) — reagisce direttamente alle sorprese macro USA.
- **HG=F** (futures sul rame) — il rame è il termometro della domanda industriale globale, e l'edilizia ne è un utilizzatore di primo piano (impianti elettrici e idraulici).
- **^VIX** (indice della volatilità implicita sull'S&P 500) — misura se la sorpresa negativa alza la domanda di protezione.

---

## Knowledge Base — research correlate

- [score=11] `dati_macro_USA_e_trasmissione_ai_mercati_(2013–2024)/…md` — *Sorprese sui dati macro USA e trasmissione ai mercati: regimi, canali e state-dependence*
  - Perché è rilevante: è la research specificamente dedicata a **come** una sorpresa macro si trasmette agli asset, e soprattutto al fatto che il segno della trasmissione **dipende dallo stato** (state-dependence): in un regime dominato dall'inflazione, un dato debole è una buona notizia per l'azionario (meno pressione sui tassi); in un regime dominato dalla crescita, è una cattiva notizia. Sapere in quale dei due siamo è la domanda centrale di questa scheda.
- [score=8] `ciclo_inflazione_eurozona_2021-2023/Ciclo inflazione Eurozona 2021–2023.md`
  - Perché è rilevante: documenta la fase in cui uno shock di offerta rende il trade-off della banca centrale non risolvibile — che è esattamente la situazione descritta dal briefing come "combinazione stagflazionaria".
- [score=6] `Fed_ reaction function, indipendenza e divergenza con la BCE (2023–2026)/…md`
  - Perché è rilevante: le minute del FOMC di luglio escono oggi pomeriggio e questo dato "sta direttamente sotto" di esse, come nota il briefing.

---

## Regime storico identificato

- **Regime**: stagflazione incipiente — attività reale in decelerazione **e** inflazione sostenuta da uno shock energetico esogeno.
- **Caratterizzazione**: il briefing formula il problema con precisione: *"un calo del 12,4% dei cantieri accanto a un trentennale ai massimi da 19 anni è la combinazione stagflazionaria che lascia la banca centrale senza uno strumento pulito"*. Il meccanismo è questo: normalmente, se l'attività rallenta, la banca centrale può tagliare i tassi e ridare ossigeno. Ma qui la causa dei tassi alti non è la politica monetaria — il target sui Fed funds è fermo al 3,50-3,75% e il mercato non sconta rialzi — bensì il **premio a termine** guidato da deficit e inflazione energetica ([news_03](news_03.md)). Un taglio del tasso di policy non abbasserebbe necessariamente il mutuo trentennale; potrebbe anzi peggiorare le aspettative di inflazione e far salire ancora la parte lunga.
- Elemento che qualifica il regime: la conferma incrociata dai risultati di Home Depot (notizia fin 05 del briefing, scartata dal triage perché single-name non in database). Le vendite comparabili crescono dell'1,7%, il dato migliore da fine 2022, ma la lettura è **scomoda, non rassicurante**: la domanda di ristrutturazione tiene *proprio perché* il mercato del nuovo è congelato e le famiglie ristrutturano invece di traslocare. Due dati che sembrano contraddirsi raccontano in realtà la stessa cosa.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla libreria (Opzione B) con:
`--theme macro_data --subtheme activity_growth --direction neg --before 2026-08-19`
→ 29 episodi con etichetta **date-locale** (filtro forte). Nessuna potatura dell'analista. L'episodio `2026-08-18` non ha dati realizzati: **N effettivo = 28**.

⚠ **Il filtro di direzione non discrimina — da dichiarare.** Lanciando lo stesso comando con `--direction pos` la libreria restituisce **28 episodi su 29 identici**. Significa che gli episodi di `activity_growth` sono etichettati in modo direzionalmente ambiguo, e che il pool descrive **"giornate di release di dati di attività"** in generale, non "sorprese al ribasso". Le mediane vanno lette come *il comportamento tipico degli asset attorno a un dato di attività*, con il segno che deriva dal fatto che la maggioranza di questi episodi cade in fasi di decelerazione, non da un filtro esplicito. È il limite metodologico principale della scheda.

Il pool è inoltre **dominato da release statunitensi di indagine congiunturale** (ISM manifatturiero e dei servizi, PMI), non da dati sull'edilizia: è un proxy del canale "sorpresa di crescita", non dello specifico canale immobiliare.

**Episodi utilizzati** (raggruppati per meccanismo, dato che sono 28):

- **Rallentamento manifatturiero globale 2015-2016** — `2015-09-03`, `2015-12-01`: **contrazione dell'ISM manifatturiero in un contesto di dollaro forte e petrolio in caduta → il dato debole veniva letto come rinvio del rialzo Fed, quindi in parte "buona notizia" per l'azionario**.
- **Shock inflazione salariale 2018** — `2018-02-02`: **il dato sull'occupazione con salari in accelerazione fa salire i rendimenti → è il caso in cui un dato *forte* è cattiva notizia, il rovescio esatto del meccanismo di oggi**.
- **Ciclo di tagli assicurativi 2019** — `2019-08-01`, `2019-09-04`, `2019-10-01`: **ISM in contrazione durante la guerra commerciale → dati deboli che validavano i tagli preventivi della Fed**.
- **Picco e rientro dell'inflazione 2022-2023** — `2022-02-04`, `2022-08-03`, `2022-10-13`, `2022-11-01`, `2022-12-01`, `2023-02-03`, `2023-06-01`, `2023-07-12`, `2023-08-01`, `2023-08-03`, `2023-12-08`: **regime in cui l'attività debole era accolta con sollievo perché riduceva la pressione sulla Fed → "bad news is good news"**.
- **Fase di atterraggio morbido 2024** — `2024-02-02`, `2024-04-01`, `2024-06-07`, `2024-07-11`, `2024-08-01`, `2024-10-01`, `2024-12-06`: **il segno si inverte progressivamente — con l'inflazione rientrata, i dati deboli tornano a essere cattive notizie per gli utili attesi**.
- **Regime corrente 2025-2026** — `2025-03-03`, `2025-09-30`, `2026-06-05`, `2026-07-24`: **decelerazione dell'attività con inflazione ancora sopra obiettivo → il regime strutturalmente più vicino a oggi**.
- *(nel pool, senza dati realizzati)* `2026-08-18` — episodio di ieri.

### Comando eseguito

```bash
venv/bin/python analogues.py find --theme macro_data --subtheme activity_growth \
  --direction neg --before 2026-08-19

venv/bin/python event_study.py \
  --ticker '^TNX,IEF,^GSPC,^NDX,DX-Y.NYB,EURUSD=X,HG=F,^VIX' \
  --events 2015-09-03,2015-12-01,2018-02-02,2019-08-01,2019-09-04,2019-10-01,2022-02-04,2022-08-03,2022-10-13,2022-11-01,2022-12-01,2023-02-03,2023-06-01,2023-07-12,2023-08-01,2023-08-03,2023-12-08,2024-02-02,2024-04-01,2024-06-07,2024-07-11,2024-08-01,2024-10-01,2024-12-06,2025-03-03,2025-09-30,2026-06-05,2026-07-24,2026-08-18 \
  --windows 1,3,5,10 --markdown
```

### Risultati

Rendimenti cumulati a T+1, T+3, T+5, T+10 **giorni di borsa** dopo l'episodio. Per ^TNX si tratta della variazione del **rendimento**; per IEF, del **prezzo** (segno opposto per costruzione). ^VIX è un indice di volatilità: sale quando cresce la domanda di protezione.

### Event study — `^TNX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.04% | +0.21% | +1.00% | +1.69% |
| mediana | +0.04% | +0.04% | +0.74% | +1.15% |
| dev std | +2.38% | +3.98% | +5.40% | +7.20% |
| p25 | -1.90% | -1.33% | -1.08% | -1.38% |
| p75 | +1.08% | +2.53% | +3.16% | +5.58% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `IEF`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.02% | -0.04% | -0.17% | -0.24% |
| mediana | -0.05% | -0.01% | -0.06% | -0.20% |
| dev std | +0.59% | +0.84% | +1.13% | +1.49% |
| p25 | -0.29% | -0.75% | -0.69% | -1.24% |
| p75 | +0.32% | +0.38% | +0.43% | +0.56% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.59% | -0.38% | -0.38% | +0.06% |
| mediana | -0.45% | -0.23% | -0.58% | +0.65% |
| dev std | +1.22% | +1.71% | +1.88% | +2.91% |
| p25 | -1.26% | -1.86% | -1.63% | -2.94% |
| p75 | +0.27% | +1.19% | +1.12% | +2.17% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `^NDX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.58% | -0.46% | -0.35% | +0.10% |
| mediana | -0.45% | +0.21% | -0.17% | +0.75% |
| dev std | +1.48% | +2.20% | +2.43% | +3.65% |
| p25 | -1.23% | -2.36% | -2.23% | -3.05% |
| p75 | +0.45% | +0.95% | +1.72% | +2.66% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `DX-Y.NYB`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.06% | -0.22% | -0.26% | -0.33% |
| mediana | -0.07% | -0.18% | -0.12% | -0.01% |
| dev std | +0.48% | +0.81% | +1.01% | +1.51% |
| p25 | -0.27% | -0.57% | -1.18% | -1.44% |
| p75 | +0.26% | +0.04% | +0.50% | +0.80% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `EURUSD=X`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.00% | +0.29% | +0.44% | +0.56% |
| mediana | +0.05% | +0.15% | +0.46% | +0.24% |
| dev std | +0.58% | +1.27% | +1.34% | +1.97% |
| p25 | -0.38% | -0.47% | -0.18% | -0.83% |
| p75 | +0.38% | +0.69% | +1.04% | +1.67% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `HG=F`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.02% | +0.53% | +0.27% | +1.01% |
| mediana | +0.16% | +0.01% | +0.47% | +1.05% |
| dev std | +1.45% | +2.62% | +3.13% | +4.20% |
| p25 | -0.86% | -1.27% | -2.32% | -0.90% |
| p75 | +0.94% | +2.00% | +1.91% | +3.66% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `^VIX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +6.67% | +4.80% | +6.03% | +5.83% |
| mediana | +0.50% | +0.70% | +4.75% | +6.34% |
| dev std | +22.65% | +16.67% | +17.58% | +20.88% |
| p25 | -1.63% | -4.60% | -6.26% | -10.72% |
| p75 | +7.67% | +7.61% | +12.96% | +18.25% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica, cosa dicono questi numeri.**

- **^GSPC (S&P 500)**: mediana **−0,45% a T+1**, −0,23% a T+3, −0,58% a T+5, poi **+0,65% a T+10**. In parole povere: nei 28 episodi simili, il giorno dopo una release di attività l'indice era in calo in oltre metà dei casi, ma il calo si riassorbiva entro due settimane. La dispersione è moderata (deviazione standard 1,2% a T+1, 2,9% a T+10). ⚠️ Scorecard 2026-W34: ^GSPC è "debole" (IC +0,10 su N=406) — direzione plausibile ma non forte.
- **^NDX (Nasdaq-100)**: profilo praticamente identico (−0,45% a T+1, +0,75% a T+10) ma con dispersione maggiore. ✅ È l'asset più affidabile della tabella (IC +0,17 su N=126, "affidabile"): la lettura direzionale poggia soprattutto qui.
- **^VIX (volatilità)**: mediana **positiva e crescente** con l'orizzonte: +0,50% a T+1, +0,70% a T+3, **+4,75% a T+5, +6,34% a T+10**. ✅ Anche ^VIX è "affidabile" (IC +0,17, hit-rate 63%). Questo è il risultato più interessante della scheda: **il mercato non reagisce subito, ma il premio per il rischio si costruisce nelle due settimane successive**. La dispersione però è enorme (deviazione standard 17-23%), quindi il segnale è di direzione, non di ampiezza.
- **^TNX (rendimento 10 anni)**: mediana quasi nulla a T+1 e T+3, poi **+0,74% a T+5 e +1,15% a T+10** — cioè i rendimenti *salgono* dopo un dato di attività debole. Controintuitivo, ed è esattamente il tipo di risultato che la scorecard ci dice di non usare. ❌ **^TNX è "controproducente": IC −0,20 su N=208, hit-rate 45%. Non traiamo alcuna direzione attesa sul decennale USA.** Riportiamo la tabella e ci fermiamo lì.
- **IEF (prezzo Treasury 7-10 anni)**: mediane leggermente negative (−0,05% a T+1, −0,20% a T+10), coerenti con ^TNX in salita — di nuovo, **segni opposti = accordo**, per la convenzione mista rendimento/prezzo. ❌ Anche IEF è "controproducente" (IC −0,29 su N=66, il peggiore dell'elenco): nessuna direzione attesa.
- **DX-Y.NYB (dollaro)**: mediane negative ma minuscole (−0,07% a T+1, −0,01% a T+10). ❌ "Controproducente" (IC −0,16 su N=156, hit-rate 32%): nessuna direzione attesa.
- **EURUSD=X (euro/dollaro)**: mediana +0,05% a T+1, +0,46% a T+5 — speculare al dollaro, come deve essere. ⚠️ "Debole" (IC −0,00 su N=193): nessun contenuto informativo apprezzabile.
- **HG=F (rame)**: mediana +0,16% a T+1 e **+1,05% a T+10**, con dispersione ampia. Non ha ancora un giudizio in scorecard (meno di 50 previsioni mature). Il fatto che il rame non scenda dopo un dato di attività USA debole è coerente con il suo essere un termometro della domanda **globale** (soprattutto cinese), non americana.

**La sintesi onesta**: dei sette asset con giudizio in scorecard, **tre sono ❌ controproducenti** (^TNX, IEF, DX-Y.NYB) e uno è privo di contenuto (EURUSD=X). La lettura direzionale di questa scheda poggia su **^NDX e ^VIX** (entrambi ✅, IC +0,17), e dice: *azionario growth in calo il giorno dopo, con recupero entro due settimane, ma premio per il rischio (volatilità) in salita per tutto il periodo*.

**Regime misto — da dichiarare, ed è cruciale qui.** La research sui dati macro USA documenta la **state-dependence**: lo stesso dato debole produce reazioni di segno opposto a seconda del regime. Nel 2022-2023 un dato di attività debole faceva salire l'azionario (meno pressione sulla Fed); nel 2024 lo faceva scendere (meno utili). Il campione contiene entrambi i regimi, e le mediane li mescolano. Nel regime attuale — attività debole **e** inflazione alta per cause esogene — il canale "meno pressione sulla banca centrale" è **bloccato**, perché la parte lunga non risponde alla Fed. Questo è un argomento per aspettarsi una reazione più vicina a quella del 2024 (bad news = bad news) che a quella del 2022-2023.

---

## Considerazioni qualitative

Il valore di questo dato non sta nel numero ma nella **catena causale che chiude**.

Passo per passo: il Tesoro americano deve collocare quantità crescenti di debito ([news_03](news_03.md)); i compratori chiedono un premio più alto per assorbirlo; il rendimento del titolo a 10 e a 30 anni sale; il mutuo residenziale americano a tasso fisso trentennale è prezzato con uno spread sopra il decennale, quindi la rata sale; a parità di reddito la famiglia può permettersi una casa meno cara, e la domanda scende; il costruttore, che vede l'invenduto accumularsi, smette di aprire cantieri. **Sette settimane fa questo era un ragionamento; oggi è un dato del Census Bureau.**

Ed è per questo che il briefing lo definisce "il canale di trasmissione dal mercato obbligazionario all'economia reale che opera in tempo reale". Le rilevazioni sull'edilizia sono fra le più anticipatrici che esistano, perché costruire richiede una decisione di investimento presa oggi per ricavi che arriveranno fra dodici-diciotto mesi. Quando il costruttore si ferma, sta dicendo qualcosa sulle sue aspettative, non sul suo presente.

**Perché la banca centrale è in trappola.** Nel manuale, un calo del 12,4% dei cantieri è un argomento per allentare: la Federal Reserve taglia, i tassi sui mutui scendono, l'edilizia riparte. Ma qui la catena si rompe in due punti. Primo: i tassi lunghi non sono alti *per colpa* della Fed — il target sui Fed funds è 3,50-3,75% e il mercato non sconta rialzi — ma per il premio a termine legato a deficit e inflazione. Tagliare il tasso di policy non lo abbassa meccanicamente. Secondo: l'inflazione è alimentata da uno shock energetico esogeno ([news_01](news_01.md)) e nell'area euro la componente energia è al 10% su base annua. Se la Fed tagliasse in questo contesto, il mercato potrebbe leggerlo come cedimento sull'obiettivo di inflazione — e le aspettative di inflazione più alte farebbero salire *ancora* il premio a termine, cioè il mutuo. **La banca centrale non ha uno strumento che agisca sulla variabile giusta.** È questo che significa "stagflazione" in termini operativi, e non è un aggettivo enfatico.

**La conferma da Home Depot.** Il briefing accosta i due dati in modo istruttivo. Home Depot riporta vendite comparabili in crescita dell'1,7%, il dato migliore dal terzo trimestre fiscale 2022, e attribuisce la forza a "domanda diffusa per progetti di dimensioni contenute". Sembra una smentita del quadro. Non lo è: è lo stesso quadro visto dall'altra parte. Se comprare una casa nuova è proibitivo, la famiglia resta dove sta e ristruttura. La spesa si sposta dal *nuovo* (che genera cantieri, occupazione edilizia, domanda di legname e cemento) al *rifacimento* (che genera scontrini in un negozio di bricolage). Il PIL non cambia molto; l'occupazione ciclica sì. Noi non abbiamo Home Depot in database — è single-name, e il nostro universo è cross-asset — quindi la notizia è stata scartata dal triage, ma serve da conferma qualitativa.

**Cosa guardare.** Le minute del FOMC del 28-29 luglio escono alle 14:00 ora di New York, e questo dato ci sta "direttamente sotto", come dice il briefing. La domanda non è se la Fed alzerà, ma **perché la maggioranza ha tenuto fermo**: se perché vede l'inflazione rientrare, oppure perché ha deciso di guardare attraverso lo shock energetico. Nel primo caso, un dato di attività debole rafforza il caso per un allentamento e l'azionario può leggerlo con sollievo. Nel secondo, il dato debole è solo un dato debole, e il canale "bad news is good news" resta chiuso. Il campione storico, mescolando i due regimi, non risolve la domanda: le minute forse sì.

---

## Glossario — sigle e termini

- **Housing starts (cantieri residenziali avviati)** — numero di nuove abitazioni la cui costruzione è iniziata nel mese, pubblicato dal Census Bureau in **ritmo annualizzato destagionalizzato** (cioè: quante se ne costruirebbero in un anno se il ritmo del mese si mantenesse, corretto per la stagionalità).
- **Single-family starts** — cantieri di case unifamiliari, la componente che assorbe più occupazione edilizia e materiali rispetto ai condomini.
- **Census Bureau** — l'ufficio statistico federale USA che pubblica il dato.
- **Consenso (consensus)** — la mediana delle previsioni degli economisti censiti prima della release; qui 1,35 milioni da un sondaggio Reuters. La differenza fra dato e consenso è la **sorpresa**, ed è ciò che il mercato prezza.
- **PIL / GDP** — Prodotto Interno Lordo, il valore di tutti i beni e servizi prodotti in un'economia.
- **ISM** — Institute for Supply Management: pubblica gli indici mensili di attività manifatturiera e dei servizi USA basati su un sondaggio ai responsabili acquisti. Sopra 50 = espansione.
- **PMI (Purchasing Managers' Index)** — indice dei responsabili acquisti, l'equivalente internazionale dell'ISM.
- **CPI (Consumer Price Index)** — indice dei prezzi al consumo, la misura standard dell'inflazione.
- **NFP (Non-Farm Payrolls)** — i nuovi posti di lavoro creati negli USA esclusa l'agricoltura, il principale dato mensile sul mercato del lavoro.
- **FOMC** — Federal Open Market Committee, il comitato di politica monetaria della Federal Reserve.
- **Fed funds target** — l'intervallo obiettivo per il tasso sui prestiti overnight fra banche USA; oggi 3,50-3,75%.
- **Premio a termine (term premium)** — il compenso extra richiesto per detenere un titolo a lunga scadenza, oltre alla media attesa dei tassi a breve. Vedi [news_03](news_03.md).
- **Stagflazione** — combinazione di attività economica debole e inflazione alta: la situazione in cui gli strumenti di politica monetaria agiscono in direzioni contrastanti sui due obiettivi.
- **State-dependence** — il fatto che la reazione dei mercati allo stesso dato cambi di segno a seconda del regime macro in cui ci si trova.
- **^TNX / ^GSPC / ^NDX / ^VIX** — rendimento Treasury USA a 10 anni; indice S&P 500; indice Nasdaq-100; indice CBOE di volatilità implicita a 30 giorni.
- **IEF** — ETF iShares su Treasury USA 7-10 anni; è un **prezzo**, quindi si muove al contrario di ^TNX.
- **DX-Y.NYB** — indice del dollaro USA contro un paniere di sei valute.
- **EURUSD=X** — cambio euro/dollaro: in salita = euro che si rafforza.
- **HG=F** — futures sul rame (Comex), usato come termometro della domanda industriale globale.
- **T+N** — N giorni di **borsa** dopo il giorno dell'evento.
- **Mediana vs media** — la mediana è il valore centrale, robusta agli estremi; la media può essere trascinata da un solo episodio.
- **p25 / p75** — primo e terzo quartile; la loro distanza misura la dispersione, cioè quanto il valore centrale sia affidabile.
- **Information Coefficient (IC)** — correlazione di rango fra previsione e risultato, calcolata settimanalmente dalla scorecard. Negativo = segno storicamente rovesciato.

---

## Caveat

1. **Il filtro di direzione non discrimina.** Con `--direction pos` la libreria restituisce 28 dei 29 episodi identici: il pool di `activity_growth` è direzionalmente ambiguo. Le mediane descrivono il comportamento tipico attorno a **una release di attività**, non a **una sorpresa al ribasso**. È il limite più serio della scheda.
2. **Pool non specifico all'edilizia.** Gli episodi sono in maggioranza release di indagine congiunturale (ISM, PMI). Il canale immobiliare — che passa per il tasso sul mutuo e ha tempi di reazione più lenti — non è rappresentato in modo specifico.
3. **State-dependence del segno.** Come documenta la research sui dati macro USA, in regime di inflazione alta un dato debole è "buona notizia" per l'azionario, in regime di crescita è "cattiva notizia". Il campione contiene entrambi, e le mediane li mescolano. Nel regime attuale il canale "meno pressione sulla banca centrale" è però bloccato, perché la parte lunga non risponde al tasso di policy.
4. **Tre asset su cui NON traiamo direzione.** Scorecard 2026-W34, sezione 5-bis: **^TNX** (IC −0,20, N=208), **IEF** (IC −0,29, N=66) e **DX-Y.NYB** (IC −0,16, N=156) sono ❌ **controproducenti**. **EURUSD=X** è ⚠️ debole con IC −0,00, cioè privo di contenuto informativo. La lettura poggia su **^NDX** e **^VIX** (✅ IC +0,17 entrambi).
5. **Convenzione di segno mista.** ^TNX è un rendimento, IEF un prezzo: mediane di segno opposto significano **accordo**, non divergenza.
6. **Volatilità dei dati sull'edilizia.** Le rilevazioni mensili sui cantieri hanno errori campionari ampi e revisioni frequenti: un singolo −12,4% va confermato dal mese successivo prima di essere trattato come cambio di tendenza.
7. **Correlazione non è causalità.** Ognuna delle 28 date conteneva anche altre notizie. L'event study misura ciò che è accaduto attorno a quelle date, non ciò che il dato ha causato.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Pool analoghi: libreria episodi (Opzione B), filtro date-locale `activity_growth`, direzione `neg` (filtro non discriminante, dichiarato), no-look-ahead `--before 2026-08-19`
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
- Catalog timestamp: 2026-08-19T07:27:10
