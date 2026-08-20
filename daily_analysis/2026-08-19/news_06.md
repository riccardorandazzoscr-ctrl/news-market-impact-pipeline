# Ordini di macchinari core giapponesi +9,7% sul mese contro +7,8% atteso e +16,9% sull'anno contro +10,8%: il capex giapponese sorprende al rialzo

**Data analisi**: 2026-08-19
**Fonte**: Morning Briefing 2026-08-19 (fin 06)
**Slug**: japan-core-machinery-orders

---

## Testo notizia (originale)

> Gli ordini core di macchinari - che escludono le voci volatili navi e utility elettriche e sono l'indicatore anticipatore standard degli investimenti fissi giapponesi con sei-nove mesi di anticipo - sono saliti del 9,7% a giugno, invertendo il -12,4% di maggio e battendo il consenso del 7,8%; il tasso annuo e' passato a +16,9% da -1,9%, contro il +10,8% atteso, il piu' rapido in quattro mesi. E' una sorpresa al rialzo sostanziale, che indica una ripresa ampia degli investimenti delle imprese, e arriva a pochi giorni da un dato debole di PIL del secondo trimestre. Mizuho, separatamente, si attende ora che la Bank of Japan alzi i tassi piu' rapidamente perche' lo yen debole alimenta il rischio inflazione. Mercati: titoli di Stato giapponesi, yen a circa 159,4 per dollaro e industriali giapponesi; ordini di beni capitali forti rimuovono uno degli ultimi argomenti contro un rialzo BoJ a settembre, ed e' cio' che ha spinto il decennale JGB al massimo dal 1996 - e la parte lunga giapponese e' l'ancora del premio a termine globale.

---

## In breve (in parole semplici)

In Giappone gli ordini di macchinari "core" — cioè gli ordini che le aziende passano ai costruttori di impianti, esclusi navi e utility elettriche perché troppo volatili — sono saliti del 9,7% a giugno contro il +7,8% atteso, e del 16,9% su base annua contro il +10,8% atteso. È l'indicatore che anticipa di sei-nove mesi gli investimenti delle imprese giapponesi, e questa è una sorpresa al rialzo ampia.

Perché conta ben oltre il Giappone: uno degli ultimi argomenti contro un rialzo dei tassi della Bank of Japan a settembre era che l'economia fosse troppo debole. Questo dato lo toglie di mezzo. E il rendimento del titolo di Stato giapponese a 10 anni, già al massimo dal 1996, è — come dice il briefing — **"l'ancora del premio a termine globale"**. Quando il Giappone smette di essere il paese dei tassi a zero, tutto il mercato obbligazionario mondiale si riprezza.

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | macro_data |
| `sub_themes` | activity_growth, boj_normalization |
| `sentiment` | bullish (sull'attività; **hawkish** sul canale di politica monetaria) |
| `confidence` | medium |
| `horizon` | intraday-3 giorni |

**Motivazione classificazione**: `macro_data` perché è una release ufficiale (Cabinet Office giapponese) con consenso pubblicato e quindi sorpresa misurabile. Il sotto-tema canonico primario è `activity_growth`. Ma la **trasmissione** di questa notizia non passa dal canale attività: passa dalle **aspettative sulla Bank of Japan**, ed è per questo che la scheda usa due pool di analoghi invece di uno (vedi sotto). Sentiment doppio e vale la pena esplicitarlo: `bullish` sull'economia reale giapponese, `hawkish` sulla politica monetaria — e per gli asset i due segni non coincidono, perché un rialzo dei tassi è una buona notizia per lo yen e una cattiva per i titoli di Stato giapponesi.

---

## Asset rilevanti

### Primary (canale diretto)
- **^N225** (indice Nikkei 225, borsa di Tokyo) — gli industriali giapponesi sono i destinatari diretti degli ordini di macchinari.
- **JPY=X** (cambio dollaro/yen) — il canale valutario del differenziale di tassi. ⚠ Verso della quotazione: JPY=X è **yen per dollaro**, quindi un valore **in salita** significa **yen più debole**. Oggi è a circa 159,4.
- **1482.T** (ETF sui JGB, titoli di Stato giapponesi) — proxy di **prezzo** della curva giapponese: scende quando i rendimenti salgono. Storia disponibile dal maggio 2016.

### Secondary (effetti indiretti)
- **^GSPC** (indice S&P 500) — canale di contagio globale del premio a termine.
- **^TNX** (rendimento del Treasury USA a 10 anni) — il canale attraverso cui una Bank of Japan più restrittiva si trasmette ai rendimenti americani (vedi Considerazioni). *Riportato ma non usato per la direzione*: è ❌ controproducente in scorecard.

---

## Knowledge Base — research correlate

- [score=8] `Giappone : Bank of Japan- carry trade, uscita YCC e interventi FX — regime ed episodi storici (1998–2026)/…md`
  - Perché è rilevante: è **la** research su questo meccanismo. Copre il carry trade in yen, lo smantellamento del controllo della curva dei rendimenti (YCC) e gli interventi sul cambio, cioè tutti e tre i canali attraverso cui questa notizia si trasmette. Match diretto su JPY=X e ^N225.
- [score=8] `Premio a termine globale e selloff sincronizzati della parte lunga — regime ed episodi storici (1994–2026)/…md`
  - Perché è rilevante: documenta come la parte lunga giapponese funga da ancora del premio a termine mondiale — il nesso esplicito con [news_03](news_03.md).
- [score=8] `dati_macro_USA_e_trasmissione_ai_mercati_(2013–2024)/…md`
  - Perché è rilevante: fornisce il quadro generale su come una sorpresa macro si trasmette agli asset, e in particolare la dipendenza dal regime.

---

## Regime storico identificato

- **Regime**: normalizzazione della Bank of Japan dentro un selloff globale sincronizzato della parte lunga.
- **Caratterizzazione**: il Giappone ha passato quasi trent'anni con tassi a zero o negativi, ed è stato per questo l'esportatore netto di capitale verso il resto del mondo — gli investitori istituzionali giapponesi compravano titoli di Stato americani, europei e australiani perché in patria non rendevano nulla. Quel meccanismo si sta chiudendo: il decennale giapponese è al massimo dal 1996, la Bank of Japan ha già abbandonato il controllo della curva (2022-2024) e i tassi negativi (marzo 2024), e Mizuho ora si attende rialzi più rapidi perché lo yen debole alimenta l'inflazione importata. **Se in Giappone si guadagna qualcosa senza rischio di cambio, i capitali giapponesi tornano a casa e il premio a termine sale ovunque.** È il nesso diretto con [news_03](news_03.md).
- Elemento di contesto che qualifica il dato: arriva a pochi giorni da un dato debole di PIL del secondo trimestre. Un indicatore anticipatore forte dopo un dato ritardato debole è la configurazione più informativa possibile — è quella in cui l'indicatore anticipatore ha più valore aggiunto.
- Contro-elemento: gli ordini di macchinari sono fra le serie giapponesi più volatili. Il +9,7% di giugno arriva dopo un −12,4% di maggio: prima di leggerlo come svolta, va notato che gran parte del movimento è **rimbalzo**, non accelerazione.

---

## Event study

### Episodi storici analoghi selezionati

Questa scheda usa **due pool**, perché la classificazione formale e il canale di trasmissione non coincidono.

**(A) Pool per classificazione — `macro_data` / `activity_growth` / `pos`, N=28**
`--theme macro_data --subtheme activity_growth --direction pos --before 2026-08-19` → 28 episodi con etichetta date-locale.

⚠ **Il filtro di direzione non discrimina.** È lo stesso pool della scheda [news_04](news_04.md), che usa `--direction neg`: le due chiamate restituiscono 28 episodi su 29 identici. Gli episodi di `activity_growth` sono etichettati in modo direzionalmente ambiguo. Inoltre il pool è dominato da release **statunitensi** (ISM, PMI): come analogo di una sorpresa sul capex giapponese è debole. Lo riportiamo per completezza e per confrontabilità con news_04, non come lettura direzionale.

**(B) Pool per canale di trasmissione — `monetary_policy` / `boj` / `pos`, N=15**
`--theme monetary_policy --subtheme boj --direction pos --before 2026-08-19` → 15 episodi con etichetta date-locale, tutti giapponesi e tutti sul canale di normalizzazione. **È il pool su cui poggia la lettura di questa scheda.**

Episodi del pool (B), con il meccanismo:
- `2011-08-04` — intervento della Bank of Japan sul cambio contro lo yen troppo forte: **azione diretta sul canale valutario**.
- `2023-10-31` — la Bank of Japan rende "di riferimento" (anziché rigido) il tetto dell'1% sul decennale: **prima crepa formale nel controllo della curva → il mercato inizia a prezzare la fine del regime**.
- `2024-03-19` — uscita dai tassi negativi e abbandono formale del controllo della curva: **fine del regime che rendeva il Giappone compratore strutturale di duration estera**.
- `2024-07-31` — rialzo a sorpresa a 0,25% con annuncio di riduzione degli acquisti di titoli: **stretta doppia, tasso più bilancio → innesco della liquidazione del carry trade**.
- `2024-08-05` — culmine dell'unwind del carry trade in yen, con il Nikkei in caduta a doppia cifra: **il caso di scuola di come una stretta giapponese si propaghi agli asset di rischio mondiali**.
- `2024-08-07` — il vicegovernatore Uchida corregge il tiro dichiarando che non si alzerà in mercati instabili: **la banca centrale mostra la propria funzione di reazione al prezzo degli asset**.
- `2024-10-23` — fase di riprezzamento delle aspettative sulla Bank of Japan.
- `2024-12-18` — la Bank of Japan tiene fermo contro attese di rialzo: **yen più debole e rendimenti globali in salita**.
- `2025-01-23` / `2025-01-24` — rialzo a 0,50%: **conferma che la normalizzazione è un sentiero e non un episodio**.
- `2025-07-31` — riunione con revisione al rialzo delle proiezioni di inflazione: **guidance restrittiva senza mossa sui tassi**.
- `2025-12-10` / `2025-12-19` — sequenza di dicembre 2025 sulla normalizzazione.
- `2026-04-30` — riunione nel regime corrente, con lo shock energetico che complica la lettura dell'inflazione.
- `2026-06-11` — episodio più recente del canale Bank of Japan: **l'analogo più vicino per regime**.

### Comando eseguito

```bash
venv/bin/python analogues.py find --theme macro_data --subtheme activity_growth \
  --direction pos --before 2026-08-19
venv/bin/python analogues.py find --theme monetary_policy --subtheme boj \
  --direction pos --before 2026-08-19

# (A) pool per classificazione
venv/bin/python event_study.py --ticker '^N225,JPY=X,1482.T,^GSPC' \
  --events 2015-09-03,2015-12-01,2018-02-02,2019-08-01,2019-09-04,2019-10-01,2022-02-04,2022-08-03,2022-10-13,2022-11-01,2022-12-01,2023-02-03,2023-06-01,2023-07-12,2023-08-01,2023-08-03,2023-12-08,2024-02-02,2024-04-01,2024-06-07,2024-07-11,2024-08-01,2024-10-01,2024-12-06,2025-03-03,2025-09-30,2026-06-05,2026-07-24 \
  --windows 1,3,5,10 --markdown

# (B) pool per canale di trasmissione
venv/bin/python event_study.py --ticker '^N225,JPY=X,1482.T,^GSPC,^TNX' \
  --events 2011-08-04,2023-10-31,2024-03-19,2024-07-31,2024-08-05,2024-08-07,2024-10-23,2024-12-18,2025-01-23,2025-01-24,2025-07-31,2025-12-10,2025-12-19,2026-04-30,2026-06-11 \
  --windows 1,3,5,10 --markdown
```

### Risultati — (B) pool Bank of Japan, N=15 *(lettura principale)*

### Event study — `^N225`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.64% | +0.36% | +1.80% | +3.29% |
| mediana | -0.07% | +1.03% | +1.90% | +2.56% |
| dev std | +3.19% | +7.12% | +6.31% | +7.46% |
| p25 | -0.82% | -1.28% | -1.01% | -1.81% |
| p75 | +1.92% | +4.52% | +4.45% | +7.12% |
| **N** | **15** | **15** | **15** | **15** |



### Event study — `JPY=X`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.38% | -0.11% | -0.27% | -0.25% |
| mediana | +0.72% | +0.37% | -0.15% | +0.20% |
| dev std | +1.29% | +1.71% | +1.91% | +1.90% |
| p25 | -0.22% | -0.79% | -1.32% | -1.43% |
| p75 | +1.17% | +1.06% | +1.21% | +1.17% |
| **N** | **15** | **15** | **15** | **15** |



### Event study — `1482.T`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.02% | +0.45% | +0.35% | +0.31% |
| mediana | +0.06% | +0.37% | +0.50% | +0.46% |
| dev std | +0.49% | +1.14% | +0.97% | +1.39% |
| p25 | -0.22% | -0.21% | -0.12% | -0.87% |
| p75 | +0.45% | +0.88% | +0.75% | +1.09% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.15% | +0.29% | +0.53% | +1.83% |
| mediana | +0.21% | +0.70% | +0.48% | +1.20% |
| dev std | +1.05% | +2.44% | +2.80% | +3.71% |
| p25 | -0.19% | -0.92% | -0.89% | -0.56% |
| p75 | +0.77% | +1.66% | +2.30% | +3.16% |
| **N** | **15** | **15** | **15** | **15** |



### Event study — `^TNX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.19% | -1.83% | -1.47% | -2.34% |
| mediana | -0.27% | -1.49% | -1.23% | -1.54% |
| dev std | +2.03% | +4.18% | +2.54% | +5.14% |
| p25 | -1.38% | -2.82% | -3.07% | -4.53% |
| p75 | +0.63% | +0.51% | -0.11% | +1.48% |
| **N** | **15** | **15** | **15** | **15** |

### Risultati — (A) pool `activity_growth`, N=28 *(confronto, filtro direzionale non discriminante)*

### Event study — `^N225`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.58% | -0.91% | -0.54% | +0.51% |
| mediana | -0.21% | -0.09% | +0.21% | +0.64% |
| dev std | +1.97% | +3.19% | +3.35% | +4.50% |
| p25 | -2.12% | -2.94% | -2.08% | -1.56% |
| p75 | +0.67% | +0.97% | +1.13% | +3.28% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `JPY=X`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.10% | -0.08% | -0.02% | +0.06% |
| mediana | -0.12% | +0.07% | +0.10% | +0.16% |
| dev std | +0.91% | +1.27% | +1.64% | +2.66% |
| p25 | -0.46% | -0.97% | -0.95% | -1.56% |
| p75 | +0.44% | +0.91% | +1.22% | +2.09% |
| **N** | **28** | **28** | **28** | **28** |



### Event study — `1482.T`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.09% | -0.18% | -0.25% | -0.55% |
| mediana | -0.13% | -0.43% | -0.34% | -0.44% |
| dev std | +0.69% | +1.04% | +1.24% | +1.76% |
| p25 | -0.57% | -0.77% | -1.00% | -1.65% |
| p75 | +0.45% | +0.45% | +0.74% | +0.65% |
| **N** | **26** | **26** | **26** | **26** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.59% | -0.38% | -0.38% | +0.06% |
| mediana | -0.45% | -0.23% | -0.58% | +0.65% |
| dev std | +1.22% | +1.71% | +1.88% | +2.91% |
| p25 | -1.26% | -1.86% | -1.63% | -2.94% |
| p75 | +0.27% | +1.19% | +1.12% | +2.17% |
| **N** | **28** | **28** | **28** | **28** |

**In pratica, cosa dicono questi numeri.**

Ricordare i due versi: **JPY=X in salita = yen più debole**; **1482.T è un prezzo**, quindi scende quando i rendimenti giapponesi salgono.

**Pool (B), Bank of Japan, N=15 — la lettura principale:**
- **^N225 (Nikkei)**: mediana −0,07% a T+1 (praticamente nulla), poi **+1,03% a T+3, +1,90% a T+5, +2,56% a T+10**. In pratica: dopo un episodio di normalizzazione giapponese l'azionario di Tokyo non reagisce subito, ma costruisce guadagno nelle due settimane successive. **Attenzione però alla dispersione: deviazione standard del 7,1% a T+3 e primo quartile a −1,28%**, cioè in un quarto dei casi il Nikkei era in perdita. Dentro questo campione c'è il 2024-08-05, il crollo a doppia cifra da unwind del carry trade: un singolo episodio del genere ricorda che la coda sinistra è grossa. ⚠️ Scorecard 2026-W34: ^N225 è "debole" (IC +0,00 su N=79) — cioè il nostro track record su questo asset non mostra capacità predittiva. La direzione va presa con molta cautela.
- **JPY=X (dollaro/yen)**: mediana **+0,72% a T+1** — cioè **yen più debole** il giorno dopo — poi +0,37% a T+3 e sostanzialmente piatto a T+5 e T+10. Controintuitivo: una banca centrale più restrittiva dovrebbe rafforzare la valuta. La spiegazione plausibile è che il campione contiene diversi episodi in cui la Bank of Japan ha **deluso** attese di stretta (2024-12-18 su tutti), e in quei casi lo yen si indebolisce. ⚠️ Scorecard: JPY=X è "debole" (IC +0,04 su N=93, hit-rate 57%): direzione da trattare come indizio, non come previsione.
- **1482.T (prezzo JGB)**: mediana **positiva** su tutti gli orizzonti (+0,06% a T+1, +0,37% a T+3, +0,50% a T+5, +0,46% a T+10), N=14. Tradotto: dopo un episodio di normalizzazione i **prezzi** dei titoli di Stato giapponesi salgono, cioè i **rendimenti scendono**. È il classico "vendi la voce, compra la notizia": l'attesa della stretta fa salire i rendimenti prima dell'evento, e dopo l'evento rientrano. Nessun giudizio in scorecard (asset recente).
- **^TNX (rendimento 10 anni USA)**: mediana **−0,27% a T+1, −1,49% a T+3, −1,54% a T+10**, cioè i rendimenti americani *scendono* dopo un episodio Bank of Japan. Coerente con quanto visto sul JGB — stesso "compra la notizia" — e con il fatto che la trasmissione Giappone→USA è reale. ❌ **Ma la scorecard marca ^TNX come controproducente (IC −0,20, N=208): non ne traiamo una direzione attesa.** Riportiamo la tabella e ci fermiamo lì.
- **^GSPC (S&P 500)**: mediana +0,21% a T+1, +0,70% a T+3, **+1,20% a T+10**. Il contagio negativo agli asset di rischio globali, che il 2024-08-05 rese famoso, **non è la norma del campione**: nella mediana l'azionario americano assorbe. ⚠️ Scorecard: "debole" (IC +0,10).

**Pool (A), activity_growth, N=28 — confronto:** il quadro è più smorzato e, sul Giappone, di segno diverso: ^N225 mediana −0,21% a T+1 e +0,64% a T+10; 1482.T mediana **negativa** su tutti gli orizzonti (−0,13% → −0,44%), cioè rendimenti giapponesi in salita. Le due tabelle divergono proprio sull'asset centrale della notizia. Il motivo è che il pool (A) è direzionalmente ambiguo e non giapponese: non lo usiamo per la lettura, lo mostriamo per rendere visibile quanto la scelta del pool cambi il risultato.

**Regime misto — da dichiarare.** Anche il pool (B) copre regimi diversi: l'intervento sul cambio del 2011 (yen troppo **forte**) è l'opposto della situazione attuale (yen troppo **debole**), e gli episodi 2023-2024 appartengono alla fase di smantellamento del controllo della curva, non a quella di rialzi ordinari. Solo gli ultimi quattro episodi (2025-07-31 in poi) condividono il regime attuale di inflazione importata e yen debole.

---

## Considerazioni qualitative

Il valore di questa notizia non è nel Giappone. È nel **canale attraverso cui il Giappone tiene bassi i tassi di tutti gli altri**.

Il meccanismo, passo per passo. Per quasi trent'anni la Bank of Japan ha tenuto i tassi a zero o sotto zero, e per gran parte di quel periodo ha anche fissato amministrativamente il rendimento decennale (il "controllo della curva dei rendimenti", YCC). Il risultato è che un'assicurazione o un fondo pensione giapponese, che deve produrre un rendimento per pagare le proprie obbligazioni future, in patria non trovava niente: comprava quindi titoli di Stato americani, francesi, australiani. Il Giappone è stato per decenni il maggiore creditore netto del mondo, e questo flusso costante di domanda **comprimeva il premio a termine ovunque**. Non c'era bisogno che un americano comprasse Treasury: li comprava Tokyo.

Ora quel meccanismo si sta invertendo. Se il decennale giapponese rende il massimo dal 1996, quello stesso fondo pensione può restare a casa — senza rischio di cambio, senza costo di copertura. La domanda estera di duration si riduce, e chi emette debito (in primis il Tesoro americano, vedi [news_03](news_03.md)) deve pagare di più per collocarlo. **L'asta a 20 anni che ha "tagliato" ieri e gli ordini di macchinari giapponesi di stamattina non sono due notizie: sono due punti dello stesso circuito.** È esattamente il senso della frase del briefing, "la parte lunga giapponese è l'ancora del premio a termine globale".

**Perché gli ordini di macchinari e non un altro dato.** La Bank of Japan si trova davanti a un problema di sequenza. L'inflazione giapponese è sospinta soprattutto dallo yen debole, che rende care le importazioni — energia in testa. Alzare i tassi rafforzerebbe lo yen e curerebbe il problema alla radice. L'argomento contrario era che l'economia reale fosse troppo fragile per reggere una stretta, argomento rafforzato dal dato debole di PIL del secondo trimestre. Gli ordini di macchinari sono l'indicatore che risponde precisamente a quell'obiezione: misurano se le imprese hanno intenzione di **investire** nei prossimi sei-nove mesi. Un +16,9% su base annua contro un +10,8% atteso dice che ce l'hanno. Da qui la lettura di Mizuho, che si aspetta rialzi più rapidi.

**La cautela dovuta.** Va detto con chiarezza che gli ordini di macchinari sono una delle serie più rumorose del panorama statistico giapponese. Giugno fa +9,7% dopo che maggio aveva fatto −12,4%: sommando i due mesi, il livello è appena sopra quello di aprile. Buona parte del "balzo" è rimbalzo tecnico da una base depressa. La misura annuale (+16,9%) è più informativa proprio perché media il rumore mensile, ma anche lì il confronto è con un giugno 2025 debole. **Un mese non fa un ciclo di capex**, e la Bank of Japan lo sa meglio di chiunque.

**Il rischio di coda che il campione contiene.** Il 5 agosto 2024 è dentro il pool (B) e merita una menzione esplicita, perché è il promemoria di cosa può andare storto. Dopo il rialzo a sorpresa della Bank of Japan del 31 luglio 2024, la liquidazione del **carry trade in yen** — la strategia di prendere a prestito in yen a costo quasi nullo per investire in attività a rendimento più alto altrove — produsse in pochi giorni un crollo a doppia cifra del Nikkei e onde d'urto sui mercati globali. La mediana del nostro campione è positiva, ma quella coda esiste, ed è tanto più rilevante oggi quanto più il posizionamento è teso: il Fund Manager Survey di Bank of America riporta liquidità ai minimi da quasi trent'anni ([news_02](news_02.md)). **Quando non c'è cassa, ogni liquidazione forzata amplifica.**

**Lettura direzionale, con i limiti dichiarati.** Sui tre asset giapponesi la scorecard 2026-W34 è severa: ^N225 e JPY=X sono entrambi ⚠️ **deboli** (IC +0,00 e +0,04), 1482.T non è ancora giudicato. Il segno che il campione (B) suggerisce — Nikkei che costruisce guadagno su due settimane, yen che si indebolisce nella prima seduta, prezzi dei titoli di Stato giapponesi in recupero (cioè rendimenti in rientro dopo l'evento) — va quindi trattato come **descrizione del passato, non come previsione**. Su ^TNX il segno è esplicitamente inaffidabile (❌ IC −0,20). L'elemento su cui poggiare è qualitativo, non statistico: **la direzione strutturale del canale, cioè che una Bank of Japan che normalizza toglie un'ancora al premio a termine mondiale.**

---

## Glossario — sigle e termini

- **Ordini di macchinari core (core machinery orders)** — ordini che le imprese giapponesi passano ai costruttori di macchinari, **esclusi navi e utility elettriche** perché caratterizzati da commesse enormi e sporadiche che ne distorcerebbero la lettura. Pubblicati dal Cabinet Office; anticipano gli investimenti fissi delle imprese di sei-nove mesi.
- **Capex (capital expenditure)** — spesa per investimenti in beni durevoli (impianti, macchinari, immobili).
- **PIL / GDP** — Prodotto Interno Lordo.
- **BoJ (Bank of Japan)** — la banca centrale giapponese.
- **YCC (Yield Curve Control)** — controllo della curva dei rendimenti: politica con cui la Bank of Japan fissava amministrativamente il rendimento del titolo decennale giapponese. Introdotta nel 2016, allentata dal 2022 e abbandonata nel marzo 2024.
- **JGB (Japanese Government Bond)** — titolo di Stato giapponese.
- **Tassi negativi** — regime in cui la banca centrale applica un tasso sotto lo zero sui depositi delle banche presso di sé. Il Giappone li ha adottati nel 2016 e abbandonati nel marzo 2024.
- **Carry trade in yen** — strategia che consiste nel prendere a prestito yen a costo quasi nullo per investire in attività a rendimento più alto in altre valute. Si smonta bruscamente quando i tassi giapponesi salgono o lo yen si rafforza, come nell'agosto 2024.
- **Premio a termine (term premium)** — il compenso extra richiesto per detenere un titolo a lunga scadenza oltre alla media attesa dei tassi a breve. Vedi [news_03](news_03.md).
- **Inflazione importata** — aumento dei prezzi interni causato dal rincaro dei beni acquistati all'estero, tipicamente per effetto di una valuta più debole.
- **^N225** — indice Nikkei 225 della borsa di Tokyo.
- **JPY=X** — cambio dollaro/yen espresso come **yen per dollaro**: in salita = yen più debole. Oggi circa 159,4.
- **1482.T** — ETF quotato a Tokyo sui JGB. È un **prezzo**: scende quando i rendimenti giapponesi salgono.
- **^GSPC / ^TNX** — indice S&P 500 e rendimento del Treasury USA a 10 anni.
- **Consenso** — mediana delle previsioni degli economisti prima della release; la differenza col dato effettivo è la **sorpresa**.
- **T+N** — N giorni di **borsa** dopo il giorno dell'evento.
- **Information Coefficient (IC)** — correlazione di rango fra previsione e risultato, calcolata dalla scorecard settimanale. Vicino a zero = nessuna capacità predittiva; negativo = segno rovesciato.

---

## Caveat

1. **Doppio pool, risultati divergenti.** La scheda usa due insiemi di analoghi che danno risposte diverse sull'asset centrale (1482.T: prezzi in salita nel pool B, in discesa nel pool A). Questo è di per sé un avvertimento: **il risultato dipende sensibilmente dalla scelta del pool**. Abbiamo scelto (B) perché è giapponese e allineato al canale di trasmissione, ma la scelta è discrezionale e va dichiarata.
2. **Il pool (A) ha filtro direzionale non discriminante.** `--direction pos` e `--direction neg` restituiscono 28 episodi su 29 identici. Inoltre è dominato da release statunitensi. Non lo usiamo per la lettura.
3. **Nessuno degli asset ha una lettura direzionale forte.** Scorecard 2026-W34: **^N225** ⚠️ debole (IC +0,00, N=79), **JPY=X** ⚠️ debole (IC +0,04, N=93), **^GSPC** ⚠️ debole (IC +0,10). **^TNX** è ❌ **controproducente** (IC −0,20, N=208): riportato ma non interpretato direzionalmente. **1482.T** non ha ancora abbastanza previsioni mature. In sostanza, questa scheda **non ha un asset ✅ affidabile** su cui appoggiarsi: la lettura è qualitativa.
4. **Regime misto anche nel pool (B).** Copre l'intervento 2011 contro uno yen troppo *forte* (situazione opposta all'attuale), la fase di smantellamento del YCC (2023-2024) e i rialzi ordinari (2025-2026). Solo gli ultimi quattro episodi condividono il regime attuale.
5. **Serie statistica molto rumorosa.** Il +9,7% di giugno segue un −12,4% di maggio: gran parte del movimento è rimbalzo da base depressa. Un solo mese non identifica un ciclo di investimenti.
6. **Versi delle quotazioni.** JPY=X è yen per dollaro (in salita = yen più debole); 1482.T è un prezzo (in salita = rendimenti giapponesi in calo). Leggere il segno al contrario su uno dei due ribalta l'intera interpretazione.
7. **Coda sinistra grossa.** Il 2024-08-05 (unwind del carry trade, Nikkei a doppia cifra negativa) è dentro il campione: la mediana positiva non deve nascondere che questo canale ha prodotto uno dei drawdown più violenti del decennio, e che il posizionamento attuale è teso.
8. **Correlazione non è causalità.** Le date del pool (B) sono riunioni e interventi della Bank of Japan, non release di dati: sono analoghi di *canale*, non di *forma dell'evento*.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Pool analoghi: libreria episodi (Opzione B) — pool principale `monetary_policy` / date-locale `boj` / direzione `pos`; pool di confronto `macro_data` / `activity_growth` / `pos` (filtro non discriminante, dichiarato). No-look-ahead `--before 2026-08-19` su entrambi.
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
- Catalog timestamp: 2026-08-19T07:27:10
