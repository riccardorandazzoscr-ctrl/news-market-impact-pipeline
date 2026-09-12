# Glossario — sigle e termini

Definizioni valide per **tutte** le schede del giorno. `render_report.py` mette
questa sezione una sola volta, in fondo al report; ogni scheda rimanda qui con
un link invece di ripetere le definizioni.

Se in una scheda usi un termine o un ticker che **non trovi qui sotto**,
aggiungilo — una riga, nella sezione più adatta, in ordine alfabetico al suo
interno — invece di definirlo nella scheda. Così la prossima scheda lo trova
già pronto.

## Metodo statistico

- **Deviazione standard / dispersione** — quanto i singoli episodi si allontanano dalla mediana. Quando è molto più grande della mediana stessa, il segno storico è debole anche se "torna" nella direzione giusta.
- **Event study** — misura sistematica di come si muove un asset nei giorni attorno a episodi storici comparabili a quello di oggi.
- **Hit rate** — quota di episodi in cui il segno del rendimento realizzato ha rispettato il segno atteso dal pool storico.
- **IC (Information Coefficient)** — correlazione di rango fra direzione prevista e rendimento realizzato; è la metrica che la scorecard usa per dire se il segno storico di un asset è affidabile.
- **Look-ahead bias** — usare, nel valutare un episodio storico, informazioni che a quella data non erano ancora disponibili. L'event study del progetto lo esclude per costruzione.
- **Media** — sensibile ai casi estremi: un singolo episodio anomalo può spostarla parecchio. Quando media e mediana hanno segno opposto, la media non è utilizzabile.
- **Mediana** — il valore centrale del campione di episodi: metà sta sopra, metà sotto. Più robusta della media sui campioni piccoli.
- **N** — numero di episodi storici nel campione. Con N<10 il risultato è **indicative only**.
- **p25 / p75** — 25° e 75° percentile: delimitano la metà centrale degli episodi. Una banda molto più larga della mediana segnala dispersione alta.
- **Punto base (bp)** — un centesimo di punto percentuale (0,01%).
- **Regime (storico/macro)** — la fase di mercato (tassi in salita, dollaro forte, ecc.) in cui un episodio è avvenuto. Episodi di regimi diversi non vanno mescolati nello stesso campione.
- **T+1 / T+3 / T+5 / T+10 (T+N)** — giorni di **borsa** dopo l'evento, non giorni di calendario. I rendimenti sono **cumulati** dal giorno dell'evento, non giornalieri.

## Dati macro e banche centrali

- **ADP** — indagine mensile sull'occupazione privata USA; anticipa di due giorni l'NFP ufficiale.
- **BCE (Banca Centrale Europea)** — fissa i tassi per i venti paesi dell'area euro. Il tasso sui depositi è quello che riconosce alle banche sui fondi depositati presso di essa.
- **Consenso** — media delle previsioni degli analisti prima di una release; la "sorpresa" è la differenza fra dato pubblicato e consenso. Fornitori diversi (Reuters, Bloomberg, Wind) pubblicano consensi diversi.
- **Core (inflazione di fondo)** — l'inflazione esclusi energia e alimentari freschi, perché quelle voci sono volatili e guidate da fattori esterni; il core misura meglio la pressione generata dall'economia interna.
- **CPI (Consumer Price Index)** — indice dei prezzi al consumo, la misura di inflazione percepita dalle famiglie.
- **Destatis** — l'istituto federale di statistica tedesco.
- **Dot plot** — il grafico a punti in cui ogni membro del comitato Fed indica anonimamente dove vede i tassi negli anni successivi. Non è un impegno, ma è il segnale di guidance più seguito.
- **Fed / Federal Reserve** — la banca centrale degli Stati Uniti.
- **Flash estimate (stima flash)** — la prima pubblicazione, rapida e provvisoria, di un dato di inflazione; viene rivista in seguito con il dato definitivo.
- **FOMC (Federal Open Market Committee)** — il comitato della Fed che decide i tassi; si riunisce otto volte l'anno.
- **Forward guidance** — l'indicazione che una banca centrale dà sul percorso futuro dei tassi, per orientare le aspettative del mercato senza agire subito.
- **Funzione di reazione** — il modo sistematico in cui una banca centrale risponde ai dati in arrivo.
- **GDP / PIL** — prodotto interno lordo: il valore di tutti i beni e servizi prodotti. "Annualizzato" = il tasso di crescita che si otterrebbe se il ritmo del trimestre proseguisse per un anno intero.
- **Headline** — l'inflazione totale, energia e alimentari inclusi (si contrappone al **core**).
- **HICP (Harmonised Index of Consumer Prices)** — l'indice armonizzato dei prezzi al consumo usato dalla BCE, costruito con la stessa metodologia in tutti i paesi dell'area euro.
- **ISM (Institute for Supply Management)** — indice USA di diffusione su manifattura/servizi da sondaggio ai responsabili acquisti. Sopra 50 = espansione, sotto 50 = contrazione; misura **quanti** rispondono che l'attività cresce, non **di quanto**.
- **JOLTS (Job Openings and Labor Turnover Survey)** — indagine mensile USA sui posti di lavoro vacanti e sul turnover, complementare all'NFP.
- **NFP (Non-Farm Payrolls)** — nuovi posti di lavoro creati negli USA, esclusa l'agricoltura; il dato macro più seguito al mondo.
- **PBOC (People's Bank of China)** — la banca centrale cinese.
- **PMI (Purchasing Managers' Index)** — indice da sondaggio ai responsabili acquisti; sopra 50 = espansione, sotto 50 = contrazione. Indicatore anticipatore.
- **PPI (Producer Price Index)** — indice dei prezzi alla produzione.
- **Produzione industriale** — indice del volume fisico prodotto da industria, costruzioni ed energia; volatile e pubblicato con oltre un mese di ritardo.
- **QE (Quantitative Easing) / QT (Quantitative Tightening)** — acquisto di titoli da parte della banca centrale per abbassare i tassi a lunga (QE) e il processo inverso di riduzione del bilancio (QT).
- **RBNZ (Reserve Bank of New Zealand)** — la banca centrale neozelandese; storicamente la prima al mondo ad adottare un obiettivo d'inflazione esplicito (1990) e spesso in anticipo sul ciclo delle banche centrali maggiori.
- **Sorpresa macro** — la differenza fra il dato pubblicato e il consenso degli analisti; è la sorpresa, non il livello, a muovere i prezzi.
- **TPI (Transmission Protection Instrument)** — lo "scudo anti-spread" della BCE contro un allargamento ingiustificato dei differenziali sovrani nell'area euro.
- **YCC (Yield Curve Control)** — controllo della curva dei rendimenti: politica con cui una banca centrale (tipicamente la BoJ) fissa un tetto al rendimento di un titolo di Stato comprandone quantità illimitate per difenderlo.

## Mercati e meccanismi

- **Bear flattening** — appiattimento della curva dei rendimenti causato dai tassi brevi che salgono più dei lunghi; è la firma di una stretta monetaria ritenuta credibile: si stringe ora, quindi l'inflazione di lungo periodo attesa scende.
- **Bear steepening** — irripidimento della curva dei rendimenti causato dai tassi lunghi che salgono più dei brevi; segnala rischio fiscale o di inflazione, non attese di stretta immediata.
- **Beta** — la sensibilità di un asset ai movimenti del suo mercato di riferimento. Un beta alto amplifica i movimenti in entrambe le direzioni.
- **Capex (Capital Expenditure)** — la spesa in conto capitale: investimenti in beni durevoli (impianti, macchinari, data center).
- **Carry trade** — indebitarsi in una valuta a basso tasso per investire in attività denominate in valute a tasso più alto. Funziona finché il differenziale resta ampio e il cambio stabile; si smonta violentemente quando una delle due condizioni cade.
- **Chokepoint** — collo di bottiglia della logistica marittima o energetica (Hormuz, Suez, Malacca, Bab el-Mandeb): un'interruzione locale ha effetti globali.
- **Curva dei rendimenti** — il grafico dei rendimenti per scadenza (2, 5, 10, 30 anni). Si irripidisce quando le scadenze lunghe salgono più delle corte.
- **Differenziale di tasso** — la differenza fra i rendimenti di due aree valutarie; principale motore dei flussi di capitale e quindi dei cambi.
- **Disinflazione** — rallentamento del *tasso di crescita* dei prezzi, non un calo dei prezzi (quello è deflazione).
- **Duration** — la sensibilità del prezzo di un'obbligazione a una variazione dei rendimenti. Scadenza più lunga = duration maggiore = movimento di prezzo più violento.
- **Effetti di secondo round** — il passaggio di uno shock di prezzo (es. energia) a salari e poi di nuovo a prezzi, che rischia di renderlo persistente invece che temporaneo.
- **Fixing** — il cambio di riferimento che una banca centrale (es. PBOC per lo yuan) pubblica ogni mattina come ancora per le oscillazioni consentite in giornata.
- **Guidance (aziendale)** — la previsione che un'azienda fornisce sui propri risultati futuri.
- **Hyperscaler** — i grandi operatori cloud (Amazon, Microsoft, Google, Meta) che costruiscono data center su scala mondiale; i principali clienti del capex AI.
- **LDI (Liability-Driven Investment)** — strategia con cui i fondi pensione britannici usano derivati sui Gilt per coprire le passività future; il crollo dei Gilt nel 2022 generò richieste di margine a catena.
- **Pass-through** — la quota dell'aumento di un costo (es. dazio, materia prima) che arriva al prezzo finale pagato dal consumatore.
- **Lock-in (mercato immobiliare)** — l'effetto per cui chi ha un mutuo acceso a tasso basso rinuncia a vendere casa per non perderlo. Prosciuga l'offerta di abitazioni esistenti e sostiene i prezzi e gli affitti, cioè la componente più pesante dell'inflazione core.
- **Premio a termine (term premium)** — il compenso extra richiesto per detenere un titolo a lunga scadenza invece di rinnovare titoli brevi. Cresce con l'incertezza sull'inflazione, l'offerta di debito e il ritiro dei compratori strutturali.
- **Premio di rischio (geopolitico)** — la componente del prezzo di una materia prima che non riflette domanda e offerta correnti, ma la probabilità percepita di una futura interruzione dell'offerta. Si "sgonfia" quando quella probabilità scende, anche senza che nulla cambi fisicamente.
- **Rendimento (yield)** — quanto rende un titolo di Stato tenuto fino a scadenza; si muove in direzione **opposta** al prezzo.
- **Shock di offerta** — un rincaro che nasce da una riduzione della disponibilità di un bene, non da un eccesso di domanda. Alzare i tassi non lo corregge: riduce solo la crescita.
- **Spare capacity (capacità inutilizzata)** — capacità produttiva che i produttori (soprattutto OPEC+) possono attivare in poche settimane; l'ammortizzatore che storicamente drena il premio di rischio sul petrolio.
- **State-dependence** — il fatto che la reazione del mercato allo stesso dato dipenda dallo stato del sistema (fase del ciclo monetario, posizionamento, regime inflazionistico).
- **Surplus commerciale** — l'eccedenza delle esportazioni sulle importazioni di un paese. Per identità contabile, il surplus di uno è il deficit di altri.
- **Tasso di sconto** — il tasso usato per attualizzare gli utili futuri di un'azienda: se sale, gli utili lontani nel tempo valgono meno oggi.
- **Tasso reale / tassi reali** — il tasso d'interesse al netto dell'inflazione attesa; è il costo-opportunità di detenere oro, che non produce reddito.
- **Vol crush** — il calo brusco della volatilità implicita subito dopo un evento atteso (una decisione di banca centrale, una pubblicazione di dati): l'incertezza si risolve e il premio pagato per proteggersi si sgonfia, a prescindere dall'esito.

## Geopolitica e istituzioni

- **CENTCOM** — United States Central Command, il comando militare USA competente per Medio Oriente e Asia centrale.
- **Corridoio del Mar Nero** — la rotta marittima per l'export cerealicolo ucraino; oggetto di accordi e sospensioni dal 2022.
- **Flotta ombra** — petroliere anziane, con proprietà opaca e assicurazioni non occidentali, usate per trasportare greggio russo aggirando il tetto al prezzo.
- **G20** — foro dei ministri delle finanze e governatori delle banche centrali delle venti maggiori economie.
- **Guerra ibrida** — azioni ostili sotto la soglia del conflitto aperto (sabotaggi, droni, attacchi informatici), tipicamente non rivendicate.
- **JCPOA (Joint Comprehensive Plan of Action)** — l'accordo del 2015 sul programma nucleare iraniano, da cui gli USA uscirono nel 2018.
- **NATO** — North Atlantic Treaty Organization, l'alleanza militare atlantica.
- **Patriot** — sistema americano di difesa antiaerea e antimissile.
- **Sezione 301** — norma del diritto commerciale USA usata dal 2018 per imporre dazi sulla base di pratiche commerciali giudicate sleali.
- **Stretto di Hormuz** — braccio di mare fra Iran e Oman da cui transita circa il 20% del petrolio scambiato via mare; il principale chokepoint energetico mondiale.
- **Tagli volontari (OPEC+)** — riduzioni di produzione annunciate da singoli membri (soprattutto Arabia Saudita) oltre le quote formali del gruppo, e quindi revocabili unilateralmente.
- **Terre rare** — 17 elementi indispensabili a magneti permanenti, motori elettrici, ottiche militari e semiconduttori. La Cina non ha il monopolio dell'estrazione ma sì, di fatto, quello della raffinazione.

## Materie prime, dazi e unità

- **Crack spread 3-2-1 (`CRACK_321`)** — il margine lordo di una raffineria: il valore di 2 barili di benzina + 1 di distillato meno il costo di 3 barili di greggio. Sale quando i prodotti raffinati sono scarsi rispetto al greggio. Serie *derivata*, calcolata e salvata come ticker nel DB del progetto.
- **Dazio (tariffa)** — imposta su un bene importato; ne aumenta il prezzo per l'acquirente domestico.
- **DRAM / NAND / HBM** — tipi di memoria per computer. DRAM = memoria volatile di sistema; NAND = memoria di archiviazione permanente (SSD); HBM (High Bandwidth Memory) = memoria ad altissima banda per acceleratori AI, il segmento a margine più alto.
- **GNL** — gas naturale liquefatto: gas raffreddato a −162°C per essere trasportato via nave invece che via gasdotto.
- **OPEC+** — l'OPEC (Organization of the Petroleum Exporting Countries) allargata a un gruppo di produttori non-OPEC guidato dalla Russia.
- **Staio (bushel)** — unità di misura dei cereali americani, circa 27 kg per il grano; i futures su grano e mais sono quotati in cent per bushel — leggere le variazioni %, mai i livelli.

## Ticker e asset

- **1482.T** — ETF quotato a Tokyo su titoli di Stato giapponesi (JGB). È un **prezzo**: scende quando i rendimenti salgono.
- **^AXJO** — indice azionario ASX 200 (Australia).
- **AUD=X** — cambio USD/AUD. ⚠ Sale quando il **dollaro australiano si indebolisce**.
- **BRL=X** — cambio dollaro/real brasiliano. Sale quando il real si indebolisce.
- **BTC-USD / ETH-USD** — Bitcoin ed Ethereum; usati nel progetto come proxy del tema "digital gold" (risk-off) e del tema digitale/AI.
- **BTP_BUND_SPREAD** — differenziale di rendimento fra BTP italiano e Bund tedesco a 10 anni; misura diretta del rischio sovrano periferico. Serie *derivata*, salvata come ticker.
- **BZ=F** — futures sul Brent, il contratto di riferimento mondiale sul petrolio greggio (quotato a Londra).
- **CAD=X** — cambio USD/CAD. ⚠ Sale quando il **dollaro canadese si indebolisce**.
- **CHF=X** — cambio USD/CHF. Sale quando il franco svizzero si indebolisce. Il franco è un safe haven monetario.
- **CNY=X** — cambio USD/CNY (yuan onshore). ⚠ Sale quando lo **yuan si indebolisce**; compresso dal fixing giornaliero della PBOC.
- **CQQQ** — ETF Invesco China Technology; storia dal 2011.
- **DX-Y.NYB** — dollar index: il dollaro USA contro un paniere di valute principali.
- **EEM** — ETF iShares MSCI Emerging Markets.
- **EIDO** — ETF azionario Indonesia.
- **EURUSD=X** — cambio euro/dollaro: sale quando l'euro si rafforza.
- **EWS** — ETF azionario Singapore.
- **EWT** — ETF azionario Taiwan; proxy diretto del rischio Taiwan-Cina (TSMC, semiconduttori avanzati).
- **EWY** — ETF azionario Corea del Sud, concentrato su Samsung Electronics e SK Hynix; epicentro memoria/HBM per il ciclo AI.
- **EWZ** — ETF azionario Brasile.
- **EXH9.DE** — ETF settoriale sulle utility europee (Francoforte); proxy del prezzo dell'elettricità EU.
- **EXV7.DE** — ETF settoriale sulla chimica europea (Francoforte); energivora e dipendente dai trasporti sul Reno.
- **FTSEMIB.MI** — indice FTSE MIB, le 40 maggiori società italiane.
- **^GDAXI** — indice DAX, le 40 maggiori società quotate tedesche.
- **GBPUSD=X** — cambio sterlina/dollaro.
- **GC=F** — futures sull'oro (COMEX); il safe haven principale.
- **GDX** — ETF sui minatori auriferi; beta ~1,6 sull'oro (GC=F), lo amplifica. In risk-off spesso più informativo del metallo stesso.
- **^GSPC** — S&P 500.
- **^GSPTSE** — indice S&P/TSX Composite, il principale indice azionario canadese.
- **HG=F** — futures sul rame (COMEX); termometro della crescita industriale globale.
- **HO=F** — futures NYMEX sul gasolio da riscaldamento (*heating oil*), riferimento per l'intera famiglia dei distillati medi, diesel incluso.
- **HYG** — ETF su obbligazioni high yield USA; primo termometro dello stress sul credito.
- **IDR=X** — cambio dollaro/rupia indonesiana.
- **IEAG.AS** — ETF iShares Core Euro Aggregate Bond (prezzo); proxy duration eurozona.
- **IEF** — ETF iShares 7-10 Year Treasury Bond (prezzo); proxy duration USA.
- **IGLT.L** — ETF quotato a Londra su Gilt UK. È un **prezzo**: scende quando i rendimenti salgono.
- **IGV** — ETF sul software; proxy per single-name e per la rotazione interna al tema AI (letto insieme a SOXX).
- **ILS=X** — cambio dollaro/shekel israeliano. Sale quando lo shekel si indebolisce; canale più diretto del conflitto mediorientale.
- **INDA** — ETF azionario India.
- **INR=X** — cambio dollaro/rupia indiana.
- **ITA** — ETF sulla difesa e aerospazio USA (separa l'impulso americano da quello europeo di SHLD.L).
- **IWM** — ETF sull'indice Russell 2000 delle small cap USA; reagisce al tratto breve della curva più dell'indice per il maggior debito a tasso variabile. Il segnale è nello spread IWM/^GSPC, non nel livello.
- **IYT** — ETF sui trasporti USA (ferrovie, camion, corrieri, aeree): il carburante è un costo diretto.
- **JGB** — Japanese Government Bond, il titolo di Stato giapponese (proxy: `1482.T`).
- **JPY=X** — cambio USD/JPY. ⚠ Sale quando lo **yen si indebolisce**. Lo yen è un safe haven monetario.
- **KOSPI** — l'indice azionario principale della Corea del Sud.
- **KRW=X** — cambio USD/KRW. ⚠ Sale quando il **won si indebolisce**.
- **KWEB** — ETF KraneShares CSI China Internet (Alibaba, PDD, JD, Meituan); proxy del consumo interno cinese via e-commerce.
- **LIT** — ETF su litio e batterie; tema transizione energetica.
- **MYR=X** — cambio dollaro/ringgit malese.
- **^MOVE** — indice ICE BofA della volatilità implicita sulle opzioni su Treasury; l'equivalente obbligazionario del VIX.
- **^N225** — indice Nikkei 225, il principale indice azionario giapponese.
- **^NDX** — Nasdaq-100: 100 titoli tecnologici e growth, molto sensibili al tasso di sconto.
- **NOK=X** — cambio dollaro/corona norvegese; la corona è una valuta petrolifera.
- **NZD=X** — cambio dollaro/dollaro neozelandese.
- **RB=F** — futures sulla benzina RBOB (*Reformulated Blendstock for Oxygenate Blending*), il contratto benzina americano.
- **REMX** — ETF su terre rare e metalli strategici.
- **SEK=X** — cambio dollaro/corona svedese.
- **SGD=X** — cambio dollaro/dollaro di Singapore.
- **SHLD.L** — ETF su difesa e sicurezza globale, forte esposizione NATO/Europa (separa l'impulso europeo da quello USA di ITA).
- **SOXX** — ETF iShares Semiconductor, indice dei semiconduttori USA; cuore del tema AI/chip.
- **^STOXX50E** — indice Euro Stoxx 50, le 50 maggiori società dell'area euro.
- **TAN** — ETF sul solare; tema transizione energetica.
- **THB=X** — cambio dollaro/baht thailandese.
- **THD** — ETF azionario Thailandia.
- **^TNX / ^FVX / ^TYX** — rendimenti del Treasury USA rispettivamente a 10, 5 e 30 anni. Sono **rendimenti**, non prezzi: salgono quando i tassi salgono.
- **TTF=F** — futures sul gas naturale al Title Transfer Facility olandese; canale diretto del gas europeo. ⚠ Scorecard: segno storico non affidabile (vedi `leggere_lo_scorecard.md`).
- **URA** — ETF su uranio e nucleare; tema transizione energetica.
- **VGB.AX** — ETF quotato a Sydney su titoli di Stato australiani (ACGB). È un **prezzo**: scende quando i rendimenti salgono.
- **^VIX** — indice CBOE della volatilità implicita a 30 giorni sull'S&P 500, detto "indice della paura"; sale quando il mercato compra protezione.
- **WTI** — West Texas Intermediate, il greggio di riferimento americano; tipicamente più legato alle scorte interne USA che ai flussi marittimi (a differenza del Brent).
- **XLE** — ETF sul settore energetico azionario USA.
- **XLP** — ETF su beni di prima necessità USA (consumo difensivo).
- **XLU** — ETF sulle utility USA; proxy del vincolo elettrico del capex AI (letto insieme a SOXX).
- **XLV** — ETF sul settore sanitario/farmaceutico USA.
- **XLY** — ETF sul consumo discrezionale USA; dominato da Amazon/Tesla, correla 0,89 con ^GSPC — leggerlo insieme a XRT, mai da solo.
- **XRT** — ETF sul retail USA, pesi distribuiti; migliore di XLY per un singolo rivenditore.
- **ZC=F** — futures sul mais (*corn*) al Chicago Board of Trade.
- **ZW=F** — futures sul grano (*wheat*) al Chicago Board of Trade; il più esposto all'export ucraino/russo (canale Mar Nero).
