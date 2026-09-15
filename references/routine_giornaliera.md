# Routine giornaliera — esecuzione locale su Claude Code

Tutto gira in locale su questo Mac, via `launchd`. Non serve nessuna app aperta:
basta che il Mac sia sveglio. Se era spento all'ora prevista, `launchd` coalizza
l'evento e lo esegue al risveglio — gli script sono idempotenti, quindi un run
in ritardo non produce doppioni.

I tre job che usano un modello lanciano `claude -p` **headless** con
`--permission-mode bypassPermissions`. Nessuna API key: l'autenticazione è quella
dell'abbonamento Claude, la stessa della CLI interattiva.

| Fase | Orario Europe/Rome | Job launchd | Script | Modello |
|---|---|---|---|---|
| Morning briefing | 07:30 ogni giorno | `…newsimpact.brief` | `run_morning_brief.sh` | Opus 5 (ricerca web) |
| Prezzi | 08:00 ogni giorno | `…newsimpact.marketdata-update` | `update_market_data.py` | Nessuno: Python deterministico |
| Analisi | 08:15, ritentativi 09:15 e 10:15 | `…newsimpact.daily` | `run_daily_analysis.sh` | Opus 5 |
| Indicizzazione KB | a ogni modifica di `knowledge_base/` | `…newsimpact.indexkb` | `index_studies.sh` | Opus 5 |
| Scorecard | Lunedì 09:00 | `…newsimpact.scorecard` | `run_scorecard.sh` | Nessuno: Python deterministico |
| Strategia mensile | Giorno 1, 09:30 | `…newsimpact.monthly` | `run_monthly_report.sh` | Opus 5 |

Il job `daily` ha anche `WatchPaths` sulla cartella dei briefing: se il brief
arriva in ritardo, l'analisi parte appena il file atterra. I ritentativi delle
09:15 e 10:15 coprono un caso diverso — il run **fallito a metà** — che i
WatchPaths non ricatturano, perché a quel punto il file del briefing non cambia
più. Entrambi escono subito se la giornata è già conclusa, e altrimenti
riprendono dalla **prima fase incompleta**: se mancano solo il report o l'invio
non richiamano l'agente. A che punto sia una giornata lo dice
`stato_giornata.py --date AAAA-MM-GG` (tabella delle sei fasi in
[quando_si_rompe.md](quando_si_rompe.md)).

⚠ Il brief delle 07:30 può far scattare l'analisi **prima** dell'aggiornamento
prezzi delle 08:00. Prima delle 08:30 quel run esce in silenzio (`ATTESA:` nel
log) e lascia fare a quello di calendario; dopo, i prezzi mancanti sono un
guasto e il run si ferma con un allarme invece di analizzare su dati vecchi.

Il brief segue `news_impact_pipeline/news_research_prompt.md` (lo script estrae
il blocco fra `=== PROMPT START/END ===`, non ne tiene una copia propria);
l'analisi segue `PHASE5_RUNBOOK.md`; il mensile `PHASE6_RUNBOOK.md`.

## I plist stanno in due posti

La copia **versionata** è in `news_impact_pipeline/launchd/`. La copia **viva**,
quella che `launchd` legge davvero, è in `~/Library/LaunchAgents/`.
Modificare la prima non ha alcun effetto finché non la copi e ricarichi il job:

```bash
cp news_impact_pipeline/launchd/com.riccardo.newsimpact.daily.plist ~/Library/LaunchAgents/
launchctl bootout gui/$(id -u)/com.riccardo.newsimpact.daily 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.riccardo.newsimpact.daily.plist
```

## Verifiche operative

Dalla cartella `/Users/riccardo/Claude/mercati_finanza`:

```bash
claude --version                                        # la CLI c'è
launchctl list | grep newsimpact                        # i 6 job sono caricati
tail -30 news_impact_pipeline/logs/brief-$(date +%F).log # il brief è uscito?
tail -30 news_impact_pipeline/logs/$(date +%F).log       # l'analisi è uscita?
ls -l "../morning brief/$(date +%F)-morning-briefing.html"
tail -3 news_impact_pipeline/logs/usage.csv             # costo degli ultimi run
```

Nella seconda colonna di `launchctl list` c'è l'ultimo exit code: `0` è
normale, un numero diverso dice che l'ultimo run è fallito. Un job assente
dall'elenco non è "a riposo", è **scaricato**: non partirà.

## Rilanciare a mano

Ogni script accetta una data ISO per rigenerare un giorno saltato, ed è
idempotente: se il lavoro di quel giorno c'è già **fino alla consegna**, esce
senza rifarlo; se è rimasto a metà, riprende da dove si era fermato senza
rifare le schede già valide.

```bash
/bin/zsh news_impact_pipeline/run_morning_brief.sh   2026-09-15
/bin/zsh news_impact_pipeline/run_daily_analysis.sh  2026-09-15
```

## Storia

Fino al 13/09/2026 l'orchestrazione è stata spostata sui task locali dell'app
ChatGPT (Codex). Rientrata su Claude Code il **15/09/2026**: stessi script,
stessi orari, stessi guardiani; è cambiato solo chi fa il lavoro. Due differenze
rispetto all'assetto ChatGPT, entrambe tenute:

- i **ritentativi 09:15/10:15** sull'analisi, che prima erano tre task separati
  e ora sono tre orari dello stesso job;
- il **morning brief**, che prima non aveva uno script locale (era una routine
  cloud, poi un task dell'app) e ora è un job come gli altri.

⚠ Se i vecchi task ChatGPT sono ancora programmati vanno **cancellati a mano**
dall'app: girerebbero sugli stessi script, e il risultato sarebbe un doppio
invio Telegram — non un doppio lavoro, perché i lock e le sentinelle reggono,
ma il rumore sì.
