# Russia-Ucraina: attrito energetico e regime sanzioni — mappa di episodi datati per event study (2022–2026)

## 1. Sintesi esecutiva

La tesi centrale di questo studio è che la guerra Russia-Ucraina non agisce sui mercati finanziari come un blocco unico, ma attraverso canali di trasmissione distinti la cui rilevanza relativa cambia in modo netto da un regime all'altro. Confondere i regimi distrugge il segnale di un event study. Nel 2022 il canale dominante è stato il gas europeo (taglio dei flussi Gazprom → TTF → equity EZ, EUR, inflazione → BCE) e il risk-off acuto; nel 2023 il canale è diventato la riallocazione dei flussi petroliferi sotto price cap (sconto Urals-Brent, re-routing verso India/Cina/Turchia), con effetti modesti sul Brent; nel 2024 il canale prevalente è stato l'attrito sulle raffinerie russe (attacchi droni → prodotti raffinati, diesel), con un Brent relativamente stabile; nel 2025-2026 i canali si sovrappongono e contaminano (sanzioni USA su Rosneft/Lukoil, shock Hormuz, OPEC+), rendendo l'attribuzione difficile.

L'event study è più affidabile su shock discreti, datati e a sorpresa con canale di trasmissione chiaro: invasione (24-02-2022), Nord Stream (26-09-2022), sanzioni USA Rosneft/Lukoil (22-10-2025). È meno affidabile dove l'evento era ampiamente anticipato (price cap del 05-12-2022, embargo UE già noto da sei mesi; fine transito gas 01-01-2025), dove il segnale è contaminato da fattori concomitanti (ciclo inflazione EZ 2022, shock Hormuz 2026), o dove la variabile-canale (TTF, Urals) non è nel database e va trattata come covariata esterna. Per ogni episodio occorre specificare cosa era noto/atteso alla data-ancora, evitando look-ahead.

## 2. Tassonomia dei canali di trasmissione

### 2.1 Gas europeo (canale dominante 2022)

Il meccanismo è una catena causale a più stadi. Un taglio dei flussi russi (Gazprom riduce o azzera Nord Stream 1) restringe l'offerta su un mercato a domanda fortemente anelastica nel breve, perché il gas serve a riscaldamento, generazione elettrica e processi industriali difficili da sostituire rapidamente. Il prezzo di riferimento TTF esplode. Lo studio ESMA sul picco di agosto 2022 documenta una domanda altamente anelastica: i volumi scambiati erano solo leggermente inferiori rispetto a un anno prima, nonostante prezzi multipli, "likely driven by the need to replenish reserves for the winter given the drop in Russian pipeline supply". Il rincaro si trasmette alla bolletta industriale (margini compressi, soprattutto in settori energy-intensive tedeschi), all'equity dell'eurozona (^GDAXI, ^STOXX50E particolarmente esposti), all'euro (deterioramento delle ragioni di scambio energetiche) e all'inflazione.

La quantificazione del costo macroeconomico è netta: secondo l'ECB Economic Bulletin (Issue 2/2023, "Who foots the bill? The uneven impact of the recent energy price shock"), il deterioramento delle ragioni di scambio energetiche "induced a cumulative loss of 2.4 percentage points of GDP between the third quarter of 2021 and the third quarter of 2022, the largest five-quarter loss on record since the launch of the euro" (scomposto in circa -1,7 pp via reddito aggregato e +0,7 pp via spese finali). Da qui la reazione BCE: la trasmissione dello shock gas all'inflazione core ha reso il ciclo di rialzi del 2022-2023 più aggressivo. La letteratura BCE (Adolfsen et al., 2024, *Journal of International Money and Finance*, "Gas price shocks and euro area inflation"; De Santis e Tornese, 2023; Neri et al., 2023, Bank of Italy Occasional Paper) stima che gli shock di offerta di gas alzano l'HICP energy di circa 1,1% e l'HICP headline di circa 0,1%, con effetti più ampi e persistenti di quelli del petrolio. La sintesi più recente (Neri, CEPR/VoxEU 2026) ribadisce che "oil supply shocks have immediate but short-lived effects, while gas supply shocks have broader and more persistent effects on euro area inflation", e che il pass-through è più forte in un regime di inflazione energetica o core già elevata.

**Nota DB**: TTF non è nel database. Va trattato come covariata/variabile esterna, ma i suoi effetti si mappano su ^GDAXI, ^STOXX50E, EURUSD=X e, indirettamente, su BTP_BUND_SPREAD.

### 2.2 Petrolio / Brent (canale dominante 2023-2024, riemergente 2025)

Il petrolio è l'unico canale energetico direttamente nel database (BZ=F). Il meccanismo distingue tre sotto-canali. Primo, lo shock di offerta puro: la prospettiva di perdere greggio russo dal mercato globale alza il Brent (come a marzo 2022). Secondo, il regime price cap + embargo: a partire da fine 2022, l'embargo UE sul greggio seaborne e il price cap G7 a 60 $/barile hanno deviato i flussi russi verso Asia senza ridurli, creando uno sconto Urals-Brent ma mantenendo l'offerta globale e quindi un Brent relativamente stabile. La letteratura peer-reviewed conferma il punto: Babina, Hilgenstock, Itskhoki, Mironov, Ribakova e Shapoval (2025, "Russian oil exports under international sanctions", *Energy Economics*) trovano che il volume di greggio russo esportato è rimasto stabile dopo invasione e sanzioni, mentre i ricavi sono calati nel 1° trimestre 2023; Kilian, Rapson e Schipper (2026, "The Impact of the 2022 Oil Embargo and Price Cap on Russian Oil Prices") concludono che l'effetto incrementale del price cap sul prezzo FOB russo a marzo 2023 era "negligible", essendo l'embargo UE il driver dominante dello sconto. Terzo, l'attrito sulla capacità di raffinazione (2024-2025): gli attacchi droni ucraini alle raffinerie russe colpiscono i prodotti raffinati (diesel) più del greggio, perché la Russia, non potendo raffinare, sposta più greggio verso l'export mantenendo stabili i volumi crude export ma riducendo i product export (analisi Baker Institute, 2026).

**Nota DB**: lo sconto Urals-Brent (tra $20-35/barile per gran parte del 2022-inizio 2023 secondo Kilian et al.), il diesel/gasolio e i crack spread dei prodotti non sono nel DB. Vanno trattati come esterni; l'effetto osservabile è su BZ=F.

### 2.3 Risk-off / safe-haven

Un'escalation militare discreta e a sorpresa innesca un riposizionamento verso asset rifugio: oro (GC=F), dollaro (DX-Y.NYB), volatilità (^VIX), Treasury e Bund. Il meccanismo è il classico flight-to-quality. Il caso dell'invasione è istruttivo: l'oro salì subito — secondo il World Gold Council (Gold Market Commentary, febbraio 2022) "The LBMA Gold Price PM jumped 6% in February, ending the month at US$1,910/oz. It's the strongest m-o-m performance since May 2021", con picco intra-mese intorno a $1.936/oz — il VIX impennò e le equity europee crollarono. Tuttavia, il canale safe-haven dell'oro è instabile e di breve durata: dopo l'impennata iniziale, la stretta Fed del 2022 (rialzo dei tassi reali, dollaro forte) sovrastò la domanda rifugio e l'oro rese circa -3,5% nei 12 mesi a febbraio 2023. La firma del canale safe-haven è quindi tipicamente di breve orizzonte (T+1/T+5), e per l'oro va distinta dalla componente strutturale di acquisti delle banche centrali post-congelamento delle riserve russe (1.082 tonnellate nel 2022, record da oltre 50 anni secondo i dati World Gold Council).

### 2.4 Frammentazione / periferia

Uno shock energetico asimmetrico (la periferia EZ più esposta o più indebitata) si trasmette agli spread sovrani e all'equity periferica (FTSEMIB.MI, BTP_BUND_SPREAD). Il meccanismo: timori di sostenibilità del debito in un contesto di stretta monetaria e shock energetico → allargamento dello spread BTP-Bund → pressione sulle banche periferiche e sull'euro. Nel 2022 lo spread BTP-Bund raggiunse un picco di circa 250 punti base a giugno (European Parliament, briefing TPI 2022), spingendo la BCE a una riunione ad hoc il 15 giugno e poi alla creazione del TPI (Transmission Protection Instrument, annunciato il 21-07-2022). La firma di questo canale è una reazione di FTSEMIB.MI e BTP_BUND_SPREAD più marcata della media EZ. Va però notato che parte dell'allargamento del 2022 era guidato da fattori globali di risk-off e dalla stretta monetaria più che dalla guerra in sé, e che la letteratura (European Parliament, Intereconomics 2023) discute se il TPI sia mai stato attivato — non lo è stato — e quanto la sua sola esistenza abbia compresso gli spread.

### 2.5 Difesa/industria e re-routing commerciale

L'escalation e l'aumento della spesa militare favoriscono i titoli della difesa europea; il re-routing dei flussi russi avvantaggia gli importatori asiatici (India, Cina, Turchia, principali destinatari del greggio russo scontato). Questi effetti sono in larga parte **non misurabili** sui 26 asset del DB: gli indici difesa europea non sono presenti. L'unico asset con esposizione tangenziale è EEM (mercati emergenti, che include esposizione a Cina/India beneficiari del greggio scontato) e HG=F (rame, proxy del ciclo industriale globale). Vanno segnalati come esterni.

## 3. Catalogo episodi-ancora datati

Nelle note si specifica cosa era noto/atteso alla data, per evitare look-ahead. La direzione attesa è dal punto di vista dell'asset-canale primario. Le date sono pensate per essere precise e isolabili come `--events` del pipeline.

| Data ISO | Evento | Tipo | Direzione attesa | Asset-canale (DB) | Note no-look-ahead |
|---|---|---|---|---|---|
| 2022-02-21 | Russia riconosce Donetsk e Luhansk; sospensione certificazione Nord Stream 2 (22-02) | escalation militare | risk-off; Brent ↑ | ^VIX↑, GC=F↑, ^STOXX50E↓ | Pre-invasione; mercati prezzavano rischio ma non invasione su vasta scala |
| 2022-02-24 | Invasione su vasta scala dell'Ucraina | escalation militare | risk-off acuto; Brent ↑; oro ↑ | BZ=F↑, GC=F↑, ^VIX↑, ^GDAXI↓, FTSEMIB.MI↓, ^STOXX50E↓ | Shock a sorpresa nella portata. Brent >$100 prima volta dal 2014; oro ai massimi da oltre un anno |
| 2022-03-08 | Picco Brent; annuncio ban USA su import energia russa | supply-shock/sanzione | Brent picco | BZ=F↑↑, GC=F↑ | Brent intraday $139,13 (futures, massimo dal 2008); chiusura +4,3% a $123,21; massimo aggiustato per inflazione dal 2014 (EIA) |
| 2022-06-03 | UE adotta 6° pacchetto (Reg. 2022/879): embargo greggio seaborne russo | sanzione | Brent ↑ | BZ=F↑ | Annuncio; effetto legale differito (crude 05-12-2022, prodotti 05-02-2023). Brent >$120 a fine maggio/giugno su prospettiva embargo |
| 2022-06-14 | Gazprom taglia Nord Stream 1 al 40% | supply-shock | TTF↑ → EZ equity↓, EUR↓ | ^GDAXI↓, EURUSD=X↓ | Motivazione "turbina Siemens"; UE parla di weaponizzazione |
| 2022-07-25 | Gazprom taglia NS1 al 20% | supply-shock | TTF↑ → EZ equity↓ | ^GDAXI↓, ^STOXX50E↓ | Ulteriore restrizione |
| 2022-08-22/26 | Picco TTF (>€300/MWh il 26-08) | supply-shock | TTF picco → EZ equity↓, EUR↓ | ^GDAXI↓, EURUSD=X↓ | TTF massimo storico; cinque giorni consecutivi sopra €265/MWh (Consilium); domanda anelastica (ESMA) |
| 2022-08-31 | Gazprom chiude NS1 "per manutenzione"; non riapre più | supply-shock | TTF↑ | ^GDAXI↓, ^STOXX50E↓ | Annuncio 19-08; il 02-09 Gazprom comunica stop indefinito; chiusura di fatto definitiva |
| 2022-09-26 | Sabotaggio Nord Stream (esplosioni) | escalation/supply-shock | risk-off; gas↑ | ^VIX↑, GC=F↑, EURUSD=X↓ | NS1 già fermo; NS2 mai operativo. Effetto più simbolico/strutturale che di flusso |
| 2022-10-05 | OPEC+ annuncia taglio 2 mln bpd | supply-shock | Brent ↑ | BZ=F↑ | Reazione muta: rally anticipato nei giorni precedenti (~$83→$93); cut formalizza in parte sotto-produzione esistente |
| 2022-10-06 | UE adotta 8° pacchetto (base legale price cap) | sanzione | Brent ↑ (limitato) | BZ=F | Risposta ad annessioni; anticipato |
| 2022-12-05 | Entrata in vigore embargo UE greggio seaborne + price cap G7 $60 | sanzione | Brent ↑ (limitato) | BZ=F↑ | Ampiamente atteso (annunciato da ~6 mesi); prezzi salirono fino a ~2% sul giorno, effetto modesto |
| 2023-02-05 | Price cap G7 sui prodotti ($100 premium/$45 discount); embargo prodotti UE | sanzione | diesel↑ (esterno) | BZ=F | Atteso; canale prodotti non in DB |
| 2023-06-23/24 | Ammutinamento Wagner (Prigozhin) | escalation interna | risk-off breve; Brent ↑ | BZ=F↑, ^VIX↑ | A sorpresa; rientrato in <48h; il 26-06 Brent ~+0,8% a ~$74,5 poi reversione ("sigh of relief") |
| 2023 (vari) | Pacchetti UE successivi e prime designazioni shadow fleet | sanzione | marginale | BZ=F | Effetti marginali, enforcement debole |
| 2024-01/03 | Intensificazione attacchi droni ucraini a raffinerie russe | supply-shock (prodotti) | diesel↑ (esterno); Brent ↑ moderato | BZ=F↑ | Campagna progressiva, non evento puntuale; Brent sopra $80; 0,4-0,9 mln bpd di capacità raffinazione colpita (stime FP) |
| 2024-02-23 | UE 13° pacchetto (2° anniversario): ban LPG, "no-Russia clause" | sanzione | marginale | BZ=F | Atteso |
| 2024-06-24 | UE 14° pacchetto: misure energia, anti-circumvention | sanzione | marginale | BZ=F | Atteso |
| 2024-12-16 | UE 15° pacchetto: focus shadow fleet (52 navi) | sanzione | marginale | BZ=F | Atteso |
| 2025-01-01 | Fine transito gas russo via Ucraina (scadenza contratto Gazprom-Naftogaz) | supply-shock | TTF↑ (lieve) | EURUSD=X, ^GDAXI | Atteso (contratto in scadenza); reazione modesta, stoccaggio UE elevato (~72% al 01-01, fonte FREE Network); impatto reale solo su Moldova |
| 2025-01-10 | OFAC sanziona Gazprom Neft, Surgutneftegaz, 183 navi | sanzione | Brent ↑ | BZ=F↑ | Amministrazione Biden; primo grande colpo a produttori |
| 2025-02-24 | UE 16° pacchetto (3° anniversario): ban alluminio primario, 52 navi | sanzione | marginale | BZ=F | Atteso |
| 2025-05-20 | UE 17° pacchetto (shadow fleet, +189 navi nel 18°) | sanzione | marginale | BZ=F | Atteso |
| 2025-06-13/24 | Conflitto Israele-Iran; rischio Hormuz; cessate-il-fuoco | escalation (esterna) | Brent ↑ poi ↓ | BZ=F↑, ^VIX↑, GC=F↑ | Shock esterno alla guerra RU-UA; Brent da ~$65 a low-$80 poi reversione; contamina il segnale petrolio |
| 2025-07-18 | UE 18° pacchetto: dynamic oil cap, 189 navi shadow fleet | sanzione | marginale | BZ=F | Atteso |
| 2025-10-22 | OFAC sanziona Rosneft e Lukoil (>50% output russo) | sanzione | Brent ↑ | BZ=F↑↑ | A sorpresa nella portata; annuncio dopo chiusura USA; Brent ~+5% mattina dopo (confermato Reuters/CNBC/Bloomberg) |
| 2025-10-23 | UE 19° pacchetto: ban import LNG russo, 117 navi (totale 557) | sanzione | Brent ↑ | BZ=F↑ | Coordinato con USA/UK |
| 2025-11 (fine) | Attacchi SBU a tanker shadow fleet (Virat, Kairos; Mar Nero/Mediterraneo) | escalation | marginale | BZ=F | Nuova fase di enforcement cinetico |
| 2026-02-28 | Operazione USA-Israele contro Iran ("Epic Fury"); minaccia Hormuz | escalation (esterna) | Brent ↑↑ | BZ=F↑↑, ^VIX↑, GC=F↑ | Shock esterno; Brent oltre $100 per la prima volta dal 2022 (single-session move più ampio dall'inizio guerra RU-UA) |

## 4. Statistiche indicative

Le seguenti ampiezze sono indicative, derivate dalle fonti citate, con bassa numerosità e da trattare con cautela.

- **Invasione / escalation militare a sorpresa**: equity EZ circa -5% nel giorno-evento. La letteratura riporta per il 24-02-2022 FTSE MIB -5,15%, DAX -4,96%, CAC40 -4,84%, FTSE100 -5,06% (Bouri/Yousaf e altri studi event-study; cfr. Federle et al., "Proximity to War: The Stock Market Response to the Russian Invasion of Ukraine", *Journal of Money, Credit and Banking* 2026, che identifica una "proximity penalty" per i paesi vicini alla zona di guerra). Oro +3-4% nella prima settimana, poi reversione. N piccolo (essenzialmente 1 episodio "puro").
- **Sanzioni energetiche a sorpresa (Rosneft/Lukoil, 22-10-2025)**: Brent +~5% nelle 24h (Reuters: +4,7% a $65,50; Bloomberg: WTI +5,6%, maggior guadagno giornaliero dal conflitto Israele-Iran di giugno). N=1-2 (con OFAC gennaio 2025 come secondo caso parziale).
- **Sanzioni ampiamente attese (price cap 05-12-2022, pacchetti UE ricorrenti)**: Brent ±2% o meno; spesso non statisticamente significativo. N elevato ma rapporto segnale/rumore basso.
- **Shock di re-routing/price cap (2023)**: effetto sul Brent quasi nullo; il segnale è nello sconto Urals-Brent (esterno), $20-35/barile nel 2022-inizio 2023, poi ridotto.

Caveat: queste ampiezze mescolano finestre e definizioni eterogenee; vanno ricalcolate internamente con CAR su finestre coerenti (T+1/T+3/T+5/T+10) e con un modello di rendimento atteso esplicito.

## 5. Segmentazione in regime phases

**Fase 1 — Shock acuto gas (2022-02-24 → 2022-12-31)**. Firma: gas (TTF) ↑↑, Brent ↑, oro ↑ (poi reversione per Fed), EUR ↓, spread BTP-Bund ↑. È il regime in cui il canale gas e il risk-off dominano. La contaminazione principale è il ciclo inflazione/stretta monetaria EZ, che agisce sull'oro e sull'euro in direzione opposta al puro safe-haven. Mischiare questa fase con le successive sovrastima il legame guerra-Brent (qui guidato dal gas, non dal petrolio russo).

**Fase 2 — Assestamento price-cap + re-routing (2023-01-01 → 2023-12-31)**. Firma: Brent stabile/↓, sconto Urals-Brent (esterno) ampio poi calante, gas in normalizzazione (TTF da €300 a ~€35 nell'arco dell'anno), oro guidato più da Fed/banche centrali che da guerra. Gli eventi-sanzione hanno effetti marginali sul Brent perché l'offerta russa resta sul mercato. L'event study sul Brent qui è poco informativo; il segnale vero è nello sconto Urals (non in DB).

**Fase 3 — Attrito raffinerie / logoramento (2024-01-01 → 2024-12-31)**. Firma: Brent moderatamente ↑ (sopra $80), diesel/prodotti (esterno) ↑, crude export russo stabile ma product export ↓. Il canale è la capacità di raffinazione, non il greggio. Gli asset DB reagiscono poco; il segnale vero è nei crack spread dei prodotti (esterni).

**Fase 4 — Sovrapposizione corrente Hormuz/OPEC+ (2025-01-01 → presente)**. Firma: contaminazione massima. Sanzioni USA dure (Rosneft/Lukoil, gennaio e ottobre 2025) + shock Hormuz (giugno 2025, febbraio 2026) + dinamiche OPEC+ + negoziati di pace ripetutamente falliti (Anchorage agosto 2025, Ginevra novembre 2025, Miami/Ginevra febbraio 2026). Qui il Brent reagisce sia alle sanzioni RU-UA sia a shock mediorientali indipendenti: separare i due richiede controllo esplicito per gli eventi Hormuz. Mischiare questa fase con le Fasi 2-3 confonde shock di sanzione con shock di chokepoint.

Perché mischiarli distrugge il segnale: il segno e l'ampiezza della reazione del Brent a una "notizia-Russia" cambiano radicalmente per regime (≈0 nel 2023, +5% nel 2025), e i canali gas/oro/EUR hanno pesi diversi. Un event study pooled su tutto il 2022-2026 produrrebbe coefficienti medi privi di significato strutturale.

## 6. Caveat metodologici

Primo, **bassa numerosità**: alcuni regimi (in particolare gli shock militari "puri" a sorpresa) hanno N=1-2, rendendo l'inferenza fragile e dominata da singoli episodi. Le statistiche del §4 vanno lette come illustrative, non come stime robuste.

Secondo, **contaminazione da fattori concomitanti**: il ciclo inflazione/stretta BCE nel 2022 agisce su oro, EUR e spread in parallelo alla guerra; lo shock Hormuz 2025-2026 agisce sul Brent indipendentemente dalle sanzioni RU-UA; le decisioni OPEC+ muovono il Brent in modo ortogonale. Senza controlli espliciti, l'event study attribuisce alla guerra effetti di altra origine.

Terzo, **variabili-canale non in DB**: TTF, Urals e lo sconto Urals-Brent, diesel/crack spread, spare capacity OPEC, volumi shadow-fleet e aderenza al price cap sono i veri "termometri" di molti episodi ma non sono tra i 26 asset; vanno trattati come covariate esterne e ricostruiti da fonti (IEA Oil Market Report, KSE Institute Russian Oil Tracker, Argus/Platts, GIE/AGSI per gli stoccaggi).

Quarto, **anticipazione e no look-ahead**: molti eventi-sanzione erano ampiamente attesi (price cap, pacchetti UE ricorrenti, fine transito gas del 01-01-2025); l'effetto è prezzato prima della data-ancora, e usare la data ufficiale come shock genera attenuazione. Per ciascun episodio va codificato il grado di sorpresa (sorpresa alta: invasione, Nord Stream, Rosneft/Lukoil; sorpresa bassa: pacchetti UE ricorrenti, fine transito gas).

Quinto, **enforcement e shadow fleet**: l'efficacia delle sanzioni (e quindi il loro impatto di mercato) dipende dall'enforcement, debole e variabile. La flotta ombra ha permesso alla Russia di aggirare il cap — secondo il KSE Institute "the shadow fleet has allowed Russia to successfully circumvent the price cap system, generating about $9.4 billion in additional revenue in 2024", con prezzo medio dell'export russo intorno ai $65/barile — attenuando l'effetto-prezzo delle designazioni. Al dicembre 2025, gli analisti KSE stimavano 621 tanker designati cumulativamente da USA/UK/UE/Canada/Australia/Nuova Zelanda, ma con un numero crescente di navi "violatrici" ancora operative (da 44 a gennaio 2025 a 143 a novembre 2025), segno che il canale di trasmissione delle sanzioni resta poroso e che il loro impatto di mercato è strutturalmente smorzato.

---
```yaml
title: "Russia-Ucraina: attrito energetico e regime sanzioni — regime ed episodi storici (2022–2026)"
date_compiled: 2026-06-18
primary_theme: geopolitical
sub_themes: [commodity_energy, oil_supply_shock, gas_supply_shock, sanctions_regime, price_cap, energy_attrition, risk_off, safe_haven_flows, eurozone_fragmentation]
relevant_assets: [BZ=F, GC=F, ^STOXX50E, ^GDAXI, FTSEMIB.MI, EURUSD=X, ^TNX, DX-Y.NYB, ^VIX, BTP_BUND_SPREAD, EEM, HG=F]
external_assets_mentioned:
  - "Gas europeo TTF — non in DB"
  - "Urals e sconto Urals-Brent — non in DB"
  - "diesel/gasolio e crack spread prodotti — non in DB"
  - "indici difesa europea — non in DB"
  - "volumi shadow fleet / aderenza price cap — non in DB"
time_window:
  start: 2022-02-24
  end: present
regime_phases:
  - acute_gas_shock_2022: 2022-02-24 to 2022-12-31
  - price_cap_rerouting_2023: 2023-01-01 to 2023-12-31
  - refinery_attrition_2024: 2024-01-01 to 2024-12-31
  - current_overlap_hormuz_opec_2025_2026: 2025-01-01 to present
keywords: [russia, ukraine, ucraina, energy attrition, sanctions, price cap, g7, oil cap, urals, gazprom, nord stream, ttf, gas europeo, repowereu, shadow fleet, refinery strikes, brent, diesel, risk-off, safe haven, eurozone fragmentation, defense, re-routing, india china oil]
```