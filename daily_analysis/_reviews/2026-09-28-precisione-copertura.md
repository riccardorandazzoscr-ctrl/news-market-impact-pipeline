# Revisione di precisione e copertura della pipeline

## Scopo e metodo

Diagnosi del codice e degli artefatti presenti il 28 settembre 2026. Nessuna modifica al sistema operativo, ai dati, alle schede, alla KB o al ledger. Le prove di riproduzione usano file temporanei; le statistiche del campione si calcolano con il comando in fondo, senza trascriverle in questo documento.

Domande distinte: il sistema misura tutte le proprie analisi? Le analogie selezionate sono pertinenti? Le statistiche aggiungono informazione rispetto a riferimenti semplici? Una buona copertura del catalogo non dimostra nessuna delle tre cose.

Sono stati letti codice di selezione, metadati, event study, tracking, istruzioni quotidiane, template, scorecard corrente, schede recenti, registro delle modifiche e reference metodologiche. Non è stato verificato esternamente ogni fatto delle notizie o degli episodi storici; autenticità delle fonti e consensi storici restano un controllo distinto. Non è stato eseguito un backtest completo fuori campione.

## P1 — La scorecard perde schede per differenze di formato

`news_impact_pipeline/forecast_tracking.py`, `parse_card`, spezza il testo su `###` e accetta soltanto intestazioni che iniziano con `Event study —` e ticker fra backtick. La presenza di tabelle valide con intestazioni differenti non genera errore: restituisce una lista vuota.

Caso riprodotto: `daily_analysis/2026-09-18/news_01.md` contiene tabelle sotto intestazioni `####` con il ticker. Il parser non estrae previsioni; cambiando esclusivamente quei titoli in una copia temporanea riconosce gli stessi dati. Anche schede dei giorni 15, 17 e 22 settembre hanno tabelle che non entrano nel ledger. Il comando diagnostico sotto misura l'estensione sull'intero archivio.

Il giorno 22 compaiono inoltre tabelle accorpate per più asset: correggere soltanto il numero di `#` non recupera tutto. Serve un censimento dei formati, non una sostituzione indiscriminata.

**Conseguenza:** la scorecard è un campione selezionato anche dalla presentazione Markdown. Non possiamo assumere che rappresenti tutta la produzione o che i cambiamenti recenti siano tutti misurati.

**Intervento:** per il futuro, generare un risultato strutturato comune a renderer e tracking, con uso dichiarato e orizzonti. Nell'immediato, fallire esplicitamente se una scheda contiene risultati ma il parser ne estrae zero, oppure se perde tabelle. Per l'archivio, aggiungere adattatori ai formati realmente presenti e quarantena dei casi ambigui. Conservare la scorecard originale e distinguere il recupero retrospettivo dalle osservazioni registrate all'epoca. Non ricostruire ex post l'etichetta “previsione attiva” dalla performance.

**Accettazione:** ogni scheda prodotta ha un esito di ingestione verificabile: acquisita, priva di risultati o esclusa con motivo. Nessuna perdita silenziosa. Test su copie delle schede reali, comprese tabelle accorpate.

## P1 — Il confronto con la monetina non dimostra valore aggiunto

`forecast_tracking.py`, `_verdict` e `cmd_scorecard`, usa il 50% come riferimento direzionale. La sintesi afferma inoltre incondizionatamente che esistono ticker con un “vantaggio reale”. La tabella per asset è più prudente, ma le schede usano comunque hit-rate superiore al 50% e IC positivo per abilitare previsioni.

Nel ledger corrente alcuni degli asset presentati come affidabili non superano una regola sempre rialzista sugli stessi casi direzionali. Il comando sotto mostra il confronto. È una diagnosi della baseline mancante, non la proposta di una strategia sempre rialzista e non un risultato fuori campione.

Esempio di propagazione: `daily_analysis/2026-09-28/news_01.md` usa le metriche di HO=F per definirlo affidabile e costruire la previsione. `2026-09-24/news_01.md` fa una scelta analoga su ^FVX. Senza riferimenti adeguati, il filtro di affidabilità può promuovere un asset che riflette soltanto la prevalenza dei rialzi nel campione.

**Intervento:** mostrare riferimenti fissi sempre-su e sempre-giù come controlli diagnostici; per la valutazione vera confrontare, sugli stessi eventi, previsioni e distribuzioni semplici costruite esclusivamente dal passato del medesimo asset/orizzonte. Separare errore della mediana, segno, copertura delle bande e loro ampiezza. Congelare regole di promozione prima del periodo di verifica: scegliere i ticker migliori dopo aver visto gli esiti è selezione retrospettiva.

Non riproporre la correzione dei rendimenti anomali già scartata: un benchmark serve a misurare il contributo del metodo, non a trasformare i rendimenti del metodo stesso.

**Accettazione:** nessun “affidabile” automatico basato sul solo hit-rate >50%; ogni confronto dichiara denominatore, astensioni, periodo e riferimento. Differenze piccole o campioni insufficienti restano inconcludenti.

## P1 — Il riepilogo cumulativo nasconde le versioni e sovrappesa eventi ripetuti

`cmd_scorecard` aggrega tutte le righe mature del ledger, escluse ritirate e scenari. Le tabelle descrittive e non dichiarate restano nel riepilogo. La distinzione di uso introdotta il 23 settembre compare soltanto in una sezione separata. I cambiamenti del parser KB e del selettore sono anch'essi recenti: la data di creazione della scheda è solo un'approssimazione della versione effettivamente utilizzata.

Una riga è scheda × asset × scenario × orizzonte. Schede diverse possono valutare lo stesso movimento di mercato; orizzonti diversi si sovrappongono. Il numero di righe non è il numero di prove indipendenti. Gli intervalli Wilson non risolvono questa dipendenza; il caveat lo ammette, ma il conteggio continua a guidare soglie e lettura.

**Intervento:** viste separate per versione e periodo di emissione, solo previsioni attive nel riepilogo prospettico; legacy e descrittive in sezioni distinte. Mostrare anche giorni, schede e movimenti di mercato unici. Valutare ogni asset e orizzonte separatamente, con incertezza che consideri raggruppamenti temporali e finestre sovrapposte. Gli stessi scenari possono restare nel registro senza fingere nuove osservazioni indipendenti.

Registrare la previsione quando nasce la scheda. Attualmente `run_scorecard.sh` esegue backfill settimanale: il primo hash può essere acquisito dopo che un esito è già noto. Inoltre `cmd_backfill` permette di aggiornare una riga finché non è valutata, che non equivale a “prima che il suo esito fosse conoscibile”. È una lacuna di auditabilità, non prova che qualcuno abbia alterato le previsioni.

**Accettazione:** versione, timestamp e input originali ricostruibili; correzioni append-only distinguibili dall'originale; riepilogo recente con orizzonti effettivamente maturi e avvertenza quando il campione è ancora insufficiente.

## P1 — Il sistema può comprare numerosità sacrificando pertinenza

`analogues.py`, `cmd_find`, allarga automaticamente dal sotto-tema locale al documento e poi al tema se non raggiunge `min_n`. Il filtro direzionale viene applicato dopo questa scelta. Il log dichiara il degrado, ma non lo impedisce. Le istruzioni prescrivono anche integrazione manuale quando il campione è piccolo.

Caso reale: `daily_analysis/2026-09-24/news_01.md` dichiara di aver rinunciato al sottoinsieme più stretto per usare l'intero tema. Nei caveat ammette che nessun precedente è un PMI, benché il PMI sia al centro della notizia; il campione include payroll, consumi, CPI e comunicazione della Fed.

Questa è copertura nominale: avere abbastanza date non significa avere abbastanza eventi confrontabili.

**Intervento:** rendere vincolanti famiglia di evento, geografia e meccanismo quando la domanda li richiede. Applicare i filtri congiuntamente e mostrare la perdita di copertura a ogni passaggio. Un fallback più largo può essere fornito come contesto descrittivo separato, mai promosso automaticamente alla stessa previsione. Con N insufficiente, astenersi o dichiarare l'evidenza indicativa; non aggiungere date solo per superare una soglia.

**Accettazione:** una query PMI non diventa un pool macro generico senza una decisione esplicita e una diversa qualifica del risultato. I vincoli obbligatori restano soddisfatti da ogni evento restituito.

## P1 — Il regime è descritto, ma non governa il pool

`analogues.py` limita alle date più recenti, senza una condizione strutturata sul regime. Un tetto di recency non identifica un regime economico: nei pool piccoli può lasciare intatto uno storico molto lungo.

`2026-09-28/news_01.md` dichiara che nessun precedente appartiene alla fase attuale e che il premio iniziale era diverso. `2026-09-28/news_02.md` mescola QE, stretta quantitativa e fase corrente. Il caveat è corretto, ma le mediane vengono comunque usate per una lettura direzionale attiva.

**Intervento:** per le famiglie più utilizzate, rendere operativi pochi criteri determinati prima dell'esito: tipo di shock, sorpresa rispetto alle attese, fase di politica monetaria; per energia distinguere interruzione fisica, sanzione, minaccia e negoziato. Se lo stato attuale non ha precedenti comparabili, mostrarlo come assenza di evidenza trasferibile. Evitare decine di filtri che frammentino ulteriormente il campione.

Si può avviare questa correzione sulle famiglie già usate quotidianamente, senza implementare prima l'intero laboratorio CPI. L'effetto sulla precisione resta da dimostrare con confronto prospettico.

## P2 — Due ambiguità residue nell'indicizzazione

**Identità incompleta.** Il Run 6 distingue eventi per data × tema × geografia. In `analogues.py`, `cmd_build`, `events.setdefault(where, ...)` unisce però eventi diversi della stessa area nello stesso giorno. Prova sintetica riprodotta in una directory temporanea: due fonti distinte, una CPI e una payroll, stessa data/tema/paese e medesimo verso; una query in intersezione CPI+NFP restituisce quella data. La correzione geografica funziona, ma non è ancora un'identità dell'evento. Questa prova non dimostra da sola la frequenza del difetto nell'archivio reale.

Rimedio: identificatore stabile del rilascio/decisione/shock, con fonti multiple riferite allo stesso evento. Conservare separati identità causale e giorno di mercato: più eventi nello stesso giorno non producono più rendimenti indipendenti.

**Sorpresa contro variazione del livello.** In `subtheme_taxonomy.yaml`, `inflation_upside` riconosce anche “sale”, `inflation_downside` anche “scende”. Entrambe le frasi sintetiche «CPI scende al 3,0%, ma sopra il consenso del 2,9%» e «CPI sale al 3,0%, ma sotto il consenso del 3,2%» ricevono entrambe le etichette. La convenzione sul verso è migliorata, ma queste regex non garantiscono che le etichette macro rappresentino la sorpresa.

Rimedio: separare variazione del livello e sorpresa rispetto al consenso; dato numerico/provenienza se disponibili, altrimenti dichiarazione esplicita verificata o stato ambiguo. Non aggiungere semplicemente altre regex per aumentare N.

## P2 — Convenzione temporale troppo implicita

`event_study.py` usa chiusura del giorno-ancora e successive righe di prezzi. Non dispone di un cutoff `as_of` che verifichi la maturazione di ciascun analogo né di un timestamp dell'annuncio. `analogues.py --before` filtra la data dell'evento, non quando furono conoscibili il suo esito o le sue etichette.

Non basta cambiare l'ancora per ottenere un vantaggio: la reference sugli esperimenti scartati documenta già un'ipotesi di ancoraggio. Occorre invece definire la domanda. Un briefing del mattino su fatti del giorno precedente e un precedente ancorato al giorno dell'annuncio non partono necessariamente dalla stessa distanza informativa dall'evento. Nel documento del 18 settembre si legge persino “chiusura precedente all'evento”, mentre il codice usa la prima chiusura alla data o dopo: la descrizione va allineata al calcolo.

Intervento: distinguere ora del fatto, ora dell'analisi e prezzo iniziale della misurazione; scegliere esplicitamente impatto o continuazione e applicare la stessa convenzione a precedenti e osservazione corrente. Rendere il cutoff un controllo del calcolo, non soltanto una frase nelle istruzioni.

## Come ampliare la copertura in modo utile

Prima recuperare e rendere accessibili i fatti già disponibili. Il recente recupero delle dichiarazioni dalla KB è un miglioramento reale dell'infrastruttura; non si traduce automaticamente in capacità predittiva.

Il prossimo elenco di lacune dovrebbe essere prodotto dal funnel effettivo:

1. Notizia rilevante e famiglia identificata.
2. Asset coerente con il canale di trasmissione.
3. Eventi della stessa famiglia e area.
4. Sorpresa o direzione documentata per il riferimento corretto.
5. Regime confrontabile e prezzi disponibili.
6. Esiti maturi e osservazioni di mercato non duplicate.

Registrare il motivo di esclusione permette di distinguere “manca una research” da “la research esiste ma mancano dati strutturati”, “il regime non è confrontabile” o “manca il consenso storico”. Le nuove ricerche, sempre commissionate dal maintainer, dovrebbero chiudere lacune ricorrenti di questo elenco. Aggiungere genericamente studi o ticker rischia di aumentare soltanto le possibilità di abbinamento debole.

## Ordine suggerito

1. Recupero controllato delle schede perse e validazione dell'ingestione futura.
2. Scorecard per coorti/versioni, riferimenti semplici e separazione fra descrizione e previsione; registrazione al momento della produzione.
3. Vincoli di pertinenza nel selettore, astensione esplicita e regime operativo sulle famiglie ricorrenti.
4. Correzione dell'identità degli eventi e delle etichette di sorpresa; copertura guidata dai motivi di esclusione.
5. Confronto prospettico del metodo precedente e di quello modificato sugli stessi casi, senza cambiare soglie dopo aver visto gli esiti.

I primi due passi rendono la misura interpretabile. I successivi possono migliorare il segnale, ma non garantiscono una percentuale di successo. Non scegliere come obiettivo soltanto un hit-rate maggiore: occorre misurare anche quante occasioni il sistema copre e su quali si astiene.

## Verifiche eseguite

- Riproduzione del difetto di intestazione su copia temporanea della scheda del 18 settembre.
- Riproduzione sintetica della fusione di due eventi della stessa area.
- Verifica delle etichette assegnate ai due esempi di CPI rispetto al consenso.
- Lettura del ledger e calcolo separato per periodo, uso e asset.
- Suite esistenti `test_forecast_tracking.py` e `test_analogues_events.py`: superate. Queste suite non coprono tutte le condizioni riprodotte sopra: il loro successo non invalida i difetti.

## Comando diagnostico riproducibile, in sola lettura

Eseguire dalla root `mercati_finanza/`. Non richiama `run`, `backfill`, `evaluate` o `build` e non scrive artefatti. I riferimenti sempre-su/sempre-giù sono controlli descrittivi sul medesimo sottoinsieme di righe con hit-rate, non strategie validate fuori campione.

```bash
PYTHONDONTWRITEBYTECODE=1 news_impact_pipeline/venv/bin/python - <<'PY'
import csv, re, sys
from collections import Counter
sys.path.insert(0, 'news_impact_pipeline')
import forecast_tracking as ft

cards = ft.discover_cards()
missed = []
for p in cards:
    tables = len(re.findall(r'^\|\s*Stat\s*\|.*T\+', p.read_text(), re.M))
    if tables and not ft.parse_card(p):
        missed.append((str(p.relative_to(ft.DAILY_DIR)), tables))
print('Schede totali:', len(cards))
print('Schede con tabelle Stat ma senza righe estratte:', len(missed))
print('Per mese:', Counter(p[:7] for p, _ in missed))
print('Casi recenti:', [(p, n) for p, n in missed if p >= '2026-09-15'])

with ft.LEDGER_PATH.open(newline='') as stream:
    all_rows = list(csv.DictReader(stream))
rows = [r for r in all_rows if r['realized_return']
        and r.get('uso') not in ('scenario', 'ritirata')]

def show(label, subset):
    h = [r for r in subset if r.get('hit_dir') not in ('', None)]
    c = [r for r in subset if r.get('in_iqr') not in ('', None)]
    def pct(values):
        return round(100 * sum(values) / len(values), 2) if values else None
    print(label, {
        'righe': len(subset),
        'schede': len({r['card_path'] for r in subset}),
        'giorni_emissione': len({r['made_date'] for r in subset}),
        'N_hit': len(h),
        'hit_pct': pct([int(r['hit_dir']) for r in h]),
        'sempre_su_pct': pct([float(r['realized_return']) > 0 for r in h]),
        'sempre_giu_pct': pct([float(r['realized_return']) < 0 for r in h]),
        'N_bande': len(c),
        'copertura_pct': pct([int(r['in_iqr']) for r in c]),
    })

show('Tutte le tabelle principali registrate', rows)
for start, end in [('2026-09-01', '2026-09-15'),
                   ('2026-09-15', '2026-09-23'),
                   ('2026-09-23', '9999-12-31')]:
    show(start + ' / ' + end,
         [r for r in rows if start <= r['made_date'] < end])
for usage in ['previsione', 'descrittiva', '']:
    show('uso=' + (usage or 'non dichiarato'),
         [r for r in rows if (r.get('uso') or '') == usage])
for asset in ['^GSPC', 'BZ=F', 'HO=F', '^VIX', '^FVX', 'EEM', 'SOXX']:
    show(asset, [r for r in rows if r['asset'] == asset])
print('Orizzonti recenti e maturazione:', Counter(
    (r['horizon'], bool(r['realized_return'])) for r in all_rows
    if r['made_date'] >= '2026-09-23'))
PY
```

Questi conteggi individuano schede interamente perse; non certificano che ogni scheda parzialmente riconosciuta sia stata acquisita completamente. Il passo di recupero deve controllare anche quel caso.
