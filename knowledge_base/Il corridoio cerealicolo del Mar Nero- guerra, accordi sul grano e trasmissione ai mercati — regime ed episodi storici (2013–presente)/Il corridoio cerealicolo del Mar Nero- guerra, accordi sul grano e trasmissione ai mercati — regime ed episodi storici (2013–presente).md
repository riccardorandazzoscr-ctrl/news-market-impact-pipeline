# Il corridoio cerealicolo del Mar Nero: guerra, accordi sul grano e trasmissione ai mercati — regime ed episodi storici (2013–presente)

## §1 — Sintesi esecutiva

1. **La tesi centrale.** Sulla stessa notizia geopolitica relativa al Mar Nero, grano (`ZW=F`) e mais (`ZC=F`) di Chicago tendono a muoversi in direzione **opposta** a gas europeo (`TTF=F`) e Brent (`BZ=F`) quando l'evento è di natura *diplomatica* (accordo, rinnovo, cessate-il-fuoco, o al contrario rottura): i cereali reagiscono a una variazione dell'**offerta fisica** ucraina realmente disponibile all'export, mentre l'energia reagisce a una variazione del **premio di rischio di escalation**. In una de-escalation entrambi scendono, ma per meccanismi opposti; in un'escalation entrambi salgono, di nuovo per meccanismi opposti. Per questo i due canali non vanno mai mediati in un pool unico di event study.

2. **L'eccezione che conferma la regola.** L'unico episodio in cui cereali ed energia sono saliti *insieme e per lo stesso segno* è l'invasione del 24 febbraio 2022, perché quel singolo shock ha simultaneamente (a) alzato il premio di rischio energetico e (b) bloccato fisicamente i porti di Odessa. È il caso in cui i due canali collassano su un unico verso — ma è irripetibile come "template", perché un blocco navale totale è un evento di coda, non il caso base.

3. **Dove l'event study è affidabile.** È robusto sugli eventi ucraini *diretti* e *ben datati*: firma della BSGI, primo carico, rinnovi con scadenza calendarizzata, sospensione del 17 luglio 2023. Qui il nesso evento→prezzo del grano è forte, rapido (T+1) e con segno prevedibile.

4. **Dove NON è affidabile.** È debole (i) sul canale **russo indiretto** (sanzioni su assicurazione/pagamenti/fertilizzanti), che si trasmette lento e sporco; (ii) sugli **attacchi ai porti** in zona di guerra, dove data e danno reale sono spesso oscurati o gonfiati dalle parti, con reazioni di prezzo di 1,6–8% che rientrano spesso entro due settimane; (iii) dal 2023 in poi, per l'assuefazione del mercato — con il corridoio unilaterale ucraino che macina volumi quasi pre-bellici, il mercato ha smesso di reagire agli attacchi "di routine". Come sintetizzava una fonte commerciale ucraina citata da S&P Global Commodity Insights (19 marzo 2025): *"The market has long since stopped reacting to what has become the normal level of attacks in and around the Black Sea."*

5. **Forza storica del disallineamento.** Il disallineamento di segno cereali-energia è storicamente marcato sugli eventi diplomatici, ma il campione di eventi puliti è piccolo (N<10 per ogni sotto-canale): le statistiche del §4 vanno lette come indicative, non come stime robuste.

## §2 — Tassonomia dei canali di trasmissione

**Canale 1 — Offerta fisica ucraina (blocco/riapertura porti).** È il canale dominante e il più pulito.
`blocco/riapertura dei porti di Odessa (o firma/rottura di un accordo che li governa) → variazione della quantità di grano/mais ucraino fisicamente esportabile → revisione delle stime di bilancio mondiale (stock-to-use) → ZW=F / ZC=F`.
Una **riapertura** (firma BSGI, primo carico, rinnovo, cessate-il-fuoco marittimo) spinge `ZW=F`/`ZC=F` **giù**; un **blocco** (invasione, sospensione, minaccia russa alle navi) li spinge **su**. Sullo stesso evento, `TTF=F`/`BZ=F` tipicamente **non reagiscono** (evento non energetico) oppure reagiscono per il Canale 2, spesso di **segno opposto**. Il peso dell'Ucraina nel commercio mondiale spiega la sensibilità: secondo il Consiglio dell'UE, l'Ucraina è il primo esportatore mondiale di olio di girasole (50% dell'export mondiale), il terzo di orzo (18%), il quarto di mais (16%) e il quinto di grano (12%).

**Canale 2 — Premio di rischio energetico.** È il canale che muove l'energia sulla *stessa* notizia, ma per un motivo diverso.
`notizia di escalation/de-escalation Russia-Ucraina → revisione della probabilità di interruzione delle forniture russe di gas/petrolio all'Europa → variazione del premio di rischio → TTF=F / BZ=F`.
Un'**escalation** alza `TTF=F`/`BZ=F`; una **de-escalation** li abbassa. Il punto critico: su una notizia di *accordo sul grano*, l'energia in genere resta ferma (non è un evento di offerta energetica); su una notizia di *cessate-il-fuoco generale*, l'energia scende per sgonfiamento del premio **mentre** il grano scende per riapertura dell'offerta — stesso segno, meccanismi opposti. Su un'*escalation bellica*, l'energia sale per premio di rischio **mentre** il grano sale per blocco fisico — di nuovo stesso segno, meccanismi opposti. Il disallineamento di *segno* emerge nitido solo negli eventi puramente diplomatici sul grano (accordo/rinnovo), dove il grano si muove e l'energia no.

**Canale 3 — Russo indiretto (sanzioni su assicurazione/pagamenti/fertilizzanti).** Da tenere separato dal Canale 1 perché più debole e lento.
`sanzioni o frizioni su assicurazione marittima / pagamenti bancari (SWIFT, Rosselkhozbank) / export di potassio e fosfati russo-bielorusso → aumento costi/incertezza su export russo di grano e su fertilizzanti → costi di produzione agricola globali e disponibilità → ZW=F / ZC=F, con ritardo`.
La Russia è il primo esportatore mondiale di grano e **non è sotto embargo cerealicolo diretto**: secondo l'International Grains Council era proiettata a esportare un record di circa 53 milioni di tonnellate con una quota globale del 26%, la più alta della sua storia. L'effetto sui prezzi globali passa quindi dai costi di transazione e dai fertilizzanti, non da un blocco dell'export russo in sé. Trasmissione lenta, difficile da datare in un event study a T+1/T+5. Proxy ausiliario suggerito: `RUB=X`. Non a caso, nel marzo 2025 la stessa parte russa ha subordinato il cessate-il-fuoco marittimo alla riconnessione di Rosselkhozbank a SWIFT — segnale che il canale è di natura bancaria/assicurativa, non di blocco fisico.

**Canale 4 — Idiosincratico del mais (rumore di fondo non-Mar Nero).** Da isolare ed escludere dal segnale Mar Nero.
`ciclo di semina/raccolto USA + domanda etanolo + raccolto sudamericano + domanda cinese → ZC=F`.
Storicamente il mais si è mosso **meno** del grano sugli shock Mar Nero: negli event study di Carter–Steinbach il grano salì circa +30–35% contro il +10–16% del mais dopo l'invasione, e il picco di marzo 2022 vide il grano toccare il record mentre il mais ebbe una salita più "controllata" (da circa 6,81 a 7,55¾ $/bu tra il giorno precedente l'invasione e il 10 maggio, secondo DTN). Il mais ha un secondo canale strutturale nordamericano (etanolo/raccolto) che introduce rumore non riconducibile al corridoio; l'elasticità di importazione di breve periodo è circa −0,4 per il grano contro circa −1,0 per il mais, il che rende il grano più reattivo agli shock di offerta.

## §3 — Catalogo di episodi-ancora datati

Note preliminari sulle date: il CBOT e i future agricoli hanno sessioni proprie e chiudono prima delle notizie serali europee; quando la notizia esce a mercato chiuso o nel weekend si usa la **prima seduta utile** e lo si annota. La colonna "Direzione attesa" è riferita a ciascun asset-canale quando i versi divergono.

Riferimenti di periodo **non-ISO** (da NON trattare come episodi): l'annessione della Crimea come fenomeno di fondo (marzo 2014); il picco pluriennale di "marzo 2022"; la fase "estate 2022"; la ripresa record dell'export via corridoio unilaterale ("aprile 2024"); l'escalation della "guerra dei porti" dell'estate 2025.

| Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead |
|---|---|---|---|---|---|
| 2014-03-03 | Ingresso truppe russe in Crimea; prima seduta CBOT dopo il weekend | escalation (controllo minore) | ZW=F: pos / ZC=F: pos (debole) | Canale 1 | Impatto storicamente contenuto: nessun blocco dei porti di Odessa. Mais a massimi di 6 mesi, grano a massimi di 3 mesi, poi rientro. |
| 2022-02-15 | Russia annuncia ritiro parziale truppe (de-escalation poi smentita) | de-escalation (head-fake) | BZ=F: neg / TTF=F: neg / ZW=F: neg (debole) | Canale 2 dominante | Dated Brent −2,06 $ a 97,655 $/b; TTF DA in rientro dal record di dicembre. Controllo di de-escalation pre-invasione. |
| 2022-02-24 | Invasione russa; blocco dei porti del Mar Nero | escalation estrema | ZW=F: pos / ZC=F: pos / TTF=F: pos / BZ=F: pos | Canali 1 e 2 insieme | **Unico caso di segno allineato.** TTF marzo +33% intraday (a circa 117 €/MWh); Brent intraday da 97,56 a 105,79 $/b, settle +2,3% a 99,08 $; gas naturale +6,5%; grano limit-up. |
| 2022-03-07 | Grano CBOT tocca il record storico | picco di regime | ZW=F: pos (esaurimento) | Canale 1 | Future maggio a 13,63½ $/bu; ridiscende sotto 11 $ entro il 10 marzo. Data del picco, non di un annuncio. |
| 2022-07-22 | Firma della Black Sea Grain Initiative (Istanbul, venerdì) | riapertura (accordo) | ZW=F: neg / ZC=F: neg / TTF=F: neutral / BZ=F: neutral | Canale 1; energia ferma | Il grano è sceso poche ore dopo la firma; l'energia non ha reagito (evento non energetico). Disallineamento di segno da manuale. |
| 2022-08-01 | Primo carico (MV Razoni, 26.527 t di mais) salpa da Odessa (lunedì) | conferma operativa | ZW=F: neg / ZC=F: neg | Canale 1 | Mais e grano in calo nel mercato dei future dopo la partenza; conferma che l'accordo è operativo, non solo annunciato. |
| 2022-10-31 | Sospensione russa dopo l'attacco a Sebastopoli; prima seduta utile (lunedì) | escalation | ZW=F: pos / ZC=F: neutral | Canale 1 | Grano +6,4% a Chicago il 31/10; le navi continuano a transitare, poi −0,9% il giorno dopo (mais pressoché invariato). |
| 2022-11-02 | Russia rientra nell'accordo | riapertura | ZW=F: neg | Canale 1 | Rientro dopo garanzie ucraine; riassorbe lo spike del 31/10. |
| 2022-11-17 | Rinnovo BSGI per 120 giorni (giovedì) | riapertura (rinnovo) | ZW=F: neg / TTF=F: neutral | Canale 1 | Attesa/conferma; allenta la pressione sui prezzi alimentari. Decorrenza 19 novembre 2022. |
| 2023-03-20 | Rinnovo BSGI annunciato sabato 18/03 → prima seduta utile lunedì | riapertura (rinnovo) | ZW=F: neg | Canale 1 | Annuncio nel weekend: reazione datata a lunedì 20/03. "Following Black Sea grain deal extension, wheat falls" (Farm Policy News). |
| 2023-05-17 | Rinnovo BSGI per 60 giorni (mercoledì) | riapertura (rinnovo) | ZW=F: neg / ZC=F: neg | Canale 1 | "Confirmation… put pressure on the CBOT grains complex, with wheat catching most of the selling" (Dow Jones). Disallineamento con energia ferma. |
| 2023-07-17 | Russia sospende la BSGI (lunedì) | rottura (blocco) | ZW=F: pos / ZC=F: pos (debole) / TTF=F: neutral | Canale 1 | Grano +circa 3% a 6,81 $/bu, mais +0,94% a 5,11 $; parte del rialzo poi rientrato in giornata. |
| 2023-07-19 | Russia dichiara le navi verso l'Ucraina possibili obiettivi militari; attacchi a Odessa | escalation (blocco de facto) | ZW=F: pos / ZC=F: pos | Canale 1 | CBOT >+8% mercoledì 19/07; grano fisico Euronext +8,2%, mais +5,4% il 20/07; +1,6% ulteriore a 7,39 $/bu il 20/07. |
| 2023-08-02 | Attacco russo al porto danubiano di Izmail (mercoledì) | attacco portuale | ZW=F: pos | Canale 1 | Prezzi alimentari globali in rialzo; 180.000 t di grano distrutte dal ritiro russo, secondo Kyiv. |
| 2023-08-16 | Nuovi attacchi ai porti del Danubio (Izmail); primo mercantile (Joseph Schulte) lascia Odessa via corridoio unilaterale | attacco + riapertura di fatto | ZW=F: pos (attacco) / ZW=F: neg (corridoio) | Canale 1 (segnali opposti in giornata) | Data con doppio segnale: danno ai silos vs partenza della prima nave. Reazione netta ambigua — da trattare con cautela. |
| 2025-03-25 | Cessate-il-fuoco sul Mar Nero mediato dagli USA (martedì) | de-escalation/riapertura | ZW=F: neg / ZC=F: neg / TTF=F: neg-muted / BZ=F: neg-muted | Canale 1 (grano) + Canale 2 (energia) | Grano maggio settle −5¢ a 5,43¼ $ (−0,9%, minimo da 5/3); mais settle −6¾¢ a 4,57¾ $ (−1,4%). Energia reazione muta (l'accordo non ripristina il transito gas russo). Suderman (StoneX): *"The ceasefire agreement is perceived as a bearish influence on wheat."* |
| 2025-12-22 | Rimbalzo del grano su nuovi attacchi ai porti (Odessa/Pivdennyi, terminal Allseeds; Taman lato russo); seduta di lunedì | attacco portuale | ZW=F: pos | Canale 1 | Grano a 5,15 $/bu rimbalzando dal minimo di quasi due mesi (5,04 $ il 17/12); guadagni limitati da ampia offerta globale attesa. |
| 2026-09-06 | Visita degli inviati USA (Witkoff, Kushner) a Kyiv dopo Mosca | annuncio di trattativa (NON accordo) | ZW=F: neutral / BZ=F: neg (debole) | Canale 2 | **Annuncio di trattativa, non accordo operativo**: nessun cessate-il-fuoco raggiunto ("the war will continue", Kyiv Independent). Da non trattare come riapertura. |

## §4 — Statistiche indicative

Ogni statistica è **INDICATIVE ONLY** perché ogni sotto-canale ha N<10 eventi puliti. I valori sono reazioni di prima seduta (T+1) desunte dalle fonti; T+3/T+5/T+10 non sono ricostruibili in modo omogeneo dalle fonti disponibili e vanno calcolati sui dati di prezzo grezzi nella pipeline.

**Cluster A — Riapertura/de-escalation dell'offerta fisica ucraina** (firma BSGI 2022-07-22; Razoni 2022-08-01; rinnovi 2022-11-17, 2023-03-20, 2023-05-17; cessate-il-fuoco 2025-03-25). **N=6. INDICATIVE ONLY.** `ZW=F` a T+1: **negativo**, ordine di grandezza tra −1% e −5%, con i casi meglio documentati (2025-03-25: −0,9%) nella fascia bassa. `ZC=F`: negativo ma spesso più contenuto o distorto da fattori non-Mar Nero (2025-03-25: −1,4%, spinto anche dall'avanzamento della semina USA e dai grandi raccolti sudamericani). `TTF=F`/`BZ=F`: **≈0** sugli accordi-grano puri; negativi ma **muti** sul cessate-il-fuoco generale del 2025 (nessuna cifra attribuibile con certezza a quella specifica notizia: l'accordo non ripristinava il transito del gas russo).

**Cluster B — Blocco/escalation dell'offerta fisica** (invasione 2022-02-24; sospensione 2022-10-31; sospensione 2023-07-17; minaccia navi/attacchi 2023-07-19; attacchi portuali 2023-08-02, 2023-08-16, 2025-12-22). **N=7. INDICATIVE ONLY.** `ZW=F` a T+1: **positivo**, con dispersione enorme (da +1,6% su un attacco portuale "di routine" fino a limit-up all'invasione e >+8% il 2023-07-19). `ZC=F`: positivo ma sistematicamente **inferiore** al grano. Reazioni spesso **riassorbite entro due settimane**: gli event study documentano che il rialzo post-17 luglio 2023 (grano +15%, mais +10% sopra il controfattuale) rientrò in meno di due settimane.

**Cluster C — Premio di rischio energetico** (de-escalation 2022-02-15; invasione 2022-02-24; cessate-il-fuoco 2025-03-25; prospettiva di pace 2025-11-24). **N=4. INDICATIVE ONLY, N<10.** `TTF=F`/`BZ=F`: segno = segno dell'escalation (fortemente positivo il 2022-02-24 con TTF +33% e Brent +9% intraday; negativo nelle de-escalation, con WTI sceso a circa 57 $/b e cali di circa 2% a fine novembre 2025 sulle notizie di piano di pace). Su questo cluster il grano è tipicamente muto sugli eventi puramente energetici, il che rafforza la separazione dei pool.

**Il fatto saliente per l'event study:** confrontando Cluster A e Cluster C sullo **stesso** evento (2025-03-25), grano ed energia scendono **entrambi** ma il grano per riapertura di offerta e l'energia per sgonfiamento del premio; sugli accordi-grano puri (2022-07-22, 2023-05-17) il grano scende **e l'energia resta ferma** — è lì che il disallineamento di segno è massimo e più sfruttabile.

## §5 — Fasi di regime

**`pre_2022_baseline`** — 2013-01-01 → 2022-02-23. Ucraina e Russia esportano insieme una quota rilevante del grano mondiale via Azov/Mar Nero — circa il 26% dell'export mondiale di grano nel 2021, secondo la FAO — ma l'annessione della Crimea del 2014 è un precedente a **basso impatto** (nessun blocco di Odessa). Gli analoghi di questa fase sono usabili solo come *controllo di bassa intensità*: mostrano quanto poco si muovano i prezzi globali quando i porti restano aperti.

**`war_blockade_2022`** — 2022-02-24 → 2022-07-21. Blocco navale totale; picco storico del grano; unico regime in cui cereali ed energia si muovono con lo **stesso** segno. La quota congiunta Russia-Ucraina nell'export mondiale di grano scese da circa 26% (2021) a circa 17% (2022) secondo la FAO. Gli analoghi qui sono usabili **solo** per eventi di blocco totale, non per la normale volatilità geopolitica: sovrastimano l'ampiezza delle reazioni nel regime corrente.

**`grain_initiative_2022_2023`** — 2022-07-22 → 2023-07-16. Corridoio governato da un accordo con scadenze calendarizzate; ogni rinnovo (novembre 2022, marzo 2023, maggio 2023) è un mini-evento di offerta. È il regime che produce gli analoghi **più puliti** per il disallineamento cereali-energia. Usabili nel regime corrente con cautela: oggi manca un accordo formale con scadenze, quindi mancano gli "appuntamenti" datati che rendevano prevedibili i mini-eventi.

**`post_suspension_unilateral_corridor_2023_2025`** — 2023-07-17 → 2025-02-28. La BSGI è morta; l'Ucraina apre un corridoio unilaterale (agosto 2023) che entro l'aprile 2024 supera i volumi mensili della BSGI (circa 5,2 Mt/mese di cereali e oleaginose dai porti del Mar Nero contro il picco BSGI di 4,2 Mt nell'ottobre 2022, secondo l'intelligence britannica). È il regime della "riapertura di fatto senza riapertura diplomatica" e dell'**assuefazione** del mercato agli attacchi. Gli analoghi di questa fase sono i **più rilevanti** per il regime corrente perché il meccanismo (corridoio militarmente difeso, non negoziato) è quello ancora in vigore.

**`negotiation_2025_2026`** — 2025-03-01 → present. Trattative ricorrenti (Riyadh marzo 2025; navette Witkoff/Kushner 2025-2026) con annunci di trattativa che vanno **distinti** dagli accordi operativi. Il mercato reagisce poco perché il corridoio unilaterale già trasporta volumi quasi pre-bellici: la notizia di riapertura ha impatto marginale ridotto. Analoghi usabili per calibrare reazioni **piccole e mute**, non grandi shock.

## §6 — Caveat metodologici

**Stagionalità del raccolto.** Nell'emisfero nord il raccolto (giugno–settembre) è il confondente strutturale principale: l'invasione del 24 febbraio 2022 cadde a ridosso della **semina**, non del raccolto, e questo va dichiarato ogni volta che si generalizza. Un blocco a raccolto in corso (come la "guerra dei porti" dell'estate 2025) ha implicazioni di offerta diverse da un blocco a semina, e questo altera l'ampiezza attesa delle reazioni.

**Liquidità.** I future agricoli (`ZW=F`, `ZC=F`) sono meno liquidi di quelli energetici (`TTF=F`, `BZ=F`): reazioni più rumorose, gap e mosse da short-covering speculativo. La Federal Reserve di Chicago ha documentato che nel 2022 il contratto CBOT reagì *più* di quello europeo per differenze di struttura di mercato e maggiore accesso degli speculatori — un artefatto di microstruttura da tenere presente quando si generalizzano le ampiezze.

**Quotazione in cent/staio.** `ZW=F` e `ZC=F` quotano in cent/staio: leggere **sempre** le variazioni percentuali, mai i livelli, coerentemente con la nota in `category_asset_map.yaml`.

**Attendibilità sugli attacchi portuali.** In zona di conflitto attivo il danno reale è spesso oscurato o gonfiato dalle parti; date e magnitudini vanno prese con doppia fonte quando possibile. Diverse date del 2023 e del 2025 sono qui datate alla seduta di reazione, non all'ora dell'attacco. La stessa data 2023-08-16 porta segnali opposti (danno ai silos vs prima nave del corridoio unilaterale), a riprova dell'ambiguità.

**Sovrapposizione con lo studio Russia-Ucraina energetico in KB.** I due studi condividono gli eventi ma **si dividono i canali**: lo studio energetico possiede `TTF=F`/`BZ=F` via premio di rischio (Canale 2); questo studio possiede `ZW=F`/`ZC=F` via offerta fisica (Canale 1). Sullo stesso evento vanno interrogati **entrambi** e poi confrontati per il segno, mai fusi in un pool unico — pena la cancellazione reciproca del segnale.

**Incertezze residue.** Le reazioni T+3/T+5/T+10 non sono ricostruite dalle fonti e vanno calcolate sui prezzi grezzi. Il chiusura di settlement CBOT del 2025-03-26 non è confermata (disponibile solo un dato intraday di sessione asiatica, comunque in calo). Nessuna fonte ha fornito una cifra di Brent/TTF attribuibile con certezza alla sola notizia del cessate-il-fuoco del 2025-03-25: la reazione energetica appare muta. Attenzione a non confondere i grandi movimenti di TTF/Brent del giugno 2025 (cessate-il-fuoco Israele-Iran, non Russia-Ucraina). Il canale russo indiretto (Canale 3) resta il più difficile da datare. Gli sviluppi del settembre 2026 sono annunci di trattativa senza accordo operativo.

```yaml
---
title: "Il corridoio cerealicolo del Mar Nero: guerra, accordi sul grano e trasmissione ai mercati — regime ed episodi storici (2013–presente)"
date_compiled: 2026-09-08
primary_theme: geopolitical
sub_themes: [black_sea, grain_corridor, export_ban, shipping_chokepoint]
relevant_assets: [ZW=F, ZC=F, TTF=F, BZ=F]
external_assets_mentioned:
  - "RUB=X — isolerebbe l'effetto sanzioni indirette sulla Russia, primo esportatore mondiale di grano e non sotto embargo cerealicolo diretto"
  - "grivnia ucraina — nessun proxy liquido quotato"
  - "MOO (VanEck Agribusiness ETF) — canale equity globale, se utile a validare il segnale sui future"
time_window:
  start: 2013-01-01
  end: present
regime_phases:
  - pre_2022_baseline: 2013-01-01 to 2022-02-23
  - war_blockade_2022: 2022-02-24 to 2022-07-21
  - grain_initiative_2022_2023: 2022-07-22 to 2023-07-16
  - post_suspension_unilateral_corridor_2023_2025: 2023-07-17 to 2025-02-28
  - negotiation_2025_2026: 2025-03-01 to present
keywords: [cereali, grano, mais, corridoio del Mar Nero, Black Sea Grain Initiative, Odessa, porti del Danubio, Izmail, Reni, blocco navale, export ban, wheat, corn, grain corridor, Ukraine grain deal, Russia grain export, fertilizer sanctions]
```