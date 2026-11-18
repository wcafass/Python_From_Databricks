# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 9 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito. Nessuna cella scrive tabelle.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L09_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L09_Esercizi_svolti`). Si esegue per prima la cella di preparazione, poi **una cella alla volta**: l'esercizio 8 contiene celle che devono fallire (**ERRORE VOLUTO**) o che producono un risultato sbagliato (**ERRORE SILENZIOSO**). Non usare Run all.
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso e una verifica `%sql` che calcola lo stesso risultato con una query: il risultato di PySpark deve coincidere con entrambe. Come nel capitolo, le colonne si indicano con `F.col()` e ogni colonna calcolata ha un nome esplicito.

# COMMAND ----------

# Cella di preparazione: import, costanti, DataFrame e valori usati negli esercizi
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

# Prenotazioni 2024 della struttura della Sardegna (16317), scritte come testo (esercizi 2 e 8f)
raw_sardinia_rows = [
    {"booking_id": 49395, "check_in": "08/06/2024", "check_out": "11/06/2024", "total_amount": "647.01"},
    {"booking_id": 59901, "check_in": "12/07/2024", "check_out": "17/07/2024", "total_amount": "590.95"},
    {"booking_id": 68070, "check_in": "17/07/2024", "check_out": "22/07/2024", "total_amount": "900.47"},
    {"booking_id": 688, "check_in": "31/07/2024", "check_out": "05/08/2024", "total_amount": "635.51"},
    {"booking_id": 9842, "check_in": "18/08/2024", "check_out": "23/08/2024", "total_amount": "759.63"},
    {"booking_id": 23944, "check_in": "23/08/2024", "check_out": "28/08/2024", "total_amount": "623.81"},
    {"booking_id": 64865, "check_in": "07/09/2024", "check_out": "08/09/2024", "total_amount": "982.21"},
]

print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Nuove colonne sulle strutture guida
# MAGIC 1. Da `properties_df` tenere le tre strutture guida (forma colonna con `F.col` e `|`) e le colonne `property_id`, `title`, `base_price`, `max_guests`.
# MAGIC 2. Aggiungere con `withColumn`: `price_per_guest` (prezzo base diviso per `max_guests`, arrotondato a due decimali), `title_upper` (il titolo in maiuscolo) e `source` (il valore fisso `wanderbricks`).
# MAGIC 3. Mostrare il risultato con `display()`, ordinato per `property_id`.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso (griglia)
print("property_id  title                  base_price  max_guests  price_per_guest  title_upper            source")
print("11670        Historic Inn in Rome   284.97      8           35.62            HISTORIC INN IN ROME   wanderbricks")
print("16225        Beach House in Amalfi  236.95      1           236.95           BEACH HOUSE IN AMALFI  wanderbricks")
print("16317        Bungalow in Sardinia   213.91      4           53.48            BUNGALOW IN SARDINIA   wanderbricks")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: prezzo per ospite 35.62, 236.95, 53.48
# MAGIC SELECT property_id, title, base_price, max_guests,
# MAGIC        ROUND(base_price / max_guests, 2) AS price_per_guest,
# MAGIC        UPPER(title)                      AS title_upper,
# MAGIC        'wanderbricks'                    AS source
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Date e importi scritti come testo
# MAGIC 1. Trasformare `raw_sardinia_rows` in un DataFrame con `spark.createDataFrame()`.
# MAGIC 2. Convertire `check_in` e `check_out` in date con `F.to_date` e il formato giusto, e `total_amount` in `double` con `cast`; aggiungere la colonna `nights` con `F.datediff`.
# MAGIC 3. Con `agg` calcolare `booking_count`, `total_nights` e `revenue` (ricavo arrotondato a due decimali).
# MAGIC 4. Da `customer_support_logs` (costante `SUPPORT_LOGS_TABLE`) contare le richieste per anno, con l'anno ricavato da `F.to_date(F.col("created_at"))`, in ordine di anno.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso (due griglie)
print("booking_count  total_nights  revenue")
print("7              29            5139.59")
print()
print("created_year  ticket_count")
print("2022          150")
print("2023          696")
print("2024          658")
print("2025          396")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: prenotazioni 2024 della Sardegna (7, 29 notti, 5139.59)
# MAGIC SELECT COUNT(*)                                AS booking_count,
# MAGIC        SUM(datediff(check_out, check_in))      AS total_nights,
# MAGIC        ROUND(SUM(total_amount), 2)             AS revenue
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id = 16317 AND year(check_in) = 2024

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: richieste per anno (150, 696, 658, 396)
# MAGIC SELECT year(to_date(created_at)) AS created_year, COUNT(*) AS ticket_count
# MAGIC FROM samples.wanderbricks.customer_support_logs
# MAGIC GROUP BY year(to_date(created_at))
# MAGIC ORDER BY created_year

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Raggruppare le strutture
# MAGIC Per tipo di struttura calcolare, con `groupBy` e `agg`: `property_count` (numero delle strutture), `destination_count` (numero delle destinazioni distinte in cui il tipo è presente) e `avg_max_guests` (media di `max_guests`, arrotondata a due decimali). Mostrare il risultato in ordine di `property_count` decrescente.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso (griglia)
print("property_type     property_count  destination_count  avg_max_guests")
print("Urban Year-Round  9264            12                 2.48")
print("Summer Getaway    7068            10                 2.48")
print("Historical Place  1646            10                 2.42")
print("Ski Resort        185             10                 2.35")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica
# MAGIC SELECT property_type,
# MAGIC        COUNT(*)                        AS property_count,
# MAGIC        COUNT(DISTINCT destination_id)  AS destination_count,
# MAGIC        ROUND(AVG(max_guests), 2)       AS avg_max_guests
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY property_type
# MAGIC ORDER BY property_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Le fasce di prezzo di tutte le strutture
# MAGIC 1. Aggiungere a `properties_df` la colonna `price_band` della sezione 9.4: `alto` da 250, `medio` da 200, altrimenti `basso`.
# MAGIC 2. Contare le strutture per fascia (`property_count`), in ordine alfabetico di fascia.
# MAGIC 3. Fare lo stesso conteggio per le sole strutture `Ski Resort`.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso (due griglie)
print("price_band  property_count")
print("alto        1894")
print("basso       12647")
print("medio       3622")
print()
print("price_band  property_count   (solo Ski Resort)")
print("alto        106")
print("basso       15")
print("medio       64")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: tutte le strutture (1894, 12647, 3622)
# MAGIC SELECT CASE WHEN base_price >= 250 THEN 'alto'
# MAGIC             WHEN base_price >= 200 THEN 'medio'
# MAGIC             ELSE 'basso' END AS price_band,
# MAGIC        COUNT(*) AS property_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY 1
# MAGIC ORDER BY price_band

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: solo Ski Resort (106, 15, 64)
# MAGIC SELECT CASE WHEN base_price >= 250 THEN 'alto'
# MAGIC             WHEN base_price >= 200 THEN 'medio'
# MAGIC             ELSE 'basso' END AS price_band,
# MAGIC        COUNT(*) AS property_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_type = 'Ski Resort'
# MAGIC GROUP BY 1
# MAGIC ORDER BY price_band

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Un filtro sui gruppi
# MAGIC 1. Contare le destinazioni per paese (`destination_count`) e tenere, con un `filter` dopo `agg`, i paesi con almeno 4 destinazioni, in ordine alfabetico.
# MAGIC 2. Contare quanti paesi hanno una sola destinazione e stampare il numero.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso
print("country        destination_count")
print("Italy          4")
print("Spain          4")
print("United States  4")
print()
print(1)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: paesi con almeno 4 destinazioni
# MAGIC SELECT country, COUNT(*) AS destination_count
# MAGIC FROM samples.wanderbricks.destinations
# MAGIC GROUP BY country
# MAGIC HAVING COUNT(*) >= 4
# MAGIC ORDER BY country

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Prenotazioni per continente
# MAGIC 1. Con tre join (prenotazioni 2024 → strutture → destinazioni → paesi), ognuno con `on=` e `how="inner"` e con un `select` delle colonne utili prima del join, contare le prenotazioni 2024 per continente (`booking_count`), in ordine decrescente.
# MAGIC 2. Contare le prenotazioni 2024 per `destination_id`; unire con un left join le destinazioni (colonne `destination_id`, `destination`, `country`) a questo conteggio e mostrare le destinazioni senza prenotazioni nel 2024.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso (due griglie)
print("continent      booking_count")
print("Europe         5556")
print("Asia           5287")
print("Oceania        1246")
print("North America  1212")
print("Africa         285")
print()
print("destination_id  destination  country  booking_count")
print("2100            Courchevel   France   null")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: prenotazioni 2024 per continente
# MAGIC SELECT c.continent, COUNT(*) AS booking_count
# MAGIC FROM samples.wanderbricks.bookings b
# MAGIC JOIN samples.wanderbricks.properties p USING (property_id)
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC JOIN samples.wanderbricks.countries c USING (country)
# MAGIC WHERE year(b.check_in) = 2024
# MAGIC GROUP BY c.continent
# MAGIC ORDER BY booking_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Il report per paese
# MAGIC Come nella sezione 9.8, ma per paese e per tutto il 2024:
# MAGIC 1. costruire un report con `country`, `continent`, `booking_count`, `cancelled_count`, `cancellation_rate` (in %, un decimale) e `cancellation_status` (`non valutabile` sotto `MIN_BOOKINGS`, `critico` sopra `CANCELLATION_RATE_THRESHOLD`, altrimenti `ok`);
# MAGIC 2. mostrarlo in ordine di tasso decrescente e poi di paese;
# MAGIC 3. contare i paesi per stato (`country_count`), in ordine alfabetico di stato.

# COMMAND ----------

# Scrivere qui la soluzione

# COMMAND ----------

# Verifica: risultato atteso (18 righe; si riportano le prime due, l'Italia e il conteggio per stato)
print("country      continent  booking_count  cancelled_count  cancellation_rate  cancellation_status")
print("Egypt        Africa     285            66               23.2               ok")
print("Switzerland  Europe     13             3                23.1               non valutabile")
print("...")
print("Italy        Europe     714            142              19.9               ok")
print("...")
print("Austria      Europe     14             2                14.3               non valutabile")
print("Canada       North America  54         5                9.3                ok")
print()
print("cancellation_status  country_count")
print("non valutabile       2")
print("ok                   16")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: il report per paese
# MAGIC SELECT d.country, c.continent,
# MAGIC        COUNT(*)                                                AS booking_count,
# MAGIC        SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
# MAGIC        ROUND(SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS cancellation_rate
# MAGIC FROM samples.wanderbricks.bookings b
# MAGIC JOIN samples.wanderbricks.properties p USING (property_id)
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC JOIN samples.wanderbricks.countries c USING (country)
# MAGIC WHERE year(b.check_in) = 2024
# MAGIC GROUP BY d.country, c.continent
# MAGIC ORDER BY cancellation_rate DESC, d.country

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare il tipo dell'errore e il messaggio (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `1070`; i prezzi medi per tipo (147.46, 266.49, 198.54, 173.04 in ordine alfabetico di tipo); `1008`; Italy, Spain, United States; `1894`; `29` notti.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (le strutture Summer Getaway care)
flagged_df = properties_df.withColumn(
    "expensive_summer",
    F.when((F.col("property_type") == "Summer Getaway") and (F.col("base_price") >= 250), "sì").otherwise("no")
)
print(flagged_df.filter(F.col("expensive_summer") == "sì").count())

# COMMAND ----------

# Correzione 8a (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE VOLUTO – cella 8b (il prezzo medio per tipo)
type_avg_df = properties_df.groupBy("property_type").agg(round(F.avg("base_price"), 2).alias("avg_price"))
display(type_avg_df)

# COMMAND ----------

# Correzione 8b (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE VOLUTO – cella 8c (le strutture italiane)
places_df = properties_df.join(destinations_df, properties_df["destination_id"] == destinations_df["destination_id"], how="inner")
print(places_df.filter(F.col("country") == "Italy").select("property_id", "destination_id").count())

# COMMAND ----------

# Correzione 8c (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE VOLUTO – cella 8d (i paesi con almeno 4 destinazioni)
big_countries_df = destinations_df.groupBy("country").filter(F.count("*") >= 4)
display(big_countries_df)

# COMMAND ----------

# Correzione 8d (tipo dell'errore: ...)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (le strutture nella fascia alta)
bands_df = properties_df.withColumn(
    "price_band",
    F.when(F.col("base_price") >= 200, "medio")
    .when(F.col("base_price") >= 250, "alto")
    .otherwise("basso")
)
print(bands_df.filter(F.col("price_band") == "alto").count())

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (le notti della struttura della Sardegna)
sardinia_df = (
    spark.createDataFrame(raw_sardinia_rows)
    .withColumn("check_in", F.to_date(F.col("check_in"), "dd/mm/yyyy"))
    .withColumn("check_out", F.to_date(F.col("check_out"), "dd/mm/yyyy"))
)
display(sardinia_df.agg(F.sum(F.datediff(F.col("check_out"), F.col("check_in"))).alias("total_nights")))

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)
