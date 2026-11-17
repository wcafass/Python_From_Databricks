# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 8 – Soluzioni
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito (gli esercizi 6, 7 e 8 leggono `workspace.libro_python.b_bookings`). Nessuna cella scrive tabelle.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Testo degli esercizi: notebook `L08_Esercizi` e fine del Capitolo 8.
# MAGIC
# MAGIC Si esegue per prima la cella di preparazione, poi **una cella alla volta**: l'esercizio 8 contiene celle che devono fallire (**ERRORE VOLUTO**) o che producono un risultato sbagliato (**ERRORE SILENZIOSO**). Non usare Run all.
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso e, quando possibile, una verifica `%sql` che calcola lo stesso risultato con una query: il risultato di PySpark deve coincidere con entrambe.

# COMMAND ----------

# Cella di preparazione: import, costanti e valori usati negli esercizi
from datetime import date, timedelta, datetime

SOURCE_SCHEMA = "samples.wanderbricks"
WORK_SCHEMA = "workspace.libro_python"
SOURCE_BOOKINGS_TABLE = f"{SOURCE_SCHEMA}.bookings"   # prenotazioni originali
PROPERTIES_TABLE = f"{SOURCE_SCHEMA}.properties"
DESTINATIONS_TABLE = f"{SOURCE_SCHEMA}.destinations"
REVIEWS_TABLE = f"{SOURCE_SCHEMA}.reviews"
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
# MAGIC ## Esercizio 1 ★ – Contare con spark.sql
# MAGIC 1. Con `spark.sql()` e una f-string che usa le costanti `PROPERTIES_TABLE`, `DESTINATIONS_TABLE` e `REVIEWS_TABLE`, preparare i DataFrame `properties_df`, `destinations_df` e `reviews_df` con tutte le righe delle tre tabelle.
# MAGIC 2. Contare le righe dei tre DataFrame con `count()` e stampare i tre numeri sulla stessa riga.
# MAGIC 3. Stampare `Strutture per destinazione: ...`, il numero medio di strutture per destinazione, con un decimale.

# COMMAND ----------

# Soluzione 1: tre DataFrame, tre conteggi, una divisione tra int
properties_df = spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")
destinations_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE}")
reviews_df = spark.sql(f"SELECT * FROM {REVIEWS_TABLE}")

properties_count = properties_df.count()
destinations_count = destinations_df.count()
reviews_count = reviews_df.count()
print(properties_count, destinations_count, reviews_count)
print(f"Strutture per destinazione: {properties_count / destinations_count:.1f}")

# COMMAND ----------

# Verifica: risultato atteso
print(18163, 42, 99793)
print("Strutture per destinazione: 432.5")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: 18163, 42, 99793
# MAGIC SELECT (SELECT COUNT(*) FROM samples.wanderbricks.properties)    AS properties_count,
# MAGIC        (SELECT COUNT(*) FROM samples.wanderbricks.destinations)  AS destinations_count,
# MAGIC        (SELECT COUNT(*) FROM samples.wanderbricks.reviews)       AS reviews_count

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – La struttura di una tabella
# MAGIC 1. Stampare lo schema di `properties_df` con `printSchema()`.
# MAGIC 2. Stampare il numero delle colonne, calcolato con `columns`.
# MAGIC 3. Stampare sulla stessa riga se `"base_price"` e `"price"` sono tra le colonne (operatore `in`).

# COMMAND ----------

# Soluzione 2: schema, numero di colonne, controllo con in
properties_df.printSchema()
print(len(properties_df.columns))
print("base_price" in properties_df.columns, "price" in properties_df.columns)

# COMMAND ----------

# Verifica: risultato atteso
print("Schema: una riga per colonna, tra cui |-- base_price: float (nullable = true)")
print("Numero di colonne: uguale al numero di righe della verifica DESCRIBE TABLE")
print(True, False)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: una riga per colonna (il numero di righe è il numero di colonne)
# MAGIC DESCRIBE TABLE samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – select e distinct
# MAGIC 1. Contare i paesi distinti di `destinations_df` (colonna `country`).
# MAGIC 2. Mostrare con `show(truncate=False)` le colonne `destination_id` e `destination` delle destinazioni italiane (`country` uguale a `"Italy"`), ordinate per nome.
# MAGIC 3. Mostrare con `show()` i tipi di struttura distinti di `properties_df`, in ordine alfabetico.

# COMMAND ----------

# Soluzione 3: distinct, filtro con ordinamento, valori distinti ordinati
print(destinations_df.select("country").distinct().count())

(
    destinations_df
    .filter(destinations_df["country"] == "Italy")
    .select("destination_id", "destination")
    .orderBy("destination")
    .show(truncate=False)
)

properties_df.select("property_type").distinct().orderBy("property_type").show()

# COMMAND ----------

# Verifica: risultato atteso
print(18)
print("1100 Amalfi, 2300 Florence, 3900 Rome, 4200 Sardinia")
print("Historical Place, Ski Resort, Summer Getaway, Urban Year-Round")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: paesi distinti (18) e tipi di struttura in ordine alfabetico
# MAGIC SELECT COUNT(DISTINCT country) AS countries FROM samples.wanderbricks.destinations

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT property_type
# MAGIC FROM samples.wanderbricks.properties
# MAGIC ORDER BY property_type

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Le due forme di filter
# MAGIC 1. Contare le strutture `Summer Getaway` con la forma testo e con la forma colonna; stampare i due conteggi sulla stessa riga.
# MAGIC 2. Con la variabile `chosen_type = "Urban Year-Round"`, contare le strutture di quel tipo nelle due forme (nella forma testo con una f-string).
# MAGIC 3. Su `reviews_df`, contare nella forma colonna le recensioni con `rating` mancante, quelle con `is_deleted` uguale a `True` e quelle con entrambe le condizioni; stampare i tre conteggi sulla stessa riga.

# COMMAND ----------

# Soluzione 4: forma testo e forma colonna, condizioni con &
print(
    properties_df.filter("property_type = 'Summer Getaway'").count(),
    properties_df.filter(properties_df["property_type"] == "Summer Getaway").count(),
)

chosen_type = "Urban Year-Round"
print(
    properties_df.filter(f"property_type = '{chosen_type}'").count(),
    properties_df.filter(properties_df["property_type"] == chosen_type).count(),
)

missing_rating_count = reviews_df.filter(reviews_df["rating"].isNull()).count()
deleted_count = reviews_df.filter(reviews_df["is_deleted"] == True).count()
both_count = reviews_df.filter(
    (reviews_df["rating"].isNull())
    & (reviews_df["is_deleted"] == True)
).count()
print(missing_rating_count, deleted_count, both_count)

# COMMAND ----------

# Verifica: risultato atteso
print(7068, 7068)
print(9264, 9264)
print(476, 476, 476)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: 7068, 9264, 476, 476, 476
# MAGIC SELECT (SELECT COUNT(*) FROM samples.wanderbricks.properties WHERE property_type = 'Summer Getaway')   AS summer_count,
# MAGIC        (SELECT COUNT(*) FROM samples.wanderbricks.properties WHERE property_type = 'Urban Year-Round') AS urban_count,
# MAGIC        (SELECT COUNT(*) FROM samples.wanderbricks.reviews WHERE rating IS NULL)                         AS missing_rating,
# MAGIC        (SELECT COUNT(*) FROM samples.wanderbricks.reviews WHERE is_deleted = true)                      AS deleted_reviews,
# MAGIC        (SELECT COUNT(*) FROM samples.wanderbricks.reviews WHERE rating IS NULL AND is_deleted = true)   AS both_conditions

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Le altre strutture guida
# MAGIC 1. Preparare `bookings_df` con tutte le righe di `SOURCE_BOOKINGS_TABLE`.
# MAGIC 2. Definire la funzione `print_guide_rate(property_id)`, con una docstring, che filtra le prenotazioni della struttura con arrivo nel `ANALYSIS_YEAR` (forma colonna, `&` e date di Python), conta le prenotazioni e le cancellate, calcola il tasso e lo stato con `classify_cancellation_rate` e stampa `property_id: N prenotazioni, N cancellate, tasso X.X% (stato)`.
# MAGIC 3. Chiamare la funzione per Roma (11670) e per la Sardegna (16317).

# COMMAND ----------

# Soluzione 5: una funzione con il filtro e i due conteggi
bookings_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")


def print_guide_rate(property_id):
    """Stampa prenotazioni, cancellate, tasso e stato di una struttura nell'anno di analisi."""
    property_df = bookings_df.filter(
        (bookings_df["property_id"] == property_id)
        & (bookings_df["check_in"] >= date(ANALYSIS_YEAR, 1, 1))
        & (bookings_df["check_in"] <= date(ANALYSIS_YEAR, 12, 31))
    )
    booking_total = property_df.count()
    cancelled_total = property_df.filter(property_df["status"] == "cancelled").count()
    rate = cancelled_total / booking_total * 100
    status = classify_cancellation_rate(rate)
    print(f"{property_id}: {booking_total} prenotazioni, {cancelled_total} cancellate, tasso {rate:.1f}% ({status})")


print_guide_rate(11670)
print_guide_rate(16317)

# COMMAND ----------

# Verifica: risultato atteso
print("11670: 6 prenotazioni, 0 cancellate, tasso 0.0% (ok)")
print("16317: 7 prenotazioni, 1 cancellate, tasso 14.3% (ok)")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: 11670 6 0; 16317 7 1
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                              AS bookings_2024,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Il profilo della copia didattica
# MAGIC 1. Preparare `teaching_bookings_df` con tutte le righe di `BOOKINGS_TABLE`.
# MAGIC 2. Raccogliere in un dizionario `profile` sei conteggi, con queste chiavi: `"righe"`, `"righe distinte"`, `"importi mancanti"`, `"importi negativi"`, `"date invertite"` (partenza prima dell'arrivo), `"importi mancanti o negativi"`.
# MAGIC 3. Con un ciclo su `profile.items()` stampare una riga `chiave valore` per controllo.

# COMMAND ----------

# Soluzione 6: un dizionario di conteggi e un ciclo su items()
teaching_bookings_df = spark.sql(f"SELECT * FROM {BOOKINGS_TABLE}")
amount = teaching_bookings_df["total_amount"]

profile = {
    "righe": teaching_bookings_df.count(),
    "righe distinte": teaching_bookings_df.distinct().count(),
    "importi mancanti": teaching_bookings_df.filter(amount.isNull()).count(),
    "importi negativi": teaching_bookings_df.filter(amount < 0).count(),
    "date invertite": teaching_bookings_df.filter(
        teaching_bookings_df["check_out"] < teaching_bookings_df["check_in"]
    ).count(),
    "importi mancanti o negativi": teaching_bookings_df.filter((amount.isNull()) | (amount < 0)).count(),
}
for check_name, value in profile.items():
    print(check_name, value)

# COMMAND ----------

# Verifica: risultato atteso
print("righe 72287")
print("righe distinte 72247")
print("importi mancanti 30")
print("importi negativi 13")
print("date invertite 8")
print("importi mancanti o negativi 43")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: 72287, 72247, 30, 13, 8, 43
# MAGIC SELECT COUNT(*)                                                         AS row_count,
# MAGIC        (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM workspace.libro_python.b_bookings)) AS distinct_rows,
# MAGIC        SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END)            AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)                AS negative_amounts,
# MAGIC        SUM(CASE WHEN check_out < check_in THEN 1 ELSE 0 END)            AS inverted_dates,
# MAGIC        SUM(CASE WHEN total_amount IS NULL OR total_amount < 0 THEN 1 ELSE 0 END) AS amount_problems
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – I ricavi dalla copia didattica
# MAGIC Le prenotazioni delle strutture guida non sono tra quelle modificate in `b_bookings` (Capitolo 0), ma gli importi della copia sono arrotondati riga per riga: verifichiamo che i ricavi 2024 restino quelli scritti a mano.
# MAGIC 1. Per ogni riga di `guide_properties`, filtrare `teaching_bookings_df` (struttura e arrivo nel 2024), portare in Python la sola colonna `total_amount` con `collect()` e sommarla con un accumulatore.
# MAGIC 2. Aggiungere a una lista `revenue_checks` un dizionario con `property_id`, `title`, `revenue_from_table` (arrotondato a 2 decimali), `revenue_written` (il valore di `guide_properties`) e `same_value` (`True` se i due valori coincidono).
# MAGIC 3. Trasformare la lista in un DataFrame con `spark.createDataFrame()`, disporre le colonne nell'ordine del punto 2 con `select()` e mostrarlo con `display()` in ordine di `revenue_from_table` decrescente.

# COMMAND ----------

# Soluzione 7: collect() e accumulatore, poi di nuovo un DataFrame
revenue_checks = []
for guide in guide_properties:
    amount_rows = (
        teaching_bookings_df
        .filter(
            (teaching_bookings_df["property_id"] == guide["property_id"])
            & (teaching_bookings_df["check_in"] >= date(ANALYSIS_YEAR, 1, 1))
            & (teaching_bookings_df["check_in"] <= date(ANALYSIS_YEAR, 12, 31))
        )
        .select("total_amount")
        .collect()
    )
    revenue_total = 0
    for row in amount_rows:
        revenue_total = revenue_total + row["total_amount"]
    revenue_from_table = round(revenue_total, 2)
    revenue_checks.append({
        "property_id": guide["property_id"],
        "title": guide["title"],
        "revenue_from_table": revenue_from_table,
        "revenue_written": guide["revenue_2024"],
        "same_value": revenue_from_table == guide["revenue_2024"],
    })

checks_df = (
    spark.createDataFrame(revenue_checks)
    .select("property_id", "title", "revenue_from_table", "revenue_written", "same_value")
    .orderBy("revenue_from_table", ascending=False)
)
display(checks_df)

# COMMAND ----------

# Verifica: risultato atteso (griglia)
print("property_id  title                  revenue_from_table  revenue_written  same_value")
print("16317        Bungalow in Sardinia   5139.59             5139.59          true")
print("11670        Historic Inn in Rome   3966.21             3966.21          true")
print("16225        Beach House in Amalfi  2896.92             2896.92          true")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: ricavi 2024 dalla copia didattica (5139.59, 3966.21, 2896.92)
# MAGIC SELECT property_id,
# MAGIC        ROUND(SUM(total_amount), 2) AS revenue_2024
# MAGIC FROM workspace.libro_python.b_bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY revenue_2024 DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare il tipo dell'errore e il messaggio (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `18163`; `4`; `4`; `42`; `30`; `7068`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (le strutture)
properties_df = spark.sql("SELECT * FROM samples.wanderbricks.propertie")
print(properties_df.count())

# COMMAND ----------

# Correzione 8a (tipo dell'errore: TABLE_OR_VIEW_NOT_FOUND, la tabella si chiama properties)
properties_df = spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")
print(properties_df.count())

# COMMAND ----------

# ERRORE VOLUTO – cella 8b (le destinazioni di un paese)
country = "Italy"
italy_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE} WHERE country = {country}")
print(italy_df.count())

# COMMAND ----------

# Correzione 8b (tipo dell'errore: UNRESOLVED_COLUMN, Italy senza apici diventa il nome di una colonna)
country = "Italy"
italy_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE} WHERE country = '{country}'")
print(italy_df.count())

# COMMAND ----------

# ERRORE VOLUTO – cella 8c (le prenotazioni 2024 della struttura di Amalfi)
bookings_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")
amalfi_df = bookings_df.filter(
    (bookings_df["property_id"] == 16225)
    and (bookings_df["check_in"] >= date(ANALYSIS_YEAR, 1, 1))
    and (bookings_df["check_in"] <= date(ANALYSIS_YEAR, 12, 31))
)
print(amalfi_df.count())

# COMMAND ----------

# Correzione 8c (tipo dell'errore: CANNOT_CONVERT_COLUMN_INTO_BOOL, and al posto di &)
bookings_df = spark.sql(f"SELECT * FROM {SOURCE_BOOKINGS_TABLE}")
amalfi_df = bookings_df.filter(
    (bookings_df["property_id"] == 16225)
    & (bookings_df["check_in"] >= date(ANALYSIS_YEAR, 1, 1))
    & (bookings_df["check_in"] <= date(ANALYSIS_YEAR, 12, 31))
)
print(amalfi_df.count())

# COMMAND ----------

# ERRORE VOLUTO – cella 8d (quante destinazioni)
destinations_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE}").show(3)
print(destinations_df.count())

# COMMAND ----------

# Correzione 8d (tipo dell'errore: AttributeError, show() restituisce None)
destinations_df = spark.sql(f"SELECT * FROM {DESTINATIONS_TABLE}")
destinations_df.show(3)
print(destinations_df.count())

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (gli importi mancanti della copia didattica)
teaching_bookings_df = spark.sql(f"SELECT * FROM {BOOKINGS_TABLE}")
print(teaching_bookings_df.filter(teaching_bookings_df["total_amount"] == None).count())

# COMMAND ----------

# Correzione 8e (che cosa non va: == None non è mai vero; i nulli si cercano con isNull())
teaching_bookings_df = spark.sql(f"SELECT * FROM {BOOKINGS_TABLE}")
print(teaching_bookings_df.filter(teaching_bookings_df["total_amount"].isNull()).count())

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (le strutture Summer Getaway)
summer_df = spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")
summer_df.filter(summer_df["property_type"] == "Summer Getaway")
print(summer_df.count())

# COMMAND ----------

# Correzione 8f (che cosa non va: il risultato di filter() non è stato assegnato)
summer_df = spark.sql(f"SELECT * FROM {PROPERTIES_TABLE}")
summer_df = summer_df.filter(summer_df["property_type"] == "Summer Getaway")
print(summer_df.count())
