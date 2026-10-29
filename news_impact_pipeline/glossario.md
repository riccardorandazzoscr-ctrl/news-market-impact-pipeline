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
- **Giorno-ancora (T=0)** — il primo giorno di borsa con dati alla data dell'evento o dopo: da lì partono i rendimenti T+N. Per un evento di sabato o domenica è il lunedì, quindi la reazione del primo giorno di contrattazione non entra nelle tabelle: l'event study misura il *seguito*, non lo scatto iniziale. Due eventi con lo stesso giorno-ancora contano una volta sola.
- **Hit rate** — quota di episodi in cui il segno del rendimento realizzato ha rispettato il segno atteso dal pool storico.
- **IC (Information Coefficient)** — correlazione di rango (Spearman) fra la mediana prevista e il rendimento realizzato: dice se le previsioni più sbilanciate corrispondono a movimenti reali più grandi, non se il segno è giusto o sbagliato. Diversa dall'hit rate — le due possono divergere — la scorecard le riporta entrambe.
- **Look-ahead bias** — usare, nel valutare un episodio storico, informazioni che a quella data non erano ancora disponibili. L'event study del progetto lo esclude per costruzione.
- **Media** — sensibile ai casi estremi: un singolo episodio anomalo può spostarla parecchio. Quando media e mediana hanno segno opposto, la media non è utilizzabile.
- **Mediana** — il valore centrale del campione di episodi: metà sta sopra, metà sotto. Più robusta della media sui campioni piccoli.
- **N** — numero di episodi storici nel campione. Con N<10 il risultato è **indicative only**.
- **p25 / p75** — 25° e 75° percentile: delimitano la metà centrale degli episodi. Una banda molto più larga della mediana segnala dispersione alta.
- **Punto base (bp)** — un centesimo di punto percentuale (0,01%).
- **Regime (storico/macro)** — la fase di mercato (tassi in salita, dollaro forte, ecc.) in cui un episodio è avvenuto. Episodi di regimi diversi non vanno mescolati nello stesso campione.
- **Rientro verso la media (mean reversion)** — la tendenza di un prezzo a recuperare parte di un movimento brusco nei giorni successivi. Nell'event study si vede quando il segno a T+3/T+10 è opposto alla pressione dichiarata all'evento: il calo (o il rialzo) si è concentrato nel giorno T=0 e poi è stato in parte restituito.
- **Sempre su / sempre giù (baseline)** — hit rate che si otterrebbe prevedendo sempre un rialzo (o sempre un ribasso) sugli stessi casi e orizzonti della scorecard. Un hit rate che non le supera non dimostra alcun vantaggio, anche se è sopra il 50%.
- **T+1 / T+3 / T+5 / T+10 (T+N)** — giorni di **borsa** dopo l'evento, non giorni di calendario. I rendimenti sono **cumulati** dal giorno dell'evento, non giornalieri.

## Dati macro e banche centrali

- **ADP** — indagine mensile sull'occupazione privata USA; anticipa di due giorni l'NFP ufficiale.
- **BCE (Banca Centrale Europea)** — fissa i tassi per i venti paesi dell'area euro. Il tasso sui depositi è quello che riconosce alle banche sui fondi depositati presso di essa.
- **Beige Book** — rapporto della Fed, otto volte l'anno, che raccoglie testimonianze qualitative dai 12 distretti su attività, occupazione e prezzi.
- **Beni durevoli (durable goods orders)** — ordini mensili USA di beni destinati a durare oltre tre anni (aerei, macchinari, auto). Il dato "esclusi trasporti" toglie gli aerei, molto volatili, ed è la lettura più pulita della spesa per investimenti delle imprese.
- **BoC (Bank of Canada)** — la banca centrale del Canada; decide il tasso overnight otto volte l'anno. Una sua stretta rafforza il dollaro canadese, quindi fa **scendere** `CAD=X`.
- **Conference Board (Consumer Confidence Index)** — indice mensile USA della fiducia dei consumatori, costruito da un'associazione privata di imprese; pesa molto la valutazione del mercato del lavoro. Sotto 80 nella componente aspettative è storicamente associato a rischio di recessione.
- **Consenso** — media delle previsioni degli analisti prima di una release; la "sorpresa" è la differenza fra dato pubblicato e consenso. Fornitori diversi (Reuters, Bloomberg, Wind) pubblicano consensi diversi.
- **Core (inflazione di fondo)** — l'inflazione esclusi energia e alimentari freschi, perché quelle voci sono volatili e guidate da fattori esterni; il core misura meglio la pressione generata dall'economia interna.
- **CPI (Consumer Price Index)** — indice dei prezzi al consumo, la misura di inflazione percepita dalle famiglie.
- **Destatis** — l'istituto federale di statistica tedesco.
- **Dissenso (FOMC)** — voto contrario alla decisione della maggioranza, reso pubblico con il comunicato. Due o più dissensi nella stessa direzione sono letti come anticipo della prossima mossa del comitato.
- **Dot plot** — il grafico a punti in cui ogni membro del comitato Fed indica anonimamente dove vede i tassi negli anni successivi. Non è un impegno, ma è il segnale di guidance più seguito.
- **Fed / Federal Reserve** — la banca centrale degli Stati Uniti.
- **Fed regionali (presidenti)** — i dodici presidenti delle Federal Reserve Bank regionali (Cleveland, New York, ecc.). Cinque votano nel FOMC a rotazione (New York sempre): un loro discorso segnala un orientamento, ma pesa meno di una decisione o del presidente della Fed.
- **Flash estimate (stima flash)** — la prima pubblicazione, rapida e provvisoria, di un dato di inflazione; viene rivista in seguito con il dato definitivo.
- **FOMC (Federal Open Market Committee)** — il comitato della Fed che decide i tassi; si riunisce otto volte l'anno.
- **Forward guidance** — l'indicazione che una banca centrale dà sul percorso futuro dei tassi, per orientare le aspettative del mercato senza agire subito.
- **Funzione di reazione** — il modo sistematico in cui una banca centrale risponde ai dati in arrivo.
- **GDP / PIL** — prodotto interno lordo: il valore di tutti i beni e servizi prodotti. "Annualizzato" = il tasso di crescita che si otterrebbe se il ritmo del trimestre proseguisse per un anno intero.
- **Hawkish / dovish** — "da falco" / "da colomba": una banca centrale (o un suo membro) è hawkish quando segnala tassi più alti o più a lungo per combattere l'inflazione, dovish quando apre a tagli o pause.
- **Headline** — l'inflazione totale, energia e alimentari inclusi (si contrappone al **core**).
- **HICP (Harmonised Index of Consumer Prices)** — l'indice armonizzato dei prezzi al consumo usato dalla BCE, costruito con la stessa metodologia in tutti i paesi dell'area euro.
- **Initial jobless claims** — richieste settimanali di sussidio di disoccupazione negli USA (dato del giovedì). Poche richieste = mercato del lavoro solido; è il dato ad alta frequenza più tempestivo sull'occupazione.
- **ISM (Institute for Supply Management)** — indice USA di diffusione su manifattura/servizi da sondaggio ai responsabili acquisti. Sopra 50 = espansione, sotto 50 = contrazione; misura **quanti** rispondono che l'attività cresce, non **di quanto**.
- **ISM prezzi pagati (prices paid)** — sotto-indice dell'ISM: quota di responsabili acquisti che pagano di più gli input. È un'inflazione «a monte», arriva prima del CPI; sopra 70 = rincari diffusi a quasi tutte le categorie.
- **JOLTS (Job Openings and Labor Turnover Survey)** — indagine mensile USA sui posti di lavoro vacanti e sul turnover, complementare all'NFP.
- **LPR (Loan Prime Rate)** — tasso di riferimento mensile dei prestiti in Cina, pubblicato intorno al 20 del mese; è lo strumento con cui la PBOC orienta il costo del credito interno, distinto dalla gestione del cambio.
- **Media troncata (trimmed mean)** — misura dell'inflazione di fondo preferita dalla RBA: scarta le variazioni di prezzo più estreme in alto e in basso (15% per lato) e fa la media del resto, così uno shock isolato (es. carburanti) pesa meno.
- **NFP (Non-Farm Payrolls)** — nuovi posti di lavoro creati negli USA, esclusa l'agricoltura; il dato macro più seguito al mondo.
- **PBOC (People's Bank of China)** — la banca centrale cinese.
- **PCE (Personal Consumption Expenditures)** — indice dei prezzi della spesa per consumi delle famiglie USA; la sua versione *core* è la misura d'inflazione che la Fed usa come obiettivo (2%), per questo pesa sulle attese di tassi più del CPI.
- **PMI (Purchasing Managers' Index)** — indice da sondaggio ai responsabili acquisti; sopra 50 = espansione, sotto 50 = contrazione. Indicatore anticipatore.
- **PPI (Producer Price Index)** — indice dei prezzi alla produzione.
- **Produzione industriale** — indice del volume fisico prodotto da industria, costruzioni ed energia; volatile e pubblicato con oltre un mese di ritardo.
- **QE (Quantitative Easing) / QT (Quantitative Tightening)** — acquisto di titoli da parte della banca centrale per abbassare i tassi a lunga (QE) e il processo inverso di riduzione del bilancio (QT).
- **RBI (Reserve Bank of India)** — la banca centrale indiana; difende la rupia sia vendendo riserve in dollari sia con misure amministrative (limiti alle coperture a termine, finestre speciali di cambio per gli importatori di petrolio), come nell'estate 2013.
- **RBNZ (Reserve Bank of New Zealand)** — la banca centrale neozelandese; storicamente la prima al mondo ad adottare un obiettivo d'inflazione esplicito (1990) e spesso in anticipo sul ciclo delle banche centrali maggiori.
- **Riserva obbligatoria in valuta / riserva di rischio sui forward** — strumenti amministrativi della PBOC sul cambio: alzare la quota di depositi in valuta da tenere in riserva, o azzerare il deposito richiesto sugli acquisti a termine di dollari, rende più facile comprare dollari e quindi frena l'apprezzamento dello yuan.
- **Selic** — il tasso ufficiale della banca centrale brasiliana, fra i più alti al mondo in termini reali; con un debito pubblico elevato, il suo livello pesa direttamente sul costo degli interessi dello Stato.
- **SONIA (Sterling Overnight Index Average)** — il tasso overnight di riferimento in sterline, calcolato dalla BoE sulle transazioni effettive; i contratti su SONIA dicono quanti rialzi o tagli della BoE il mercato si aspetta.
- **Sorpresa macro** — la differenza fra il dato pubblicato e il consenso degli analisti; è la sorpresa, non il livello, a muovere i prezzi.
- **TPI (Transmission Protection Instrument)** — lo "scudo anti-spread" della BCE contro un allargamento ingiustificato dei differenziali sovrani nell'area euro.
- **UMich (University of Michigan Consumer Sentiment)** — indagine mensile sulla fiducia dei consumatori USA, con stima preliminare a metà mese e finale a fine mese. Include le aspettative d'inflazione delle famiglie a 1 anno e a 5-10 anni, seguite dalla Fed. Dal 2024 si raccoglie online: i livelli non sono confrontabili con quelli precedenti.
- **Vendite al dettaglio (retail sales)** — dato mensile USA (Census Bureau) sulla spesa nei negozi e online; è nominale, quindi include l'effetto dei prezzi: con l'inflazione alta una parte della crescita è solo rincaro.
- **Verbali (minutes) della Fed** — il resoconto della riunione del FOMC, pubblicato tre settimane dopo la decisione. Raramente sono una sorpresa: contano quando rivelano un orientamento della maggioranza diverso da quello prezzato.
- **YCC (Yield Curve Control)** — controllo della curva dei rendimenti: politica con cui una banca centrale (tipicamente la BoJ) fissa un tetto al rendimento di un titolo di Stato comprandone quantità illimitate per difenderlo.

## Mercati e meccanismi

- **Asta del Tesoro: coda (tail) e bid-to-cover** — gli indicatori della domanda a un'asta di titoli di Stato. La *coda* è lo scarto fra il rendimento di aggiudicazione e quello trattato sul mercato poco prima: una coda positiva significa che il Tesoro ha dovuto pagare di più per collocare tutto, cioè domanda debole. Il *bid-to-cover* è il rapporto fra domanda e importo offerto: più è basso, più l'asta è "fiacca".
- **Azioni senza diritto di voto (classe C)** — azioni che danno diritto ai dividendi e al valore dell'azienda ma non al voto in assemblea. Permettono di raccogliere capitale senza diluire il controllo del fondatore (caso Meta, ottobre 2026).
- **Bear flattening** — appiattimento della curva dei rendimenti causato dai tassi brevi che salgono più dei lunghi; è la firma di una stretta monetaria ritenuta credibile: si stringe ora, quindi l'inflazione di lungo periodo attesa scende.
- **Bear steepening** — irripidimento della curva dei rendimenti causato dai tassi lunghi che salgono più dei brevi; segnala rischio fiscale o di inflazione, non attese di stretta immediata.
- **Beta** — la sensibilità di un asset ai movimenti del suo mercato di riferimento. Un beta alto amplifica i movimenti in entrambe le direzioni.
- **Breakeven d'inflazione** — l'inflazione media implicita nei prezzi di mercato: la differenza fra il rendimento di un titolo di Stato nominale e quello del gemello indicizzato all'inflazione. Sale quando il mercato si aspetta più inflazione (es. con il petrolio in rialzo).
- **BTP Valore** — titolo di Stato italiano riservato ai risparmiatori retail, collocato in finestre di pochi giorni con premio fedeltà a scadenza; la sua raccolta misura la domanda domestica di debito italiano, un sostegno allo spread che altri paesi (es. la Francia) non hanno.
- **Capex (Capital Expenditure)** — la spesa in conto capitale: investimenti in beni durevoli (impianti, macchinari, data center).
- **Carry trade** — indebitarsi in una valuta a basso tasso per investire in attività denominate in valute a tasso più alto. Funziona finché il differenziale resta ampio e il cambio stabile; si smonta violentemente quando una delle due condizioni cade.
- **CDS (Credit Default Swap)** — contratto che assicura contro il default di un emittente: chi lo compra paga un premio annuo, in punti base del nominale. Se il premio sale, il mercato giudica più probabile il default o chiede più compenso per quel rischio.
- **Chokepoint** — collo di bottiglia della logistica marittima o energetica (Hormuz, Suez, Malacca, Bab el-Mandeb): un'interruzione locale ha effetti globali.
- **CME FedWatch** — strumento del CME che ricava dai futures sui Fed Funds la probabilità implicita di ogni decisione Fed alle prossime riunioni.
- **CNH** — lo yuan scambiato offshore (Hong Kong), libero dalla banda di oscillazione del cambio onshore (CNY): reagisce prima e di più ai segnali della PBOC.
- **Curva dei rendimenti** — il grafico dei rendimenti per scadenza (2, 5, 10, 30 anni). Si irripidisce quando le scadenze lunghe salgono più delle corte.
- **De-rating** — calo del multiplo (prezzo/utili) che il mercato è disposto a pagare, a utili invariati: tipico quando salgono i tassi o la fiducia nella crescita futura.
- **DeepSeek** — laboratorio cinese di intelligenza artificiale; i suoi modelli efficienti (R1 a gennaio 2025, V4.1-Flash a ottobre 2026) mettono in dubbio quanto calcolo serva all'AI e quindi la domanda di chip e memoria.
- **Differenziale di tasso** — la differenza fra i rendimenti di due aree valutarie; principale motore dei flussi di capitale e quindi dei cambi.
- **Diluizione** — quando una società emette azioni nuove, ogni azione esistente ha diritto a una quota più piccola degli utili e del valore dell'azienda. È il costo, per gli azionisti attuali, di finanziarsi con l'equity invece che con il debito.
- **Disinflazione** — rallentamento del *tasso di crescita* dei prezzi, non un calo dei prezzi (quello è deflazione).
- **Distressed debt (debito in difficoltà)** — obbligazioni che quotano molto sotto la pari, con rendimenti tali da implicare un rischio concreto di insolvenza o ristrutturazione.
- **Duration** — la sensibilità del prezzo di un'obbligazione a una variazione dei rendimenti. Scadenza più lunga = duration maggiore = movimento di prezzo più violento.
- **Effetti di secondo round** — il passaggio di uno shock di prezzo (es. energia) a salari e poi di nuovo a prezzi, che rischia di renderlo persistente invece che temporaneo.
- **Fixing** — il cambio di riferimento che una banca centrale (es. PBOC per lo yuan) pubblica ogni mattina come ancora per le oscillazioni consentite in giornata.
- **Free cash flow (flusso di cassa libero)** — la cassa generata dall'attività meno gli investimenti (capex). Se è negativo, l'azienda deve finanziare gli investimenti con debito, nuove azioni o riserve.
- **Futures DI (Depósito Interfinanceiro)** — futures brasiliani sul tasso interbancario medio futuro: dicono dove il mercato vede il costo del denaro in Brasile. Salgono quando cresce il rischio fiscale o l'inflazione attesa.
- **Gilt** — i titoli di Stato del Regno Unito. In DB li rappresenta l'ETF `IGLT.L`, che è un prezzo: scende quando i rendimenti dei gilt salgono.
- **Guidance (aziendale)** — la previsione che un'azienda fornisce sui propri risultati futuri.
- **Hyperscaler** — i grandi operatori cloud (Amazon, Microsoft, Google, Meta) che costruiscono data center su scala mondiale; i principali clienti del capex AI.
- **Ibovespa (Bovespa)** — l'indice principale della borsa di San Paolo, pesato su Petrobras, Vale e le grandi banche. Non è in DB: lo rappresenta `EWZ`.
- **Inferenza (AI)** — l'uso di un modello già addestrato per rispondere alle richieste (contrapposta all'addestramento). Un modello più "snello" consuma meno calcolo per risposta: il cosiddetto *shock di efficienza* è il timore che questo riduca i chip necessari per unità di domanda AI.
- **IPO (Initial Public Offering)** — la prima quotazione in borsa di una società, con vendita di azioni al pubblico. Quando la volatilità sale gli emittenti rinviano o ritirano le IPO: una «finestra chiusa» è un segnale di stress sul finanziamento di un settore.
- **LDI (Liability-Driven Investment)** — strategia con cui i fondi pensione britannici usano derivati sui Gilt per coprire le passività future; il crollo dei Gilt nel 2022 generò richieste di margine a catena.
- **Neocloud** — fornitori di potenza di calcolo AI in affitto nati per questo scopo (CoreWeave, Nebius…), finanziati in larga parte a debito garantito dalle GPU; il punto più fragile della filiera del capex AI.
- **Pass-through** — la quota dell'aumento di un costo (es. dazio, materia prima) che arriva al prezzo finale pagato dal consumatore.
- **Lock-in (mercato immobiliare)** — l'effetto per cui chi ha un mutuo acceso a tasso basso rinuncia a vendere casa per non perderlo. Prosciuga l'offerta di abitazioni esistenti e sostiene i prezzi e gli affitti, cioè la componente più pesante dell'inflazione core.
- **Premio a termine (term premium)** — il compenso extra richiesto per detenere un titolo a lunga scadenza invece di rinnovare titoli brevi. Cresce con l'incertezza sull'inflazione, l'offerta di debito e il ritiro dei compratori strutturali.
- **Premio di rischio (geopolitico)** — la componente del prezzo di una materia prima che non riflette domanda e offerta correnti, ma la probabilità percepita di una futura interruzione dell'offerta. Si "sgonfia" quando quella probabilità scende, anche senza che nulla cambi fisicamente.
- **Rating sovrano** — il giudizio di un'agenzia (Moody's, S&P, Fitch) sulla capacità di uno Stato di ripagare il debito. Un declassamento alza il costo del debito e può costringere fondi vincolati al merito di credito a vendere.
- **Rendimento (yield)** — quanto rende un titolo di Stato tenuto fino a scadenza; si muove in direzione **opposta** al prezzo.
- **Ricavi annualizzati (run-rate)** — i ricavi di un periodo breve (un mese, un trimestre) moltiplicati per portarli su base annua. Indicano il ritmo attuale, non un bilancio consuntivo: per le società private non quotate (es. i laboratori AI) sono spesso l'unico dato disponibile e arrivano da fonti indirette.
- **S-1** — il documento di registrazione che una società deposita presso la SEC per quotarsi negli Stati Uniti: conti, rischi, struttura del capitale. Quando diventa pubblico, l'IPO è in genere a poche settimane.
- **SAFE (Simple Agreement for Future Equity)** — contratto con cui un investitore versa capitale oggi in cambio di azioni future, a un prezzo fissato al successivo round o alla quotazione. Finché non si converte va rivalutato in bilancio, e le variazioni di valore possono gonfiare la perdita contabile senza muovere la cassa.
- **Shock di offerta** — un rincaro che nasce da una riduzione della disponibilità di un bene, non da un eccesso di domanda. Alzare i tassi non lo corregge: riduce solo la crescita.
- **Spare capacity (capacità inutilizzata)** — capacità produttiva che i produttori (soprattutto OPEC+) possono attivare in poche settimane; l'ammortizzatore che storicamente drena il premio di rischio sul petrolio.
- **Spread OAT-Bund** — differenza fra il rendimento del titolo di Stato francese a 10 anni (OAT, Obligation Assimilable du Trésor) e quello del Bund tedesco: il premio chiesto per il rischio Francia. Nel DB come serie derivata `OAT_BUND_SPREAD` (dal 2026-10-02).
- **SPV (special purpose vehicle, veicolo fuori bilancio)** — società creata apposta per finanziare un'attività precisa: il debito sta nel veicolo, non nel bilancio di chi usa i beni. Nel capex AI serve a comprare chip per conto di uno sviluppatore senza appesantirne lo stato patrimoniale.
- **Stagflazione** — crescita debole (o recessione) insieme a inflazione alta. È lo scenario più scomodo per una banca centrale: alzare i tassi frena ancora l'economia, tagliarli alimenta i prezzi. Sui mercati si vede quando i dati deboli non fanno scendere i rendimenti.
- **State-dependence** — il fatto che la reazione del mercato allo stesso dato dipenda dallo stato del sistema (fase del ciclo monetario, posizionamento, regime inflazionistico).
- **Surplus commerciale** — l'eccedenza delle esportazioni sulle importazioni di un paese. Per identità contabile, il surplus di uno è il deficit di altri.
- **Taper tantrum** — il balzo dei rendimenti USA di maggio-settembre 2013, quando Bernanke annunciò che la Fed avrebbe ridotto gli acquisti di titoli (QE): esempio di scuola di premio a termine che sale per un cambio di guidance, senza un rialzo dei tassi.
- **Tasso di sconto** — il tasso usato per attualizzare gli utili futuri di un'azienda: se sale, gli utili lontani nel tempo valgono meno oggi.
- **Tasso reale / tassi reali** — il tasso d'interesse al netto dell'inflazione attesa; è il costo-opportunità di detenere oro, che non produce reddito.
- **When-issued** — il rendimento a cui un titolo di Stato viene trattato prima dell'asta. Se l'asta si chiude *sotto* quel livello («through»), il Tesoro ha trovato più domanda del previsto.
- **Vol crush** — il calo brusco della volatilità implicita subito dopo un evento atteso (una decisione di banca centrale, una pubblicazione di dati): l'incertezza si risolve e il premio pagato per proteggersi si sgonfia, a prescindere dall'esito.

## Geopolitica e istituzioni

- **Aramco (Saudi Aramco)** — la compagnia petrolifera di Stato saudita, primo esportatore di greggio al mondo; gestisce impianti chiave come Abqaiq (stabilizzazione del greggio), Ras Tanura e il terminal di Yanbu sul Mar Rosso.
- **Articolo 49.3** — norma della Costituzione francese che consente al governo di far approvare un testo (tipicamente il bilancio) senza voto dell'Assemblea; in cambio l'opposizione può presentare una mozione di sfiducia, che se passa fa cadere il governo.
- **CENTCOM** — United States Central Command, il comando militare USA competente per Medio Oriente e Asia centrale.
- **Centrão** — il blocco di partiti di centro-destra del Congresso brasiliano senza un'ideologia forte, che appoggia il governo di turno in cambio di incarichi e fondi; senza di lui nessun presidente ha una maggioranza.
- **Corridoio del Mar Nero** — la rotta marittima per l'export cerealicolo ucraino; oggetto di accordi e sospensioni dal 2022.
- **EBV (Erdölbevorratungsverband)** — l'agenzia tedesca che detiene le riserve strategiche di greggio e prodotti petroliferi; può metterle in vendita per calmierare i prezzi in una crisi d'offerta.
- **Elezioni di metà mandato (midterm)** — le elezioni americane a metà del mandato presidenziale, in cui si rinnovano tutta la Camera e un terzo del Senato; nel 2026 si tengono il 3 novembre.
- **EPF (European Peace Facility)** — fondo fuori dal bilancio UE con cui l'Unione rimborsa agli Stati membri le armi inviate a paesi terzi (soprattutto l'Ucraina) e finanzia acquisti congiunti. Le decisioni richiedono l'unanimità, da cui il potere di veto dell'Ungheria.
- **Flotta ombra** — petroliere anziane, con proprietà opaca e assicurazioni non occidentali, usate per trasportare greggio russo aggirando il tetto al prezzo.
- **FMI (Fondo monetario internazionale, in inglese IMF)** — istituzione di Washington che presta ai paesi in crisi di bilancia dei pagamenti e pubblica analisi e raccomandazioni di politica economica (World Economic Outlook, rapporti regionali). Le sue raccomandazioni non sono vincolanti, ma i mercati le leggono come il parere di un osservatore esterno autorevole.
- **G20** — foro dei ministri delle finanze e governatori delle banche centrali delle venti maggiori economie.
- **GCC (Gulf Cooperation Council, Consiglio di cooperazione del Golfo)** — blocco di sei monarchie del Golfo (Arabia Saudita, Emirati, Kuwait, Qatar, Bahrein, Oman) con un patto di difesa comune: un attacco a un membro è considerato un attacco a tutti.
- **Graham Act (Sanctioning Russia Act)** — legge sulle sanzioni alla Russia promossa dal senatore Lindsey Graham, approvata dal Congresso USA nel settembre 2026: dazi sulle merci russe, penalità per chi compra petrolio e gas russo e dazi secondari fino al 100% sui maggiori importatori. Sospesa per 60 giorni da Trump il 2026-10-17.
- **Guerra ibrida** — azioni ostili sotto la soglia del conflitto aperto (sabotaggi, droni, attacchi informatici), tipicamente non rivendicate.
- **Houthi** — movimento armato sciita yemenita (Ansar Allah), sostenuto dall'Iran; colpisce con missili e droni il naviglio nel Mar Rosso e le infrastrutture saudite.
- **IEA (International Energy Agency)** — agenzia dell'OCSE per la sicurezza energetica; coordina i rilasci d'emergenza delle scorte strategiche dei Paesi membri.
- **IRGC (Islamic Revolutionary Guard Corps, Pasdaran)** — il corpo militare d'élite iraniano, distinto dall'esercito regolare; controlla le operazioni navali nello Stretto di Hormuz.
- **JCPOA (Joint Comprehensive Plan of Action)** — l'accordo del 2015 sul programma nucleare iraniano, da cui gli USA uscirono nel 2018.
- **Knesset** — il parlamento monocamerale di Israele, 120 seggi: per governare serve una coalizione di almeno 61.
- **MFF (Multiannual Financial Framework, Quadro finanziario pluriennale)** — il bilancio settennale dell'Unione europea (il prossimo copre il 2028-2034): fissa quanto spende l'UE e per cosa (agricoltura, coesione, difesa, ricerca). Si approva all'unanimità, quindi ogni grande contributore netto, come la Germania, ha di fatto un veto.
- **MoU (Memorandum of Understanding)** — memorandum d'intesa: accordo politico preliminare, meno vincolante di un trattato. Nel 2026 è il formato della trattativa USA-Iran su Hormuz.
- **NATO** — North Atlantic Treaty Organization, l'alleanza militare atlantica.
- **OFAC (Office of Foreign Assets Control)** — l'ufficio del Tesoro USA che emette e applica le sanzioni economiche (liste di persone ed entità, licenze di deroga).
- **OSINT (Open Source Intelligence)** — informazioni ricavate da fonti aperte: immagini satellitari commerciali, video sui social, dati di navigazione. Nei conflitti spesso anticipano o smentiscono le versioni ufficiali sui danni.
- **Patriot** — sistema americano di difesa antiaerea e antimissile.
- **Preemption federale** — principio per cui una legge federale USA prevale su quelle dei singoli Stati; nel dibattito sull'AI significa sostituire le leggi statali (es. California) con un'unica regola nazionale, di solito più leggera.
- **Sanzioni secondarie (dazi secondari)** — misure che colpiscono non il Paese sanzionato ma **chi commercia con lui** in Paesi terzi (es. un raffinatore indiano che compra greggio russo). Pesano sull'offerta molto più delle sanzioni dirette, perché toccano i compratori effettivi.
- **Sezione 301** — norma del diritto commerciale USA usata dal 2018 per imporre dazi sulla base di pratiche commerciali giudicate sleali.
- **Stretto di Hormuz** — braccio di mare fra Iran e Oman da cui transita circa il 20% del petrolio scambiato via mare; il principale chokepoint energetico mondiale.
- **Tagli volontari (OPEC+)** — riduzioni di produzione annunciate da singoli membri (soprattutto Arabia Saudita) oltre le quote formali del gruppo, e quindi revocabili unilateralmente.
- **Terre rare** — 17 elementi indispensabili a magneti permanenti, motori elettrici, ottiche militari e semiconduttori. La Cina non ha il monopolio dell'estrazione ma sì, di fatto, quello della raffinazione.
- **UKMTO (UK Maritime Trade Operations)** — centro della Marina britannica che raccoglie e diffonde le segnalazioni di attacchi e incidenti alle navi mercantili fra Golfo, Mar Rosso e Oceano Indiano; è la fonte primaria sugli attacchi nello Stretto.
- **War-risk (assicurazione)** — copertura aggiuntiva che armatori e caricatori pagano per transitare in zone di conflitto; quando le navi vengono colpite il premio sale e si somma al nolo, rincarando la merce trasportata.

## Materie prime, dazi e unità

- **AVT (unità di distillazione atmosferica e sotto vuoto)** — l'impianto primario di una raffineria russa, quello che separa il greggio nelle sue frazioni (benzina, cherosene, diesel, olio combustibile). Se un'unità AVT si ferma, la capacità di lavorazione dell'intero impianto scende in proporzione.
- **Bunker fuel** — il carburante delle navi (olio combustibile pesante e gasolio marino); il suo prezzo entra direttamente nei noli e quindi nel costo delle merci importate.
- **CHP (Combined Heat and Power, cogenerazione)** — centrale che produce insieme elettricità e calore per il teleriscaldamento urbano; colpirla toglie luce e riscaldamento a interi quartieri.
- **Crack spread 3-2-1 (`CRACK_321`)** — il margine lordo di una raffineria: il valore di 2 barili di benzina + 1 di distillato meno il costo di 3 barili di greggio. Sale quando i prodotti raffinati sono scarsi rispetto al greggio. Serie *derivata*, calcolata e salvata come ticker nel DB del progetto.
- **Dazio (tariffa)** — imposta su un bene importato; ne aumenta il prezzo per l'acquirente domestico.
- **DRAM / NAND / HBM** — tipi di memoria per computer. DRAM = memoria volatile di sistema; NAND = memoria di archiviazione permanente (SSD); HBM (High Bandwidth Memory) = memoria ad altissima banda per acceleratori AI, il segmento a margine più alto.
- **GNL** — gas naturale liquefatto: gas raffreddato a −162°C per essere trasportato via nave invece che via gasdotto.
- **GPL (gas di petrolio liquefatto, in inglese LPG)** — propano e butano liquefatti sotto pressione, sottoprodotti di estrazione e raffinazione; viaggiano su navi dedicate (gasiere GPL). Da non confondere con il GNL, che è metano.
- **Kpler** — società di analisi che traccia via satellite e dati AIS i carichi di petrolio, gas e prodotti raffinati nave per nave; le sue stime dei flussi (es. attraverso Hormuz) sono una delle fonti più citate quando i dati ufficiali non ci sono.
- **Landfall** — il momento in cui l'occhio di un uragano raggiunge la costa. Per i mercati energetici segna il passaggio dalla previsione (rischio sul cono di traiettoria) alla verifica del danno reale su piattaforme e raffinerie.
- **Nolo (freight rate)** — il prezzo del trasporto marittimo di un carico, per il greggio espresso in dollari al barile. Include carburante, noleggio della nave e premi assicurativi (war-risk): quando sale, il greggio *consegnato* costa di più anche se quello estratto costa uguale, e il rincaro pesa di più su chi è lontano dall'origine.
- **OPEC+** — l'OPEC (Organization of the Petroleum Exporting Countries) allargata a un gruppo di produttori non-OPEC guidato dalla Russia.
- **Scorte settimanali EIA** — il dato del mercoledì dell'Energy Information Administration USA sulle scorte di greggio, benzina e distillati; un calo superiore alle attese segnala domanda forte o offerta scarsa.
- **Scorte strategiche (SPR, Strategic Petroleum Reserve)** — riserve d'emergenza di greggio e prodotti detenute dai governi; un rilascio coordinato aggiunge offerta temporanea e tende a pesare sul prezzo, per lo più nei giorni successivi all'annuncio.
- **Shut-in** — produzione petrolifera fermata in via precauzionale (tipicamente le piattaforme del Golfo del Messico all'arrivo di una tempesta): offerta tolta subito ma per lo più temporanea.
- **Staio (bushel)** — unità di misura dei cereali americani, circa 27 kg per il grano; i futures su grano e mais sono quotati in cent per bushel — leggere le variazioni %, mai i livelli.

## Ticker e asset

- **1482.T** — ETF quotato a Tokyo su titoli di Stato giapponesi (JGB). È un **prezzo**: scende quando i rendimenti salgono.
- **^AXJO** — indice azionario ASX 200 (Australia).
- **AUD=X** — cambio USD/AUD. ⚠ Sale quando il **dollaro australiano si indebolisce**.
- **BRL=X** — cambio dollaro/real brasiliano. Sale quando il real si indebolisce.
- **BTC-USD / ETH-USD** — Bitcoin ed Ethereum; usati nel progetto come proxy del tema "digital gold" (risk-off) e del tema digitale/AI.
- **BTP_BUND_SPREAD** — differenziale di rendimento fra BTP italiano e Bund tedesco a 10 anni; misura diretta del rischio sovrano periferico. Serie *derivata*, salvata come ticker.
- **OAT_BUND_SPREAD** — differenziale di rendimento fra OAT francese e Bund tedesco a 10 anni, in punti base; misura diretta del rischio fiscale e politico francese. Serie *derivata*, salvata come ticker (dal 2005-11).
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
- **KOSDAQ** — il listino secondario coreano (tecnologia e small cap); più volatile del KOSPI, con sospensioni automatiche (circuit breaker) sui ribassi estremi.
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
