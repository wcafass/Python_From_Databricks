# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 10 – Leggere e scrivere tabelle Delta
# MAGIC
# MAGIC Notebook del Capitolo 10 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Leggere una tabella con `spark.table()` e riconoscere le caratteristiche di una tabella Delta
# MAGIC - Dare un nome alle tabelle (prefisso, argomento, granularità) e scriverle con `saveAsTable`, in modalità `overwrite` o `append`
# MAGIC - Leggere lo storico (`DESCRIBE HISTORY`, `VERSION AS OF`) e capire il controllo dello schema
# MAGIC - Aggiornare una tabella con `MERGE` (SQL e `DeltaTable`)
# MAGIC - Caricare il notebook comune `utils` con `%run ./utils` e scrivere un report in quattro passi
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–9; notebook collegato al compute **Serverless**
# MAGIC - `L00_Prepara_Dati` già eseguito; il notebook `utils` nella stessa cartella `Libro_Python` (arriva con il **Pull** del Git folder)
# MAGIC - Questo notebook **scrive tabelle** nello schema `workspace.libro_python`: `s_prenotazioni_giornaliere`, `s_prenotazioni_importi_giornaliere`, `s_strutture_guida_prenotazioni`, `s_strutture_guida_aggiornamenti`, `g_cancellazioni_destinazione_mese`
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio, **dall'alto in basso**. **Non usare Run all**: alcune celle contengono errori voluti, e molte celle scrivono tabelle che le celle successive rileggono.
# MAGIC Si esegue per prima la **cella di preparazione** (scritta a mano: `%run ./utils` si introduce nella sezione 10.9; dal Capitolo 11 la preparazione sarà `%run ./utils`). Le celle vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si leggono il tipo, il messaggio e la riga;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** sotto deve funzionare **senza errori**, con il risultato indicato.
# MAGIC
# MAGIC Per gli errori di Spark (nome tra parentesi quadre e `SQLSTATE`) si legge la **riga di riepilogo**; nel traceback si cerca la riga della cella e si saltano i blocchi della libreria.
# MAGIC
# MAGIC **Se il notebook è già stato eseguito**: la prima scrittura della sezione 10.4 fallisce anche lei con `TABLE_OR_VIEW_ALREADY_EXISTS` (è normale, si prosegue), e lo storico della sezione 10.6 mostra più versioni di quelle del testo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `Preparazione completata`.

# COMMAND ----------

# Cella di preparazione: import e costanti (dal Capitolo 11: %run ./utils, sezione 10.9)
import pyspark.sql.functions as F
from datetime import date, timedelta, datetime
from delta.tables import DeltaTable

# Schemi e tabelle: samples è in sola lettura, workspace.libro_python è lo schema di lavoro
SOURCE_SCHEMA = "samples.wanderbricks"
WORK_SCHEMA = "workspace.libro_python"
SOURCE_BOOKINGS_TABLE = f"{SOURCE_SCHEMA}.bookings"           # prenotazioni originali
BOOKING_UPDATES_TABLE = f"{SOURCE_SCHEMA}.booking_updates"    # aggiornamenti delle prenotazioni
PROPERTIES_TABLE = f"{SOURCE_SCHEMA}.properties"
DESTINATIONS_TABLE = f"{SOURCE_SCHEMA}.destinations"
BOOKINGS_TABLE = f"{WORK_SCHEMA}.b_bookings"                  # copia didattica con anomalie (Capitolo 0)

ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %
MIN_BOOKINGS = 20                    # prenotazioni minime perché un tasso sia valutabile

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
GUIDE_PROPERTY_IDS = [11670, 16317, 16225]

print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.1 Le tabelle Delta

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC format  name
# MAGIC delta   workspace.libro_python.b_bookings
# MAGIC ```

# COMMAND ----------

display(spark.sql(f"DESCRIBE DETAIL {BOOKINGS_TABLE}").select("format", "name"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: la riga completa di `DESCRIBE DETAIL` (tra le colonne `format` = `delta`).

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.2 Leggere una tabella: spark.table

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `72247 72287`.

# COMMAND ----------

bookings_df = spark.table(SOURCE_BOOKINGS_TABLE)
properties_df = spark.table(PROPERTIES_TABLE)
destinations_df = spark.table(DESTINATIONS_TABLE)
teaching_bookings_df = spark.table(BOOKINGS_TABLE)
print(bookings_df.count(), teaching_bookings_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `True`.

# COMMAND ----------

print(bookings_df.columns == spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}").columns)

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (la tabella si chiama booking_updates, non bookings_updates; l'errore compare sulla riga 3, quella di count()).

# COMMAND ----------

# ERRORE VOLUTO – la tabella si chiama booking_updates, non bookings_updates
updates_df = spark.table(f"{SOURCE_SCHEMA}.bookings_updates")
print(updates_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il nome giusto, dalla costante `BOOKING_UPDATES_TABLE`. Risultato atteso: `83068`.

# COMMAND ----------

# Correzione: il nome della tabella dalla costante
updates_df = spark.table(BOOKING_UPDATES_TABLE)
print(updates_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.3 Dare un nome alle tabelle

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso (alla prima esecuzione; dopo, compaiono anche le tabelle del capitolo):
# MAGIC ```
# MAGIC database      tableName             isTemporary
# MAGIC libro_python  b_bookings            false
# MAGIC libro_python  b_bookings_modifiche  false
# MAGIC ```

# COMMAND ----------

display(spark.sql(f"SHOW TABLES IN {WORK_SCHEMA}"))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC workspace.libro_python.s_prenotazioni_giornaliere
# MAGIC workspace.libro_python.s_prenotazioni_importi_giornaliere
# MAGIC workspace.libro_python.s_strutture_guida_prenotazioni
# MAGIC workspace.libro_python.s_strutture_guida_aggiornamenti
# MAGIC workspace.libro_python.g_cancellazioni_destinazione_mese
# MAGIC ```

# COMMAND ----------

def build_table_name(topic, granularity, layer="s"):
    """Costruisce il nome completo di una tabella nello schema di lavoro."""
    return f"{WORK_SCHEMA}.{layer}_{topic}_{granularity}"


DAILY_BOOKINGS_TABLE = build_table_name("prenotazioni", "giornaliere")
DAILY_AMOUNTS_TABLE = build_table_name("prenotazioni_importi", "giornaliere")
GUIDE_BOOKINGS_TABLE = build_table_name("strutture_guida", "prenotazioni")
GUIDE_UPDATES_TABLE = build_table_name("strutture_guida", "aggiornamenti")
CANCELLATION_REPORT_TABLE = build_table_name("cancellazioni", "destinazione_mese", layer="g")

print(DAILY_BOOKINGS_TABLE)
print(DAILY_AMOUNTS_TABLE)
print(GUIDE_BOOKINGS_TABLE)
print(GUIDE_UPDATES_TABLE)
print(CANCELLATION_REPORT_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC **Errore silenzioso (solo descritto)**: le costanti delle tabelle di riferimento (`SOURCE_BOOKINGS_TABLE`, `BOOKINGS_TABLE`, ...) non si usano mai in una scrittura. Su `b_bookings` la scrittura riuscirebbe senza avvisi e la copia didattica andrebbe persa: si ripara rieseguendo `L00_Prepara_Dati`. Nelle scritture si usano solo le costanti costruite con `build_table_name`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.4 Scrivere una tabella: saveAsTable

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `30 29`.

# COMMAND ----------

daily_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .groupBy("check_in")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
    )
)
january_df = daily_df.filter(F.month(F.col("check_in")) == 1)
february_df = daily_df.filter(F.month(F.col("check_in")) == 2)
print(january_df.count(), february_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso (se il notebook è già stato eseguito, questa cella fallisce con TABLE_OR_VIEW_ALREADY_EXISTS: è normale, si prosegue):
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_giornaliere
# MAGIC ```

# COMMAND ----------

print(f"Scrittura di {DAILY_BOOKINGS_TABLE}")
january_df.write.saveAsTable(DAILY_BOOKINGS_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC 30
# MAGIC
# MAGIC check_in    booking_count  cancelled_count  revenue
# MAGIC 2024-01-01  16             4                8221.8
# MAGIC 2024-01-03  1              0                880.12
# MAGIC ```

# COMMAND ----------

daily_table_df = spark.table(DAILY_BOOKINGS_TABLE)
print(daily_table_df.count())
display(daily_table_df.orderBy("check_in").limit(2))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC day_count  booking_count  cancelled_count  revenue
# MAGIC 30         204            40               108766.13
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)                    AS day_count,
# MAGIC        SUM(booking_count)          AS booking_count,
# MAGIC        SUM(cancelled_count)        AS cancelled_count,
# MAGIC        ROUND(SUM(revenue), 2)      AS revenue
# MAGIC FROM workspace.libro_python.s_prenotazioni_giornaliere

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (la tabella esiste già e la modalità non è indicata).

# COMMAND ----------

# ERRORE VOLUTO – la tabella esiste già e la modalità non è indicata
january_df.write.saveAsTable(DAILY_BOOKINGS_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la modalità di scrittura, nella sezione 10.5.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.5 Le modalità di scrittura: overwrite e append

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_giornaliere
# MAGIC 30
# MAGIC
# MAGIC 30
# MAGIC ```

# COMMAND ----------

print(f"Scrittura di {DAILY_BOOKINGS_TABLE}")
(
    january_df.write
    .mode("overwrite")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)
print(spark.table(DAILY_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_giornaliere
# MAGIC 59
# MAGIC
# MAGIC 59
# MAGIC ```

# COMMAND ----------

print(f"Scrittura di {DAILY_BOOKINGS_TABLE}")
(
    february_df.write
    .mode("append")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)
print(spark.table(DAILY_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente non dà errori ma produce un risultato sbagliato (la cella dell'append eseguita una seconda volta): `88 59`.

# COMMAND ----------

# ERRORE SILENZIOSO – la cella dell'append eseguita una seconda volta
(
    february_df.write
    .mode("append")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)
daily_table_df = spark.table(DAILY_BOOKINGS_TABLE)
print(daily_table_df.count(), daily_table_df.distinct().count())

# COMMAND ----------

# MAGIC %md
# MAGIC Controllo in SQL sulla chiave della tabella. Risultato atteso:
# MAGIC ```
# MAGIC row_count  day_count  booking_count
# MAGIC 88         59         626
# MAGIC ```

# COMMAND ----------

display(spark.sql(f"""
    SELECT COUNT(*)                 AS row_count,
           COUNT(DISTINCT check_in) AS day_count,
           SUM(booking_count)       AS booking_count
    FROM {DAILY_BOOKINGS_TABLE}
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: overwrite con il DataFrame completo dei due mesi. Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_giornaliere
# MAGIC 59 59
# MAGIC ```

# COMMAND ----------

# Correzione: overwrite con il DataFrame completo, da uno stato noto
two_months_df = daily_df.filter(F.month(F.col("check_in")) <= 2)
print(f"Scrittura di {DAILY_BOOKINGS_TABLE}")
(
    two_months_df.write
    .mode("overwrite")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)
daily_table_df = spark.table(DAILY_BOOKINGS_TABLE)
print(daily_table_df.count(), daily_table_df.distinct().count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (la modalità si scrive overwrite, non overwrites).

# COMMAND ----------

# ERRORE VOLUTO – la modalità si scrive overwrite, non overwrites
(
    two_months_df.write
    .mode("overwrites")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la modalità scritta esattamente, `"overwrite"`, come nelle celle precedenti. La tabella non è stata toccata e non serve riscriverla. Risultato atteso: `59`.

# COMMAND ----------

# Correzione: la tabella non è cambiata (la modalità giusta è "overwrite")
print(spark.table(DAILY_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.6 Lo storico delle versioni

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC version  operation
# MAGIC 0        CREATE TABLE AS SELECT
# MAGIC 1        CREATE OR REPLACE TABLE AS SELECT
# MAGIC 2        WRITE
# MAGIC 3        WRITE
# MAGIC 4        CREATE OR REPLACE TABLE AS SELECT
# MAGIC ```

# COMMAND ----------

history_df = spark.sql(f"DESCRIBE HISTORY {DAILY_BOOKINGS_TABLE}")
display(history_df.select("version", "operation").orderBy("version"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: lo storico completo, dalla versione più recente.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY workspace.libro_python.s_prenotazioni_giornaliere

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC 0 30
# MAGIC 1 30
# MAGIC 2 59
# MAGIC 3 88
# MAGIC 4 59
# MAGIC ```

# COMMAND ----------

for version in range(5):
    version_query = f"SELECT COUNT(*) AS row_count FROM {DAILY_BOOKINGS_TABLE} VERSION AS OF {version}"
    row_count = spark.sql(version_query).collect()[0]["row_count"]
    print(version, row_count)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC row_count
# MAGIC 88
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS row_count
# MAGIC FROM workspace.libro_python.s_prenotazioni_giornaliere VERSION AS OF 3

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.7 Lo schema della tabella

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC 90 31
# MAGIC ['check_in', 'booking_count', 'cancelled_count', 'revenue', 'avg_amount']
# MAGIC ```

# COMMAND ----------

daily_amounts_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .filter(F.month(F.col("check_in")) <= 3)
    .groupBy("check_in")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
        F.round(F.avg("total_amount"), 2).alias("avg_amount"),
    )
)
march_amounts_df = daily_amounts_df.filter(F.month(F.col("check_in")) == 3)
print(daily_amounts_df.count(), march_amounts_df.count())
print(march_amounts_df.columns)

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (il DataFrame ha una colonna che la tabella non ha; si leggono anche Table schema e Data schema nel messaggio).

# COMMAND ----------

# ERRORE VOLUTO – il DataFrame ha una colonna che la tabella non ha
(
    march_amounts_df.write
    .mode("append")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)

# COMMAND ----------

# MAGIC %md
# MAGIC La tabella non è cambiata. Risultato atteso:
# MAGIC ```
# MAGIC 59
# MAGIC ['check_in', 'booking_count', 'cancelled_count', 'revenue']
# MAGIC ```

# COMMAND ----------

print(spark.table(DAILY_BOOKINGS_TABLE).count())
print(spark.table(DAILY_BOOKINGS_TABLE).columns)

# COMMAND ----------

# MAGIC %md
# MAGIC Soluzione consigliata: una tabella nuova. Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_importi_giornaliere
# MAGIC 90
# MAGIC ```

# COMMAND ----------

print(f"Scrittura di {DAILY_AMOUNTS_TABLE}")
(
    daily_amounts_df.write
    .mode("overwrite")
    .saveAsTable(DAILY_AMOUNTS_TABLE)
)
print(spark.table(DAILY_AMOUNTS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Cambiare lo schema di una tabella esistente (solo se concordato): `overwrite` con `overwriteSchema`. Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_giornaliere
# MAGIC 90
# MAGIC ['check_in', 'booking_count', 'cancelled_count', 'revenue', 'avg_amount']
# MAGIC ```

# COMMAND ----------

print(f"Scrittura di {DAILY_BOOKINGS_TABLE}")
(
    daily_amounts_df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(DAILY_BOOKINGS_TABLE)
)
print(spark.table(DAILY_BOOKINGS_TABLE).count())
print(spark.table(DAILY_BOOKINGS_TABLE).columns)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.8 Aggiornare una tabella: MERGE

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_strutture_guida_prenotazioni
# MAGIC 17
# MAGIC ```

# COMMAND ----------

guide_bookings_df = (
    bookings_df
    .filter(
        (F.col("property_id") == 11670)
        | (F.col("property_id") == 16317)
        | (F.col("property_id") == 16225)
    )
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
print(f"Scrittura di {GUIDE_BOOKINGS_TABLE}")
(
    guide_bookings_df.write
    .mode("overwrite")
    .saveAsTable(GUIDE_BOOKINGS_TABLE)
)
print(spark.table(GUIDE_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Riepilogo per struttura **prima** del MERGE. Risultato atteso:
# MAGIC ```
# MAGIC property_id  booking_count  cancelled_count  revenue
# MAGIC 11670        6              0                3966.21
# MAGIC 16225        4              2                2896.92
# MAGIC 16317        7              1                5139.59
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                              AS booking_count,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
# MAGIC        ROUND(SUM(total_amount), 2)                           AS revenue
# MAGIC FROM workspace.libro_python.s_strutture_guida_prenotazioni
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC 20 13
# MAGIC
# MAGIC booking_id  booking_update_id  status     total_amount  updated_at
# MAGIC 49395       17570289837900     confirmed  647.01        2024-03-26T07:15:08.000Z
# MAGIC 49395       17570290017629     cancelled  647.01        2024-06-07T02:14:15.000Z
# MAGIC ```

# COMMAND ----------

updates_df = spark.table(BOOKING_UPDATES_TABLE)
guide_updates_df = (
    updates_df
    .filter(
        (F.col("property_id") == 11670)
        | (F.col("property_id") == 16317)
        | (F.col("property_id") == 16225)
    )
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
print(guide_updates_df.count(), guide_updates_df.select("booking_id").distinct().count())
display(
    guide_updates_df
    .filter(F.col("booking_id") == 49395)
    .select("booking_id", "booking_update_id", "status", "total_amount", "updated_at")
    .orderBy("updated_at")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `13 13`.

# COMMAND ----------

last_update_df = (
    guide_updates_df
    .groupBy("booking_id")
    .agg(F.max("updated_at").alias("last_updated_at"))
)
latest_updates_df = (
    guide_updates_df
    .join(last_update_df, on="booking_id", how="inner")
    .filter(F.col("updated_at") == F.col("last_updated_at"))
    .select(guide_bookings_df.columns)
)
print(latest_updates_df.count(), latest_updates_df.select("booking_id").distinct().count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_strutture_guida_aggiornamenti
# MAGIC 13
# MAGIC ```

# COMMAND ----------

print(f"Scrittura di {GUIDE_UPDATES_TABLE}")
(
    latest_updates_df.write
    .mode("overwrite")
    .saveAsTable(GUIDE_UPDATES_TABLE)
)
print(spark.table(GUIDE_UPDATES_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Il MERGE in SQL. Risultato atteso (la print della query, poi i contatori):
# MAGIC ```
# MAGIC MERGE INTO workspace.libro_python.s_strutture_guida_prenotazioni AS t
# MAGIC USING workspace.libro_python.s_strutture_guida_aggiornamenti AS s
# MAGIC ON t.booking_id = s.booking_id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *
# MAGIC
# MAGIC num_affected_rows  num_updated_rows  num_deleted_rows  num_inserted_rows
# MAGIC 13                 13                0                 0
# MAGIC ```

# COMMAND ----------

MERGE_KEY = "t.booking_id = s.booking_id"

merge_query = f"""
MERGE INTO {GUIDE_BOOKINGS_TABLE} AS t
USING {GUIDE_UPDATES_TABLE} AS s
ON {MERGE_KEY}
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""
print(merge_query)
display(spark.sql(merge_query))

# COMMAND ----------

# MAGIC %md
# MAGIC Riepilogo per struttura **dopo** il MERGE (stessa query di prima). Risultato atteso:
# MAGIC ```
# MAGIC property_id  booking_count  cancelled_count  revenue
# MAGIC 11670        6              0                4065.21
# MAGIC 16225        4              2                2911.92
# MAGIC 16317        7              2                5139.59
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                              AS booking_count,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
# MAGIC        ROUND(SUM(total_amount), 2)                           AS revenue
# MAGIC FROM workspace.libro_python.s_strutture_guida_prenotazioni
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC Rieseguendo la cella del MERGE i contatori restano `13 13 0 0` e la tabella non cambia: il MERGE è rieseguibile.

# COMMAND ----------

# MAGIC %md
# MAGIC Il MERGE in Python con `DeltaTable`. Risultato atteso: `17`.

# COMMAND ----------

guide_table = DeltaTable.forName(spark, GUIDE_BOOKINGS_TABLE)
(
    guide_table.alias("t")
    .merge(latest_updates_df.alias("s"), MERGE_KEY)
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
print(spark.table(GUIDE_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (la sorgente ha più righe per la stessa prenotazione).

# COMMAND ----------

# ERRORE VOLUTO – la sorgente ha più righe per la stessa prenotazione
(
    guide_table.alias("t")
    .merge(guide_updates_df.select(guide_bookings_df.columns).alias("s"), MERGE_KEY)
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# COMMAND ----------

# MAGIC %md
# MAGIC La tabella è rimasta intatta (tutto o niente). Risultato atteso:
# MAGIC ```
# MAGIC 17
# MAGIC version  operation
# MAGIC 0        CREATE OR REPLACE TABLE AS SELECT
# MAGIC 1        MERGE
# MAGIC 2        MERGE
# MAGIC ```
# MAGIC Se il notebook è stato eseguito più volte, le versioni sono di più.

# COMMAND ----------

# Controllo: righe e storico della tabella dopo il MERGE fallito
print(spark.table(GUIDE_BOOKINGS_TABLE).count())
display(spark.sql(f"DESCRIBE HISTORY {GUIDE_BOOKINGS_TABLE}").select("version", "operation").orderBy("version"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.9 Riutilizzare il codice: %run e il notebook utils

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente contiene solo `%run ./utils` e non produce output. Il notebook `utils` deve trovarsi nella stessa cartella di questo notebook.

# COMMAND ----------

# MAGIC %run ./utils

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC workspace.libro_python.g_cancellazioni_destinazione_mese
# MAGIC 20 30.0 [11670, 16317, 16225]
# MAGIC Help on function write_table in module __main__:
# MAGIC
# MAGIC write_table(df, table_name, mode='overwrite')
# MAGIC     Scrive un DataFrame in una tabella Delta, poi la rilegge e ne stampa le righe.
# MAGIC
# MAGIC ```

# COMMAND ----------

print(build_table_name("cancellazioni", "destinazione_mese", layer="g"))
print(MIN_BOOKINGS, CANCELLATION_RATE_THRESHOLD, GUIDE_PROPERTY_IDS)
help(write_table)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.10 Un esempio completo in quattro passi

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.g_cancellazioni_destinazione_mese (mode=overwrite)
# MAGIC Righe nella tabella: 317
# MAGIC ```

# COMMAND ----------

# 1. Leggere: prenotazioni senza righe ripetute, con gli importi negativi resi NULL
clean_bookings_df = read_clean_bookings()
property_places_df = spark.table(PROPERTIES_TABLE).select("property_id", "destination_id")
destination_names_df = spark.table(DESTINATIONS_TABLE).select("destination_id", "destination", "country")

# 2. Trasformare: il report del Capitolo 9, con il ricavo
report_df = (
    clean_bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .select("booking_id", "property_id", "check_in", "status", "total_amount")
    .join(property_places_df, on="property_id", how="inner")
    .join(destination_names_df, on="destination_id", how="inner")
    .withColumn("check_in_month", F.month(F.col("check_in")))
    .groupBy("destination", "country", "check_in_month")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
    )
    .withColumn("cancellation_rate", F.round(F.col("cancelled_count") / F.col("booking_count") * 100, 1))
    .withColumn("cancellation_status", cancellation_status_column())
)

# 3. Scrivere
write_table(report_df, CANCELLATION_REPORT_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC cancellation_status  combination_count
# MAGIC critico              8
# MAGIC non valutabile       152
# MAGIC ok                   157
# MAGIC ```

# COMMAND ----------

# 4. Verificare: rilettura della tabella scritta
report_table_df = spark.table(CANCELLATION_REPORT_TABLE)
display(
    report_table_df
    .groupBy("cancellation_status")
    .agg(F.count("*").alias("combination_count"))
    .orderBy("cancellation_status")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Verifica indipendente in SQL: le due righe devono coincidere. Risultato atteso:
# MAGIC ```
# MAGIC source      booking_count  cancelled_count  revenue
# MAGIC tabella g_  13586          2647             7477734.15
# MAGIC b_bookings  13586          2647             7477734.15
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'tabella g_' AS source,
# MAGIC        SUM(booking_count)   AS booking_count,
# MAGIC        SUM(cancelled_count) AS cancelled_count,
# MAGIC        ROUND(SUM(revenue), 2) AS revenue
# MAGIC FROM workspace.libro_python.g_cancellazioni_destinazione_mese
# MAGIC UNION ALL
# MAGIC SELECT 'b_bookings' AS source,
# MAGIC        COUNT(*),
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END),
# MAGIC        ROUND(SUM(CASE WHEN total_amount >= 0 THEN total_amount END), 2)
# MAGIC FROM (SELECT DISTINCT * FROM workspace.libro_python.b_bookings)
# MAGIC WHERE year(check_in) = 2024

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso:
# MAGIC ```
# MAGIC destination  country               check_in_month  booking_count  cancelled_count  revenue   cancellation_rate  cancellation_status
# MAGIC Cairo        Egypt                 9               35             13               18543.88  37.1               critico
# MAGIC London       United Kingdom        9               35             13               20159.36  37.1               critico
# MAGIC Madrid       Spain                 4               21             7                12162.47  33.3               critico
# MAGIC London       United Kingdom        11              37             12               21052.88  32.4               critico
# MAGIC Dubai        United Arab Emirates  3               25             8                14315.84  32                 critico
# MAGIC Barcelona    Spain                 8               44             14               25647.98  31.8               critico
# MAGIC Cairo        Egypt                 12              45             14               27447.89  31.1               critico
# MAGIC Byron Bay    Australia             8               53             16               27598.21  30.2               critico
# MAGIC ```

# COMMAND ----------

display(
    report_table_df
    .filter(F.col("cancellation_status") == "critico")
    .orderBy(F.col("cancellation_rate").desc(), "destination", "check_in_month")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10.11 Errori comuni con le tabelle

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (saveAsTable non restituisce un DataFrame).

# COMMAND ----------

# ERRORE VOLUTO – saveAsTable non restituisce un DataFrame
result_df = daily_amounts_df.write.mode("overwrite").saveAsTable(DAILY_BOOKINGS_TABLE)
print(result_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la scrittura non si assegna; si rilegge la tabella. Risultato atteso: `90`.

# COMMAND ----------

# Correzione: si rilegge la tabella scritta
print(spark.table(DAILY_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC degli errori che non producono messaggi
# MAGIC
# MAGIC Tre errori di questo capitolo non si possono mostrare con una cella, perché non danno messaggi, e conviene conoscerli prima di incontrarli.
# MAGIC
# MAGIC - **Scrivere su una tabella di riferimento.** Una costante sbagliata in una scrittura, per esempio `BOOKINGS_TABLE` al posto di una costante costruita con `build_table_name`, sovrascrive la copia didattica `b_bookings` senza nessun avviso (sezione 10.3). Il rimedio è rieseguire `L00_Prepara_Dati`; la prevenzione è usare nelle scritture solo le costanti del proprio notebook, e rileggere con attenzione la riga stampata prima di ogni scrittura.
# MAGIC - **Modificare `utils` senza rieseguire `%run`.** Il notebook continua a usare le definizioni caricate prima della modifica (sezione 10.9). Dopo ogni modifica di `utils`, e dopo ogni riavvio del compute, si riesegue la cella con `%run ./utils`.
# MAGIC - **Rieseguire una cella con `append`.** È l'errore della sezione 10.5, il più frequente dei tre: righe ripetute in silenzio. Si previene con `overwrite` nei notebook rieseguibili e si scopre confrontando `count()` con `distinct().count()`, o con lo storico.
# MAGIC
# MAGIC Se la cella con `%run` non trova il notebook, perché `utils` non è nella stessa cartella o il nome è scritto diversamente, il comando si ferma con un messaggio che dice che il notebook non è stato trovato: si controllano il percorso e la cartella. Se invece la cella con `%run` non è stata eseguita, le funzioni di `utils` non esistono, e la prima che si usa produce un `NameError` del Capitolo 6, per esempio `NameError: name 'write_table' is not defined`.
# MAGIC
# MAGIC ## Errori comuni
# MAGIC
# MAGIC | Tipo di errore | Messaggio tipico | Significato | Prima cosa da controllare |
# MAGIC | --- | --- | --- | --- |
# MAGIC | `TABLE_OR_VIEW_NOT_FOUND` | ``The table or view `...` cannot be found`` | la tabella da leggere non esiste | il nome nella costante; il Catalog Explorer |
# MAGIC | `TABLE_OR_VIEW_ALREADY_EXISTS` | ``Cannot create table or view `...` because it already exists`` | `saveAsTable` senza modalità su una tabella esistente | `mode("overwrite")` o `mode("append")` |
# MAGIC | `UNSUPPORTED_OPERATION` | `overwrites is not supported` | una modalità scritta male | il testo della modalità: `"overwrite"`, `"append"` |
# MAGIC | `DELTA_METADATA_MISMATCH` | `A schema mismatch detected when writing to the Delta table` | il DataFrame ha colonne o tipi diversi dalla tabella | `Table schema` e `Data schema` nel messaggio; una tabella nuova |
# MAGIC | `DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE` | `multiple source rows matched ... the same target row` | la sorgente del `MERGE` ha più righe per chiave | righe contro chiavi distinte della sorgente; la regola per scegliere la riga |
# MAGIC | `AttributeError` | `'NoneType' object has no attribute 'count'` | il risultato di una scrittura usato come DataFrame | la scrittura non si assegna; si rilegge con `spark.table` |
# MAGIC | `NameError` | `name 'write_table' is not defined` | `utils` non caricato | la cella con `%run ./utils` |
# MAGIC | (nessun errore) | righe ripetute, somme gonfiate | un `append` rieseguito | `count()` contro `distinct().count()`; `DESCRIBE HISTORY` |
# MAGIC | (nessun errore) | una tabella di riferimento cambiata | una scrittura con la costante sbagliata | la riga stampata prima della scrittura; `L00_Prepara_Dati` |
# MAGIC | (nessun errore) | una correzione a `utils` che non ha effetto | `%run` non rieseguito | rieseguire la cella con `%run ./utils` |
