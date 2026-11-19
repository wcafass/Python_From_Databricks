# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 10 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito; il notebook `utils` nella stessa cartella `Libro_Python`. Gli esercizi **scrivono tabelle** nello schema `workspace.libro_python`.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L10_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L10_Esercizi_svolti`) **nella stessa cartella**, perché la prima cella carica `utils` con `%run ./utils`. Si eseguono per prime la cella con `%run` e la cella di preparazione, poi **una cella alla volta**: l'esercizio 8 contiene celle che devono fallire (**ERRORE VOLUTO**) o che producono un risultato sbagliato (**ERRORE SILENZIOSO**). Non usare Run all.
# MAGIC Ogni esercizio ha una cella di **verifica** con il risultato atteso; le verifiche SQL sulle tabelle scritte dagli esercizi usano `display(spark.sql(f"..."))`, perché una cella `%sql` non vede le costanti Python. Gli esercizi 4 e 8 usano tabelle scritte negli esercizi precedenti (3 e 7): se un esercizio è stato saltato, la cella che le legge fallisce con `TABLE_OR_VIEW_NOT_FOUND`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione
# MAGIC La prima cella contiene solo `%run ./utils` e mostra soltanto la cella di testo iniziale di `utils`; la seconda definisce le costanti degli esercizi. Risultato atteso: `Preparazione completata`.

# COMMAND ----------

# MAGIC %run ./utils

# COMMAND ----------

# Cella di preparazione: le tabelle che gli esercizi scrivono e i DataFrame delle tabelle di partenza
ITALY_TABLE = build_table_name("prenotazioni_italia", "destinazione_mese")
QUARTER_TABLE = build_table_name("prenotazioni_trimestre", "giornaliere")
TYPE_MONTH_TABLE = build_table_name("prenotazioni_tipo", "mese", layer="g")
ABU_DHABI_BOOKINGS_TABLE = build_table_name("strutture_abu_dhabi", "prenotazioni")
ABU_DHABI_UPDATES_TABLE = build_table_name("strutture_abu_dhabi", "aggiornamenti")

bookings_df = spark.table(SOURCE_BOOKINGS_TABLE)
properties_df = spark.table(PROPERTIES_TABLE)
destinations_df = spark.table(DESTINATIONS_TABLE)

print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Leggere con spark.table
# MAGIC 1. Leggere con `spark.table()` le tabelle `PROPERTIES_TABLE` e `DESTINATIONS_TABLE` e stampare, per ciascuna, il numero delle righe e il numero delle colonne (`len()` della lista `columns`).
# MAGIC 2. Stampare il confronto tra le colonne di `spark.table(PROPERTIES_TABLE)` e quelle di `spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")`.
# MAGIC 3. Con `DESCRIBE DETAIL` sulla tabella `BOOKINGS_TABLE`, stampare il valore della colonna `format` (suggerimento: `collect()[0]["format"]`).

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso
print("18163 13")
print("42 6")
print("True")
print("delta")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – I nomi delle tabelle
# MAGIC 1. Con `build_table_name` costruire e stampare i nomi di due tabelle: i dati di lavoro con le prenotazioni riepilogate per struttura (argomento `prenotazioni`, granularità `struttura`) e il report per una dashboard con i ricavi per paese e anno (argomento `ricavi`, granularità `paese_anno`, strato `g`).
# MAGIC 2. Stampare le cinque costanti della cella di preparazione.
# MAGIC 3. In un commento, dire quali di questi nomi rispettano la convenzione del libro e perché gli altri no: `s_prenotazioni_giornaliere`, `S_Prenotazioni`, `g-ricavi-paese-anno`, `tabella_finale`.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso
print("workspace.libro_python.s_prenotazioni_struttura")
print("workspace.libro_python.g_ricavi_paese_anno")
print("workspace.libro_python.s_prenotazioni_italia_destinazione_mese")
print("workspace.libro_python.s_prenotazioni_trimestre_giornaliere")
print("workspace.libro_python.g_prenotazioni_tipo_mese")
print("workspace.libro_python.s_strutture_abu_dhabi_prenotazioni")
print("workspace.libro_python.s_strutture_abu_dhabi_aggiornamenti")
print("Nomi corretti: solo s_prenotazioni_giornaliere")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Scrivere una tabella
# MAGIC 1. Costruire il riepilogo delle prenotazioni 2024 delle destinazioni italiane (`country` = `Italy`) per destinazione e mese di arrivo, con le colonne `destination`, `country`, `check_in_month`, `booking_count` e `cancelled_count`, in quest'ordine (prenotazioni → strutture → destinazioni, con `select` prima dei join).
# MAGIC 2. Scriverlo nella tabella `ITALY_TABLE` con `overwrite`, stampando prima il nome della tabella.
# MAGIC 3. Rileggere la tabella con `spark.table()` e stampare il numero delle righe.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: totali della tabella scritta (atteso: 29 714 142)
display(spark.sql(f"""
    SELECT COUNT(*) AS row_count, SUM(booking_count) AS booking_count, SUM(cancelled_count) AS cancelled_count
    FROM {ITALY_TABLE}
"""))

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica indipendente: prenotazioni e cancellate 2024 in Italia (714, 142)
# MAGIC SELECT COUNT(*)                                                AS booking_count,
# MAGIC        SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count
# MAGIC FROM samples.wanderbricks.bookings b
# MAGIC JOIN samples.wanderbricks.properties p USING (property_id)
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC WHERE year(b.check_in) = 2024 AND d.country = 'Italy'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Append, riparazione e storico
# MAGIC 1. Preparare `quarter_daily_df`, il riepilogo giornaliero del primo trimestre del 2024 (`check_in`, `booking_count`, `cancelled_count`, `revenue` arrotondato), e scriverlo nella tabella `QUARTER_TABLE` un mese alla volta: gennaio con `overwrite`, febbraio con `append`, marzo con `append`. Stampare le righe della tabella.
# MAGIC 2. In una nuova cella, rieseguire l'`append` di marzo (come se la cella fosse stata eseguita due volte) e stampare `count()` e `distinct().count()` della tabella.
# MAGIC 3. Riparare la tabella con un `overwrite` del trimestre completo e stampare di nuovo i due conteggi.
# MAGIC 4. Mostrare lo storico (`version`, `operation`, in ordine di versione) e, con un ciclo e `VERSION AS OF`, il numero delle righe delle versioni da 0 a 4.

# COMMAND ----------

# Scrivere qui la soluzione (punto 1)

# COMMAND ----------

# Scrivere qui la soluzione (punto 2)

# COMMAND ----------

# Scrivere qui la soluzione (punto 3)

# COMMAND ----------

# Scrivere qui la soluzione (punto 4)

# COMMAND ----------

# Verifica: risultato atteso (alla prima esecuzione dell'esercizio)
print("punto 1: 90")
print("punto 2: 121 90")
print("punto 3: 90 90")
print("punto 4: versioni 0 CREATE OR REPLACE TABLE AS SELECT, 1 WRITE, 2 WRITE, 3 WRITE, 4 CREATE OR REPLACE TABLE AS SELECT")
print("         righe: 0 30 / 1 59 / 2 90 / 3 121 / 4 90")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Un report con write_table
# MAGIC 1. Costruire il report 2024 per tipo di struttura e mese di arrivo con `property_type`, `check_in_month`, `booking_count`, `cancelled_count`, `cancellation_rate` (in %, un decimale) e `cancellation_status` (con `cancellation_status_column()` di `utils`).
# MAGIC 2. Scriverlo nella tabella `TYPE_MONTH_TABLE` con `write_table`.
# MAGIC 3. Rileggendo la tabella, contare le righe per stato (`combination_count`), in ordine alfabetico di stato.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso
print("Scrittura di workspace.libro_python.g_prenotazioni_tipo_mese (mode=overwrite)")
print("Righe nella tabella: 32")
print("cancellation_status  combination_count")
print("non valutabile       2")
print("ok                   30")

# COMMAND ----------

# Verifica SQL: totali della tabella (atteso: 32 13586 2647)
display(spark.sql(f"""
    SELECT COUNT(*) AS row_count, SUM(booking_count) AS booking_count, SUM(cancelled_count) AS cancelled_count
    FROM {TYPE_MONTH_TABLE}
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Un notebook personale con %run
# MAGIC 1. Nella cartella `Libro_Python` creare un notebook chiamato `my_utils` (**Create → Notebook**) e scrivere in una cella il codice seguente:
# MAGIC ```python
# MAGIC # Notebook my_utils: costanti e funzioni personali (si carica dopo utils)
# MAGIC MY_PROPERTY_ID = 16225
# MAGIC
# MAGIC
# MAGIC def count_property_bookings(property_id, year=ANALYSIS_YEAR):
# MAGIC     """Conta le prenotazioni di una struttura con arrivo nell'anno indicato."""
# MAGIC     return (
# MAGIC         spark.table(SOURCE_BOOKINGS_TABLE)
# MAGIC         .filter((F.col("property_id") == property_id) & (F.year(F.col("check_in")) == year))
# MAGIC         .count()
# MAGIC     )
# MAGIC ```
# MAGIC 2. Eseguire la cella con `%run ./my_utils` qui sotto (la cella con `%run ./utils` deve essere già stata eseguita: `my_utils` usa `F`, `SOURCE_BOOKINGS_TABLE` e `ANALYSIS_YEAR`).
# MAGIC 3. Stampare `MY_PROPERTY_ID` con il suo conteggio, e i conteggi delle strutture `11670` e `16317`.
# MAGIC 4. In `my_utils`, cambiare il valore di `MY_PROPERTY_ID` in `11670`. **Senza** rieseguire la cella con `%run`, stampare `MY_PROPERTY_ID`; poi rieseguire la seconda cella con `%run ./my_utils` e stamparlo di nuovo. Alla fine riportare `my_utils` al valore `16225`.

# COMMAND ----------

# MAGIC %run ./my_utils

# COMMAND ----------

# Scrivere qui la soluzione (punto 3)

# COMMAND ----------

# Scrivere qui la soluzione (punto 4, prima di rieseguire %run)

# COMMAND ----------

# MAGIC %run ./my_utils

# COMMAND ----------

# Scrivere qui la soluzione (punto 4, dopo aver rieseguito %run)

# COMMAND ----------

# Verifica: risultato atteso
print("16225 4")
print("11670 6")
print("16317 7")
print("dopo la modifica, senza %run: 16225")
print("dopo aver rieseguito %run: 11670 6")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Un MERGE con inserimenti
# MAGIC Le strutture `16047` e `5134`, ad Abu Dhabi, hanno aggiornamenti per prenotazioni 2024 che in `bookings` non compaiono.
# MAGIC 1. Scrivere nella tabella `ABU_DHABI_BOOKINGS_TABLE` (con `write_table`) le prenotazioni 2024 delle due strutture prese da `bookings_df`.
# MAGIC 2. Leggere gli aggiornamenti 2024 delle due strutture da `BOOKING_UPDATES_TABLE`, stampare righe e prenotazioni distinte; scegliere per ogni prenotazione l'aggiornamento più recente (come nella sezione 10.8), con le colonne della tabella di destinazione; stampare righe e chiavi distinte; scrivere il risultato in `ABU_DHABI_UPDATES_TABLE`.
# MAGIC 3. Eseguire il `MERGE` in SQL con `spark.sql()` (`UPDATE SET *`, `INSERT *`, chiave `booking_id`) e mostrarne i contatori.
# MAGIC 4. Mostrare la tabella finale (`booking_id`, `property_id`, `check_in`, `status`, `total_amount`, in ordine di `booking_id`) e, con `agg`, il numero delle prenotazioni, delle cancellate e il ricavo arrotondato.

# COMMAND ----------

# Scrivere qui la soluzione (punto 1)

# COMMAND ----------

# Scrivere qui la soluzione (punto 2)

# COMMAND ----------

# Scrivere qui la soluzione (punto 3)

# COMMAND ----------

# Scrivere qui la soluzione (punto 4)

# COMMAND ----------

# Verifica: risultato atteso (alla prima esecuzione del MERGE)
print("punto 1: Righe nella tabella: 4")
print("punto 2: 8 5, poi 5 5; Righe nella tabella: 5")
print("punto 3: num_affected_rows 5, num_updated_rows 3, num_deleted_rows 0, num_inserted_rows 2")
print("punto 4:")
print("booking_id  property_id  check_in    status     total_amount")
print("682         16047        2024-12-24  completed  834.57")
print("3985        5134         2024-05-13  completed  664.28")
print("48985       16047        2024-09-04  completed  493.94")
print("51744       16047        2024-10-24  cancelled  486.32")
print("72662       16047        2024-12-10  cancelled  100.16")
print("72668       5134         2024-10-07  cancelled  695.94")
print("booking_count 6, cancelled_count 3, revenue 3275.21")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare il tipo dell'errore e il messaggio (o il risultato sbagliato) e scrivere sotto la versione corretta. Le celle usano le tabelle degli esercizi 3 e 7; le prime tre scrivono una copia del riepilogo italiano nella tabella `ITALY_COPY_TABLE`, definita nella cella 8a.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: le celle 8a, 8b, 8c, 8e e 8f scrivono o rileggono `29` righe; il `MERGE` corretto della cella 8d, eseguito dopo l'esercizio 7, aggiorna `5` righe e non ne inserisce nessuna (la tabella resta di `6` righe).

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (una copia del riepilogo italiano)
ITALY_COPY_TABLE = build_table_name("prenotazioni_italia_copia", "destinazione_mese")
italy_df = spark.table(ITALY_TABLE)
(
    italy_df.write
    .mode("replace")
    .saveAsTable(ITALY_COPY_TABLE)
)

# COMMAND ----------

# Correzione 8a (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE VOLUTO – cella 8b (le destinazioni della copia)
result_df = italy_df.write.mode("overwrite").saveAsTable(ITALY_COPY_TABLE)
display(result_df.orderBy("destination"))

# COMMAND ----------

# Correzione 8b (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE VOLUTO – cella 8c (la copia scritta di nuovo)
italy_df.write.saveAsTable(ITALY_COPY_TABLE)

# COMMAND ----------

# Correzione 8c (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE VOLUTO – cella 8d (il MERGE di Abu Dhabi con tutti gli aggiornamenti)
abu_dhabi_updates_df = (
    spark.table(BOOKING_UPDATES_TABLE)
    .filter((F.col("property_id") == 16047) | (F.col("property_id") == 5134))
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
abu_dhabi_table = DeltaTable.forName(spark, ABU_DHABI_BOOKINGS_TABLE)
(
    abu_dhabi_table.alias("t")
    .merge(abu_dhabi_updates_df.select(spark.table(ABU_DHABI_BOOKINGS_TABLE).columns).alias("s"), "t.booking_id = s.booking_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# COMMAND ----------

# Correzione 8d (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (solo le destinazioni italiane)
all_destinations_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .select("booking_id", "property_id", "check_in", "status")
    .join(properties_df.select("property_id", "destination_id"), on="property_id", how="inner")
    .join(destinations_df.select("destination_id", "destination", "country"), on="destination_id", how="inner")
    .withColumn("check_in_month", F.month(F.col("check_in")))
    .groupBy("destination", "country", "check_in_month")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
    )
)
all_destinations_df.filter(F.col("country") == "Italy")
write_table(all_destinations_df, ITALY_TABLE)

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (aggiornare il riepilogo italiano)
italy_only_df = all_destinations_df.filter(F.col("country") == "Italy")
write_table(italy_only_df, ITALY_TABLE, mode="append")

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)
