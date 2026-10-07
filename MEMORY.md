# MEMORY — News-to-Market Impact Pipeline

Stato per filone. Max 10 righe a filone. Ciò che resta vero per sempre va in
`CLAUDE.md` o in `references/`.

---

## Impianto generale

- **Stato** — tutte le fasi implementate: market data, knowledge base, classificazione
  dell'agente, event study "Opzione B", analisi giornaliera, report mensile e scorecard.
  Il 15/09/2026 l'orchestrazione è **rientrata su Claude Code** (era passata ai task
  ChatGPT il 13/09): 6 job launchd, i tre che usano un modello lanciano `claude -p`
  headless su Opus 5.5. ⚠ Non descrivere fasi come "da fare".
- **Deciso** — niente API key Anthropic; l'Opzione B ha sostituito le ~5 analogie scelte
  a mano; le research le scrive il maintainer. Il morning brief, che non aveva uno
  script locale, ora è un job come gli altri: niente dipende più da un'app aperta.
- **Deciso (15/09, R07)** — la catena giornaliera ha **sei fasi verificabili**
  (`stato_giornata.py`): il ritentativo riparte dalla prima incompleta e non
  richiama l'agente se mancano solo render o consegna. La verità è il disco;
  `_state.json` tiene solo impronta dell'input e ricevuta dell'invio. I prezzi sono
  un cancello bloccante senza scavalco: si ripara il dato.
- **Osservato (16/09)** — primo ciclo completo dopo i Run 1–4b: brief 07:40 → dati
  08:00 → analisi 08:15 → Telegram 08:26:49, tutte e sei le fasi ✔ al primo colpo
  (nessun ritentativo, riuso schede non ancora testato su un caso vero). Costo
  $3,10 (contro $27,9 di agosto, altro modello/formato — confronto non ancora
  solido su un solo run). Nessun buco/riga senza prezzo, link interni al report ok,
  ricevuta Telegram ok.
- **Prossimo passo** — confermare il costo su altri giorni (non solo 20 notizie/2
  schede come il 16/09) e osservare il primo ritentativo vero per verificare che il
  riuso delle schede scatti davvero. Vedi `references/routine_giornaliera.md`.

Aggiornato: 2026-09-16

---

## Costo del run

- **Stato** — media **$27,9 a run** (misurato 2026-08-21), guidata dal numero di turni:
  il cache-read è l'85% e cresce col quadrato dei turni. Quattro interventi applicati il
  21/08, ora tracciato in `news_impact_pipeline/logs/usage.csv`.
- **Deciso** — si riducono i **byte riletti a ogni turno**, non le operazioni. Il runbook
  ha una sezione "Economia del run" vincolante.
- **Prossimo passo** — una proposta applicata, una no:
  (1) **fatto il 2026-09-11** — glossario unico in `news_impact_pipeline/glossario.md`,
  reso da `render_report.py` una sola volta in fondo al report; ogni scheda linka lì
  invece di ridefinire le sigle. Il template dice all'agente di aggiungere un termine
  mancante al file condiviso solo se genuinamente nuovo, non di riscriverlo.
  (2) resta aperta — **persistere le descrizioni degli episodi** in `_episodes.yaml`,
  che oggi butta via il testo — il 21/08 su 129 righe riscritte a memoria, 119 erano
  già in libreria.
- **Da verificare** — l'effetto sul costo si vede solo al prossimo run reale
  (`logs/usage.csv`): la scommessa è che l'agente smetta di riscrivere definizioni
  già note, ma non è stato ancora osservato su un run vero.
- **Deciso (23/09, Run 10/R14)** — registro unico per schema (non più file): un CSV
  per job (`usage.csv`/`usage_brief.csv`/`usage_monthly.csv`, prima assente per il
  mensile) con identità, stato e tentativo; un run fallito produce sempre una riga,
  mai zero. `usage_report.py` per $/scheda e $/giornata completata.

Metodo e misure: [references/economia_del_run.md](references/economia_del_run.md)
Aggiornato: 2026-09-23

---

## Copertura asset

- **Stato** — G10 valutario completo dal 29/08. Si è passati dalle aggiunte reattive
  all'**audit non reattivo** (primo il 19/08, secondo il 29/08).
- **Deciso** — il segnale che serve un audit è la **ripetizione** della stessa classe di
  scarto in triage, non il singolo caso. Prima di aggiungere un ETF si misura la
  correlazione con quel che c'è già: sopra ~0,85 è un duplicato.
- **Prossimo passo** — due lacune aperte: **rame LME** (serve fonte esterna, i candidati
  ovvi sono tutti Comex-based) e **equipaggiamento di rete/turbine** (`XLU` è la domanda
  elettrica, non chi vende gli impianti; `GRID` scartato, correlava 0,80 con `SOXX`).

Criteri e cronologia: [references/copertura_asset.md](references/copertura_asset.md)
Aggiornato: 2026-08-30

---

## Qualità delle previsioni

- **Stato** — revisione precisione applicata il 30/09/2026; verifica con `news_impact_pipeline/run_tests.sh precisione` e `forecast_tracking.py audit`.
- **Deciso** — registrazione giornaliera prima della consegna; valori congelati anche pendenti, copie delle schede e versione del metodo. Recuperi storici separati dal flusso live.
- **Deciso** — analoghi stretti per default, senza ampliamento per raggiungere N; conflitti direzionali esclusi. `--as-of` limita gli esiti osservabili.
- **Deciso** — scorecard per uso/provenienza e asset/orizzonte, con benchmark sugli stessi casi; niente semafori basati sul 50%.
- **Prossimo passo** — osservare le coorti live mature prima di giudicare il miglioramento. Regimi strutturati e identità univoca delle release restano da implementare.

Metodo: [references/leggere_lo_scorecard.md](references/leggere_lo_scorecard.md)

---

## Qualità delle etichette

- **Stato** — quarto livello `directions_declared` introdotto il 29/08: **356 episodi con
  verso dichiarato (36,2%), 235 netti**. Prima erano 171 su 984 con `pos` e `neg` insieme,
  152 dei quali dichiarati. Il 10/09 aggiunte due etichette `inflation_upside`/
  `inflation_downside` in `subtheme_taxonomy.yaml`: il verso dichiarato codifica la
  reazione dell'asset della scheda, non il verso del dato, e il pool `inflation_print`
  mescolava rialzi e ribassi del CPI/PCE (N=1143, mediane schiacciate a zero). N=14/15
  episodi date-locali, sopra soglia; testato con 27 casi sintetici prima del deploy.
- **Deciso** — il verso dichiarato a mano batte ogni euristica e **cresce da solo** mentre
  le schede compilano il blocco: nessuna regex da mantenere. Gli errori tipo "imporre vs
  revocare una sanzione" **non erano problemi di vocabolario**. Per il verso del *dato*
  macro (diverso dal verso della *reazione*) si usa un sotto-tema regex date-locale, non
  si tocca il formato dichiarato — che resta sulla reazione, per costruzione.
- **Deciso (23/09, Run 5d)** — il verso è la **sorpresa** rispetto al già prezzato. I versi
  delle research stanno nel registro `_direction_reviews.yaml` (11 research, approvate riga per
  riga); le schede di agosto **non** si recuperano (il loro Verso non aveva un asset).
  (30/09) Rivisti a mano su `IEF` gli episodi `macro_data` USA lavoro/fiducia: dato debole →
  `pos`, forte → `neg`, esclusi i casi con segnali opposti o eventi simultanei.
- **Prossimo passo** — le prossime schede su `inflation_print` usano `--subtheme
  inflation_upside`/`inflation_downside` invece di `--direction` quando la domanda è sul
  dato. Ricontrollare fra un mese se la mediana di `macro_data` si allontana da zero.

Meccanica e post-mortem: [references/etichette_date_locali.md](references/etichette_date_locali.md)
Aggiornato: 2026-09-23

---

## Laboratorio CPI

- **Stato** — archivio 2015–2026-08 e calendario XNYS completi; conteggi con `cpi_lab.py validate`, esiti con `replay` + `report` (vedi reference).
- **Deciso** — consenso solo «Median Forecast» MarketWatch da snapshot Wayback pre-rilascio; da settembre 2026 il calendario è Onclusive/Dow Jones («Forecast»): non si mescola. Protocollo 1.1.0 (campione iniziale dal 2015).
- **Deciso** — (04/10) primo replay: su `^GSPC` da chiusura del rilascio a T+5 né il condizionato (sorpresa × ultima mossa Fed) né gli analoghi battono il riferimento; segno ~50%.
- **Deciso** — (04/10) versione 2.0 (reazione del giorno, `IEF`, «solo sorpresa»): la sorpresa indica il verso del giorno nel 59–66% dei casi, l'ampiezza no; nessun confronto regge la correzione per 12 test.
- **Deciso** — (04/10) protocollo 3.0.0: inversione della reazione di `IEF` a 5 sedute, da verificare sui rilasci 2011–2014 e sui primi 30 da ottobre 2026; sui dati già visti è 54%, aspettativa bassa.
- **Deciso** — (04/10) campione A del 3.0.0 (2011–2014): 27/48 opposti, p=0,235, inversione non sostenuta.
- **Deciso** — (04/10) un fornitore di consenso per serie, dichiarato nel protocollo (`consensus_providers`); Onclusive è serie a sé, unibile alla mediana MarketWatch solo con raccordo 11/12.
- **Prossimo passo** — campione B del 3.0.0 a 30 rilasci (circa fine 2028); per la serie Onclusive serve catturare la pagina prima di ogni CPI, non automatizzato.

Metodo: [references/laboratorio_cpi.md](references/laboratorio_cpi.md)

---

## Quantitativo «reazione, non seguito» (Run 11)

- **Stato** — 11a chiuso il 2026-10-07: protocollo `experiments/quant_reazione/protocol-1.0.0.json` registrato prima del codice; misure esplorative con `news_impact_pipeline/quant_reazione.py replay`.
- **Deciso** — (07/10) il segno del seguito T+h non ha informazione (~50%); l'informazione sta nella reazione del giorno della notizia. Il cancello |z| ≥ 2 e N ≥ 10 (protocollo 1.0.0, decisione a 60 giorni) sui dati visti **non** batte la regola cieca «sempre sotto la mediana normale» (34/11 contro 33/11): il test contro il 50% confonde il pool con il regime.
- **Prossimo passo** — prima dell'11b il maintainer decide: protocollo 1.1.0 (test contro benchmark o permutazione, un voto per seduta-ancora) oppure niente previsioni sul seguito (reazione + già prezzato + «seguito non distinguibile»). Le definizioni di `quant_reazione.py` restano il riferimento per l'11b.

Spec e sequenza: [PIANO_REVISIONE_PIPELINE.md](PIANO_REVISIONE_PIPELINE.md) (Run 11)
