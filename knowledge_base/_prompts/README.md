# `_prompts/` — prompt di deep research da eseguire a mano

## Regola (decisa il 2026-08-16, corretta il 2026-08-18)

Quando l'analisi giornaliera segnala una **lacuna di Knowledge Base** — cioè manca
uno studio che copra un tema/regime che il `match` non riesce a servire — Claude
**NON scrive la research** e **NON scrive nemmeno il prompt**. Si limita a
descrivere la lacuna nella sezione "Lacune emerse" di
`daily_analysis/YYYY-MM-DD/_index.md`, con abbastanza dettaglio da poterci tornare:
tema canonico, asset coinvolti, perché il pool attuale non basta, quante volte è
già ricorsa.

**Il prompt in questa cartella si scrive solo quando il maintainer lo chiede
esplicitamente.** Non è un passo del run giornaliero. La prima versione di questa
regola lo rendeva automatico e il 17-18 agosto 2026 la cartella si è riempita da
sola con tre prompt mai richiesti: da lì la correzione.

Quando la richiesta arriva:

1. si crea `_prompts/<slug>.md` seguendo `_TEMPLATE.md`;
2. lo si cita per percorso nella sezione "Lacune emerse" della giornata pertinente;
3. la deep research la esegue il maintainer per conto proprio, sullo strumento che preferisce.

Cosa fa Claude **dopo** che la research è stata eseguita e caricata:

1. la research finita va in una **sua cartella** sotto `knowledge_base/`
   (non qui) — es. `knowledge_base/Titolo dello studio/Titolo dello studio.md`;
2. `venv/bin/python build_catalog.py` per indicizzarla;
3. `venv/bin/python analogues.py build` per far entrare le date nella libreria episodi;
4. il prompt in `_prompts/` si **cancella** (o si marca `[ESEGUITO → percorso]` in testa),
   così questa cartella resta la lista di ciò che manca ancora.

## Git (deciso 2026-09-10)

I prompt (`<slug>.md`) **restano solo locali, mai committati** — sono richieste di
lavoro in sospeso per il maintainer, non output finito. Esclusi via `.gitignore`
(`knowledge_base/_prompts/*`). Questo file e `_TEMPLATE.md` restano tracciati:
sono l'infrastruttura della cartella, non una richiesta pendente.
⚠ Prima di questa data due prompt erano stati committati per errore (rimossi dal
tracking, restano sul disco): non è un precedente da seguire.

## Perché il prefisso `_`

Sia `build_catalog.py` sia `analogues.py` saltano ogni file/cartella il cui nome
inizia per `_`. Serve perché i prompt contengono un blocco ```yaml di **esempio**
e date ISO di **esempio**: senza l'esclusione finirebbero nel `catalog.yaml` come
studi fantasma e nella libreria `_episodes.yaml` come episodi inesistenti.
Non rinominare la cartella e non togliere il trattino basso.

## Stato

Un file qui = una research richiesta e non ancora eseguita.
