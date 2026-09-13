# Routine ChatGPT — esecuzione locale

La cartella resta in `/Users/riccardo/Claude`. Il Mac deve essere acceso e l'app
ChatGPT aperta durante le attività. Le attività sono visibili in **Scheduled**.
I vecchi job `com.riccardo.newsimpact.*` restano disabilitati: non riattivarli
insieme ai task ChatGPT, per evitare analisi e invii Telegram duplicati.

| Fase | Orario Europe/Rome | Task ChatGPT | Modello che fa il lavoro |
|---|---|---|---|
| Morning briefing | 07:30 ogni giorno | Ricerca web e HTML, nel progetto Claude | GPT-5.6 Terra, high |
| Indicizzazione KB | 07:55 ogni giorno | Esegue `index_studies.sh` | GPT-5.6 Terra, medium (interno) |
| Prezzi | 08:00 ogni giorno | Esegue `update_market_data.py` | Nessuno: Python deterministico |
| Analisi | 08:15, 09:15, 10:15 ogni giorno | Esegue `run_daily_analysis.sh`; retry idempotenti | GPT-5.6 Sol, high (interno) |
| Scorecard | Lunedì 09:00 | Esegue `run_scorecard.sh` | Nessuno: Python deterministico |
| Strategia mensile | Giorno 1, 09:30 | Esegue `run_monthly_report.sh` | GPT-6 Astra, high (interno) |
| Controllo di salute | 11:30 ogni giorno | Verifica brief, analisi, dati e Telegram; avvisa solo su guasti | Nessuno: controlli su file e log |

I task che avviano uno script usano GPT-5.6 Luna/minimal solo per coordinare e
riportare l'esito. Non duplicano l'analisi svolta dal modello interno allo script.
Il brief segue `news_impact_pipeline/news_research_prompt.md`; l'analisi segue
`PHASE5_RUNBOOK.md`; il mensile segue `PHASE6_RUNBOOK.md`. Il brief deve avere
20 elementi `class="story"` e va pubblicato in modo atomico. Il job giornaliero
verifica completezza, tiene lock e watchdog, e invia il risultato su Telegram.

Verifiche operative:

```bash
codex login status
launchctl print-disabled gui/$(id -u) | rg newsimpact
tail -30 news_impact_pipeline/logs/$(date +%F).log
ls -l "../morning brief/$(date +%F)-morning-briefing.html"
```

L'ultimo comando è valido partendo da `/Users/riccardo/Claude/mercati_finanza`.
La routine Claude **Daily morning briefing** è in pausa. Gli storici restano
nel vecchio formato; i nuovi consumi Codex vanno in `logs/codex_usage.csv`.
