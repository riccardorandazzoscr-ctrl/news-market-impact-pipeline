# Regno Unito: shock politici e monetari — regime ed episodi storici (2016–2026)

## 1. Sintesi esecutiva

La tesi centrale è che, nello spettro di shock-notizia britannici 2016–2026, l'unico canale di trasmissione UK-specifico e robustamente misurabile con l'universo-DB attuale è la **STERLINA** (`GBPUSD=X`): premio di rischio politico/fiscale → deprezzamento/apprezzamento del cambio. I **gilt** — la variabile dove la reazione è spesso più violenta (mini-budget 2022, episodi Reeves/Starmer 2025–26) — NON sono nel DB; vanno trattati come covariata esterna e approssimati solo grossolanamente col canale tassi globale (`^TNX`, `IEF`) e con il risk-off (oro `GC=F`, `^VIX`, `DX-Y.NYB`). Gli episodi si dividono in regimi strutturalmente diversi: (i) shock Brexit e incertezza negoziale 2016–2019; (ii) pandemia/QE 2020–2021; (iii) shock fiscale e crisi gilt 2022; (iv) disinflazione e ciclo tagli BoE 2023–2026, con sovrapposto un sottostrato di transizioni di leadership 2024–2026. L'event study è più affidabile per shock discreti, esogeni e a sorpresa (referendum Brexit; mini-budget; elezione 2019; *tears* di Reeves) e meno affidabile dove lo shock è atteso/prezzato (la maggior parte dei tagli BoE 2024–26, ampiamente anticipati) o contaminato da fattori macro globali concomitanti (ciclo inflazione 2022; conflitto Medio Oriente 2026). Disciplina costante: distinguere **FATTO DATATO** da **INTERPRETAZIONE**, e specificare per ogni ancora cosa era noto/atteso alla data (no look-ahead).

## 2. Tassonomia dei canali di trasmissione

**Sterlina (`GBPUSD=X`) — canale dominante e unico UK-specifico nel DB.** Catena causale: shock politico/fiscale → revisione delle aspettative sul percorso futuro di crescita/apertura commerciale/credibilità fiscale + variazione del premio di rischio politico → riallocazione di portafoglio fuori da asset in GBP → deprezzamento. Manasse, Moramarco & Trigilia (2024, *Economica* 91(362):621–652) mostrano che la sterlina incorpora un premio di rischio politico *time-varying* distinto dalle aspettative sul livello del cambio: la probabilità di Leave prediceva un deprezzamento, e il rischio politico agiva indipendentemente. Costa et al. (2024, *Journal of International Economics*) documentano che il 24/06/2016 il crollo fu il maggiore calo giornaliero di una delle quattro valute principali dal crollo di Bretton Woods.

**Gilt / tassi (NON nel DB → proxy imperfetta).** Catena causale: shock di credibilità fiscale → aumento del *term premium* e dei rendimenti gilt (soprattutto sul tratto lungo, dove siede il rischio di offerta). Limite metodologico critico: i gilt e lo spread gilt-Bund non sono nel DB. `^TNX` (rendimento 10Y Treasury USA) e `IEF` (ETF Treasury 7–10Y) catturano solo la componente tassi globale e il contagio risk-off, NON la componente UK-specifica del rendimento gilt — che nel 2022 e nel 2025–26 fu proprio la parte dominante. Usare `^TNX`/`IEF` come proxy del gilt introduce errore di misura sistematico; va dichiarato.

**Risk-off / safe-haven (`GC=F`, `DX-Y.NYB`, `^VIX`).** Catena causale: crisi acuta/sistemica → fuga verso la qualità → oro e dollaro su, VIX su. Il 24/06/2016 il VIX salì 8,5 punti da 17,3 a 25,8 (S&P 500 −3,6%), il "biggest one-day rise since the Chinese-induced sell-off in August 2015" (Cboe, *VIX Index Attribution of Notable Tail Events*; The Hedge Fund Journal), e l'oro salì. Nel 2022 il canale fu più attenuato verso il dollaro per via del ciclo Fed concomitante.

**Spillover europeo (`^STOXX50E`, `^GDAXI`, `EURUSD=X`; `BTP_BUND_SPREAD` solo per stress sistemico).** Catena causale: shock UK → revisione integrazione finanziaria EU + canale commerciale → equity euro e EUR. Il `BTP_BUND_SPREAD` va usato SOLO nei momenti di stress sistemico (es. picco crisi gilt 2022) come proxy di frammentazione della periferia, non per shock politici idiosincratici UK.

**Equity UK (FTSE 100 — NON nel DB, variabile esterna).** Paradosso noto: sterlina debole → FTSE 100 su, perché la quota dominante dei ricavi delle large cap è estera. Secondo l'analisi FTSE Russell (ottobre 2022), "around 82% of the FTSE 100 revenues are from overseas markets", mentre per il FTSE 250 la cifra scende a circa il 57%. Breinlich et al. (2018, *Fiscal Studies*) e la FEDS Note del Fed (2026) documentano che il FTSE 100 recuperò rapidamente e sovraperformò post-Brexit proprio grazie al deprezzamento. Quindi il FTSE 100 NON è un buon proxy del sentiment UK domestico; il FTSE 250 lo sarebbe di più (ma anch'esso fuori DB).

## 3. Catalogo episodi-ancora datati

Legenda tipo: REF=referendum/voto; FISC=shock fiscale; BOE=decisione BoE; LEAD=transizione di leadership; EMERG=intervento di emergenza.

| Data ISO | Evento | Tipo | Direzione attesa | Asset-canale (DB) | Note no-look-ahead |
|---|---|---|---|---|---|
| 2016-06-23 | Giorno del referendum Brexit (voto) | REF | GBP ↑ se Remain (atteso) | `GBPUSD=X` | Alle 22:00 il mercato prezzava Remain (~$1.50); esito ignoto fino a notte |
| 2016-06-24 | Apertura mercati post-esito Leave | REF | GBP ↓↓, risk-off | `GBPUSD=X`, `^VIX`, `GC=F`, `^STOXX50E`, `^GDAXI`, `EURUSD=X` | GBP −8% vs USD in 24h; shock a sorpresa puro |
| 2016-06-24 | Dimissioni Cameron | LEAD | GBP ↓ (marginale) | `GBPUSD=X` | Contemporaneo all'esito; effetto non isolabile dal voto |
| 2016-10-02 | Conf. Tory May: hard Brexit | REF/LEAD | GBP ↓ | `GBPUSD=X` | Prima conferma direzione "hard"; sterlina verso $1.18 intraday a ottobre |
| 2016-10-07 | Flash crash sterlina | FISC/altro | GBP ↓↓ intraday | `GBPUSD=X` | Evento tecnico/algoritmico; non politico puro |
| 2017-01-17 | Discorso Lancaster House (May) | REF | GBP ambiguo | `GBPUSD=X` | Chiarezza riduce premio rischio nonostante hard Brexit |
| 2017-03-29 | Attivazione Articolo 50 | REF | GBP ↓ lieve | `GBPUSD=X` | Ampiamente atteso → reazione contenuta |
| 2017-06-08 | Elezioni generali: hung parliament | REF | GBP ↓ | `GBPUSD=X` | Exit poll a sorpresa (atteso: maggioranza Tory); GBP −2% |
| 2018-12-10 | Rinvio del primo *meaningful vote* | REF | GBP ↓ | `GBPUSD=X` | May rinvia perché sconfitta certa |
| 2019-01-15 | Primo *meaningful vote*: sconfitta 432–202 | REF | GBP ambiguo | `GBPUSD=X` | Sconfitta record ma largamente attesa → reazione attenuata |
| 2019-03-12 | Secondo *meaningful vote*: sconfitta 391–242 | REF | GBP ambiguo | `GBPUSD=X` | Atteso |
| 2019-03-29 | Terzo *meaningful vote*: sconfitta 286–344 | REF | GBP ↓ | `GBPUSD=X` | Data originaria Brexit; incertezza estensione |
| 2019-05-24 | Annuncio dimissioni May | LEAD | GBP ↓ | `GBPUSD=X` | Apre fase Johnson/no-deal |
| 2019-07-24 | Johnson PM | LEAD | GBP ↓ | `GBPUSD=X` | Aumenta rischio no-deal |
| 2019-08 (fine) | Picco timori no-deal | REF | GBP ↓↓ | `GBPUSD=X` | Sterlina ~$1.196, minimo dal 2016 |
| 2019-12-12/13 | Elezione: maggioranza Johnson | REF/LEAD | GBP ↑↑ | `GBPUSD=X` | Exit poll → GBP +2%, $1.3445; riduzione premio rischio |
| 2020-01-31 | Brexit formale | REF | GBP neutro | `GBPUSD=X` | Atteso, prezzato |
| 2020-03-11/19 | Tagli emergenza BoE Covid (a 0,10%) | BOE/EMERG | GBP ↓, risk-off | `GBPUSD=X`, `^VIX`, `GC=F` | Shock pandemia globale, non UK-specifico |
| 2022-09-06 | Truss PM | LEAD | GBP ↓ lieve | `GBPUSD=X` | Attesa politica fiscale espansiva |
| 2022-09-23 | Mini-budget Kwarteng ("Growth Plan") | FISC | GBP ↓↓, gilt ↓↓ | `GBPUSD=X` (gilt esterno) | £45bn tagli non finanziati senza forecast OBR; 3° peggior giorno GBP vs USD dal 1992 |
| 2022-09-26 | Minimo storico sterlina | FISC | GBP ↓↓ | `GBPUSD=X`, `DX-Y.NYB` | $1.0327, minimo da decimalizzazione 1971 |
| 2022-09-28 | Intervento emergenza BoE sui gilt (LDI backstop) | EMERG | GBP/gilt stabilizzazione | `GBPUSD=X` (gilt esterno), `^TNX` | Acquisti temporanei gilt lunghi; stress sistemico → `BTP_BUND_SPREAD` rilevante |
| 2022-10-14 | Licenziamento Kwarteng | FISC/LEAD | GBP ambiguo | `GBPUSD=X` | Hunt cancelliere |
| 2022-10-17 | Hunt annulla mini-budget | FISC | GBP ↑, gilt ↑ | `GBPUSD=X` | Ripristino credibilità fiscale |
| 2022-10-20 | Dimissioni Truss | LEAD | GBP ↑ lieve | `GBPUSD=X` | PM più breve della storia (49 gg) |
| 2022-10-25 | Sunak PM | LEAD | GBP ↑ | `GBPUSD=X` | Rendimenti gilt 30Y tornano a livelli pre-mini-budget |
| 2024-07-04/05 | Elezione: landslide Labour (Starmer) | REF/LEAD | GBP neutro/↑ lieve | `GBPUSD=X` | Ampiamente atteso (sondaggi) → reazione contenuta |
| 2024-08-01 | Primo taglio BoE del ciclo (5,25%→5,0%) | BOE | GBP ↓ lieve | `GBPUSD=X`, `^TNX` | Voto 5–4 (riunione conclusa 31/07); mossa al limite del prezzato |
| 2024-11-07 | Taglio BoE a 4,75% | BOE | GBP ↓ lieve | `GBPUSD=X` | Voto 8–1; atteso |
| 2025-02-06 | Taglio BoE a 4,5% | BOE | GBP ↓ lieve | `GBPUSD=X` | Voto 7–2 (riunione conclusa 05/02) |
| 2025-05-08 | Taglio BoE a 4,25% | BOE | GBP ↓ lieve | `GBPUSD=X` | Voto 5–4 (riunione conclusa 07/05); contaminato da shock tariffe USA |
| 2025-07-02 | "Tears" di Reeves in Parlamento | LEAD/FISC | GBP ↓, gilt ↓↓ | `GBPUSD=X` (gilt esterno) | Timore uscita Reeves → premio rischio fiscale |
| 2025-08-07 | Taglio BoE a 4,0% | BOE | GBP ↓ lieve | `GBPUSD=X` | Voto 5–4 (riunione conclusa 06/08) |
| 2025-12-18 | Taglio BoE a 3,75% | BOE | GBP ↓ lieve | `GBPUSD=X` | Voto 5–4 (riunione conclusa 17/12); sesto taglio dal 2024 |
| 2026-05-07/08 | Elezioni locali; pressione su Starmer | LEAD | GBP ↓, gilt ↓↓ | `GBPUSD=X` (gilt esterno) | Gilt 10Y ai massimi dal 2008 |
| 2026-06-18/22 | By-election Makerfield (Burnham); dimissioni Starmer | LEAD | GBP/gilt volatilità | `GBPUSD=X` | Starmer si dimette 22/06; apre contesa leadership |
| 2026-07-09 | Apertura nomination leadership Labour | LEAD | GBP/gilt incertezza | `GBPUSD=X` (gilt esterno) | Catalyst di leadership imminente; esito ignoto alla data |

**Nota episodi pre-2011 / fuori finestra prezzi:** episodi storici come Black Wednesday (1992) e la crisi del 2008 sono citati solo come benchmark comparativi; il loro event study NON è calcolabile col DB attuale (la finestra prezzi parte dopo). Anche tutto ciò che precede il 23/06/2016 resta fuori dalla finestra dello studio.

## 4. Statistiche indicative (mai obbligatorie)

Ampiezza tipica della reazione di GBP per tipo di episodio (N piccolo; trattare come ordine di grandezza, non stima puntuale):

- **Shock a sorpresa esogeno e binario** (referendum 2016, elezione 2019): movimento GBP/USD di 2–8% in T+1. Brexit 24/06/2016: −8% vs USD, −6% vs EUR (24h). Elezione 12–13/12/2019: +2%. N≈2 → altissima incertezza.
- **Shock fiscale di credibilità** (mini-budget 2022): GBP/USD da ~$1.12 a minimo $1.0327 in ~3 giorni di trading (≈ −8% cumulato), con la reazione dominante sui gilt — il rendimento gilt 30Y salì di 120bp in tre giorni ("the 30-year gilt yield spiking 120 basis points over three days, one of the largest yield increases ever seen in such a short space of time", EFG International). N=1.
- **Decisioni BoE attese** (gran parte dei tagli 2024–26): reazione GBP spesso <1% e talvolta di segno contrario alle attese (cut già prezzati; conta la *guidance*). Event study debole per questi.
- **Mini-crisi di leadership/fiscali** (*tears* di Reeves 2025; pressioni Starmer 2026): GBP ↓ modesto ma gilt lunghi a massimi pluridecennali — la firma è sul tratto lungo della curva (fuori DB), non sul cambio.

## 5. Segmentazione in regime phases databili

**(i) `brexit_uncertainty_2016_2019` (2016-06-23 → 2019-12-31).** Firma: GBP guidato dal premio di rischio politico; il cambio è il termometro principale; equity UK (FTSE 100) anticorrelata col cambio (paradosso esportatori). Risk-off episodico ma non sistemico. La sterlina resta persistentemente più debole (Breinlich et al. 2018; Costa et al. 2024).

**(ii) `pandemic_qe_2020_2021` (2020-01-01 → 2021-12-31).** Firma: shock globale, non UK-specifico; GBP guidato dal dollaro-safe-haven e dal QE; gli shock UK-idiosincratici sono sommersi dal Covid. Event study UK-specifico quasi inutilizzabile.

**(iii) `fiscal_shock_gilt_crisis_2022` (2022-01-01 → 2022-12-31).** Firma: shock di credibilità fiscale → GBP ↓↓ E gilt ↓↓ simultaneamente (rara correlazione positiva yield-up/GBP-down "da mercato emergente"); stress sistemico con possibile contagio (`BTP_BUND_SPREAD` rilevante solo qui). L'intervento BoE del 28/09 è il punto di svolta.

**(iv) `disinflation_boe_cuts_2023_2026` (2023-01-01 → presente).** Firma: GBP guidato dal differenziale-tassi e dalla "reaction function" BoE (servizi sticky + salari); tagli ampiamente prezzati → bassa reattività del cambio agli annunci MPC. Sovrapposto: transizioni di leadership 2024–26 con firma sui gilt lunghi (*term premium*/rischio fiscale) più che sul cambio.

**Perché mischiarli distrugge il segnale:** il segno della correlazione GBP–gilt cambia tra regimi (negativa-difensiva nel 2016; "emergente" positiva nel 2022); i tagli BoE attesi diluiscono la reattività media; e il Covid introduce un grande blocco di varianza non-UK. Stimare un unico CAR medio su tutto il campione mescola meccanismi opposti.

## 6. Caveat metodologici

1. **Bassa numerosità.** Diversi regimi/tipi hanno N=1–2 (mini-budget; crisi gilt; elezioni binarie). Nessuna inferenza statistica robusta; usare gli ampiezza-tipo come ordine di grandezza.
2. **Contaminazione macro concomitante.** 2022: ciclo inflazione/rialzi tassi globali; 2025–26: tariffe USA e conflitto Medio Oriente con shock energetico. Isolare la componente UK richiede covariate di controllo (`^TNX`, `DX-Y.NYB`).
3. **Dipendenza dal sentiment fiscale.** Dal 2022 il driver dominante degli shock UK è la credibilità fiscale, che si scarica soprattutto sui gilt lunghi — fuori DB.
4. **FTSE 100 e gilt non nel DB.** Da trattare come covariate esterne; il FTSE 100 è fuorviante come proxy domestico per il paradosso esportatori.
5. **No look-ahead.** Per ogni ancora va fissato l'orizzonte informativo alla data: es. l'esito Brexit era ignoto fino a notte fonda del 23/06; molte sconfitte ai *meaningful votes* erano già attese (reazione attenuata).
6. **Proxy gilt imperfetta.** `^TNX`/`IEF` non catturano la componente UK-specifica; rischio di errore di misura sistematico nei momenti di stress idiosincratico UK.

## 7. Approfondimento: i due episodi-cardine

**Mini-budget e crisi gilt 2022 (il regime fiscale puro).** Il 23/09/2022 Kwarteng annunciò £45mld di tagli fiscali non finanziati senza una previsione OBR di accompagnamento. La sterlina perse il 3% vs USD il giorno stesso e toccò il minimo storico di $1.0327 il 26/09; i gilt subirono uno dei maggiori sell-off della storia. Il meccanismo del *doom loop*: la salita dei rendimenti innescò *margin call* sui fondi LDI (*liability-driven investment*) dei fondi pensione, che vendettero gilt per fare cassa, alimentando ulteriori rialzi di rendimento (fire-sale). Il 28/09/2022 la BoE intervenne con un *backstop* temporaneo e mirato di acquisti di gilt lunghi; acquistò solo £19,26mld dei £65mld stanziati tra il 28/09 e il 14/10 (EFG International) — coerente col £19,3bn di Alexander et al. (2023). L'inversione fiscale di Hunt (17/10) e l'arrivo di Sunak (25/10) riportarono i rendimenti 30Y ai livelli pre-mini-budget. Questo è l'esempio paradigmatico in cui GBP e gilt si muovono "da mercato emergente".

**Le mini-crisi di leadership 2025–2026 (regime fiscale-politico).** Il 02/07/2025 "U.K. bond yields spiked and the pound sank against the dollar and euro as tears fell down Chancellor Rachel Reeves' face... traders speculated that Reeves could be about to lose her job" (CNBC, 3 luglio 2025): il mercato prezzava che l'uscita di Reeves avrebbe significato l'abbandono delle *fiscal rules*. La firma di questi episodi è sul tratto lungo della curva gilt: a fine 2025 la BoE rilevò che "10-year yields [were] at levels previously observed in 2008 and 30-year yields at their highest levels since the turn of this century" (BoE, *What were the drivers of UK long-term interest rates in 2025?*, dati al 19/12/2025). La contesa di leadership Labour aperta dalle dimissioni di Starmer (22/06/2026), con apertura nomination il 09/07/2026 e Andy Burnham frontrunner, è il catalyst aperto alla data di compilazione: l'esito è ignoto e i gilt restano il termometro principale del rischio fiscale percepito.

## Recommendations

1. **Privilegiare GBPUSD=X come variabile dipendente primaria** per ogni event study UK-specifico, e usare gli altri ticker DB (`^VIX`, `GC=F`, `DX-Y.NYB`, `^STOXX50E`, `^GDAXI`, `EURUSD=X`) come canali di conferma risk-off/spillover. Soglia decisionale: se la reazione di GBP a T+1 è < ±0,5%, considerare lo shock "prezzato" e declassare l'evento.
2. **Stimare i CAR separatamente per regime**, mai pooled sull'intero 2016–2026. Benchmark che cambia la strategia: se la correlazione GBP–`^TNX` cambia segno tra due sotto-finestre, NON aggregarle.
3. **Tarare gli orizzonti T+1/T+3/T+5/T+10 sul tipo di shock.** Per shock binari a sorpresa (Brexit, 2019) la maggior parte del segnale è in T+1; per crisi di credibilità (2022) la dinamica si dispiega su T+3/T+5 (fire-sale + risposta di policy); per i tagli BoE attesi usare T+1 con controllo per la sorpresa rispetto alla curva OIS.
4. **Includere covariate di controllo globali** (`^TNX`, `DX-Y.NYB`) in ogni regressione per assorbire la contaminazione macro 2022 e 2025–26 (tariffe USA, shock energetico Medio Oriente).
5. **Trattare gilt e FTSE 100 come `external_assets_mentioned`**: documentarli in narrativa ma non usarli come asset-canale calcolabile; segnalare esplicitamente la proxy imperfetta `^TNX`/`IEF`.
6. **Pre-registrare la lista `--events`** con le date ISO della Sezione 3, marcando per ciascuna il flag "atteso/sorpresa" per evitare look-ahead. Per il 09/07/2026 trattare l'evento come *forward-looking*: la sua finestra T+ non sarà calcolabile fino a maturazione dei prezzi post-data.

## Caveats

- **Numerosità strutturalmente bassa**: gli episodi più informativi (mini-budget, crisi gilt, elezioni binarie) hanno N=1–2; nessuna inferenza statistica forte è difendibile, solo ordini di grandezza.
- **Contaminazione macro pervasiva**: 2022 (inflazione/rialzi globali), 2025–26 (tariffe USA, conflitto Medio Oriente con shock energetico). La componente UK-specifica va isolata, mai assunta.
- **Il driver è migrato dai gilt al cambio e ritorno**: nel 2016–19 il segnale è sul cambio; nel 2022 e 2025–26 il segnale dominante è sui gilt lunghi — proprio l'asset fuori DB. L'event study col DB attuale è quindi sistematicamente più cieco proprio negli episodi fiscali più violenti.
- **FTSE 100 fuorviante** come proxy domestico (paradosso esportatori, ~82% ricavi esteri).
- **Eventi 2026 in evoluzione**: la contesa di leadership Labour e il catalyst del 09/07/2026 sono aperti alla data di compilazione (2026-06-23); ogni direzione attesa è interpretazione, non fatto.
- **Conflitto di fonti note**: il dato sulla durata di Truss appare come "49 giorni" e "44 giorni" a seconda della fonte e del riferimento (insediamento vs. annuncio dimissioni vs. uscita effettiva 25/10); qui si riporta come "PM più breve della storia". Le voci di mercato intraday non datate da fonti primarie (Reuters/Bloomberg) restano da verificare nel pipeline prima dell'uso quantitativo.

---

```yaml
title: "Regno Unito: shock politici e monetari — regime ed episodi storici (2016–2026)"
date_compiled: 2026-06-23
primary_theme: geopolitical
sub_themes: [monetary_policy, fiscal_policy, uk_political_risk, gbp, boe_reaction_function, boe, uk_cpi, cpi, inflation, macro_data, gilt_crisis, brexit, leadership_transition, safe_haven_flows]
relevant_assets: [GBPUSD=X, ^TNX, IEF, GC=F, ^VIX, DX-Y.NYB, ^STOXX50E, ^GDAXI, EURUSD=X, BTP_BUND_SPREAD]
external_assets_mentioned:
  - "FTSE 100 — non in DB"
  - "rendimenti gilt UK 2Y/10Y/30Y — non in DB"
  - "spread gilt-Bund — non in DB"
  - "indici settoriali UK — non in DB"
time_window:
  start: 2016-06-23
  end: present
regime_phases:
  - brexit_uncertainty_2016_2019: 2016-06-23 to 2019-12-31
  - pandemic_qe_2020_2021: 2020-01-01 to 2021-12-31
  - fiscal_shock_gilt_crisis_2022: 2022-01-01 to 2022-12-31
  - disinflation_boe_cuts_2023_2026: 2023-01-01 to present
keywords: [uk, regno unito, brexit, referendum, truss, kwarteng, mini-budget, gilt crisis, ldi, pension funds, bank of england, boe, mpc, bailey, rate cuts, services inflation, sterlina, gbp, pound, starmer, labour, sunak, leadership transition, fiscal credibility, obr, risk-off, safe haven]
```