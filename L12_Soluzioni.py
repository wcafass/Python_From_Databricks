# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 12 – Soluzioni
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; il notebook `L11_Progetto_Finale` eseguito almeno una volta (tabella `g_cancellazioni_aggiornate_destinazione_mese`); il notebook `utils` nella stessa cartella `Libro_Python`. Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Commenti alle soluzioni: Appendice A.
# MAGIC
# MAGIC Le soluzioni contengono la parte di notebook di ogni esercizio; la parte nella dashboard è descritta nelle celle di testo. Il notebook **non scrive tabelle**. Si eseguono prima la cella con `%run ./utils` e la cella di preparazione, poi le soluzioni in ordine. L'esercizio 8 contiene una cella che deve fallire (**ERRORE VOLUTO**) e due celle che producono un risultato sbagliato (**ERRORE SILENZIOSO**), ciascuna con la correzione nella cella subito sotto. Non usare Run all: si fermerebbe alla cella 8a.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione
# MAGIC
# MAGIC Risultato atteso: `317` e `Preparazione completata`.

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
# MAGIC Dashboard: **Add a visualization** → **Counter** → **Value** `revenue` (**SUM**); nel campo, **Format** → **Custom**, **Abbreviation** → **None**; titolo **Ricavo**. Valori: `7.529.860,44` (Paese **All**) e `408.538,77` (Paese **Italy**).
# MAGIC
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 7529860.44 408538.77
# MAGIC ```

# COMMAND ----------

total_revenue = report_df.agg(F.round(F.sum("revenue"), 2)).collect()[0][0]
italy_revenue = (
    report_df
    .filter(F.col("country") == "Italy")
    .agg(F.round(F.sum("revenue"), 2))
    .collect()[0][0]
)
print(total_revenue, italy_revenue)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Un filtro sulla destinazione
# MAGIC
# MAGIC Dashboard: **Add a filter (field/parameter)** → **Multiple values** → **Fields** `destination`; titolo **Destinazione**; valore **Amalfi**. Contatori: `51`, `41,2`, `1`, `29.503,96`.
# MAGIC
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC Prenotazioni                          51        51  OK
# MAGIC Tasso di cancellazione (%)          41.2      41.2  OK
# MAGIC Combinazioni critiche                  1         1  OK
# MAGIC Ricavo                          29503.96  29503.96  OK
# MAGIC ```

# COMMAND ----------

amalfi = (
    report_df
    .filter(F.col("destination") == "Amalfi")
    .agg(
        F.sum("booking_count").alias("booking_count"),
        F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1).alias("overall_cancellation_rate"),
        F.sum(F.when(F.col("cancellation_status") == "critico", 1).otherwise(0)).alias("critical_count"),
        F.round(F.sum("revenue"), 2).alias("revenue"),
    )
    .collect()[0]
)

amalfi_dashboard = {
    "Prenotazioni": 51,
    "Tasso di cancellazione (%)": 41.2,
    "Combinazioni critiche": 1,
    "Ricavo": 29503.96,
}
amalfi_expected = {
    "Prenotazioni": amalfi["booking_count"],
    "Tasso di cancellazione (%)": amalfi["overall_cancellation_rate"],
    "Combinazioni critiche": amalfi["critical_count"],
    "Ricavo": amalfi["revenue"],
}

for widget_name, value in amalfi_dashboard.items():
    expected = amalfi_expected[widget_name]
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    print(f"{widget_name:<30}{value:>10}{expected:>10}  {outcome}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – La soglia in movimento
# MAGIC
# MAGIC Dashboard: il contatore **Combinazioni critiche** vale `157`, `115`, `32`, `6` con le soglie 25, 35, 45, 50.
# MAGIC
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 25.0 157
# MAGIC 35.0 115
# MAGIC 45.0 32
# MAGIC 50.0 6
# MAGIC ```

# COMMAND ----------

for threshold in [25.0, 35.0, 45.0, 50.0]:
    status_df = spark.sql(exercise_query, args={"threshold": threshold, "min_bookings": MIN_BOOKINGS})
    print(threshold, status_df.filter(F.col("cancellation_status") == "critico").count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Il grafico per paese
# MAGIC
# MAGIC Dashboard: grafico **Bar**, **X axis** `country` (un testo, quindi già una categoria), **Y axis** la misura `overall_cancellation_rate`, **Labels** attivo.
# MAGIC
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC country               overall_cancellation_rate  average_of_rates
# MAGIC China                 44.6                       50.4
# MAGIC India                 42.7                       41.7
# MAGIC Egypt                 40.7                       36.2
# MAGIC France                40.1                       35.5
# MAGIC Greece                38.9                       35.9
# MAGIC Australia             38.6                       39.6
# MAGIC Singapore             37.9                       39
# MAGIC Italy                 37.8                       35.4
# MAGIC Germany               37.5                       37.7
# MAGIC Spain                 37.5                       37.9
# MAGIC United States         37.2                       40.3
# MAGIC United Arab Emirates  37                         37.3
# MAGIC Thailand              36.6                       37
# MAGIC Japan                 36.3                       37.8
# MAGIC Austria               35.7                       20.8
# MAGIC United Kingdom        35                         31.9
# MAGIC Switzerland           30.8                       30.7
# MAGIC Canada                29.6                       18.4
# MAGIC ```
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC China 44.6
# MAGIC Canada 29.6
# MAGIC ```

# COMMAND ----------

country_df = (
    report_df
    .groupBy("country")
    .agg(
        F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1).alias("overall_cancellation_rate"),
        F.round(F.avg("cancellation_rate"), 1).alias("average_of_rates"),
    )
    .orderBy(F.col("overall_cancellation_rate").desc(), "country")
)
display(country_df)

# COMMAND ----------

country_rows = country_df.collect()
print(country_rows[0]["country"], country_rows[0]["overall_cancellation_rate"])
print(country_rows[-1]["country"], country_rows[-1]["overall_cancellation_rate"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Il volume minimo come parametro
# MAGIC
# MAGIC Dashboard: nella query del dataset `20` diventa `:min_bookings`; nel riquadro del nuovo parametro, ingranaggio → **Type** **Numeric**, **Display name** `Volume minimo`, valore 20; sulla pagina un filtro **Single value** con **Parameters** → **Volume minimo**.
# MAGIC
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 10 [('critico', 190), ('non valutabile', 93), ('ok', 34)]
# MAGIC 30 [('critico', 114), ('non valutabile', 191), ('ok', 12)]
# MAGIC ```

# COMMAND ----------

for min_bookings in [10, 30]:
    status_df = spark.sql(exercise_query, args={"threshold": 30.0, "min_bookings": min_bookings})
    status_rows = status_df.groupBy("cancellation_status").count().orderBy("cancellation_status").collect()
    print(min_bookings, [(row["cancellation_status"], row["count"]) for row in status_rows])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Una pagina per continente
# MAGIC
# MAGIC Dashboard: **Data** → **+ Add SQL dataset** con la query stampata qui sotto (nome **Report per continente**); **+ Add custom calculation** con `ROUND(SUM(cancelled_count) / SUM(booking_count) * 100, 1)`; nuova pagina con **+** accanto alle pagine, rinominata **Continenti**, con un grafico **Bar** (`continent` sull'asse X, la misura sull'asse Y) e una **Table**.
# MAGIC
# MAGIC Risultato atteso – output: il testo della query, `317`, poi la griglia.
# MAGIC ```
# MAGIC continent      booking_count  cancelled_count  overall_cancellation_rate
# MAGIC Europe         5557           2110             38
# MAGIC Asia           5290           1969             37.2
# MAGIC Oceania        1246           481              38.6
# MAGIC North America  1212           447              36.9
# MAGIC Africa         285            116              40.7
# MAGIC ```

# COMMAND ----------

continent_query = f"""SELECT r.destination, r.country, c.continent, r.check_in_month,
       r.booking_count, r.cancelled_count, r.revenue, r.cancellation_rate
FROM {PROJECT_REPORT_TABLE} r
JOIN {COUNTRIES_TABLE} c ON r.country = c.country"""

print(continent_query)
continent_df = spark.sql(continent_query)
print(continent_df.count())
display(
    continent_df
    .groupBy("continent")
    .agg(
        F.sum("booking_count").alias("booking_count"),
        F.sum("cancelled_count").alias("cancelled_count"),
        F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1).alias("overall_cancellation_rate"),
    )
    .orderBy(F.col("booking_count").desc())
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – La verifica di una vista filtrata
# MAGIC
# MAGIC Dashboard: **Paese** **Italy**, soglia 40, volume minimo 20. Contatori: `714`, `37,8`, `4`, `408.538,77`.
# MAGIC
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC Prenotazioni                         714       714  OK
# MAGIC Tasso di cancellazione (%)          37.8      37.8  OK
# MAGIC Combinazioni critiche                  4         4  OK
# MAGIC Ricavo                         408538.77 408538.77  OK
# MAGIC ```

# COMMAND ----------

italy_view = (
    spark.sql(exercise_query, args={"threshold": 40.0, "min_bookings": 20})
    .filter(F.col("country") == "Italy")
    .agg(
        F.sum("booking_count").alias("booking_count"),
        F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1).alias("overall_cancellation_rate"),
        F.sum(F.when(F.col("cancellation_status") == "critico", 1).otherwise(0)).alias("critical_count"),
        F.round(F.sum("revenue"), 2).alias("revenue"),
    )
    .collect()[0]
)

italy_dashboard = {
    "Prenotazioni": 714,
    "Tasso di cancellazione (%)": 37.8,
    "Combinazioni critiche": 4,
    "Ricavo": 408538.77,
}
italy_expected = {
    "Prenotazioni": italy_view["booking_count"],
    "Tasso di cancellazione (%)": italy_view["overall_cancellation_rate"],
    "Combinazioni critiche": italy_view["critical_count"],
    "Ricavo": italy_view["revenue"],
}

for widget_name, value in italy_dashboard.items():
    expected = italy_expected[widget_name]
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    print(f"{widget_name:<30}{value:>10}{expected:>10}  {outcome}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC
# MAGIC Dashboard: **8d** si sostituisce `AVG(cancellation_rate)` con la misura `overall_cancellation_rate` (37,7); **8e** nel campo dell'asse X si sceglie **Scale type** → **Categorical** (le 12 barre della sezione 12.7); **8f** si fa clic su **Publish** e la versione pubblicata mostra il titolo nuovo.

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE VOLUTO**: la cella seguente deve fallire; la cella *Correzione* sotto deve funzionare.
# MAGIC Risultato atteso – messaggio (riga di riepilogo):
# MAGIC ```
# MAGIC [UNBOUND_SQL_PARAMETER] Found the unbound parameter: min_bookings. Please, fix `args` and provide a mapping of the parameter to either a SQL literal or collection constructor functions such as `map()`, `array()`, `struct()`. SQLSTATE: 42P02
# MAGIC ```
# MAGIC Risultato atteso della correzione: `317`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (la query con due parametri)
print(spark.sql(exercise_query, args={"threshold": 30.0}).count())

# COMMAND ----------

# Correzione 8a: un valore per ogni parametro della query
print(spark.sql(exercise_query, args={"threshold": 30.0, "min_bookings": 20}).count())

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso: `31.9`; della correzione: `35.0`.

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8b (il tasso del Regno Unito)
uk_df = report_df.filter(F.col("country") == "United Kingdom")
print(uk_df.agg(F.round(F.avg("cancellation_rate"), 1)).collect()[0][0])

# COMMAND ----------

# Correzione 8b: il tasso dalle somme, non la media dei tassi
print(uk_df.agg(F.round(F.sum("cancelled_count") / F.sum("booking_count") * 100, 1)).collect()[0][0])

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso: `False`; della correzione: `True`.

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8c (il valore letto sulla dashboard)
dashboard_bookings = 13.590
print(dashboard_bookings == 13590)

# COMMAND ----------

# Correzione 8c: il numero si trascrive senza il punto delle migliaia
dashboard_bookings = 13590
print(dashboard_bookings == 13590)
