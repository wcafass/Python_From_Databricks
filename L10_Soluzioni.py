# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 10 – Soluzioni
# MAGIC
# MAGIC Soluzioni commentate degli esercizi di `L10_Esercizi` (anche nell'Appendice A del libro).
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito; `utils` nella stessa cartella. Il notebook **scrive tabelle** nello schema `workspace.libro_python`.
# MAGIC Si esegue una cella alla volta, dall'alto in basso: le celle dell'esercizio 8 marcate **ERRORE VOLUTO** devono fallire, quelle marcate **ERRORE SILENZIOSO** producono un risultato sbagliato; la correzione è nella cella sotto. Per l'esercizio 6 serve il notebook `my_utils` (contenuto nella sezione dell'esercizio).
# MAGIC Se il notebook è già stato eseguito, lo storico dell'esercizio 4 mostra più versioni e il MERGE dell'esercizio 7 non inserisce più righe (contatori `5 5 0 0`).

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

# Soluzione 1: spark.table, columns, DESCRIBE DETAIL
properties_table_df = spark.table(PROPERTIES_TABLE)
destinations_table_df = spark.table(DESTINATIONS_TABLE)
print(properties_table_df.count(), len(properties_table_df.columns))
print(destinations_table_df.count(), len(destinations_table_df.columns))
print(properties_table_df.columns == spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}").columns)
detail_row = spark.sql(f"DESCRIBE DETAIL {BOOKINGS_TABLE}").collect()[0]
print(detail_row["format"])

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

# Soluzione 2: nomi costruiti con build_table_name
print(build_table_name("prenotazioni", "struttura"))
print(build_table_name("ricavi", "paese_anno", layer="g"))
print(ITALY_TABLE)
print(QUARTER_TABLE)
print(TYPE_MONTH_TABLE)
print(ABU_DHABI_BOOKINGS_TABLE)
print(ABU_DHABI_UPDATES_TABLE)
# s_prenotazioni_giornaliere: corretto (prefisso, argomento, granularità; minuscole e trattini bassi)
# S_Prenotazioni: lettere maiuscole e granularità mancante
# g-ricavi-paese-anno: trattini al posto dei trattini bassi (non ammessi nei nomi del libro)
# tabella_finale: manca il prefisso, l'argomento non dice di che cosa parla, manca la granularità

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

# Soluzione 3: riepilogo italiano per destinazione e mese, scritto con overwrite
italy_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .select("booking_id", "property_id", "check_in", "status")
    .join(properties_df.select("property_id", "destination_id"), on="property_id", how="inner")
    .join(destinations_df.select("destination_id", "destination", "country"), on="destination_id", how="inner")
    .filter(F.col("country") == "Italy")
    .withColumn("check_in_month", F.month(F.col("check_in")))
    .groupBy("destination", "country", "check_in_month")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
    )
)
print(f"Scrittura di {ITALY_TABLE}")
(
    italy_df.write
    .mode("overwrite")
    .saveAsTable(ITALY_TABLE)
)
print(spark.table(ITALY_TABLE).count())

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

# Soluzione 4a: il trimestre un mese alla volta (gennaio overwrite, febbraio e marzo append)
quarter_daily_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .filter(F.month(F.col("check_in")) <= 3)
    .groupBy("check_in")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
    )
)
print(f"Scrittura di {QUARTER_TABLE}")
(
    quarter_daily_df.filter(F.month(F.col("check_in")) == 1).write
    .mode("overwrite")
    .saveAsTable(QUARTER_TABLE)
)
(
    quarter_daily_df.filter(F.month(F.col("check_in")) == 2).write
    .mode("append")
    .saveAsTable(QUARTER_TABLE)
)
(
    quarter_daily_df.filter(F.month(F.col("check_in")) == 3).write
    .mode("append")
    .saveAsTable(QUARTER_TABLE)
)
print(spark.table(QUARTER_TABLE).count())

# COMMAND ----------

# Soluzione 4b: l'append di marzo rieseguito per sbaglio, scoperto con count e distinct
(
    quarter_daily_df.filter(F.month(F.col("check_in")) == 3).write
    .mode("append")
    .saveAsTable(QUARTER_TABLE)
)
quarter_table_df = spark.table(QUARTER_TABLE)
print(quarter_table_df.count(), quarter_table_df.distinct().count())

# COMMAND ----------

# Soluzione 4c: riparazione con un overwrite del trimestre completo
print(f"Scrittura di {QUARTER_TABLE}")
(
    quarter_daily_df.write
    .mode("overwrite")
    .saveAsTable(QUARTER_TABLE)
)
quarter_table_df = spark.table(QUARTER_TABLE)
print(quarter_table_df.count(), quarter_table_df.distinct().count())

# COMMAND ----------

# Soluzione 4d: storico e righe di ogni versione
display(spark.sql(f"DESCRIBE HISTORY {QUARTER_TABLE}").select("version", "operation").orderBy("version"))
for version in range(5):
    version_query = f"SELECT COUNT(*) AS row_count FROM {QUARTER_TABLE} VERSION AS OF {version}"
    print(version, spark.sql(version_query).collect()[0]["row_count"])

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

# Soluzione 5: report per tipo di struttura e mese, scritto con write_table
type_month_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .select("booking_id", "property_id", "check_in", "status")
    .join(properties_df.select("property_id", "property_type"), on="property_id", how="inner")
    .withColumn("check_in_month", F.month(F.col("check_in")))
    .groupBy("property_type", "check_in_month")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
    )
    .withColumn("cancellation_rate", F.round(F.col("cancelled_count") / F.col("booking_count") * 100, 1))
    .withColumn("cancellation_status", cancellation_status_column())
)
write_table(type_month_df, TYPE_MONTH_TABLE)
display(
    spark.table(TYPE_MONTH_TABLE)
    .groupBy("cancellation_status")
    .agg(F.count("*").alias("combination_count"))
    .orderBy("cancellation_status")
)

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

# Soluzione 6a: le definizioni di my_utils
print(MY_PROPERTY_ID, count_property_bookings(MY_PROPERTY_ID))
print(11670, count_property_bookings(11670))
print(16317, count_property_bookings(16317))

# COMMAND ----------

# Soluzione 6b: dopo aver cambiato MY_PROPERTY_ID in my_utils, senza rieseguire %run
print(MY_PROPERTY_ID)

# COMMAND ----------

# MAGIC %run ./my_utils

# COMMAND ----------

# Soluzione 6c: dopo aver rieseguito la cella con %run ./my_utils
print(MY_PROPERTY_ID, count_property_bookings(MY_PROPERTY_ID))

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

# Soluzione 7a: la tabella di destinazione con le prenotazioni 2024 delle due strutture
abu_dhabi_bookings_df = (
    bookings_df
    .filter((F.col("property_id") == 16047) | (F.col("property_id") == 5134))
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
write_table(abu_dhabi_bookings_df, ABU_DHABI_BOOKINGS_TABLE)

# COMMAND ----------

# Soluzione 7b: l'aggiornamento più recente per prenotazione, con il controllo righe = chiavi
abu_dhabi_updates_df = (
    spark.table(BOOKING_UPDATES_TABLE)
    .filter((F.col("property_id") == 16047) | (F.col("property_id") == 5134))
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
print(abu_dhabi_updates_df.count(), abu_dhabi_updates_df.select("booking_id").distinct().count())
abu_dhabi_last_df = (
    abu_dhabi_updates_df
    .groupBy("booking_id")
    .agg(F.max("updated_at").alias("last_updated_at"))
)
abu_dhabi_latest_df = (
    abu_dhabi_updates_df
    .join(abu_dhabi_last_df, on="booking_id", how="inner")
    .filter(F.col("updated_at") == F.col("last_updated_at"))
    .select(abu_dhabi_bookings_df.columns)
)
print(abu_dhabi_latest_df.count(), abu_dhabi_latest_df.select("booking_id").distinct().count())
write_table(abu_dhabi_latest_df, ABU_DHABI_UPDATES_TABLE)

# COMMAND ----------

# Soluzione 7c: il MERGE in SQL e la tabella finale
abu_dhabi_merge_query = f"""
MERGE INTO {ABU_DHABI_BOOKINGS_TABLE} AS t
USING {ABU_DHABI_UPDATES_TABLE} AS s
ON t.booking_id = s.booking_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""
display(spark.sql(abu_dhabi_merge_query))

# COMMAND ----------

# Soluzione 7d: la tabella dopo il MERGE
abu_dhabi_table_df = spark.table(ABU_DHABI_BOOKINGS_TABLE)
display(abu_dhabi_table_df.select("booking_id", "property_id", "check_in", "status", "total_amount").orderBy("booking_id"))
display(
    abu_dhabi_table_df.agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
    )
)

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

# Correzione 8a (UNSUPPORTED_OPERATION: la modalità si scrive "overwrite")
ITALY_COPY_TABLE = build_table_name("prenotazioni_italia_copia", "destinazione_mese")
italy_df = spark.table(ITALY_TABLE)
(
    italy_df.write
    .mode("overwrite")
    .saveAsTable(ITALY_COPY_TABLE)
)
print(spark.table(ITALY_COPY_TABLE).count())

# COMMAND ----------

# ERRORE VOLUTO – cella 8b (le destinazioni della copia)
result_df = italy_df.write.mode("overwrite").saveAsTable(ITALY_COPY_TABLE)
display(result_df.orderBy("destination"))

# COMMAND ----------

# Correzione 8b (AttributeError: saveAsTable restituisce None; si rilegge la tabella)
italy_df.write.mode("overwrite").saveAsTable(ITALY_COPY_TABLE)
display(spark.table(ITALY_COPY_TABLE).orderBy("destination"))

# COMMAND ----------

# ERRORE VOLUTO – cella 8c (la copia scritta di nuovo)
italy_df.write.saveAsTable(ITALY_COPY_TABLE)

# COMMAND ----------

# Correzione 8c (TABLE_OR_VIEW_ALREADY_EXISTS: la modalità va sempre indicata)
italy_df.write.mode("overwrite").saveAsTable(ITALY_COPY_TABLE)
print(spark.table(ITALY_COPY_TABLE).count())

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

# Correzione 8d (DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE: una riga per chiave,
# l'aggiornamento più recente dell'esercizio 7)
(
    abu_dhabi_table.alias("t")
    .merge(abu_dhabi_latest_df.alias("s"), "t.booking_id = s.booking_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
print(spark.table(ABU_DHABI_BOOKINGS_TABLE).count())

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

# Correzione 8e (il risultato del filter non era salvato: write_table scriveva tutte le destinazioni)
italy_only_df = all_destinations_df.filter(F.col("country") == "Italy")
write_table(italy_only_df, ITALY_TABLE)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (aggiornare il riepilogo italiano)
italy_only_df = all_destinations_df.filter(F.col("country") == "Italy")
write_table(italy_only_df, ITALY_TABLE, mode="append")

# COMMAND ----------

# Correzione 8f (append in un notebook rieseguibile: righe ripetute; si usa overwrite)
write_table(italy_only_df, ITALY_TABLE)
