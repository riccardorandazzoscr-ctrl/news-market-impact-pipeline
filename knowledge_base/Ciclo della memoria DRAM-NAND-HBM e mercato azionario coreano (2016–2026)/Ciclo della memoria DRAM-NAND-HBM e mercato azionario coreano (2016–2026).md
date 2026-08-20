# Ciclo della memoria (DRAM/NAND/HBM) e mercato azionario coreano — regime ed episodi storici (2016–2026)

## 1. Sintesi esecutiva

Questo studio nasce da una lacuna dichiarata nell'analisi giornaliera del **15 agosto 2026**: con Corea (EWY) e Taiwan (EWT) entrati nell'universo il 10 agosto 2026 e con il tema HBM ormai centrale, il `match` di Knowledge Base restituiva come primo risultato una ricerca sulla **difesa europea**, per sola corrispondenza di ticker. Nessuno studio copriva il ciclo della memoria.

La tesi centrale è che il mercato azionario coreano **non è un mercato-paese**: è un'espressione a leva del ciclo dei prezzi della memoria, mediata da due sole società. Samsung Electronics e SK Hynix pesano insieme circa il **40% del KOSPI** e ne guidano quasi il **30% dei movimenti** (CNBC, agosto 2026). Ne discendono tre conseguenze operative:

1. **Una notizia sulla memoria è una notizia macro coreana**, e viceversa: separare i due canali nell'event study è impossibile con EWY come unico proxy. Qualunque lettura che attribuisca un movimento di EWY alla politica interna coreana, alla difesa o al won senza controllare per il prezzo del DRAM è quasi certamente mal attribuita.
2. **Il ciclo della memoria ha cambiato natura, non solo fase.** Storicamente era un ciclo commodity: sovracapacità → crollo dei prezzi → tagli di produzione → risalita, con ampiezza brutale e periodicità di 2-3 anni (il picco DRAM di inizio 2018 a oltre $6/GB scese a meno di $3; l'esercizio fiscale 2019 di Micron chiuse con ricavi −42% e utile netto non-GAAP −85% anno su anno). Dal 2023 la domanda di **HBM** per acceleratori AI ha introdotto una componente *design-win*: la capacità viene allocata su contratti pluriennali, e nel 2025-2026 DRAM, NAND e HBM dei tre produttori risultano **esauriti in prevendita** per l'intero 2026. Il ciclo non è sparito — è diventato un ciclo di *qualifica presso il cliente* invece che di prezzo spot.
3. **Il rischio dominante oggi non è la domanda: è la struttura del duopolio.** Le due sole notizie che hanno prodotto crolli a doppia cifra nel 2026 riguardano entrambe la **contendibilità** del margine — la produzione cinese di macchine litografiche DUV (2026-07-28) e la speculazione su un rientro di Intel nella memoria ad alta banda (2026-08-14). Non la domanda finale, che nelle stesse settimane è rimasta in eccesso.

Dove l'event study è affidabile: shock di *offerta e di concorrenza* datati e isolabili nel regime 2023–2026, misurati su EWY/EWT/SOXX. Dove **non** è affidabile: (a) attribuire a un episodio "memoria" un movimento di EWY quando nella stessa seduta c'era uno shock AI generale (praticamente sempre dal 2024); (b) leggere direzionalmente i rendimenti a T+5/T+10 di un campione interamente contenuto in un mercato toro strutturale (v. §6); (c) trattare EWY e KOSPI come lo stesso oggetto — non lo sono, per il motivo di fuso orario spiegato in §6.

## 2. Tassonomia dei canali di trasmissione

**Prezzo della memoria → utili dei due costituenti → indice (proxy: EWY).** Catena causale: variazione del prezzo contrattuale DRAM/NAND → variazione quasi lineare del margine operativo di Samsung e SK Hynix (costo fisso alto, prezzo variabile) → revisione degli utili attesi → rivalutazione dei due titoli → movimento dell'indice per peso. È il canale **primario** e il più affidabile: l'elasticità è alta e il ritardo è breve. Ordine di grandezza del regime attuale: prezzi DRAM +~50% nei primi tre trimestri del 2025, +30% atteso nel Q4 2025, +20% a inizio 2026 (Counterpoint), e un +90% nel Q1 2026 sul trimestre precedente, con circa il 93% della capacità combinata dei tre produttori dirottata su HBM per data center.

**Qualifica HBM presso il cliente (proxy: EWY vs EWT come spread).** Catena causale: superamento (o fallimento) della qualifica di un fornitore presso Nvidia → riallocazione di quote su un mercato a capacità fissa → trasferimento di margine *fra* i produttori, a domanda finale invariata. È un canale **redistributivo**, non direzionale sul settore: è l'unico che dovrebbe muovere EWY ed EWT in **direzioni opposte**, ed è per questo il più informativo quando accade. La sequenza storica: SK Hynix qualifica per prima l'HBM3E 8-Hi (Q4 2023, forniture a Nvidia dal Q1 2024 per H200); Micron seconda (Q2 2024); Samsung arriva dopo una serie documentata di fallimenti, ottenendo la qualifica 12-Hi solo nel settembre 2025 — circa 18 mesi dopo aver completato lo sviluppo del chip. La quota Samsung passa dal 17% al 35% nel Q3 2025 proprio su quella qualifica.

**Contendibilità del duopolio / concorrenza cinese (proxy: EWY, EWT, SOXX, ^NDX).** Catena causale: evidenza che un terzo produttore possa entrare — via strumenti di produzione domestici cinesi (SMIC, Hua Hong, CXMT come destinatari attesi delle prime consegne DUV) o via rientro di un incumbent occidentale — → riduzione del margine di equilibrio atteso a *volume invariato* → derating dei multipli. È il canale che ha prodotto gli shock più violenti del 2026, ed è concettualmente diverso da uno shock di domanda: colpisce il **prezzo**, non la **quantità**, quindi non si vede nei dati di spedizione.

**Controlli all'export e ritorsioni (proxy: EWY, EWT, SOXX, EEM, CNY=X).** Catena causale: restrizione all'export di chip/attrezzature (o contro-restrizione cinese) → riduzione del mercato indirizzabile e frammentazione delle catene → compressione dei multipli dell'intero complesso. Archetipi già in libreria dal lato USA-Cina: Huawei in Entity List (2019-05-15), controlli Biden sui chip avanzati (2022-10-07), controlli cinesi su gallio e germanio (2023-07-03), ban cinese su Micron (2023-05-21). Questo canale **non discrimina** Corea da Taiwan.

**Leva del retail e struttura di mercato coreana (proxy: EWY).** Catena causale: accumulo di posizioni a margine e su ETF a leva su singolo titolo → un ribasso ordinario innesca liquidazioni forzate → il ribasso si autoalimenta indipendentemente dai fondamentali. Non è un canale informativo ma un **amplificatore**, e nel 2026 è stato decisivo: leva in essere a un record di 29,2 mila miliardi di won (~$19,7 mld) a inizio luglio, 2,3 mila miliardi di won di liquidazioni forzate in due mesi e mezzo, oltre 360.000 conti retail liquidati d'ufficio, *circuit breaker* attivati in sedute consecutive per la prima volta nella storia dell'indice. Implicazione operativa: nel regime attuale l'**ampiezza** della reazione coreana a una notizia sulla memoria non è informativa sull'importanza della notizia.

**Politica monetaria e valuta coreana (proxy: EWY; il won NON è in DB).** Catena causale: rialzo dei tassi BoK → costo del capitale e freno alla leva retail → pressione sull'indice, in parte compensata da un won più forte per l'investitore in dollari. Canale **secondario e mal misurabile**: `KRW=X` non è nell'universo, quindi su EWY (denominato in dollari) l'effetto valuta e l'effetto azionario restano confusi. Da dichiarare come limite ogni volta che si legge un episodio di politica monetaria coreana.

## 3. Catalogo episodi-ancora datati

La colonna "data" è la data **della notizia** nel fuso in cui il pipeline la misura, cioè quella della seduta USA in cui EWY/EWT reagiscono (v. §6 sul disallineamento con il KOSPI). Dove la notizia è uscita a mercati USA chiusi, la nota lo dichiara.

| Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead |
|---|---|---|---|---|---|
| inizio 2018 (nessuna data ISO, di proposito) | Picco del ciclo DRAM precedente: prezzo oltre $6/GB | ciclo della memoria / picco prezzi | negativo lento | EWY, SOXX | Massimo di una serie di prezzo, non un annuncio: una data puntuale sarebbe arbitraria. **Non usabile come `--events`**, ed è scritta in forma non-ISO perché la libreria non la raccolga |
| 2019-06-25 | Micron: risultati FY19 con ricavi −42% e utile non-GAAP −85% a/a | shock di utili (memoria) | negativo | EWY, SOXX | Fine del *down-cycle* commodity pre-AI; il minimo dei prezzi arriva più tardi |
| 2023-04-06 | Samsung annuncia il taglio della produzione di memoria; utile operativo Q1 atteso −96% a/a | ciclo della memoria / taglio di produzione | positivo (segnale di minimo) | EWY, EWT, SOXX | Annuncio 7-apr KST; il 7-apr-2023 le borse USA erano chiuse (Good Friday) → la seduta di riferimento è il **6-apr**. Stime di taglio 20-25% |
| 2023-05-22 | La Cina vieta i prodotti Micron nelle infrastrutture critiche | controlli all'export / ritorsione | negativo (settore), positivo (concorrenti coreani) | EWY, EWT, SOXX, EEM | Annuncio CAC domenica 21-mag ora cinese → prima seduta USA utile il 22-mag. Doppio segno: penalizza Micron, avvantaggia i coreani |
| 2023-07-27 | Samsung estende il taglio di produzione e sposta il mix sul segmento AI di fascia alta | ciclo della memoria / taglio di produzione | positivo | EWY, SOXX | Prima chiara riallocazione dichiarata verso HBM |
| 2023-11-06 | Entra in vigore il divieto di vendite allo scoperto su KOSPI/KOSDAQ/KONEX | struttura di mercato coreana | ambiguo | EWY | Annuncio 5-nov (domenica). Shock di *struttura*, non di fondamentali: rialzo iniziale, ma peggiora la formazione dei prezzi e pesa sull'accessibilità per gli esteri |
| 2023-11-09 | Samsung: taglio DRAM esteso a fine anno, recupero NAND lento | ciclo della memoria / taglio di produzione | positivo | EWY, SOXX | Conferma di traiettoria, non sorpresa |
| 2024-08-05 | *Yen carry unwind*: vendite forzate su tutto il complesso AI-hardware asiatico | evento di liquidità / deleveraging | negativo acuto | EWY, EWT, SOXX, ^VIX | Episodio **non** specifico della memoria: usarlo solo come controllo di liquidità, non come analogo di ciclo |
| 2024-12-04 | Ricaduta di mercato della legge marziale dichiarata e revocata a Seul | rischio politico coreano | negativo (Corea), neutro (Taiwan) | EWY | Dichiarazione la sera del 3-dic KST, revocata dall'Assemblea Nazionale dopo tre ore. **L'episodio più pulito per isolare il rischio-paese dal fattore settoriale**: EWT come controllo |
| 2025-01-27 | Shock DeepSeek: riprezzamento dell'efficienza dei modelli di frontiera | shock di capacità dei modelli | negativo (AI-hardware) | EWY, EWT, SOXX, ^NDX | Colpisce la *domanda attesa* di acceleratori, quindi la memoria per derivata. Già in libreria |
| 2025-03-31 | Fine del divieto di vendite allo scoperto in Corea | struttura di mercato coreana | ambiguo | EWY | Ripristino della piena operatività short; rilevante per la riammissione ai panieri esteri |
| 2025-09-19 | Samsung supera la qualifica Nvidia per l'HBM3E a 12 strati | qualifica HBM / memoria | positivo (Samsung), negativo relativo (SK Hynix, Micron) | EWY, EWT, SOXX | ~18 mesi dopo il completamento dello sviluppo e dopo ripetuti fallimenti. Canale **redistributivo**: quota Samsung dal 17% al 35% nel Q3 2025 |
| 2026-06-19 | KOSPI al massimo storico di 46 anni: 9.385,59 (+116% dal minimo) | valutazioni / picco di ciclo | negativo lento | EWY | **Non misurabile su EWY**: il 19-giu-2026 le borse USA erano chiuse (Juneteenth). Il massimo di EWY è del 18-giu (219,20) e del 22-giu (219,02) |
| 2026-07-02 | Crollo dell'ETF tematico DRAM (Micron/SK Hynix/SanDisk) | valutazioni / de-risking | negativo | SOXX, EWY | Primo segnale di rottura del tema *prima* del crollo di indice |
| 2026-07-16 | Bank of Korea alza al 2,75%, primo rialzo dal gennaio 2023; KOSPI −6,37% ed entra in mercato orso (−25% dal picco) | politica monetaria coreana | negativo | EWY | Duplice causa nella stessa seduta (rialzo BoK **e** ribasso dei chip USA la notte prima): attribuzione ambigua. Inflazione a 3,2% in giugno, spinta dallo shock energetico iraniano |
| 2026-07-28 | Notizie sulla produzione di massa cinese di macchine DUV a immersione | contendibilità del duopolio / concorrenza | negativo forte | EWY, EWT, SOXX, ^NDX, EEM | Prime consegne attese a SMIC, Hua Hong, CXMT; ~5 unità nel 2026, 20 nel 2027. KOSPI −11% con *circuit breaker*, TAIEX −2.030 punti, ASML −7%. **Alcune fonti datano la notizia al 27-lug**: EWY reagisce il 28 (−6,05%) |
| 2026-07-29 | SK Hynix Q2 2026: utile operativo record (+557% a/a) ma ricavi sotto le attese | shock di utili (memoria) | negativo | EWY, EWT, SOXX | Ricavi 79,32 vs 84 mila mld di won attesi; spedizioni HBM4 sotto le attese con slittamento dei ricavi. EWY −4,78% e **minimo del ciclo** (144,21) |
| 2026-07-30 | Rimbalzo record: EWY +11,79% in una seduta | rimbalzo tecnico / liquidità | positivo | EWY, EWT | Corrisponde al +17,91% del KOSPI, il maggior rialzo giornaliero della sua storia, che le fonti datano **31-lug KST** (una fonte lo colloca alla prima seduta di agosto). Sull'ETF USA il movimento è il **30-lug**: v. §6 |
| 2026-08-13 | Il KOSPI rientra in mercato toro: +22% in dieci sedute dal minimo | rimbalzo tecnico / valutazioni | positivo | EWY, EWT | Round-trip completo in circa 60 giorni. Recupero guidato dagli stessi due titoli che avevano guidato il crollo |
| 2026-08-14 | Citi: il dibattito sulla bolla si è spostato su KOSPI e indice semiconduttori di Filadelfia | valutazioni / de-risking | negativo lento | EWY, EWT, SOXX, EEM | SOX +88% e KOSPI +84% nel trimestre, entrambi record. Citi osserva che nel crollo di luglio valutazioni e utili non erano il fattore: lo furono tecnici e flussi |
| 2026-08-14 | Intel raccoglie $20 mld di capitale, primo aumento dall'IPO del 1971; speculazione su un rientro nella memoria | contendibilità del duopolio / concorrenza | negativo (margini memoria) | EWY, EWT, SOXX | Minaccia al margine del duopolio HBM, non alla domanda. Tesi **non confermata** alla data: trattarlo come episodio di riprezzamento del rischio, non di fatto |

**Episodi deliberatamente esclusi.** Le date di svolta del ciclo commodity 2018-2019 e 2021-2022 non compaiono come `--events` puntuali perché sono massimi e minimi di *serie di prezzo*, non annunci datati: usarle produrrebbe un event study su una data arbitraria. Restano in §5 come confini di regime.

## 4. Statistiche indicative

Pool completo dei dieci episodi datati e misurabili del canale memoria (2023-04-06, 2023-05-22, 2023-07-27, 2023-11-09, 2024-08-05, 2025-01-27, 2025-09-19, 2026-07-16, 2026-07-28, 2026-07-29), rendimenti cumulati:

| Asset | T+1 | T+3 | T+5 | T+10 | N |
|---|---|---|---|---|---|
| EWY (mediana) | +0,13% | +2,82% | +4,22% | +4,10% | 10 |
| EWY (p25) | −0,96% | +1,46% | −0,85% | +1,48% | 10 |
| EWT (mediana) | +1,04% | +1,53% | +2,08% | +4,07% | 10 |
| EWT (p25) | −0,78% | +0,33% | −0,11% | −1,07% | 10 |

**Questo pool è contaminato per costruzione** e il numero da non citare è la mediana a T+10: mescola tagli di produzione (segnali di minimo, quindi rialzisti) con shock di concorrenza (ribassisti), e include 2026-07-29, che è il **minimo esatto** del ciclo — il suo +21,95% a T+10 su EWY è aritmetica del punto di partenza, non un risultato.

Sotto-pool dei soli shock **negativi** di concorrenza/domanda (2023-05-22, 2025-01-27, 2026-07-16, 2026-07-28), ⚠ **INDICATIVE ONLY, N=4**:

| Asset | T+1 | T+3 | T+5 | T+10 |
|---|---|---|---|---|
| EWY (mediana) | −0,85% | +2,53% | +3,48% | +2,59% |
| EWT (mediana) | −1,95% | +1,53% | +2,08% | +4,07% |
| SOXX (mediana) | −1,44% | +3,18% | +7,02% | +5,93% |

La firma è netta e sempre la stessa: **impatto il giorno stesso, recupero completo entro T+3, sovraperformance entro T+5**. È la stessa "firma di regime" già osservata sul tema AI nelle schede del 15 agosto 2026 e va letta come tale — non come previsione, ma come descrizione di un campione interamente contenuto in un mercato toro (v. §6).

**Il numero più utile dello studio è la divergenza EWY−EWT.** Sui dieci episodi del pool completo, le mediane a T+10 sono +4,10% (EWY) e +4,07% (EWT): **indistinguibili**. Il mercato non ha mai discriminato fra memoria (Corea) e logica (Taiwan), nemmeno sugli episodi di qualifica HBM che in teoria sono redistributivi. Ne segue un test operativo: se una tesi di erosione del margine della memoria — Intel, CXMT — venisse presa sul serio, EWY dovrebbe cominciare a sottoperformare EWT in modo **persistente**, comportamento senza precedenti in questo campione e proprio per questo informativo.

## 5. Segmentazione in regime phases

- `commodity_cycle_pre_ai` (2016-01-01 → 2022-12-31): ciclo classico offerta/domanda, ampiezza brutale, nessuna componente AI. La Corea si muove come esportatore ciclico. Analoghi di questo regime **non** sono validi per il presente.
- `hbm_transition` (2023-01-01 → 2024-12-31): tagli di produzione sul DRAM commodity e simultanea corsa alla qualifica HBM. Regime di transizione: convivono segnali da ciclo commodity (tagli) e da design-win (qualifiche).
- `hbm_scarcity_bull` (2025-01-01 → 2026-06-30): capacità venduta in prevendita, prezzi in rialzo a doppia cifra per trimestre, KOSPI +116% fino al massimo storico. La memoria smette di comportarsi da commodity.
- `duopoly_contestability` (2026-07-01 → presente): la domanda resta in eccesso, ma il mercato riprezza la **difendibilità** del margine — DUV cinese, rientro Intel. È il regime corrente ed è quello in cui vanno cercati gli analoghi.

## 6. Caveat metodologici

**EWY non è il KOSPI, e lo scarto è di una seduta.** EWY è quotato negli Stati Uniti e il mercato coreano chiude prima dell'apertura americana: una notizia coreana della mattina KST viene prezzata da EWY nella seduta USA che comincia lo stesso giorno civile, mentre una reazione del KOSPI del giorno successivo KST è spesso già dentro EWY il giorno prima. Due verifiche fatte sui dati in DB: il massimo storico del KOSPI del **2026-06-19** non ha alcuna osservazione EWY (Juneteenth, borse USA chiuse) e il massimo di EWY è del 18-giugno; il rialzo record del KOSPI (+17,91%) che le fonti datano **31-luglio** compare su EWY come **+11,79% il 30-luglio**, seguito da −2,55% il 31. Conseguenza operativa: **non copiare mai una data di reazione del KOSPI dentro `--events`** — va usata la data della seduta USA, e in caso di dubbio vanno controllate entrambe.

**Attribuzione: dal 2024 quasi ogni episodio è multi-causa.** Il 2026-07-16 mette nella stessa seduta il primo rialzo BoK in tre anni e la scia del ribasso dei chip USA della notte prima. Il 2024-08-05 è liquidità globale, non memoria. Regola pratica: usare EWT come controllo per lo shock AI-hardware generale e tenere solo la componente EWY−EWT come contenuto specificamente coreano.

**Il campione è tutto dentro un mercato toro.** Ogni episodio misurabile con EWY/EWT nel regime AI cade fra il 2023 e il 2026, un periodo in cui il livello di partenza è quasi sempre più basso di quello di due settimane dopo. Le mediane positive a T+5 e T+10 sono in larga parte un effetto meccanico del *drift*: vanno dichiarate come firma di regime, mai spacciate per capacità predittiva.

**La leva retail rompe il legame fra importanza della notizia e ampiezza della reazione.** Nel luglio 2026 il crollo è stato amplificato da liquidazioni forzate su scala storica. Un −11% del KOSPI in quel contesto non misura la gravità della notizia sulla DUV cinese: misura quanta leva c'era. Non usare l'ampiezza come proxy della rilevanza informativa nel regime corrente.

**Il won non è in DB.** `KRW=X` non fa parte dell'universo, quindi su ogni episodio di politica monetaria coreana l'effetto valuta e l'effetto azionario restano confusi dentro EWY, che è denominato in dollari. È la singola aggiunta che migliorerebbe di più questo studio.

**N piccolo per costruzione.** Il canale della *qualifica HBM* ha oggi 2-3 episodi datati: qualunque statistica su quel sotto-tema è indicativa e va marcata come tale. Il canale della *contendibilità del duopolio* ne ha due, entrambi nel 2026. Sono lacune reali, non difetti di ricerca: gli episodi non esistono ancora.

**Fonti e incertezze dichiarate.** Le cifre puntuali (prezzi DRAM, quote di mercato, valori delle liquidazioni forzate, risultati SK Hynix) provengono dalla stampa finanziaria dell'agosto 2026 e non sono state riconciliate con i bilanci societari. Due date restano incerte e sono segnalate come tali in §3: quella della notizia sulla DUV cinese (27 o 28 luglio 2026 a seconda della fonte) e quella del rialzo record del KOSPI (31 luglio 2026, con una fonte che lo colloca alla prima seduta di agosto). I movimenti di EWY citati sono invece verificati direttamente sulla tabella `prices` del database.

```yaml
---
title: "Ciclo della memoria (DRAM/NAND/HBM) e mercato azionario coreano — regime ed episodi storici (2016–2026)"
date_compiled: 2026-08-15
primary_theme: structural_themes
sub_themes: [memory_cycle, hbm, dram, nand, korea, kospi, semiconductor_cycle, foundry_logic, export_controls, valuation_derisking, duopoly_contestability, retail_leverage, market_structure_korea]
relevant_assets: [EWY, EWT, SOXX, ^NDX, EEM, ^VIX, CNY=X]
external_assets_mentioned:
  - "KRW=X (won coreano) — NON in DB: è la lacuna più rilevante per questo studio"
  - "Samsung Electronics 005930.KS, SK Hynix 000660.KS — single-name, non in DB"
  - "Micron MU, SanDisk, Intel INTC, ASML, TSMC, SMIC, Hua Hong, CXMT — non in DB"
  - "KOSPI (indice locale) — non in DB; EWY ne è il proxy con scarto di una seduta"
  - "prezzi contrattuali DRAM/NAND (TrendForce, Counterpoint) — serie non in DB"
time_window:
  start: 2016-01-01
  end: present
regime_phases:
  - commodity_cycle_pre_ai: 2016-01-01 to 2022-12-31
  - hbm_transition: 2023-01-01 to 2024-12-31
  - hbm_scarcity_bull: 2025-01-01 to 2026-06-30
  - duopoly_contestability: 2026-07-01 to present
keywords: [memoria, memory, dram, nand, hbm, hbm3e, hbm4, ciclo della memoria, memory cycle, samsung, sk hynix, micron, corea, korea, kospi, ewy, ewt, taiwan, duopolio, duopoly, cxmt, duv, litografia, lithography, qualifica, qualification, taglio di produzione, production cut, vendite allo scoperto, short selling ban, legge marziale, martial law, bank of korea, leva retail, liquidazioni forzate, circuit breaker, semiconductor cycle, export controls]
```
