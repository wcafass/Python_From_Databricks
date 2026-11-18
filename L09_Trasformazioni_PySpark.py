# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 9 – Trasformazioni con PySpark
# MAGIC
# MAGIC Notebook del Capitolo 9 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Usare le funzioni di Spark con `import pyspark.sql.functions as F` e indicare le colonne con `F.col()`
# MAGIC - Aggiungere colonne con `withColumn`, `F.lit`, `alias`; convertire con `F.to_date` e `cast`
# MAGIC - Classificare con `F.when` / `otherwise`
# MAGIC - Aggregare con `groupBy` + `agg` (WHERE e HAVING), anche su dati sporchi
# MAGIC - Unire tabelle con `join` e costruire il report del tasso di cancellazione per destinazione e mese
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–8; notebook collegato al compute **Serverless**
# MAGIC - `L00_Prepara_Dati` già eseguito (la sezione 9.6 legge `workspace.libro_python.b_bookings`); nessuna cella scrive tabelle
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio, **dall'alto in basso**. **Non usare Run all**: alcune celle contengono errori voluti.
# MAGIC Si esegue per prima la **cella di preparazione**. Le celle vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si leggono il tipo, il messaggio e la riga;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** sotto deve funzionare **senza errori**, con il risultato indicato.
# MAGIC
# MAGIC Per gli errori di Spark (nome tra parentesi quadre e `SQLSTATE`) si legge la **riga di riepilogo**; nel traceback si cerca la riga della cella e si saltano i blocchi della libreria PySpark.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `Preparazione completata`.

# COMMAND ----------

# Cella di preparazione: import, costanti e DataFrame usati nelle sezioni
import pyspark.sql.functions as F
from datetime import date, timedelta, datetime

# Schemi e tabelle: samples è in sola lettura, workspace.libro_python è lo schema di lavoro
SOURCE_SCHEMA = "samples.wanderbricks"
WORK_SCHEMA = "workspace.libro_python"
SOURCE_BOOKINGS_TABLE = f"{SOURCE_SCHEMA}.bookings"   # prenotazioni originali
PROPERTIES_TABLE = f"{SOURCE_SCHEMA}.properties"
DESTINATIONS_TABLE = f"{SOURCE_SCHEMA}.destinations"
COUNTRIES_TABLE = f"{SOURCE_SCHEMA}.countries"
SUPPORT_LOGS_TABLE = f"{SOURCE_SCHEMA}.customer_support_logs"
BOOKINGS_TABLE = f"{WORK_SCHEMA}.b_bookings"           # copia didattica con anomalie (Capitolo 0)

ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %
MIN_BOOKINGS = 20                    # prenotazioni minime perché un tasso sia valutabile (sezione 9.8)

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
GUIDE_PROPERTY_IDS = [11670, 16317, 16225]

# DataFrame delle tabelle (ricette: nessun dato viene ancora letto)
bookings_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")
properties_df = spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")
destinations_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE}")
countries_df = spark.sql(f"SELECT * FROM {COUNTRIES_TABLE}")
teaching_bookings_df = spark.sql(f"SELECT * FROM {BOOKINGS_TABLE}")

print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.1 Le funzioni di Spark: F e F.col

# COMMAND ----------

import pyspark.sql.functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 735.83
# MAGIC Column<'sum(base_price)'>
# MAGIC ```

# COMMAND ----------

print(sum([284.97, 213.91, 236.95]))
print(F.sum("base_price"))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC Column<'base_price'>
# MAGIC Column<'base_price'>
# MAGIC ```

# COMMAND ----------

print(F.col("base_price"))
print(properties_df["base_price"])

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 4
# MAGIC 185
# MAGIC ```

# COMMAND ----------

amalfi_2024_df = bookings_df.filter(
    (F.col("property_id") == 16225)
    & (F.col("check_in") >= date(ANALYSIS_YEAR, 1, 1))
    & (F.col("check_in") <= date(ANALYSIS_YEAR, 12, 31))
)
print(amalfi_2024_df.count())
print(properties_df.filter(F.col("property_type") == "Ski Resort").count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.2 Nuove colonne: withColumn, F.lit e alias

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_id  check_in    check_out   total_amount  status
# MAGIC 24996       2024-06-28  2024-07-01  914.47        pending
# MAGIC 52528       2024-07-21  2024-07-26  709.36        cancelled
# MAGIC 57340       2024-08-23  2024-08-26  865.17        pending
# MAGIC 12488       2024-08-30  2024-09-05  407.92        cancelled
# MAGIC ```

# COMMAND ----------

amalfi_df = (
    amalfi_2024_df
    .select("booking_id", "check_in", "check_out", "total_amount", "status")
    .orderBy("check_in")
)
display(amalfi_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_id  check_in    check_out   total_amount  status     nights
# MAGIC 24996       2024-06-28  2024-07-01  914.47        pending    3
# MAGIC 52528       2024-07-21  2024-07-26  709.36        cancelled  5
# MAGIC 57340       2024-08-23  2024-08-26  865.17        pending    3
# MAGIC 12488       2024-08-30  2024-09-05  407.92        cancelled  6
# MAGIC ```

# COMMAND ----------

amalfi_nights_df = amalfi_df.withColumn("nights", F.datediff(F.col("check_out"), F.col("check_in")))
display(amalfi_nights_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT booking_id, check_in, check_out, total_amount, status,
# MAGIC        datediff(check_out, check_in) AS nights
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id = 16225
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC ORDER BY check_in

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_id  nights  amount_per_night  check_in_month  check_in_weekday  status_label  source
# MAGIC 24996       3       304.82            6               6                 PENDING       wanderbricks
# MAGIC 52528       5       141.87            7               1                 CANCELLED     wanderbricks
# MAGIC 57340       3       288.39            8               6                 PENDING       wanderbricks
# MAGIC 12488       6       67.99             8               6                 CANCELLED     wanderbricks
# MAGIC ```

# COMMAND ----------

amalfi_report_df = (
    amalfi_df
    .withColumn("nights", F.datediff(F.col("check_out"), F.col("check_in")))
    .withColumn("amount_per_night", F.round(F.col("total_amount") / F.col("nights"), 2))
    .withColumn("check_in_month", F.month(F.col("check_in")))
    .withColumn("check_in_weekday", F.dayofweek(F.col("check_in")))
    .withColumn("status_label", F.upper(F.col("status")))
    .withColumn("source", F.lit("wanderbricks"))
)
display(amalfi_report_df.select("booking_id", "nights", "amount_per_night", "check_in_month", "check_in_weekday", "status_label", "source"))

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (il secondo argomento di withColumn deve essere una colonna).

# COMMAND ----------

# ERRORE VOLUTO – il secondo argomento di withColumn deve essere una colonna
amalfi_source_df = amalfi_df.withColumn("source", "wanderbricks")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il valore fisso con `F.lit()`. Risultato atteso: `['booking_id', 'check_in', 'check_out', 'total_amount', 'status', 'source']`.

# COMMAND ----------

# Correzione: il valore fisso diventa una colonna con F.lit()
amalfi_source_df = amalfi_df.withColumn("source", F.lit("wanderbricks"))
print(amalfi_source_df.columns)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_id  check_in    check_out   total_amount  status
# MAGIC 24996       2024-06-28  2024-07-01  914           pending
# MAGIC 52528       2024-07-21  2024-07-26  709           cancelled
# MAGIC 57340       2024-08-23  2024-08-26  865           pending
# MAGIC 12488       2024-08-30  2024-09-05  408           cancelled
# MAGIC ```

# COMMAND ----------

rounded_df = amalfi_df.withColumn("total_amount", F.round(F.col("total_amount"), 0))
display(rounded_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_id  amount_with_fee  round((total_amount * 1.1), 2)
# MAGIC 24996       1005.92          1005.92
# MAGIC 52528       780.3            780.3
# MAGIC 57340       951.69           951.69
# MAGIC 12488       448.71           448.71
# MAGIC ```

# COMMAND ----------

display(
    amalfi_df.select(
        "booking_id",
        F.round(F.col("total_amount") * 1.1, 2).alias("amount_with_fee"),
        F.round(F.col("total_amount") * 1.1, 2),
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.3 Date e tipi: F.to_date e cast

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC root
# MAGIC  |-- booking_id: long (nullable = true)
# MAGIC  |-- check_in: string (nullable = true)
# MAGIC  |-- check_out: string (nullable = true)
# MAGIC  |-- total_amount: string (nullable = true)
# MAGIC ```

# COMMAND ----------

raw_amalfi_df = spark.createDataFrame([
    {"booking_id": 24996, "check_in": "28/06/2024", "check_out": "01/07/2024", "total_amount": "914.47"},
    {"booking_id": 52528, "check_in": "21/07/2024", "check_out": "26/07/2024", "total_amount": "709.36"},
    {"booking_id": 57340, "check_in": "23/08/2024", "check_out": "26/08/2024", "total_amount": "865.17"},
    {"booking_id": 12488, "check_in": "30/08/2024", "check_out": "05/09/2024", "total_amount": "407.92"},
])
raw_amalfi_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC root
# MAGIC  |-- booking_id: long (nullable = true)
# MAGIC  |-- check_in: date (nullable = true)
# MAGIC  |-- check_out: date (nullable = true)
# MAGIC  |-- total_amount: double (nullable = true)
# MAGIC
# MAGIC booking_id  check_in    check_out   total_amount  nights
# MAGIC 24996       2024-06-28  2024-07-01  914.47        3
# MAGIC 52528       2024-07-21  2024-07-26  709.36        5
# MAGIC 57340       2024-08-23  2024-08-26  865.17        3
# MAGIC 12488       2024-08-30  2024-09-05  407.92        6
# MAGIC ```

# COMMAND ----------

amalfi_dates_df = (
    raw_amalfi_df
    .withColumn("check_in", F.to_date(F.col("check_in"), "dd/MM/yyyy"))
    .withColumn("check_out", F.to_date(F.col("check_out"), "dd/MM/yyyy"))
    .withColumn("total_amount", F.col("total_amount").cast("double"))
)
amalfi_dates_df.printSchema()
display(amalfi_dates_df.withColumn("nights", F.datediff(F.col("check_out"), F.col("check_in"))))

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente non dà errori ma produce un risultato sbagliato (mm sono i minuti, non il mese):
# MAGIC ```
# MAGIC booking_id  check_in    check_out   total_amount  nights
# MAGIC 24996       2024-01-28  2024-01-01  914.47        -27
# MAGIC 52528       2024-01-21  2024-01-26  709.36        5
# MAGIC 57340       2024-01-23  2024-01-26  865.17        3
# MAGIC 12488       2024-01-30  2024-01-05  407.92        -25
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – mm sono i minuti, non il mese
wrong_dates_df = (
    raw_amalfi_df
    .withColumn("check_in", F.to_date(F.col("check_in"), "dd/mm/yyyy"))
    .withColumn("check_out", F.to_date(F.col("check_out"), "dd/mm/yyyy"))
)
display(wrong_dates_df.withColumn("nights", F.datediff(F.col("check_out"), F.col("check_in"))))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il mese si scrive `MM`. Risultato atteso: le date di giugno, luglio, agosto e settembre e le notti `3 5 3 6`.

# COMMAND ----------

# Correzione: MM è il mese, mm i minuti
right_dates_df = (
    raw_amalfi_df
    .withColumn("check_in", F.to_date(F.col("check_in"), "dd/MM/yyyy"))
    .withColumn("check_out", F.to_date(F.col("check_out"), "dd/MM/yyyy"))
)
display(right_dates_df.withColumn("nights", F.datediff(F.col("check_out"), F.col("check_in"))))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC root
# MAGIC  |-- ticket_id: string (nullable = true)
# MAGIC  |-- created_at: string (nullable = true)
# MAGIC
# MAGIC 1900 658
# MAGIC ```

# COMMAND ----------

logs_df = spark.sql(f"SELECT ticket_id, created_at FROM {SUPPORT_LOGS_TABLE}")
logs_df.printSchema()
logs_2024_count = (
    logs_df
    .withColumn("created_date", F.to_date(F.col("created_at")))
    .filter(F.year(F.col("created_date")) == ANALYSIS_YEAR)
    .count()
)
print(logs_df.count(), logs_2024_count)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC +-----------+----------+--------------+------------------+-------------+
# MAGIC |property_id|base_price|base_price_int| base_price_double|property_code|
# MAGIC +-----------+----------+--------------+------------------+-------------+
# MAGIC |      11670|    284.97|           284| 284.9700012207031|        11670|
# MAGIC |      16225|    236.95|           236| 236.9499969482422|        16225|
# MAGIC |      16317|    213.91|           213|213.91000366210938|        16317|
# MAGIC +-----------+----------+--------------+------------------+-------------+
# MAGIC
# MAGIC root
# MAGIC  |-- property_id: long (nullable = false)
# MAGIC  |-- base_price: float (nullable = true)
# MAGIC  |-- base_price_int: integer (nullable = true)
# MAGIC  |-- base_price_double: double (nullable = true)
# MAGIC  |-- property_code: string (nullable = true)
# MAGIC ```

# COMMAND ----------

guide_prices_df = (
    properties_df
    .filter(
        (F.col("property_id") == 11670)
        | (F.col("property_id") == 16317)
        | (F.col("property_id") == 16225)
    )
    .select(
        "property_id",
        "base_price",
        F.col("base_price").cast("int").alias("base_price_int"),
        F.col("base_price").cast("double").alias("base_price_double"),
        F.col("property_id").cast("string").alias("property_code"),
    )
    .orderBy("property_id")
)
guide_prices_df.show()
guide_prices_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC ok_date     wrong_date  amount  price_int
# MAGIC 2024-06-28  2024-01-28  914.47  284
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT to_date('28/06/2024', 'dd/MM/yyyy') AS ok_date,
# MAGIC        to_date('28/06/2024', 'dd/mm/yyyy') AS wrong_date,
# MAGIC        CAST('914.47' AS DOUBLE)            AS amount,
# MAGIC        CAST(284.97 AS INT)                 AS price_int

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.4 Condizioni sulle colonne: F.when e otherwise

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC property_id  base_price  price_band
# MAGIC 11670        284.97      alto
# MAGIC 16225        236.95      medio
# MAGIC 16317        213.91      medio
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, base_price,
# MAGIC        CASE WHEN base_price >= 250 THEN 'alto'
# MAGIC             WHEN base_price >= 200 THEN 'medio'
# MAGIC             ELSE 'basso'
# MAGIC        END AS price_band
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  base_price  price_band
# MAGIC 11670        284.97      alto
# MAGIC 16225        236.95      medio
# MAGIC 16317        213.91      medio
# MAGIC ```

# COMMAND ----------

guide_bands_df = (
    properties_df
    .filter(
        (F.col("property_id") == 11670)
        | (F.col("property_id") == 16317)
        | (F.col("property_id") == 16225)
    )
    .select("property_id", "base_price")
    .withColumn(
        "price_band",
        F.when(F.col("base_price") >= 250, "alto")
        .when(F.col("base_price") >= 200, "medio")
        .otherwise("basso")
    )
    .orderBy("property_id")
)
display(guide_bands_df)

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente non dà errori ma produce un risultato sbagliato (la condizione più larga è scritta per prima):
# MAGIC ```
# MAGIC property_id  base_price  price_band
# MAGIC 11670        284.97      medio
# MAGIC 16225        236.95      medio
# MAGIC 16317        213.91      medio
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – la condizione più larga è scritta per prima
wrong_bands_df = guide_bands_df.withColumn(
    "price_band",
    F.when(F.col("base_price") >= 200, "medio")
    .when(F.col("base_price") >= 250, "alto")
    .otherwise("basso")
)
display(wrong_bands_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: dalla condizione più stretta alla più larga. Risultato atteso: `alto`, `medio`, `medio`.

# COMMAND ----------

# Correzione: prima >= 250, poi >= 200
right_bands_df = guide_bands_df.withColumn(
    "price_band",
    F.when(F.col("base_price") >= 250, "alto")
    .when(F.col("base_price") >= 200, "medio")
    .otherwise("basso")
)
display(right_bands_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  base_price  price_band  is_expensive
# MAGIC 11670        284.97      alto        sì
# MAGIC 16225        236.95      medio       null
# MAGIC 16317        213.91      medio       null
# MAGIC ```

# COMMAND ----------

display(guide_bands_df.withColumn("is_expensive", F.when(F.col("base_price") >= 250, "sì")))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_id  check_in    check_in_weekday  arrival_type
# MAGIC 24996       2024-06-28  6                 fine settimana
# MAGIC 52528       2024-07-21  1                 infrasettimanale
# MAGIC 57340       2024-08-23  6                 fine settimana
# MAGIC 12488       2024-08-30  6                 fine settimana
# MAGIC ```

# COMMAND ----------

weekend_arrival = (F.col("check_in_weekday") == 6) | (F.col("check_in_weekday") == 7)

amalfi_arrivals_df = amalfi_report_df.withColumn(
    "arrival_type",
    F.when(weekend_arrival, "fine settimana").otherwise("infrasettimanale")
)
display(amalfi_arrivals_df.select("booking_id", "check_in", "check_in_weekday", "arrival_type"))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  cancellation_rate  cancellation_status
# MAGIC 11670        0                  ok
# MAGIC 16317        14.3               ok
# MAGIC 16225        50                 critico
# MAGIC 99998        null               dato mancante
# MAGIC 99999        120                valore impossibile
# MAGIC ```

# COMMAND ----------

rates_df = spark.createDataFrame([
    {"property_id": 11670, "cancellation_rate": 0.0},
    {"property_id": 16317, "cancellation_rate": 14.3},
    {"property_id": 16225, "cancellation_rate": 50.0},
    {"property_id": 99998, "cancellation_rate": None},
    {"property_id": 99999, "cancellation_rate": 120.0},
]).select("property_id", "cancellation_rate")

rate_status = (
    F.when(F.col("cancellation_rate").isNull(), "dato mancante")
    .when((F.col("cancellation_rate") < 0) | (F.col("cancellation_rate") > 100), "valore impossibile")
    .when(F.col("cancellation_rate") > CANCELLATION_RATE_THRESHOLD, "critico")
    .otherwise("ok")
)
display(rates_df.withColumn("cancellation_status", rate_status))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.5 Raggruppare: groupBy e agg

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `13586`.

# COMMAND ----------

bookings_2024_df = bookings_df.filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
print(bookings_2024_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC status     booking_count
# MAGIC pending    6015
# MAGIC confirmed  3491
# MAGIC cancelled  2647
# MAGIC completed  1433
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status, COUNT(*) AS booking_count
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE year(check_in) = 2024
# MAGIC GROUP BY status
# MAGIC ORDER BY booking_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC status     booking_count
# MAGIC pending    6015
# MAGIC confirmed  3491
# MAGIC cancelled  2647
# MAGIC completed  1433
# MAGIC ```

# COMMAND ----------

status_2024_df = (
    bookings_2024_df
    .groupBy("status")
    .agg(F.count("*").alias("booking_count"))
    .orderBy(F.col("booking_count").desc())
)
display(status_2024_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC status     booking_count  property_count  revenue     avg_amount
# MAGIC pending    6015           3988            3305872.47  549.6
# MAGIC confirmed  3491           2754            1941435.37  556.13
# MAGIC cancelled  2647           2202            1462553     552.53
# MAGIC completed  1433           1311            791628.83   552.43
# MAGIC ```

# COMMAND ----------

status_summary_df = (
    bookings_2024_df
    .groupBy("status")
    .agg(
        F.count("*").alias("booking_count"),
        F.countDistinct("property_id").alias("property_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
        F.round(F.avg("total_amount"), 2).alias("avg_amount"),
    )
    .orderBy(F.col("booking_count").desc())
)
display(status_summary_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status,
# MAGIC        COUNT(*)                     AS booking_count,
# MAGIC        COUNT(DISTINCT property_id)  AS property_count,
# MAGIC        ROUND(SUM(total_amount), 2)  AS revenue,
# MAGIC        ROUND(AVG(total_amount), 2)  AS avg_amount
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE year(check_in) = 2024
# MAGIC GROUP BY status
# MAGIC ORDER BY booking_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  booking_count  cancelled_count  revenue  cancellation_rate
# MAGIC 11670        6              0                3966.21  0
# MAGIC 16225        4              2                2896.92  50
# MAGIC 16317        7              1                5139.59  14.3
# MAGIC ```

# COMMAND ----------

guide_summary_df = (
    bookings_2024_df
    .filter(
        (F.col("property_id") == 11670)
        | (F.col("property_id") == 16317)
        | (F.col("property_id") == 16225)
    )
    .groupBy("property_id")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
    )
    .withColumn("cancellation_rate", F.round(F.col("cancelled_count") / F.col("booking_count") * 100, 1))
    .orderBy("property_id")
)
display(guide_summary_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_type     property_count  avg_price  min_price  max_price
# MAGIC Urban Year-Round  9264            173.04     82.2       561.97
# MAGIC Summer Getaway    7068            198.54     101.01     517.6
# MAGIC Historical Place  1646            147.46     55.93      330.19
# MAGIC Ski Resort        185             266.49     143.95     530.96
# MAGIC ```

# COMMAND ----------

type_prices_df = (
    properties_df
    .groupBy("property_type")
    .agg(
        F.count("*").alias("property_count"),
        F.round(F.avg("base_price"), 2).alias("avg_price"),
        F.min("base_price").alias("min_price"),
        F.max("base_price").alias("max_price"),
    )
    .orderBy(F.col("property_count").desc())
)
display(type_prices_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT destination_id, COUNT(*) AS property_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY destination_id
# MAGIC HAVING COUNT(*) > 1000
# MAGIC ORDER BY property_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination_id  property_count
# MAGIC 3800            1788
# MAGIC 3300            1626
# MAGIC 2400            1624
# MAGIC 3750            1440
# MAGIC 1000            1103
# MAGIC ```

# COMMAND ----------

large_destinations_df = (
    properties_df
    .groupBy("destination_id")
    .agg(F.count("*").alias("property_count"))
    .filter(F.col("property_count") > 1000)
    .orderBy(F.col("property_count").desc())
)
display(large_destinations_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `<class 'pyspark.sql.connect.group.GroupedData'>`.

# COMMAND ----------

grouped = bookings_2024_df.groupBy("status")
print(type(grouped))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.6 Aggregare dati sporchi

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC row_count  amount_count  avg_amount
# MAGIC 13626      13596         551.11
# MAGIC ```

# COMMAND ----------

teaching_2024_df = teaching_bookings_df.filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)

display(
    teaching_2024_df.agg(
        F.count("*").alias("row_count"),
        F.count("total_amount").alias("amount_count"),
        F.round(F.avg("total_amount"), 2).alias("avg_amount"),
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC avg_all  avg_valid  valid_count
# MAGIC 551.11   552.17     13584
# MAGIC ```

# COMMAND ----------

valid_amount = F.when(F.col("total_amount") >= 0, F.col("total_amount"))

display(
    teaching_2024_df.agg(
        F.round(F.avg("total_amount"), 2).alias("avg_all"),
        F.round(F.avg(valid_amount), 2).alias("avg_valid"),
        F.count(valid_amount).alias("valid_count"),
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC avg_all  avg_valid  valid_count
# MAGIC 551.11   552.17     13584
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ROUND(AVG(total_amount), 2)                                         AS avg_all,
# MAGIC        ROUND(AVG(CASE WHEN total_amount >= 0 THEN total_amount END), 2)    AS avg_valid,
# MAGIC        COUNT(CASE WHEN total_amount >= 0 THEN total_amount END)            AS valid_count
# MAGIC FROM workspace.libro_python.b_bookings
# MAGIC WHERE year(check_in) = 2024

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC booking_count  booking_ids  valid_count  revenue     avg_amount
# MAGIC 13586          13586        13544        7477734.15  552.11
# MAGIC ```

# COMMAND ----------

clean_2024_df = teaching_2024_df.distinct()

display(
    clean_2024_df.agg(
        F.count("*").alias("booking_count"),
        F.countDistinct("booking_id").alias("booking_ids"),
        F.count(valid_amount).alias("valid_count"),
        F.round(F.sum(valid_amount), 2).alias("revenue"),
        F.round(F.avg(valid_amount), 2).alias("avg_amount"),
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.7 Unire tabelle: join

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC property_id  title                  destination_id  destination  country
# MAGIC 11670        Historic Inn in Rome   3900            Rome         Italy
# MAGIC 16225        Beach House in Amalfi  1100            Amalfi       Italy
# MAGIC 16317        Bungalow in Sardinia   4200            Sardinia     Italy
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT p.property_id, p.title, p.destination_id, d.destination, d.country
# MAGIC FROM samples.wanderbricks.properties p
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC WHERE p.property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY p.property_id

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination_id  property_id  title                  destination  country
# MAGIC 3900            11670        Historic Inn in Rome   Rome         Italy
# MAGIC 1100            16225        Beach House in Amalfi  Amalfi       Italy
# MAGIC 4200            16317        Bungalow in Sardinia   Sardinia     Italy
# MAGIC ```

# COMMAND ----------

destination_names_df = destinations_df.select("destination_id", "destination", "country")

guide_places_df = (
    properties_df
    .filter(
        (F.col("property_id") == 11670)
        | (F.col("property_id") == 16317)
        | (F.col("property_id") == 16225)
    )
    .select("property_id", "title", "destination_id")
    .join(destination_names_df, on="destination_id", how="inner")
    .orderBy("property_id")
)
display(guide_places_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 42 42
# MAGIC 18163 18163
# MAGIC ```

# COMMAND ----------

print(destination_names_df.count(), destination_names_df.select("destination_id").distinct().count())
print(properties_df.count(), properties_df.join(destination_names_df, on="destination_id", how="inner").count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination  country               booking_count  cancelled_count
# MAGIC Phuket       Thailand              1262           258
# MAGIC Paris        France                1149           225
# MAGIC Mallorca     Spain                 1126           217
# MAGIC Gold Coast   Australia             1069           214
# MAGIC Abu Dhabi    United Arab Emirates  871            166
# MAGIC
# MAGIC destination  country  booking_count  cancelled_count
# MAGIC Sardinia     Italy    311            63
# MAGIC Rome         Italy    294            56
# MAGIC Florence     Italy    58             11
# MAGIC Amalfi       Italy    51             12
# MAGIC ```

# COMMAND ----------

property_places_df = properties_df.select("property_id", "destination_id")

destination_2024_df = (
    bookings_2024_df
    .select("booking_id", "property_id", "status")
    .join(property_places_df, on="property_id", how="inner")
    .join(destination_names_df, on="destination_id", how="inner")
    .groupBy("destination", "country")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
    )
    .orderBy(F.col("booking_count").desc())
)
display(destination_2024_df.limit(5))
display(destination_2024_df.filter(F.col("country") == "Italy"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT d.destination, d.country,
# MAGIC        COUNT(*)                                                AS booking_count,
# MAGIC        SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count
# MAGIC FROM samples.wanderbricks.bookings b
# MAGIC JOIN samples.wanderbricks.properties p USING (property_id)
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC WHERE year(b.check_in) = 2024 AND d.country = 'Italy'
# MAGIC GROUP BY d.destination, d.country
# MAGIC ORDER BY booking_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `17724 439`.

# COMMAND ----------

booked_df = (
    bookings_df
    .select("property_id")
    .distinct()
    .withColumn("has_bookings", F.lit(True))
)

never_booked_df = (
    properties_df
    .select("property_id", "title", "property_type")
    .join(booked_df, on="property_id", how="left")
    .filter(F.col("has_bookings").isNull())
)
print(booked_df.count(), never_booked_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (con la condizione == la chiave compare due volte).

# COMMAND ----------

# ERRORE VOLUTO – con la condizione == la chiave compare due volte
joined_df = bookings_2024_df.join(properties_df, bookings_2024_df["property_id"] == properties_df["property_id"], how="inner")
display(joined_df.select("booking_id", "property_id", "title"))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `on="property_id"` e `select` prima del join. Risultato atteso: 13586 righe; le prime con `booking_id`, `property_id` e `title`.

# COMMAND ----------

# Correzione: chiave con on= e solo le colonne utili della tabella di destra
joined_df = bookings_2024_df.join(properties_df.select("property_id", "title"), on="property_id", how="inner")
print(joined_df.count())
display(joined_df.select("booking_id", "property_id", "title").limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.8 Una trasformazione completa

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 317
# MAGIC
# MAGIC cancellation_status  combination_count
# MAGIC critico              8
# MAGIC non valutabile       152
# MAGIC ok                   157
# MAGIC ```

# COMMAND ----------

cancellation_status = (
    F.when(F.col("booking_count") < MIN_BOOKINGS, "non valutabile")
    .when(F.col("cancellation_rate") > CANCELLATION_RATE_THRESHOLD, "critico")
    .otherwise("ok")
)

destination_month_df = (
    bookings_df
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)                 # 1. righe del 2024 (WHERE)
    .select("booking_id", "property_id", "check_in", "status")          # 2. solo le colonne utili
    .join(property_places_df, on="property_id", how="inner")           # 3. struttura → destinazione
    .join(destination_names_df, on="destination_id", how="inner")      # 4. destinazione → nome e paese
    .withColumn("check_in_month", F.month(F.col("check_in")))          # 5. mese di arrivo
    .groupBy("destination", "country", "check_in_month")               # 6. una riga per destinazione e mese
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
    )
    .withColumn("cancellation_rate", F.round(F.col("cancelled_count") / F.col("booking_count") * 100, 1))
    .withColumn("cancellation_status", cancellation_status)            # 7. stato con il volume minimo
)
print(destination_month_df.count())
display(destination_month_df.groupBy("cancellation_status").agg(F.count("*").alias("combination_count")).orderBy("cancellation_status"))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination  country               check_in_month  booking_count  cancelled_count  cancellation_rate  cancellation_status
# MAGIC Cairo        Egypt                 9               35             13               37.1               critico
# MAGIC London       United Kingdom        9               35             13               37.1               critico
# MAGIC Madrid       Spain                 4               21             7                33.3               critico
# MAGIC London       United Kingdom        11              37             12               32.4               critico
# MAGIC Dubai        United Arab Emirates  3               25             8                32                 critico
# MAGIC Barcelona    Spain                 8               44             14               31.8               critico
# MAGIC Cairo        Egypt                 12              45             14               31.1               critico
# MAGIC Byron Bay    Australia             8               53             16               30.2               critico
# MAGIC ```

# COMMAND ----------

critical_df = (
    destination_month_df
    .filter(F.col("cancellation_status") == "critico")                   # 8. solo le critiche (HAVING)
    .orderBy(F.col("cancellation_rate").desc(), "destination", "check_in_month")
)
display(critical_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination  country  check_in_month  booking_count  cancelled_count  cancellation_rate  cancellation_status
# MAGIC Amalfi       Italy    6               13              5                38.5               non valutabile
# MAGIC Amalfi       Italy    7               9               1                11.1               non valutabile
# MAGIC Amalfi       Italy    8               20              5                25                 ok
# MAGIC Amalfi       Italy    9               9               1                11.1               non valutabile
# MAGIC ```

# COMMAND ----------

display(destination_month_df.filter(F.col("destination") == "Amalfi").orderBy("check_in_month"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT d.destination, d.country,
# MAGIC        month(b.check_in)                                       AS check_in_month,
# MAGIC        COUNT(*)                                                AS booking_count,
# MAGIC        SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
# MAGIC        ROUND(SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS cancellation_rate
# MAGIC FROM samples.wanderbricks.bookings b
# MAGIC JOIN samples.wanderbricks.properties p USING (property_id)
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC WHERE year(b.check_in) = 2024
# MAGIC GROUP BY d.destination, d.country, month(b.check_in)
# MAGIC HAVING COUNT(*) >= 20
# MAGIC    AND SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100 > 30
# MAGIC ORDER BY cancellation_rate DESC, d.destination, check_in_month

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9.9 Errori comuni con le trasformazioni

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (and di Python al posto di &).

# COMMAND ----------

# ERRORE VOLUTO – and di Python al posto di &
ski_bands_df = properties_df.withColumn(
    "luxury_ski",
    F.when((F.col("property_type") == "Ski Resort") and (F.col("base_price") >= 250), "sì").otherwise("no")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `&` e ogni condizione tra parentesi. Risultato atteso: `106`.

# COMMAND ----------

# Correzione: & al posto di and
ski_bands_df = properties_df.withColumn(
    "luxury_ski",
    F.when((F.col("property_type") == "Ski Resort") & (F.col("base_price") >= 250), "sì").otherwise("no")
)
print(ski_bands_df.filter(F.col("luxury_ski") == "sì").count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (sum di Python al posto di F.sum).

# COMMAND ----------

# ERRORE VOLUTO – sum di Python al posto di F.sum
revenue_df = bookings_2024_df.groupBy("status").agg(sum("total_amount"))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `F.sum` con il prefisso. Risultato atteso: i ricavi per stato della sezione 9.5 (pending 3305872.47, confirmed 1941435.37, cancelled 1462553, completed 791628.83).

# COMMAND ----------

# Correzione: la sum di Spark, con il prefisso F.
revenue_df = bookings_2024_df.groupBy("status").agg(F.round(F.sum("total_amount"), 2).alias("revenue"))
display(revenue_df.orderBy(F.col("revenue").desc()))

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (dopo groupBy manca agg).

# COMMAND ----------

# ERRORE VOLUTO – dopo groupBy manca agg
status_df = bookings_2024_df.groupBy("status").orderBy("status")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: prima `agg`, poi `orderBy`. Risultato atteso: `cancelled 2647`, `completed 1433`, `confirmed 3491`, `pending 6015`.

# COMMAND ----------

# Correzione: groupBy seguito da agg, poi i metodi del DataFrame
status_df = bookings_2024_df.groupBy("status").agg(F.count("*").alias("booking_count")).orderBy("status")
display(status_df)

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (l'aggregazione non ha un alias).

# COMMAND ----------

# ERRORE VOLUTO – l'aggregazione non ha un alias
large_df = (
    properties_df
    .groupBy("destination_id")
    .agg(F.count("*"))
    .filter(F.col("property_count") > 1000)
)
display(large_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: un `alias` per l'aggregazione. Risultato atteso: le cinque destinazioni con più di 1000 strutture (3800, 3300, 2400, 3750, 1000).

# COMMAND ----------

# Correzione: ogni aggregazione con un nome
large_df = (
    properties_df
    .groupBy("destination_id")
    .agg(F.count("*").alias("property_count"))
    .filter(F.col("property_count") > 1000)
)
display(large_df.orderBy(F.col("property_count").desc()))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC degli errori silenziosi
# MAGIC
# MAGIC Gli errori silenziosi di questo capitolo producono tutti un risultato plausibile: `mm` al posto di `MM` in un formato (date spostate a gennaio, sezione 9.3); le condizioni di `when` dalla più larga alla più stretta (una fascia vuota, sezione 9.4); un `filter` sui valori al posto di `F.when` senza `otherwise` (righe perse, sezione 9.6); un'aggregazione su righe ripetute, senza `distinct()` (conteggi e somme gonfiati, sezione 9.6); un join con una tabella di decodifica che ha chiavi ripetute (righe moltiplicate, sezione 9.7); un tasso valutato su pochi casi (falsi allarmi, sezione 9.8). La difesa resta quella dei Capitoli 6 e 8: sapere prima che risultato aspettarsi, contare le righe prima e dopo ogni join, confrontare il risultato con una query SQL scritta a parte.
# MAGIC
# MAGIC ## Errori comuni
# MAGIC
# MAGIC | Tipo di errore | Messaggio tipico | Significato | Prima cosa da controllare |
# MAGIC | --- | --- | --- | --- |
# MAGIC | `NOT_COLUMN` | ``Argument `col` should be a Column, got str`` | un valore fisso dove serve una colonna | `F.lit()` attorno al valore |
# MAGIC | `CANNOT_CONVERT_COLUMN_INTO_BOOL` | `Cannot convert column into bool` | una condizione di colonna usata come vero/falso | `&`, `\|`, `~` al posto di `and`, `or`, `not`; le parentesi; un `if` al posto di `F.when` |
# MAGIC | `TypeError` | `unsupported operand type(s) for +: 'int' and 'str'` | una funzione di Python al posto di quella di Spark | il prefisso `F.` (`F.sum`, `F.round`, `F.min`, `F.max`) |
# MAGIC | `AttributeError` | `'GroupedData' object has no attribute 'orderBy'` | `groupBy` senza `agg` | l'`agg()` dopo `groupBy()` |
# MAGIC | `UNRESOLVED_COLUMN` | ``... with name `property_count` cannot be resolved ... [`count(1)`, ...]`` | una colonna che non esiste, spesso un'aggregazione senza nome | l'`alias()` di ogni aggregazione; i suggerimenti del messaggio |
# MAGIC | `AMBIGUOUS_REFERENCE` | ``Reference `property_id` is ambiguous`` | due colonne con lo stesso nome dopo un join | `on="colonna"` al posto della condizione `==`; `select` prima del join |
# MAGIC | `CAST_INVALID_INPUT`, `CANNOT_PARSE_TIMESTAMP` | `... could not be parsed ...` | un testo non convertibile | i valori della colonna; il formato di `F.to_date` |
# MAGIC | (nessun errore) | date tutte a gennaio | minuti al posto del mese | `MM` (mese) e `mm` (minuti) nel formato |
# MAGIC | (nessun errore) | una fascia o uno stato che non compare mai | condizioni di `when` nell'ordine sbagliato | dalla condizione più stretta alla più larga |
# MAGIC | (nessun errore) | conteggi più alti del previsto | righe ripetute o chiavi ripetute nel join | `count()` contro `countDistinct` della chiave; righe prima e dopo il join |
