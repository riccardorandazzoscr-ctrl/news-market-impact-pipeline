# Prompt dell'anteprima settimanale (v1.2, 2026-10-17)

> Il job `com.riccardo.newsimpact.weeklypreview` (`run_weekly_preview.sh`) estrae da qui SOLO
> il blocco fra `=== PROMPT START/END ===` e sostituisce `{{WEEK_DIR}}` con la cartella della
> settimana. I numeri li calcola `weekly_preview.py build`; il modello scrive solo il testo, e
> `weekly_preview.py validate` rifiuta ogni cifra che non sta nelle tabelle.
>
> v1→v1.1 (17/10): bozza LinkedIn in inglese, con il campione dichiarato (da quando partono gli
> episodi, da dove si misura) e 3–6 hashtag; il commento resta in italiano.
> v1.1→v1.2 (17/10): il post dice cosa contiene il pool (riga «Pool» e composizione) e scrive
> i rendimenti dei Treasury in punti base.

=== PROMPT START ===
Leggi `{{WEEK_DIR}}/tabelle.md`: è l'anteprima della settimana prossima. Per ogni evento ci
sono due scenari storici condizionali (verso `pos` e `neg` sull'asset di riferimento) con N,
la mediana del rendimento cumulato e la quota di casi positivi a T+1, T+3, T+5, T+10.

Scrivi un solo file, `{{WEEK_DIR}}/testo.md`, con una sezione per ogni evento con `stato: ok` e
nessun'altra, in questo formato esatto (titoli delle sezioni come qui, commento in italiano,
bozza in inglese):

## <id dell'evento, copiato dall'intestazione, per esempio 2026-10-29:us_pce>
### Commento
<100–150 parole: cosa distingue i due scenari, su quali asset la differenza è netta e dove
gli analoghi sono deboli (N piccolo, scenario insufficiente, quota di positivi vicina al 50%).>
### Bozza LinkedIn
<IN ENGLISH, 120–200 words for a post: a hook on the upcoming event and the comparison between
the two scenarios with the figures from the table. It must say clearly what the sample is, so a
reader does not mistake it for the full history: how many past episodes, from which year to which
year (the «campione dal … al …» of each scenario), what the episodes are (use the «Pool» line
and the «composizione» counts: e.g. say "US inflation surprises, mostly CPI" rather than calling
them PCE releases), that they come from our own library rather than every past release, and that returns run from the close of the event day to n
sessions later (the event-day move itself is not included). Close with N (written as N=<number>)
and the exact sentence "Descriptive statistics, not a forecast." On the last line, 3 to 6
hashtags in English (e.g. #Fed #Inflation #Treasuries #Macro), no numbers in them.>

Regole:
- usa solo cifre presenti in `tabelle.md`, scritte come lì (puoi arrotondare a una cifra
  decimale) e con lo stesso segno; nessuna cifra nuova, nessun livello di prezzo, nessuna data
  che non sia nelle tabelle;
- niente raccomandazioni operative e nessuna previsione: sono analoghi storici;
- espandi ogni sigla al primo uso (in inglese nella bozza);
- le celle in «bp» sono punti base (variazioni del rendimento): scrivile così, mai in percentuale;
- non modificare altri file e non lanciare altri comandi oltre alla lettura e alla scrittura.

Alla fine rispondi con una riga: quante sezioni hai scritto.
=== PROMPT END ===
