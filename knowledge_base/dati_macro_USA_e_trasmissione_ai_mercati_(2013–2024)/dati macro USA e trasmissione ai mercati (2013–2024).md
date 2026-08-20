# Sorprese sui dati macro USA e trasmissione ai mercati (2013–2024): regimi, canali e state-dependence

## Sintesi esecutiva

Questo documento ricostruisce come le sorprese nei principali dati macroeconomici statunitensi si trasmettono ai mercati finanziari (Treasury, azionario USA, dollaro, oro) e come questa trasmissione cambia in funzione del regime di politica monetaria. La tesi centrale è che ciò che muove i prezzi non è il livello del dato, ma la sua componente non attesa — la sorpresa rispetto al consenso — e che il segno della reazione, soprattutto dell'azionario, è state-dependent: dipende dal punto del ciclo e dal regime di reaction function della Fed. Per un sistema di analogie storiche, ne segue che un episodio è trasferibile a un altro solo se condiviso regime di policy, posizione nel ciclo e regime di inflazione/attenzione: lo stesso dato (es. un CPI caldo) può produrre reazioni di segno opposto in regimi diversi.

## 1. Il framework "sorpresa vs atteso"

I prezzi degli asset incorporano in ogni istante le aspettative del mercato. Un dato che esce esattamente in linea con il consenso non contiene nuova informazione e, in teoria di mercati efficienti, non dovrebbe muovere i prezzi: ciò che li muove è la divergenza tra il dato realizzato e quello atteso, cioè la "sorpresa" o "news". Formalmente la sorpresa standardizzata si definisce come S = (A − E)/σ, dove A è il dato realizzato, E il consenso (mediana dei sondaggi, ad es. Bloomberg o Dow Jones) e σ la deviazione standard storica delle sorprese di quel dato; questa standardizzazione, introdotta da Balduzzi, Elton e Green (2001) e resa standard da Andersen, Bollerslev, Diebold e Vega (2003), rende confrontabili release con unità di misura diverse.

Questo è il risultato fondante della letteratura sull'"announcement effect". Andersen, Bollerslev, Diebold e Vega (2003, *American Economic Review*) dimostrano, con dati ad alta frequenza sul mercato dei cambi, che le sorprese macro producono "conditional mean jumps" — salti immediati nella media condizionata dei prezzi — collegando così le dinamiche FX ad alta frequenza ai fondamentali. Lo stesso quadro è poi esteso a bond e azioni in Andersen, Bollerslev, Diebold e Vega (2007, *Journal of International Economics*).

Per aggregare le molte sorprese in un'unica misura sintetica, gli operatori usano gli **indici di sorpresa economica**, di cui il più noto è il **Citi Economic Surprise Index (CESI)**. Il CESI è definito come una somma/media ponderata degli scarti standardizzati tra dati realizzati e consenso Bloomberg, calcolata su una finestra mobile di tre mesi; i pesi derivano dall'impatto storico ad alta frequenza di una sorpresa di una deviazione standard sul mercato dei cambi, con un fattore di decadimento temporale che replica la "memoria limitata" dei mercati. Due caratteristiche sono cruciali per l'uso: (i) il CESI è **mean-reverting** per costruzione — quando il consenso si adegua a una serie di dati forti, l'asticella si alza e diventa più difficile sorprendere al rialzo, e viceversa — per cui oscilla tra estremi; (ii) è nato come strumento per il trading valutario, non come predittore dell'azionario, e la sua correlazione con l'S&P 500 è storicamente debole. Va quindi letto come misura del "momentum delle sorprese" rispetto al consenso, non come segnale direzionale di equity.

Un'avvertenza interpretativa: la "sorpresa" è definita rispetto al consenso pubblicato, ma il consenso stesso può essere distorto o lento ad aggiornarsi (problema di nowcasting). Negli episodi di rottura — pandemia, cambi di regime — il consenso diventa poco informativo e la sorpresa misurata sovrastima o sottostima la vera componente inattesa.

## 2. Segmentazione per fasi di regime

La reaction function della Fed e la posizione nel ciclo cambiano la "funzione di trasmissione" dalla sorpresa al prezzo. Si distinguono cinque fasi.

### 2.1 ZIRP, forward guidance e taper tantrum (2013–2015)

Con i tassi a zero (ZIRP) e il QE in corso, la variabile-chiave non era il livello dei tassi (ancorato a zero) ma il *timing* del ritiro dello stimolo. In questo regime un dato macro forte veniva letto come "tapering più vicino": **bad news is bad news for bonds** — dati forti spingevano i rendimenti al rialzo perché anticipavano la riduzione degli acquisti. L'episodio emblematico è il **taper tantrum** del 2013: il 22 maggio 2013 Ben Bernanke, in testimonianza al Congresso, accennò alla possibilità di rallentare gli acquisti. Secondo il blog FRED della Fed di St. Louis, il rendimento del Treasury decennale salì da circa il 2% di maggio 2013 a circa il 3% di dicembre 2013; misurato sui punti estremi citati da S&P Global, il decennale passò dal 2,03% del 22 maggio al picco del 3,04% del 31 dicembre 2013. Per l'azionario l'effetto era ambiguo: dati forti segnalavano sia ritiro dello stimolo (negativo via tassi di sconto) sia economia in miglioramento (positivo via utili).

### 2.2 Normalizzazione e hiking graduale (2015–2018), picco hawkish fine 2018

Dopo il primo rialzo del dicembre 2015, la Fed entrò in un ciclo di rialzi graduali e prevedibili. In questo regime i dati su lavoro e inflazione contavano per la traiettoria attesa dei tassi, ma in modo ordinato. Il **picco hawkish** si ebbe a fine 2018: alla riunione del 19 dicembre 2018 Powell descrisse il roll-off del bilancio come destinato a proseguire senza modifiche ("I don't see us changing that"), indicando i tassi come lo strumento attivo della politica monetaria; questa percezione di un restringimento del bilancio "in modalità automatica" (autopilot) alimentò un forte sell-off azionario, con l'S&P 500 che a dicembre entrò in territorio di bear market con un calo del 20% su base intraday (CNBC). Il 4 gennaio 2019 Powell fece marcia indietro ("patient", "flexible"), innescando un violento rimbalzo. Significativamente, lo stesso 4 gennaio uscì un dato sul lavoro fortissimo: i nonfarm payroll di dicembre 2018 salirono di 312.000 unità, contro un consenso Dow Jones di 176.000. Quel dato non spaventò però il mercato, perché dominava il messaggio dovish della Fed: un esempio di come il regime di policy filtri la reazione al dato.

### 2.3 Shock COVID e ripartenza (2020–2021)

La pandemia ruppe la stagionalità e rese molti dati poco informativi. Le variazioni dei payroll furono di ordini di grandezza senza precedenti (crollo storico in primavera 2020, poi recuperi enormi), e il consenso degli economisti aveva errori giganteschi: la sorpresa misurata perdeva significato. Inoltre la procedura di destagionalizzazione del BLS andò in crisi: come documentato da Liberty Street Economics della Fed di New York ("Reasonable Seasonals? Seasonal Echoes in Economic Data after COVID-19", marzo 2021), il BLS passò da fattori stagionali "moltiplicativi" ad "additivi", trattando i mesi da marzo 2020 in poi come additive outlier; le distorsioni stimate sul livello dei payroll superavano in alcuni mesi i 100.000 posti ed erano "positive in primavera ed estate e negative in autunno e inverno". In questa fase i dati erano spesso "rumore" più che segnale, e i mercati reagivano più a vaccini, riaperture e politica fiscale/monetaria che alle singole release.

### 2.4 Shock inflazionistico e hiking aggressivo (2021–2023)

Con l'inflazione oltre l'obiettivo e la Fed in rialzo aggressivo, si instaurò il regime **"good news is bad news" per l'azionario**: un CPI più caldo del previsto innescava un repricing hawkish (più rialzi attesi), con azioni giù, rendimenti su e dollaro su. L'esempio classico è il CPI di agosto 2022 (pubblicato il 13 settembre 2022): l'inflazione headline uscì all'8,3% a/a contro attese di rallentamento (consenso Dow Jones di −0,1% m/m sul headline; core atteso +0,3% m/m ma uscito +0,6%). La reazione fu violenta: il Dow Jones chiuse in calo di oltre 1.200 punti (circa −2,6% / −3,9% a seconda dell'orario), nella peggiore seduta da giugno 2020. In questa fase la sensibilità dei mercati al CPI esplose: Kroner (2025, FEDS 2025-022) documenta che la reazione dei rendimenti alle sorprese CPI fu "più di un ordine di grandezza" (>10×) più forte nel periodo ad alta inflazione (maggio 2021–luglio 2023) rispetto al periodo a bassa inflazione (2009–maggio 2021), mentre la sensibilità alle altre release restò sostanzialmente invariata — un fenomeno attribuito all'attenzione degli investitori (investor attention).

### 2.5 Disinflazione e pivot atteso (2023–2024)

Con l'inflazione in calo, il focus del mercato tornò sul **lavoro** come segnale di atterraggio morbido vs duro. Il dato di luglio 2024 (pubblicato il 2 agosto 2024) è emblematico: i payroll salirono solo di 114.000 unità contro un consenso di circa 175.000 (FactSet), la disoccupazione salì dal 4,1% al 4,3%, e si attivò la **regola di Sahm** (media trimestrale del tasso di disoccupazione 0,5pp sopra il minimo dei 12 mesi precedenti; valore registrato 0,53pp). Seguì un forte sell-off azionario — secondo CNN Business, il Dow chiuse a −612 punti (−1,5%), l'S&P 500 a −1,8% e il Nasdaq a −2,4% — con rendimenti in calo. In questo regime una sorpresa debole sul lavoro non era più "buona" (meno rialzi) ma "cattiva" (rischio recessione): il segno della reazione si era ribaltato rispetto al 2022.

## 3. Meccanismi di trasmissione per asset

Per ogni dato-chiave la sorpresa si propaga attraverso canali distinti su curva dei Treasury, azionario, dollaro e oro.

### 3.1 Curva dei Treasury (front-end vs 10Y)

Il front-end (2 anni) prezza prevalentemente la traiettoria attesa della Fed; il 10 anni incorpora crescita, inflazione attesa e premio a termine. Balduzzi, Elton e Green (2001) trovano che 17 release hanno impatto significativo su bill a 3 mesi, note a 2 e 10 anni e bond a 30 anni, con effetti che variano per scadenza e aggiustamento entro un minuto dalla pubblicazione; le sorprese sui payroll muovono soprattutto le scadenze brevi e medie, mentre le sorprese sull'inflazione si propagano al tratto lungo. L'entità è quantificabile: Beechey e Wright (2007, FEDS 2007-05) stimano che, nel periodo pre-2021 (campione luglio 1991–settembre 2006), una sorpresa del core CPI di 1 punto percentuale muoveva il rendimento decennale di circa 19,7 bp e il biennale di circa 18,5 bp — cioè circa 2 bp sul 10 anni per una sorpresa di 0,1pp (deviazione standard storica della sorpresa core CPI ≈ 0,10pp). Per il lavoro, la Fed di San Francisco (2011) documenta che la risposta più forte alle sorprese sui payroll si ha intorno alla scadenza biennale (circa 7 bp, ovvero ~0,07pp, per una sorpresa di una deviazione standard), svanendo oltre i 6 anni; le sorprese core CPI hanno effetto minore (~1,5 bp) ma esteso anche al tratto lungo. È esattamente questo baseline a bassa inflazione che Kroner (2025) trova moltiplicato di oltre dieci volte nel regime 2021-2023.

- **CPI**: una sorpresa al rialzo alza i breakeven e/o i tassi reali e, via Taylor rule attesa, alza i rendimenti su tutta la curva, con front-end mosso dal repricing Fed e tratto lungo da inflazione attesa.
- **NFP**: una sorpresa forte sul lavoro alza front-end e tratto medio (più rialzi/meno tagli attesi); è storicamente il dato più potente — Andersen, Bollerslev, Diebold e Vega (2007) lo definiscono il "re" degli annunci (king of announcements). Una sorpresa di una deviazione standard sui payroll corrisponde a circa 90.000 posti (Kroner 2025); una sorpresa di 100.000 è quindi circa 1,1 deviazioni standard.
- **GDP/ISM**: sorprese di crescita muovono i rendimenti reali e il tratto medio della curva; l'ISM manifatturiero è un mover rilevante perché tempestivo e leading.

### 3.2 Azionario USA (effetto tassi di sconto vs effetto cash-flow)

Il prezzo di un'azione è il valore attuale dei flussi di cassa futuri scontati. Una sorpresa macro agisce su due canali opposti: l'**effetto cash-flow** (dati forti → utili attesi più alti → prezzi su) e l'**effetto tasso di sconto** (dati forti → tassi più alti → prezzi giù). Quale prevale dipende dal regime. Quando la Fed è aggressiva e il focus è sull'inflazione (2022), domina l'effetto tasso di sconto: "good news is bad news". Quando la crescita è il rischio principale (recessione o suo timore), domina l'effetto cash-flow: dati forti = azioni su. Questo è il meccanismo formalizzato da McQueen e Roley (1993) e Boyd, Hu e Jagannathan (2005), trattato nella sezione 4.

### 3.3 Dollaro (differenziale di tasso) e oro (tassi reali, safe haven)

**Dollaro**: il canale principale è il differenziale di tasso d'interesse. Una sorpresa macro USA positiva alza i rendimenti USA attesi e tende ad apprezzare il dollaro. Faust, Rogers, Wang e Wright (2007, *Journal of Monetary Economics*) documentano ad alta frequenza che per diverse sorprese reali un dato USA più forte del previsto apprezza immediatamente il dollaro.

**Oro**: l'oro non paga cedola, quindi il suo costo-opportunità sono i **tassi reali**. Sorprese che alzano i tassi reali (CPI caldo che spinge la Fed) tendono a deprimere l'oro; sorprese che segnalano rischio sistemico attivano la domanda di **bene rifugio**, che può sovrastare il canale dei tassi reali. La relazione inversa oro/tassi reali (correlazione storica spesso tra −0,5 e −0,8) si è infatti rotta nel 2022-2024, quando oro e tassi reali sono saliti insieme per acquisti delle banche centrali e tensioni geopolitiche.

## 4. State-dependence esplicita: la reazione dell'azionario al lavoro cambia segno

Il risultato più importante per un sistema di analogie storiche è che **il segno della reazione dell'azionario a una sorpresa sul lavoro cambia tra espansione e recessione**. McQueen e Roley (1993, *Review of Financial Studies*) mostrano che, tenendo conto delle fasi del ciclo, esiste una relazione molto più forte tra prezzi azionari e notizie macro di quanto la letteratura precedente avesse trovato: quando l'economia è forte, il mercato reagisce **negativamente** a notizie di maggiore attività reale, perché l'aumento dei tassi di sconto supera l'aumento dei flussi di cassa attesi.

Boyd, Hu e Jagannathan (2005, *Journal of Finance*) formalizzano questo per il dato sulla disoccupazione: in media un annuncio di **disoccupazione in aumento è "buona notizia" per le azioni durante le espansioni e "cattiva notizia" durante le recessioni**. La notizia sulla disoccupazione "impacchetta" tre informazioni: tassi futuri, premio per il rischio azionario, e utili/dividendi futuri. In espansione domina l'informazione sui tassi (disoccupazione su → tassi giù → azioni su); in recessione domina l'informazione sugli utili (disoccupazione su → utili giù → azioni giù). Andersen, Bollerslev, Diebold e Vega (2007) confermano questa dipendenza dallo stato del ciclo come spiegazione della bassa correlazione media stock-bond. Questo è esattamente il meccanismo che ha fatto ribaltare il segno tra il 2022 (sorpresa forte sul lavoro = azioni giù via tassi) e l'agosto 2024 (sorpresa debole sul lavoro = azioni giù via timori di crescita).

## 5. Asimmetrie e finestre temporali

**Velocità**: l'aggiustamento ai dati è quasi istantaneo. Balduzzi, Elton e Green (2001) trovano che l'impatto sui prezzi dei Treasury avviene entro un minuto dall'annuncio, con volatilità e volumi elevati e bid-ask spread che si allargano al momento del rilascio per poi rientrare in 5-15 minuti.

**Asimmetria up/down**: Andersen, Bollerslev, Diebold e Vega (2003) documentano un "sign effect" — la cattiva notizia ha impatto maggiore della buona notizia, in linea con la teoria del price discovery e dell'elaborazione dell'informazione. Nel regime ad alta inflazione, però, l'asimmetria per il CPI si inverte: Sahin et al. ("Asymmetric S&P 500 reactions to CPI surprises in a high-inflation environment", *Applied Economics Letters*, 2026; campione 2021-2025) trovano che le sorprese positive (CPI sotto le attese, cioè disinflazionistiche) generano rendimenti anomali cumulati ampi e statisticamente significativi (CAR oltre l'1% in tutte le finestre), mentre le sorprese negative (CPI sopra le attese) producono cali di magnitudine simile ma non statisticamente significativi.

**Persistenza vs attenuazione**: l'effetto sui rendimenti e sul cambio tende a essere permanente (un repricing dei fondamentali), mentre la componente di volatilità si attenua in pochi minuti/ore. Su finestre più lunghe (T+1, T+5) l'effetto della singola sorpresa si confonde con il flusso di notizie successivo e con eventuali revisioni dei dati (i payroll sono soggetti a revisioni rilevanti, come visto con le ampie revisioni al ribasso del 2024). Per un event study, la finestra intraday (5-60 minuti) isola meglio l'effetto causale; finestre giornaliere o plurigiornaliere catturano anche reazioni di secondo ordine e contaminazioni.

## 6. Cosa NON trasferire tra regimi

Per un sistema che mappa notizie correnti a episodi storici, alcuni elementi sono **irripetibili** e rendono rischioso usare un episodio di un regime come analogo per un altro:

- **Rotture COVID (2020-2021)**: l'ampiezza abnorme dei payroll, le rotture di stagionalità e gli errori di consenso rendono le sorprese di quel periodo non comparabili. Il passaggio del BLS da fattori stagionali moltiplicativi ad additivi (Liberty Street Economics, 2021) ha introdotto discontinuità metodologiche.
- **Cambi di regime di policy**: un dato forte sotto ZIRP/forward guidance (2013) significa "tapering più vicino" (bad news for bonds); lo stesso dato in piena disinflazione con pivot atteso (2024) significa "atterraggio morbido confermato" (potenzialmente good news per equity). Il segno della reazione dell'azionario al lavoro è esplicitamente diverso tra espansione e recessione (Boyd, Hu e Jagannathan 2005), quindi un analogo storico va selezionato condizionando sul punto del ciclo, non solo sul tipo e segno della sorpresa.
- **Effetti di livello dei tassi**: vicino allo zero lower bound i canali di trasmissione cambiano (la curva non può scendere oltre certi livelli; la forward guidance e il QE diventano i margini attivi). Episodi ZLB non sono analoghi puliti per episodi a tassi elevati.
- **Mutamenti dell'attenzione**: la sensibilità al CPI è esplosa nel 2021-2023 per ragioni di attenzione (Kroner 2025) ed è destinata a normalizzarsi con il rientro dell'inflazione; usare l'elasticità CPI→rendimenti del 2022 (oltre dieci volte quella pre-2021) per un regime a bassa inflazione sovrastimerebbe enormemente la reazione.

## 7. Rassegna dei paper fondanti

- **Andersen, Bollerslev, Diebold & Vega (2003), *American Economic Review* 93(1):38-62** — "Micro effects of macro announcements: Real-time price discovery in foreign exchange". Dimostra, con dati FX ad alta frequenza, che le sorprese macro producono salti nella media condizionata e che la reazione è asimmetrica (la cattiva notizia pesa più della buona).
- **Andersen, Bollerslev, Diebold & Vega (2007), *Journal of International Economics* 73(2):251-277** — "Real-time price discovery in global stock, bond and foreign exchange markets". Estende l'analisi a azioni, bond e FX; mostra che l'azionario reagisce diversamente alle notizie a seconda della fase del ciclo economico, razionalizzando la bassa correlazione media stock-bond tramite l'alternanza degli effetti cash-flow e tasso di sconto. Identifica i nonfarm payroll come il dato più significativo per tutti i mercati ("re" degli annunci).
- **Balduzzi, Elton & Green (2001), *Journal of Financial and Quantitative Analysis* 36(4):523-543** — "Economic News and Bond Prices: Evidence from the U.S. Treasury Market". Usa dati intraday del mercato interdealer; identifica 17 release significative sui Treasury, mostra che gli effetti variano per scadenza, che i payroll muovono soprattutto le scadenze brevi/medie mentre l'inflazione colpisce il tratto lungo, e che l'aggiustamento avviene entro un minuto.
- **Boyd, Hu & Jagannathan (2005), *Journal of Finance* 60(2):649-672** — "The Stock Market's Reaction to Unemployment News: Why Bad News Is Usually Good for Stocks". Dimostra che l'annuncio di disoccupazione in aumento è buona notizia per le azioni in espansione e cattiva in recessione, perché l'informazione sui tassi domina in espansione e quella sugli utili in recessione.
- **McQueen & Roley (1993), *Review of Financial Studies* 6(3):683-707** — "Stock Prices, News, and Business Conditions". Mostra che, condizionando sullo stato dell'economia, la relazione tra prezzi azionari e notizie macro è molto più forte; con economia forte il mercato reagisce negativamente a notizie di maggiore attività reale (effetto tasso di sconto > effetto cash-flow).
- **Gürkaynak, Sack & Swanson (2005), *International Journal of Central Banking*** — "Do Actions Speak Louder than Words? The Response of Asset Prices to Monetary Policy Actions and Statements". Mostra che la politica monetaria ha due dimensioni: un fattore "target" (sorpresa sul tasso corrente) e un fattore "path" (sorpresa sulla traiettoria attesa); il fattore path, legato ai comunicati FOMC, spiega gran parte dei movimenti dei tassi a lungo termine. (Gli stessi autori, in un paper gemello del 2005 sull'*American Economic Review*, mostrano che i tassi forward a lungo termine reagiscono alle sorprese macro, contrariamente ai modelli standard.)
- **Nakamura & Steinsson (2018), *Quarterly Journal of Economics* 133(3):1283-1330** — "High-Frequency Identification of Monetary Non-Neutrality: The Information Effect". Identifica gli effetti della politica monetaria nella finestra di 30 minuti attorno agli annunci FOMC; documenta il "Fed information effect": a un rialzo dei tassi seguono revisioni al rialzo delle previsioni di crescita, segno che gli annunci Fed trasmettono informazione sui fondamentali oltre che sulla policy.
- **Bauer & Swanson (2023), *NBER Macroeconomics Annual* vol. 37** — "A Reassessment of Monetary Policy Surprises and High-Frequency Identification". Rilegge il Fed information effect: la correlazione tra sorprese di policy e dati macro precedenti non richiede informazione privata della Fed, ma si spiega col canale "Fed response to news" (il pubblico sottostima quanto la Fed reagirà ai dati). Trova scarsa evidenza di information effect su survey, azioni e cambi.
- **Faust, Rogers, Wang & Wright (2007), *Journal of Monetary Economics* 54(4):1051-1068** — "The high-frequency response of exchange rates and interest rates to macroeconomic announcements". Studia il movimento congiunto di cambi e strutture a termine USA/estere attorno alle release macro; per diverse sorprese reali un dato USA più forte del previsto apprezza immediatamente il dollaro, con implicazioni su premi a termine e premi al rischio di cambio.

Fonti complementari rilevanti: Beechey & Wright (2007, FEDS 2007-05) per le ampiezze pre-2021 delle reazioni dei rendimenti al core CPI; Kroner (2025, FEDS 2025-022) per l'aumento di oltre un ordine di grandezza della sensibilità al CPI nel 2021-2023 e il ruolo dell'investor attention; Liberty Street Economics (Fed di New York, 2021) per le distorsioni di destagionalizzazione post-COVID.

## 8. Implicazioni per un sistema di event study basato su analogie storiche

1. **Indicizzare per regime, non solo per dato**: ogni episodio storico va etichettato con (a) regime di policy (ZIRP/QE, hiking, hold, tagli/pivot), (b) posizione nel ciclo (espansione vs recessione/timore), (c) regime di inflazione (alta vs bassa). Un CPI caldo nel 2022 e un CPI caldo nel 2015 non sono analoghi.
2. **Condizionare il segno equity sullo stato del ciclo**: applicare il risultato Boyd-Hu-Jagannathan/McQueen-Roley come regola di selezione: in espansione/regime hawkish la sorpresa forte sul lavoro è "cattiva" per le azioni via tassi; in recessione/timore una sorpresa debole è "cattiva" via crescita, e una sorpresa debole è "buona" solo se domina l'aspettativa di tagli.
3. **Pesare per attenzione**: la stessa sorpresa CPI ha avuto elasticità su rendimenti oltre dieci volte maggiore nel 2021-2023 (Kroner 2025). Le elasticità storiche vanno scalate per il regime di attenzione/inflazione corrente.
4. **Preferire finestre intraday per l'identificazione**: l'effetto causale pulito è nei primi minuti/ora; finestre T+1/T+5 introducono contaminazione e revisioni.
5. **Escludere o trattare separatamente gli episodi COVID**: rotture di stagionalità e ampiezze abnormi li rendono outlier non trasferibili.

## Avvertenze e limiti

- **Fatti vs interpretazioni**: i risultati dei paper accademici citati (segno state-dependent, jump istantanei, asimmetria, fattori target/path) sono fatti supportati da dati. Le narrazioni sui singoli episodi (es. "il mercato ha prezzato X") derivano da cronache di mercato e vanno trattate come interpretazioni.
- **Numeri puntuali**: le ampiezze citate (es. ~2 bp sul 10Y per 0,1pp di sorpresa core CPI pre-2021, da Beechey-Wright 2007; ~7 bp sul forward biennale per 1 dev. std. di sorpresa payroll, da Fed di San Francisco 2011) provengono da stime econometriche su campioni specifici e non sono costanti universali: variano per campione, finestra e regime. I coefficienti precisi delle tabelle di Balduzzi-Elton-Green (2001) e Andersen et al. (2003/2007) non sono stati estratti dal testo accessibile (tabelle paywalled): per quei valori puntuali si rimanda ai PDF originali.
- **CESI**: utile come misura aggregata del momentum delle sorprese, ma nato per il FX e con debole potere segnaletico sull'azionario; da non usare come predittore direzionale di equity.
- **Revisioni dei dati**: payroll e GDP sono soggetti a revisioni significative; la "sorpresa" del giorno del rilascio può essere smentita da revisioni successive, il che limita la trasferibilità di singoli episodi.
- **Perimetro temporale**: il documento copre il periodo 2013-2024; riferimenti a eventi 2025-2026 emersi in alcune fonti consultate non sono inclusi nel perimetro analitico.

```yaml
---
title: "Sorprese sui dati macro USA e trasmissione ai mercati (2013–2024): regimi, canali e state-dependence"
date_compiled: 2026-06-04
primary_theme: macro_data
sub_themes: [inflation_surprises, cpi, ppi, pce, labor_market, nfp, payrolls, jobless_claims, claims, ism, pmi, retail_sales, monetary_policy, yield_curve, dollar_dynamics, state_dependence]
relevant_assets:
  - ^GSPC
  - ^TNX
  - IEF
  - EURUSD=X
  - JPY=X
  - GC=F
external_assets_mentioned:
  - "Citi Economic Surprise Index (CESI) — non in DB, indice di sorpresa"
  - "2Y Treasury / front-end della curva — non in DB (in DB solo ^TNX 10Y e IEF 7-10Y)"
  - "DXY dollar index — non in DB (proxy: EURUSD=X, JPY=X)"
  - "Fed funds futures / OIS — non in DB"
time_window:
  start: 2013-01-01
  end: 2024-12-31
regime_phases:
  - zirp_forward_guidance_taper: 2013-01-01 to 2015-11-30
  - gradual_normalization_to_2018_peak: 2015-12-01 to 2019-07-31
  - covid_shock_and_reopening: 2020-02-01 to 2021-02-28
  - inflation_shock_aggressive_hiking: 2021-03-01 to 2023-07-31
  - disinflation_and_pivot_expectations: 2023-08-01 to 2024-12-31
keywords:
  - macro surprise
  - economic surprise index
  - citi surprise index
  - cpi
  - pce
  - non-farm payrolls
  - nfp
  - employment situation
  - unemployment rate
  - jolts
  - ism
  - pmi
  - gdp
  - retail sales
  - treasury yields
  - yield curve
  - 10-year yield
  - federal reserve
  - fomc
  - dot plot
  - forward guidance
  - taper tantrum
  - good news is bad news
  - state dependence
  - business cycle
  - announcement effect
  - high-frequency identification
  - fed information effect
  - dollar
  - real rates
  - safe haven
  - soft landing
  - hard landing
---
```