# La gestione del cambio da parte della People's Bank of China: fixing, strumenti, regimi ed episodi datati (2005–2026)

## §1 Sintesi esecutiva

In un cambio amministrato quotidianamente come quello cinese, il segnale di un episodio di policy della PBoC **non è quasi mai osservabile su USD/CNY stesso** — che per costruzione è vincolato a una banda del ±2% attorno al fixing — ma si sposta sugli asset satellite (valute asiatiche libere, azionario EM, rame) e sulle misure di pressione (differenziale onshore-offshore CNY−CNH, punti a termine). Questa è la tesi operativa dello studio, che alimenta una pipeline di event study e deve impedire due errori sistematici: (a) trattare il renminbi come lo yen (float libero difeso con interventi rari) e (b) applicare gli analoghi di difesa dal deprezzamento alla configurazione oggi in essere, che è invece di **freno all'apprezzamento**. I punti centrali:

1. **Il segnale è negli asset satellite, non nel CNY.** Nelle giornate di "segnale" più forti dell'ultimo anno lo spot onshore ha reagito di appena 0,1–0,4%, perché la banda comprime il movimento. L'informazione osservabile è altrove: (a) valute asiatiche libere (KRW, MYR, THB, IDR, TWD), con beta storici verso il renminbi spesso superiori a 0,7; (b) azionario EM (EEM, EWY, EWT) e satelliti di materie prime (HG=F, REMX, LIT); (c) le misure di pressione — differenziale CNY−CNH e punti a termine — che catturano quanto il mercato spinga contro il fixing. La tesi è corroborata dal fatto che le tre uniche svalutazioni cinesi che hanno prodotto un vero risk-off globale (2015-08-11, 2016-01-07, 2019-08-05) sono anche le uniche in cui il CNH si è staccato nettamente dal CNY.

2. **L'asimmetria freno-alla-caduta / freno-alla-salita è il contributo principale.** Quando la PBoC frena il deprezzamento consuma riserve e vende dollari tramite le banche di Stato: si propaga scarsità di dollari, stress di funding e pressione su tutte le valute EM. Quando frena l'apprezzamento (2010–2014, 2020–2021, 2025–2026) accumula riserve o rende costoso comprare dollari a termine: ciò che si propaga è pressione competitiva sui partner asiatici e un tono reflazionistico sulle materie prime, se accompagnato da stimolo. I due casi hanno **segno opposto** sugli stessi asset satellite e non vanno mai mescolati.

3. **Lo strumentario extra-fixing è spesso più informativo del fixing.** La riserva obbligatoria sui depositi in valuta (FX deposit RRR), la riserva di rischio del 20% sui forward, il fattore controciclico, i titoli PBoC a Hong Kong e le finestre di orientamento hanno ciascuno una data certa e un segno inequivocabile: un rialzo della riserva di rischio sui forward è difesa dal deprezzamento; il suo azzeramento è freno all'apprezzamento.

4. **Dove l'event study è affidabile:** riforme di regime e svalutazioni disordinate con reazione cross-asset ampia; strumenti amministrativi con data certa; canale dei vicini asiatici. **Dove non lo è:** il canale del fixing quotidiano isolato (rumore alto, soglia di significatività incerta); tutto ciò che è contaminato dai dazi 2018–2019 e 2025–2026, dove componente-cambio e componente-guerra-commerciale sono inseparabili senza un asset di controllo; ogni episodio anteriore al 2010 (conto capitale, assenza del CNH e microstruttura non confrontabili).

5. **Configurazione corrente (agosto 2026): freno all'apprezzamento.** Da novembre 2025 la PBoC fissa il riferimento sistematicamente più debole del consenso; il 20 agosto 2026 il gap ha toccato 598 pip (fix a 6,7808 contro un consenso Bloomberg superiore), il più ampio da febbraio 2026. Gli analoghi utili sono **2020–2021 e 2010–2015**, non la difesa 2022–2024.

## §2 Tassonomia dei canali di trasmissione

**Canale del segnale di fixing (direzionale / amplificatore).** `Fixing pubblicato alle 9:15 di Pechino con scarto anomalo rispetto al consenso Reuters/Bloomberg → il mercato lo legge come decisione di policy, non come errore → riprezzamento delle attese sul cambio → reazione su CNH, punti a termine e valute-proxy`. Le stime di consenso rappresentano il "model-implied fix" (chiusura del giorno precedente più movimenti overnight del paniere); lo scarto è la deviazione del fix effettivo da tale stima, in pip. In condizioni normali è di poche decine di pip. Diventa segnale quando supera circa 150–200 pip; gli episodi descritti come "forte pushback" nei rapporti recenti stanno tra 322 e 598 pip (2026) e arrivano fino a 1.323 pip nella difesa (2 gennaio 2025, il gap più ampio dal luglio precedente secondo Bloomberg). Come regola di calibrazione, uno scarto oltre ~2 deviazioni standard della sua distribuzione recente qualifica il segnale; **due sedute consecutive** nella stessa direzione distinguono una posizione di policy da un aggiustamento isolato — criterio corroborato dal fatto che ING e Maybank descrivono la "fixing bias" come un pattern che dura settimane, non giorni (dalla difesa continua da novembre 2024 al freno persistente da novembre 2025). Risposta alla domanda operativa che ha generato la richiesta: **sì, due sedute consecutive sono il criterio corretto per il pool "posizione"**; una singola seduta va trattata come rumore, salvo scarto estremo (oltre ~500 pip). Asset-proxy: CNY=X (poco informativo), CNH e punti a termine (informativi).

**Canale della trasmissione ai vicini (redistributivo).** `Yuan più debole, o freno alla salita → variazione di competitività dei partner asiatici che esportano beni sostituti → KRW, MYR, THB, IDR, TWD si muovono nella stessa direzione, spesso amplificata`. È il canale osservabile per eccellenza perché queste valute sono libere mentre lo yuan è gestito. I beta storici del co-movimento (β1 di ciascuna valuta verso il CNY, metodologia Frankel-Wei, BIS Working Paper No. 727, McCauley & Shu, giugno 2018) mostrano un salto netto dopo la riforma dell'11 agosto 2015: won coreano da 0,53 a 1,26, ringgit malese da 0,49 a 1,02, dollaro di Taiwan da 0,37 a 0,72, rupia indonesiana da 0,67 a 0,73; il pannello asiatico aggregato passa da 0,42 a 0,77 e quello non asiatico da un valore non significativo a 0,97. Won e ringgit hanno il beta più alto e sono le proxy migliori; nella fase di gestione controciclica (post-2017) solo won (0,83) e dollaro di Taiwan (0,54) restano sopra 0,5, configurando una "zona renminbi" nordasiatica. **SGD e THB non sono nel campione di regressione BIS** (compaiono solo come pesi del paniere CFETS, rispettivamente ~3,0% e ~3,4% dal 2025) e vanno usati con cautela. Asset-proxy: KRW=X, MYR=X, THB=X, IDR=X, EWY, EWT, EWS, THD, EIDO.

**Canale materie prime (direzionale, ambiguo).** `Cambio più stimolo cinese → attese sulla domanda industriale → rame (HG=F), terre rare (REMX), litio (LIT)`. Distinzione critica: quando il movimento del cambio è **accompagnato** da stimolo fiscale o creditizio (es. 24 settembre 2024, pacchetto stimato ~7,5 trilioni RMB) il segnale è di domanda in salita e il rame può salire nonostante lo yuan debole; quando il movimento è **isolato** — una svalutazione difensiva senza stimolo, come agosto 2015 — il rame scende insieme allo yuan. Sono due segni opposti sullo stesso asset ed è la principale fonte di rumore in questo canale: la variabile di controllo da affiancare è la presenza o assenza di un annuncio di stimolo con importo nella stessa finestra temporale.

**Canale del rischio globale (amplificatore).** `Svalutazione cinese percepita come disordinata o non comunicata → timore di currency war e di implosione della crescita cinese → risk-off mondiale (EEM giù, ^VIX su, GC=F su, ^GSPC giù)`. Cosa distingueva agosto 2015, gennaio 2016 e agosto 2019 dalle centinaia di variazioni del cambio senza reazione globale: in tutti e tre i casi (a) c'era una rottura di regime o di soglia psicologica (l'"811", il crollo del CNH di inizio 2016, la rottura di 7,00 per la prima volta dal 2008), (b) la comunicazione PBoC fu percepita come opaca o ostile, (c) il CNH si staccò nettamente dal CNY segnalando fuga di capitali. In assenza di questi tre marcatori, una variazione del fixing **non** appartiene al pool "risk-off globale". Confondere i due pool sovrastima sistematicamente l'impatto: è precisamente l'errore da evitare.

**Canale dello strumentario (direzionale, ad alto contenuto informativo).** Il cambio non è l'unico strumento. Ognuno ha una data e un segno netto: (i) **FX deposit RRR** — rialzo = freno all'apprezzamento, taglio = difesa dal deprezzamento; (ii) **riserva di rischio del 20% sui forward** — imposizione = difesa, azzeramento = freno alla salita; (iii) **fattore controciclico** nel fixing — introdotto o rafforzato per contrastare l'attesa dominante; (iv) **titoli PBoC in yuan a Hong Kong** — drenano liquidità CNH offshore, storicamente per difendere ma da fine 2025 anche per limitare la salita; (v) **finestre di orientamento** alle banche di Stato (non dichiarate). Questi strumenti sono più netti del fixing perché il loro segno è inequivocabile.

Classificazione sintetica: canali **direzionali** = fixing, strumentario e (parzialmente) materie prime; canale **redistributivo** = trasmissione ai vicini; **amplificatori** = rischio globale e la componente-segnale del fixing nelle rotture di regime.

## §3 Catalogo di episodi-ancora datati

Formato date: `YYYY-MM-DD` = seduta di mercato in cui l'asset-proxy reagisce. Il fixing esce alle 9:15 di Pechino (prima dell'apertura europea, ~15 ore prima di New York): una valuta asiatica reagisce immediatamente; un ETF USA su sottostante asiatico (EEM, EWY) reagisce lo stesso giorno di calendario, ma alla sua apertura. Annunci in festivi cinesi (Capodanno lunare, Settimana d'oro di ottobre) o nel weekend → prima seduta utile, spiegato nelle Note.

| Data (ISO) | Evento | Tipo | Direzione attesa | Asset-canale | Note no-look-ahead |
|---|---|---|---|---|---|
| 2005-07-21 | Rivalutazione 2,1% (8,2765→8,11) e passaggio a managed float con paniere | riforma_regime | CNY forte | CNY=X, KRW=X, EEM | Annuncio serale 21 lug; reazione piena il 22. Regime pre-2010: non confrontabile col corrente. |
| 2007-05-21 | Banda allargata da ±0,3% a ±0,5% | riforma_regime | CNY forte | CNY=X | Fase di apprezzamento amministrato. |
| 2010-06-21 | Uscita dal peg di crisi, ripresa della flessibilità | riforma_regime | CNY forte | CNY=X, KRW=X, HG=F, EEM | Annuncio sabato 19 giu; prima seduta utile lun 21 giu. |
| 2012-04-16 | Banda allargata da ±0,5% a ±1% | riforma_regime | CNY forte (due vie) | CNY=X | Contesto di freno all'apprezzamento: la banda serve a gestire la salita. |
| 2014-03-17 | Banda allargata da ±1% a ±2% | riforma_regime | CNY debole (due vie) | CNY=X, KRW=X | Annuncio sab 15 mar; effettiva e reazione lun 17 mar. Contesto: freno all'apprezzamento 2010-14. |
| 2015-08-11 | Riforma "811": taglio del fix di 1,9% (da 6,1162 a 6,2298, −1.136 pip), nuovo meccanismo | svalutazione_disordinata | CNY debole | CNY=X, CNH, KRW=X, EEM, HG=F, ^VIX | Il più grande calo giornaliero del fix dal 1994. Innesco di risk-off globale; CNH si stacca dal CNY. |
| 2015-08-12 | Secondo taglio consecutivo del fix (cumulato ~4,4% in 3 sedute) | svalutazione_disordinata | CNY debole | CNH, EEM, ^GSPC, ^VIX, HG=F | Seconda seduta consecutiva → conferma posizione, non caso isolato. |
| 2015-10-15 | Introduzione riserva di rischio 20% sui forward (prima volta) | strumento_amministrativo | difesa (CNY forte) | CNH, punti a termine | Difesa dal deprezzamento post-811. |
| 2015-12-11 | Pubblicazione indice paniere CFETS RMB (13 valute; USD 26,40%, EUR 21,39%, JPY 14,68%) | riforma_regime | CNY debole vs paniere | CNY=X, indice CFETS | Sposta il focus dal solo USD al paniere; consente deprezzamento vs USD "stabile vs paniere". |
| 2016-01-07 | Crollo yuan/CNH inizio 2016, fix più debole, risk-off globale | svalutazione_disordinata | CNY debole | CNH, EEM, ^GSPC, ^VIX, HG=F | La seduta del 7 gen è quella del massimo stress; CNH ai minimi, ~−8,5% azionario in pochi giorni. |
| 2017-05-26 | Introduzione del fattore controciclico nel fixing | strumento_amministrativo | difesa (CNY forte) | CNY=X, CNH | Annuncio ven 26 mag (confermato nel Rapporto di Policy Q2 2017); frena il deprezzamento. |
| 2018-08-06 | Riserva di rischio 20% sui forward re-imposta (da 0%) | strumento_amministrativo | difesa (CNY forte) | CNH, punti a termine | Annuncio ven 3 ago sera; effettiva e reazione lun 6 ago. Contaminato dai dazi. |
| 2018-08-24 | Fattore controciclico reintrodotto nel fixing | strumento_amministrativo | difesa (CNY forte) | CNY=X, CNH | Statement CFETS ven 24 ago; Reuters stesso giorno. Ripristino dopo la sospensione di gennaio 2018. |
| 2018-11-07 | Prima emissione di titoli PBoC in yuan a Hong Kong (20 mld RMB: 10 a 3 mesi + 10 a 1 anno) | strumento_amministrativo | difesa (CNY forte) | CNH, punti a termine | Annuncio 31 ott; emissione 7 nov. Drena liquidità CNH offshore. |
| 2019-08-05 | Rottura di 7,00 per la prima volta dal 2008 (fix a 6,9225); designazione USA "manipolatore" | svalutazione_disordinata | CNY debole | CNY=X, CNH, EEM, ^GSPC (Dow −767 pt, −2,9%), ^VIX, HG=F | Contaminato dai dazi. Innesco di risk-off. Fix la mattina di Pechino; Dow reagisce stessa data USA. |
| 2019-06-25 | Fix più forte del consenso (record dallo storico agosto 2017) + annuncio bond a HK | strumento_amministrativo | difesa (CNY forte) | CNY=X, CNH | **Data da verificare:** ricostruita da un'unica fonte (gulfnews, "martedì" di giugno 2019); usare con cautela. |
| 2020-10-12 | Azzeramento riserva di rischio forward (da 20% a 0%) | strumento_amministrativo | freno all'apprezzamento | CNH, KRW=X, EEM | Annuncio 10 ott (sabato); prima seduta utile lun 12 ott. Yuan al massimo da 2 anni. |
| 2021-05-31 | Primo rialzo FX deposit RRR in 14 anni (5%→7%) | strumento_amministrativo | freno all'apprezzamento | CNH, KRW=X, MYR=X, EEM | Annuncio lun 31 mag; effettivo 15 giu. Prima revisione dal maggio 2007 (allora 4%→5%). |
| 2021-12-09 | Secondo rialzo FX deposit RRR 2021 (7%→9%) | strumento_amministrativo | freno all'apprezzamento | CNH, KRW=X, EEM | Annuncio giovedì sera 9 dic; effettivo 15 dic. CNH ai minimi del mese sull'annuncio. |
| 2022-09-05 | Taglio FX deposit RRR (8%→6%) per frenare il deprezzamento | strumento_amministrativo | difesa (CNY forte) | CNH, KRW=X, EEM | Effettivo 15 set. Yuan a 6,94; "segnale forte di difesa" (Pinpoint). |
| 2022-09-26 | Riserva di rischio forward rialzata (0%→20%) | strumento_amministrativo | difesa (CNY forte) | CNH, punti a termine | Annuncio lun 26 set; effettivo 28 set. Yuan verso 7,2. CNH rimbalza ~300 pip. |
| 2025-01-02 | Fix 1.323 pip più forte del consenso (gap max da luglio) | fixing_anomalo_forte | difesa (CNY forte) | CNY=X, CNH | Difesa contro il tumble di fine 2024. Contaminato dalle attese dazi Trump. |
| 2025-01-15 | Emissione record di titoli PBoC a HK (60 mld RMB, 6 mesi) | strumento_amministrativo | difesa (CNY forte) | CNH, punti a termine | Annuncio ~9 gen; emissione 15 gen. Più grande emissione singola offshore e prima a gennaio. |
| 2025-04-08 | Fix oltre 7,20 per la prima volta dal 2023 (7,2038) durante shock dazi; CNH a minimo record 7,4287 | fixing_anomalo_debole | CNY debole (controllata) | CNY=X, CNH, EEM, KRW=X, ^VIX | Contaminato dai dazi (145%). Fix comunque molto più forte del consenso 7,3321 → difesa camuffata. |
| 2024-09-24 | Pacchetto di stimolo monetario/creditizio (taglio RRR 0,5pp ≈ 1 trilione RMB; 2×800 mld facility azionarie; pacchetto totale stimato ~7,5 trilioni RMB da Deutsche Bank) | stimolo_fiscale_o_creditizio | reflazione (HG=F su) | HG=F, REMX, LIT, EEM, ^GSPC | Conferenza stampa PBoC/regolatori 24 set; Politburo 26 set. |
| 2024-11-08 | Swap del debito degli enti locali: +6 trilioni RMB al tetto, totale 10 trilioni RMB (~1,4 trln USD) fino al 2028 | stimolo_fiscale_o_creditizio | reflazione | HG=F, EEM, LIT | Approvato dal Comitato Permanente NPC l'8 nov (Min. Finanze Lan Fo'an). |
| 2024-12-09 | Politburo: svolta a politica monetaria "moderatamente accomodante" (prima dal 2010) | stimolo_fiscale_o_creditizio | reflazione | EEM, ^GSPC, HG=F | Cambio di stance verbale, senza importo puntuale; Hang Seng +2,8%. |
| 2008-11-09 | Pacchetto di stimolo post-crisi (4 trilioni RMB) | stimolo_fiscale_o_creditizio | reflazione | HG=F, EEM | Regime pre-2010: usare come analogo con cautela. |
| 2026-02-27 | Azzeramento riserva di rischio forward (20%→0%) per frenare l'apprezzamento | strumento_amministrativo | freno all'apprezzamento | CNH, KRW=X, MYR=X, EEM | Annuncio ven 27 feb; effettivo 2 mar. Yuan al massimo da ~3 anni; fix contestuale più debole del consenso. CNH crolla >1% sotto 6,85 (annuncio precedente del 2015, stesso strumento). |
| 2026-08-20 | Fix 598 pip più debole del consenso (fix 6,7808 vs previsione superiore; gap max da febbraio) | fixing_anomalo_debole | freno all'apprezzamento | CNY=X, CNH, KRW=X | Configurazione corrente. Da nov 2025 pattern persistente di fix debole. |

**Non-episodi (scritti deliberatamente in forma non-ISO, per evitare che diventino ancore):** l'ancoraggio rigido "fino al luglio 2005"; il "riancoraggio di crisi 2008–metà 2010" (~6,83); l'"apprezzamento graduale 2011–2013" verso ~6,05; l'"estate 2015" come minimo/inizio di fase; la "difesa prolungata 2023–2024"; l'"inizio 2022" come riferimento generico.

**Verifica della distribuzione minima richiesta:** freno all'apprezzamento = 2020-10-12, 2021-05-31, 2021-12-09, 2026-02-27, 2026-08-20 (+ contesto 2012-04-16, 2014-03-17) → ≥ 8 con le fasi-contesto; difesa dal deprezzamento = 2015-10-15, 2017-05-26, 2018-08-06, 2018-08-24, 2018-11-07, 2019-06-25, 2022-09-05, 2022-09-26, 2025-01-02, 2025-01-15, 2025-04-08 → 11 (≥ 10); riforma del regime = 2005-07-21, 2007-05-21, 2010-06-21, 2012-04-16, 2014-03-17, 2015-08-11, 2015-12-11 → 7 (≥ 5); stimolo con importo = 2008-11-09 (4 trln), 2024-09-24 (~7,5 trln), 2024-11-08 (10 trln), 2024-12-09 (svolta di stance) → ≥ 5 con la svolta di stance conteggiata come annuncio creditizio.

## §4 Statistiche indicative

Il database interno contiene i prezzi degli asset-proxy elencati ma **non** il differenziale CNY−CNH né il fixing implicito di consenso; le statistiche seguenti sono direzionali/qualitative, non rendimenti cumulati calcolati (il calcolo T+1/T+3/T+5/T+10 spetta alla pipeline). Sono raggruppate per Tipo e per configurazione, con N sempre indicato; sono marcate "INDICATIVE ONLY" tutte quelle con N < 10.

**Svalutazione disordinata (N = 4: 2015-08-11, 2015-08-12, 2016-01-07, 2019-08-05) — INDICATIVE ONLY.** Configurazione: rottura difensiva. Pattern storico: EEM negativo e ^VIX positivo su T+1..T+5; HG=F negativo; KRW e MYR si deprezzano più del CNY (beta > 1 nel post-2015); CNH−CNY si allarga (CNH più debole). È il pool con la reazione cross-asset più ampia e affidabile, ma va tenuto rigorosamente separato dai semplici fix deboli: mescolarlo sovrastima l'impatto.

**Strumento amministrativo — difesa dal deprezzamento (N = 7: 2015-10-15, 2017-05-26, 2018-08-06, 2018-08-24, 2018-11-07, 2022-09-05, 2022-09-26) — INDICATIVE ONLY.** Pattern: CNH si rafforza sull'annuncio (es. ~300 pip il 2022-09-26); punti a termine si comprimono; effetto su EEM/azionario modesto e spesso oscurato dalla componente-dazi negli episodi 2018.

**Strumento amministrativo — freno all'apprezzamento (N = 4: 2020-10-12, 2021-05-31, 2021-12-09, 2026-02-27) — INDICATIVE ONLY.** Pattern speculare: CNH si indebolisce sull'annuncio (es. crollo > 1% sotto 6,85 il 2026-02-27, secondo Reuters/Yicai); KRW e MYR tendono a seguire per pressione competitiva; nessun risk-off — anzi, contesto di inflow su EEM. È la configurazione oggi scoperta e il segno sugli asset satellite è **opposto** a quello della difesa.

**Fixing anomalo (forte: N = 1, 2025-01-02; debole: N = 2, 2025-04-08, 2026-08-20) — INDICATIVE ONLY.** Il fix forte isolato ha effetto minimo e rapidamente riassorbito su CNY=X; il segnale, se c'è, è su CNH e punti a termine. Il fix debole isolato in configurazione di freno alla salita produce un movimento di pochi decimi di punto sullo spot.

**Stimolo fiscale/creditizio con importo (N = 4: 2008-11-09, 2024-09-24, 2024-11-08, 2024-12-09) — INDICATIVE ONLY.** Pattern: quando lo stimolo è ampio e a sorpresa, HG=F, REMX, LIT ed EEM salgono su T+1..T+10 anche se lo yuan è debole; è il caso che rovescia il segno del canale materie prime rispetto alla svalutazione isolata.

**Riforma del regime (N = 7).** Reazione eterogenea: le riforme "verso più mercato" in fase di apprezzamento (2005, 2007, 2010) hanno sostenuto CNY e valute EM; l'811 (2015) appartiene invece al pool svalutazione disordinata. Non trattare gli allargamenti di banda (2007, 2012, 2014) come segnali direzionali: sono aggiustamenti di microstruttura.

**Differenziale CNY−CNH (serie non nel database).** Storicamente: in difesa dal deprezzamento il CNH quota più debole del CNY (USD/CNH > USD/CNY), con picchi come l'8 aprile 2025 (USD/CNH a 7,4287, ~8 cent sopra il CNY, il gap più ampio da oltre un decennio) e inizio 2016; in freno all'apprezzamento il segno si può invertire (CNH più forte del CNY, osservato in più sedute del 2025). È la misura diretta della pressione di mercato contro il fixing: la sua documentazione storica indica che **vale la pena procurarsi la serie**, perché è il singolo indicatore più informativo dell'intero apparato e non è sostituibile dagli asset quotati. Come contesto quantitativo del "war chest" che sostiene la credibilità della difesa: le riserve valutarie cinesi sono scese da un picco di 3.993,2 mld USD (giugno 2014) a 3.330,4 mld USD (dicembre 2015), fino a sotto i 3.000 mld a gennaio 2017 (dati SAFE), per poi stabilizzarsi intorno ai 3.200 mld negli anni recenti.

## §5 Fasi di regime

Nomi in snake_case. Per ogni fase, la frase operativa: se gli analoghi siano usabili nel regime corrente e perché.

- **hard_peg** (fino a 2005-07-21). Peg fisso a 8,2765/USD. **Non usabili:** conto capitale chiuso, nessuna microstruttura di fixing/banda, nessun CNH.
- **administered_appreciation** (2005-07-21 → 2008-12-31). Apprezzamento amministrato di oltre il 17%, banda ±0,3%→±0,5%. **Parzialmente usabili** solo come analogo di freno all'apprezzamento, ma con forte cautela: conto capitale molto più chiuso, CNH inesistente.
- **crisis_reanchoring** (2008-12-31 → 2010-06-21). Riancoraggio al dollaro ~6,83. **Non usabili** come segnali direzionali; utili solo come precedente di "peg di crisi difensivo".
- **gradual_appreciation_widening_band** (2010-06-21 → 2015-08-11). Apprezzamento graduale, banda a ±1% (2012) e ±2% (2014). **Usabili** come miglior analogo storico dell'attuale freno all'apprezzamento, tenendo conto che il CNH nasce solo nel 2010 e matura durante la fase.
- **eight_eleven_reform_disorderly_defense** (2015-08-11 → 2017-05-26). L'811, la difesa disordinata, il crollo delle riserve da ~3.993 a ~3.330 mld USD (poi sotto 3.000 nel 2017), l'introduzione del paniere CFETS. **Usabili con attenzione:** ottimo per il pool svalutazione disordinata/risk-off, ma la microstruttura del fixing è cambiata dopo il 2017.
- **countercyclical_factor_basket_management** (2017-05-26 → 2019-05-01). Fattore controciclico e gestione del paniere. **Molto usabili:** stesso strumentario tuttora in uso.
- **tariffs_and_seven_threshold** (2019-05-01 → 2019-12-31). Dazi, rottura di 7,00 il 2019-08-05, designazione "manipolatore". **Usabili** ma **contaminati dai dazi**: richiedono un asset di controllo per separare cambio da guerra commerciale.
- **covid_appreciation** (2020-01-01 → 2021-12-31). Apprezzamento post-COVID verso ~6,3; strumenti di freno alla salita (azzeramento riserva forward ottobre 2020, rialzi FX RRR 2021). **Il miglior analogo del regime corrente** insieme a gradual_appreciation_widening_band.
- **depreciation_defense** (2022-01-01 → 2024-12-31). Difesa da deprezzamento con fix forte, tagli FX RRR, riserva forward al 20%, vendite via banche di Stato. **Usabili per la difesa**, ma **da NON applicare alla configurazione corrente** di freno alla salita: segno opposto sugli asset satellite.
- **current_appreciation_management** (2025-01-01 → present). Freno all'apprezzamento: fix più debole del consenso da novembre 2025, azzeramento riserva forward il 2026-02-27, emissioni CNH per gestire la liquidità offshore. Contaminazione con i dazi 2025. Analoghi: covid_appreciation e gradual_appreciation_widening_band.

## §6 Caveat metodologici

**Non osservabilità della funzione di reazione.** Le stime di consenso sul fixing sono di banche private (Reuters, Bloomberg) con metodologie diverse e soggette a revisione. "555 pip più debole delle stime" (14 agosto 2026, stima Reuters 6,7262 contro fix 6,7817) dipende da quali stime: lo stesso giorno Bloomberg poteva riportare un gap diverso, e il 20 agosto 2026 Bloomberg indicava 598 pip. Lo scarto va sempre ancorato alla fonte specifica e la sua distribuzione storica va ricalcolata per il fornitore usato.

**Opacità degli interventi.** Le riserve valutarie SAFE sono mensili e non distinguono l'effetto-valutazione dal flusso. Gli interventi passano per le banche di Stato e non sono dichiarati; il fattore controciclico non ha formula pubblica. Non esiste una serie ufficiale di "intervento giornaliero" cinese confrontabile con i dati del Ministero delle Finanze/BoJ giapponesi.

**Contaminazione con i dazi.** Molti episodi 2018-2019 e 2025-2026 sono simultaneamente episodi di guerra commerciale (2019-08-05, 2025-04-08). Per separare la componente-cambio dalla componente-dazi: usare come controllo un asset esposto ai dazi ma non direttamente al cambio cinese (un paniere di esportatori USA, oppure il differenziale tra EWY/EWT — esposte alla supply chain — e un indice EM non asiatico), o confrontare la reazione del CNH con quella dell'S&P 500: se ^GSPC reagisce quanto EEM, la componente dominante è il rischio commerciale, non il cambio.

**Perché NON trasferire gli analoghi giapponesi (una riga per motivo).** (1) Il Giappone difende un float libero con interventi rari e discreti; la Cina amministra un fix quotidiano con banda. (2) La variabile-segnale giapponese è l'intervento dichiarato ex post dal MoF; quella cinese è lo scarto del fix, mai dichiarato. (3) Lo yen è valuta rifugio (sale nel risk-off); lo yuan è valuta EM (scende nel risk-off). (4) Lo yen è pienamente convertibile; lo yuan ha conto capitale controllato e mercato onshore/offshore segmentato. (5) Lo spillover giapponese passa per il carry trade globale; quello cinese per la competitività dei vicini asiatici.

**Episodi anteriori al 2010.** Cadono in un regime di conto capitale e apertura non confrontabili: il CNH non esisteva prima del 2010, la banda era ±0,3-0,5% e la composizione degli asset-proxy EM era diversa. Usarli solo come contesto, mai come analoghi diretti per la pipeline.

**Serie citate ma non disponibili nel database:** differenziale CNY−CNH (la misura più informativa); indice paniere CFETS RMB (per distinguere debolezza-vs-USD da debolezza-vs-paniere); punti a termine USD/CNY e USD/CNH; fixing implicito di consenso Reuters/Bloomberg; riserve SAFE mensili; CNH HIBOR (funding offshore). La loro assenza è la principale limitazione: senza CNY−CNH e CFETS il segnale-fix è quasi non osservabile.

**Incertezze residue sulle date.** La data 2019-06-25 (fix forte record e annuncio bond) è ricostruita da un'unica fonte (gulfnews) e va verificata su una seconda. Dove l'annuncio cade di sabato (2005-07-21, 2010-06-19, 2020-10-10) la seduta di reazione è la prima utile e la data va disambiguata tra annuncio ed effetto. Per gli strumenti amministrativi, annuncio ed effettiva applicazione differiscono spesso di alcuni giorni (es. FX RRR 2021: annuncio 31 mag, effettivo 15 giu): per l'event study conta la seduta di reazione, tipicamente quella dell'annuncio.

```yaml
---
title: "La gestione del cambio da parte della People's Bank of China: fixing, strumenti, regimi ed episodi datati (2005–2026)"
date_compiled: 2026-08-21
primary_theme: monetary_policy
sub_themes: [pboc, cny, fx_intervention, fixing, managed_float, capital_controls, china_stimulus, asian_fx_spillover]
relevant_assets: [CNY=X, KRW=X, SGD=X, MYR=X, IDR=X, THB=X, JPY=X, EEM, HG=F, DX-Y.NYB, EWS, THD, EIDO, EWY, EWT, ^GSPC, ^VIX, GC=F, REMX, LIT]
external_assets_mentioned:
  - "CNY-CNH spread (differenziale onshore-offshore): misura diretta della pressione di mercato contro il fixing; non nel database"
  - "CFETS RMB Index: distingue debolezza vs USD da debolezza vs paniere; non nel database"
  - "USD/CNY e USD/CNH forward points: catturano attese e costo di scommettere contro il fix"
  - "SAFE monthly FX reserves: proxy (imperfetta) di intervento; mescola valutazione e flusso"
  - "CNH HIBOR: costo di funding offshore, indicatore di squeeze anti-short"
  - "Reuters/Bloomberg model-implied fix consensus: denominatore dello scarto di fixing"
time_window:
  start: 2005-07-21
  end: present
regime_phases:
  - hard_peg: 1994-01-01 to 2005-07-21
  - administered_appreciation: 2005-07-21 to 2008-12-31
  - crisis_reanchoring: 2008-12-31 to 2010-06-21
  - gradual_appreciation_widening_band: 2010-06-21 to 2015-08-11
  - eight_eleven_reform_disorderly_defense: 2015-08-11 to 2017-05-26
  - countercyclical_factor_basket_management: 2017-05-26 to 2019-05-01
  - tariffs_and_seven_threshold: 2019-05-01 to 2019-12-31
  - covid_appreciation: 2020-01-01 to 2021-12-31
  - depreciation_defense: 2022-01-01 to 2024-12-31
  - current_appreciation_management: 2025-01-01 to present
keywords: [yuan, renminbi, fixing, tasso di riferimento, banda, svalutazione, riserve valutarie, stimolo, PBoC, daily fix, midpoint, countercyclical factor, devaluation, managed float, CNH, offshore yuan, RRR, reserve requirement, CFETS, capital controls, asian fx spillover]
```