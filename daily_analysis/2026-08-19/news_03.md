# L'asta USA a 20 anni 'taglia' a 5,047% e il trentennale tocca il massimo da 19 anni: il premio a termine si riprezza, e l'oro rompe al ribasso

**Data analisi**: 2026-08-19
**Fonte**: Morning Briefing 2026-08-19 (fin 03, fin 09)
**Slug**: us-20y-auction-tail-term-premium

---

## Testo notizia (originale)

> Il Tesoro USA ha collocato 16 miliardi di dollari di titoli a 20 anni a un rendimento massimo del 5,047%, sopra il 5,035% atteso alla chiusura delle offerte e molto sopra il 4,810% dell'asta precedente: cinque delle sette aste precedenti a 20 anni avevano gia' 'tagliato' (tailed), segno che la domanda dei dealer per la duration lunga si sta assottigliando. Il rendimento trentennale ha superato il 5,33% intraday martedi', massimo dal 2007, prima di rientrare verso il 5,285%, mentre il decennale si e' spinto verso il 4,75%. Cio' avviene mentre la probabilita' di un rialzo Fed a breve si indebolisce sui dati deboli: la parte lunga sta quindi rispondendo a offerta, deficit e persistenza dell'inflazione, non al sentiero di policy (il target sui Fed funds resta 3,50-3,75%). In parallelo l'oro spot e' sceso a 4.340-4.350 dollari l'oncia dopo aver rotto quota 4.400, dai 4.430 della seduta precedente, e l'argento ha perso il 3,5% a circa 63,5 dollari: la coppia anomala 'oro vicino ai record + rendimenti nominali record' si e' risolta nella direzione convenzionale, cioe' il costo-opportunita' di detenere un asset a cedola zero.

---

## In breve (in parole semplici)

Il Tesoro americano ha venduto 16 miliardi di dollari di titoli a 20 anni e ha dovuto pagare **più** di quanto il mercato si aspettasse per collocarli: è quello che in gergo si chiama "asta che taglia" (*tail*). Non è la prima volta: cinque delle sette aste precedenti a 20 anni erano già andate così. In parallelo il rendimento del titolo a 30 anni ha toccato il 5,33%, il livello più alto dal 2007.

La cosa importante è *perché* sta succedendo. Non perché il mercato si aspetti un rialzo dei tassi dalla banca centrale — anzi, i dati deboli hanno spinto gli operatori a scommettere che la Federal Reserve non li alzerà. Sta succedendo perché **c'è troppa carta da collocare**, il deficit è alto e l'inflazione non scende: fattori che riguardano l'offerta di titoli e il premio richiesto per tenerli a lungo, non la politica monetaria.

Nella stessa seduta l'oro ha rotto al ribasso quota 4.400 dollari. Non è una coincidenza: è lo stesso meccanismo visto dall'altro lato.

---

## Classificazione

| Campo | Valore |
|---|---|
| `primary_theme` | monetary_policy |
| `sub_themes` | term_premium, auction, curve_steepening |
| `sentiment` | bearish (sui titoli a lunga scadenza) |
| `confidence` | medium |
| `horizon` | 1-10 giorni di trading |

**Motivazione classificazione**: `monetary_policy` è la categoria in cui la libreria colloca gli episodi di **premio a termine**, con 17 episodi a etichetta date-locale sul token `term_premium`. È una scelta di comodo tassonomico più che concettuale: il contenuto della notizia è **fiscale e di offerta** (deficit, emissioni, domanda dei dealer), non di politica monetaria — è precisamente il punto della notizia, cioè che la parte lunga ha smesso di prendere il segnale dal tasso di policy. La categoria `fiscal_policy`, che sarebbe concettualmente più appropriata, ha nella libreria solo 10 episodi con etichetta date-locale (il token `term_premium` vi compare **solo a livello di documento**, cioè con il filtro debole): sarebbe stato un campione insufficiente. Sentiment `bearish` sui titoli a lunga. Confidence `medium`.

**Consolidamento**: questa scheda copre due notizie del briefing — fin 03 (asta e rendimenti) e fin 09 (rottura dell'oro) — perché sono lo stesso meccanismo osservato su due asset. Quando i rendimenti nominali salgono abbastanza, il costo-opportunità di detenere un'attività che non paga cedola (l'oro) diventa insostenibile e la domanda da bene rifugio cede.

---

## Asset rilevanti

### Primary (canale diretto)
- **^TYX** (rendimento del Treasury USA a 30 anni) — la scadenza dove vive il premio a termine: è *l'*asset della notizia.
- **^TNX** (rendimento del Treasury USA a 10 anni) — il benchmark globale del costo del denaro a lungo.
- **IEF** (ETF iShares su Treasury USA 7-10 anni) — proxy di **prezzo** della duration americana.
- **IGLT.L** (ETF iShares su Gilt, titoli di Stato britannici) — proxy di **prezzo** della curva UK.
- **1482.T** (ETF su JGB, titoli di Stato giapponesi) — proxy di **prezzo** della curva giapponese.
- **VGB.AX** (ETF Vanguard su titoli di Stato australiani) — proxy di **prezzo** della curva australiana.
- **EXX6.DE** (ETF su Bund/governativi tedeschi) — proxy di **prezzo** della curva tedesca.

⚠ **Convenzione di segno mista — leggere con attenzione.** `^TYX` e `^TNX` sono **rendimenti**: salgono quando i titoli vengono venduti. `IEF`, `IGLT.L`, `1482.T`, `VGB.AX`, `EXX6.DE` sono **prezzi di ETF**: scendono nello stesso momento. In un selloff globale sincronizzato la tabella mostra i primi in positivo e i secondi in negativo: **è coerenza, non divergenza**. Nella tabella qui sotto vale il contrario, perché la mediana degli analoghi indica un *rientro* dei rendimenti (^TYX negativo) e quindi un *recupero* dei prezzi (ETF positivi) — ancora una volta, i due gruppi concordano.

### Secondary (effetti indiretti)
- **GC=F** (futures sull'oro) — l'oro non paga cedola: quando i rendimenti nominali salgono, tenerlo costa in termini di rendimento rinunciato.
- **^NDX** (indice Nasdaq-100) — le società growth valgono per i flussi di cassa lontani, che vengono scontati proprio con i tassi a lunga: sono le più sensibili.
- **^GSPC** (indice S&P 500) — canale generale del "tasso privo di rischio".
- **DX-Y.NYB** (indice del dollaro contro un paniere di valute) — canale valutario del differenziale di rendimento.

---

## Knowledge Base — research correlate

- [score=10] `Premio a termine globale e selloff sincronizzati della parte lunga — regime ed episodi storici (1994–2026)/…md`
  - Perché è rilevante: è la research dedicata esattamente a questo fenomeno — i selloff sincronizzati della parte lunga delle curve sovrane — e fornisce la base storica sia degli episodi sia della distinzione fra shock locale e shock globale.
- [score=9] `Fed_ reaction function, indipendenza e divergenza con la BCE (2023–2026)/…md`
  - Perché è rilevante: serve per capire cosa il mercato si aspetta dalla Federal Reserve (le minute del FOMC di luglio escono oggi pomeriggio) e perché la parte lunga si sta **scollegando** dalla funzione di reazione della banca centrale.
- [score=8] `Giappone : Bank of Japan- carry trade, uscita YCC e interventi FX — regime ed episodi storici (1998–2026)/…md`
  - Perché è rilevante: il decennale giapponese è ai massimi dal 1996 e la parte lunga giapponese è, come nota il briefing, "l'ancora del premio a termine globale" — vedi anche [news_06](news_06.md).

---

## Regime storico identificato

- **Regime**: selloff sincronizzato globale della parte lunga, in corso e riconosciuto dal progetto almeno dal 2026-08-18 (data in cui sono stati aggiunti al database ^TYX, IGLT.L, 1482.T e VGB.AX proprio per poterlo misurare).
- **Caratterizzazione**: il tratto distintivo di questo regime è la **disconnessione fra tasso di policy e parte lunga**. Il target sui Fed funds è fermo al 3,50-3,75% e il mercato ha smesso di scontare rialzi, eppure il trentennale è al massimo da 19 anni. Quando la parte lunga sale mentre le aspettative di policy scendono, la componente che sta salendo non è il tasso atteso ma il **premio a termine**: il compenso extra che gli investitori chiedono per immobilizzare denaro per trent'anni in un contesto di deficit elevati e inflazione persistente. Il briefing lo formula esattamente così: *"un'asta che taglia è l'evidenza più pulita disponibile che il premio a termine è fissato dal bilancio del compratore marginale e non dalle previsioni macro"*.
- Elemento di regime aggiuntivo: la sincronizzazione. Il gilt decennale britannico è sopra il 5,05%, il JGB decennale al massimo dal 1996. Non è una storia americana; è una storia di **capacità di bilancio** dei detentori di duration in tutto il mondo.
- Elemento nuovo di oggi: **l'oro cede**. La research e il regime documentavano una coppia anomala — oro vicino ai record insieme a rendimenti nominali record — che si spiegava leggendo l'oro come copertura contro il rischio di credibilità fiscale e monetaria, non come attività a tasso reale. La rottura sotto 4.400 dollari suggerisce che quella lettura si stia esaurendo, il che, come nota il briefing, rende *più difficile* leggere il segnale sul rischio istituzionale.

---

## Event study

### Episodi storici analoghi selezionati

Pool ottenuto dalla libreria (Opzione B) con:
`--theme monetary_policy --subtheme term_premium --direction neg --before 2026-08-19`
→ 17 episodi con etichetta **date-locale** sul token `term_premium`. Nessuna potatura dell'analista.

⚠ **Filtro di direzione debole — da dichiarare.** La diagnostica della libreria segnala: *"direzione 'neg' stretta dava solo 5 episodi (<12) → incluso mixed/sconosciuto"*. Il pool contiene quindi anche episodi a direzione non determinata, ed è più corretto leggerlo come **"giornate di riprezzamento del premio a termine"** che come "shock negativi sulla parte lunga". Questo è il limite principale di questa scheda.

Tre episodi non entrano nell'event study: `1994-02-04` e `2003-06-25` precedono l'inizio del database (2011), e `2026-08-18` è di ieri e non ha ancora giorni realizzati. **N effettivo = 14** (12 per il JGB, che ha storia dal 2016-05).

**Episodi utilizzati** (con il meccanismo, non solo il fatto):

- `2015-05-07` — apice del "Bund tantrum": **il rendimento del decennale tedesco passa da quasi zero a oltre lo 0,7% in poche settimane senza alcun cambio di politica BCE → riprezzamento puro del premio a termine su posizionamento affollato**.
- `2015-06-04` — seconda gamba dello stesso tantrum, dopo che Draghi invita il mercato ad "abituarsi alla volatilità": **la banca centrale rinuncia esplicitamente ad ancorare la parte lunga**.
- `2021-02-25` — asta del 7 anni USA con domanda disastrosa: **è l'analogo più stretto della notizia di oggi — un'asta che non trova compratori al prezzo atteso → salto discreto del premio a termine e contagio all'azionario growth**.
- `2021-03-18` — riunione FOMC che tollera la salita dei rendimenti lunghi: **assenza di reazione della banca centrale → validazione implicita del premio a termine più alto**.
- `2022-12-20` — la Bank of Japan allarga a sorpresa la banda di oscillazione del controllo della curva (YCC): **rimozione parziale dell'ancora giapponese → i capitali giapponesi hanno meno bisogno di comprare duration estera, premio a termine globale in salita**.
- `2023-10-19` — il decennale USA tocca il 5%: **culmine del selloff da offerta del 2023, con deficit e emissioni al centro del dibattito**.
- `2024-03-19` — la Bank of Japan esce dai tassi negativi: **fine del regime che rendeva il Giappone compratore strutturale di duration mondiale**.
- `2024-11-06` — reazione all'esito elettorale USA: **riprezzamento delle aspettative fiscali → il premio a termine incorpora deficit attesi più alti**.
- `2025-04-04` — turbolenza da annunci commerciali: **shock che colpisce simultaneamente inflazione attesa e domanda estera di Treasury**.
- `2025-05-19` — declassamento del rating sovrano USA da parte di Moody's: **peggioramento della percezione di merito di credito sovrano → premio richiesto sulla scadenza lunga**.
- `2025-05-21` — asta del 20 anni USA che taglia: **è, insieme al 2021-02-25, l'analogo formalmente identico alla notizia di oggi**.
- `2025-09-03` — nuova gamba di selloff sulla parte lunga globale: **sincronizzazione fra curve**.
- `2025-12-24` — episodio di riprezzamento in seduta a bassa liquidità: **quando il book è sottile, l'ampiezza del movimento sovrastima il contenuto informativo**.
- `2026-05-19` — episodio di premio a termine nel regime corrente: **l'analogo più vicino per regime macro (guerra USA-Iran, inflazione energetica, deficit)**.
- *(fuori campione ma nel pool)* `1994-02-04` — rialzo a sorpresa della Federal Reserve che apre il "grande bond massacre" del 1994; `2003-06-25` — taglio di 25 punti base invece dei 50 attesi, con i rendimenti lunghi che **salgono** dopo un allentamento: entrambi antecedenti al database, citati perché sono i casi di scuola del fenomeno.
- *(nel pool ma senza dati realizzati)* `2026-08-18` — l'episodio di ieri, che ha motivato l'aggiunta al database delle curve sovrane non-USA.

### Comando eseguito

```bash
venv/bin/python analogues.py find --theme monetary_policy --subtheme term_premium \
  --direction neg --before 2026-08-19

venv/bin/python event_study.py \
  --ticker '^TYX,^TNX,IEF,IGLT.L,1482.T,VGB.AX,EXX6.DE,GC=F,^NDX,^GSPC,DX-Y.NYB' \
  --events 1994-02-04,2003-06-25,2015-05-07,2015-06-04,2021-02-25,2021-03-18,2022-12-20,2023-10-19,2024-03-19,2024-11-06,2025-04-04,2025-05-19,2025-05-21,2025-09-03,2025-12-24,2026-05-19,2026-08-18 \
  --windows 1,3,5,10 --markdown
```

### Risultati

Rendimenti cumulati a T+1, T+3, T+5, T+10 **giorni di borsa** dopo l'episodio. Per ^TYX e ^TNX la variazione è quella del **rendimento** (un +2% significa che il rendimento è salito del 2% relativo, non di 2 punti percentuali); per gli ETF obbligazionari è la variazione del **prezzo**.

### Event study — `^TYX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.13% | -0.21% | +0.53% | -0.16% |
| mediana | -0.29% | -1.68% | +0.02% | +0.11% |
| dev std | +2.21% | +4.08% | +4.61% | +4.62% |
| p25 | -0.88% | -2.90% | -3.02% | -3.96% |
| p75 | +0.42% | +2.50% | +2.10% | +1.61% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `^TNX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.31% | -0.52% | +0.29% | -0.37% |
| mediana | -0.69% | -2.09% | -0.18% | -0.14% |
| dev std | +2.19% | +4.58% | +4.96% | +4.02% |
| p25 | -1.49% | -3.39% | -3.52% | -3.14% |
| p75 | +0.09% | +1.80% | +2.42% | +0.94% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `IEF`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.18% | +0.25% | +0.06% | +0.33% |
| mediana | +0.31% | +0.74% | +0.15% | +0.17% |
| dev std | +0.58% | +0.97% | +1.23% | +1.10% |
| p25 | -0.02% | -0.43% | -0.31% | +0.03% |
| p75 | +0.55% | +0.93% | +1.02% | +0.81% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `IGLT.L`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.11% | +0.35% | +0.37% | +0.88% |
| mediana | +0.24% | +0.82% | +0.43% | +0.99% |
| dev std | +0.60% | +1.27% | +1.09% | +1.10% |
| p25 | +0.01% | -0.40% | -0.20% | +0.30% |
| p75 | +0.43% | +1.15% | +1.07% | +1.46% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `1482.T`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.03% | +0.05% | -0.09% | +0.10% |
| mediana | +0.03% | +0.06% | +0.09% | +0.03% |
| dev std | +0.49% | +1.08% | +1.12% | +1.19% |
| p25 | -0.32% | -0.26% | -0.32% | -0.39% |
| p75 | +0.31% | +0.86% | +0.53% | +0.87% |
| **N** | **12** | **12** | **12** | **12** |



### Event study — `VGB.AX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.16% | +0.19% | +0.15% | +0.58% |
| mediana | +0.17% | +0.13% | +0.33% | +0.62% |
| dev std | +0.38% | +0.42% | +0.70% | +0.59% |
| p25 | -0.02% | +0.05% | -0.35% | +0.15% |
| p75 | +0.35% | +0.49% | +0.75% | +1.06% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `EXX6.DE`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.05% | +0.30% | +0.35% | +1.14% |
| mediana | +0.02% | +0.99% | +0.94% | +1.35% |
| dev std | +0.57% | +1.56% | +1.92% | +1.17% |
| p25 | -0.45% | -0.99% | -0.13% | +0.64% |
| p75 | +0.37% | +1.46% | +1.62% | +1.90% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `GC=F`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | -0.02% | -0.16% | +0.24% | +2.07% |
| mediana | +0.30% | +0.14% | +0.33% | +1.15% |
| dev std | +1.19% | +1.41% | +2.96% | +3.86% |
| p25 | -0.58% | -0.93% | -1.09% | -0.15% |
| p75 | +0.68% | +0.73% | +1.29% | +2.42% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `^NDX`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.54% | +1.29% | +0.44% | +1.68% |
| mediana | +0.62% | +1.52% | +0.51% | +1.38% |
| dev std | +0.90% | +2.84% | +3.11% | +2.18% |
| p25 | +0.00% | -0.63% | -1.35% | +0.76% |
| p75 | +1.26% | +1.77% | +1.73% | +2.77% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `^GSPC`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.27% | +0.83% | +0.45% | +1.34% |
| mediana | -0.04% | +0.67% | +0.55% | +1.42% |
| dev std | +0.80% | +2.19% | +2.11% | +1.11% |
| p25 | -0.21% | -0.42% | -0.93% | +0.53% |
| p75 | +0.88% | +1.18% | +1.26% | +2.28% |
| **N** | **14** | **14** | **14** | **14** |



### Event study — `DX-Y.NYB`

| Stat | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| media | +0.11% | +0.04% | -0.06% | -0.17% |
| mediana | +0.13% | +0.02% | +0.33% | +0.33% |
| dev std | +0.42% | +0.46% | +1.27% | +1.69% |
| p25 | -0.16% | -0.26% | -0.47% | -1.16% |
| p75 | +0.23% | +0.40% | +0.47% | +1.14% |
| **N** | **14** | **14** | **14** | **14** |

**In pratica, cosa dicono questi numeri.**

Il quadro è internamente coerente e va letto ricordando la convenzione di segno mista:

- **^TYX (rendimento 30 anni USA)**: mediana **−1,68% a T+3** e −0,29% a T+1, cioè il rendimento tende a **rientrare** nelle sedute successive allo shock. A T+5 e T+10 la mediana è sostanzialmente nulla (+0,02% / +0,11%): il rientro si esaurisce.
- **^TNX (rendimento 10 anni USA)**: stesso profilo, mediana −0,69% a T+1 e **−2,09% a T+3**. ❌ **Ma la scorecard 2026-W34 marca ^TNX come "controproducente": IC = −0,20 su N=208, hit-rate 45%. È l'asset con il segno storico più sistematicamente rovesciato di tutto il nostro universo. Non traiamo alcuna direzione attesa sul decennale USA da questa tabella.**
- **IEF, IGLT.L, VGB.AX, EXX6.DE (prezzi di ETF obbligazionari)**: mediane **positive** su tutti gli orizzonti (IEF +0,74% a T+3, IGLT.L +0,82%, VGB.AX +0,13%, EXX6.DE +0,99%). ✅ **Questo è esattamente ciò che deve accadere se i rendimenti rientrano: rendimenti giù ⇒ prezzi su.** Il fatto che ^TYX/^TNX siano negativi e gli ETF positivi è **coerenza fra i due gruppi**, non contraddizione. ❌ Su **IEF** però la scorecard segnala IC = −0,29 su N=66, il peggiore dell'intero elenco: anche qui, nessuna direzione attesa.
- **1482.T (JGB)**: praticamente piatto (mediana +0,03% / +0,06% / +0,09% / +0,03%), su N=12. Il Giappone si muove meno perché per gran parte del campione la sua curva era amministrata dalla banca centrale.
- **GC=F (oro)**: mediana leggermente positiva a breve (+0,30% a T+1) e **+1,15% a T+10**. ❌ **Scorecard: IC = −0,07 su N=302, "controproducente". Non ne traiamo una direzione**, il che è particolarmente rilevante oggi perché è proprio l'asset di cui parla la notizia fin 09. Ci limitiamo a osservare che, storicamente, dopo uno shock di premio a termine l'oro **non** aveva continuato a scendere — un'osservazione descrittiva che il track record del sistema su questo ticker impone di non trasformare in previsione.
- **^NDX (Nasdaq-100)**: mediana **+0,62% a T+1, +1,52% a T+3, +1,38% a T+10**. ✅ È l'asset più affidabile della tabella (scorecard: IC +0,17, N=126, "affidabile"). La lettura è che l'azionario growth, dopo lo shock, tende a recuperare insieme al rientro dei rendimenti — coerente con il meccanismo del tasso di sconto.
- **^GSPC (S&P 500)**: mediana −0,04% a T+1 ma **+1,42% a T+10**, con primo quartile positivo a T+10 (+0,53%). ⚠️ Scorecard: "debole" (IC +0,10, N=406). Direzione plausibile ma non forte.
- **DX-Y.NYB (dollaro)**: mediane minuscole e senza segno stabile. ❌ Scorecard: IC = −0,16 su N=156, "controproducente", con hit-rate al 32% (cioè sbagliato due volte su tre). Nessuna direzione attesa.

**La sintesi onesta**: su **quattro** degli asset più rilevanti di questa scheda — ^TNX, IEF, GC=F, DX-Y.NYB — la scorecard corrente ci dice che il segno storico è inaffidabile. La lettura direzionale poggia quindi su ^NDX (✅) e, in misura minore, ^GSPC (⚠️), più sulla **coerenza interna** fra rendimenti e prezzi obbligazionari, che è un controllo di qualità del dato più che una previsione.

**Regime misto — da dichiarare.** Il campione mescola shock di premio a termine europei (Bund tantrum 2015), giapponesi (uscita YCC 2022-2024), americani da offerta (2021, 2023, 2025) e da credito sovrano (declassamento Moody's 2025). Ha senso raggrupparli perché il *canale* è lo stesso — il compenso richiesto per la duration — ma l'ampiezza no: il 2025-04-04 (+9,2% sul rendimento a T+3) e il 2021-03-18 (−5,2%) sono agli antipodi.

---

## Considerazioni qualitative

Conviene partire dai termini, perché qui il gergo nasconde il meccanismo.

**Cos'è un'asta che "taglia".** Il Tesoro americano vende titoli all'asta. Prima dell'asta esiste un prezzo di riferimento sul mercato "when-issued" (il mercato a termine su titoli non ancora emessi). Se l'asta si chiude a un rendimento **più alto** di quel riferimento, significa che per piazzare tutta la carta il Tesoro ha dovuto offrire di più: la domanda era più debole del previsto. Quella differenza si chiama *tail*, coda. Ieri il riferimento era 5,035% e l'asta ha chiuso a 5,047%: 1,2 punti base di coda. È poco in assoluto, ma il segnale non è nel singolo numero — è che **cinque delle sette aste precedenti erano già andate così**. Una coda isolata è rumore; una serie di code è una tendenza nella capacità del sistema di assorbire duration.

**Cos'è il premio a termine.** Il rendimento di un titolo a 30 anni si può scomporre in due pezzi: (1) la media dei tassi a breve che il mercato si aspetta nei prossimi trent'anni, e (2) un compenso extra per il rischio di sbagliarsi — il **premio a termine**. Normalmente il pezzo (1) domina, e per questo i rendimenti lunghi seguono le aspettative sulla banca centrale. Oggi accade l'opposto: gli operatori hanno smesso di scontare rialzi della Federal Reserve (base case: nessun rialzo a settembre) e nonostante ciò il trentennale è al massimo da 19 anni. Per costruzione, se (1) scende e il totale sale, sta salendo (2). **Il bond market ha smesso di prendere il segnale dal tasso di policy** — che è letteralmente la frase del briefing.

**Perché è un fatto fiscale.** Il premio a termine sale quando (a) c'è più carta da collocare — deficit alti significano più emissioni — e (b) i compratori disposti a tenerla hanno meno capacità di bilancio. Il briefing fotografa il punto in modo esemplare: *"il premio a termine è fissato dal bilancio del compratore marginale, non dalle previsioni macro"*. Non è che gli economisti prevedano tassi più alti; è che i dealer non hanno più spazio per assorbire duration. Ed è per questo che la classificazione formale in `monetary_policy` è, come ammesso sopra, una scelta tassonomica e non concettuale.

**Perché l'oro cede proprio ora.** L'oro non paga cedole. Se un titolo di Stato sicuro rende il 5,33% annuo, tenere un lingotto costa quel 5,33% in rendimento rinunciato. Finché l'oro saliva *insieme* ai rendimenti — la coppia che il briefing definisce anomala e che durava da un paio di settimane — la spiegazione era che gli investitori non lo compravano come alternativa ai tassi reali ma come **assicurazione contro il rischio istituzionale**: contro il dubbio che il debito americano sia sostenibile e che la banca centrale resti indipendente. La rottura sotto 4.400 dollari, con l'argento a −3,5%, suggerisce che quel premio assicurativo si stia sgonfiando e che l'oro torni a comportarsi come un'attività a tasso reale. Il paradosso, ben colto dal briefing, è che questo **peggiora** la nostra capacità di leggere il mercato: finché l'oro segnalava il rischio istituzionale, era un termometro utile; se torna a seguire i tassi reali, quel termometro si spegne.

**Il nesso con il resto della giornata.** Questa scheda è il perno di tutte le altre. I tassi lunghi alti fanno crollare i cantieri residenziali USA ([news_04](news_04.md)) perché il mutuo trentennale è agganciato al rendimento decennale. Un movimento di 5 punti base sul trentennale sta producendo movimenti del 5% sul Kospi ([news_02](news_02.md)) perché le società growth valgono per i flussi lontani e il posizionamento non ha ammortizzatori. La parte lunga giapponese, che il briefing chiama "l'ancora del premio a termine globale", è a sua volta spinta dalle aspettative di rialzo della Bank of Japan ([news_06](news_06.md)). E l'inflazione energetica che alimenta la persistenza dei prezzi viene dal Golfo ([news_01](news_01.md)). **È un solo circuito.**

**Cosa guardare oggi.** Le minute del FOMC di luglio escono alle 14:00 ora di New York. Alla riunione del 28-29 luglio tre presidenti regionali (Logan, Hammack, Kashkari) avevano dissentito chiedendo un rialzo di 25 punti base. La domanda a cui le minute rispondono non è "alzeranno?" ma **"perché la maggioranza ha tenuto fermo?"**: perché ritiene che l'inflazione stia rientrando, o perché ritiene che uno shock energetico vada guardato attraverso (*look through*) senza reagire? Sono due funzioni di reazione molto diverse, e il briefing osserva che la parte lunga non sta prezzando né l'una né l'altra. Una lettura hawkish delle minute, su un mercato che apre con il Kospi a −5% alle spalle e la liquidità dei gestori ai minimi dal 1998, è la combinazione con meno margine d'errore della giornata.

---

## Glossario — sigle e termini

- **^TYX** — rendimento del titolo di Stato USA (Treasury) a 30 anni.
- **^TNX** — rendimento del titolo di Stato USA a 10 anni; il benchmark globale del costo del denaro a lungo termine.
- **IEF** — ETF iShares che detiene Treasury USA con scadenza 7-10 anni. È un **prezzo**: sale quando i rendimenti scendono.
- **IGLT.L** — ETF iShares sui Gilt, i titoli di Stato britannici. Anche questo un prezzo.
- **1482.T** — ETF quotato a Tokyo sui JGB (Japanese Government Bonds), i titoli di Stato giapponesi. Storia disponibile dal maggio 2016.
- **VGB.AX** — ETF Vanguard sugli ACGB (Australian Commonwealth Government Bonds). Storia dall'aprile 2012.
- **EXX6.DE** — ETF sui titoli di Stato tedeschi (Bund e affini).
- **GC=F** — futures sull'oro (Comex).
- **^NDX / ^GSPC** — indici Nasdaq-100 e S&P 500.
- **DX-Y.NYB** — indice del dollaro USA contro un paniere di sei valute principali.
- **Tail (coda) di un'asta** — differenza fra il rendimento a cui l'asta si chiude e quello atteso dal mercato subito prima. Positiva = domanda più debole del previsto.
- **Premio a termine (term premium)** — il compenso extra, oltre alla media attesa dei tassi a breve, che un investitore richiede per immobilizzare denaro su una scadenza lunga.
- **FOMC (Federal Open Market Committee)** — il comitato di politica monetaria della Federal Reserve, che fissa il tasso sui Fed funds.
- **Fed funds target** — l'intervallo obiettivo per il tasso sui prestiti overnight fra banche USA; oggi 3,50-3,75%.
- **Dissenso (dissent)** — voto contrario di un membro del comitato rispetto alla decisione della maggioranza; alla riunione di luglio ce ne sono stati tre, tutti a favore di un rialzo.
- **Forward guidance** — la comunicazione con cui una banca centrale indica il sentiero futuro dei tassi. Il presidente Warsh ha dichiarato di non volerla usare, il che aumenta l'incertezza sulla parte lunga.
- **Look through (guardare attraverso)** — scelta di una banca centrale di non reagire a un rialzo dei prezzi che considera temporaneo o esogeno (es. uno shock energetico).
- **YCC (Yield Curve Control)** — controllo della curva dei rendimenti: politica con cui la Bank of Japan fissava amministrativamente il rendimento decennale giapponese. Smantellata gradualmente fra il 2022 e il 2024.
- **Duration** — sensibilità del prezzo di un'obbligazione a una variazione dei tassi. "Assorbire duration" significa accettare quel rischio nel proprio bilancio.
- **Dealer** — gli intermediari (primary dealer) che hanno l'obbligo di partecipare alle aste del Tesoro USA e che poi rivendono i titoli sul mercato.
- **Punto base (basis point, bp)** — un centesimo di punto percentuale: 5 punti base = 0,05%.
- **Bund tantrum** — episodio del maggio-giugno 2015 in cui il rendimento del decennale tedesco passò da quasi zero a oltre lo 0,7% in poche settimane senza alcun cambio di politica della BCE.
- **T+N** — N giorni di **borsa** dopo il giorno dell'evento.
- **Information Coefficient (IC)** — correlazione di rango fra ciò che la scheda prevedeva e ciò che è accaduto. Negativo = il segno storico è sistematicamente rovesciato su quell'asset.

---

## Caveat

1. **Filtro di direzione debole.** La libreria ha dovuto includere episodi a direzione "mixed/sconosciuta" perché il filtro `neg` stretto lasciava solo 5 episodi. Il pool va letto come **"giornate di riprezzamento del premio a termine"**, non come "shock negativi": è il limite metodologico principale di questa scheda e spiega perché le mediane sono modeste.
2. **Quattro asset su cui NON traiamo direzione.** Secondo la scorecard 2026-W34, sezione 5-bis: **^TNX** (IC −0,20, N=208), **IEF** (IC −0,29, N=66), **GC=F** (IC −0,07, N=302) e **DX-Y.NYB** (IC −0,16, N=156) sono ❌ **controproducenti** — la mediana storica punta nella direzione sbagliata più spesso che no. Le loro tabelle sono riportate a fini descrittivi. La lettura direzionale poggia su ^NDX (✅ IC +0,17) e, debolmente, ^GSPC (⚠️ IC +0,10).
3. **Convenzione di segno mista.** ^TYX e ^TNX sono rendimenti, gli ETF obbligazionari sono prezzi: segni opposti significano **accordo**. Chi legge la tabella senza questo avvertimento conclude il contrario.
4. **Classificazione di comodo.** Il tema è sostanzialmente fiscale/di offerta, ma è classificato `monetary_policy` perché è lì che la libreria colloca `term_premium` con copertura sufficiente (17 episodi date-locali contro 10 in tutto `fiscal_policy`, dove `term_premium` esiste solo a livello di documento). Va tenuto presente confrontando questa scheda con la statistica per tema della scorecard.
5. **Campione ridotto rispetto al pool.** Su 17 episodi, 3 non producono dati: due precedono il database (1994, 2003) e uno è di ieri (2026-08-18). N=14, e N=12 per il JGB. Sopra la soglia "indicative only" ma non di molto.
6. **Regimi eterogenei.** Bund tantrum europeo, uscita dal YCC giapponese, shock da offerta americani e declassamento del rating sono lo stesso *canale* ma non la stessa *ampiezza*.
7. **La notizia sull'oro non ha un pool proprio.** Il consolidamento di fin 09 in questa scheda è concettualmente motivato (stesso meccanismo di costo-opportunità), ma il pool è costruito su episodi di premio a termine, non su rotture tecniche dell'oro. Sommato al fatto che GC=F è ❌ in scorecard, la parte "oro" di questa scheda va letta come **narrativa, non come misura**.
8. **Ancoraggio temporale.** I livelli citati sono chiusure USA del 18 agosto o quotazioni asiatiche del 19; le minute del FOMC non erano ancora uscite al momento della compilazione.

---

## Provenance

- Generata da: Claude Code session (manual classification)
- Tool versions: pipeline_tools.py / analogues.py / event_study.py (project news_impact_pipeline)
- Pool analoghi: libreria episodi (Opzione B), filtro date-locale `term_premium`, direzione `neg` (con fallback mixed dichiarato), no-look-ahead `--before 2026-08-19`
- Scorecard consultata: `daily_analysis/_scorecard/2026-W34.md`, sezione 5-bis
- Catalog timestamp: 2026-08-19T07:27:10
