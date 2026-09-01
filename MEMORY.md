# MEMORY — News-to-Market Impact Pipeline

Stato per filone. Max 10 righe a filone. Ciò che resta vero per sempre va in
`CLAUDE.md` o in `references/`.

---

## Impianto generale

- **Stato** — **tutte le fasi complete e live**: market data (update 08:00), knowledge
  base (auto-indicizzata), classificazione (l'agente stesso), event study con libreria
  episodi "Opzione B", automazione giornaliera, report mensile strategico, scorecard
  settimanale. ⚠ Non descrivere nessuna fase come "da fare" o "Opzione A".
- **Deciso** — niente API key Anthropic; l'Opzione B ha sostituito le ~5 analogie scelte
  a mano; le research le scrive il maintainer.
- **Prossimo passo** — nessuno aperto sull'impianto: il lavoro è sui tre filoni sotto.

Aggiornato: 2026-08-30

---

## Costo del run

- **Stato** — media **$27,9 a run** (misurato 2026-08-21), guidata dal numero di turni:
  il cache-read è l'85% e cresce col quadrato dei turni. Quattro interventi applicati il
  21/08, ora tracciato in `news_impact_pipeline/logs/usage.csv`.
- **Deciso** — si riducono i **byte riletti a ogni turno**, non le operazioni. Il runbook
  ha una sezione "Economia del run" vincolante.
- **Prossimo passo** — due proposte non ancora applicate, la seconda più redditizia:
  (1) cap di lunghezza per scheda/indice con glossario unico in `render_report.py`;
  (2) **persistere le descrizioni degli episodi** in `_episodes.yaml`, che oggi butta via
  il testo — il 21/08 su 129 righe riscritte a memoria, 119 erano già in libreria.

Metodo e misure: [references/economia_del_run.md](references/economia_del_run.md)
Aggiornato: 2026-08-30

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

- **Stato** — audit del 2026-08-10: l'edge **non è mediocre ovunque, è spaccato per
  asset**. Bene su rischio/equity (`^VIX` IC +0,27), male su rifugio/tassi/dollaro
  (`IEF` −0,33, `DX-Y.NYB` hit 31%). L'IC ora si calcola dentro ciascun asset: il
  metodo vecchio sovrastimava ~3 volte.
- **Deciso** — la lettura direzionale si scrive **dopo** aver letto la sezione 5-bis
  della scorecard corrente, e sugli asset ❌ si dichiara inaffidabile il segno storico.
  Sempre con rimando alla scorecard viva, **mai a una lista fissa**.
- **Prossimo passo** — verificare sulle prossime scorecard che `monetary_policy` (IC 0,00
  con N=558, il più alto) e `DX-Y.NYB` migliorino, ora che il bug sulla direzione è
  corretto. ⚠ Da rivedere: ogni conclusione passata basata sull'IC alto a T+10, che era
  in gran parte artefatto di scala.

Dettaglio: [references/leggere_lo_scorecard.md](references/leggere_lo_scorecard.md)
Aggiornato: 2026-08-30

---

## Qualità delle etichette

- **Stato** — quarto livello `directions_declared` introdotto il 29/08: **356 episodi con
  verso dichiarato (36,2%), 235 netti**. Prima erano 171 su 984 con `pos` e `neg` insieme,
  152 dei quali dichiarati.
- **Deciso** — il verso dichiarato a mano batte ogni euristica e **cresce da solo** mentre
  le schede compilano il blocco: nessuna regex da mantenere. Gli errori tipo "imporre vs
  revocare una sanzione" **non erano problemi di vocabolario**.
- **Prossimo passo** — monitorare l'adozione con `analogues.py stats`; nessun intervento
  di codice previsto.

Meccanica e post-mortem: [references/etichette_date_locali.md](references/etichette_date_locali.md)
Aggiornato: 2026-08-30
