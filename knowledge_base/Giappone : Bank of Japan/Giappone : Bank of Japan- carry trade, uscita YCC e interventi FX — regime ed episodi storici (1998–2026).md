# Giappone / Bank of Japan: carry trade, uscita YCC e interventi FX — regime ed episodi storici (1998–2026)

## 1. Sintesi esecutiva
La tesi centrale è che lo **yen carry trade unwind** è il canale di trasmissione più potente e sotto-apprezzato tra le decisioni giapponesi e i mercati globali: quando lo yen si rafforza bruscamente, non è un fatto locale ma uno shock di rischio cross-asset che colpisce ^N225, ^NDX, ^GSPC e fa esplodere ^VIX. Il driver primario resta la BoJ (`monetary_policy`), ma il valore per un event study sta nel canale risk-off. Distinguiamo due nature di evento profondamente diverse: (a) le **decisioni BoJ attese/telegrafate** (es. uscita NIRP marzo 2024), che producono reazioni modeste e talvolta "contrarie" (yen più debole dopo un rialzo, perché la guidance resta accomodante); (b) gli **unwind improvvisi guidati dal risk-off** (5 agosto 2024, ottobre 1998, autunno 2008), che hanno code negative violente e asimmetriche. L'event study è affidabile per gli eventi discreti e isolabili post-2011 (coperti dal DB prezzi): decisioni BoJ datate, interventi MoF confermati, il crash del 5 agosto 2024. È meno affidabile dove: gli episodi sono ibridi (un unwind innescato da dati USA deboli — il payroll del 2 agosto 2024), il timing T=0 è ambiguo per il fuso Tokyo/NY, e gli interventi FX sono difficili da datare ex-ante. Gli episodi pre-2011 (LTCM 1998, deleveraging 2008) sono fuori dal DB prezzi: vanno segnalati come precedenti strutturali ma il loro event study non è calcolabile. Attenzione metodologica capitale: la fortissima skewness negativa del carry (Brunnermeier-Nagel-Pedersen) significa che media e mediana divergono molto e che il campione dei crash è piccolo (N basso), quindi le statistiche vanno lette con enorme cautela.

## 2. Tassonomia dei canali di trasmissione

### 2.1 Yen (USD/JPY) — canale diretto
Catena causale: decisione BoJ (o variazione del differenziale tassi US-JP) → repricing di JPY=X. Un rialzo BoJ o una guidance hawkish restringe il differenziale con la Fed e tende a rafforzare lo yen (USD/JPY giù). Poiché lo yen è la valuta di funding per eccellenza, uno yen più forte accompagna il risk-off: gli investitori che si erano finanziati in yen devono ricomprarlo. Il canale diretto è il più pulito da datare quando la decisione è discreta.

### 2.2 Carry trade unwind → risk-off globale (meccanismo cruciale)
Catena causale esplicita: investitori si finanziano in yen a tasso ~0 → convertono in USD/MXN/AUD e comprano asset a rendimento più alto (Treasury, tech USA, EM) → guadagno = differenziale + leva. Quando lo yen si rafforza bruscamente (per un rialzo BoJ, dati USA deboli, o uno shock di volatilità), le posizioni vanno in perdita → margin call → vendite forzate simultanee su entrambe le gambe (ricomprare yen + vendere gli asset comprati) → ^N225 e ^NDX/^GSPC giù, ^VIX su. È il canale che rende lo yen un **evento globale**. La dimensione del carry in yen è intrinsecamente imprecisa: secondo il BIS Bulletin No. 90 (Aquilina, Lombardi, Schrimpf, Sushko, agosto 2024), "various estimates based on both on- and off-balance sheet activity yield a rough middle ballpark of ¥40 trillion ($250 billion) going into the event, which, if anything, is biased down due to data gaps"; stime sell-side arrivano fino a $500 mld di picco (UBS) o cifre molto più ampie ($1-20 trilioni) a seconda di quanto ampiamente si misura. La teoria (Brunnermeier-Pedersen 2009, "Market Liquidity and Funding Liquidity", RFS) spiega le "liquidity spirals": shock che generano perdite per gli speculatori sono amplificati quando questi colpiscono i vincoli di funding, deprimendo ulteriormente i prezzi e aumentando volatilità e margini.

### 2.3 Azionario giapponese (^N225)
Catena causale: yen forte → gli esportatori giapponesi (Toyota, Sony, Tokyo Electron) vedono ridursi i ricavi esteri tradotti in yen → margini compressi → Nikkei giù. Relazione inversa storica yen/Nikkei. Nel crash del 5 agosto 2024, secondo Reuters, Tokyo Electron (produttore di apparecchiature per chip) perse il 18,48% e fu il maggior peso sul Nikkei, mentre SoftBank Group crollò del 18,66%.

### 2.4 Tassi USA (^TNX / IEF)
Catena causale ambigua e bidirezionale: (a) risk-off → fuga verso i Treasury → rendimenti giù (^TNX giù, IEF su); (b) ma un carry unwind può comportare vendite di Treasury per coprire posizioni → rendimenti su. Inoltre, flussi di rimpatrio giapponese e repricing globale dei tassi contano: il Giappone è il primo detentore estero di Treasury USA. Il segno netto su ^TNX in un unwind è quindi incerto e va verificato caso per caso.

### 2.5 Safe-haven
Lo yen stesso è bene rifugio: in risk-off gli investitori comprano JPY per la sua "affidabilità". Insieme allo yen si muovono GC=F (oro) e CHF=X (franco svizzero) come rifugi alternativi. DX-Y.NYB (dollaro) è ambiguo: in alcuni episodi il dollaro si rafforza come rifugio globale, ma contro lo yen specificamente tende a indebolirsi in un carry unwind.

## 3. Catalogo episodi-ancora datati

Legenda tipo: [BoJ]=decisione BoJ; [FX]=intervento MoF/BoJ sul cambio; [UNWIND]=carry unwind/risk-off; [POLICY]=svolta di policy/framework; [EXT]=shock esterno.

| Data ISO | Evento | Tipo | Direzione attesa | Asset-canale (DB) | Note no-look-ahead |
|---|---|---|---|---|---|
| 1998-10-07 | Squeeze storico dello yen durante l'unwind LTCM: USD/JPY -7% in un giorno (il maggior movimento intraday mai registrato allora); ~-15% in 8 settimane | UNWIND/EXT | JPY forte, risk-off | JPY=X, (^N225 esterno pre-DB) | **Pre-2011: fuori dal DB prezzi, event study NON calcolabile.** Precedente strutturale. Alla data: default russo (agosto) e salvataggio LTCM in corso |
| 1999-02-12 | Introduzione ZIRP (Zero Interest Rate Policy) | POLICY/BoJ | JPY debole | JPY=X | Pre-2011, non calcolabile. Contesto deflazione |
| 2001-03-19 | Avvio Quantitative Easing (QE) | POLICY/BoJ | JPY debole | JPY=X | Pre-2011, non calcolabile |
| 2006-05 | Mini-unwind del carry: yen +5% aprile-maggio, precede la volatilità azionaria (VIX sale dopo) | UNWIND | JPY forte, risk-off | JPY=X | Pre-2011, non calcolabile. Il carry reversal precedette l'equity vol (IMF 2019) |
| 2007-06-22 | Picco di USD/JPY (~124) prima dell'inizio del lungo apprezzamento dello yen | UNWIND/EXT | JPY forte | JPY=X | Pre-2011, non calcolabile. Inizio del grande deleveraging |
| 2008-09-15 | Fallimento Lehman → deleveraging globale; nel 2008 lo yen (NEER) +32,4%, il maggior movimento dal 1971 | UNWIND/EXT | JPY forte, risk-off estremo | JPY=X, (^N225/equity esterni) | Pre-2011, non calcolabile. USD/JPY da ~124 (giu-2007) a ~87 (gen-2009), yen +29% |
| 2013-04-04 | Kuroda lancia il QQE ("bazooka"): base monetaria raddoppiata in ~2 anni, obiettivo inflazione 2% | POLICY/BoJ | JPY debole, ^N225 su | JPY=X, ^N225 | Inizio Abenomics/QQE. Nel DB prezzi (calcolabile) |
| 2016-01-29 | Introduzione NIRP: tasso -0,1% (voto 5-4), a sorpresa (Kuroda aveva negato una settimana prima) | BoJ/POLICY | JPY debole atteso, ma reazione "contraria" | JPY=X, ^N225 | **Sorpresa.** Reazione insolita: yen più forte e azioni giù nei giorni successivi nonostante lo stimolo. TOPIX +3% il giorno stesso, poi inversione |
| 2016-09-21 | Introduzione YCC (QQE with Yield Curve Control): target 10Y JGB ~0%, tasso breve -0,1% | BoJ/POLICY | JPY neutrale/debole | JPY=X, (JGB esterno) | Passaggio da target di quantità a target di prezzo |
| 2018-07-31 | Allargamento banda 10Y a ±0,2% | BoJ | JPY marginale | JPY=X | Aggiustamento minore; volatilità JGB salì |
| 2022-09-22 | Primo intervento MoF di acquisto yen dal 1998: ¥2.838,2 mld | FX | JPY forte (temporaneo) | JPY=X | Effetto di breve durata (studi SCM). USD/JPY ~145 |
| 2022-10-21/24 | Interventi MoF: ¥6.349,9 mld nel periodo (record mensile ottobre ¥6,3 trilioni) | FX | JPY forte | JPY=X | Effetto durato >10 giorni lavorativi (SCM). USD/JPY vicino a 152 |
| 2022-12-20 | Sorpresa: allargamento banda YCC 10Y da ±0,25% a ±0,50% | BoJ/POLICY | JPY forte, ^N225 giù | JPY=X, ^N225, (JGB est.) | **Grande sorpresa.** Nikkei -2,5%, USD/JPY -2,7% a ~133; 10Y JGB a ~0,46% |
| 2023-07-28 | YCC "più flessibile": cap 10Y portato di fatto all'1% (0,5% diventa riferimento) | BoJ/POLICY | JPY volatile | JPY=X, (JGB est.) | Voto 8-1. Aumento outlook inflazione |
| 2023-10-31 | Cap 1% reso "riferimento" (non più tetto rigido): termine effettivo dello YCC | BoJ/POLICY | JPY debole | JPY=X, (JGB est.) | Yen restò debole nonostante l'hawkishness (differenziale ancora ampio) |
| 2024-03-19 | **Uscita da NIRP e YCC**: primo rialzo dal 2007, tasso a 0-0,1%; stop acquisti ETF/J-REIT | BoJ/POLICY | JPY forte atteso, ma "contraria" | JPY=X, ^N225 | **Ben telegrafato.** Reazione contraria: yen sotto 150 (più debole), Nikkei su, per guidance accomodante ("accommodative conditions for the time being") |
| 2024-04-29 | Intervento MoF: ¥5.918,5 mld (acquisto yen) dopo USD/JPY a 160,03 (minimo di 34 anni) | FX | JPY forte | JPY=X | Parte del round aprile-maggio |
| 2024-05-01 | Intervento MoF: ¥3.870,0 mld | FX | JPY forte | JPY=X | Totale round aprile-maggio ¥9.788,5 mld (¥9,79 trilioni, ~$62,25 mld); MoF disclose solo 29/4 e 1/5 |
| 2024-07-11 | Intervento MoF: ¥3.167,8 mld, con USD/JPY che scende da ~161,8 verso 157,3 | FX | JPY forte | JPY=X | Coincidente con CPI USA debole |
| 2024-07-12 | Intervento MoF: ¥2.367,0 mld | FX | JPY forte | JPY=X | Totale luglio ¥5.534,8 mld (¥5,53 trilioni, ~$36,8 mld) |
| 2024-07-31 | Rialzo BoJ a 0,25% (+15 pb) + piano di riduzione acquisti JGB; tono hawkish | BoJ | JPY forte | JPY=X, ^N225 | Innesco prossimale dell'unwind di agosto. A sorpresa nel timing |
| 2024-08-02 | Payroll USA debole: +114k (vs consenso Dow Jones 185k), disoccupazione al 4,3% (massimo da ott-2021) → timori recessione + attese tagli Fed | EXT | risk-off, JPY forte | ^GSPC, ^NDX, JPY=X | Amplificatore esterno. Nikkei -5,81% a 35.909,7 (peggior giorno dal marzo 2020), TOPIX -6,14% |
| 2024-08-05 | **Grande carry unwind**: Nikkei -12,4% (-4.451,28 pt a 31.458,42), maggior calo in punti di sempre; VIX picco pre-market ~65,73, chiusura 38,57; S&P 500 -3,0%, Nasdaq -3,4% a 16.200,08 | UNWIND | risk-off globale violento | ^N225, ^NDX, ^GSPC, ^VIX, JPY=X | **Evento chiave del DB.** Ibrido: BoJ + payroll USA. Yen già +~6% tra 29/7 e 5/8. Calo biennale a due giorni -18,2% (record). TOPIX -12,23% a 2.227,15 |
| 2024-08-06 | Rimbalzo: Nikkei +10,2% (recupera quasi tutte le perdite) | UNWIND (rev.) | risk-on parziale | ^N225, ^VIX | Rimbalzo tecnico |
| 2024-08-07 | Uchida (vice-governatore BoJ): "niente rialzi in periodi di instabilità" → USD/JPY +2% a ~147,8 | BoJ (verbale) | risk-on, JPY debole | JPY=X, ^N225 | Walk-back dovish che spense l'incendio |
| 2025-01-24 | Rialzo BoJ a 0,50% (massimo in 17 anni) | BoJ | JPY forte | JPY=X, ^N225 | Ampiamente atteso |
| 2025-07-31 | BoJ ferma a 0,50%; alza outlook inflazione FY2025 a 2,7% | BoJ | JPY neutrale | JPY=X | Pausa; incertezza dazi USA |
| 2025-12-19 | Rialzo BoJ a 0,75% (massimo dal 1995); 10Y JGB oltre il 2% (massimo dal 1999) | BoJ | JPY forte atteso, reazione muta | JPY=X, (JGB est.) | Ben anticipato; reazione muta, yen leggermente più debole. Prima volta dal 1998 (formato 2 giorni) che BoJ e Fed muovono in direzioni opposte nello stesso mese |

## 4. Statistiche indicative (con forti caveat)
Le ampiezze tipiche di reazione differiscono radicalmente per tipo di episodio:

- **Decisioni BoJ attese/telegrafate** (es. 2024-03-19 uscita NIRP; 2025-01-24; 2025-12-19): reazione di JPY=X spesso modesta (<1-2%) e a volte di segno "contrario" (yen più debole dopo un rialzo, perché la guidance resta accomodante e il differenziale resta ampio). ^N225 può salire. ^VIX poco mosso. N di questa categoria: diversi episodi datati, event study affidabile.
- **Sorprese di policy** (2016-01-29 NIRP; 2022-12-20 banda YCC): movimenti di JPY=X del 2-3% in giornata, ^N225 -2,5%, spostamenti significativi ma ordinati. N piccolo.
- **Carry unwind improvvisi** (2024-08-05): code negative violente e asimmetriche. ^N225 fino a -12,4%, ^VIX da 23,39 a picco pre-market ~65,73 (poi rientro a 38,57 in chiusura — il salto close-to-close di +15,18 punti fu il 7° maggiore di sempre, e per il BIS Bulletin No. 95 "the biggest ever one-day spike, increasing by 180%"), ^GSPC -3,0%, ^NDX -3,4%. JPY=X +5-6% in pochi giorni. **N molto piccolo** (praticamente un solo episodio puro nel DB post-2011: agosto 2024), quindi qualunque "media" è dominata da un singolo evento. La skewness rende media e mediana molto diverse.

Caveat: gli interventi MoF (2022, 2024) mostrano effetti eterogenei — lo studio con Synthetic Control Method (J. of International Money and Finance, 2025) trova che il 22 settembre 2022 ebbe effetto di breve durata, mentre il 21/24 ottobre 2022 durò oltre 10 giorni lavorativi.

## 5. Segmentazione in regime phases

- **ZIRP/deflazione pre-2013 (1998-01-01 → 2012-12-31)**: firma = tassi a zero, deflazione cronica, yen bene rifugio in ogni crisi globale; i grandi unwind (1998, 2008) sono qui ma fuori dal DB prezzi. Segnale: yen forte = risk-off globale, non driver BoJ.
- **Abenomics + QQE (2013-01-01 → 2015-12-31)**: firma = yen strutturalmente debole per lo stimolo massiccio, ^N225 in forte rialzo, relazione inversa yen/Nikkei molto marcata. Reaction function dominata dall'espansione.
- **NIRP+YCC (2016-01-01 → 2022-11-30)**: firma = tassi negativi + 10Y ancorato a ~0%; volatilità JGB soppressa; le sorprese (2016) contano più delle riunioni ordinarie. Carry trade in yen si accumula silenziosamente.
- **Normalizzazione/uscita (2022-12-01 → 2024-03-31)**: firma = allargamenti banda YCC come mini-shock hawkish, yen debolissimo (fino a 160), interventi MoF. Ogni "aggiustamento tecnico" muove i mercati.
- **Post-YCC (2024-04-01 → presente)**: firma = ciclo di rialzi graduali, yen ipersensibile al differenziale Fed-BoJ, rischio di carry unwind latente (agosto 2024). Le decisioni attese hanno reazioni mute; il rischio è nell'unwind improvviso.

Mischiare i regimi distrugge il segnale: una decisione BoJ *attesa* (reazione modesta, spesso contraria) e un carry unwind *improvviso* risk-off (coda negativa violenta) hanno firme opposte. Aggregarli produce medie prive di significato.

## 6. Caveat metodologici
1. **Skewness/asimmetria del carry** (Brunnermeier-Nagel-Pedersen, NBER Macro Annual 2008/2009): il carry genera rendimenti piccoli e positivi a lungo, poi crash violenti ("raccogliere monetine davanti a un rullo compressore"). Media e mediana divergono molto; N piccolo sui crash rende le stime instabili.
2. **Episodi ibridi**: un unwind può essere innescato da fattori esterni (il payroll USA debole del 2 agosto 2024) più che dalla sola BoJ. Difficile attribuire causalità pulita.
3. **Fuso orario Tokyo/NY**: T=0 ambiguo. Il crash del 5 agosto è "lunedì Tokyo" ma la sequenza payroll→VIX→Nikkei attraversa fusi diversi; definire T=0 cambia i risultati T+1/T+3/T+5/T+10.
4. **Interventi FX difficili da datare ex-ante**: il MoF conferma gli importi solo ex-post (totale mensile, poi dettaglio giornaliero trimestrale); alla data-ancora l'intervento è solo "sospetto".
5. **No look-ahead**: per ogni episodio va usato solo ciò che era noto/atteso alla data. Es. il 2024-03-19 era ampiamente telegrafato (quindi già in parte prezzato); il 2016-01-29 fu una sorpresa pura.
6. **Asset esterni al DB**: JGB, TOPIX, indici bancari giapponesi, coppie AUD/JPY e MXN/JPY sono canali reali ma non nel DB; vanno segnalati, non usati come asset-canale calcolabile.

## 7. Riferimenti alla letteratura scientifica
- **Brunnermeier, Nagel, Pedersen (2008/2009)**, "Carry Trades and Currency Crashes", *NBER Macroeconomics Annual* vol. 23, pp. 313-347. Finding: i carry trader sono soggetti a crash risk; i movimenti di cambio tra valute ad alto e basso tasso sono negativamente skewed; lo skew deriva dall'unwind improvviso quando calano risk appetite e funding liquidity. VIX e TED spread predicono i rendimenti del carry.
- **Brunnermeier, Pedersen (2009)**, "Market Liquidity and Funding Liquidity", *Review of Financial Studies*. Finding: liquidity spirals; gli asset in cui gli speculatori sono lunghi hanno rendimento medio positivo e skew negativo (shock di perdita amplificati dai vincoli di funding).
- **Menkhoff, Sarno, Schmeling, Schrimpf (2012)**, "Carry Trades and Global Foreign Exchange Volatility", *Journal of Finance* 67(2), pp. 681-718. Finding: le valute ad alto tasso sono negativamente correlate alle innovazioni di volatilità FX globale (rendimenti bassi quando la volatilità è alta a sorpresa); la volatilità FX globale spiega >90% della variazione cross-sezionale in 5 portafogli di carry.
- **Lustig, Roussanov, Verdelhan (2011)**, "Common Risk Factors in Currency Markets", *Review of Financial Studies* 24(11), pp. 3731-3777. Finding: fattore "slope" (HML) nei cambi; le valute ad alto tasso caricano di più su questo fattore di rischio globale, legato alla volatilità dei mercati azionari globali. Extra-rendimento delle valute a basso tasso ~4,8% annuo inferiore rispetto a quelle ad alto tasso (dopo costi).
- **BIS Bulletin No. 90 (2024)**, Aquilina, Lombardi, Schrimpf, Sushko, "The market turbulence and carry trade unwind of August 2024". Finding: lo spike del VIX (livelli non visti dal Covid) fu amplificato da deleveraging e aumento dei margini; i carry in yen furono i più colpiti; un breve sell-off con segni di unwind era già avvenuto il 24 luglio; stima "middle ballpark" del carry ~¥40 trilioni ($250 mld).
- **BIS Bulletin No. 95 (2024)**, Todorov & Vilkov. Finding: il 5 agosto 2024 il VIX registrò "the biggest ever one-day spike, increasing by 180% to almost 66 pre-market".
- **Federal Reserve IFDP 899 (2007)**, "What Can the Data Tell Us about Carry Trades in Japanese Yen?". Finding: difficoltà a misurare direttamente il carry; l'unwind di ottobre 1998 fu il più drammatico episodio documentato.
- **IMF WP/18/131 (2018)**, "Pushed Past the Limit? How Japanese Banks Reacted to Negative Interest Rates". Finding: l'annuncio NIRP fu una sorpresa che colpì i titoli bancari giapponesi.
- **IMF, "Yen Carry Trade and the Subprime Crisis"** (IMF Staff Papers 2009). Finding: l'unwind del carry attraverso i bilanci interconnessi degli intermediari amplificò gli spillover della crisi 2007-08.

## 8. Raccomandazioni operative (per il pipeline event-study)
1. **Segmenta sempre per tipo di evento prima di aggregare.** Non calcolare mai una "reazione media BoJ": separa `decisione_attesa`, `sorpresa_policy`, `carry_unwind`, `intervento_FX`. Le firme sono opposte e mescolarle azzera il segnale.
2. **Tratta il 5 agosto 2024 come caso-studio singolo, non come punto di una distribuzione.** Con N≈1 per gli unwind puri post-2011, riporta l'evento in forma narrativa (T+1/T+3/T+5/T+10 su ^N225, ^NDX, ^GSPC, ^VIX, JPY=X) senza pretese statistiche. Aggiungi il 2 e il 6-7 agosto come finestra.
3. **Usa JPY=X come variabile-trigger, non solo come outcome.** Come suggerito dagli analisti FX, un apprezzamento rapido dello yen (es. USD/JPY che rompe sotto 150) è un leading indicator della volatilità azionaria USA, spesso più affidabile del VIX (che reagisce ex-post). Costruisci un flag "yen shock" (variazione JPY=X > soglia in n giorni) da incrociare con gli eventi discreti.
4. **Datazione degli interventi MoF: usa la data di esecuzione presunta, non quella di conferma.** Marca gli interventi come "sospetti a T=0, confermati a T+dettaglio". Per il pipeline, le date-ancora affidabili sono 2022-09-22, 2024-04-29, 2024-05-01, 2024-07-11, 2024-07-12.
5. **Gestisci il fuso Tokyo/NY esplicitamente.** Definisci T=0 in modo coerente (chiusura Tokyo vs chiusura NY) e testa la robustezza spostando T=0 di un giorno.
6. **Escludi gli episodi pre-2011 dal calcolo** (LTCM 1998, deleveraging 2008): usali solo come contesto qualitativo per la calibrazione delle code.

**Soglie/benchmark che cambierebbero queste raccomandazioni:** se il DB prezzi venisse esteso indietro al 1998 (includendo ^N225 e JPY=X storici), gli unwind 1998/2008 diventerebbero calcolabili e N degli eventi-crash salirebbe a 3-4, giustificando statistiche di coda più formali. Se emergesse un secondo carry unwind post-2024 (rischio segnalato dalla ricostruzione delle posizioni short-yen nel 2025-2026), aggiornare la categoria `carry_unwind` e ricalcolare. Se il differenziale Fed-BoJ si comprimesse sotto ~200 pb, la probabilità e l'ampiezza di un unwind cambierebbero materialmente.

## 9. Caveat generali su fonti e affidabilità
- Le cifre di mercato del 5 agosto 2024 (Nikkei -12,4%/-4.451,28 pt, VIX picco ~65,73, chiusura 38,57, S&P -3,0%, Nasdaq -3,4%) sono da fonti primarie/di alta qualità (MoF, CBOE/BIS, Reuters, CNBC, Washington Post). Nota: alcune fonti riportano cali intraday all'apertura più severi (S&P -4,2%, Nasdaq -6,3% per il live blog CNBC); qui si usano i valori di **chiusura**.
- Le stime della dimensione del carry ($250 mld – $20 trilioni) sono strutturalmente imprecise perché aggregano FX swap, forward, acquisti di bond esteri e leva azionaria; vanno trattate come ordini di grandezza, non come dati.
- Molte fonti di commento (blog, siti di trading) sono state usate solo per corroborare date già presenti in fonti primarie; le affermazioni prospettiche ("il prossimo unwind", target USD/JPY) sono opinioni/speculazioni e non fatti datati.

```yaml
title: "Giappone / Bank of Japan: carry trade, uscita YCC e interventi FX — regime ed episodi storici (1998–2026)"
date_compiled: 2026-07-19
primary_theme: monetary_policy
sub_themes: [boj, yen, jpy, carry_trade, carry_unwind, ycc, nirp, fx_intervention, risk_off, safe_haven, japan]
relevant_assets: [JPY=X, ^N225, ^NDX, ^GSPC, ^VIX, ^TNX, IEF, GC=F, CHF=X, DX-Y.NYB]
external_assets_mentioned: JGB (titoli di stato giapponesi 10Y) — non in DB; TOPIX / indici bancari giapponesi — non in DB; coppie di carry AUD/JPY, MXN/JPY — non in DB
time_window: start 1998-01-01, end present
regime_phases: zirp_deflation_pre_2013 (1998-01-01 to 2012-12-31); abenomics_qqe_2013_2015 (2013-01-01 to 2015-12-31); nirp_ycc_2016_2022 (2016-01-01 to 2022-11-30); normalization_exit_2022_2024 (2022-12-01 to 2024-03-31); post_ycc_2024_2026 (2024-04-01 to present)
keywords: [giappone, japan, bank of japan, boj, yen, jpy, usd/jpy, carry trade, carry unwind, ycc, yield curve control, nirp, negative rates, fx intervention, mof, ministry of finance, abenomics, qqe, nikkei, risk-off, safe haven, august 2024, deleveraging, crash risk]
```