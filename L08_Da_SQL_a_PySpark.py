# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 8 – Da SQL a PySpark
# MAGIC
# MAGIC Notebook del Capitolo 8 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Eseguire query SQL da Python con `spark.sql()`, anche con f-string
# MAGIC - Capire il DataFrame come ricetta: operazioni che preparano e azioni (`display`, `show`, `count`, `collect`)
# MAGIC - Guardare un DataFrame con `display()`, `show()`, `printSchema()`, `columns`
# MAGIC - Usare `select`, `distinct`, `filter`, `orderBy`, `limit` al posto delle clausole SQL
# MAGIC - Portare risultati piccoli in Python con `collect()` e tornare a Spark con `spark.createDataFrame()`
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–7; notebook collegato al compute **Serverless**
# MAGIC - `L00_Prepara_Dati` già eseguito (le sezioni 8.7–8.8 leggono `workspace.libro_python.b_bookings`); nessuna cella scrive tabelle
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

# Cella di preparazione: import, costanti e valori usati nelle sezioni
from datetime import date, timedelta, datetime

# Schemi e tabelle: samples è in sola lettura, workspace.libro_python è lo schema di lavoro
SOURCE_SCHEMA = "samples.wanderbricks"
WORK_SCHEMA = "workspace.libro_python"
SOURCE_BOOKINGS_TABLE = f"{SOURCE_SCHEMA}.bookings"   # prenotazioni originali
PROPERTIES_TABLE = f"{SOURCE_SCHEMA}.properties"
DESTINATIONS_TABLE = f"{SOURCE_SCHEMA}.destinations"
BOOKINGS_TABLE = f"{WORK_SCHEMA}.b_bookings"           # copia didattica con anomalie (Capitolo 0)

ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
GUIDE_PROPERTY_IDS = [11670, 16317, 16225]
guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]


def classify_cancellation_rate(rate, threshold=CANCELLATION_RATE_THRESHOLD):
    """Classifica un tasso di cancellazione (in %) in quattro stati, come nel Capitolo 5."""
    if rate is None:
        return "dato mancante"
    if rate < 0 or rate > 100:
        return "valore impossibile"
    if rate > threshold:
        return "critico"
    return "ok"


print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.1 Spark e la variabile spark

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `<class 'pyspark.sql.connect.session.SparkSession'>`.

# COMMAND ----------

print(type(spark))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `DataFrame[bookings_count: bigint]`.

# COMMAND ----------

spark.sql("SELECT COUNT(*) AS bookings_count FROM samples.wanderbricks.bookings")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC bookings_count
# MAGIC 72247
# MAGIC ```

# COMMAND ----------

display(spark.sql("SELECT COUNT(*) AS bookings_count FROM samples.wanderbricks.bookings"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC bookings_count
# MAGIC 72247
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS bookings_count
# MAGIC FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.2 La query come testo: triple virgolette e f-string

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC cancelled_count
# MAGIC 15285
# MAGIC ```

# COMMAND ----------

query = """
SELECT COUNT(*) AS cancelled_count
FROM samples.wanderbricks.bookings
WHERE status = 'cancelled'
"""
display(spark.sql(query))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC
# MAGIC SELECT COUNT(*) AS bookings_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id = 16225
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC
# MAGIC
# MAGIC bookings_2024
# MAGIC 4
# MAGIC ```

# COMMAND ----------

property_id = 16225
query = f"""
SELECT COUNT(*) AS bookings_2024
FROM {SOURCE_BOOKINGS_TABLE}
WHERE property_id = {property_id}
  AND check_in BETWEEN '{ANALYSIS_YEAR}-01-01' AND '{ANALYSIS_YEAR}-12-31'
"""
print(query)
display(spark.sql(query))

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (il valore di testo è inserito senza apici).

# COMMAND ----------

# ERRORE VOLUTO – il valore di testo è inserito senza apici
city = "Amalfi"
query = f"SELECT destination_id, destination FROM {DESTINATIONS_TABLE} WHERE destination = {city}"
display(spark.sql(query))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: gli apici attorno alle graffe. Risultato atteso: una riga, `1100 Amalfi`.

# COMMAND ----------

# Correzione: il testo va tra apici anche nella f-string
city = "Amalfi"
query = f"SELECT destination_id, destination FROM {DESTINATIONS_TABLE} WHERE destination = '{city}'"
display(spark.sql(query))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.3 Il DataFrame: ricetta e piatto

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC DataFrame[booking_id: bigint, user_id: bigint, property_id: bigint, check_in: date, check_out: date, guests_count: int, total_amount: float, status: string, created_at: timestamp, updated_at: timestamp]
# MAGIC ```

# COMMAND ----------

bookings_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")
bookings_df

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `<class 'pyspark.sql.connect.dataframe.DataFrame'>`.

# COMMAND ----------

print(type(bookings_df))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 72247
# MAGIC <class 'int'>
# MAGIC ```

# COMMAND ----------

bookings_count = bookings_df.count()
print(bookings_count)
print(type(bookings_count))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC Cancellate: 15285 su 72247 (21.2%)
# MAGIC ok
# MAGIC ```

# COMMAND ----------

cancelled_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE} WHERE status = 'cancelled'")
cancelled_count = cancelled_df.count()
cancellation_rate = cancelled_count / bookings_count * 100
print(f"Cancellate: {cancelled_count} su {bookings_count} ({cancellation_rate:.1f}%)")
print(classify_cancellation_rate(cancellation_rate))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC ['booking_id', 'user_id', 'property_id', 'check_in', 'check_out', 'guests_count', 'total_amount', 'status', 'created_at', 'updated_at']
# MAGIC 10
# MAGIC ```

# COMMAND ----------

print(bookings_df.columns)
print(len(bookings_df.columns))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.4 Guardare i dati: display, show e printSchema

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination_id  destination  country
# MAGIC 1100            Amalfi       Italy
# MAGIC 2300            Florence     Italy
# MAGIC 3900            Rome         Italy
# MAGIC 4200            Sardinia     Italy
# MAGIC ```

# COMMAND ----------

italy_df = spark.sql(f"""
SELECT destination_id, destination, country
FROM {DESTINATIONS_TABLE}
WHERE country = 'Italy'
ORDER BY destination_id
""")
display(italy_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC +--------------+-----------+-------+
# MAGIC |destination_id|destination|country|
# MAGIC +--------------+-----------+-------+
# MAGIC |          1100|     Amalfi|  Italy|
# MAGIC |          2300|   Florence|  Italy|
# MAGIC |          3900|       Rome|  Italy|
# MAGIC |          4200|   Sardinia|  Italy|
# MAGIC +--------------+-----------+-------+
# MAGIC ```

# COMMAND ----------

italy_df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC +-----------+--------------------+----------+
# MAGIC |property_id|               title|base_price|
# MAGIC +-----------+--------------------+----------+
# MAGIC |      11670|Historic Inn in Rome|    284.97|
# MAGIC |      16225|Beach House in Am...|    236.95|
# MAGIC |      16317|Bungalow in Sardinia|    213.91|
# MAGIC +-----------+--------------------+----------+
# MAGIC
# MAGIC +-----------+---------------------+----------+
# MAGIC |property_id|title                |base_price|
# MAGIC +-----------+---------------------+----------+
# MAGIC |11670      |Historic Inn in Rome |284.97    |
# MAGIC |16225      |Beach House in Amalfi|236.95    |
# MAGIC |16317      |Bungalow in Sardinia |213.91    |
# MAGIC +-----------+---------------------+----------+
# MAGIC ```

# COMMAND ----------

guide_titles_df = spark.sql(f"""
SELECT property_id, title, base_price
FROM {PROPERTIES_TABLE}
WHERE property_id IN (11670, 16317, 16225)
ORDER BY property_id
""")
guide_titles_df.show()
guide_titles_df.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC +--------------+-----------+-------+
# MAGIC |destination_id|destination|country|
# MAGIC +--------------+-----------+-------+
# MAGIC |          1100|     Amalfi|  Italy|
# MAGIC +--------------+-----------+-------+
# MAGIC only showing top 1 row
# MAGIC None
# MAGIC ```

# COMMAND ----------

result = italy_df.show(1)
print(result)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC root
# MAGIC  |-- booking_id: long (nullable = false)
# MAGIC  |-- user_id: long (nullable = true)
# MAGIC  |-- property_id: long (nullable = true)
# MAGIC  |-- check_in: date (nullable = true)
# MAGIC  |-- check_out: date (nullable = true)
# MAGIC  |-- guests_count: integer (nullable = true)
# MAGIC  |-- total_amount: float (nullable = true)
# MAGIC  |-- status: string (nullable = true)
# MAGIC  |-- created_at: timestamp (nullable = true)
# MAGIC  |-- updated_at: timestamp (nullable = true)
# MAGIC ```

# COMMAND ----------

bookings_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.5 Scegliere le colonne: select e distinct

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `18163 42`.

# COMMAND ----------

bookings_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")
properties_df = spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")
destinations_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE}")
print(properties_df.count(), destinations_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, title, property_type, base_price
# MAGIC FROM samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `['property_id', 'title', 'property_type', 'base_price']`.

# COMMAND ----------

property_prices_df = properties_df.select("property_id", "title", "property_type", "base_price")
print(property_prices_df.columns)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC Column<'base_price'>
# MAGIC <class 'pyspark.sql.connect.column.Column'>
# MAGIC ```

# COMMAND ----------

print(properties_df["base_price"])
print(type(properties_df["base_price"]))

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (la colonna si chiama base_price, non price).

# COMMAND ----------

# ERRORE VOLUTO – la colonna si chiama base_price, non price
prices_df = properties_df.select("property_id", "price")
display(prices_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il nome corretto della colonna. Risultato atteso: `['property_id', 'base_price']`.

# COMMAND ----------

# Correzione: la colonna si chiama base_price
prices_df = properties_df.select("property_id", "base_price")
print(prices_df.columns)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_type
# MAGIC Historical Place
# MAGIC Urban Year-Round
# MAGIC Summer Getaway
# MAGIC Ski Resort
# MAGIC
# MAGIC 4
# MAGIC ```

# COMMAND ----------

property_types_df = properties_df.select("property_type").distinct()
display(property_types_df)
print(property_types_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC property_types  countries
# MAGIC 4               18
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(DISTINCT property_type) AS property_types,
# MAGIC        (SELECT COUNT(DISTINCT country) FROM samples.wanderbricks.destinations) AS countries
# MAGIC FROM samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.6 Filtrare le righe: filter e where

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `185`.

# COMMAND ----------

ski_df = properties_df.filter("property_type = 'Ski Resort'")
print(ski_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `185`.

# COMMAND ----------

ski_df = properties_df.filter(properties_df["property_type"] == "Ski Resort")
print(ski_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `Column<'==(property_type, Ski Resort)'>`.

# COMMAND ----------

print(properties_df["property_type"] == "Ski Resort")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `1646 1646`.

# COMMAND ----------

chosen_type = "Historical Place"
text_df = properties_df.filter(f"property_type = '{chosen_type}'")
column_df = properties_df.filter(properties_df["property_type"] == chosen_type)
print(text_df.count(), column_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC historical_count
# MAGIC 1646
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS historical_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_type = 'Historical Place'

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 15285
# MAGIC 40672
# MAGIC 0
# MAGIC ```

# COMMAND ----------

print(bookings_df.filter(bookings_df["status"] == "cancelled").count())
print(bookings_df.filter(bookings_df["status"] != "pending").count())
print(bookings_df.filter(bookings_df["check_in"] > date(2025, 7, 30)).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.7 Condizioni multiple e valori nulli

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC Prenotazioni 2024: 4 - cancellate: 2 - tasso: 50.0%
# MAGIC critico
# MAGIC ```

# COMMAND ----------

amalfi_2024_df = bookings_df.filter(
    (bookings_df["property_id"] == 16225)
    & (bookings_df["check_in"] >= date(ANALYSIS_YEAR, 1, 1))
    & (bookings_df["check_in"] <= date(ANALYSIS_YEAR, 12, 31))
)
amalfi_bookings = amalfi_2024_df.count()
amalfi_cancelled = amalfi_2024_df.filter(amalfi_2024_df["status"] == "cancelled").count()
amalfi_rate = amalfi_cancelled / amalfi_bookings * 100
print(f"Prenotazioni 2024: {amalfi_bookings} - cancellate: {amalfi_cancelled} - tasso: {amalfi_rate:.1f}%")
print(classify_cancellation_rate(amalfi_rate))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC bookings_2024  cancelled_2024
# MAGIC 4              2
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS bookings_2024,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id = 16225
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `1831 40672`.

# COMMAND ----------

historic_or_ski_df = properties_df.filter(
    (properties_df["property_type"] == "Historical Place")
    | (properties_df["property_type"] == "Ski Resort")
)
not_pending_df = bookings_df.filter(~(bookings_df["status"] == "pending"))
print(historic_or_ski_df.count(), not_pending_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (senza parentesi | viene calcolato prima di ==).

# COMMAND ----------

# ERRORE VOLUTO – senza parentesi | viene calcolato prima di ==
historic_or_ski_df = properties_df.filter(properties_df["property_type"] == "Historical Place" | properties_df["property_type"] == "Ski Resort")
print(historic_or_ski_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: ogni confronto tra parentesi. Risultato atteso: `1831`.

# COMMAND ----------

# Correzione: ogni condizione tra parentesi
historic_or_ski_df = properties_df.filter(
    (properties_df["property_type"] == "Historical Place")
    | (properties_df["property_type"] == "Ski Resort")
)
print(historic_or_ski_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `72287 30 72257`.

# COMMAND ----------

teaching_bookings_df = spark.sql(f"SELECT * FROM {BOOKINGS_TABLE}")
missing_amount_df = teaching_bookings_df.filter(teaching_bookings_df["total_amount"].isNull())
present_amount_df = teaching_bookings_df.filter(teaching_bookings_df["total_amount"].isNotNull())
print(teaching_bookings_df.count(), missing_amount_df.count(), present_amount_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente non dà errori ma produce un risultato sbagliato (il confronto con None non trova mai nessuna riga): `0`.

# COMMAND ----------

# ERRORE SILENZIOSO – il confronto con None non trova mai nessuna riga
wrong_missing_df = teaching_bookings_df.filter(teaching_bookings_df["total_amount"] == None)
print(wrong_missing_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `isNull()`. Risultato atteso: `30`.

# COMMAND ----------

# Correzione: i valori mancanti si cercano con isNull()
print(teaching_bookings_df.filter(teaching_bookings_df["total_amount"].isNull()).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 13
# MAGIC 43
# MAGIC ```

# COMMAND ----------

amount_problems_df = teaching_bookings_df.filter(
    (teaching_bookings_df["total_amount"].isNull())
    | (teaching_bookings_df["total_amount"] < 0)
)
print(teaching_bookings_df.filter(teaching_bookings_df["total_amount"] < 0).count())
print(amount_problems_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `8 40`.

# COMMAND ----------

inverted_df = teaching_bookings_df.filter(teaching_bookings_df["check_out"] < teaching_bookings_df["check_in"])
duplicate_rows = teaching_bookings_df.count() - teaching_bookings_df.distinct().count()
print(inverted_df.count(), duplicate_rows)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC row_count  missing_amounts  negative_amounts  inverted_dates  duplicate_rows
# MAGIC 72287      30               13                8               40
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)                                                     AS row_count,
# MAGIC        SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END)        AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)            AS negative_amounts,
# MAGIC        SUM(CASE WHEN check_out < check_in THEN 1 ELSE 0 END)        AS inverted_dates,
# MAGIC        COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM workspace.libro_python.b_bookings)) AS duplicate_rows
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.8 Ordinare e limitare: orderBy e limit

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  title                  base_price
# MAGIC 11670        Historic Inn in Rome   284.97
# MAGIC 16225        Beach House in Amalfi  236.95
# MAGIC 16317        Bungalow in Sardinia   213.91
# MAGIC ```

# COMMAND ----------

guide_df = properties_df.filter(
    (properties_df["property_id"] == 11670)
    | (properties_df["property_id"] == 16317)
    | (properties_df["property_id"] == 16225)
)
display(guide_df.select("property_id", "title", "base_price").orderBy("base_price", ascending=False))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC +------------+
# MAGIC |total_amount|
# MAGIC +------------+
# MAGIC |        NULL|
# MAGIC |        NULL|
# MAGIC |        NULL|
# MAGIC +------------+
# MAGIC only showing top 3 rows
# MAGIC ```

# COMMAND ----------

amounts_df = teaching_bookings_df.select("total_amount")
amounts_df.orderBy("total_amount").show(3)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC destination_id  destination  country
# MAGIC 1100            Amalfi       Italy
# MAGIC 2300            Florence     Italy
# MAGIC
# MAGIC 2
# MAGIC ```

# COMMAND ----------

first_italian_df = italy_df.orderBy("destination").limit(2)
display(first_italian_df)
print(first_italian_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.9 Concatenare le operazioni

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, title, property_type, base_price
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id = 11670 OR property_id = 16317 OR property_id = 16225
# MAGIC ORDER BY base_price DESC
# MAGIC LIMIT 3

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  title                  property_type     base_price
# MAGIC 11670        Historic Inn in Rome   Historical Place  284.97
# MAGIC 16225        Beach House in Amalfi  Summer Getaway    236.95
# MAGIC 16317        Bungalow in Sardinia   Summer Getaway    213.91
# MAGIC ```

# COMMAND ----------

guide_report_df = (
    properties_df
    .filter(
        (properties_df["property_id"] == 11670)
        | (properties_df["property_id"] == 16317)
        | (properties_df["property_id"] == 16225)
    )
    .select("property_id", "title", "property_type", "base_price")
    .orderBy("base_price", ascending=False)
    .limit(3)
)
display(guide_report_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 18163
# MAGIC 3
# MAGIC 18163
# MAGIC ```

# COMMAND ----------

print(properties_df.count())
print(guide_report_df.count())
print(properties_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente non dà errori ma produce un risultato sbagliato (il risultato di filter() non è messo in una variabile): `18163`.

# COMMAND ----------

# ERRORE SILENZIOSO – il risultato di filter() non è messo in una variabile
ski_df = properties_df
ski_df.filter(ski_df["property_type"] == "Ski Resort")
print(ski_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il risultato si assegna. Risultato atteso: `185`.

# COMMAND ----------

# Correzione: il risultato di filter() si mette in una variabile
ski_df = properties_df.filter(properties_df["property_type"] == "Ski Resort")
print(ski_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.10 Da Spark a Python e ritorno: collect e createDataFrame

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC <class 'list'> 3
# MAGIC Row(property_id=11670, title='Historic Inn in Rome', property_type='Historical Place', base_price=284.9700012207031)
# MAGIC ```

# COMMAND ----------

guide_rows = guide_report_df.collect()
print(type(guide_rows), len(guide_rows))
print(guide_rows[0])

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC Historic Inn in Rome
# MAGIC 284.9700012207031
# MAGIC 284.97
# MAGIC {'property_id': 11670, 'title': 'Historic Inn in Rome', 'property_type': 'Historical Place', 'base_price': 284.9700012207031}
# MAGIC ```

# COMMAND ----------

first_row = guide_rows[0]
print(first_row["title"])
print(first_row["base_price"])
print(f"{first_row['base_price']:.2f}")
print(first_row.asDict())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC Row(first_check_in=datetime.date(2022, 12, 29), last_check_in=datetime.date(2025, 7, 30))
# MAGIC <class 'datetime.date'>
# MAGIC Arrivi dal 29/12/2022 al 30/07/2025: 944 giorni
# MAGIC ```

# COMMAND ----------

period_row = spark.sql(f"""
SELECT MIN(check_in) AS first_check_in, MAX(check_in) AS last_check_in
FROM {SOURCE_BOOKINGS_TABLE}
""").collect()[0]
print(period_row)
first_check_in = period_row["first_check_in"]
last_check_in = period_row["last_check_in"]
print(type(first_check_in))
print(f"Arrivi dal {first_check_in.strftime('%d/%m/%Y')} al {last_check_in.strftime('%d/%m/%Y')}: {(last_check_in - first_check_in).days} giorni")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC 11670: 6 prenotazioni, 0 cancellate, tasso 0.0% (ok), ricavo 3966.21
# MAGIC 16317: 7 prenotazioni, 1 cancellate, tasso 14.3% (ok), ricavo 5139.59
# MAGIC 16225: 4 prenotazioni, 2 cancellate, tasso 50.0% (critico), ricavo 2896.92
# MAGIC ```

# COMMAND ----------

guide_results = []
for property_id in GUIDE_PROPERTY_IDS:
    rows_2024 = (
        bookings_df
        .filter(
            (bookings_df["property_id"] == property_id)
            & (bookings_df["check_in"] >= date(ANALYSIS_YEAR, 1, 1))
            & (bookings_df["check_in"] <= date(ANALYSIS_YEAR, 12, 31))
        )
        .select("status", "total_amount")
        .collect()
    )
    booking_total = len(rows_2024)
    cancelled_total = 0
    revenue_total = 0
    for row in rows_2024:
        revenue_total = revenue_total + row["total_amount"]
        if row["status"] == "cancelled":
            cancelled_total = cancelled_total + 1
    rate = cancelled_total / booking_total * 100
    status = classify_cancellation_rate(rate)
    print(f"{property_id}: {booking_total} prenotazioni, {cancelled_total} cancellate, tasso {rate:.1f}% ({status}), ricavo {revenue_total:.2f}")
    guide_results.append({
        "property_id": property_id,
        "bookings_2024": booking_total,
        "cancelled_2024": cancelled_total,
        "cancellation_rate": round(rate, 1),
        "cancellation_status": status,
        "revenue_2024": round(revenue_total, 2),
    })

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `['bookings_2024', 'cancellation_rate', 'cancellation_status', 'cancelled_2024', 'property_id', 'revenue_2024']`.

# COMMAND ----------

results_df = spark.createDataFrame(guide_results)
print(results_df.columns)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 
# MAGIC ```
# MAGIC property_id  bookings_2024  cancelled_2024  cancellation_rate  cancellation_status  revenue_2024
# MAGIC 16225        4              2               50.0               critico              2896.92
# MAGIC 16317        7              1               14.3               ok                   5139.59
# MAGIC 11670        6              0               0.0                ok                   3966.21
# MAGIC ```

# COMMAND ----------

results_df = results_df.select(
    "property_id", "bookings_2024", "cancelled_2024", "cancellation_rate", "cancellation_status", "revenue_2024"
)
display(results_df.orderBy("cancellation_rate", ascending=False))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: risultato atteso
# MAGIC ```
# MAGIC property_id  bookings_2024  cancelled_2024  revenue_2024
# MAGIC 11670        6              0               3966.21
# MAGIC 16225        4              2               2896.92
# MAGIC 16317        7              1               5139.59
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                                  AS bookings_2024,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)     AS cancelled_2024,
# MAGIC        ROUND(SUM(total_amount), 2)                               AS revenue_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8.11 Errori comuni con PySpark

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (la tabella si chiama bookings, non booking).

# COMMAND ----------

# ERRORE VOLUTO – la tabella si chiama bookings, non booking
wrong_df = spark.sql("SELECT * FROM samples.wanderbricks.booking")
print(wrong_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la costante della cella di preparazione. Risultato atteso: `72247`.

# COMMAND ----------

# Correzione: il nome della tabella dalla costante
right_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")
print(right_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente deve fallire (show() restituisce None, non un DataFrame).

# COMMAND ----------

# ERRORE VOLUTO – show() restituisce None, non un DataFrame
italy_shown_df = italy_df.show()
print(italy_shown_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il DataFrame si salva senza `show()`. Risultato atteso: la griglia delle quattro destinazioni e `4`.

# COMMAND ----------

# Correzione: si salva il DataFrame, show() si chiama da solo
italy_shown_df = italy_df
italy_shown_df.show()
print(italy_shown_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC La cella seguente non dà errori ma produce un risultato sbagliato (count senza parentesi non conta le righe): `<bound method DataFrame.count of DataFrame[destination_id: bigint, destination: string, country: string]>`.

# COMMAND ----------

# ERRORE SILENZIOSO – count senza parentesi non conta le righe
print(italy_df.count)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: le parentesi. Risultato atteso: `4`.

# COMMAND ----------

# Correzione: count() con le parentesi
print(italy_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - `spark.sql(testo)` esegue una query e restituisce un **DataFrame**; la query si compone con le f-string (testi tra apici).
# MAGIC - Un DataFrame è una **ricetta**: `select`, `distinct`, `filter`, `orderBy`, `limit` preparano; `display`, `show`, `count`, `collect` sono **azioni**.
# MAGIC - `display()` griglia interattiva; `show(n, truncate=False)` griglia di testo; entrambe restituiscono `None`. `printSchema()` come `DESCRIBE TABLE`; `count()` dà un `int`; `columns` è una lista.
# MAGIC - Filtri in forma testo (`"status = 'cancelled'"`) o colonna (`df["status"] == "cancelled"`); `&` `|` `~` con ogni condizione tra parentesi; `isNull()` / `isNotNull()`, mai `== None`.
# MAGIC - `orderBy(..., ascending=False)` o `.desc()`; in Spark i `NULL` vanno in cima nell'ordine crescente; `limit()` sempre dopo `orderBy()`.
# MAGIC - Catene tra parentesi, un'operazione per riga; il DataFrame di partenza non cambia: il risultato si assegna.
# MAGIC - `collect()` → lista di `Row` (come dizionari, `asDict()`), solo per risultati piccoli; `spark.createDataFrame(lista)` mette le colonne in ordine alfabetico: si riordinano con `select()`.
