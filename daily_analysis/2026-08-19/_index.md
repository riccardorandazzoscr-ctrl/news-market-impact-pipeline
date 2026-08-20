# Daily Analysis — 2026-08-19

- **Briefing:** `~/Claude/morning brief/2026-08-19-morning-briefing.html`
- **Generato:** 2026-08-19
- **Catalog KB:** 2026-08-19T07:27:10

Triage del briefing del giorno. Per ogni notizia: decisione (✅ = scheda prodotta, ✖ = scartata), tema/motivazione, e link alla scheda `news_NN.md` quando prodotta. Scope: subset triato — scheda completa solo per notizie che mappano su uno degli asset dell'universo corrente in DB (elenco autorevole: `category_asset_map.yaml`) e hanno un analogo storico plausibile. Notizie sullo stesso tema sono consolidate in un'unica scheda.

## Triage

| # | Sez. | Notizia | Decisione | Tema / Motivazione | Scheda |
|---|------|---------|-----------|--------------------|--------|
| 01 | intl | The United Arab Emirates Halts All Trade, Commercial and Financial Transactions With Iran After Saying Two Iranian Ballistic Missiles Were Fired at Its Territory | ✅ | **geopolitical / energia** — la sospensione totale di scambi commerciali e finanziari degli Emirati Arabi Uniti verso l'Iran chiude il principale canale di re-export e di intermediazione finanziaria iraniano: shock di offerta e di rischio-Paese con trasmissione diretta su BZ=F, CRACK_321, HO=F, GC=F, CHF=X, ^VIX. Consolidata con intl 02-03 e fin 08. | [news_01](news_01.md) |
| 02 | intl | France Will Expel Two Iranian Diplomats Over the July Detention of French Embassy Staff in Tehran | ✅ | **geopolitical / energia** — l'espulsione dei diplomatici iraniani da parte della Francia chiude uno degli ultimi canali diplomatici europei verso Teheran: stesso shock di escalation. Consolidata in news_01. | [news_01](news_01.md) |
| 03 | intl | A Vessel Is Struck by an Unknown Projectile Leaving the Strait of Hormuz as Iran Signals a “Fully Offensive” Posture and Trump Insists the Blockade Stands | ✅ | **geopolitical / energia** — nave colpita in uscita dallo Stretto di Hormuz, postura iraniana «fully offensive», blocco navale USA confermato: è il canale di trasmissione più diretto su greggio e prodotti raffinati. Consolidata in news_01. | [news_01](news_01.md) |
| 04 | intl | Israel Strikes Hamas Nukhba Commanders in Gaza City as Both Sides Restate Incompatible Preconditions for the Late-July Roadmap | ✖ | Gaza — riaffermazione di precondizioni già note (nessuna delle due parti si è mossa dal roadmap di fine luglio). Nessun elemento nuovo e nessun canale di trasmissione discreto sugli asset in DB. |  |
| 05 | intl | South Korean Media Report the Ulchi Freedom Shield Exercise Will Be Cut by About Half, Reversing Seoul’s Position of a Day Earlier | ✖ | Riduzione ~50% dell'esercitazione Ulchi Freedom Shield: evento di politica di alleanza senza canale di prezzo diretto. Il crollo del Kospi dello stesso giorno è attribuibile al selloff dei semiconduttori, trattato in news_02 (EWY). |  |
| 06 | intl | Zelensky Formally Nominates Khmara as Defence Minister and Returns Sybiha to the Foreign Ministry, Ruling Out Fedorov’s Comeback | ✖ | Rimpasto di governo ucraino (Difesa, Esteri, Procurement): storia di governance interna, nessuna trasmissione su asset quotati del nostro universo. |  |
| 07 | intl | A Drone Explosion at a Bus Stop Used by Zaporizhzhia Nuclear Power Plant Staff Kills One and Injures Fifteen, the IAEA Says | ✖ | Attacco con drone alla fermata bus del personale di Zaporizhzhia e raid su centrale DTEK: infrastruttura elettrica *ucraina*, non export russo — non tocca TTF=F né i flussi che il nostro universo prezza. Rischio di coda nucleare non event-studiabile. |  |
| 08 | intl | Russia’s State Development Bank Removes Its Chief Economist After He Warned Moscow Cannot Win a War of Attrition | ✖ | Rimozione del capo economista di VEB.RF: segnale sull'ambiente informativo russo, nessun asset di trasmissione (Russia non quotata nel nostro universo). |  |
| 09 | intl | András Baka Takes Office as Hungary’s President Today, Completing the Post-Orbán Institutional Handover | ✖ | Insediamento del presidente ungherese Baka: esito già noto dall'11 agosto, evento cerimoniale e completamente prezzato. Nessun analogo con contenuto informativo. |  |
| 10 | intl | Florida’s Primaries Set a Donalds–Jolly Governor’s Race, the First Marquee Contest of the November Midterms | ✖ | Primarie della Florida: primo test elettorale del ciclo midterm, orizzonte novembre. Nessuna trasmissione di breve periodo (1-10 giorni) sugli asset in DB. |  |
| 01 | fin | Trump Pauses the 50% Tariffs on Canada for Three Days, Less Than Two Hours Before the Deadline, Saying a Deal Is Done Subject to Documentation | ✅ | **regulatory / dazi** — pausa di tre giorni sui dazi al 50% verso il Canada a due ore dalla scadenza. Canale diretto su CAD=X e ^GSPTSE, entrambi aggiunti al DB (2026-08-16 e 2026-08-18) proprio per questo tipo di evento. | [news_05](news_05.md) |
| 02 | fin | South Korea’s Kospi Triggers a Sidecar Halt and Falls 5.2% While the Nikkei Drops 2.6%, as the Artificial-Intelligence Complex Unwinds Across Asia | ✅ | **structural_themes / ciclo memoria** — unwind del complesso AI in Asia (Kospi −5,2% con sidecar, Nikkei −2,6%, Samsung e SK Hynix −7%) su apertura cinese all'H200 di Nvidia. Canale diretto su SOXX, ^NDX, EWY, EWT, ^N225, ^VIX. | [news_02](news_02.md) |
| 03 | fin | The US 20-Year Auction Tails at 5.047% Against 5.035% Expected as the Thirty-Year Yield Touches a Fresh 19-Year High of 5.33% | ✅ | **monetary_policy / premio a termine** — asta 20 anni che «taglia» (tail) e trentennale al massimo da 19 anni: repricing della parte lunga guidato da offerta e deficit, non dal tasso di policy. Canale su ^TYX, ^TNX, IEF, IGLT.L, 1482.T, VGB.AX. Consolidata con fin 09 (oro). | [news_03](news_03.md) |
| 04 | fin | US July Housing Starts Fall 12.4% to an Annualised 1.239 Million Against 1.350 Million Expected, With Single-Family Starts Down 9.9% | ✅ | **macro_data / attività** — housing starts USA −12,4% contro un consenso di 1,35 mln: prima serie di attività reale a mostrare la trasmissione del repricing dei tassi lunghi. Sorpresa al ribasso ampia e misurabile. | [news_04](news_04.md) |
| 05 | fin | Home Depot Beats With Comparable Sales up 1.7%, the Best Since Late 2022, and Reaffirms Full-Year Guidance | ✖ | Home Depot: single-name statunitense (HD) non presente nel DB, che è cross-asset e non azionario-singolo. corporate_idiosyncratic è anche l'unico tema con IC negativo (−0,06) nella scorecard W34. |  |
| 06 | fin | Japan’s June Core Machinery Orders Jump 9.7% on the Month Against 7.8% Expected, and 16.9% on the Year Against 10.8% Expected | ✅ | **macro_data / attività** — ordini di macchinari core giapponesi +9,7% m/m contro +7,8% atteso e +16,9% a/a contro +10,8%: sorpresa al rialzo ampia sul principale indicatore anticipatore del capex giapponese. Canale su ^N225, JPY=X, 1482.T. | [news_06](news_06.md) |
| 07 | fin | Australian Wages Rise 0.8% in the June Quarter, Exactly as Expected, as Deputy Governor Hauser Says Inflation Is Too High and Further Hikes Remain Possible | ✖ | Salari australiani +0,8% t/t *esattamente in linea* col consenso: nessuna sorpresa da event-studiare. Il commento hawkish di Hauser non è una decisione. Inoltre AUD=X non è nell'universo: l'unico asset australiano in DB è VGB.AX, trasmissione troppo sottile per una scheda. |  |
| 08 | fin | Crude Extends Gains to a Fourth Session and a Three-Week High, With a Private Inventory Survey Showing a Large Diesel Draw | ✅ | **commodity_energy** — quarta seduta di rialzo del greggio e forte calo delle scorte di distillati: è la traduzione di prezzo dell'escalation Emirati-Iran-Hormuz. Consolidata in news_01, dove il canale primario sono CRACK_321 e HO=F oltre a BZ=F. | [news_01](news_01.md) |
| 09 | fin | Gold Breaks Below $4,400 to About $4,340–4,350 and Silver Falls 3.5% to Roughly $63.5, Reversing the Safe-Haven Bid | ✅ | **monetary_policy / premio a termine** — oro sotto 4.400 $ e argento −3,5%: rottura del bid da bene rifugio proprio mentre i rendimenti sovrani toccano massimi pluridecennali. Stesso meccanismo dell'asta 20 anni (costo-opportunità dell'asset a cedola zero) → consolidata in news_03. | [news_03](news_03.md) |
| 10 | fin | Bank of America’s August Fund Manager Survey Shows Cash at 3.5%, the Sixth-Lowest Since 1998, and Equity Allocation at the Highest Since November 2021 | ✖ | Fund Manager Survey di Bank of America (cassa al 3,5%, allocazione azionaria ai massimi da nov-2021): fotografia di posizionamento, non uno shock-notizia discreto e databile. Non event-studiabile; usata come contesto nella sintesi di sessione. |  |

## 🔍 One Thing to Watch Today

**The July Federal Open Market Committee Minutes at 14:00 Eastern — Because Three Officials Dissented for a Hike, and the Market Has Since Moved to Pricing No Hike at All**

The minutes of the 28–29 July meeting are released this afternoon, and they are the single most consequential scheduled item on the calendar because of the gap that has opened between what the Committee was arguing about three weeks ago and what the market believes today. At that meeting the Federal Open Market Committee held the federal funds target at 3.50–3.75% with three regional presidents — Logan, Hammack and Kashkari — dissenting in favour of a 25 basis-point increase, and the statement was left almost unchanged from June with no forward guidance, consistent with Chair Kevin Warsh’s stated aversion to signalling the path. Since then, a run of soft data has pushed markets to price a September hold as the base case and to stop fully discounting any increase this year. What the minutes will reveal is the composition of the majority: whether the seven or so members who voted to hold did so because they judged inflation to be easing, or because they judged the transmission of an energy-driven price shock to be something monetary policy should look through. Those are very different reaction functions, and the long end is currently pricing neither of them — the thirty-year at a 19-year high and a tailing 20-year auction say the bond market has stopped taking its cue from the policy rate at all. Three markers through the session, in sequence. First, UK July consumer price inflation at 07:00 London time, where Pantheon Macroeconomics and Deutsche Bank both look for 2.9% against 2.6% in June, driven by the 13% Ofgem energy price cap increase on 1 July, with core expected at 2.5%; an upside miss with the ten-year gilt already above 5.05% would be the day’s cleanest evidence that the energy shock is now general rather than sectoral. Second, the final euro-area harmonised index of consumer prices at 11:00 Central European Time, confirming or revising the 2.9% flash estimate for July with energy at 10.0% year on year — the component the European Central Bank’s 2.25% deposit rate cannot address, and which Chief Economist Philip Lane has said makes the outlook “highly dependent” on the US–Iran war. Third, the minutes themselves into a US session that opens with the Kospi down more than 5% behind it, Bank of America reporting the lowest fund-manager cash balances since 1998, and a fourth consecutive up-day in crude. A hawkish read of the July discussion into that tape is the combination with the least margin for error.

## Sintesi di sessione

**Esito del triage: 10 notizie tenute su 20, consolidate in 6 schede; 10 scartate.**
Il rapporto tenute/schede (10 → 6) è alto rispetto alla media perché due gruppi di notizie descrivevano lo stesso shock visto da angoli diversi: quattro item sull'escalation Iran-Golfo e sul greggio → `news_01`; due item sul riprezzamento della parte lunga (asta e oro) → `news_03`.

### Il tema dominante: un solo circuito, osservato in cinque punti

La giornata non ha sei storie. Ne ha **una**, e le schede sono i punti in cui la si può misurare:

> **shock energetico da Hormuz** ([news_01](news_01.md)) → **inflazione persistente e premio a termine in salita** ([news_03](news_03.md)) → **tassi sui mutui più alti → crollo dei cantieri residenziali USA** ([news_04](news_04.md)) → **de-rating delle valutazioni growth sul complesso AI** ([news_02](news_02.md)), amplificato da un posizionamento senza liquidità di riserva. In parallelo, l'ancora che teneva basso il premio a termine globale — il Giappone a tasso zero — si sta staccando ([news_06](news_06.md)).

Il briefing stesso fornisce la misura più eloquente della catena: *"un movimento di 5 punti base sul trentennale sta producendo movimenti del 5% sul Kospi"*. Cinque punti base sono un'inezia. Il fattore 100 fra causa ed effetto **non** è nel meccanismo economico: è nella leva di posizionamento. Il Fund Manager Survey di Bank of America (fin 10, scartata dal triage perché fotografia di posizionamento e non shock databile) misura la stessa cosa dall'altro lato: liquidità al 3,5% degli attivi, sesta lettura più bassa dal 1998, allocazione azionaria ai massimi da novembre 2021, e intervistati che dichiarano di **non** preoccuparsi né di rialzi dei tassi né di capex AI. La complacency registrata dal sondaggio e il drawdown in corso sono lo stesso fenomeno osservato in due momenti diversi.

### Letture trasversali

1. **Lo shock energetico non si legge sul petrolio.** È il risultato più netto della giornata: sui 22 analoghi di `news_01`, il margine di raffinazione **CRACK_321** ha mediana **+7,1% a T+3 e +9,8% a T+10** con primo quartile sempre positivo, mentre il Brent ha mediana **negativa** a T+1 e appena +0,78% a T+10 con deviazione standard del 12,7%. Quando il collo di bottiglia è marittimo, il valore si sposta dalla materia prima al prodotto trasformato — il greggio si stocca e si rilascia dalle riserve strategiche, il diesel già raffinato e già in transito no. Questo canale è anche il ponte con l'inflazione: il diesel entra nei costi di quasi tutto.

2. **La parte lunga ha smesso di prendere il segnale dalla politica monetaria.** Il target sui Fed funds è fermo a 3,50-3,75% e il mercato non sconta rialzi, eppure il trentennale è al massimo da 19 anni e cinque delle ultime sette aste a 20 anni hanno "tagliato". Per costruzione, se le aspettative di policy scendono e il rendimento sale, sta salendo il **premio a termine**. Il briefing lo formula come *"fissato dal bilancio del compratore marginale, non dalle previsioni macro"*. È una storia fiscale e di offerta, non monetaria — al punto che classificarla `monetary_policy` in `news_03` è stata una scelta tassonomica obbligata (in `fiscal_policy` il token `term_premium` esiste solo a livello di documento, filtro debole).

3. **L'oro sta cambiando funzione, e questo peggiora la nostra visibilità.** Per due settimane oro vicino ai record e rendimenti nominali record erano coesistiti: si spiegava leggendo l'oro come assicurazione contro il rischio di credibilità fiscale/monetaria, non come attività a tasso reale. La rottura sotto 4.400 dollari (argento −3,5%) suggerisce che quel premio si stia sgonfiando. Il paradosso, ben colto dal briefing: finché l'oro segnalava il rischio istituzionale era un termometro utile; se torna a seguire i tassi reali, quel termometro si spegne.

4. **Segno misto sui bond: coerenza, non divergenza.** In `news_03` la mediana degli analoghi mostra ^TYX e ^TNX (rendimenti) **negativi** e IEF, IGLT.L, VGB.AX, EXX6.DE (prezzi di ETF) **positivi**. È lo stesso fatto — i rendimenti rientrano dopo lo shock — letto con due convenzioni opposte. Va detto esplicitamente ogni volta che due di questi asset compaiono nella stessa tabella.

5. **Un rimbalzo meccanico non è una previsione di rialzo.** Sia `news_01` (^VIX in discesa, ^GSPC positivo) sia `news_02` (SOXX +2,67% a T+3) mostrano mediane positive dopo shock negativi. La ragione è di disegno: l'event study parte dalla chiusura del giorno dello shock, quando il ribasso è già avvenuto, e cattura quindi il rientro dell'eccesso da liquidazione forzata. È informazione utile — dice che le vendite da margin call rientrano — ma non è un segnale di acquisto. La dispersione crescente a T+10 lo conferma.

### Qualità del segnale: cosa la scorecard ci impedisce di dire

Rilettura della **scorecard 2026-W34, sezione 5-bis** prima di ogni lettura direzionale. Gli asset ❌ **controproducenti** (IC storicamente negativo) sono **DX-Y.NYB, GC=F, IEF, ^TNX**. Su questi le schede riportano l'event study ma dichiarano esplicitamente che il segno storico è inaffidabile e non ne traggono direzione. Il vincolo morde parecchio oggi:

| Scheda | Asset ✅ affidabili disponibili | Asset ❌ neutralizzati | Effetto |
|---|---|---|---|
| news_01 (Hormuz/crude) | — (CRACK_321, HO=F, CHF=X non giudicati) | GC=F | lettura poggia su asset non ancora giudicati; ^VIX ✅ e ^GSPC ⚠️ come contorno |
| news_02 (AI/memoria) | ^NDX, ^VIX, EEM (IC +0,17 tutti e tre) | — (SOXX ⚠️ debole) | **la scheda meglio sostenuta della giornata** |
| news_03 (premio a termine) | ^NDX | ^TNX, IEF, GC=F, DX-Y.NYB | **quattro asset centrali neutralizzati**: resta la coerenza interna rendimenti/prezzi |
| news_04 (housing starts) | ^NDX, ^VIX | ^TNX, IEF, DX-Y.NYB (+ EURUSD=X privo di contenuto) | lettura ridotta a due asset |
| news_05 (dazi Canada) | ^VIX | DX-Y.NYB | CAD=X e ^GSPTSE non ancora giudicati (in DB da 3-5 giorni) |
| news_06 (Giappone) | **nessuno** | ^TNX | ^N225 e JPY=X entrambi ⚠️ deboli → lettura dichiaratamente qualitativa |

**Osservazione ricorrente**: gli asset controproducenti sono sistematicamente quelli di **rifugio, tassi e dollaro** (GC=F, IEF, ^TNX, DX-Y.NYB), mentre quelli affidabili sono **azionario e volatilità** (^NDX, ^VIX, EEM, ^STOXX50E, BZ=F). Questa asimmetria è stabile da almeno tre audit (2026-08-10 e successivi) e merita di essere trattata come una proprietà del sistema, non come rumore settimanale: le schede su temi obbligazionari/valutari sono strutturalmente le più deboli che produciamo.

### Debolezze metodologiche emerse oggi (non lacune di KB)

- **Il filtro `--direction` non discrimina su `activity_growth`.** `--direction pos` e `--direction neg` restituiscono 28 episodi su 29 identici (verificato incrociando `news_04` e `news_06`). Il pool descrive "giornate di release di dati di attività", non "sorprese al ribasso" o "al rialzo". Finché resta così, ogni scheda `macro_data / activity_growth` ha un filtro direzionale nominale.
- **Su `regulatory / tariff_escalation` la direzione `pos` restituisce ZERO episodi in senso stretto.** La libreria non contiene un solo episodio di dazi etichettato come distensivo: ogni scheda su una de-escalation commerciale è costretta a usare un pool di escalation. In `news_05` abbiamo aggirato il problema con un sottoinsieme potato a mano (N=7, INDICATIVE ONLY), che non è una soluzione.
- **Su `term_premium` la direzione `neg` stretta dà solo 5 episodi** e la libreria ricade su mixed/sconosciuto per arrivare a 17.

In tutti e tre i casi la causa è la stessa già misurata il 2026-08-18: gli episodi vengono etichettati dal testo *attorno alla data*, e le righe di episodio delle schede passate nominano il fatto ma non il **verso** né il **meccanismo**. Il rimedio non è nel codice ma nella scrittura delle schede — cosa che le sei di oggi provano ad applicare, nominando esplicitamente il canale in ogni riga di episodio.

#### Interventi fatti sulle lacune (2026-08-19, sessione di manutenzione)

**La diagnosi qui sopra era giusta sui sintomi ma sbagliata sulla causa: era un bug, ed è corretto.**
Non era (solo) la scrittura delle schede. `harvest_card` estrae **un solo `sentiment` per
scheda** e `cmd_build` lo applicava a **tutte** le date della scheda — comprese le 20-30
date storiche citate come analoghi, che non hanno nulla a che vedere col segno della
notizia del giorno. In pratica la direzione di un episodio non descriveva l'episodio: era
l'orientamento della scheda che l'aveva citato. Misurato: **367 episodi su 844 (43%)
portavano 2 o 3 direzioni contemporaneamente**, e su `regulatory/tariff_escalation` le
`pos` erano **zero** semplicemente perché nessuna scheda distensiva aveva mai citato quegli
episodi.

Introdotta `directions_local`, stesso principio di `subthemes_local`: il verso si legge dai
marcatori nel testo *attorno a quella data*. Vocabolario calibrato su **2.880 contesti
reali** (`shock` 284, `hawkish` 195, `escalation` 189, `attacc` 136 sul lato negativo;
`dovish` 67, `rally` 51, `rimbalz` 36, `accordo` 32 sul positivo). Esclusi `tagli` e `dazi`
perché marcatori di **tema**, non di verso; `\bmiss\b` ancorato perché senza confini
catturava **missile**, frequentissimo nelle schede geopolitiche.

Risultato sulle tre debolezze:

| Pool | Prima (livello scheda) | Dopo (date-locale) |
|---|---|---|
| `macro_data/activity_growth` | 37 pos / 57 neg, **35 con entrambe** | 20 pos / 28 neg, 13 con entrambe |
| `monetary_policy/term_premium` | 24 pos / 52 neg | 20 pos / 31 neg |
| `regulatory/tariff_escalation` | 13 pos / 36 neg (0 in senso stretto) | 2 pos / 9 neg |

Sul primo pool `--direction pos` e `--direction neg` restituiscono ora **16 e 20 date con
12 in comune**, contro le 28 su 29 identiche di stamattina. `find --direction` ha adesso i
tre livelli già usati per i sotto-temi e **dichiara in stderr** quando degrada
(«uso la direzione a livello di scheda: FILTRO DEBOLE»).

**Terza debolezza — non risolvibile in codice, e la misura lo conferma.** Su
`tariff_escalation` le `pos` date-locali sono **2**: sotto qualunque soglia. Non è
etichettatura, è assenza di dati — la libreria non contiene episodi di *distensione*
commerciale perché non ne abbiamo mai scritti. Si chiude solo con episodi datati, ed è
esattamente ciò che copre la lacuna KB n.1 qui sotto.

### Lacune emerse (Knowledge Base)

1. **Dazi e commercio USA-Canada / quadro USMCA — lacuna nuova, priorità alta.**
   - *Tema canonico*: `regulatory`, sotto-tema `tariff_escalation` / `nafta_usmca`.
   - *Asset coinvolti*: **CAD=X** (in DB dal 2026-08-16) e **^GSPTSE** (in DB dal 2026-08-18), più ^GSPC sul canale costi di input.
   - *Perché il pool attuale non basta*: il `match` su `--theme regulatory --keyword tariff --keyword canada --asset CAD=X --asset ^GSPTSE` restituisce **punteggio massimo 1**, su match puramente lessicale, senza alcun match di asset. L'unica research sui dazi (`Dazi e guerra commerciale USA 2018–2026`) è interamente costruita sul canale **USA-Cina**. Tutti i 13 episodi analoghi disponibili per `news_05` sono cinesi: il campione non contiene un solo episodio canadese.
   - *Cosa manca in concreto*: cronologia datata degli attriti commerciali USA-Canada (rinegoziazione NAFTA 2017-2018, dazi acciaio/alluminio Section 232 del 2018 e loro rimozione nel maggio 2019, entrata in vigore USMCA 2020, ciclo 2025-2026); trasmissione documentata su CAD=X e ^GSPTSE; e — elemento senza precedenti nel campione esistente — il **rischio giuridico**, cioè l'annullamento dei dazi da parte della Corte Suprema nel febbraio 2026 e il ripiego sulla **Section 338** del Tariff Act 1930, norma mai testata.
   - *Ricorrenze*: il canale dazi USA-Canada ha già motivato due estensioni dell'universo asset in quattro giorni (CAD=X il 16 agosto, ^GSPTSE il 18 agosto) senza che la KB sia stata estesa di conseguenza. È la seconda volta in una settimana che una scheda su questo tema deve dichiarare "nessun episodio specifico nel campione".

2. **Ciclo del capex giapponese e trasmissione al premio a termine globale — lacuna parziale, priorità media.**
   - *Tema canonico*: `macro_data` (release giapponesi) in intersezione con `monetary_policy` (funzione di reazione BoJ).
   - *Asset coinvolti*: **^N225**, **JPY=X**, **1482.T**, con contagio su ^TNX e ^TYX.
   - *Perché il pool attuale non basta*: per `news_06` nessuno dei due pool disponibili è adeguato. `macro_data / activity_growth` è dominato da ISM e PMI **statunitensi** e ha filtro direzionale non discriminante; `monetary_policy / boj` contiene solo **riunioni e interventi** della banca centrale, non release di dati. Abbiamo dovuto usare entrambi e dichiarare che danno risultati divergenti proprio sull'asset centrale (1482.T: prezzi in salita nel pool BoJ, in discesa nel pool activity). Le due research esistenti (`Giappone/Bank of Japan` e `Premio a termine globale`) coprono i canali carry trade, YCC e interventi FX, ma **non** la catena "sorpresa su dati di attività giapponesi → riprezzamento delle attese BoJ → JGB → premio a termine estero".
   - *Cosa manca in concreto*: episodi datati di **sorprese macro giapponesi** (Tankan, ordini di macchinari core, PIL, CPI di Tokyo) con la reazione misurata su ^N225/JPY=X/1482.T, distinguendo i casi in cui la sorpresa ha spostato le attese di policy da quelli in cui non l'ha fatta.
   - *Ricorrenze*: prima volta che viene esplicitata in questa forma, ma il nesso "parte lunga giapponese = ancora del premio a termine globale" è comparso nel briefing e nelle schede più volte da quando le curve sovrane non-USA sono state aggiunte al DB il 2026-08-18.

*(Come da regola fissata il 2026-08-16 e precisata il 2026-08-18: le lacune vengono solo descritte qui. Né la research né il prompt di deep research vengono scritti nel run giornaliero; il prompt in `knowledge_base/_prompts/` si scrive solo su richiesta esplicita del maintainer.)*

### Da tenere d'occhio nelle prossime sedute

- **Oggi 14:00 New York — minute FOMC del 28-29 luglio.** La domanda non è "alzeranno?" ma **perché la maggioranza ha tenuto fermo**: perché vede l'inflazione rientrare, o perché ha deciso di guardare attraverso lo shock energetico? Sono due funzioni di reazione diverse, e la parte lunga non prezza né l'una né l'altra. Una lettura hawkish su un mercato che apre col Kospi a −5% alle spalle e la liquidità dei gestori ai minimi dal 1998 è la combinazione con meno margine d'errore della giornata.
- **Numero di transiti giornalieri da Hormuz.** È la variabile che prezza il greggio, non la retorica. Finché resta a una cifra siamo in regime di offerta; l'episodio del 2026-04-17 (escluso dal pool perché opposto) mostra che la riapertura può valere oltre l'11% sul Brent **in una sola seduta**.
- **Venerdì 21 agosto, dazi Canada.** Se i documenti non sono firmati entro la chiusura, il fine settimana si apre con un rischio binario e lunedì 24 può riprezzare bruscamente. Il pattern degli analoghi descrive ciò che accade quando un rischio viene *rimosso*, non *rinviato di tre giorni*.
- **⚠ `BTP_BUND_SPREAD` fermo al 2026-08-07.** Il fetch da Stooq restituisce HTTP 404 su tutti i simboli di rendimento benchmark (problema noto dal 2026-08-18, chiave API o endpoint). Nessuna scheda di oggi lo usa, ma va ricordato che **non è leggibile come dato corrente** finché non è risolto.


