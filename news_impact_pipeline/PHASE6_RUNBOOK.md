# Fase 6 — Runbook Report Strategico Mensile

Procedura che l'agente Claude esegue una volta al mese per produrre il **Report
Strategico Mensile**: una sintesi di **regime e scenari** che aggrega tutto il lavoro
del mese (schede giornaliere + scorecard + Knowledge Base).

## Principio (decisivo)

NON è un oracolo a lungo raggio. La scorecard **coerente con la data del report**
(mai una fissa nel prompt) dice, sezione 3, se e quanto l'edge predittivo decade
con l'orizzonte, e sezione 5/5-bis quali temi/asset hanno IC negativo — cambia nel
tempo, non fissarlo qui. Quindi questo report:
- descrive i **regimi attivi** e il **bilancio dei rischi**, non dà prezzi-obiettivo;
- propone **scenari condizionali** ("se X → Y"), non una previsione singola;
- è **pesato dalla scorecard**: dà peso ai temi/asset con IC positivo nell'estratto
  (sez. 5/5-bis) e **declassa** esplicitamente quelli a IC ≈0 o negativo, chiunque
  siano quel mese → lettura qualitativa, mai magnitudo;
- chiude con **3-4 previsioni falsificabili**, che il mese dopo verranno verificate
  (scorecard a lungo raggio — vedi §"Verifica").

Meglio onesto e utile che sicuro e sbagliato: è la stessa disciplina del resto del
sistema (riportare N, dispersione, "indicative only").

## Input

- Schede del mese in `~/Claude/mercati_finanza/daily_analysis/YYYY-MM-*/news_*.md`.
- Scorecard **coerente con il mese del report** (la più recente non successiva a
  fine mese, non sempre l'ultima in assoluto) in
  `~/Claude/mercati_finanza/daily_analysis/_scorecard/`.
- Catalogo KB (`knowledge_base/catalog.yaml`) per i regimi attivi **alla data del
  report** (fine mese), non l'ultima fase elencata nel file.

## Output

- `~/Claude/mercati_finanza/daily_analysis/_monthly/YYYY-MM.md` (+ `.html`): il report compilato.

## Procedura (comandi dalla dir `news_impact_pipeline/`)

1. **Genera la bozza aggregata** (il mese di norma è quello appena concluso):
   ```bash
   venv/bin/python monthly_digest.py --month YYYY-MM
   ```
   Crea `daily_analysis/_monthly/YYYY-MM.md` con: schede aggregate (temi, sentiment,
   asset), regimi KB attivi alla data del report, **estratto della scorecard
   coerente con quella data** (sintesi + tabella per tema + tabella per asset,
   5-bis), ed elenco schede per tema. La sezione "Materiale aggregato" NON va
   modificata.

2. **Compila le 6 sezioni** del report via Edit, leggendo il materiale aggregato (e,
   se serve dettaglio, le singole schede del mese):
   1. **Mappa dei regimi attivi** — quali regimi dominano ora, da quando, quali asset.
   2. **Bilancio dei rischi cross-asset** — direzione di rischio prevalente per
      azionario / tassi / FX / commodity / credito-volatilità.
   3. **Catalizzatori in arrivo (calendario)** — eventi datati del mese entrante
      (CPI/NFP/PIL, banche centrali, elezioni, scadenze). Fattuale.
   4. **Scenari condizionali** — 2-3 scenari "condizione → conseguenze", ramificati.
   5. **Lettura pesata dalla scorecard** — esplicita dove fidarsi (temi con edge) e
      dove no (IC≈0 o negativo). Ricorda che l'edge è a orizzonte breve.
   6. **Previsioni falsificabili del mese** — 3-4 affermazioni verificabili tra ~1
      mese, ognuna con condizione/metro e data di verifica (la tabella è già pronta).

3. **Rigenera l'HTML** dopo aver compilato:
   ```bash
   venv/bin/python monthly_digest.py --month YYYY-MM --render-only
   ```

## Stile (VINCOLANTE)

Vale la stessa sezione "Stile e chiarezza" di `PHASE5_RUNBOOK.md`: **espandi ogni
sigla** alla prima occorrenza (dati macro, policy, ticker), **spiega i meccanismi**
causali, **interpreta i numeri a parole**, tono didattico, chiarezza > brevità.

## Verifica (scorecard a lungo raggio)

Le "Previsioni falsificabili" (§6) di ogni edizione sono pensate per essere
controllate il mese successivo: l'edizione N+1 dovrebbe aprire con un breve
**consuntivo** delle previsioni dell'edizione N (azzeccate / mancate / parziali),
costruendo un track record del layer mensile — esattamente come la scorecard
settimanale fa per le schede giornaliere. (Automazione della verifica: da costruire
quando ci sarà almeno un'edizione di previsioni da controllare.)

## Cadenza

- **Mensile**, il 1° del mese (copre il mese appena concluso). Job launchd
  `com.newsimpact.monthly`.
- **Edizione straordinaria** opzionale a fronte di un break di regime (shock estremo):
  rilevatore da costruire in seguito; per ora si lancia a mano la procedura.

## Prompt suggerito per la routine `/schedule`

> Produci il Report Strategico Mensile del mese appena concluso seguendo
> `~/Claude/mercati_finanza/news_impact_pipeline/PHASE6_RUNBOOK.md`: genera la bozza aggregata con
> `monthly_digest.py`, poi compila le 6 sezioni (regimi, rischi, calendario, scenari
> condizionali, lettura pesata dalla scorecard, 3-4 previsioni falsificabili),
> rispettando lo stile (espandi le sigle, spiega i meccanismi, pesa per la scorecard:
> NIENTE magnitudo sui temi a IC negativo). Apri l'edizione con il consuntivo delle
> previsioni falsificabili del mese precedente, se esiste. Infine rigenera l'HTML
> con `--render-only`. Riporta in chat: regimi dominanti e le previsioni falsificabili.
