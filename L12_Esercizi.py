# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 12 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; il notebook `L11_Progetto_Finale` eseguito almeno una volta (tabella `g_cancellazioni_aggiornate_destinazione_mese`); il notebook `utils` nella stessa cartella `Libro_Python`; la dashboard **Cancellazioni per destinazione 2024** costruita seguendo il Capitolo 12. Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L12_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una **copia** di questo notebook, creata con **Clone** (per esempio `L12_Esercizi_svolti`). Ogni esercizio ha una parte nella dashboard e una parte nel notebook, che calcola i valori con cui confrontare la dashboard. Il notebook **non scrive tabelle**.
# MAGIC
# MAGIC Si eseguono prima la cella con `%run ./utils` e la cella di preparazione, poi un esercizio alla volta. L'esercizio 8 contiene una cella che deve fallire (**ERRORE VOLUTO**) e due celle che producono un risultato sbagliato (**ERRORE SILENZIOSO**): sotto ciascuna si scrive la correzione. Non usare Run all.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione
# MAGIC
# MAGIC La prima cella contiene solo `%run ./utils`; la seconda legge la tabella del report e definisce `exercise_query`, la query del dataset con i due parametri `:threshold` e `:min_bookings` (esercizio 5). Risultato atteso: `317` e `Preparazione completata`.

# COMMAND ----------

# MAGIC %run ./utils

# COMMAND ----------

# Cella di preparazione: la tabella del report e la query con due parametri
PROJECT_REPORT_TABLE = build_table_name("cancellazioni_aggiornate", "destinazione_mese", layer="g")
report_df = spark.table(PROJECT_REPORT_TABLE)

exercise_query = f"""SELECT destination, country, check_in_month,
       booking_count, cancelled_count, revenue, cancellation_rate,
       CASE WHEN booking_count < :min_bookings THEN 'non valutabile'
            WHEN cancellation_rate > :threshold THEN 'critico'
            ELSE 'ok' END AS cancellation_status
FROM {PROJECT_REPORT_TABLE}"""

print(report_df.count())
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Il contatore del ricavo
# MAGIC
# MAGIC **Dashboard.** Nella pagina **Panoramica** si aggiunga un contatore **Ricavo** con la somma di `revenue` (**Value** → `revenue`, aggregazione **SUM**), con **Format** → **Custom**, **Abbreviation** → **None**. Si legga il valore con il filtro **Paese** su **All** e su **Italy**.
# MAGIC
# MAGIC **Notebook.** Si calcolino il ricavo totale e quello dell'Italia, arrotondati a due decimali, e li si stampi sulla stessa riga.
# MAGIC
# MAGIC *Risultato atteso:* nella dashboard `7.529.860,44` e `408.538,77`; nel notebook `7529860.44 408538.77`.

# COMMAND ----------

# Esercizio 1 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Un filtro sulla destinazione
# MAGIC
# MAGIC **Dashboard.** Si aggiunga alla pagina un filtro **Multiple values** sul campo `destination`, con il titolo **Destinazione**, e si scelga **Amalfi** (con **Paese** su **All**). Si leggano i quattro contatori.
# MAGIC
# MAGIC **Notebook.** Si scrivano i valori letti nel dizionario `amalfi_dashboard` (chiavi: `Prenotazioni`, `Tasso di cancellazione (%)`, `Combinazioni critiche`, `Ricavo`), si calcolino gli stessi valori in `amalfi_expected` e li si confronti con un ciclo, come nella sezione 12.12.
# MAGIC
# MAGIC *Risultato atteso:* nella dashboard `51`, `41,2`, `1`, `29.503,96`; nel notebook quattro righe con esito `OK`.

# COMMAND ----------

# Esercizio 2 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – La soglia in movimento
# MAGIC
# MAGIC **Dashboard.** Con **Destinazione** e **Paese** su **All**, si scrivano nel parametro **Soglia (%)** i valori 25, 35, 45 e 50, annotando ogni volta il contatore **Combinazioni critiche**. Alla fine si riporti la soglia a 30.
# MAGIC
# MAGIC **Notebook.** Con un ciclo sulla lista `[25.0, 35.0, 45.0, 50.0]` si esegua `exercise_query` con `args={"threshold": ..., "min_bookings": MIN_BOOKINGS}` e si stampino la soglia e il numero delle combinazioni critiche.
# MAGIC
# MAGIC *Risultato atteso:* `157`, `115`, `32`, `6`.

# COMMAND ----------

# Esercizio 3 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Il grafico per paese
# MAGIC
# MAGIC **Dashboard.** Si aggiunga un grafico a barre con `country` sull'asse X e la misura `overall_cancellation_rate` sull'asse Y, con **Labels** attivo e il titolo **Tasso di cancellazione per paese (%)**.
# MAGIC
# MAGIC **Notebook.** Si calcolino per ogni paese il tasso complessivo (`overall_cancellation_rate`) e la media dei tassi (`average_of_rates`), si mostri il risultato in ordine di tasso decrescente (a parità di tasso, per nome del paese) e si stampino il paese con il tasso più alto e quello con il tasso più basso.
# MAGIC
# MAGIC *Risultato atteso:* 18 righe; il più alto `China 44.6`, il più basso `Canada 29.6`; Egypt `40.7`, media dei tassi `36.2`.

# COMMAND ----------

# Esercizio 4 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Il volume minimo come parametro
# MAGIC
# MAGIC **Dashboard.** Nella query del dataset **Report cancellazioni** si sostituisca il numero 20 con il parametro `:min_bookings` (la query diventa quella di `exercise_query`); nelle impostazioni del parametro si scelgano **Type** → **Numeric**, **Numeric type** → **Integer**, **Display name** `Volume minimo` e valore 20. Lo si aggiunga alla pagina con un filtro **Single value**. Con la soglia al 30%, si leggano le combinazioni critiche con il volume minimo a 10 e a 30, poi lo si riporti a 20.
# MAGIC
# MAGIC **Notebook.** Per i volumi minimi 10 e 30 si esegua `exercise_query` con la soglia 30 e si conti ogni stato (`groupBy` + `count`), stampando una lista di coppie (stato, numero).
# MAGIC
# MAGIC *Risultato atteso:* con 10, `critico 190`, `non valutabile 93`, `ok 34`; con 30, `critico 114`, `non valutabile 191`, `ok 12`.

# COMMAND ----------

# Esercizio 5 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Una pagina per continente
# MAGIC
# MAGIC **Dashboard.** Si crei un secondo dataset, **Report per continente**, con una query che unisce la tabella del report a `samples.wanderbricks.countries` sul nome del paese e aggiunge la colonna `continent`; nel nuovo dataset si definisca una misura con il tasso complessivo. Si crei una seconda pagina, **Continenti**, con un grafico a barre del tasso per continente e una tabella con prenotazioni e cancellate per continente.
# MAGIC
# MAGIC **Notebook.** Si scriva la stessa query in `continent_query` (con le costanti `PROJECT_REPORT_TABLE` e `COUNTRIES_TABLE`), si contino le sue righe e si mostrino per continente prenotazioni, cancellate e tasso complessivo, in ordine di prenotazioni decrescente.
# MAGIC
# MAGIC *Risultato atteso:* `317` righe (nessuna persa nel join); Europe `5557 2110 38`, Asia `5290 1969 37.2`, Oceania `1246 481 38.6`, North America `1212 447 36.9`, Africa `285 116 40.7`.

# COMMAND ----------

# Esercizio 6 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – La verifica di una vista filtrata
# MAGIC
# MAGIC **Dashboard.** Si imposti la pagina **Panoramica** con **Paese** su **Italy**, **Destinazione** su **All**, soglia 40 e volume minimo 20, e si leggano i contatori **Prenotazioni**, **Tasso di cancellazione (%)**, **Combinazioni critiche** e **Ricavo**. Alla fine si usi **Reset all to default**.
# MAGIC
# MAGIC **Notebook.** Si scrivano i valori letti in un dizionario; si esegua `exercise_query` con gli stessi parametri, si applichi lo stesso filtro sul paese, si calcolino i quattro valori e li si confronti con un ciclo.
# MAGIC
# MAGIC *Risultato atteso:* `714`, `37.8`, `4`, `408538.77`; quattro righe con esito `OK`.

# COMMAND ----------

# Esercizio 7 – il tuo codice qui


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC
# MAGIC **Notebook.** Per ciascuna delle tre celle seguenti: si esegua la cella, si annotino il tipo dell'errore e il messaggio (o il risultato sbagliato), e si scriva la correzione nella cella vuota sotto.
# MAGIC
# MAGIC **Dashboard.** Si riproducano e si correggano tre errori: **8d** un contatore con `AVG(cancellation_rate)` al posto della misura; **8e** il grafico per mese con `check_in_month` sull'asse X lasciato con la scala **Continuous** e l'aggregazione **SUM**; **8f** una modifica a un titolo nella bozza, poi la versione pubblicata aperta con **View published** senza pubblicare di nuovo.
# MAGIC
# MAGIC *Risultato atteso:* 8a `UNBOUND_SQL_PARAMETER` su `min_bookings`; 8b nessun errore ma `31.9` invece di `35.0`; 8c nessun errore ma `False` invece di `True`; 8d `37,3` invece di `37,7`; 8e una sola barra lunga `2.164` invece delle 12 barre del tasso; 8f il titolo vecchio nella versione pubblicata.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (la query con due parametri)
print(spark.sql(exercise_query, args={"threshold": 30.0}).count())

# COMMAND ----------

# Correzione 8a – il tuo codice qui


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8b (il tasso del Regno Unito)
uk_df = report_df.filter(F.col("country") == "United Kingdom")
print(uk_df.agg(F.round(F.avg("cancellation_rate"), 1)).collect()[0][0])

# COMMAND ----------

# Correzione 8b – il tuo codice qui


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8c (il valore letto sulla dashboard)
dashboard_bookings = 13.590
print(dashboard_bookings == 13590)

# COMMAND ----------

# Correzione 8c – il tuo codice qui

