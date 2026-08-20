# Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)

*Studio deep-research segmentato per regime, base per event study (reazione T+1/T+3/T+5/T+10 a shock-notizia discreti). Ruolo: analista quantitativo macro/politico-commerciale. Fatto datato e interpretazione sono tenuti rigorosamente distinti; per ogni episodio la colonna "no-look-ahead" indica cosa era noto/atteso alla data-ancora.*

## 1. Sintesi esecutiva

La tesi centrale è che gli shock-notizia della guerra commerciale USA si trasmettono agli asset finanziari attraverso canali stabili e identificabili, ma la firma quantitativa della reazione dipende in modo decisivo dal REGIME in cui l'episodio cade: mischiare il 2018-2019 con il 2025-2026 distrugge il segnale. Nel 2018-2019 la Fed era in modalità "insurance cuts" (tre tagli: 31 luglio, 18 settembre, 30 ottobre 2019), con Powell che li definì esplicitamente "insurance against ongoing risks", fornendo un cuscino all'equity che attenuava e talvolta invertiva le reazioni ribassiste. Nel 2025-2026 la reaction function della Fed è diversa (inflazione post-pandemica ancora vicino/sopra target, Fed non automaticamente dovish), quindi lo stesso shock tariffario può avere un beta più violento e meno "riassorbito". I canali che contano di più: (1) equity USA/risk-off (^GSPC, ^NDX, ^VIX); (2) semiconduttori/tech (SOXX/^NDX), spesso il canale più violento perché combina dazi, controlli all'export e concentrazione di supply chain; (3) yuan onshore (CNY=X) come "valvola" di policy cinese; (4) rame (HG=F) come proxy del ciclo industriale globale; (5) dollaro (DX-Y.NYB) e oro (GC=F) come rifugi; (6) Europa (^STOXX50E, ^GDAXI, EURUSD=X) via spillover auto e commercio. L'event study è affidabile per shock discreti, isolabili e non anticipati (es. 22 mar 2018, 5 ago 2019, 2 apr 2025). È inaffidabile dove: (a) l'annuncio arriva via tweet/Truth Social a mercati aperti, rendendo ambiguo il T=0; (b) l'episodio è contaminato da riunioni Fed concomitanti; (c) l'evento era già scontato ("sell-the-rumor/buy-the-news"); (d) si usa CNY=X, che è onshore e gestito entro banda PBOC, quindi cattura il segnale di policy più che il puro mercato.

## 2. Tassonomia dei canali di trasmissione

**Canale 1 — Equity USA / risk-off (^GSPC, ^NDX, ^VIX).**
Catena causale: annuncio dazi → revisione al ribasso delle attese su margini (costi input più alti; la letteratura documenta pass-through completo dei dazi ai prezzi domestici, vedi §Dettagli) + incertezza su supply chain e domanda finale → aumento del premio per il rischio azionario e taglio delle attese di EPS → vendita di ^GSPC/^NDX e acquisto di protezione → spike ^VIX. David Kostin, chief US equity strategist di Goldman Sachs Research, stima che «ogni +5pp di tariffa effettiva USA riduca l'EPS dell'S&P 500 di circa 1-2%, assumendo che le aziende riescano a trasferire gran parte dei dazi ai consumatori». La stessa Goldman Sachs Research quantifica che nel 2018-2019 l'S&P 500 sia sceso di un totale cumulato del 5% nei giorni di annuncio dazi USA e del 7% (leggermente di più) nei giorni di ritorsioni estere. Va distinto l'effetto "sell-the-rumor/buy-the-news": in alcuni annunci attesi il mercato aveva già scontato la notizia e ha reagito poco o in rimbalzo; nelle tregue/pause il rimbalzo è stato violento (es. +9,52% S&P 500 il 9 apr 2025).

**Canale 2 — Semiconduttori / tech (SOXX, ^NDX).**
Catena causale: controllo all'export / dazio su chip → taglio diretto del mercato indirizzabile (revenue China) e timori su capex data-center → repricing dei nomi ad alta beta (Nvidia, AMD, Applied Materials, Lam Research, KLA) → SOXX e, per composizione, ^NDX. È spesso il canale più violento e più "pulito" per l'event study perché gli shock export-control sono discreti e datati (BIS/Federal Register). Datapoint: il 7 ott 2022 (controlli BIS avanzati) il PHLX Semiconductor (SOX) crollò ~6% nella giornata di venerdì e un altro ~3% il lunedì successivo (Fortune, 10 ott 2022), con Nvidia -11% e il SOX già -41% da inizio anno prima dell'annuncio. Il 17 ott 2023 (ban A800/H800) il PHLX Semiconductor bruciò ~$73bn di capitalizzazione (Bloomberg); Nvidia chiuse -4,7% (CNN Business). Il 15-16 apr 2025 (licenza H20 richiesta, charge Nvidia fino a $5,5bn) Nvidia -6/6,5% after-hours il 15, poi il 16 il VanEck Semiconductor ETF (SMH) -4% e AMD -7% (CNBC). Il 15 lug 2025 (riapertura licenze H20/MI308) Nvidia +4% con Nasdaq a chiusura record (CNBC), AMD +4%.

**Canale 3 — Yuan e mercati emergenti (CNY=X, EEM).**
Catena causale: dazi USA sulla Cina → per compensare la perdita di competitività dell'export, la PBOC tollera/guida un deprezzamento del renminbi → CNY=X sale (yuan più debole) → contagio su valute e azioni EM (EEM) via canale di risk-off e timori di currency war. Episodio-cardine: il 5 ago 2019 lo yuan onshore ruppe quota 7/USD per la prima volta dal 2008 (fixing PBOC a 6,9225) dopo la minaccia di dazi sul $300bn del 1 ago; il Tesoro USA sotto il Segretario Steven Mnuchin designò formalmente la Cina "currency manipulator" a mercati chiusi. Caveat cruciale: CNY=X è onshore e gestito entro la banda del "daily fixing" PBOC, quindi cattura il segnale di policy (dove la PBOC "lascia andare" il fixing) più che il puro mercato; lo yuan offshore CNH è più libero ma non è in DB.

**Canale 4 — Rame e ciclo globale (HG=F).**
Catena causale: escalation commerciale → timori su domanda industriale globale (Cina epicentro della domanda di rame) → vendita di HG=F come proxy pro-ciclico ("Dr. Copper"). Attenzione: nel 2025 il rame è stato anche OGGETTO diretto di dazio (Section 232, 50% su semilavorati e derivati intensivi di rame dal 1 ago 2025, Proclamation 10962 del 30 lug — a fronte di un 30% raccomandato dal BIS), che ha creato distorsioni idiosincratiche (arbitraggio COMEX vs LME, front-loading verso i porti USA) — quindi in quel periodo HG=F riflette sia il segnale ciclico sia lo shock tariffario specifico.

**Canale 5 — Dollaro e safe-haven (DX-Y.NYB, GC=F).**
Catena causale nelle fasi acute: escalation → risk-off globale → flusso verso beni rifugio → dollaro forte (DX-Y.NYB su) e oro forte (GC=F su). Va notata l'eccezione del 2025: durante il "Liberation Day" e la fase acuta di aprile 2025, il dollaro in alcune sedute si INDEBOLÌ mentre l'oro saliva — segnale di un parziale ripricing del dollaro come rifugio, atipico rispetto al 2018-2019 (da verificare per singolo evento).

**Canale 6 — Europa (^STOXX50E, ^GDAXI, EURUSD=X).**
Catena causale: dazi su auto/UE o spillover globale → colpo agli esportatori europei (auto tedesche in primis) → vendita ^STOXX50E/^GDAXI; l'effetto su EURUSD=X è ambiguo (risk-off pro-dollaro vs. debolezza ciclica USA).

## 3. Catalogo episodi-ancora datati (elemento centrale)

Legenda tipo: A=annuncio dazi; E=escalation; R=ritorsione; T=tregua/deal; X=controllo export.
Direzione attesa riferita all'asset-canale primario. "no-look-ahead" = cosa era noto/atteso alla data-ancora (nessuna informazione successiva).

| Data ISO | Evento | Tipo | Direzione attesa | Asset-canale (DB) | Note no-look-ahead |
|---|---|---|---|---|---|
| 2018-01-22 | Dazi Section 201 pannelli solari (30%) e lavatrici (20-50%) | A | ↓ equity settoriale (lieve) | ^GSPC | Primo atto protezionista; impatto macro modesto, atteso |
| 2018-03-01 | Annuncio dazi acciaio 25% / alluminio 10% (Section 232) | A | ↓ equity, ↑VIX | ^GSPC, ^VIX | Annuncio a sorpresa; WSJ lo definì "policy blunder"; esenzioni ancora ignote |
| 2018-03-22 | Memorandum Section 301 su ~$50-60bn Cina | A | ↓↓ equity | ^GSPC, ^NDX | Dow -724pt (-2,9%); S&P -2,5%; evento largamente NON anticipato |
| 2018-03-23 | Entrata in vigore dazi 232 acciaio/alluminio | A | ↓ equity | ^GSPC | Data di implementazione; esenzioni temporanee per alleati |
| 2018-06-01 | Fine esenzioni 232 per UE/Canada/Messico | E | ↓ Europa | ^STOXX50E, ^GDAXI | Colpo agli alleati; ritorsioni annunciate |
| 2018-06-22 | Ritorsioni UE (~$3bn: acciaio, bourbon, moto, jeans) | R | ↓ Europa | ^STOXX50E | Harley-Davidson annuncia spostamento produzione |
| 2018-07-06 | Primo round Section 301: 25% su $34bn (List 1) | A/E | ↓ equity/tech | ^NDX, ^GSPC | Prima tariffa 301 effettiva; Cina ritorsione speculare stessa data |
| 2018-08-23 | List 2: 25% su $16bn; ritorsione cinese speculare | E/R | ↓ equity | ^GSPC | Completa i "$50bn"; atteso |
| 2018-09-24 | List 3: 10% su $200bn (poi 25%) | E | ↓ equity, ↑VIX | ^GSPC, ^NDX | Salto di scala della copertura; aumento al 25% previsto 1-gen-2019 |
| 2018-12-01 | Tregua G20 Buenos Aires (Trump-Xi): pausa 90gg | T | ↑ equity | ^GSPC | Rinvio aumento List 3; sollievo temporaneo |
| 2019-05-05 | Tweet Trump: aumento al 25% su $200bn | E | ↓ equity, ↑VIX | ^GSPC, ^VIX | Annuncio via tweet DOMENICA; rompe l'ottimismo su deal imminente |
| 2019-05-10 | Aumento formale List 3 da 10% a 25% | E | ↓ equity | ^GSPC | Implementazione della minaccia del 5 mag |
| 2019-05-13 | Ritorsione cinese su $60bn | R | ↓ equity | ^GSPC | Cina alza dazi su beni USA |
| 2019-06-29 | Tregua G20 Osaka: ripresa negoziati | T | ↑ equity | ^GSPC | Sospensione minaccia $300bn; nessun impegno cinese confermato |
| 2019-08-01 | Minaccia dazi 10% su $300bn (List 4) dal 1-set | E | ↓ equity, ↑VIX | ^GSPC, ^VIX | Annuncio via tweet a mercati aperti; rompe la tregua di Osaka |
| 2019-08-05 | Yuan rompe 7/USD; Cina stop acquisti agricoli; USA "currency manipulator" | E/R | ↑ USD/CNY, ↓ equity, ↑VIX | CNY=X, ^GSPC, ^VIX | Dow -767pt (-2,9%, peggior giorno 2019); S&P -3% a 2.844,74; VIX +36% sopra 23; fixing PBOC 6,9225; designazione a mercati chiusi |
| 2019-08-13 | USTR sposta parte List 4 al 15-dic (elettronica, giocattoli) | A | ↑ equity (sollievo) | ^NDX | Rinvio per stagione shopping; "buy-the-news" parziale |
| 2019-08-23 | Cina ritorsione $75bn; Trump "ordina" alle aziende di lasciare la Cina | E/R | ↓ equity | ^GSPC | Dow -623pt; Trump alza aliquote in risposta |
| 2019-09-01 | Entrata in vigore dazi 15% su tranche List 4A | E | ↓ equity | ^GSPC | Implementazione; parzialmente atteso |
| 2019-10-11 | "Phase One" annuncio verbale (mini-deal) | T | ↑ equity | ^GSPC | Accordo di massima; testo non finalizzato |
| 2019-12-13 | Annuncio accordo Phase One; cancellato dazio 15-dic | T | ↑ equity | ^GSPC, ^NDX | Evita deadline 15-dic (List 4B); mercati a nuovi massimi |
| 2020-01-15 | Firma Phase One alla Casa Bianca | T | ↑ equity (scontato) | ^GSPC | Testo già noto dal 13-dic; reazione contenuta (buy-the-rumor) |
| 2020-02-14 | Entrata in vigore Phase One; List 4A da 15% a 7,5% | T | neutro/↑ | ^GSPC | Dazi List 1-3 (25% su $250bn) restano |
| 2025-02-01 | EO dazi 10% Cina + 25% Canada/Messico (IEEPA) | A/E | ↓ equity | ^GSPC | Annuncio weekend; valutato 3-feb; Canada/Messico poi in pausa |
| 2025-02-10 | Dazi 232 acciaio/alluminio 25%, fine esenzioni | E | ↓ equity (lieve) | ^GSPC | Reazione modesta (+0,4% Russell/Mag7) |
| 2025-03-04 | Dazi Cina da 10% a 20%; dazi pieni Canada | E | ↓ equity | ^GSPC | S&P -1,2% |
| 2025-03-26 | Dazi 232 auto/componenti 25% | A | ↓ Europa/auto | ^GDAXI, ^GSPC | Mag7 -3,0%; colpo diretto auto |
| 2025-04-02 | "Liberation Day": dazio base 10% + reciproci su ~60 partner (EO 14257, IEEPA) | A/E | ↓↓ equity, ↑VIX | ^GSPC, ^NDX, ^VIX | Annuncio dopo chiusura; valutato 3-apr; S&P -4,8% il 3-apr |
| 2025-04-04 | Ritorsione Cina 34%; Dow -2.200pt (2 giorni) | R | ↓↓ equity | ^GSPC, EEM | Peggior 2 giorni da COVID; risk-off globale |
| 2025-04-08 | Dazio addizionale su Cina (totale 104%) | E | ↓ equity | ^GSPC | Russell -2,7%, Mag7 -2,4% |
| 2025-04-09 | Pausa 90gg reciproci (tranne Cina, a 125%) | T | ↑↑ equity | ^GSPC, ^NDX | S&P +9,52% a 5.456,90 (miglior giorno da 2008, 3° post-WWII); Dow +7,87%, Nasdaq +12,16% |
| 2025-04-11 | Esenzione smartphone/semiconduttori da EO 2-apr | T/X | ↑ tech | ^NDX, SOXX | Sollievo settoriale; Mag7 +1,9% |
| 2025-04-15 | Nvidia: licenza richiesta per H20; charge fino a $5,5bn | X | ↓↓ semi | SOXX, ^NDX | Nvidia -6/6,5% AH; SMH -4% e AMD -7% il 16-apr |
| 2025-05-12 | Tregua di Ginevra: reciproci USA-Cina tagliati al 10% per 90gg | T | ↑ equity | ^GSPC, EEM | De-escalation; rally |
| 2025-07-14 | USA riammette licenze H20/MI308 (Nvidia/AMD) | X/T | ↑ semi | SOXX, ^NDX | Nvidia +4% (Nasdaq record close), AMD +4% il 15-lug |
| 2025-07-30 | Dazio 232 rame 50% (dal 1-ago) su semilavorati/derivati (Procl. 10962) | A | volatilità rame | HG=F | Front-loading COMEX; input grezzi/scrap esclusi; BIS aveva raccomandato 30% |
| 2025-08-12 | Estensione tregua Cina di 90gg | T | ↑ equity | ^GSPC | Evita ritorno al 34% |
| 2025-10-09 | Cina: nuovi controlli export su terre rare (annuncio) | R/X | ↓ equity, ↑ oro | ^GSPC, GC=F | Leva cinese; minaccia Trump di 100% dazi |
| 2025-10-30 | Vertice Trump-Xi Busan: tregua 1 anno | T | ↑ equity | ^GSPC, EEM | Cina sospende terre rare 1 anno; fentanyl tariff da 20% a 10% |
| 2025-11-10 | Attuazione deal: fentanyl tariff -10pp; sospensione controlli reciproci | T | ↑ equity | ^GSPC | Sospensioni MOFCOM confermate; reciproci al 10% fino a nov-2026 |
| 2025-12-08 | Trump autorizza export H200 verso Cina (case-by-case) | X/T | ↑ semi (muted) | SOXX | Reazione attenuata/negativa per contro-restrizioni Pechino |

## 4. Statistiche indicative

Cautela: N piccolo, eterogeneità di regime, contaminazione Fed. Cifre da fonti citate, one-day salvo diverso.

- **^GSPC, escalation "pure" (2018-2019):** ordine di grandezza -2,5% / -3,0% one-day nei giorni di annuncio non anticipati (22 mar 2018: -2,5%; 5 ago 2019: -3,0% a 2.844,74). Goldman Sachs Research: cumulato -5% sui giorni di annuncio dazi USA nel 2018-19, e -7% sui giorni di ritorsioni estere.
- **^GSPC, escalation seconda ondata (2025):** più violente: 3-apr-2025 -4,8%; giorni post-Liberation Day fino a -6% (Nasdaq). N piccolo.
- **^GSPC, tregue/deal:** rimbalzi ampi e asimmetrici: +9,52% (9 apr 2025, miglior giorno dal 2008); nuovi massimi dic-2019. La firma "deal" nel 2025 è più violenta di quella "escalation" per via del rimbalzo da livelli ipervenduti.
- **CNY=X:** il movimento-chiave è il salto sopra 7,00 il 5 ago 2019 (fixing 6,9225; yuan onshore ~7,05 in giornata). CNY=X registra soprattutto la decisione di policy PBOC, non un mercato libero.
- **SOXX/semi:** reazioni export-control tra -4% e -6% one-day (index) e fino a -11/-14,5% sul singolo nome (Nvidia, ott 2022); rimbalzi +4% su riaperture licenze (lug 2025).

## 5. Segmentazione in regime phases

**Fase A — Prima guerra commerciale (2018-01-01 → 2019-12-31).**
Firma: escalation gradualista per "liste" e tranche datate, con annunci via tweet crescenti nel 2019; Fed in modalità "insurance cuts" (tagli 31 lug, 18 set, 30 ott 2019; Powell: taglio «per fornire assicurazione contro i rischi in corso»). Powell citò come precedenti i tre tagli del 1995 e del 1998. Questo cuscino monetario ATTENUAVA i drawdown azionari e ne accelerava il recupero; l'S&P chiuse il 2019 a nuovi massimi nonostante l'escalation. Implicazione per l'event study: le finestre T+5/T+10 sono contaminate dalle attese Fed; le reazioni "pure" vanno lette su T+1/T+3. Canale yuan attivissimo (culmine 5 ago 2019). La letteratura (Caldara-Iacoviello et al. 2020) mostra inoltre che l'incertezza di policy commerciale — non solo i dazi effettivi — riduceva investimenti e attività, un canale "lento" che non si cattura in finestre strette di event study.

**Fase B — Tregua / Phase One (2020-01-01 → 2020-12-31).**
Firma: de-escalation, poi shock COVID che DOMINA qualsiasi segnale tariffario da fine feb 2020. L'event study tariffario è di fatto inservibile nel Q1-Q2 2020 per contaminazione pandemica. Utile solo la finestra gen 2020 (firma Phase One, 15-gen) come esempio di "buy-the-rumor/sell-the-news" (testo noto dal 13-dic).

**Fase C — Seconda ondata (2025-01-01 → presente).**
Firma: dazi generalizzati e simultanei (IEEPA, non solo 301/232), su decine di partner, con ampiezza e velocità superiori; strumenti nuovi (reciproci "Liberation Day", controlli export su chip come arma bidirezionale, terre rare cinesi come contro-leva). Contesto Fed diverso: inflazione post-pandemica ancora vicino/sopra target, Fed meno automaticamente dovish → minor cuscino, beta potenzialmente più alto e recuperi meno garantiti dalla politica monetaria. Da VERIFICARE puntualmente la reaction function Fed nel 2025-2026 per ogni episodio. Nota istituzionale: molti dazi 2025 poggiano su IEEPA, la cui legittimità è stata oggetto di contenzioso (i risultati di search indicano una sentenza della Corte Suprema nel 2026 nel caso *Learning Resources v. Trump* — da verificare come rischio di reversal, non come fatto assodato per l'event study).

**Perché non mischiare i regimi:** (1) diversa reaction function Fed (cuscino 2019 presente, incerto 2026); (2) diversa ampiezza e simultaneità degli shock (liste mirate vs. dazi universali); (3) diversi strumenti (301/232 vs. IEEPA + export controls + terre rare); (4) diverso comportamento del dollaro come rifugio (classico 2019 vs. atipico apr-2025). Un event study che pooli 2019 e 2025 stima un beta medio privo di significato: la reaction function della Fed nel 2019 era un contro-bilanciamento sistematico che nel 2026 non si può assumere presente.

## 6. Caveat metodologici

1. **Scelta del T=0.** Nel 2018-2019 (e ancor più nel 2025) molti annunci arrivavano via tweet/Truth Social a mercati aperti o nei weekend. Regole operative: per annunci weekend usare la prima seduta utile (es. 2-feb-2025 → 3-feb; AIER usa 3-feb come proxy); per annunci post-chiusura usare la variazione close-to-close del giorno successivo (es. Liberation Day 2-apr → valutazione 3-apr); per tweet intraday, considerare che parte della reazione è già nel close del giorno stesso.
2. **Contaminazione Fed.** Nel 2019 tre tagli concomitanti; isolare per quanto possibile escludendo finestre che includono FOMC (30-31 lug, 17-18 set, 29-30 ott 2019).
3. **Regime-mixing 2019 vs 2026.** Non poolare; stimare beta separati per fase.
4. **CNY=X onshore e gestito.** Cattura il segnale di policy PBOC (banda/fixing), non il mercato puro; per il "vero" mercato valutario servirebbe CNH offshore (non in DB).
5. **No look-ahead.** Per ogni episodio, condizionare solo sull'informazione disponibile alla data-ancora (es. il 13-dic-2019 il testo Phase One era già noto, quindi il 15-gen è "news" solo per la firma formale, non per il contenuto).
6. **Sovrapposizione di eventi.** Nel 2025 dazi, controlli export e ritorsioni si sono accavallati in giorni contigui (2-11 apr): difficile isolare il singolo canale; usare finestre strette T+1.
7. **Reazioni after-hours vs. seduta regolare.** Per gli shock export-control (es. Nvidia H20, 15-16 apr 2025) la reazione più violenta è spesso after-hours: distinguere il close-to-close del giorno-annuncio dalla seduta successiva.
8. **Asset esterni non in DB.** Singoli titoli tariff-exposed (auto, industriali, agricoltura), soybean/commodity agricole, yuan offshore CNH e indici settoriali US/EU vanno segnalati come external_assets_mentioned, non usati come asset-canale nella tabella.

## Riferimenti scientifici chiave (autore, anno, rivista, finding)

- **Amiti, Redding, Weinstein (2019), *Journal of Economic Perspectives* 33(4):187-210** — "The Impact of the 2018 Tariffs on Prices and Welfare": pass-through completo dei dazi ai prezzi domestici; incidenza interamente su consumatori/importatori USA; riduzione del reddito reale USA di $1,4bn/mese a fine 2018.
- **Fajgelbaum, Goldberg, Kennedy, Khandelwal (2020), *Quarterly Journal of Economics* 135(1):1-55** — "The Return to Protectionism": pass-through completo ai prezzi duty-inclusive; perdite per consumatori/imprese USA $51bn (0,27% del PIL); perdita netta aggregata $7,2bn (0,04% del PIL) dopo revenue e guadagni ai produttori domestici.
- **Caldara, Iacoviello, Molligo, Prestipino, Raffo (2020), *Journal of Monetary Economics* 109:38-59** — "The Economic Effects of Trade Policy Uncertainty": costruzione del TPU Index; un aumento della TPU riduce investimenti e attività; la TPU avrebbe ridotto gli investimenti privati USA di ~1-1,5% nel 2018; sono gli ANNUNCI/anticipazioni, non solo i dazi effettivi, a generare gli effetti macro.
- **USITC (2023), Pub. 5405** — effetti Section 232/301: 301 ridusse import di semiconduttori dalla Cina del 72,3% e alzò i prezzi USA del 4,1%; effetti downstream 232 modesti ma negativi sulla produzione a valle.

---

```yaml
---
title: "Dazi e guerra commerciale USA — regime ed episodi storici (2018–2026)"
date_compiled: 2026-07-13
primary_theme: geopolitical
sub_themes: [trade_war, tariffs, us_china, protectionism, supply_chain, export_controls, trade_policy_uncertainty, cny, risk_off]
relevant_assets: [^GSPC, ^NDX, SOXX, CNY=X, EEM, HG=F, ^VIX, DX-Y.NYB, GC=F, ^STOXX50E, ^GDAXI, EURUSD=X]
external_assets_mentioned:
  - "singoli titoli tariff-exposed (auto, industriali, agricoltura) — non in DB"
  - "soybean / commodity agricole — non in DB"
  - "yuan offshore CNH — non in DB (storia yfinance assente)"
  - "indici settoriali US/EU — non in DB"
time_window:
  start: 2018-01-01
  end: present
regime_phases:
  - first_trade_war_2018_2019: 2018-01-01 to 2019-12-31
  - phase_one_truce_2020: 2020-01-01 to 2020-12-31
  - second_wave_tariffs_2025_2026: 2025-01-01 to present
keywords: [dazi, tariffs, trade war, guerra commerciale, section 301, section 232, usmca, us-china, cina, yuan, cny, liberation day, trump tariffs, phase one, export controls, semiconductor, chip, protezionismo, supply chain, trade policy uncertainty, retaliation, wto, piie, risk-off]
---
```