# Daily Analysis — 2026-08-18

- **Briefing:** `~/Claude/morning brief/2026-08-18-morning-briefing.html`
- **Generato:** 2026-08-18
- **Catalog KB:** 2026-08-17T08:04:03

Triage del briefing del giorno. Per ogni notizia: decisione (✅ = scheda prodotta, ✖ = scartata), tema/motivazione, e link alla scheda `news_NN.md` quando prodotta. Scope: subset triato — scheda completa solo per notizie che mappano su uno dei 46 asset attualmente in DB (elenco autorevole: `category_asset_map.yaml`) e hanno un analogo storico plausibile. Le notizie sullo stesso tema sono consolidate in un'unica scheda.

## Triage

| # | Sez. | Notizia | Decisione | Tema / Motivazione | Scheda |
|---|------|---------|-----------|--------------------|--------|
| 01 | intl | The US–Iran Memorandum Expires Without Replacement and Trump Says He Has No Interest in Extending It, While Tehran Claims a Hormuz Deal With Oman That Excludes Washington | ✅ | **commodity_energy** — la scadenza senza sostituto del memorandum toglie il contenitore diplomatico al conflitto e tiene strozzato il transito di Hormuz; canale diretto su BZ=F, CRACK_321, HO=F, RB=F. Consolidata con intl 02, intl 07 e fin 02. | [news_01](news_01.md) |
| 02 | intl | Iranian Kamikaze Drones Strike the Private Office of Iraqi Kurdistan’s Prime Minister in Erbil and the Home of the Region’s Intelligence Chief | ✅ *(consolidata)* | Escalation militare dello stesso dossier Iran; nessun canale asset autonomo (il Kurdistan iracheno non ha proxy quotato), ma stabilisce che il vuoto diplomatico non è una pausa tecnica. | [news_01](news_01.md) |
| 03 | intl | Zambia’s Electoral Commission Declares Hakainde Hichilema Re-Elected With About 60% to Mundubile’s 38%, on Turnout of 56.4% | ✖ | Nessun asset dell'universo mappa lo Zambia — né equity né valuta, e il rame non è un canale utilizzabile (produzione zambiana ~4% dell'offerta mondiale, nessun episodio del pool la coinvolge). Rischio politico reale, trasmissione ai nostri 46 asset assente. |  |
| 04 | intl | Kushner and Netanyahu Agree That a US General Should Supervise Hamas’s Weapons Handover and That No Gaza Reconstruction Begins Before Disarmament | ✖ | Passo diplomatico su un percorso senza scadenza né trasmissione asset discreta: il canale energetico di Gaza è nullo e non è stato messo a Hamas. Il dossier mediorientale è coperto da news_01 sul lato che muove i mercati. |  |
| 05 | intl | Ukraine Hits Moscow Oblast Overnight With Roughly 200 Drones Downed Over the Region and Says It Has Now Disabled Seven of Russia’s Ten Largest Wildberries Logistics Centres | ✖ | La selezione del bersaglio è **esplicitamente non energetica** — centri logistici di e-commerce, non raffinerie. Manca quindi il canale CRACK_321/HO=F che renderebbe la notizia mappabile; l'effetto mira ai prezzi al consumo russi, che non abbiamo in DB. |  |
| 06 | intl | The Flores Earthquake Toll Rises to at Least 68 With About 12,800 Displaced as Indonesia Marked Independence Day | ✖ | IDR=X ed EIDO coprono l'Indonesia, ma un sisma con questo perimetro (isola periferica, nessun distretto industriale o hub di export coinvolto) non ha storicamente prodotto reazione misurabile su valuta o equity nazionale. Tragedia umanitaria, non shock di mercato. |  |
| 07 | intl | Iran’s Army Chief Offers a $30,000 Bounty for Killing or Capturing American Soldiers, Doubled if Carried Out by a Woman | ✅ *(consolidata)* | Incitamento formale senza programma operativo: rileva come misura del restringimento dello spazio negoziale, non come evento asset autonomo. | [news_01](news_01.md) |
| 08 | intl | Seoul Says Ulchi Freedom Shield Is “Proceeding as Planned” Despite Trump’s Order to Substantially Reduce It | ✖ | EWY (Corea) è in DB dal 2026-08-10, quindi sarebbe **tecnicamente mappabile**. Scartata perché il mercato l'ha già risolta in senso benigno nella seduta stessa (Kospi +1,9% alla riapertura post-festività): manca la sorpresa non ancora prezzata che rende sensato un event study. |  |
| 09 | intl | Erdogan Says Israeli Strikes on Lebanon and Syria Now Threaten Turkey, and Netanyahu Calls Him an “Antisemitic Dictator” | ✖ | Scambio di dichiarazioni senza atto materiale. Nessun asset turco in DB e nessun canale di trasmissione all'universo attuale; rischio di secondo ordine sul dossier già coperto da news_01. |  |
| 10 | intl | An African Union Peace and Security Council Delegation Meets Burhan in Khartoum — the Bloc’s First Visit Since the 2021 Coup | ✖ | Passo procedurale di rientro dell'Unione Africana in un dossier da cui era assente dal 2021. Nessun asset sudanese o proxy regionale in DB, nessun canale commodity attivato. |  |
| 01 | fin | China’s July Activity Data Misses Across the Board: Retail Sales +0.6% Against +1.5% Expected, Industrial Output +4.5% Against +4.8%, Fixed-Asset Investment −6.7% Against −6.2% | ✅ | **macro_data** — sorpresa negativa su tutte e tre le voci, con la debolezza che esce dall'immobiliare (investimenti ex-property −3,7%). Canali diretti CNY=X, HG=F, EEM; secondari ^STOXX50E, BZ=F, ^VIX. | [news_03](news_03.md) |
| 02 | fin | Crude Rises for a Third Straight Session After Trump Rules Out Extending the Interim Deal — West Texas Intermediate Above $85, Brent Near $91.5 | ✅ *(consolidata)* | È la manifestazione di prezzo della stessa notizia (scadenza del memorandum). Il dettaglio sui prodotti raffinati — benzina +57%, gasolio +98% a/a contro greggio +38% — è il cuore analitico di quella scheda. | [news_01](news_01.md) |
| 03 | fin | The Japanese Ten-Year Yield Hits 2.93%, Its Highest Since October 1996, With Five-Year and Two-Year Yields at Multi-Decade Records on September Hike Bets | ✅ | **monetary_policy** — epicentro strutturale del selloff globale: la normalizzazione BoJ ritira il compratore giapponese dai sovrani esteri. Consolidata con fin 04, 05, 06, 09 e la One Thing to Watch. | [news_02](news_02.md) |
| 04 | fin | The US Thirty-Year Yield Reaches a 19-Year High and the Ten-Year Sits Near 4.71–4.73% as Michigan Inflation Expectations Stay Above 4% for a Fifth Month | ✅ *(consolidata)* | Il canale americano dello stesso fenomeno: curva che si irripidisce sulle aspettative di inflazione mentre il front-end prezza un hold al 67%. È **l'unica delle quattro curve che abbiamo in DB** (^TNX, IEF). | [news_02](news_02.md) |
| 05 | fin | Australia’s Ten-Year Yield Pushes Above 5.04% and the Thirty-Year to 5.60% as the Reserve Bank Keeps the Door Open to Another Hike | ✅ *(consolidata)* | Terza gamba del selloff sincronizzato. ⚠ Nessun asset australiano in DB: discussa qualitativamente, non misurabile. | [news_02](news_02.md) |
| 06 | fin | UK Gilt Yields Hold Above 5.05% Into Wednesday’s July Inflation Print, the Highest Long-Rate in the G7 | ✅ *(consolidata)* | Quarta gamba, e il caso più netto di premio a termine che i fondamentali domestici non giustificano (inflazione 2,6%, disoccupazione in salita al 4,9%, salari al 3,4%). ⚠ Gilt non in DB. | [news_02](news_02.md) |
| 07 | fin | Automotive Rules Are Blocking a Canada–US Deal With 50% Tariffs Due Wednesday: Washington Holding at a 15% Minimum, Ottawa Pressing for 10% | ✅ | **regulatory** — scadenza a 36 ore con gap di 5 punti sul dossier auto. Canale diretto CAD=X (in DB dal 2026-08-16); il vero oggetto è il **test della base legale Section 338**, che vale ben oltre il Canada. | [news_04](news_04.md) |
| 08 | fin | Home Depot Reports Before the Open as the First Company-Level Read on the Quarter US Retail Sales Fell 0.6%, With Consensus at $4.71 Earnings per Share on About $47bn | ✖ | `corporate_idiosyncratic` su un ticker non in DB (universo cross-asset, non single-name) e su **numeri di consenso pre-release, non risultati pubblicati**. Il proxy ^GSPC è troppo diluito, e la scorecard 2026-W34 dà a questo tema l'unico IC negativo (−0,06, N=72). |  |
| 09 | fin | Gold Holds Above $4,400 at Roughly $4,430 an Ounce, up 10.5% in a Month and 33.5% Year on Year | ✅ *(consolidata)* | Come scheda propria sarebbe un movimento di prezzo senza shock-notizia discreto, e GC=F è ❌ controproducente in scorecard. Come **co-movimento anomalo con i rendimenti** è invece un pezzo essenziale della lettura di credibilità. | [news_02](news_02.md) |
| 10 | fin | The Rhine at Kaub Falls Further to Roughly 16–17 Centimetres, With Forecasters Pointing to Single-Digit Readings by Midweek | ✅ | **commodity_energy** (shock di offerta logistico) — canali TTF=F, EXH9.DE, ^GDAXI, HO=F, EURUSD=X. Durata attesa fino a ottobre; ING stimò 0,3 punti di PIL tedesco per la siccità 2018 e ne attende di più quest'anno. | [news_05](news_05.md) |

## 🔍 One Thing to Watch Today

**The Synchronised Long-End Selloff — Because Four Major Bond Markets Are at Multi-Decade Highs Simultaneously, and Oil Just Removed the One Assumption Holding Them Together**

Yesterday the question was whether the US–Iran ceasefire would be extended. It was not, and Trump has said he does not want to extend it — so the risk that was binary is now resolved in the direction that keeps energy prices elevated, with West Texas Intermediate above $85 and Brent near $91.5 after a third consecutive up session. What deserves attention today is the second-order effect, which is showing up in an unusually clean form. The Japanese ten-year yield is at 2.93%, the highest since October 1996, with the five-year at an all-time high. Australia’s ten-year is above 5.04% and its thirty-year at 5.60%. The UK ten-year is above 5.05%. The US thirty-year is at a 19-year high with the ten-year near 4.71%. Four independent central banks, four different domestic cycles, one common move — and in each case the driver is an inflation expectation, not a growth forecast: Michigan year-ahead expectations above 4% for a fifth month, the Bank of Japan expected to hike in September, the Reserve Bank of Australia refusing to close the door on 4.60%. The reason this is the thing to watch rather than merely a thing to note is what it does to the equity and credit complex. Monday’s US session fell with Meta down 3.5% and Microsoft down 3.0% — the long-duration names took the hit, which is the correct response to a term-premium shock rather than a growth shock. Gold at $4,430 rising in the same tape confirms the interpretation: this is a repricing of policy credibility, not a flight to the safety of government bonds, which is precisely why the bonds are not rallying. Three markers through the session: whether the US thirty-year extends beyond yesterday’s 19-year high once the cash session opens; whether Home Depot’s comparable sales corroborate the 0.6% fall in July US retail sales, which would put a genuine demand contraction underneath an inflation-driven yield move; and whether the Canada–US automotive gap — 15% against 10% — closes before the 50% Section 338 tariffs take effect tomorrow, since a tariff shock landing on a market already pricing an inflation regime is the combination with no clean central-bank answer.

## Sintesi di sessione

**Bilancio del triage**: 20 notizie esaminate → **5 schede prodotte**, 11 notizie scartate, 4 consolidate dentro schede esistenti (più 2 che sono la manifestazione di prezzo di notizie già tenute). In totale 9 righe su 20 finiscono in una scheda.

---

### 1. Il tema dominante: tre shock di offerta indipendenti nello stesso trimestre

Il briefing di oggi ha una struttura insolitamente coerente, e la coerenza sta in una constatazione che nessuna singola notizia enuncia: **stanno atterrando contemporaneamente tre shock di offerta scollegati fra loro**.

1. **Energia** (`news_01`) — il memorandum USA-Iran scade senza sostituto, il transito di Hormuz resta a una frazione del normale, e il rincaro si scarica sui prodotti raffinati molto più che sul greggio: benzina +57% e gasolio +98% anno su anno, contro un Brent a +38%.
2. **Commercio** (`news_04`) — dazi americani al 50% sulle merci canadesi in vigore mercoledì salvo intesa, bloccati su cinque punti percentuali di differenza sul dossier auto, imposti con una base giuridica (Section 338) mai testata prima.
3. **Logistica** (`news_05`) — il Reno a Kaub a 16-17 centimetri, minimo assoluto dal 1880, con previsioni sotto i 10 entro metà settimana e disruption potenzialmente fino a ottobre. BASF, Thyssenkrupp e Lanxess stanno **riorganizzando** le catene di fornitura anziché pagare sovrapprezzi: la reazione a un problema strutturale, non temporaneo.

Uno shock di offerta alza i prezzi e riduce la produzione simultaneamente. Preso singolarmente, ciascuno è un evento che una banca centrale può ragionevolmente ignorare ("guardare attraverso"), perché temporaneo. **Tre insieme diventano difficili da chiamare temporanei**, ed è esattamente questo che collega tutte le schede alla quarta.

### 2. La conseguenza: il selloff sincronizzato della parte lunga (`news_02`)

Quattro mercati obbligazionari maggiori — Giappone, Stati Uniti, Australia, Regno Unito — su massimi pluridecennali nello stesso giorno, con quattro banche centrali diverse e quattro cicli domestici diversi. Il driver comune non è la crescita ma l'aspettativa di inflazione unita al dubbio sulla reazione delle banche centrali. Due conferme indipendenti nel briefing stesso:

- la curva americana si irripidisce mentre il front-end prezza il 67% di probabilità che la Fed **non** muova a settembre. Chi si aspetta inazione contro l'inflazione chiede più rendimento per il rischio di duration — è la definizione di **premio a termine**;
- l'oro è ai massimi (~$4.430, +10,5% in un mese) *insieme* ai rendimenti nominali, che è l'opposto della relazione normale. Non è un trade sui tassi reali, è una copertura contro la credibilità della risposta di policy.

Il pezzo strutturale è il Giappone: con il decennale al 2,93% viene meno la convenienza per le istituzioni giapponesi a esportare risparmio verso Treasury e sovrani europei. **Un compratore strutturale di debito altrui si ritira**, e la sua uscita alza i rendimenti ovunque.

### 3. La contro-forza: la Cina (`news_03`)

Unica notizia del giorno che tira in direzione opposta. I dati di attività di luglio mancano su tutte e tre le voci, e la novità è che la debolezza **esce dall'immobiliare** (investimenti ex-property a −3,7%): non è più una crisi settoriale. Una domanda cinese debole è disinflazionistica per il mondo e ribassista sul greggio — l'event study dà `BZ=F` in calo (media −1,20% a T+10) su un asset che la scorecard marca ✅ affidabile.

Convivono quindi sul petrolio **due spinte opposte**: offerta iraniana strozzata che spinge in su, domanda cinese che cede e spinge in giù. Storicamente il canale dell'offerta domina nel breve e quello della domanda nel medio, ed è probabilmente la ragione per cui il Brent nell'event study della `news_01` mostra mediane così modeste (+0,78% a T+10) a fronte di un `CRACK_321` che si allarga nettamente (+7,65%). **Da tenere d'occhio: la configurazione in cui il greggio scende mentre i prodotti raffinati continuano a salire.**

Nota di contrasto interessante: nello stesso giorno il decennale giapponese è al 2,93% e quello cinese all'1,68%. Due economie asiatiche, curve opposte. Il Giappone esce dalla deflazione, la Cina rischia di entrarci.

---

### 4. Letture trasversali sugli asset

**Il canale dei prodotti raffinati batte il canale del greggio.** È il risultato metodologicamente più solido della giornata, ed esce indipendentemente da due schede diverse. Nella `news_01`, `CRACK_321` ha mediana +5,65% a T+3 con anche il quartile basso positivo (+1,35%) — cioè oltre tre quarti dei 28 episodi hanno visto il margine allargarsi entro tre giorni. Nella `news_05`, `HO=F` ha mediana +3,84% a T+3, di nuovo con p25 positivo. **Due pool di episodi diversi, stesso segnale**: quando lo shock è logistico, il prezzo si forma sul prodotto e sul margine, non sul barile. Vale la pena ricordare che CRACK_321 è in DB solo dal 2026-08-11: senza quell'aggiunta, la scheda principale di oggi avrebbe mancato il suo canale migliore.

**La divergenza Europa/Stati Uniti sull'energia.** Sempre nella `news_01`: l'S&P 500 sale (mediana +1,15% a T+10), l'Euro Stoxx 50 scende (−0,86%). Non è statistica, è contabilità — gli Stati Uniti sono esportatori netti di energia, l'area euro importatrice netta, e lo stesso rincaro sposta reddito dall'una all'altra.

**L'euro è l'asset con il campione più coerente della giornata — e con IC nullo.** Nella `news_05`, `EURUSD=X` scende in modo monotono (−0,34% a T+1 → −0,87% a T+10), con media e mediana quasi identiche, la deviazione standard più bassa fra tutti gli asset del giorno, e da T+3 in poi **perfino il quartile alto negativo**. È la regolarità statistica più netta emersa oggi. Ed è anche un promemoria della differenza fra regolarità e capacità predittiva: la scorecard dà `EURUSD=X` a IC −0,00 con hit-rate 50% su 193 previsioni. Il campione è coerente, il sistema storicamente non ne ha ricavato nulla. Riportata come osservazione, non come previsione.

**Il rischio è nelle code, non nelle mediane.** Ricorre in tre schede su cinque: `TTF=F` con media +7,22% a T+5 contro mediana +0,08%; `^VIX` nella `news_04` con media +4,35% a T+3 contro mediana −5,76%; `^GSPC` nella `news_04` con mediana positiva e media a zero. In tutti i casi il caso tipico è mite e il campione contiene pochi episodi molto violenti. La lettura operativa: oggi il sistema non indica direzioni forti, indica **dove il caso avverso è grande**.

### 5. Vincoli dalla scorecard 2026-W34 (sezione 5-bis)

Asset marcati **❌ controproducente**, su cui **nessuna direzione è stata derivata** in nessuna scheda: `DX-Y.NYB` (IC −0,16, hit-rate 32%, N=156), `GC=F` (−0,07, N=302), `IEF` (−0,29, N=66), `^TNX` (−0,20, N=208).

Questo vincolo ha morso in modo particolarmente pesante oggi, e vale la pena registrarlo: **la notizia dominante della giornata è un fenomeno obbligazionario, e i due asset obbligazionari del database sono entrambi vietati per la direzione**. La `news_02` ha potuto derivare letture direzionali solo su `^NDX`, `^STOXX50E`, `^VIX` (✅ affidabili) e con cautela su `^GSPC`. Su tassi, dollaro e oro l'event study è riportato in tabella con dichiarazione esplicita di inaffidabilità del segno.

Asset ✅ affidabili usati come ancore della lettura: `^STOXX50E` (IC +0,17), `^VIX` (+0,17, hit-rate 63%), `^NDX` (+0,17), `EEM` (+0,17, hit-rate 61%), `BZ=F` (+0,13, hit-rate 61%).

Asset **non ancora validati** (meno di 50 previsioni mature) e quindi usati con cautela esplicita: `CAD=X` (in DB da due giorni), `HG=F`, `CNY=X`, `TTF=F`, `EXH9.DE`, `^GDAXI`, `HO=F`, `CRACK_321`.

### 6. Qualità dei pool di analoghi

| Scheda | Tema | Sotto-tema | Livello filtro | N | Regime |
|---|---|---|---|---|---|
| news_01 | commodity_energy | `shipping_chokepoint` | **forte** (date-locale, 32 disp.) | 28 | eterogeneo (2012→2026) |
| news_02 | monetary_policy | `guidance_pivot` | **forte** (date-locale, 44 disp.) | 30 | omogeneo (2022-09→2026-06) |
| news_03 | macro_data | `activity_growth` | **forte** (date-locale, 29 disp.) | 28 | eterogeneo, non Cina-specifico |
| news_04 | regulatory | `tariff_escalation` | **forte** (date-locale, 16 disp.) | 16 | due regimi distinti (2018-19 / 2025-26) |
| news_05 | commodity_energy | `supply_disruption`+`gas_europe`+`refinery_products` | **forte** solo in combinazione | 13 | shock energetici, non idrologici |

Tutti e cinque i pool hanno agganciato il **filtro date-locale forte**, il che è un buon risultato rispetto alle sessioni in cui la libreria ricadeva sui sotto-temi di documento. Il caso `news_05` è istruttivo: `supply_disruption` da solo scendeva a 4 episodi date-locali e la libreria ricadeva sul filtro debole; la combinazione di tre token ha riportato il pool a 14 sul livello forte. **Vale come tecnica riutilizzabile**: su temi a bassa copertura, combinare token affini invece di allargare a tutto il tema.

Il pool più debole per costruzione è quello della `news_04` (N=16, dieci episodi appartenenti a un regime tariffario strutturalmente diverso). Non è stato potato perché escludere il blocco 2018-19 lo avrebbe portato a N=6.

### 7. Lacune emerse

**A. Premio a termine cross-mercato — NUOVA, segnalata oggi.** Il catalogo ha uno studio per ciascuna banca centrale (Fed, BoJ, Regno Unito) ma nessuno sul canale che le collega: il premio a termine come fenomeno globale, la fine del Giappone come esportatore netto di risparmio, e la distinzione — cruciale per la pipeline — fra selloff guidati dal premio a termine e selloff guidati dalle aspettative sui tassi. La libreria non ha alcun token per un movimento *sincronizzato* (`curve` e `curve_steepening` esistono solo al livello debole di documento). Un tale studio servirebbe anche a **diagnosticare il difetto peggiore del sistema**: `^TNX` a IC −0,20 e `IEF` a IC −0,29 significa che sui tassi prevediamo sistematicamente al contrario, e l'ipotesi più plausibile è che il campione mescoli i due tipi di episodio, che hanno segno opposto sull'azionario.
→ Prompt di deep research: **`knowledge_base/_prompts/premio-a-termine-globale-selloff-sincronizzati.md`**

**B. Siccità e logistica fluviale europea — RICORRENTE (2ª segnalazione).** Già segnalata il 2026-08-17; oggi si ripresenta con il Reno al minimo assoluto della serie dal 1880. Nel pool della `news_05` **solo 2 episodi su 13** sono precedenti idrologici diretti (agosto 2022): gli altri undici sono shock energetici di origine politica, che condividono il meccanismo ma non la causa. La priorità sale: l'evento è in corso e potrebbe durare fino a ottobre.
→ Prompt già pronto (non eseguito): **`knowledge_base/_prompts/siccita-logistica-fluviale-europa.md`**

**C. Dazi USA-Canada / USMCA e base legale post-Corte Suprema — RICORRENTE (2ª segnalazione).** Già segnalata il 2026-08-17; oggi la scadenza è a 36 ore. La research esistente sui dazi è centrata sull'asse USA-Cina, e la dimensione **giuridica** (quale autorità sostiene i dazi dopo l'annullamento del febbraio 2026) non ha alcun precedente nel campione. Con `CAD=X` in DB da due giorni e mai validato in scorecard, la `news_04` misura la reazione a eventi che in gran parte non riguardavano il Canada.
→ Prompt già pronto (non eseguito): **`knowledge_base/_prompts/dazi-usa-canada-usmca-base-legale.md`**

### 8. Lacune di **universo asset** (non di knowledge base)

Distinte dalle precedenti perché non si risolvono con una research ma estendendo `bootstrap_market_data.py`. Emerse oggi, in ordine di impatto:

1. **Rendimenti sovrani non-USA.** La notizia dominante del giorno riguarda quattro curve; ne abbiamo **una** (`^TNX`, e solo il 10 anni — il fenomeno del 2026 è soprattutto sul 30 anni). Mancano gilt UK, JGB giapponese e ACGB australiano. Questa è la lacuna di universo più costosa mai emersa: un intero tema di giornata è misurabile solo di riflesso.
2. **Azionario canadese (TSX).** La `news_04` non può misurare l'asset più direttamente colpito, e il briefing segnala che si è già ritirato da un massimo storico.
3. **Chimica europea.** La `news_05` usa `^GDAXI` come proxy di BASF, Thyssenkrupp e Lanxess: molto diluito. Un ETF settoriale sulla chimica europea (tipo STOXX Europe 600 Chemicals) coprirebbe un canale che con il Reno si ripresenta ogni estate.

#### Interventi fatti sulle lacune (2026-08-18, sessione di manutenzione)

**Tutte e tre le lacune di universo — risolte. Universo 46 → 52 asset.**

| Ticker | Copre | Storia | Note |
|---|---|---|---|
| `^TYX` | 30Y USA | dal 2011-01-03 | **rendimento**, la scadenza dove vive il premio a termine |
| `IGLT.L` | gilt UK | dal 2011-01-04 | prezzo ETF |
| `1482.T` | JGB Giappone | dal 2016-05-25 | prezzo ETF, storia più corta |
| `VGB.AX` | ACGB Australia | dal 2012-04-24 | prezzo ETF |
| `^GSPTSE` | azionario Canada | dal 2011-01-04 | completa `CAD=X` del 2026-08-16 |
| `EXV7.DE` | chimica europea | dal 2011-01-03 | STOXX Europe 600 Chemicals |

Mappati in `category_asset_map.yaml`: le quattro curve sotto `monetary_policy.primary`
e `fiscal_policy.secondary`, `^GSPTSE` sotto `regulatory`/`fiscal_policy`, `EXV7.DE`
sotto `commodity_energy.secondary`.

⚠ **Attenzione al segno, ed è strutturale.** La via "rendimenti" (come `BTP_BUND_SPREAD`
via Stooq) non era percorribile — v. sotto — quindi tre curve su quattro entrano come
**prezzi di ETF**, che si muovono *inversi* ai rendimenti. In un selloff sincronizzato
`^TYX` sale mentre `IGLT.L`, `1482.T` e `VGB.AX` scendono: è coerenza, non divergenza.
Va dichiarato in ogni scheda che ne usa due insieme (ora scritto nel runbook).

**🔴 Difetto trovato per strada, non segnalato da nessuna analisi: `BTP_BUND_SPREAD` è
fermo al 2026-08-07.** Stooq risponde **404 su ogni simbolo di rendimento benchmark**,
compresi `10YITY.B`/`10YDEY.B` che funzionavano: non è un problema di simbolo ma
dell'endpoint o della `STOOQ_API_KEY` (le chiavi scadono e vanno riemesse col captcha).
Finché non si sistema, lo spread resta valido per gli episodi **storici** ma non va letto
come dato corrente. Serve la tua chiave nuova — è l'unico passo che non posso fare io.

**Lacuna A (premio a termine) — solo la parte di codice, e il risultato è negativo.**
La research resta a te. Ho aggiunto i token `term_premium`, `sovereign_auction`,
`synchronized_selloff`, ma la misura dice che **non funzionano e non è un problema di
calibrazione**: su 2.805 contesti date-locali portano rispettivamente 5, 0 e 1 episodio.
I pattern sono corretti (i match trovati sono veri), ma quel vocabolario compare **144
volte nelle schede e solo 5 volte vicino a una data**: vive nella prosa, mentre le
etichette date-locali vedono solo il testo attorno alla data, che nelle righe-episodio è
telegrafico («2017-12-22 — Trump firma il TCJA»). Lasciati come *semi* con un avviso
esplicito in tassonomia di **non usarli** in `find --subtheme` finché `labels` non mostra
copertura. La correzione vera è a monte: il runbook ora chiede che ogni riga-episodio
nomini il **meccanismo**, non solo il fatto.

**Bug collaterale corretto.** Cercando la causa ho trovato che l'intestazione delle schede
(`**Data analisi**`, `**Fonte**`, `**Slug**`) finiva nei contesti date-locali: **386 su
2.944, il 13,1%**. Lo `**Slug**` è una collana di parole chiave (`warsh-fed-chair-fomc-split`)
che spalmava mezzo vocabolario sulla data di analisi. Escluso in `analogues.py` come già si
faceva con le righe-argomento; contaminazione ora **0%**, nessuna regressione sui pool
esistenti.

---

### 9. Materiale utilizzabile per contenuti

Tre spunti con una tesi già formata e numeri a supporto:

- **"Il barile non è il prezzo che conta"** — perché in uno shock logistico il margine di raffinazione è più informativo del greggio, con l'evidenza di due event study indipendenti (CRACK_321 +5,65% e HO=F +3,84% a T+3, entrambi con p25 positivo) e la conferma nei dati odierni (benzina +57%, gasolio +98%, greggio +38%).
- **"Oro e rendimenti che salgono insieme"** — l'anomalia che segnala un repricing di credibilità anziché un trade sui tassi reali, e perché in questa configurazione i titoli di Stato *non* rimbalzano.
- **"Tre shock di offerta e nessuna risposta di banca centrale"** — Hormuz, Section 338 e il Reno nello stesso trimestre, e perché la regola del "guardare attraverso" gli shock temporanei smette di funzionare quando ne arrivano tre insieme e le aspettative sono già sopra il 4%.

Nota di onestà metodologica da mantenere in qualunque contenuto derivato: **nessuna scheda di oggi produce un segnale direzionale forte**. La giornata è ricca di meccanismi chiari e povera di previsioni robuste, e i quattro asset più centrali alla notizia dominante sono proprio quelli su cui la scorecard vieta di trarre una direzione.


