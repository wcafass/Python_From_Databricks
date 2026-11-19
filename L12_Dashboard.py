# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 12 – Dalla tabella alla dashboard
# MAGIC
# MAGIC Notebook del Capitolo 12 di *Oltre la SELECT*. Obiettivi: preparare e provare le query della dashboard **Cancellazioni per destinazione 2024**, calcolare nel notebook i valori che la dashboard deve mostrare e confrontarli con quelli letti sulla dashboard.
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; il notebook `L11_Progetto_Finale` eseguito almeno una volta (deve esistere la tabella `g_cancellazioni_aggiornate_destinazione_mese`); il notebook `utils` nella stessa cartella `Libro_Python`. Il notebook **non scrive tabelle**: la dashboard si costruisce nell'interfaccia (barra laterale → **Dashboards**), seguendo il testo del capitolo.
# MAGIC
# MAGIC Si esegue **una cella alla volta**, dall'alto in basso. La sezione 12.5 contiene una cella che deve fallire (**ERRORE VOLUTO**) e la sezione 12.13 una cella che produce un risultato sbagliato (**ERRORE SILENZIOSO**), ciascuna con la correzione nella cella subito sotto. Non usare Run all. Se il compute si ferma, si rieseguono la cella `%run ./utils`, la cella delle costanti e le celle che creano le variabili usate più avanti.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduzione

# COMMAND ----------

# MAGIC %md
# MAGIC ### La cella di preparazione

# COMMAND ----------

# MAGIC %run ./utils

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese
# MAGIC 317
# MAGIC ['destination', 'country', 'check_in_month', 'booking_count', 'cancelled_count', 'revenue', 'cancellation_rate', 'cancellation_status']
# MAGIC ```

# COMMAND ----------

# Costanti del capitolo: la tabella del report del Capitolo 11, fonte della dashboard
PROJECT_REPORT_TABLE = build_table_name("cancellazioni_aggiornate", "destinazione_mese", layer="g")
DASHBOARD_THRESHOLDS = [30.0, 40.0]

# La tabella del report, letta una volta
report_df = spark.table(PROJECT_REPORT_TABLE)

print(PROJECT_REPORT_TABLE)
print(report_df.count())
print(report_df.columns)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.1 Che cos'è una dashboard

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC cancellation_status  combination_count
# MAGIC critico              147
# MAGIC non valutabile       152
# MAGIC ok                   18
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT cancellation_status, COUNT(*) AS combination_count
# MAGIC FROM workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese
# MAGIC GROUP BY cancellation_status
# MAGIC ORDER BY cancellation_status

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.2 Creare la dashboard e il primo dataset

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output: il testo della query (da copiare nell'editor del dataset), poi il numero delle righe.
# MAGIC ```
# MAGIC SELECT destination, country, check_in_month,
# MAGIC        booking_count, cancelled_count, revenue,
# MAGIC        cancellation_rate, cancellation_status
# MAGIC FROM workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese
# MAGIC 317
# MAGIC ```

# COMMAND ----------

dataset_query = f"""SELECT destination, country, check_in_month,
       booking_count, cancelled_count, revenue,
       cancellation_rate, cancellation_status
FROM {PROJECT_REPORT_TABLE}"""

print(dataset_query)
print(spark.sql(dataset_query).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.3 I primi widget: i contatori

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 13590 5123 7529860.44
# MAGIC ```

# COMMAND ----------

totals = report_df.agg(
    F.sum("booking_count").alias("booking_count"),
    F.sum("cancelled_count").alias("cancelled_count"),
    F.round(F.sum("revenue"), 2).alias("revenue"),
).collect()[0]

print(totals["booking_count"], totals["cancelled_count"], totals["revenue"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.4 Le misure: il tasso complessivo

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 37.7 37.3 11825.9
# MAGIC ```

# COMMAND ----------

rates = report_df.agg(
    F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1).alias("overall_cancellation_rate"),
    F.round(F.avg("cancellation_rate"), 1).alias("average_of_rates"),
    F.round(F.sum("cancellation_rate"), 1).alias("sum_of_rates"),
).collect()[0]

print(rates["overall_cancellation_rate"], rates["average_of_rates"], rates["sum_of_rates"])

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC overall_cancellation_rate  average_of_rates
# MAGIC 37.7                       37.3
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ROUND(SUM(cancelled_count) / SUM(booking_count) * 100, 1) AS overall_cancellation_rate,
# MAGIC        ROUND(AVG(cancellation_rate), 1)                          AS average_of_rates
# MAGIC FROM workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 147
# MAGIC ```

# COMMAND ----------

critical_count = report_df.filter(F.col("cancellation_status") == "critico").count()
print(critical_count)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.5 La soglia come parametro

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output: il testo della query con il parametro `:threshold` (da copiare nell'editor del dataset al posto della prima query).
# MAGIC ```
# MAGIC SELECT destination, country, check_in_month,
# MAGIC        booking_count, cancelled_count, revenue, cancellation_rate,
# MAGIC        CASE WHEN booking_count < 20 THEN 'non valutabile'
# MAGIC             WHEN cancellation_rate > :threshold THEN 'critico'
# MAGIC             ELSE 'ok' END AS cancellation_status
# MAGIC FROM workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese
# MAGIC ```

# COMMAND ----------

dashboard_query = f"""SELECT destination, country, check_in_month,
       booking_count, cancelled_count, revenue, cancellation_rate,
       CASE WHEN booking_count < {MIN_BOOKINGS} THEN 'non valutabile'
            WHEN cancellation_rate > :threshold THEN 'critico'
            ELSE 'ok' END AS cancellation_status
FROM {PROJECT_REPORT_TABLE}"""

print(dashboard_query)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Lo stesso parametro nel notebook

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE VOLUTO**: la cella seguente deve fallire; la cella *Correzione* sotto deve funzionare.
# MAGIC Risultato atteso – messaggio (riga di riepilogo):
# MAGIC ```
# MAGIC [UNBOUND_SQL_PARAMETER] Found the unbound parameter: threshold. Please, fix `args` and provide a mapping of the parameter to either a SQL literal or collection constructor functions such as `map()`, `array()`, `struct()`. SQLSTATE: 42P02
# MAGIC ```
# MAGIC Il traceback indica la riga 2 della cella.

# COMMAND ----------

# ERRORE VOLUTO – la query ha un parametro, ma nessun valore
print(spark.sql(dashboard_query).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso della correzione – output:
# MAGIC ```
# MAGIC Soglia 30.0: 147 combinazioni critiche
# MAGIC Soglia 40.0: 59 combinazioni critiche
# MAGIC ```

# COMMAND ----------

# Correzione: il valore del parametro passato con args
for threshold in DASHBOARD_THRESHOLDS:
    status_df = spark.sql(dashboard_query, args={"threshold": threshold})
    critical_count = status_df.filter(F.col("cancellation_status") == "critico").count()
    print(f"Soglia {threshold}: {critical_count} combinazioni critiche")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 59
# MAGIC ```

# COMMAND ----------

print(report_df.filter(cancellation_status_column(threshold=40.0) == "critico").count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.6 I filtri

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 714 37.8 11
# MAGIC ```

# COMMAND ----------

italy_totals = (
    report_df
    .filter(F.col("country") == "Italy")
    .agg(
        F.sum("booking_count").alias("booking_count"),
        F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1).alias("overall_cancellation_rate"),
        F.sum(F.when(F.col("cancellation_status") == "critico", 1).otherwise(0)).alias("critical_count"),
    )
    .collect()[0]
)

print(italy_totals["booking_count"], italy_totals["overall_cancellation_rate"], italy_totals["critical_count"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.7 Un grafico a barre

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC check_in_month  booking_count  cancelled_count  cancellation_rate  average_of_rates
# MAGIC 1               204            68               33.3               29
# MAGIC 2               211            71               33.6               28.9
# MAGIC 3               319            125              39.2               43.1
# MAGIC 4               337            141              41.8               38.9
# MAGIC 5               379            154              40.6               43
# MAGIC 6               1661           639              38.5               37.6
# MAGIC 7               2050           750              36.6               40.6
# MAGIC 8               2431           904              37.2               36.8
# MAGIC 9               1577           594              37.7               33.9
# MAGIC 10              1163           436              37.5               38.3
# MAGIC 11              1396           529              37.9               38.2
# MAGIC 12              1862           712              38.2               40.9
# MAGIC ```

# COMMAND ----------

monthly_df = (
    report_df
    .groupBy("check_in_month")
    .agg(
        F.sum("booking_count").alias("booking_count"),
        F.sum("cancelled_count").alias("cancelled_count"),
        F.round(F.avg("cancellation_rate"), 1).alias("average_of_rates"),
    )
    .withColumn("cancellation_rate", F.round(F.col("cancelled_count") / F.col("booking_count") * 100, 1))
    .select("check_in_month", "booking_count", "cancelled_count", "cancellation_rate", "average_of_rates")
    .orderBy("check_in_month")
)
display(monthly_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.8 La tabella delle combinazioni critiche

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC destination  country               check_in_month  booking_count  cancelled_count  cancellation_rate
# MAGIC Singapore    Singapore             4               20             11               55
# MAGIC Ibiza        Spain                 6               68             37               54.4
# MAGIC London       United Kingdom        11              37             20               54.1
# MAGIC Cairo        Egypt                 10              30             16               53.3
# MAGIC Paris        France                4               54             28               51.9
# MAGIC Berlin       Germany               8               35             18               51.4
# MAGIC Abu Dhabi    United Arab Emirates  5               38             19               50
# MAGIC Amalfi       Italy                 8               20             10               50
# MAGIC ```

# COMMAND ----------

display(
    report_df
    .filter(F.col("cancellation_status") == "critico")
    .select("destination", "country", "check_in_month", "booking_count", "cancelled_count", "cancellation_rate")
    .orderBy(F.col("cancellation_rate").desc(), "destination", "check_in_month")
    .limit(8)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.9 Il layout e il testo

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.10 Pubblicare e condividere

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.11 L'aggiornamento dei dati

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.12 Verificare la dashboard

# COMMAND ----------

# MAGIC %md
# MAGIC Nel dizionario `dashboard_values` si scrivono i valori letti sulla dashboard (bozza o versione pubblicata, filtri al valore predefinito). Risultato atteso – output:
# MAGIC ```
# MAGIC Prenotazioni                       13590     13590  OK
# MAGIC Tasso di cancellazione (%)          37.7      37.7  OK
# MAGIC Combinazioni critiche                147       147  OK
# MAGIC ```

# COMMAND ----------

# I valori letti sulla dashboard, scritti a mano (con il punto per i decimali)
dashboard_values = {
    "Prenotazioni": 13590,
    "Tasso di cancellazione (%)": 37.7,
    "Combinazioni critiche": 147,
}

# Gli stessi valori calcolati nel notebook
expected_values = {
    "Prenotazioni": totals["booking_count"],
    "Tasso di cancellazione (%)": rates["overall_cancellation_rate"],
    "Combinazioni critiche": report_df.filter(F.col("cancellation_status") == "critico").count(),
}

for widget_name, value in dashboard_values.items():
    expected = expected_values[widget_name]
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    print(f"{widget_name:<30}{value:>10}{expected:>10}  {outcome}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12.13 Errori comuni della dashboard

# COMMAND ----------

# MAGIC %md
# MAGIC ### La media dei tassi

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 35.4
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – il tasso dell'Italia calcolato come media dei tassi
italy_df = report_df.filter(F.col("country") == "Italy")
print(italy_df.agg(F.round(F.avg("cancellation_rate"), 1)).collect()[0][0])

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso della correzione – output:
# MAGIC ```
# MAGIC 37.8
# MAGIC ```

# COMMAND ----------

# Correzione: cancellate totali diviso prenotazioni totali
print(italy_df.agg(F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1)).collect()[0][0])
