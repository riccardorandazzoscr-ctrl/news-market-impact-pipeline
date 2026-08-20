# Daily Analysis — 2026-08-17

- **Briefing:** `~/Claude/morning brief/2026-08-17-morning-briefing.html`
- **Generato:** 2026-08-17
- **Catalog KB:** 2026-08-16T19:11:12

Triage del briefing del giorno. Per ogni notizia: decisione (✅ = scheda prodotta, ✖ = scartata), tema/motivazione, e link alla scheda `news_NN.md` quando prodotta. Scope: subset triato — scheda completa solo per notizie che mappano su uno degli asset dell'universo corrente in DB (46 strumenti, elenco autorevole in `category_asset_map.yaml`) e hanno un analogo storico plausibile.

## Triage

| # | Sez. | Notizia | Decisione | Tema / Motivazione | Scheda |
|---|------|---------|-----------|--------------------|--------|
| 01 | intl | The US–Iran Ceasefire Lapses Today With No Agreement on the Strait of Hormuz and Washington Preparing an “Economic Isolation” Package | ✅ | `commodity_energy` / `shipping_chokepoint` — chokepoint marittimo chiuso al greggio: canale diretto su BZ=F, CRACK_321, HO=F, GC=F, ^VIX. Pool di 30 analoghi date-locali. **Consolidata** con intl 02 + fin 05 + One Thing to Watch. | [news_01](news_01.md) |
| 02 | intl | The Lebanon Death Toll From Saturday's Israeli Strikes Rises to 11, and Israel Names Two Hezbollah Commanders It Says It Killed | ✅ | Stesso teatro di escalation mediorientale dell'item 01: restringe lo spazio diplomatico alla vigilia della scadenza. Consolidata, non ha una scheda propria. | [news_01](news_01.md) |
| 03 | intl | Kushner Meets Hamas's Khalil al-Hayya in Egypt for More Than Two Hours; Hamas Ties Disarmament to a Public Netanyahu Commitment | ✖ | Trattativa diplomatica in stallo reciproco, senza alcun canale di trasmissione misurabile sugli asset in DB: nessuno strumento quotato prezza il sequenziamento del disarmo di Hamas. | — |
| 04 | intl | Trump Orders the Pentagon to “Substantially Reduce” Joint Exercises With South Korea on the Day Ulchi Freedom Shield Begins | ✖ | Mapperebbe su EWY e SHLD.L, ma manca il requisito (b): nessun pool di analoghi utilizzabile in libreria per un *ridimensionamento* di alleanza (i token disponibili coprono escalation, non de-escalation), e il mercato coreano è chiuso per il Liberation Day — non prezzabile a T+0. Segnalato come lacuna. | — |
| 05 | intl | A Spanish F-18 Shoots Down a Suspected Russian Drone Over Romania — the Fourth Aircraft Romania Has Downed This Year | ✖ | Quarto abbattimento dell'anno: l'evento è ormai ricorrente e non costituisce uno shock-notizia discreto. Nessuna attribuzione ufficiale dell'origine del drone, nessuna invocazione dell'Articolo 5. | — |
| 06 | intl | The Flores Earthquake Toll Reaches at Least 51 as Rescuers Clear Landslides and Reach Cut-Off Inland Villages | ✖ | Disastro naturale con bilancio provvisorio in aggiornamento per accesso ai villaggi, non per nuovi eventi. Indonesia mappabile (EIDO, IDR=X) ma senza impatto su infrastrutture esportative o produttive di rilievo di mercato. | — |
| 07 | intl | Colombia's Earthquake Toll Reaches 294 as President de la Espriella Asks Trump to Suspend Tariffs to Fund Reconstruction | ✖ | Nessun proxy quotato per la Colombia nell'universo asset (EWZ/BRL=X coprono il Brasile, non la regione andina). La richiesta di sospensione dei dazi è senza risposta e non ha una data operativa. | — |
| 08 | intl | Zambia's Electoral Commission Is Due to Declare the Presidential Result Today, With Observers Reporting Intimidation and the Opposition Already Claiming Victory | ✖ | Nessun asset dell'universo mappa sullo Zambia; EEM è troppo diluito (peso trascurabile) per esprimere il rischio elettorale di un singolo Paese africano. | — |
| 09 | intl | New Copernicus Imagery Shows Four of Europe's Largest Rivers at Record Lows, With About Half the Continent Under Drought | ✅ | Stesso fenomeno di fin 06, con la dimensione continentale (Danubio/Paks → generazione elettrica). Consolidata. | [news_05](news_05.md) |
| 10 | intl | Australia Sets 2 November for the Gun Buyback Prompted by the Bondi Beach Attack, With Compensation up to A$1,000 a Firearm | ✖ | Politica interna australiana su un orizzonte di novembre; nessun asset australiano in DB e nessun canale di trasmissione finanziario. | — |
| 01 | fin | Japan's Second-Quarter GDP Grows Just 0.3% on the Quarter Against 0.5% Expected — 1.1% Annualised Versus 2.0% Forecast, a Clear Downside Surprise | ✅ | `macro_data` / `activity_growth` — sorpresa negativa con consenso pubblicato; canale su JPY=X, ^N225, ^TNX, ^VIX. Pool di 28 analoghi date-locali. | [news_02](news_02.md) |
| 02 | fin | China's July Bank Lending Contracted by 340 Billion Yuan Against Expectations of a 45 Billion Yuan Expansion — the Largest Monthly Contraction on Record | ✅ | `macro_data` / `cny` + `credit_channel` — contrazione record del credito: canale su CNY=X, HG=F, EEM, ^STOXX50E. **Consolidata** con fin 03 + fin 08. | [news_03](news_03.md) |
| 03 | fin | China's July Activity Data Lands This Morning: Consensus Is Retail Sales +1.5%, Industrial Output +4.8% and Fixed-Asset Investment −5.9% Year to Date | ✅ | Stesso oggetto (ciclo domanda/credito cinese) di fin 02; dato non ancora pubblicato al momento della scheda. Consolidata. | [news_03](news_03.md) |
| 04 | fin | The September Federal Reserve Hike Has Been Priced Out: Futures Now Put 69% on a Hold, and the Two-Year Yield Has Touched a Seven-Week Low | ✅ | `monetary_policy` / `guidance_pivot` — ri-prezzatura del percorso dei tassi USA; canale su ^GSPC, ^NDX, ^TNX, IEF, DX-Y.NYB, ^VIX. Pool di 25 analoghi date-locali. | [news_04](news_04.md) |
| 05 | fin | Brent Holds at $88.50 Into the Ceasefire Expiry, and US Pump Prices Are 29% Higher Than a Year Ago at $4.08 a Gallon | ✅ | È il lato-prezzo dello stesso evento di intl 01 (livelli Brent + benzina alla pompa come canale verso il CPI). Consolidata. | [news_01](news_01.md) |
| 06 | fin | The Rhine Falls to 19 Centimetres at Kaub, the Lowest Since Records Began in 1880, and Barge Freight Rates Are up About 400% in Two Months | ✅ | `commodity_energy` / `supply_disruption` — vincolo fisico su logistica ed energia europea; canale su TTF=F, EXH9.DE, ^GDAXI, EURUSD=X, HO=F. Pool di 13 analoghi (forzato con `--min-n 5`). **Consolidata** con intl 09. Confidence *low*: fenomeno graduale, non evento discreto. | [news_05](news_05.md) |
| 07 | fin | Asian Markets Drift Ahead of the China Data With Seoul Shut, While European and US Futures Point Marginally Higher | ✖ | Cronaca di mercato, non shock-notizia: descrive movimenti (peraltro minimi, in attesa del dato cinese) senza un evento discreto da cui far partire un event study. Il contenuto rilevante è già in news_02 e news_03. | — |
| 08 | fin | The Offshore Renminbi Sits at Its Strongest Since February 2023 Near 6.74 While Chinese Yields Hover at One-Year Lows | ✅ | Il paradosso valuta forte / credito in contrazione è parte integrante della diagnosi cinese di fin 02. Consolidata. | [news_03](news_03.md) |
| 09 | fin | Canada Rejects Washington's Latest Offer With 50% Tariffs Due on Wednesday, and Ottawa Has Warned the Levies Could Halt Talks Altogether | ✅ | `regulatory` / `tariff_escalation` — scadenza tariffaria datata (19 agosto) e test della base legale post-sentenza; canale su CAD=X, DX-Y.NYB, ^GSPC, ^VIX, ^STOXX50E. Pool di 30 analoghi dal ramo `geopolitical`. | [news_06](news_06.md) |
| 10 | fin | The US Consumer Gets Its Corporate Cross-Check This Week: Home Depot Tuesday, Target and Lowe's Wednesday, Walmart Thursday, Flash PMIs Friday | ✖ | Calendario prospettico, non un evento: le trimestrali non sono ancora uscite. Inoltre `corporate_idiosyncratic` su single-name (Home Depot, Target, Lowe's, Walmart) non presenti in DB; il proxy ^GSPC è troppo diluito. Da riprendere a dati pubblicati. | — |

## 🔍 One Thing to Watch Today

**The Expiry of the US–Iran Ceasefire — Because Oil Is the One Variable Holding Two Central Banks in Place, and It Is the Only Thing Markets Have Not Repriced**

Everything else on today's calendar is a known quantity with a published consensus. The ceasefire expiry is not. It lapses on Monday with tanker traffic through the Strait of Hormuz still halted, no announced extension, Tehran publicly demanding that Washington accept defeat and the Treasury preparing an economic-isolation package; the weekend's Israeli strikes in Nabatieh, which killed 11 and took out two named Hezbollah commanders, have narrowed the diplomatic space rather than widened it. Brent is steady at $88.50 after a 6% week, and the market is carrying that position into an event with a binary structure and no price discovery until the outcome is known. What makes it decisive rather than merely important is what oil is currently holding up. The September Federal Reserve hike has been priced out — futures now put 69% on a hold, and the two-year yield touched a seven-week low last week — on the strength of a 0.6% fall in retail sales, a soft July payrolls report and benign inflation. That repricing assumes energy behaves. US pump prices are already 29% above a year ago at $4.08 a gallon, and Trump spent the weekend telling voters to accept it. If the ceasefire lapses without replacement and Brent breaks $89 towards the $100 level at which AMP expects Washington to intervene, the inflation path that justified the postponement stops holding, and the front end has to reprice a second time in three weeks. Three markers through the session: whether any extension or Omani-brokered corridor announcement emerges before the European open; whether Brent takes out last week's high rather than fading it as it did through late July; and, separately, whether China's July activity data — consensus retail sales +1.5%, industrial output +4.8% — confirm the deleveraging that July's record 340bn yuan credit contraction implies. A weak Chinese print plus a lapsed ceasefire is the combination that puts a genuine supply shock on top of a demand contraction, and that is the configuration no central bank has a clean answer for.

## Sintesi di sessione

**Esito del triage: 6 schede prodotte, 11 notizie tenute (di cui 5 consolidate), 9 scartate.**

### I temi dominanti

La sessione ha una struttura insolitamente **verticale**: quasi tutte le notizie tenute descrivono lo stesso nodo visto da lati diversi, cioè uno **shock di offerta energetica che si scontra con una domanda globale che si sta indebolendo**, mentre le banche centrali hanno appena scommesso che l'energia si comporti bene.

Tre blocchi:

1. **Offerta energetica sotto vincolo** (`news_01`, `news_05`). Da un lato la scadenza della tregua USA-Iran con lo Stretto di Hormuz ancora chiuso e il Brent a 88,50 dollari; dall'altro il Reno a 19 centimetri a Kaub — minimo dal 1880 — con noli fluviali a +400% e metà Europa in siccità. Sono due shock di offerta indipendenti che colpiscono lo **stesso importatore netto**: l'area euro. Il primo è geopolitico e discreto, il secondo climatico e graduale.
2. **Domanda globale che rallenta** (`news_02`, `news_03`). Il PIL giapponese del secondo trimestre delude con consumi piatti e investimenti in calo, "salvato" solo dal crollo delle importazioni — cioè dal petrolio che non arriva. La Cina registra la contrazione del credito più profonda della serie storica (−340 miliardi di yuan a luglio contro +45 attesi), con famiglie e imprese che rimborsano invece di indebitarsi. Sono due economie che, per ragioni diverse, smettono di tirare.
3. **Politica economica che ha già scommesso** (`news_04`, `news_06`). La Federal Reserve ha visto prezzare via il rialzo di settembre (69% di *hold*) sulla base di inflazione benigna e consumatore debole; l'amministrazione americana porta i dazi al 50% sul Canada in vigore mercoledì, testando insieme il Canada e la propria base legale post-sentenza.

### La lettura trasversale

**La scommessa del mercato è internamente incoerente, e oggi è la giornata in cui potrebbe emergere.** La ri-prezzatura della Fed poggia sull'ipotesi che l'energia si comporti bene. Ma la benzina alla pompa è già a 4,08 dollari al gallone (+29% su un anno), la tregua scade oggi e — dato più interessante dell'intera sessione — negli analoghi storici il **margine di raffinazione** (`CRACK_321`) ha mediana **+5,65% a T+3** e **+7,65% a T+10**, mentre il Brent puro si ferma a **+0,78% a T+10** con dispersione del 12,7%. Il canale che porta la guerra all'indice dei prezzi al consumo americano non passa dal greggio: passa dai prodotti raffinati. Se si vuole guardare un solo prezzo per capire se il rinvio della Fed regge, non è il Brent — è il crack spread.

**Il contrappeso disinflazionistico è cinese, e potrebbe salvare la scommessa per la ragione sbagliata.** Se le vendite al dettaglio cinesi di oggi confermano il deleveraging simultaneo di famiglie e imprese, la domanda cinese diventa una seconda fonte indipendente di disinflazione globale — abbastanza forte da compensare l'energia. Ma "l'inflazione non sale perché il mondo rallenta" non è lo scenario che i mercati azionari stanno prezzando. Il briefing lo formula bene: uno shock di offerta sopra una contrazione di domanda è la configurazione per cui nessuna banca centrale ha una risposta pulita.

**L'asimmetria Europa/Stati Uniti è la conclusione con il supporto statistico migliore.** Emerge indipendentemente in due schede: negli analoghi su chokepoint energetici l'`^STOXX50E` è l'unico indice con mediana **negativa a T+10 (−0,86%)** dove l'S&P 500 è positivo (+1,15%); negli analoghi su shock di offerta europei l'`EURUSD=X` ha mediana negativa a **tutti** gli orizzonti con il p75 sotto zero da T+3 (cioè l'euro si è indebolito in più di tre quarti degli episodi). La ragione è la stessa: l'area euro paga in valuta estera l'energia che non produce, e oggi ne sta subendo due shock insieme. Entrambi gli asset sono ✅ affidabili / ⚠️ deboli ma con N grande in scorecard, quindi la lettura è solida quanto può esserlo.

### Nota metodologica sugli asset ❌ (scorecard 2026-W33, sez. 5-bis)

Gli asset **DX-Y.NYB, GC=F, IEF, SOXX, ^TNX** hanno IC storicamente negativo e su di essi **non è stata tratta alcuna direzione attesa** in nessuna scheda; le tabelle sono riportate con dichiarazione esplicita di inaffidabilità del segno. Questo pesa in modo asimmetrico sulla giornata: la scheda sulla Fed (`news_04`) ha **quattro asset su otto** in questa condizione — e sono proprio tassi, dollaro e oro, cioè il canale *primario* di una notizia di politica monetaria. La sua lettura direzionale poggia quindi interamente su `^NDX`, `^GSPC` e `^VIX`. Anche `news_01` perde l'oro, che sarebbe stato l'asset più naturale per un'escalation geopolitica.

Asset ✅ affidabili usati come ancoraggio: `^VIX` (IC +0,27), `^STOXX50E` (+0,16), `^NDX` (+0,16), `EEM` (+0,17).

**Asset senza validazione**: `CRACK_321`, `HO=F`, `TTF=F`, `EXH9.DE`, `^GDAXI` e soprattutto `CAD=X` — quest'ultimo entrato in DB solo il 2026-08-16 — non compaiono in scorecard (meno di 50 previsioni mature). I loro segnali vanno trattati come ipotesi, non come regolarità confermate. Il crack spread in particolare, che è il risultato più interessante della sessione, è anche quello meno validato.

### Qualità dei pool di analoghi

| Scheda | Filtro | N | Livello del filtro | Nota |
|---|---|---|---|---|
| news_01 | `commodity_energy` / `shipping_chokepoint` / neg | 28 | forte (date-locali) | 9 date su 28 appartengono alla crisi 2026 in corso: non sono osservazioni indipendenti |
| news_02 | `macro_data` / `activity_growth` / neg | 28 | forte (date-locali) | mescola sorprese USA, area euro e Giappone: probabile causa dell'assenza di segnale su JPY=X |
| news_03 | `macro_data` / `cny` / neg | 13 | forte, **direzione degradata** | la direzione stretta dava 8 episodi (<12) → inclusi mixed: il pool contiene annunci di stimolo, che sono di segno opposto |
| news_04 | `monetary_policy` / `guidance_pivot` / pos | 25 | forte (date-locali) | token scelto su copertura (`guidance_pivot` 44 vs `rate_decision` 49) e su pertinenza concettuale |
| news_05 | `commodity_energy` / `gas_europe`+`supply_disruption`+`refinery_products` / neg | 13 | forte, **forzato** con `--min-n 5` | senza il forzamento la libreria ricadeva sul pool di tema, dominato da Iran/Hormuz — avrebbe misurato lo shock sbagliato |
| news_06 | `geopolitical` / `tariff_escalation` / neg | 30 | forte (date-locali) | preso dal ramo `geopolitical` perché `regulatory` ha solo 19 episodi in tutto; **solo 2 date su 30 riguardano il Canada** |

Nessuna scheda è sotto la soglia di N=10, quindi nessuna è marcata "INDICATIVE ONLY". Le due più fragili sono comunque `news_03` (direzione degradata) e `news_05` (analoghi non analoghi per causa).

### Lacune emerse

1. **Siccità, logistica fluviale europea e vincoli idrici alla generazione elettrica.** Nessuna research copre il canale. Il `match` su `--keyword drought --keyword rhine` restituisce solo la research Iran/Hormuz (per coincidenza di `primary_theme`) e due corrispondenze da singola keyword. In libreria, `analogues.py labels --theme commodity_energy` dà 4 episodi date-locali su `gas_europe` e 4 su `supply_disruption`: nessuno è una siccità. È un canale che si ripresenta ogni estate dal 2018 e che oggi tocca il minimo storico dal 1880, quindi la lacuna è strutturale, non episodica.
   → prompt di deep research redatto in **`knowledge_base/_prompts/siccita-logistica-fluviale-europa.md`**

2. **Dazi USA-Canada/USMCA e base legale delle tariffe dopo la sentenza della Corte Suprema.** La research esistente sui dazi è centrata sull'asse USA-Cina. Mancano sia il canale bilaterale nordamericano (catene del valore integrate, energia, auto — strutturalmente diverso dal caso cinese, dove i beni attraversano il confine una volta sola) sia — soprattutto — la **dimensione giuridica**: come reagiscono i mercati alle *decisioni giudiziarie* sull'autorità legale che sostiene i dazi. Su 30 episodi disponibili, solo 2 riguardano il Canada e **nessuno** si è svolto dopo una sentenza che invalidava la base legale.
   → prompt di deep research redatto in **`knowledge_base/_prompts/dazi-usa-canada-usmca-base-legale.md`**

3. **De-escalation di alleanze militari (non urgente, segnalata per memoria).** L'ordine di ridurre le esercitazioni congiunte con la Corea del Sud (intl 04) è stato scartato anche perché la libreria copre l'escalation militare (`military_escalation`, 34 episodi date-locali) ma non il suo opposto — il ritiro o ridimensionamento di un impegno di alleanza da parte della potenza garante. Con `EWY`, `EWT` e `SHLD.L` ormai in DB, è un canale che vale la pena coprire se si ripresenta. **Non è stato scritto un prompt**: una sola occorrenza non giustifica ancora una research.

### Da riprendere nei prossimi giorni

- **Mercoledì 19 agosto**: scadenza dei dazi al 50% sul Canada. L'esito è binario e il contenuto informativo vero è giuridico, non commerciale.
- **Dati di attività cinesi di luglio**: pubblicati in giornata dopo la compilazione della scheda `news_03`. La sorpresa rispetto al consenso (vendite al dettaglio +1,5%) è ciò che muove i prezzi, non il livello.
- **Trimestrali dei retailer USA** (Home Depot martedì, Target e Lowe's mercoledì, Walmart giovedì) e **PMI flash di venerdì**: scartate oggi come calendario prospettico, da riprendere a dati pubblicati come verifica incrociata sul consumatore americano — l'ipotesi su cui poggia il rinvio della Fed.
- **CRACK_321 e HO=F** come indicatori guida della trasmissione energia → inflazione, più informativi del Brent.

