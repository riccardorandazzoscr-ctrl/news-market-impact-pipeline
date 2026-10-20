# Prompt dell'anteprima settimanale (v1.3, 2026-10-19)

> Il job `com.riccardo.newsimpact.weeklypreview` (`run_weekly_preview.sh`) estrae da qui SOLO
> il blocco fra `=== PROMPT START/END ===` e sostituisce `{{WEEK_DIR}}` con la cartella della
> settimana. I numeri li calcola `weekly_preview.py build`; il modello scrive solo il testo, e
> `weekly_preview.py validate` rifiuta ogni cifra che non sta nelle tabelle.
>
> v1→v1.1 (17/10): bozza LinkedIn in inglese, con il campione dichiarato (da quando partono gli
> episodi, da dove si misura) e 3–6 hashtag; il commento resta in italiano.
> v1.1→v1.2 (17/10): il post dice cosa contiene il pool (riga «Pool» e composizione) e scrive
> i rendimenti dei Treasury in punti base.
> v1.2→v1.3 (19/10): commento più leggibile — si apre con cos'è l'evento, asset chiamati per
> nome, pochi numeri, paragrafi brevi (la pagina era troppo densa da leggere).

=== PROMPT START ===
Leggi `{{WEEK_DIR}}/tabelle.md`: è l'anteprima della settimana prossima. Per ogni evento ci
sono due scenari storici condizionali (verso `pos` e `neg` sull'asset di riferimento) con N,
la mediana del rendimento cumulato e la quota di casi positivi a T+1, T+3, T+5, T+10.

Scrivi un solo file, `{{WEEK_DIR}}/testo.md`, con una sezione per ogni evento con `stato: ok` e
nessun'altra, in questo formato esatto (titoli delle sezioni come qui, commento in italiano,
bozza in inglese):

## <id dell'evento, copiato dall'intestazione, per esempio 2026-10-29:us_pce>
### Commento
<100–150 parole, in due o tre paragrafi brevi, con il tono di una nota per un lettore curioso
ma non tecnico. Prima frase: cos'è l'appuntamento e perché conta, senza cifre. Poi, in parole
semplici, cosa distingue i due scenari: su quali asset la differenza è netta e dove i casi
passati dicono poco (pochi casi, scenario insufficiente, quota di positivi vicina al 50%).
Chiama gli asset per nome (il rame, lo yuan, le azioni dei mercati emergenti); il ticker solo
tra parentesi, e solo la prima volta. Al massimo due o tre cifre per paragrafo, arrotondate a
una decimale; non elencare tutti gli orizzonti, scegli quello che racconta meglio la differenza.
Niente formule tipo «T+3» nel testo: scrivi «dopo tre sedute».>
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
