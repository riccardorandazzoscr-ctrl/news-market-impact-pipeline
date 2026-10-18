# Anteprima settimanale dal calendario — design

Data: 2026-10-17 · Stato: in revisione del maintainer · Approccio scelto: A (Python per i numeri, modello per il testo)

## Perché

Oggi la knowledge base si usa solo in modo reattivo: le circa tre schede al giorno pescano gli
studi che le notizie del giorno richiamano. Il 2026-10-17 risultava che dei 36 studi 10 non sono
citati nell'ultimo mese e 4 mai, e che 19 degli 81 asset non compaiono nelle ultime 90 schede.
L'anteprima usa la libreria in modo **proattivo**: parte dagli eventi della settimana successiva,
non dalle notizie già uscite.

Serve a tre scopi, con lo stesso peso:
- **contenuti LinkedIn** preparati prima dell'evento;
- **studio**: cosa dicono gli analoghi storici sugli eventi in arrivo;
- **letture direzionali più affidabili**: ogni evento senza analoghi sufficienti diventa una
  lacuna dichiarata, che alimenta le revisioni direzionali.

È **statistica descrittiva, non previsione**. Il verso di un evento futuro non si conosce, quindi
per ogni evento si mostrano due scenari condizionali, uno per verso, ciascuno con N.

## Decisioni prese

| Tema | Scelta |
|---|---|
| Forma | report settimanale, domenica alle 18:00, sugli eventi da lunedì a venerdì successivi |
| Calendario | API FRED per i rilasci USA, più un file annuale delle riunioni delle banche centrali |
| Costruzione | Python deterministico per pool ed event study; `claude -p` solo per commento e bozze |
| Fuori dal primo giro | dati europei e asiatici minori (HICP, PMI, Tankan); richiamo giornaliero degli eventi del giorno dopo |

## Architettura

### Ingressi

**`news_impact_pipeline/calendario_banche_centrali.yaml`.** Si compila a mano una volta l'anno
dai calendari ufficiali. Una riga per riunione:

```yaml
meetings:
  - bank: boj                 # fed | ecb | boj | boe | pboc
    decision: 2026-10-30      # giorno dell'annuncio
    reaction_session: 2026-10-30   # prima seduta in cui reagiscono gli asset di riferimento
    time_local: "12:00 Asia/Tokyo"  # orario indicativo dell'annuncio
```

`reaction_session` è esplicito perché il fuso decide la seduta: la BoJ annuncia durante la seduta
di Tokyo, la Fed alle 14:00 di New York. Quando mancano meno di 60 giorni all'ultima riunione del
file, il job manda un avviso Telegram, al massimo uno al giorno.

**Rilasci USA da FRED.** Si usa l'endpoint delle date di rilascio, con le date future incluse, come
in `cpi_lab_auto.py`. Le riunioni Fed stanno nel file delle banche centrali: la release FOMC di
FRED (101) ha date giornaliere e non serve. Il primo giro copre CPI, Employment Situation (payroll), Personal Income
and Outlays (PCE), PIL e vendite al dettaglio. I `release_id` si verificano sull'API al momento
dell'implementazione e non si scrivono a memoria. L'ora è quella ufficiale, 08:30 New York, e la
seduta di reazione è lo stesso giorno.

**`news_impact_pipeline/anteprima_eventi.yaml`.** Una voce per tipo di evento, circa 15 voci:

```yaml
boj_decision:
  label: "Decisione Bank of Japan"
  theme: monetary_policy
  subthemes: [boj]
  match_all: false
  reference: JPY=X
  scenarios:
    pos: "accomodante rispetto alle attese (yen debole, USD/JPY su)"
    neg: "restrittiva rispetto alle attese (yen forte, USD/JPY giù)"
  assets: [JPY=X, 1482.T, ^N225, ^TNX]     # tutti presenti in category_asset_map.yaml
  match_query: "Bank of Japan decisione tassi yen"
```

Un evento del calendario senza voce nella tabella è un **errore esplicito** nel log e nel
report, non un salto silenzioso. Ogni ticker in `assets` e `reference` deve esistere nella
tabella `assets` del DB: lo controlla un test.

### `weekly_preview.py build [--week-of AAAA-MM-GG] [--as-of AAAA-MM-GG]`

È la parte deterministica e non usa nessun modello.

1. Raccoglie gli eventi della settimana da lunedì a venerdì successivi a `--week-of`, che di
   default è oggi.
2. Per ogni evento chiama `analogues.py find` due volte, con `--direction pos` e poi `neg`,
   riferiti a `reference`. Usa `--before` uguale a `--as-of`, che di default è oggi, così entrano
   solo episodi già noti (no look-ahead).
3. Su ciascun pool lancia `event_study.py` sugli asset dell'evento, a T+1, T+3, T+5 e T+10, con
   `--as-of`.
4. Cerca le 2 research più pertinenti con `pipeline_tools.py match "<match_query>"`.
5. Scrive in `weekly_preview/AAAA-Www/`:
   - `tabelle.json`: eventi, pool (date e N), statistiche per asset e orizzonte, research
     collegate;
   - `tabelle.md`: le stesse informazioni in forma leggibile, che il modello riceve in ingresso.

Le funzioni di `analogues.py` ed `event_study.py` si importano direttamente, senza subprocess, se
la loro interfaccia lo permette. Se non lo permette, si usano le CLI. Niente logica duplicata. Gli
indicatori calcolati non si persistono nel DB: le statistiche vivono solo nei file della
settimana.

**Onestà del campione (2026-10-17).** Ogni evento dichiara a parole cosa contiene il pool
(campo `pool` della mappa) e ogni scenario ne riporta la composizione calcolata (etichette
date-locali più frequenti), il periodo del campione e l'N minimo delle celle; lo stato segue
l'N minimo. Per `^TNX`, `^FVX`, `^TYX`, che quotano un rendimento, la variazione è in punti base.

**Soglie.** Con N<10 lo scenario è marcato «indicativo». Con N<5 in **entrambi** gli scenari
l'evento è «analoghi insufficienti»: niente tabelle, niente commento, niente bozza. Finisce nella
sezione «Lacune» del report con tema, asset di riferimento e N, nella stessa forma di «Lacune
emerse» delle giornate.

### `run_weekly_preview.sh`: il job launchd

Il plist si chiama `com.riccardo.newsimpact.weeklypreview` e diventa l'ottavo job. Gira ogni
ora con `RunAtLoad`, come il job CPI, perché `StartCalendarInterval` non recupera i run persi
a Mac spento. Lo script lavora solo dalla domenica alle 18:00 e, in ripresa, fino a martedì,
con i soli eventi da oggi in poi (corretto nel piano del 2026-10-17).

1. `attendi_rete.sh`, con `RETE_URL` impostato su FRED.
2. Se `weekly_preview/AAAA-Www/anteprima.html` esiste e passa la validazione, esce subito.
   Questo rende il job idempotente.
3. `weekly_preview.py build`.
4. Se ci sono eventi con analoghi sufficienti, `claude -p` su Opus 5.5. Prompt corto, versionato
   in `news_impact_pipeline/weekly_preview_prompt.md` ed estratto fra marcatori come per il brief.
   Il modello legge `tabelle.md` e scrive `testo.md` con:
   - per ogni evento un commento di 100–150 parole, che spiega cosa distingue i due scenari e
     dove gli analoghi sono deboli;
   - per ogni evento una bozza di post LinkedIn **in inglese** (deciso il 2026-10-17), che
     dichiara il campione (quanti episodi, da che anno a che anno, presi dalla nostra libreria e
     non da tutti i rilasci, rendimenti dalla chiusura del giorno dell'evento), chiude con N e con
     «Descriptive statistics, not a forecast.» e termina con 3–6 hashtag in inglese. Il commento
     resta in italiano.

   Il consumo si registra con `record_claude_usage.py`, come per gli altri job.
5. `weekly_preview.py validate`: ogni numero in `testo.md` deve comparire in `tabelle.json`, con
   la stessa formattazione o con un arrotondamento a una cifra decimale. Fanno eccezione date,
   orizzonti (T+n) e N.
6. `weekly_preview.py charts` (aggiunto il 2026-10-17): un PNG quadrato 1200×1200 per evento
   `ok`, in inglese, deterministico: mediana dei due scenari a T+1…T+10 per gli asset fissati in
   `chart` nella mappa (il primo è il riferimento), con N, periodo del campione, convenzione di
   misura e «Descriptive statistics, not a forecast». Poi `weekly_preview.py render` produce
   `anteprima.html` con i grafici incorporati, e i PNG partono su Telegram come file.
7. `send_telegram.sh`: invia un messaggio corto con gli eventi della settimana e il percorso del
   report.

### Il report

`anteprima.html` contiene, in ordine:
1. il calendario della settimana: giorno, ora di Roma, evento, stato degli analoghi;
2. per ogni evento:
   - due tabelle affiancate, una per scenario: per asset, mediana e quota di casi positivi a
     T+1, T+3, T+5 e T+10, con N;
   - il commento;
   - le research collegate;
3. la sezione «Lacune»;
4. le bozze LinkedIn, marcate come bozze da rivedere.

## Casi d'errore

| Caso | Comportamento |
|---|---|
| FRED non risponde dopo l'attesa della rete | esce senza report; riprova al run successivo |
| Calendario banche centrali in scadenza | avviso Telegram una volta al giorno, con un deduplicatore proprio (`cpi_lab_auto.py` è solo locale e non si importa) |
| Evento senza voce in `anteprima_eventi.yaml` | errore nel log e riga «non mappato» nel report; il resto procede |
| Run del modello fallito, o validatore che rifiuta | report con le sole tabelle; il Telegram lo dice e il log riporta il motivo |
| Nessun evento in settimana | Telegram breve, nessun run del modello |
| Rilancio nella stessa settimana | non rifà nulla se `anteprima.html` è valido |

## Test

`news_impact_pipeline/tests/test_weekly_preview.py`, offline e registrato in `run_tests.sh`:
- calendario: date FRED finte più file delle banche centrali finto → eventi della settimana
  giusta, con `reaction_session` rispettata;
- un evento non mappato produce un errore esplicito;
- ogni ticker di `anteprima_eventi.yaml` esiste nel DB;
- scenari su una libreria finta: N corretto, «indicativo» sotto 10, «insufficienti» sotto 5;
- validatore: rifiuta una cifra assente dalle tabelle, accetta date, T+n e N;
- no look-ahead: un episodio con data uguale o successiva ad `--as-of` non entra nel pool.

## Documentazione da aggiornare all'implementazione

- `references/routine_giornaliera.md`: riga del job, orario e ricarica.
- `CLAUDE.md` e `../CLAUDE.md`: da 7 a 8 job.
- `MEMORY.md`: un filone «Anteprima settimanale» (stato, decisioni, prossimo passo).
- `news_impact_pipeline/launchd/`: il plist versionato.

## Fuori perimetro (per ora)

- Dati europei e asiatici minori (HICP flash, PMI, Tankan): si aggiungono con una fonte
  verificata, non con la ricerca web.
- Il richiamo giornaliero degli eventi del giorno dopo nel report quotidiano.
- La strada 2 (tutti gli asset di una research in ogni scheda) e la strada 3 (le tabelle delle
  research come fonte di verso per asset): sono i passi successivi, ciascuno con il suo design.
