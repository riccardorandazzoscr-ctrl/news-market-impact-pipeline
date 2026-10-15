# Sorprese d'inflazione negli Stati Uniti (CPI e PCE) e trasmissione a Treasury, dollaro, oro e azionario — regime ed episodi storici (2017–presente)

Nel campione documentato, una sorpresa sul CPI americano rispetto al consenso della vigilia ha mosso il rendimento del Treasury a 10 anni nella stessa direzione della sorpresa in 15 casi su 17 verificabili. Su 12 casi documentati, l'S&P 500 si è mosso in senso opposto alla sorpresa in 11 casi. Oro e dollaro, invece, hanno un segno che dipende dal regime e che non si può dare per scontato.

## §1 Sintesi esecutiva

Primo: a muovere i prezzi è la sorpresa sul **core m/m**, non il livello e non l'headline. Nel 2026 c'è stata una serie di stampe in cui l'headline, gonfiato dall'energia, era già allineato al consenso, e il mercato ha prezzato soltanto lo scarto del core. Il 2026-04-10 l'headline è uscito a +0,9% m/m come previsto e il core a +0,2% contro +0,3%.\[1\] Il 2026-10-14 l'headline è uscito a +0,6% come previsto e il core a +0,3% contro +0,2%: secondo il sondaggio Bloomberg citato da TheStreet, solo 11 economisti su 73 si aspettavano 0,3%.\[2\]\[3\]

Secondo: il canale tassi è direzionale e robusto. Le sorprese calde alzano i rendimenti, a partire dal segmento a 2 anni, e quelle fredde li abbassano. Dove il segno è stato contraddetto c'era quasi sempre un altro evento nella stessa seduta.

Terzo: il segno dell'azionario («good news is bad news») e quello dell'oro (canale dei tassi reali) valgono nei regimi in cui la Fed reagisce all'inflazione: 2022–2023, 2024 e 2026. Non valgono nella fase «transitorio» del 2021, quando l'oro è salito su un CPI caldo, né, per l'oro, nel 2025, quando il metallo era guidato da fattori estranei ai tassi.

Quarto: il PCE porta poca informazione nuova. Solo due release PCE del campione hanno una sorpresa documentata, e una delle due ha un consenso conteso fra fonti.

**Dove l'event study è affidabile:** per segno e ordine di grandezza della reazione di `^TNX`, `IEF` e, in misura minore, `DX-Y.NYB` a T+1, nelle sedute senza FOMC, payroll o shock tariffari. **Dove non lo è:** per l'oro nei regimi 2021 e 2025, per gli orizzonti T+5/T+10, che nel 2022 e nel 2026 sono dominati dal drift dei rendimenti e da Fed, energia e guerra, e per qualunque statistica su `JPY=X`, `EURUSD=X` e `^MOVE`, per cui il campione documentato è praticamente vuoto.

## §2 Tassonomia dei canali di trasmissione

**Canale tassi Fed (direzionale).** La catena è: sorpresa sul core CPI → riprezzamento del percorso dei Fed Funds → rendimento a 2 anni → rendimento a 5 e 10 anni → prezzo dei Treasury. È il canale primario e il più pulito, con la risposta concentrata sul tratto breve. Il 2024-04-10 il 2 anni è salito di 22 pb, al 4,969%, e il 10 anni di oltre 18 pb, al 4,548% (CNBC). Il 2026-10-14 il 2 anni è salito fino a 16 pb in seduta, al 4,95% (Bloomberg), mentre le probabilità di un rialzo a ottobre passavano da circa il 20% al 46% secondo Bloomberg (dal 22% al 44% secondo i dati CME FedWatch citati da Axios). Proxy: `^FVX`, `^TNX`, `IEF` e, per la coda lunga, `^TYX`. Il 2 anni e i future sui Fed Funds o SOFR non sono nel database: li si nomina solo nelle Note.

**Canale dollaro (direzionale).** La catena è: sorpresa → differenziale di tassi a breve USA contro area euro e Giappone → flussi di carry → dollaro. Una sorpresa calda porta `DX-Y.NYB` pos, `EURUSD=X` neg e `JPY=X` pos. Il canale funziona quando la sorpresa sposta il 2 anni e si indebolisce quando il rialzo dei rendimenti viene dal premio a termine, come nel 2026: secondo Schwab, a inizio ottobre il term premium a 10 anni era ai massimi da oltre un decennio.\[2\] Il 2026-10-14 l'indice del dollaro è salito dello 0,69% a 102,90, massimo da aprile 2025 secondo FXStreet.

**Canale tassi reali sull'oro (redistributivo rispetto ai Treasury).** La catena è: sorpresa calda → rendimento reale (TIPS) su più del breakeven → costo opportunità dell'oro su → `GC=F` giù. È redistributivo perché, in un regime credibile, muove oro e rendimenti in direzioni opposte. Il segno si inverte quando il mercato legge la sorpresa come «Fed dietro la curva»: sale il breakeven e scende il tasso reale. È successo il 2021-11-10, con l'oro ai massimi da cinque mesi dopo un CPI al 6,2% contro il 5,8% atteso.\[4\] Nel 2026 il canale è tornato ortodosso: secondo un'analisi su Investing.com il tasso reale a 10 anni è salito in 12 mesi da circa 1,80% a circa 2,91%, e il future COMEX ha chiuso a 4.191 dollari, oltre il 21% sotto il picco di 5.318,40 del 29 gennaio 2026.\[5\] Il 2026-10-14 l'oro è sceso fino a 4.073,41 dollari.\[6\]

**Canale azionario (dipendente dal regime).** La catena è: sorpresa calda → tasso di sconto e percorso Fed → multipli, soprattutto sulla duration lunga di `^NDX` e sul costo del debito di `IWM` → `^GSPC` giù. Con la Fed in stretta o in attesa di tagliare vale «good news is bad news»: il 2022-09-13, con il core a +0,6% contro +0,3%, l'S&P 500 ha perso il 4,3% e il Nasdaq Composite oltre il 5%.\[7\] In regime di bassa attenzione il segno è indeterminato.

**Volatilità dei tassi (amplificatore).** La catena è: sorpresa grande in qualunque verso → incertezza sul percorso Fed → `^MOVE` su → reazioni più ampie negli altri canali, senza cambiarne il segno. Nessuna fonte consultata documenta il MOVE nelle date del catalogo, per cui `^MOVE` non compare in tabella.

**Canale energetico (amplificatore e confondente nel 2026).** La catena è: shock petrolifero → headline CPI → consenso già aggiornato → sorpresa concentrata sul core. Nel 2026 l'energia ha alzato l'headline atteso, ma il mercato ha reagito al core.\[8\]

## §3 Catalogo di episodi-ancora datati

| Data | Asset | Verso | Meccanismo | Evento | Note |
|---|---|---|---|---|---|
| 2017-04-17 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI marzo 2017 −0,3% m/m contro +0,2% atteso; core −0,1% m/m\[9\] | Uscito il 2017-04-14, Venerdì Santo (NYSE e cash Treasury chiusi, SIFMA): prima seduta utile 2017-04-17. Consenso: CNBC (Barclays). Weekend con tensioni geopolitiche: attribuzione debole\[10\] |
| 2017-04-17 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI marzo 2017 −0,3% m/m contro +0,2% atteso | Seduta spostata per il Venerdì Santo |
| 2017-04-17 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI marzo 2017 −0,3% m/m contro +0,2% atteso | Bassa attenzione: ampiezza attesa piccola |
| 2017-04-17 | GC=F | pos, neg | inflation_print, us_cpi, inflation_downside | CPI marzo 2017 −0,3% m/m contro +0,2% atteso | Oro dominato dal rischio geopolitico |
| 2017-04-17 | ^GSPC | pos, neg | inflation_print, us_cpi, inflation_downside | CPI marzo 2017 −0,3% m/m contro +0,2% atteso | Bassa attenzione: verso ambiguo |
| 2018-02-14 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2018 +0,5% m/m contro +0,3% atteso; core +0,3% contro +0,2% | Consenso: Reuters. 10 anni al massimo da quattro anni (Reuters via Business Standard). Dopo lo shock salariale del 2 febbraio\[11\] |
| 2018-02-14 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI gennaio 2018 +0,5% m/m contro +0,3% atteso; core +0,3% contro +0,2% | Core m/m più alto dal 2005 (First Trust)\[12\] |
| 2018-02-14 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI gennaio 2018 +0,5% m/m contro +0,3% atteso | Fase di dollaro debole: osservato può divergere |
| 2018-02-14 | GC=F | pos, neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2018 +0,5% m/m contro +0,3% atteso | Oro guidato dal dollaro debole |
| 2018-02-14 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2018 +0,5% m/m contro +0,3% atteso | Chiusura non verificata |
| 2019-06-12 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI maggio 2019 +1,8% a/a contro +1,9% atteso; headline +0,1% m/m in linea; core +0,1% m/m | Consenso headline: Reuters; consenso core m/m non nel testo. Rendimenti in calo (Reuters/CNBC). FOMC del 18-19 giugno entro T+5\[13\]\[14\] |
| 2019-06-12 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI maggio 2019 +1,8% a/a contro +1,9% atteso | Rendimenti scesi (Reuters)\[13\] |
| 2019-06-12 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI maggio 2019 +1,8% a/a contro +1,9% atteso | Reazione non documentata |
| 2019-06-12 | GC=F | pos, neg | inflation_print, us_cpi, inflation_downside | CPI maggio 2019 +1,8% a/a contro +1,9% atteso | Oro guidato da attese di taglio e guerra commerciale |
| 2019-06-12 | ^GSPC | pos, neg | inflation_print, us_cpi, inflation_downside | CPI maggio 2019 +1,8% a/a contro +1,9% atteso | Bassa attenzione |
| 2019-07-11 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI giugno 2019 core +0,3% m/m contro +0,2% atteso; core +2,1% a/a contro 2,0%; headline +0,1% contro 0,0% | Consenso: FXStreet. Stessa seduta: testimonianza di Powell al Senato\[15\] |
| 2019-07-11 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI giugno 2019 core +0,3% m/m contro +0,2% atteso | Attribuzione parziale |
| 2019-07-11 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI giugno 2019 core +0,3% m/m contro +0,2% atteso | DXY rimbalzato verso 97 (FXStreet)\[15\] |
| 2019-07-11 | GC=F | pos, neg | inflation_print, us_cpi, inflation_upside | CPI giugno 2019 core +0,3% m/m contro +0,2% atteso | Taglio di luglio già prezzato |
| 2019-07-11 | ^GSPC | pos, neg | inflation_print, us_cpi, inflation_upside | CPI giugno 2019 core +0,3% m/m contro +0,2% atteso | Bassa attenzione |
| 2021-11-10 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI ottobre 2021 +0,9% m/m contro +0,5% atteso; +6,2% a/a contro 5,8%; core +0,6% contro +0,4%\[16\] | Consenso: Econoday (CNBC: core +0,4%). Rendimenti in rialzo (CNBC). Stessa giornata: asta del 30 anni\[16\]\[17\] |
| 2021-11-10 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI ottobre 2021 +6,2% a/a contro 5,8% atteso | — |
| 2021-11-10 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI ottobre 2021 +6,2% a/a contro 5,8% atteso | Probabilità di rialzo a giugno 2022 al 46% circa (Forex.com)\[4\] |
| 2021-11-10 | GC=F | pos, neg | inflation_print, us_cpi, inflation_upside | CPI ottobre 2021 +6,2% a/a contro 5,8% atteso | Regime «transitorio»: oro ai massimi da cinque mesi (Forex.com)\[4\] |
| 2021-11-10 | ^GSPC | pos, neg | inflation_print, us_cpi, inflation_upside | CPI ottobre 2021 +6,2% a/a contro 5,8% atteso | Futures in calo (CNBC), attesa ambigua\[16\] |
| 2022-02-10 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2022 +0,6% m/m contro +0,4% atteso; +7,5% a/a contro 7,2%; core +0,6% contro +0,4%, 6,0% contro 5,9%\[18\] | Consenso: Dow Jones (CNBC). Stessa mattina: sussidi (223k contro 230k).\[18\] Dopo la chiusura Bullard chiede 100 pb entro luglio: contamina T+1 |
| 2022-02-10 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI gennaio 2022 +7,5% a/a contro 7,2% atteso | Chiusura sopra il 2% non verificata |
| 2022-02-10 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI gennaio 2022 +7,5% a/a contro 7,2% atteso | — |
| 2022-02-10 | GC=F | pos, neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2022 +7,5% a/a contro 7,2% atteso | Tensioni Russia-Ucraina: rifugio confondente |
| 2022-02-10 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2022 +7,5% a/a contro 7,2% atteso | — |
| 2022-05-11 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI aprile 2022 +0,3% m/m contro +0,2% atteso; +8,3% a/a contro 8,1%; core +0,6% contro +0,4%\[19\] | Consenso: Dow Jones (CNBC). Futures da Dow +280 a −105 (Zacks).\[20\] 10 anni forse in calo per fuga verso la qualità (non verificato) |
| 2022-05-11 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI aprile 2022 core +0,6% m/m contro +0,4% atteso | Osservato forse opposto all'attesa |
| 2022-05-11 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI aprile 2022 core +0,6% m/m contro +0,4% atteso | Reazione non documentata |
| 2022-05-11 | GC=F | neg | inflation_print, us_cpi, inflation_upside | CPI aprile 2022 core +0,6% m/m contro +0,4% atteso | — |
| 2022-05-11 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI aprile 2022 core +0,6% m/m contro +0,4% atteso | Futures girati in negativo (Zacks)\[20\] |
| 2022-07-13 | IEF | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI giugno 2022 +1,3% m/m contro +1,1% atteso; +9,1% a/a contro 8,8%; core +0,7% contro +0,5%\[21\] | Consenso: Dow Jones (CNBC). Stessa seduta: Bank of Canada +100 pb e Beige Book |
| 2022-07-13 | ^TNX | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI giugno 2022 +9,1% a/a contro 8,8% atteso | — |
| 2022-07-13 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI giugno 2022 +9,1% a/a contro 8,8% atteso | Drift rialzista del dollaro 2022 |
| 2022-07-13 | GC=F | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI giugno 2022 +9,1% a/a contro 8,8% atteso | — |
| 2022-07-13 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI giugno 2022 +9,1% a/a contro 8,8% atteso | — |
| 2022-09-13 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI agosto 2022 +0,1% m/m contro −0,1% atteso; core +0,6% contro +0,3% | Consenso: Dow Jones (NBC News). FOMC del 20-21 settembre entro T+10\[7\] |
| 2022-09-13 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI agosto 2022 core +0,6% m/m contro +0,3% atteso | — |
| 2022-09-13 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI agosto 2022 core +0,6% m/m contro +0,3% atteso | — |
| 2022-09-13 | GC=F | neg | inflation_print, us_cpi, inflation_upside | CPI agosto 2022 core +0,6% m/m contro +0,3% atteso | — |
| 2022-09-13 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI agosto 2022 core +0,6% m/m contro +0,3% atteso | S&P 500 −4,3%, Dow −1.276 punti (NBC News)\[7\] |
| 2022-09-13 | ^NDX | neg | inflation_print, us_cpi, inflation_upside | CPI agosto 2022 core +0,6% m/m contro +0,3% atteso | Fonte sul Nasdaq Composite (oltre −5%), non sul Nasdaq-100\[7\] |
| 2022-11-10 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI ottobre 2022 +0,4% m/m contro +0,5% atteso; +7,7% a/a contro 7,9%; core +0,3% contro +0,5%, 6,3% contro 6,5%\[22\] | Consenso: Bloomberg (Yahoo Finance). Rendimenti «in caduta», azioni in forte rialzo (Yahoo Finance)\[22\]\[23\] |
| 2022-11-10 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI ottobre 2022 core +0,3% m/m contro +0,5% atteso | — |
| 2022-11-10 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI ottobre 2022 core +0,3% m/m contro +0,5% atteso | — |
| 2022-11-10 | GC=F | pos | inflation_print, us_cpi, inflation_downside | CPI ottobre 2022 core +0,3% m/m contro +0,5% atteso | — |
| 2022-11-10 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI ottobre 2022 core +0,3% m/m contro +0,5% atteso | — |
| 2022-12-13 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI novembre 2022 +0,1% m/m contro +0,3% atteso; core +0,2% contro +0,3% | Consenso e reazione: Schwab via Benzinga. Prima giornata del FOMC del 13-14 dicembre\[24\] |
| 2022-12-13 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI novembre 2022 core +0,2% m/m contro +0,3% atteso | −12 pb al 3,48% subito dopo il dato; 2 anni −16 pb al 4,23% (Schwab via Benzinga) |
| 2022-12-13 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI novembre 2022 core +0,2% m/m contro +0,3% atteso | DXY sotto 104 per la prima volta da fine giugno\[24\] |
| 2022-12-13 | GC=F | pos | inflation_print, us_cpi, inflation_downside | CPI novembre 2022 core +0,2% m/m contro +0,3% atteso | — |
| 2022-12-13 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI novembre 2022 core +0,2% m/m contro +0,3% atteso | Futures in rialzo\[24\] |
| 2023-07-12 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI giugno 2023 +0,2% m/m contro +0,3% atteso; +3,0% a/a contro 3,1%; core sotto le attese\[25\] | Consenso: Seeking Alpha; consenso numerico del core non nel testo. Rialzo Fed del 26 luglio entro T+10 |
| 2023-07-12 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI giugno 2023 +3,0% a/a contro 3,1% atteso | — |
| 2023-07-12 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI giugno 2023 +3,0% a/a contro 3,1% atteso | — |
| 2023-07-12 | GC=F | pos | inflation_print, us_cpi, inflation_downside | CPI giugno 2023 +3,0% a/a contro 3,1% atteso | — |
| 2023-07-12 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI giugno 2023 +3,0% a/a contro 3,1% atteso | — |
| 2023-09-13 | IEF | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2023 core +0,3% m/m contro +0,2% atteso; headline +0,6% in linea, 3,7% a/a contro 3,6%\[26\] | Consenso: Dow Jones (CNBC). Rendimenti «più alti su tutta la curva» (CNBC). Rialzo a novembre circa 44% (CME)\[26\] |
| 2023-09-13 | ^TNX | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2023 core +0,3% m/m contro +0,2% atteso | — |
| 2023-09-13 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2023 core +0,3% m/m contro +0,2% atteso | Reazione non documentata |
| 2023-09-13 | GC=F | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2023 core +0,3% m/m contro +0,2% atteso | — |
| 2023-09-13 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2023 core +0,3% m/m contro +0,2% atteso | Osservato: SPY +0,1%, QQQ +0,4% (Benzinga). Attesa smentita: pausa già prezzata\[27\] |
| 2023-11-14 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI ottobre 2023 headline invariato; core +0,2% m/m contro +0,3% atteso, 4,0% a/a contro 4,1% | Consenso: Bloomberg (Yahoo Finance); consenso headline non nel testo\[28\] |
| 2023-11-14 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI ottobre 2023 core +0,2% m/m contro +0,3% atteso | — |
| 2023-11-14 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI ottobre 2023 core +0,2% m/m contro +0,3% atteso | — |
| 2023-11-14 | GC=F | pos | inflation_print, us_cpi, inflation_downside | CPI ottobre 2023 core +0,2% m/m contro +0,3% atteso | — |
| 2023-11-14 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI ottobre 2023 core +0,2% m/m contro +0,3% atteso | — |
| 2024-02-13 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2024 +0,3% m/m contro +0,2% atteso; +3,1% a/a contro 2,9%; core +0,4% contro +0,3%, 3,9% contro 3,7%\[29\] | Consenso: Dow Jones (CNBC); FactSet concorde (CNN). Rendimenti «in forte rialzo» (CNBC). Rimbalzo il giorno dopo (Zacks)\[29\]\[30\]\[31\] |
| 2024-02-13 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI gennaio 2024 core +0,4% m/m contro +0,3% atteso | — |
| 2024-02-13 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI gennaio 2024 core +0,4% m/m contro +0,3% atteso | — |
| 2024-02-13 | GC=F | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2024 core +0,4% m/m contro +0,3% atteso | — |
| 2024-02-13 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI gennaio 2024 core +0,4% m/m contro +0,3% atteso | Dow −525 punti (−1,4%), calo più ampio da marzo 2023 (CNN)\[30\] |
| 2024-03-12 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI febbraio 2024 +0,4% m/m in linea; +3,2% a/a contro 3,1% atteso; core +0,4% contro +0,3%, 3,8% contro 3,7%\[32\] | Consenso: Benzinga. 2 anni «sostanzialmente invariato» al 4,55%: reazione smorzata\[32\] |
| 2024-03-12 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI febbraio 2024 core +0,4% m/m contro +0,3% atteso | Osservato quasi piatto |
| 2024-03-12 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI febbraio 2024 core +0,4% m/m contro +0,3% atteso | DXY in lieve rialzo (Benzinga)\[32\] |
| 2024-03-12 | GC=F | neg | inflation_print, us_cpi, inflation_upside | CPI febbraio 2024 core +0,4% m/m contro +0,3% atteso | — |
| 2024-03-12 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI febbraio 2024 core +0,4% m/m contro +0,3% atteso | Osservato non verificato |
| 2024-04-10 | IEF | neg | inflation_print, us_cpi, inflation_upside | CPI marzo 2024 +0,4% m/m contro +0,3% atteso; +3,5% a/a contro 3,4%; core +0,4% contro +0,3%, 3,8% contro 3,7%\[33\] | Consenso: Dow Jones (CNBC) e FactSet (Benzinga dà core 3,7% «in linea»: si adotta CNBC). 2 anni +22 pb al 4,969%, 10 anni +18 pb al 4,548% (CNBC). Verbali FOMC alle 14:00 |
| 2024-04-10 | ^TNX | pos | inflation_print, us_cpi, inflation_upside | CPI marzo 2024 core +0,4% m/m contro +0,3% atteso | Primo taglio spostato da giugno a settembre (CNBC)\[33\] |
| 2024-04-10 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside | CPI marzo 2024 core +0,4% m/m contro +0,3% atteso | Rialzo di circa l'1% non verificato |
| 2024-04-10 | GC=F | neg | inflation_print, us_cpi, inflation_upside | CPI marzo 2024 core +0,4% m/m contro +0,3% atteso | Acquisti delle banche centrali: drift confondente |
| 2024-04-10 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside | CPI marzo 2024 core +0,4% m/m contro +0,3% atteso | S&P 500 −1,0% a 5.160,64 (Zacks)\[34\] |
| 2024-05-15 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI aprile 2024 +0,3% m/m contro +0,4% atteso; a/a 3,4% in linea; core +0,3% e 3,6% in linea\[35\] | Consenso: Benzinga. Sorpresa solo sull'headline m/m. Stessa mattina: vendite al dettaglio deboli, stesso segno. 2 anni al 4,72%\[35\]\[36\] |
| 2024-05-15 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI aprile 2024 +0,3% m/m contro +0,4% atteso | Rendimenti in calo (Benzinga)\[35\] |
| 2024-05-15 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI aprile 2024 +0,3% m/m contro +0,4% atteso | Dollaro in calo (Benzinga)\[35\] |
| 2024-05-15 | GC=F | pos | inflation_print, us_cpi, inflation_downside | CPI aprile 2024 +0,3% m/m contro +0,4% atteso | — |
| 2024-05-15 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI aprile 2024 +0,3% m/m contro +0,4% atteso | Futures in rialzo (Benzinga)\[35\] |
| 2024-05-31 | IEF | pos, neg | inflation_print, inflation_downside | PCE aprile 2024 core +0,2% m/m contro +0,3% atteso (FactSet/investingLive); headline +0,3% e 2,7% in linea | Consenso conteso: FactSet e investingLive 0,3%, Dow Jones (CNBC) 0,2%. Core non arrotondato 0,249%, ricostruibile da CPI e PPI. 10 anni −5 pb al 4,501% (CNBC)\[37\]\[38\]\[39\] |
| 2024-05-31 | ^TNX | pos, neg | inflation_print, inflation_downside | PCE aprile 2024 core +0,2% m/m contro +0,3% atteso (FactSet) | Sorpresa dipendente dalla fonte |
| 2024-05-31 | DX-Y.NYB | pos, neg | inflation_print, inflation_downside | PCE aprile 2024 core +0,2% m/m contro +0,3% atteso (FactSet) | Come sopra |
| 2024-05-31 | GC=F | pos, neg | inflation_print, inflation_downside | PCE aprile 2024 core +0,2% m/m contro +0,3% atteso (FactSet) | Come sopra |
| 2024-05-31 | ^GSPC | pos, neg | inflation_print, inflation_downside | PCE aprile 2024 core +0,2% m/m contro +0,3% atteso (FactSet) | Futures in rialzo (CNBC)\[40\] |
| 2024-07-11 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI giugno 2024 −0,1% m/m; +3,0% a/a contro 3,1% atteso; core +0,1% contro +0,2%\[41\] | Consenso: TradingEconomics via Benzinga\[42\] |
| 2024-07-11 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI giugno 2024 core +0,1% m/m contro +0,2% atteso | −10 pb al 4,18% (Benzinga)\[42\] |
| 2024-07-11 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI giugno 2024 core +0,1% m/m contro +0,2% atteso | Reazione non documentata |
| 2024-07-11 | GC=F | pos | inflation_print, us_cpi, inflation_downside | CPI giugno 2024 core +0,1% m/m contro +0,2% atteso | — |
| 2024-07-11 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI giugno 2024 core +0,1% m/m contro +0,2% atteso | Futures in rialzo\[42\] |
| 2025-05-13 | IEF | pos | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI aprile 2025 headline e core +0,2% m/m contro +0,3% atteso\[43\] | Consenso: J.P. Morgan. Primo CPI dopo i dazi del 2 aprile. Tregua USA-Cina del 2025-05-12: T+1…T+10 contaminati |
| 2025-05-13 | ^TNX | neg | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI aprile 2025 core +0,2% m/m contro +0,3% atteso | — |
| 2025-05-13 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI aprile 2025 core +0,2% m/m contro +0,3% atteso | — |
| 2025-05-13 | GC=F | pos, neg | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI aprile 2025 core +0,2% m/m contro +0,3% atteso | Oro 2025 guidato da domanda ufficiale e dazi |
| 2025-05-13 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI aprile 2025 core +0,2% m/m contro +0,3% atteso | — |
| 2025-08-12 | IEF | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8% atteso; core 3,1% a/a contro 3,0%; m/m in linea | Consenso: FactSet (Morningstar), Dow Jones (CNBC). Headline e core opposti; taglio di settembre dall'84% al 90% (CME via CoinDesk); 10 anni −3 pb al 4,26%\[44\]\[45\] |
| 2025-08-12 | ^TNX | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8%; core 3,1% contro 3,0% | Sorpresa mista |
| 2025-08-12 | DX-Y.NYB | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8%; core 3,1% contro 3,0% | Dollaro in lieve calo (CoinDesk)\[45\] |
| 2025-08-12 | GC=F | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8%; core 3,1% contro 3,0% | Sorpresa mista |
| 2025-08-12 | ^GSPC | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8%; core 3,1% contro 3,0% | Futures +0,6% (Benzinga)\[46\] |
| 2025-08-12 | ^NDX | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8%; core 3,1% contro 3,0% | Futures +0,8% (Benzinga)\[46\] |
| 2025-08-12 | IWM | pos, neg | inflation_print, us_cpi, inflation_upside, inflation_downside, tariff_escalation | CPI luglio 2025: headline 2,7% a/a contro 2,8%; core 3,1% contro 3,0% | Russell 2000 futures +1,5% (Benzinga)\[46\] |
| 2025-10-24 | IEF | pos | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI settembre 2025 +0,3% m/m contro +0,4% atteso; 3,0% a/a contro 3,1%; core +0,2% contro +0,3%, 3,0% contro 3,1% | Consenso: FactSet (Morningstar). Release spostata dal 2025-10-15 al 2025-10-24 per lo shutdown; seduta aperta. FOMC del 28-29 ottobre entro T+3\[47\]\[48\]\[49\] |
| 2025-10-24 | ^TNX | neg | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI settembre 2025 core +0,2% m/m contro +0,3% atteso | Unico dato ufficiale durante lo shutdown\[50\] |
| 2025-10-24 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI settembre 2025 core +0,2% m/m contro +0,3% atteso | — |
| 2025-10-24 | GC=F | pos, neg | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI settembre 2025 core +0,2% m/m contro +0,3% atteso | Regime 2025 dell'oro |
| 2025-10-24 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside, tariff_escalation | CPI settembre 2025 core +0,2% m/m contro +0,3% atteso | — |
| 2026-02-13 | IEF | pos | inflation_print, us_cpi, inflation_downside | CPI gennaio 2026 +0,2% m/m contro +0,3% atteso; 2,4% a/a contro 2,5%; core +0,3% e 2,5% in linea\[51\] | Consenso: Dow Jones (CNBC) e Forex.com. Release ritardata per lo shutdown parziale; seduta aperta. 2 anni −6 pb al 3,406% (CNBC)\[52\]\[53\] |
| 2026-02-13 | ^TNX | neg | inflation_print, us_cpi, inflation_downside | CPI gennaio 2026 2,4% a/a contro 2,5% atteso | −5 pb al 4,05% (CNBC)\[52\] |
| 2026-02-13 | ^TYX | neg | inflation_print, us_cpi, inflation_downside | CPI gennaio 2026 2,4% a/a contro 2,5% atteso | −3 pb al 4,695% (CNBC)\[52\] |
| 2026-02-13 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside | CPI gennaio 2026 2,4% a/a contro 2,5% atteso | Reazione non documentata |
| 2026-02-13 | GC=F | pos, neg | inflation_print, us_cpi, inflation_downside | CPI gennaio 2026 2,4% a/a contro 2,5% atteso | Oro post-picco del 29 gennaio: drift dominante |
| 2026-02-13 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside | CPI gennaio 2026 2,4% a/a contro 2,5% atteso | Futures poco mossi (CNBC)\[51\] |
| 2026-04-10 | IEF | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI marzo 2026: headline +0,9% m/m e 3,3% a/a in linea; core +0,2% contro +0,3%, 2,6% contro 2,7%\[1\] | Consenso: Dow Jones (CNBC). Benzina +21,2% m/m. Osservato contro l'attesa: 10 anni +2 pb al 4,321% (CNBC). Alle 10:00 Michigan: attese a 1 anno 4,8% dal 3,8%\[1\]\[54\] |
| 2026-04-10 | ^TNX | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI marzo 2026 core +0,2% m/m contro +0,3% atteso | Attesa smentita |
| 2026-04-10 | ^TYX | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI marzo 2026 core +0,2% m/m contro +0,3% atteso | 30 anni al 4,913% (CNBC)\[1\] |
| 2026-04-10 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI marzo 2026 core +0,2% m/m contro +0,3% atteso | Reazione non documentata |
| 2026-04-10 | GC=F | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI marzo 2026 core +0,2% m/m contro +0,3% atteso | — |
| 2026-04-10 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI marzo 2026 core +0,2% m/m contro +0,3% atteso | Futures in lieve rialzo (CNBC)\[54\] |
| 2026-05-12 | IEF | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI aprile 2026 +0,6% m/m in linea; 3,8% a/a contro 3,7%; core +0,4% contro +0,3%, 2,8% contro 2,7%\[55\]\[56\] | Consenso: Dow Jones (CNBC), FactSet/Kiplinger, Investing.com. Rendimenti in rialzo, futures negativi (CNBC)\[56\]\[57\]\[58\] |
| 2026-05-12 | ^TNX | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI aprile 2026 core +0,4% m/m contro +0,3% atteso | 10 anni sopra il 4,45% (fonte secondaria debole)\[59\] |
| 2026-05-12 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI aprile 2026 core +0,4% m/m contro +0,3% atteso | Reazione non documentata |
| 2026-05-12 | GC=F | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI aprile 2026 core +0,4% m/m contro +0,3% atteso | — |
| 2026-05-12 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI aprile 2026 core +0,4% m/m contro +0,3% atteso | Futures negativi (CNBC)\[56\] |
| 2026-05-28 | IEF | pos | inflation_print, inflation_downside, energy_passthrough | PCE aprile 2026 +0,4% m/m contro +0,5% atteso; core +0,2% contro +0,3%; a/a in linea (3,8% e 3,3%) | Consenso: Dow Jones (CNBC); FactSet core +0,30% (Morningstar). Perché ha sorpreso: core non arrotondato poi rivisto a 0,24% (Morningstar), sotto la traduzione CPI/PPI; causa per componente non documentata\[60\]\[61\]\[62\] |
| 2026-05-28 | ^TNX | neg | inflation_print, inflation_downside, energy_passthrough | PCE aprile 2026 core +0,2% m/m contro +0,3% atteso | Rendimenti in lieve calo (CNBC)\[60\] |
| 2026-05-28 | DX-Y.NYB | neg | inflation_print, inflation_downside, energy_passthrough | PCE aprile 2026 core +0,2% m/m contro +0,3% atteso | Reazione non documentata |
| 2026-05-28 | GC=F | pos | inflation_print, inflation_downside, energy_passthrough | PCE aprile 2026 core +0,2% m/m contro +0,3% atteso | — |
| 2026-05-28 | ^GSPC | pos | inflation_print, inflation_downside, energy_passthrough | PCE aprile 2026 core +0,2% m/m contro +0,3% atteso | Altre release della mattina non verificate |
| 2026-06-10 | IEF | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI maggio 2026 +0,5% m/m e 4,2% a/a in linea; core +0,2% contro +0,3%, 2,9% a/a in linea\[63\] | Consenso: FactSet (Morningstar). Picco headline 2026. Notizie sull'Iran nella stessa seduta (fonte secondaria)\[63\]\[64\] |
| 2026-06-10 | ^TNX | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI maggio 2026 core +0,2% m/m contro +0,3% atteso | 2 anni al 4,13% (CM Elite)\[65\] |
| 2026-06-10 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI maggio 2026 core +0,2% m/m contro +0,3% atteso | Dollaro in calo (TickerSpark via Admirals)\[8\] |
| 2026-06-10 | GC=F | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI maggio 2026 core +0,2% m/m contro +0,3% atteso | Oro «tira il fiato» (Kitco)\[66\] |
| 2026-06-10 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI maggio 2026 core +0,2% m/m contro +0,3% atteso | Recupero intraday (Bitget, fonte debole)\[67\] |
| 2026-07-14 | IEF | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI giugno 2026 −0,4% m/m (benzina −9,7%); core 0,0% m/m contro +0,2% atteso\[68\]\[69\] | Consenso core: CBCAL; consenso headline m/m non documentato. 2 anni −7 pb al 4,185% (FinanceCalendar)\[68\]\[70\] |
| 2026-07-14 | ^TNX | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI giugno 2026 core 0,0% m/m contro +0,2% atteso | −2 pb al 4,583%\[70\] |
| 2026-07-14 | DX-Y.NYB | neg | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI giugno 2026 core 0,0% m/m contro +0,2% atteso | Reazione non documentata |
| 2026-07-14 | GC=F | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI giugno 2026 core 0,0% m/m contro +0,2% atteso | — |
| 2026-07-14 | ^GSPC | pos | inflation_print, us_cpi, inflation_downside, energy_passthrough | CPI giugno 2026 core 0,0% m/m contro +0,2% atteso | — |
| 2026-09-11 | IEF | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2026 +0,4% m/m in linea; core +0,3% contro +0,2% atteso; core 2,4% a/a in linea\[8\] | Consenso: TradingEconomics e Admirals. Rialzo a settembre da 70% a quasi 90% (CME FedWatch via CBS News). FOMC del 15-16 settembre entro T+3 |
| 2026-09-11 | ^TNX | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2026 core +0,3% m/m contro +0,2% atteso | — |
| 2026-09-11 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2026 core +0,3% m/m contro +0,2% atteso | — |
| 2026-09-11 | GC=F | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2026 core +0,3% m/m contro +0,2% atteso | — |
| 2026-09-11 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI agosto 2026 core +0,3% m/m contro +0,2% atteso | — |
| 2026-10-14 | IEF | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI settembre 2026 +0,6% m/m in linea; 3,7% a/a contro 3,6%; core +0,3% contro +0,2%, 2,6% contro 2,5%\[2\] | Consenso: Dow Jones (CNBC) e Bloomberg (11 su 73, TheStreet). Non arrotondati 0,649% e 0,335% contro 0,58% e 0,21% (Kiplinger). Stessa mattina: utili Bank of America\[3\]\[8\]\[71\]\[72\]\[73\] |
| 2026-10-14 | ^TNX | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI settembre 2026 core +0,3% m/m contro +0,2% atteso | +9 pb al 5,304% (Quartz); 2 anni fino a +16 pb al 4,95% (Bloomberg) |
| 2026-10-14 | ^TYX | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI settembre 2026 core +0,3% m/m contro +0,2% atteso | Massimo di 24 anni (5,733%) prima delle aste (Quartz)\[74\] |
| 2026-10-14 | DX-Y.NYB | pos | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI settembre 2026 core +0,3% m/m contro +0,2% atteso | DXY +0,69% a 102,90, massimo da aprile 2025 (FXStreet) |
| 2026-10-14 | GC=F | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI settembre 2026 core +0,3% m/m contro +0,2% atteso | Fino a 4.073,41 dollari (TradingKey)\[6\] |
| 2026-10-14 | ^GSPC | neg | inflation_print, us_cpi, inflation_upside, energy_passthrough | CPI settembre 2026 core +0,3% m/m contro +0,2% atteso | −1,11% secondo Mitrade (fonte debole, che dà anche il dollaro in ritracciamento a 101,74 e l'oro in rialzo in chiusura: da verificare); circa −1% in mattinata (CNBC); vendite sull'IA concomitanti |

**Date dei nostri appunti: verifica.** Il 2021-11-10, il 2022-02-10, il 2022-05-11, il 2022-07-13, il 2023-09-13, il 2024-02-13 e il 2024-04-10 corrispondono ai CPI indicati e hanno un consenso documentato: sono tutti in tabella. Il **2024-05-31** corrisponde correttamente al PCE di aprile 2024 ed è in tabella con `pos, neg` su tutte le righe, perché la sorpresa dipende dalla fonte del consenso: 0,3% per FactSet e investingLive, 0,2% per Dow Jones. Il **2021-10-13** corrisponde correttamente al CPI di settembre 2021 (headline +0,4% m/m e 5,4% a/a, secondo il BLS), ma è escluso dalla tabella.\[75\] Il consenso (headline 0,3% m/m e 5,3% a/a, core in linea a 0,2%) non è stato verificato su una fonte nominata, la sorpresa era di un decimo sul solo headline, e nella stessa seduta uscivano i verbali FOMC che anticipavano il tapering, insieme alle trimestrali delle grandi banche.\[76\] Il PPI del 2021-10-14 resta fuori dai token CPI/PCE per costruzione; lo citiamo solo come esempio di release che contamina il T+1 del CPI del giorno prima. Il **2022-09-13** degli appunti è confermato e incluso.

**Date candidate scartate.** Tre CPI con sorpresa fredda documentata sono stati esclusi perché la seduta era contaminata. Il 2017-06-14 (CPI maggio 2017 −0,1% m/m contro 0,0%, core +0,1% contro +0,2%, secondo First Trust) coincideva con un rialzo FOMC.\[77\] Il 2019-05-10 (CPI aprile 2019 +0,3% contro +0,4%, core +0,1% contro +0,2%, secondo Econoday) coincideva con l'entrata in vigore dei dazi al 25% sui beni cinesi.\[78\] Il 2024-06-12 (CPI maggio 2024 0,0% m/m contro +0,1%) coincideva con la decisione FOMC e il dot plot. Il PCE di agosto 2026 (core +0,2% m/m contro +0,3% atteso, 3,0% a/a contro 3,3%, secondo TradingEconomics) ha una sorpresa fredda documentata, ma le fonti non permettono di fissare la seduta: le due candidate sono il 2026-09-30 e il 2026-10-01, e l'analisi FXStreet datata 1° ottobre può essere un commento del giorno dopo.\[79\] Lo lasciamo fuori finché non si verifica il calendario BEA. Il CPI di luglio 2026 (2026-08-12) e quello di febbraio 2026 (2026-03-11) sono usciti in linea su tutte le misure (CNBC), quindi non sono sorprese.

## §4 Statistiche indicative

Il catalogo comprende 31 date distinte: 14 sorprese calde, 16 fredde (14 CPI e 2 PCE) e 1 mista. Due date sono marcate interamente `pos, neg` (2024-05-31 per consenso conteso, 2025-08-12 per sorpresa mista); in molte altre lo sono solo oro o azionario. Le statistiche descrivono **solo la reazione nella seduta dell'evento** documentata dalle fonti testuali. I rendimenti cumulati a T+1, T+3, T+5 e T+10 vanno calcolati dalla pipeline sulle serie di prezzo: non li riportiamo per non inventare cifre.

**Rendimenti (`^TNX`, o il 2 anni quando è l'unico documentato), sorprese calde.** I casi verificabili sono 2018-02-14, 2021-11-10, 2023-09-13, 2024-02-13, 2024-03-12, 2024-04-10, 2026-05-12 e 2026-10-14. In 7 i rendimenti sono saliti; il 2024-03-12 il 2 anni è rimasto sostanzialmente invariato (N = 8, INDICATIVE ONLY). Ampiezze documentate: +9 pb sul 10 anni e fino a +16 pb sul 2 anni il 2026-10-14 (Bloomberg); +22 pb sul 2 anni il 2024-04-10 (CNBC).

**Rendimenti, sorprese fredde.** I casi verificabili sono 2019-06-12, 2022-11-10, 2022-12-13, 2024-05-15, 2024-07-11, 2026-02-13, 2026-04-10, 2026-05-28 e 2026-07-14. In 8 i rendimenti sono scesi; il 2026-04-10 sono saliti di 2 pb (N = 9, INDICATIVE ONLY). Ampiezze documentate sul 10 anni: −12 pb (2022-12-13), −10 pb (2024-07-11), −5 pb (2026-02-13), −2 pb (2026-07-14). L'unico caso contrario ha una spiegazione concomitante: il balzo delle aspettative d'inflazione del Michigan alle 10:00, in piena guerra con l'Iran.

**Rendimenti, totale.** Su N = 17 casi il rendimento si è mosso nel verso della sorpresa in 15, con 1 caso piatto e 1 contrario. È il risultato più solido dello studio, da ridimensionare per selection bias: le fonti giornalistiche tendono a raccontare le reazioni coerenti.

**Azionario (`^GSPC` o futures), sorprese calde.** I casi verificabili sono 2021-11-10, 2022-05-11, 2022-09-13, 2023-09-13, 2024-02-13, 2024-04-10, 2026-05-12 e 2026-10-14. In 7 l'indice è sceso; il 2023-09-13 è rimasto piatto, a +0,1% (N = 8, INDICATIVE ONLY). Il caso estremo è il −4,3% del 2022-09-13; nel 2024 il calo tipico era fra −1,0% e −1,4%, nel 2026 fra −0,6% e −1,1% secondo le fonti (Mitrade, fonte debole, indica −1,11% il 2026-10-14).

**Azionario, sorprese fredde.** Nei casi del 2022-11-10, 2022-12-13, 2024-05-15 e 2024-07-11 l'indice è salito in tutti e 4 (N = 4, INDICATIVE ONLY). In totale il segno «good news is bad news» è rispettato in 11 casi su N = 12, solo in regimi con la Fed reattiva; nessun caso del 2017–2019 entra nel conteggio.

**Dollaro.** Sulle sorprese calde il dollaro è salito in 2 casi su 2 (2024-03-12 e 2026-10-14; N = 2, INDICATIVE ONLY). Sulle sorprese fredde è sceso in 3 casi su 3 (2022-12-13, 2024-05-15 e 2026-06-10; N = 3, INDICATIVE ONLY). Su `EURUSD=X` e `JPY=X` non c'è alcun caso documentato (N = 0).

**Oro.** I casi documentati sono 2, con segni opposti: il 2021-11-10 l'oro è salito su un CPI caldo in regime «transitorio», il 2026-10-14 è sceso su un CPI caldo in regime di stretta (N = 2, INDICATIVE ONLY). È il motivo per cui l'oro è marcato `pos, neg` nel 2021 e nel 2025.

**Per regime.** Nessuna fase raggiunge N ≥ 10 di reazioni documentate su un singolo asset, per cui il confronto è qualitativo. Il 2022 mostra le reazioni più ampie (S&P −4,3%, 10 anni −12 pb), il 2024 reazioni medie (2 anni fra +22 e −10 pb), il 2026 reazioni simili al 2024 sui tassi ma più piccole sull'azionario, perché l'headline energetico era già nel consenso.

## §5 Fasi di regime

**low_attention (2017-01-01 → 2021-03-31).** L'inflazione oscillava intorno al 2%, la Fed alzava gradualmente i tassi nel 2017–2018 e li tagliava per assicurazione nel 2019, e la pandemia ha compresso tutto nel 2020. Le sorprese erano di un decimo e muovevano poco i rendimenti; dollaro e oro rispondevano più a commercio e geopolitica. Due delle quattro date in tabella hanno attribuzione debole (weekend di Pasqua, testimonianza di Powell), e due candidate sono state escluse per FOMC e dazi. **Usabilità nel 2026:** solo per il segno dei rendimenti, non per l'ampiezza né per l'azionario.

**transitory (2021-04-01 → 2022-03-15).** Il confine superiore è la vigilia del primo rialzo del 16 marzo 2022; quello inferiore è una convenzione legata alla fiammata dei CPI di primavera 2021. La Fed dichiarava l'inflazione temporanea e il mercato leggeva le sorprese calde come «Fed dietro la curva»: breakeven in salita, tassi reali compressi, oro sostenuto. **Usabilità nel 2026:** no per oro e azionario, perché la funzione di reazione della Fed è opposta; sì, con cautela, per il segno dei rendimenti nominali.

**tightening_2022_2023 (2022-03-16 → 2023-12-12).** Stretta più rapida da quattro decenni: ogni decimo di core spostava l'entità del rialzo successivo. Tutti i canali sono ortodossi e ampi e vale «good news is bad news». È l'analogo più vicino al 2026 per funzione di reazione, con l'energia come fattore nel 2022. Ma il livello d'inflazione era doppio e il drift ribassista di Treasury e azioni nel 2022 gonfia qualunque media a T+5/T+10. **Usabilità nel 2026:** sì per i segni, dimezzando le ampiezze.

**last_mile_and_tariffs (2023-12-13 → 2026-02-27).** Fusione di due sottofasi con confine interno al 2025-04-02, il giorno dei dazi «Liberation Day». Comincia con la svolta del FOMC del 13 dicembre 2023. Nel 2024 il mercato cercava la data del primo taglio: le sorprese calde lo rinviavano (2024-04-10: da giugno a settembre secondo CNBC) e quelle fredde lo anticipavano. Nel 2025 i dazi hanno prodotto sorprese miste fra headline e core (2025-08-12), e l'oro si è sganciato dai tassi reali fino al picco di gennaio 2026. **Usabilità nel 2026:** sì per tassi e dollaro, no per l'oro.

**energy_shock_2026 (2026-02-28 → present).** La guerra con l'Iran, iniziata il 28 febbraio secondo CNBC, ha portato la benzina a +21,2% m/m a marzo e il CPI a un picco del 4,2% a/a a maggio. La Fed ha alzato i tassi il 16 settembre 2026 (al 3,75–4,00%, 12 voti a 0) e il 10 anni ha toccato il 5,31% il 5 ottobre, massimo dal 2002. Il consenso incorpora rapidamente l'energia, anche tramite il nowcast di Cleveland: la sorpresa informativa sta quasi solo in core e supercore, e il canale oro-tassi reali è tornato ortodosso. **Usabilità:** è il regime corrente, ma ha solo 7 date in tabella; usarlo da solo è statisticamente fragile e conviene affiancarlo alla fase 2022–2023.

## §6 Caveat metodologici

**Release multiple nella stessa seduta.** CPI e PCE escono alle 8:30 insieme ad altri dati (richieste di sussidio, vendite al dettaglio, reddito personale) e a volte nella stessa giornata di verbali FOMC, aste o testimonianze; la chiusura giornaliera somma questi effetti. Per isolare il CPI conviene un controllo che reagisce ai dati USA ma non al tema specifico: `EURUSD=X` contro `DX-Y.NYB`, per separare la componente europea, oppure il differenziale fra `^FVX` e `^TYX`, perché il tratto breve è più legato alla Fed e quello lungo al premio a termine. Il controllo ideale sarebbe la variazione 8:25–9:00 del future sul 2 anni, che non è nel database.

**Consenso che si aggiorna e nowcast.** Il consenso del sondaggio della vigilia può essere superato dal «whisper number» e dai nowcast. Il 2026-10-14 il consenso Dow Jones sull'headline era 0,6%, quello Bloomberg 0,58% non arrotondato e il nowcast di Cleveland 0,53%: lo stesso 0,649% era una sorpresa piccola o grande secondo il riferimento. Sul core nowcast e consenso coincidevano a 0,20–0,21%, e la sorpresa di 0,335% era genuina. Per il PCE il problema è strutturale: dopo CPI e PPI gli economisti ricostruiscono il core PCE al centesimo, e una sorpresa «da 0,3 a 0,2» può valere 0,05 pp non arrotondati, come il 2024-05-31 (0,249%).

**Headline contro core in versi opposti.** Nel campione il mercato ha guardato il core quasi sempre (2023-09-13, 2026-04-10, 2026-06-10, 2026-10-14). L'eccezione rilevante è il 2025-08-12, quando un core sopra le attese è stato ignorato a favore dell'headline e del taglio già prezzato. Per questo le date miste sono marcate `pos, neg` e portano entrambi i token di direzione.

**Drift di fondo.** Nel 2022 il 2 anni è salito dallo 0,73% al 4,41% di fine anno, secondo il Tesoro USA; nel 2026 il 10 anni è salito di quasi 120 pb da inizio anno. In questi contesti qualunque campione di date, anche casuali, mostra rendimenti in rialzo a T+5/T+10. La pipeline dovrebbe sottrarre il drift medio della fase (per esempio la media mobile a 60 giorni dei rendimenti giornalieri) o confrontare con date placebo dello stesso regime.

**Serie citate ma non disponibili.** Mancano il rendimento del 2 anni, miglior termometro del canale Fed e citato in quasi tutte le Note; il breakeven a 10 anni e i TIPS, necessari per separare tasso reale e inflazione attesa nel canale oro; i future sui Fed Funds e SOFR, che misurano direttamente la sorpresa di policy; gli swap d'inflazione e i fixing CPI, consenso di mercato alternativo al sondaggio; TLT, proxy di duration lunga alternativo a `^TYX`.

**Fonti e incertezze residue.** I consensi vengono in prevalenza da Dow Jones (CNBC), FactSet (Morningstar) e Bloomberg citato da terzi, raramente dai sondaggi Reuters o Bloomberg letti direttamente come chiedeva la specifica: le differenze fra sondaggi possono cambiare il segno di sorprese di un decimo (2024-05-31). Diverse reazioni vengono da aggregatori (Benzinga, BigGo, TradingKey, FinanceCalendar) e sono marcate come non verificate quando la fonte è debole. I livelli di chiusura di DXY, oro e 10 anni per il 2022 non sono verificati su fonte primaria, e le fonti 2026 più recenti potrebbero essere riviste.

```yaml
---
title: "Sorprese d'inflazione negli Stati Uniti (CPI e PCE) e trasmissione a Treasury, dollaro, oro e azionario — regime ed episodi storici (2017–presente)"
date_compiled: 2026-10-15
primary_theme: macro_data
sub_themes: [inflation_surprise, us_cpi, us_pce, core_vs_headline, fed_reaction_function, treasury_yields, us_dollar, gold_real_yields, equity_rate_sensitivity, energy_shock, tariff_passthrough, consensus_nowcast]
relevant_assets: [IEF, ^FVX, ^TNX, ^TYX, DX-Y.NYB, EURUSD=X, JPY=X, GC=F, ^GSPC, ^NDX, IWM, ^MOVE]
external_assets_mentioned:
  - "Rendimento Treasury a 2 anni — miglior proxy del riprezzamento del percorso Fed, citato in quasi tutte le Note"
  - "Breakeven a 10 anni e rendimento reale TIPS — necessari per separare tasso reale e inflazione attesa nel canale oro"
  - "Future sui Fed Funds e SOFR (CME FedWatch) — misurano direttamente la sorpresa di policy (es. probabilità di rialzo a ottobre dal 20% al 46% il 2026-10-14)"
  - "Swap d'inflazione e fixing CPI — consenso di mercato alternativo al sondaggio degli economisti"
  - "TLT — proxy di duration lunga alternativo a ^TYX"
  - "Nowcast d'inflazione della Fed di Cleveland — riferimento che rende meno sorprendente un dato formalmente fuori consenso"
time_window:
  start: 2017-01-01
  end: present
regime_phases:
  - low_attention: 2017-01-01 to 2021-03-31
  - transitory: 2021-04-01 to 2022-03-15
  - tightening_2022_2023: 2022-03-16 to 2023-12-12
  - last_mile_and_tariffs: 2023-12-13 to 2026-02-27
  - energy_shock_2026: 2026-02-28 to present
keywords: [CPI, PCE, inflazione core, inflazione headline, consumer price index, personal consumption expenditures, hot print, cool print, sorpresa d'inflazione, inflation surprise, core CPI, supercore, consenso, consensus, Treasury, rendimenti, yields, dollaro, dollar index, oro, gold, tassi reali, real yields, Fed, rialzo dei tassi, rate hike, taglio dei tassi, rate cut, good news is bad news, shock energetico, energy shock, dazi, tariffs, BLS, nowcast Cleveland]
```

## Sources

1. [Treasury yields rise slightly after March core inflation was less than expected](https://www.cnbc.com/2026/04/10/treasury-yields-flat-as-traders-brace-for-march-cpi-print.html)
2. ['Hot' CPI Data Sends Yields, Rate Hike Odds Higher](https://www.schwab.com/learn/story/stock-market-update-open)
3. [Hot CPI Puts October Rate Hike Back in Play](https://pro.thestreet.com/market-commentary/hot-cpi-puts-october-rate-hike-back-in-play)
4. [US CPI: Highest level in nearly 30 years! Gold near 5-month highs](https://www.forex.com/en/news-and-analysis/us-cpi--highest-level-in-nearly-30-years--gold-near-5-month-highs/)
5. [Treasury Yields Vs. Gold: What Wednesday’s CPI Means for US Dollar and XAU/USD](https://www.investing.com/analysis/treasury-yields-vs-gold-what-wednesdays-cpi-means-for-us-dollar-and-xauusd-200689370)
6. [Gold Price Forecast: Higher-Than-Expected CPI Weighs on Gold, Can PPI Push Gold Back to \$4,200?](https://www.tradingkey.com/analysis/commodities/metal/262218421-gold-price-forecast-cpi-pressure-ppi-4200-tradingkey)
7. [Dow tumbles 1,200 points for worst day since June 2020 after hot inflation report](https://www.nbcnews.com/business/markets/stock-market-open-to-close-september-13-rcna47504)
8. [US CPI September 2026 Preview: Scenarios and Fed Odds](https://admiralmarkets.com/analytics/traders-blog/us-cpi-september-2026-scenarios-fed-october)
9. [US Consumer Price Index fell 0.3% in March vs 0.2% increase expected](https://www.cnbc.com/2017/04/14/us-consumer-price-index-march-2017.html)
10. [us cpi preview decline in core cpi march transitory nomura 201705112242](https://www.fxstreet.com/news/us-cpi-preview-decline-in-core-cpi-march-transitory-nomura-201705112242)
11. [Friday, January 02, 2026 | 05:48 PM ISTहिंदी में पढें](https://www.business-standard.com/article/international/us-consumer-prices-rise-0-5-in-jan-core-cpi-gains-0-3-largest-in-a-year-118021401145_1.html)
12. [The Consumer Price Index Rose 0.5% in January](https://www.ftportfolios.com/blogs/EconBlog/2018/2/14/the-consumer-price-index-rose-0.5percent-in-january)
13. [US Consumer Price Index (CPI) - May 2019: Consumer prices barely rise in May](https://www.cnbc.com/2019/06/12/consumer-price-index-may-2019.html)
14. [Consumer Price Index-May 2019](https://www.bls.gov/news.release/archives/cpi_06122019.pdf)
15. [us annual core cpi ticks up to 21 in june vs 2 expected dxy rebounds toward 97 201907111233](https://www.fxstreet.com/news/us-annual-core-cpi-ticks-up-to-21-in-june-vs-2-expected-dxy-rebounds-toward-97-201907111233)
16. [U.S. consumer prices jump 6.2% in October, the biggest inflation surge in more than 30 years](https://www.cnbc.com/2021/11/10/consumer-price-index-october.html)
17. [Econoday Economic Report: CPI](https://us.econoday.com/byevent?cust=us&fid=522375&lid=0&prev=%2Fbyweek.asp&year=2021)
18. [January 2022 CPI: Inflation rises 7.5% over the past year, even more than expected](https://www.cnbc.com/2022/02/10/january-2022-cpi-inflation-rises-7point5percent-over-the-past-year-even-more-than-expected.html)
19. [CPI April 2022: Inflation barreled ahead at 8.3% in April from a year ago, remaining near 40-year highs](https://www.cnbc.com/2022/05/11/cpi-april-2022.html)
20. [Wednesday, May 11, 2022](https://zacks.com/stock/news/1922704/%7Bhttps:/www.zackstrade.com/2019-1-dollar%7D)
21. [Inflation rose 9.1% in June, even more than expected, as consumer pressures intensify](https://www.cnbc.com/2022/07/13/inflation-rose-9point1percent-in-june-even-more-than-expected-as-price-pressures-intensify.html)
22. [stock market news for nov 11 2022](https://zacks.com/stock/news/2017297/stock-market-news-for-nov-11-2022)
23. [October CPI: Inflation moderates, rising at annual 7.7% over last year](https://finance.yahoo.com/news/october-consumer-prices-inflation-data-cpi-november-10-210744752.html)
24. [Hope Floats? Big CPI Slowdown Triggers the Bulls](https://benzinga.com/z/30063753)
25. [Core CPI cools more than expected in June, with smallest increase since August '21](https://seekingalpha.com/news/3987031-june-cpi-cools-more-than-expected-in-june)
26. <https://www.cnbc.com/2023/09/13/cpi-inflation-report-august-2023-.html>
27. [benzinga.com](https://benzinga.com/z/35198234)
28. [Inflation: Consumer prices were unchanged in October, core inflation rises at slowest pace since September 2021](https://finance.yahoo.com/news/inflation-consumer-prices-were-unchanged-in-october-core-inflation-rises-at-slowest-pace-since-september-2021-133133563.html)
29. <https://www.cnbc.com/2024/02/13/cpi-inflation-january-2024-consumer-prices-rose-0point3percent-in-january-more-than-expected-as-the-annual-rate-moved-to-3point1percent.html>
30. [Dow tumbles more than 500 points as hot inflation data stokes fears about higher-for-longer rates](https://www.cnn.com/2024/02/13/investing/stocks-tuesday-january-cpi)
31. [Stock Market News for Feb 15, 2024 - February 15, 2024 - Zacks.com](https://www.zacks.com/stock/news/2226782/stock-market-news-for-feb-15-2024)
32. [Inflation Rises More Than Expected To 3.2% In February, Rebuffs Expectations Of June Fed Rate Cut](https://benzinga.com/z/37615483)
33. <https://www.cnbc.com/2024/04/10/cpi-inflation-march-2024-consumer-prices-rose-3point5percent-from-a-year-ago-in-march.html>
34. [Stock Market News for Apr 11, 2024 - April 11, 2024 - Zacks.com](https://www.zacks.com/stock/news/2253868/stock-market-news-for-apr-11-2024)
35. [US Inflation Falls As Expected In April, Bolsters Fed Rate Cut Bets (UPDATED)](https://benzinga.com/z/38842603)
36. [CPI inflation April 2024: Consumer prices rose 0.3%](https://www.cnbc.com/2024/05/15/cpi-inflation-april-2024-consumer-prices-rose-0point3percent-in-april.html)
37. [US core PCE for April 0.2% vs 0.3% estimate](https://investinglive.com/news/us-core-pce-for-april-02-vs-03-estimate-20240531/)
38. [10-year Treasury yield hovers near 4.5% after inflation data roughly matches expectations](https://www.cnbc.com/2024/05/31/us-treasurys-ahead-of-april-pce-inflation-data.html)
39. [April PCE Index Forecasts Show Inflation Remaining Sticky](https://www.morningstar.com/economy/april-pce-index-forecasts-show-inflation-remaining-sticky)
40. [PCE inflation April 2024: The Fed’s preferred inflation measure rose 0.2% in April](https://www.cnbc.com/2024/05/31/pce-inflation-april-2024-the-feds-preferred-inflation-measure-rose-0point2percent-in-april.html)
41. [Inflation falls 0.1% in June from prior month, helping case for lower rates](https://www.cnbc.com/2024/07/11/cpi-inflation-report-june-2024.html)
42. [Zinger Key Points](https://benzinga.com/economics/macro-economic-events/24/07/39728268/inflation-slows-more-expected-to-3-in-june-heightens-expectations-for-rate-cuts-t)
43. [April 2025 CPI: Inflation Lower Than Expected](https://www.jpmorgan.com/insights/markets-and-economy/economy/cpi-report-april-2025)
44. [July US CPI Report Shows Inflation at a 2.7% Annual Rate, Slightly Below Expected](https://www.morningstar.com/economy/july-us-cpi-report-shows-inflation-27-annual-rate-slightly-below-expected)
45. [U.S. July CPI Rose Softer Than Forecast 2.7%, but Core Rate of 3.1% Disappoints](https://finance.yahoo.com/news/u-july-cpi-rose-softer-123639502.html)
46. [us inflation july tariffs](https://benzinga.com/markets/economic-data/25/08/47057291/us-inflation-july-tariffs)
47. [With the September CPI Report Delayed, Here’s What We Know About Inflation From Other Sources](https://www.chase.com/personal/investments/learning-and-insights/article/inflation-data-government-shutdown-2025)
48. [Inflation Cools in September as Consumer Price Index Rises Below Forecasts](https://cbcal.com/economic-report/september-consumer-price-index-cpi-inflation-update/)
49. [CPI Report Expected to Show Continued Inflation](https://www.morningstar.com/economy/cpi-report-expected-show-continued-inflation)
50. [Inflation rose to 3% in September, CPI shows in delayed release](https://qz.com/cpi-inflation-us-economy-consumer-prices-interest-rate-cut)
51. [CPI inflation report January 2026:](https://www.cnbc.com/2026/02/13/cpi-inflation-report-january-2026.html)
52. [U.S. Treasury yields: consumer inflation report comes in lighter](https://www.cnbc.com/2026/02/13/us-treasury-yields-key-consumer-inflation-report-comes-into-focus-.html)
53. [US CPI Preview: Sticky Inflation to Keep the Fed on Hold Until the Summer?](https://www.forex.com/en-us/news-and-analysis/us-cpi-preview-sticky-inflation-to-keep-the-fed-on-hold-until-the-summer/)
54. [CPI inflation report March 2026: Consumer prices rose 3.3%](https://www.cnbc.com/2026/04/10/cpi-inflation-report-march-2026.html)
55. [April CPI Report Shows Inflation Broadening As Energy Spike Impact Spreads](https://www.morningstar.com/economy/april-cpi-report-shows-inflation-38-annual-rate)
56. [CPI inflation April 2026: Prices rose 3.8% annually](https://www.cnbc.com/2026/05/12/cpi-inflation-april-2026-.html)
57. [United States Core Consumer Price Index (CPI) YoY](<https://www.investing.com/economic-calendar/united-states-core-consumer-price-index-(cpi)-yoy-736>)
58. [April CPI Preview: 3.7% Print Could Crush Rate-Cut Bets](https://dealpropfirm.com/blog/april-cpi-2026-preview-3-7-percent-rate-cut-bets)
59. [April 2026 CPI Report: Inflation Surges to 3.8% as Energy Prices Drive Highest Reading Since May 2023](https://www.unboxfuture.com/2026/05/april-2026-cpi-report-inflation-surges.html?m=1)
60. [Core inflation hit an annual rate of 3.3% in April, as expected, Fed’s preferred gauge shows](https://www.cnbc.com/2026/05/28/core-inflation-hit-an-annual-rate-of-3point3percent-in-april-as-expected-feds-preferred-gauge-shows-.html)
61. [May PCE Expected to Show Rising Inflation](https://www.morningstar.com/economy/may-pce-expected-show-rising-inflation)
62. [April PCE Report Seen Showing Energy-Driven Inflation Rising to 3-Year Highs](https://www.morningstar.com/economy/april-pce-report-seen-showing-energy-driven-inflation-rising-3-year-highs)
63. [May CPI Report: Energy-Driven Inflation Is Contained, for Now](https://www.morningstar.com/economy/may-cpi-report-shows-inflation-42-annual-rate-line-with-forecasts)
64. [May 2026 CPI: The Energy Shock Hiding Softer Core Inflation](https://www.money365.market/articles/may-2026-cpi-decoded)
65. [CPI Report: Release Time, Schedule, Latest Data and How It Moves Markets](https://www.cmelitegroup.com/knowledge-hub/cpi-report-release-time-schedule-latest-data-and-how-it-moves-markets/)
66. [Gold market exhales as U.S. CPI rises roughly in line with expectations](https://www.kitco.com/news/article/2026-06-10/gold-market-exhales-us-cpi-rises-roughly-line-expectations)
67. [May 2026 US CPI Report & Trading Guide](https://www.bitget.com/amp/academy/may-2026-us-cpi-report-and-trading-guide)
68. [Treasury Yields Rise as Housing Market Slows](https://cbcal.com/economic-report/weekly-economic-review-june-inflation-cpi-ppi-oil-prices/)
69. [Consumer Price Index News Release - 2026 M06 Results](https://www.bls.gov/news.release/archives/cpi_07142026.htm)
70. [US CPI June 2026: Inflation Falls to 3.5%, Below Forecast: Date, Time & What to Expect](https://www.financecalendar.com/event/us-cpi-report-july-2026/)
71. [September CPI Report Shows Inflation Remains Red-Hot: What to Know](https://www.kiplinger.com/investing/economy/cpi-report-september-2026-what-to-expect)
72. [CPI inflation report September 2026](https://www.cnbc.com/2026/10/14/cpi-inflation-report-september-2026.html)
73. [U.S. Core Inflation Unexpectedly Heats Up, Market Reassesses October Rate Hike Risks — BigGo Finance](https://finance.biggo.com/news/52045320-5f7c-4796-aad5-0a9e082ca3a3)
74. [September 2026 CPI inflation beats Wall Street forecasts](https://qz.com/september-cpi-inflation-treasury-yields-101426)
75. [USDL-21-1831 Transmission of material in this release is embargoed until](https://www.bls.gov/news.release/archives/cpi_10132021.pdf)
76. [Stock Market News for Oct 14, 2021](https://sports.yahoo.com/stock-market-news-oct-14-123012313.html)
77. [CPI - U May-17 Apr-17 Mar-17 3-mo % Ch. 6-mo % Ch. Yr to Yr](https://www.ftportfolios.com/Commentary/EconomicResearch/2017/6/14/the-consumer-price-index-declined-0.1percent-in-may)
78. [Econoday Economic Report: CPI](https://us.econoday.com/byevent?amp=&amp=&amp=&amp=&cust=us&fid=498772&lid=0&prev=%2Fbyweek.asp&year=2019)
79. [United States Core PCE Price Index Annual Change](https://tradingeconomics.com/united-states/core-pce-price-index-annual-change)
