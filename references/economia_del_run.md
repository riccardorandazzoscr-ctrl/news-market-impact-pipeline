# Economia del run giornaliero

**Quando aprire questo file:** il costo del run è cresciuto, o stai modificando il
runbook, un tool della pipeline o il formato delle schede.

## Dove va la spesa

Il job delle 08:15 è **l'unica voce di spesa** della pipeline: lo scorecard settimanale
e `forecast_tracking.py` sono Python puro (zero chiamate al modello), il report mensile
è un run al mese.

Misurato il 2026-08-21 sui transcript in `~/.claude/projects/`: media **$27,9 a run**,
intervallo da $12 a $53. ⚠ **È una fotografia di quel giorno, non il costo attuale**:
gli interventi sotto sono nati per abbassarla, e il numero non si aggiorna da solo —
non riciclarlo come fattura. Il costo di oggi si legge dal registro (sotto), mai da
questo file.

**Il costo dipende quasi solo dal numero di turni**, perché a ogni chiamata di tool
l'intero contesto accumulato viene riletto: il cache-read è l'**85% della spesa** e
cresceva col **quadrato** dei turni sul campione dell'8/21 (tabella sotto). ⚠ È un
modello semplificato di come si accumula il contesto in QUEL campione, non una legge
universale — non trattarlo come un vincolo da imporre in un prompt.

| turni | costo (8/21) |
|---|---|
| 55 | $23 |
| 96 | $36 |
| 134 | $53 |

**Registro dei consumi** — uno schema unico, un file per job (R14, 2026-09-23):
`news_impact_pipeline/logs/usage.csv` (giornaliero), `usage_brief.csv` (briefing),
`usage_monthly.csv` (mensile). Ogni riga: identità (data, job, modello, tentativo),
stato (`ok` / `incompleto` / `errore` / `interrotto` — mai assente: un tentativo
fallito produce comunque una riga, i campi che non si conoscono restano **vuoti**,
non `0`), turni, token, costo riportato dal client. Storico pre-R14 (schema a 8
colonne, senza job/stato) archiviato in `usage.csv.pre-r14` / `usage_brief.csv.pre-r14`.
Costo per **scheda utile** e per **giornata completata** (join col conteggio schede
e la ricevuta di consegna, non un numero scritto qui):
```bash
news_impact_pipeline/venv/bin/python news_impact_pipeline/usage_report.py
```
⚠ Il costo riportato dal client (`total_cost_usd`), i token e la quota
dell'abbonamento sono **grandezze diverse**: un cache-read alto mostra rilettura di
contesto, non da solo il costo monetario o quanta quota è stata consumata.

## Interventi applicati il 2026-08-21

Nessuno tocca il contenuto delle schede.

1. **`event_study.py --markdown` omette di default il blocco `<details>` per-evento**
   — da 13.023 a 2.743 byte a chiamata. Serve solo per potare il pool o cacciare
   outlier: si richiede con `--detail` su quella singola chiamata.
2. **`run_daily_analysis.sh` gira con `--output-format json`** e accoda una riga a
   `logs/usage.csv`. Prima **il consumo non era misurabile** se non scavando nei
   transcript. Il testo finale resta nel log come prima; se il JSON è malformato (401,
   crash) il grezzo finisce comunque nel log e l'allarme di fallimento continua a
   funzionare.
3. **Sezione "Economia del run" vincolante nel runbook**: scrivi ogni file in un
   passaggio solo; Edit chirurgico per le correzioni; niente riletture di ciò che hai
   appena scritto; niente `--help`. Il 21/08 sono servite 43 chiamate di scrittura per
   9 file (`_index.md` riscritto 7 volte, `news_01.md` 7 volte, `news_03.md` 7 volte),
   ognuna rigenerando il corpo intero via heredoc; nello stesso run se ne andavano 10 KB
   di contesto in `--help` di comandi usati ogni giorno. Più una **"Riferimento
   comandi"** che documenta i flag, per non doverli più chiedere.
4. **Elenco asset rimosso** dal runbook e dal prompt del wrapper, dov'era duplicato e
   stale (diceva "46 asset" con 66 in DB). Fonte unica: `category_asset_map.yaml`.
   Era proprio la copia stale a costringere l'agente a rileggere lo YAML ogni mattina.

## Il principio che li accomuna

Tutti e quattro riducono **byte riletti a ogni turno**, non il numero di operazioni.
In un sistema dove il cache-read è l'85% della spesa, è l'unica leva che conta —
e una **copia stale costa doppio**: occupa contesto *e* costringe a rileggere la fonte
vera per non fidarsene.

## Interventi applicati il 2026-09-11

**Glossario unico**: `news_impact_pipeline/glossario.md` è la fonte unica delle
definizioni (sigle, dati macro, ticker); `render_report.py` lo rende una sola volta,
in fondo al report. Il template scheda non ha più la sezione "Glossario" — solo un
link (`#doc-glossario`) e un'istruzione: aggiungere un termine al file condiviso
**solo se manca davvero**, non ridefinirlo in scheda. Nato dall'11/09: un run parziale
(6 schede su 20, limite di sessione) aveva già speso quanto un giorno intero, in parte
perché ogni scheda riscriveva da zero glossari quasi identici.

⚠ **Non ancora verificato su un run reale** — l'effetto si legge sul registro
(sopra) al prossimo run, confrontando byte/turno con la tabella di riferimento sopra.

## Interventi applicati il 2026-09-23 (R14 — telemetria)

Il mensile era l'unico dei tre job col modello a non registrare nulla — zero righe,
mai. Indicizzazione e scorecard non usano un modello (Python puro): non gli manca
un registratore, non ne serve uno.

1. **`record_claude_usage.py` riscritto**: uno schema con identità (`job`, `model`,
   `attempt` — contato dal registro stesso, nessun contatore esterno) e `status`.
   Un grezzo non-JSON o senza blocco `usage` **produceva zero righe o una riga a
   zero**: ora produce sempre una riga (`errore`/`incompleto`), con i campi ignoti
   **vuoti**, non `0` — uno zero è indistinguibile da un run davvero gratis.
2. **`run_monthly_report.sh`** ora chiama `claude` con `--output-format json` e
   registra su `usage_monthly.csv`, come gli altri due job.
3. **Run interrotto da segnale esterno**: in tutti e tre i wrapper, se il grezzo
   esiste ancora quando il trap di pulizia scatta (il run non è mai arrivato alla
   registrazione), viene registrato con stato `interrotto` prima di essere tolto di
   mezzo — non più buttato via in silenzio (era il buco del run delle 09:19 del
   14/09, con consumo reale nei transcript ma nessuna riga nel CSV).
4. **`usage_report.py`** (nuovo): unisce il registro con `daily_analysis/` per il
   costo per scheda utile e per giornata completata — comando, non un numero da
   tenere aggiornato a mano.

## Proposte aperte

Stato e priorità in [MEMORY.md](../MEMORY.md).

- **Persistenza delle descrizioni degli episodi**: oggi `_episodes.yaml` salva
  data/verso/sotto-temi ma **butta via il testo**, così ogni mattina l'agente ri-scrive
  a memoria descrizioni di episodi già noti. Il 21/08 sono state scritte 129 righe di
  "Blocco dichiarato" su 119 date, **119 delle quali già in libreria**.
