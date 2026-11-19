# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 11 – Progetto finale
# MAGIC
# MAGIC Notebook del Capitolo 11 di *Oltre la SELECT*. Obiettivi: profilare, pulire, aggiornare con un `MERGE`, aggregare e verificare le prenotazioni 2024, fino al report `g_cancellazioni_aggiornate_destinazione_mese`.
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito; il notebook `utils` nella stessa cartella `Libro_Python`. Il notebook **scrive tabelle** nello schema `workspace.libro_python`: `s_prenotazioni_pulite_prenotazione`, `s_aggiornamenti_puliti_prenotazione`, `g_cancellazioni_aggiornate_destinazione_mese`.
# MAGIC
# MAGIC Si esegue **una cella alla volta**, dall'alto in basso: la sezione 11.12 contiene celle che devono fallire (**ERRORE VOLUTO**) o che producono un risultato sbagliato (**ERRORE SILENZIOSO**), ciascuna con la correzione nella cella subito sotto; alcune scrivono sulla tabella pulita e la riparano. Non usare Run all. Se il compute si ferma, si rieseguono la cella `%run ./utils`, la cella delle costanti e le celle che creano le variabili usate più avanti.
# MAGIC
# MAGIC I risultati attesi sono quelli della **prima esecuzione** del notebook; se lo si riesegue, cambiano solo lo storico (versioni in più) e, se si riesegue da sola la cella del `MERGE`, i suoi contatori (`9133 9133 0 0`).

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
# MAGIC workspace.libro_python.s_prenotazioni_pulite_prenotazione
# MAGIC workspace.libro_python.s_aggiornamenti_puliti_prenotazione
# MAGIC workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese
# MAGIC ```

# COMMAND ----------

# Costanti del capitolo: le tabelle che il progetto scrive e la chiave del MERGE
CLEAN_BOOKINGS_TABLE = build_table_name("prenotazioni_pulite", "prenotazione")
CLEAN_UPDATES_TABLE = build_table_name("aggiornamenti_puliti", "prenotazione")
PROJECT_REPORT_TABLE = build_table_name("cancellazioni_aggiornate", "destinazione_mese", layer="g")
MERGE_KEY = "t.booking_id = s.booking_id"

# Tabelle di decodifica, lette una volta
properties_df = spark.table(PROPERTIES_TABLE)
destinations_df = spark.table(DESTINATIONS_TABLE)

print(CLEAN_BOOKINGS_TABLE)
print(CLEAN_UPDATES_TABLE)
print(PROJECT_REPORT_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.1 Leggere e profilare le prenotazioni

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC righe                       13626
# MAGIC righe distinte              13586
# MAGIC chiavi (booking_id)         13586
# MAGIC importo mancante               30
# MAGIC importo negativo               12
# MAGIC date invertite                  8
# MAGIC struttura sconosciuta           0
# MAGIC ```

# COMMAND ----------

bookings_2024_df = (
    spark.table(BOOKINGS_TABLE)
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
known_properties_df = properties_df.select("property_id").withColumn("is_known_property", F.lit(True))

booking_profile = {
    "righe": bookings_2024_df.count(),
    "righe distinte": bookings_2024_df.distinct().count(),
    "chiavi (booking_id)": bookings_2024_df.select("booking_id").distinct().count(),
    "importo mancante": bookings_2024_df.filter(F.col("total_amount").isNull()).count(),
    "importo negativo": bookings_2024_df.filter(F.col("total_amount") < 0).count(),
    "date invertite": bookings_2024_df.filter(F.col("check_out") < F.col("check_in")).count(),
    "struttura sconosciuta": (
        bookings_2024_df
        .join(known_properties_df, on="property_id", how="left")
        .filter(F.col("is_known_property").isNull())
        .count()
    ),
}

for check_name, value in booking_profile.items():
    print(f"{check_name:<25}{value:>8}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Righe distinte e chiavi

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)                                                 AS row_count,
# MAGIC        (SELECT COUNT(*) FROM (SELECT DISTINCT *
# MAGIC                               FROM workspace.libro_python.b_bookings
# MAGIC                               WHERE year(check_in) = 2024))     AS distinct_row_count,
# MAGIC        COUNT(DISTINCT booking_id)                               AS key_count,
# MAGIC        SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END)    AS missing_amount,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)        AS negative_amount,
# MAGIC        SUM(CASE WHEN check_out < check_in THEN 1 ELSE 0 END)    AS inverted_dates
# MAGIC FROM workspace.libro_python.b_bookings
# MAGIC WHERE year(check_in) = 2024

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.2 Profilare gli aggiornamenti

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC righe                       15820
# MAGIC righe distinte              15820
# MAGIC chiavi (booking_id)          9133
# MAGIC pareggi su updated_at          57
# MAGIC importo mancante                0
# MAGIC importo negativo                4
# MAGIC date invertite                  0
# MAGIC prenotazioni nuove              4
# MAGIC ```

# COMMAND ----------

updates_2024_df = (
    spark.table(BOOKING_UPDATES_TABLE)
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
ties_df = (
    updates_2024_df
    .groupBy("booking_id", "updated_at")
    .agg(F.count("*").alias("row_count"))
    .filter(F.col("row_count") > 1)
)
known_bookings_df = bookings_2024_df.select("booking_id").distinct().withColumn("is_known_booking", F.lit(True))

update_profile = {
    "righe": updates_2024_df.count(),
    "righe distinte": updates_2024_df.distinct().count(),
    "chiavi (booking_id)": updates_2024_df.select("booking_id").distinct().count(),
    "pareggi su updated_at": ties_df.count(),
    "importo mancante": updates_2024_df.filter(F.col("total_amount").isNull()).count(),
    "importo negativo": updates_2024_df.filter(F.col("total_amount") < 0).count(),
    "date invertite": updates_2024_df.filter(F.col("check_out") < F.col("check_in")).count(),
    "prenotazioni nuove": (
        updates_2024_df
        .join(known_bookings_df, on="booking_id", how="left")
        .filter(F.col("is_known_booking").isNull())
        .select("booking_id")
        .distinct()
        .count()
    ),
}

for check_name, value in update_profile.items():
    print(f"{check_name:<25}{value:>8}")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC booking_id  booking_update_id  status     total_amount      updated_at
# MAGIC 2563        17570289891300     pending    776.260009765625  2024-07-13T23:59:59.000+00:00
# MAGIC 2563        17570289907102     cancelled  776.260009765625  2024-07-13T23:59:59.000+00:00
# MAGIC ```

# COMMAND ----------

display(
    updates_2024_df
    .filter(F.col("booking_id") == 2563)
    .select("booking_id", "booking_update_id", "status", "total_amount", "updated_at")
    .orderBy("booking_update_id")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.3 Le regole di pulizia

# COMMAND ----------

# MAGIC %md
# MAGIC ### Le colonne di tracciamento

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.4 Le regole in una funzione

# COMMAND ----------

def quality_note_column():
    """Nota di qualità di una prenotazione, calcolata sui valori non ancora corretti."""
    return (
        F.when(F.col("total_amount").isNull(), "importo mancante")
        .when(F.col("total_amount") < 0, "importo negativo")
        .when(F.col("check_out") < F.col("check_in"), "date invertite")
        .otherwise("ok")
    )

# COMMAND ----------

def clean_booking_values(df, source):
    """Applica le regole di pulizia del progetto a un DataFrame di prenotazioni.

    Aggiunge quality_note (calcolata prima delle correzioni) e source;
    scambia check_in e check_out se sono invertite; arrotonda l'importo
    a 2 decimali come double e rende NULL gli importi negativi.
    """
    dates_inverted = F.col("check_out") < F.col("check_in")
    rounded_amount = F.round(F.col("total_amount").cast("double"), 2)
    return (
        df
        .withColumn("quality_note", quality_note_column())
        .select(
            "booking_id",
            "user_id",
            "property_id",
            F.when(dates_inverted, F.col("check_out")).otherwise(F.col("check_in")).alias("check_in"),
            F.when(dates_inverted, F.col("check_in")).otherwise(F.col("check_out")).alias("check_out"),
            "guests_count",
            F.when(rounded_amount >= 0, rounded_amount).alias("total_amount"),
            "status",
            "created_at",
            "updated_at",
            "quality_note",
            F.lit(source).alias("source"),
        )
    )

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC quality_note      booking_count
# MAGIC date invertite    8
# MAGIC importo mancante  30
# MAGIC importo negativo  12
# MAGIC ok                13536
# MAGIC ```

# COMMAND ----------

clean_bookings_df = (
    clean_booking_values(spark.table(BOOKINGS_TABLE).distinct(), "originale")
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
display(
    clean_bookings_df
    .groupBy("quality_note")
    .agg(F.count("*").alias("booking_count"))
    .orderBy("quality_note")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.5 Scrivere la tabella pulita

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_pulite_prenotazione (mode=overwrite)
# MAGIC Righe nella tabella: 13,586
# MAGIC ```

# COMMAND ----------

write_table(clean_bookings_df, CLEAN_BOOKINGS_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC righe                       13586   13586  OK
# MAGIC chiavi (booking_id)         13586   13586  OK
# MAGIC importo negativo                0       0  OK
# MAGIC date invertite                  0       0  OK
# MAGIC ```

# COMMAND ----------

clean_table_df = spark.table(CLEAN_BOOKINGS_TABLE)
clean_checks = {
    "righe": (clean_table_df.count(), booking_profile["chiavi (booking_id)"]),
    "chiavi (booking_id)": (clean_table_df.select("booking_id").distinct().count(), booking_profile["chiavi (booking_id)"]),
    "importo negativo": (clean_table_df.filter(F.col("total_amount") < 0).count(), 0),
    "date invertite": (clean_table_df.filter(F.col("check_out") < F.col("check_in")).count(), 0),
}

for check_name, (value, expected) in clean_checks.items():
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    print(f"{check_name:<25}{value:>8}{expected:>8}  {outcome}")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS booking_count,
# MAGIC        SUM(CASE WHEN c.check_in <> o.check_in OR c.check_out <> o.check_out THEN 1 ELSE 0 END) AS different_dates
# MAGIC FROM workspace.libro_python.s_prenotazioni_pulite_prenotazione c
# MAGIC JOIN samples.wanderbricks.bookings o USING (booking_id)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.6 Una riga per prenotazione: versioni e pareggi

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 9188 9133
# MAGIC ```

# COMMAND ----------

last_update_df = (
    updates_2024_df
    .groupBy("booking_id")
    .agg(F.max("updated_at").alias("last_updated_at"))
)
latest_updates_df = (
    updates_2024_df
    .join(last_update_df, on="booking_id", how="inner")
    .filter(F.col("updated_at") == F.col("last_updated_at"))
)
print(latest_updates_df.count(), latest_updates_df.select("booking_id").distinct().count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 9133 9133
# MAGIC ```

# COMMAND ----------

last_update_id_df = (
    latest_updates_df
    .groupBy("booking_id")
    .agg(F.max("booking_update_id").alias("booking_update_id"))
)
chosen_updates_df = latest_updates_df.join(
    last_update_id_df,
    on=["booking_id", "booking_update_id"],
    how="inner",
)
print(chosen_updates_df.count(), chosen_updates_df.select("booking_id").distinct().count())

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH updates_2024 AS (
# MAGIC   SELECT * FROM samples.wanderbricks.booking_updates WHERE year(check_in) = 2024
# MAGIC ),
# MAGIC last_update AS (
# MAGIC   SELECT booking_id, MAX(updated_at) AS updated_at FROM updates_2024 GROUP BY booking_id
# MAGIC ),
# MAGIC latest AS (
# MAGIC   SELECT * FROM updates_2024 JOIN last_update USING (booking_id, updated_at)
# MAGIC ),
# MAGIC last_update_id AS (
# MAGIC   SELECT booking_id, MAX(booking_update_id) AS booking_update_id FROM latest GROUP BY booking_id
# MAGIC )
# MAGIC SELECT COUNT(*) AS row_count, COUNT(DISTINCT booking_id) AS key_count
# MAGIC FROM latest JOIN last_update_id USING (booking_id, booking_update_id)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC booking_id  booking_update_id  status     updated_at
# MAGIC 2563        17570289907102     cancelled  2024-07-13T23:59:59.000+00:00
# MAGIC ```

# COMMAND ----------

display(
    chosen_updates_df
    .filter(F.col("booking_id") == 2563)
    .select("booking_id", "booking_update_id", "status", "updated_at")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (le due righe di `write_table`, poi la griglia, poi `True`):
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_aggiornamenti_puliti_prenotazione (mode=overwrite)
# MAGIC Righe nella tabella: 9,133
# MAGIC
# MAGIC quality_note      booking_count
# MAGIC importo negativo  1
# MAGIC ok                9132
# MAGIC
# MAGIC True
# MAGIC ```

# COMMAND ----------

clean_updates_df = clean_booking_values(chosen_updates_df, "aggiornamento")
write_table(clean_updates_df, CLEAN_UPDATES_TABLE)
display(
    spark.table(CLEAN_UPDATES_TABLE)
    .groupBy("quality_note")
    .agg(F.count("*").alias("booking_count"))
    .orderBy("quality_note")
)
print(spark.table(CLEAN_UPDATES_TABLE).columns == spark.table(CLEAN_BOOKINGS_TABLE).columns)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.7 Applicare gli aggiornamenti: il MERGE

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC num_affected_rows  num_updated_rows  num_deleted_rows  num_inserted_rows
# MAGIC 9133               9129              0                 4
# MAGIC ```

# COMMAND ----------

merge_query = f"""
MERGE INTO {CLEAN_BOOKINGS_TABLE} AS t
USING {CLEAN_UPDATES_TABLE} AS s
ON {MERGE_KEY}
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""
display(spark.sql(merge_query))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 13590 13590
# MAGIC ```
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC source         quality_note      booking_count
# MAGIC aggiornamento  importo negativo  1
# MAGIC aggiornamento  ok                9132
# MAGIC originale      date invertite    2
# MAGIC originale      importo mancante  13
# MAGIC originale      importo negativo  2
# MAGIC originale      ok                4440
# MAGIC ```

# COMMAND ----------

merged_df = spark.table(CLEAN_BOOKINGS_TABLE)
print(merged_df.count(), merged_df.select("booking_id").distinct().count())
display(
    merged_df
    .groupBy("source", "quality_note")
    .agg(F.count("*").alias("booking_count"))
    .orderBy("source", "quality_note")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC status     before_merge  after_merge
# MAGIC cancelled  2647          5123
# MAGIC completed  1433          7090
# MAGIC confirmed  3491          1156
# MAGIC pending    6015          221
# MAGIC ```

# COMMAND ----------

before_df = clean_bookings_df.groupBy("status").agg(F.count("*").alias("before_merge"))
after_df = merged_df.groupBy("status").agg(F.count("*").alias("after_merge"))
display(before_df.join(after_df, on="status", how="inner").orderBy("status"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status, before_merge, after_merge
# MAGIC FROM (SELECT status, COUNT(*) AS before_merge
# MAGIC       FROM (SELECT DISTINCT * FROM workspace.libro_python.b_bookings)
# MAGIC       WHERE year(CASE WHEN check_out < check_in THEN check_out ELSE check_in END) = 2024
# MAGIC       GROUP BY status)
# MAGIC JOIN (SELECT status, COUNT(*) AS after_merge
# MAGIC       FROM workspace.libro_python.s_prenotazioni_pulite_prenotazione
# MAGIC       GROUP BY status)
# MAGIC USING (status)
# MAGIC ORDER BY status

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.8 Il report

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.g_cancellazioni_aggiornate_destinazione_mese (mode=overwrite)
# MAGIC Righe nella tabella: 317
# MAGIC ```

# COMMAND ----------

report_df = (
    spark.table(CLEAN_BOOKINGS_TABLE)
    .select("booking_id", "property_id", "check_in", "status", "total_amount")
    .join(properties_df.select("property_id", "destination_id"), on="property_id", how="inner")
    .join(destinations_df.select("destination_id", "destination", "country"), on="destination_id", how="inner")
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
write_table(report_df, PROJECT_REPORT_TABLE)

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

report_table_df = spark.table(PROJECT_REPORT_TABLE)
display(
    report_table_df
    .groupBy("cancellation_status")
    .agg(F.count("*").alias("combination_count"))
    .orderBy("cancellation_status")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC destination  country  check_in_month  booking_count  cancelled_count  revenue   cancellation_rate  cancellation_status
# MAGIC Amalfi       Italy    6               13             6                7356      46.2               non valutabile
# MAGIC Amalfi       Italy    7               9              3                6918.84   33.3               non valutabile
# MAGIC Amalfi       Italy    8               20             10               11138.2   50                 critico
# MAGIC Amalfi       Italy    9               9              2                4090.92   22.2               non valutabile
# MAGIC ```

# COMMAND ----------

display(report_table_df.filter(F.col("destination") == "Amalfi").orderBy("check_in_month"))

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC destination  country         check_in_month  booking_count  cancelled_count  revenue   cancellation_rate  cancellation_status
# MAGIC Singapore    Singapore       4               20             11               10950.05  55                 critico
# MAGIC Ibiza        Spain           6               68             37               39895.55  54.4               critico
# MAGIC London       United Kingdom  11              37             20               21075.88  54.1               critico
# MAGIC Cairo        Egypt           10              30             16               15458.08  53.3               critico
# MAGIC Paris        France          4               54             28               27885.04  51.9               critico
# MAGIC ```

# COMMAND ----------

display(
    report_table_df
    .filter(F.col("cancellation_status") == "critico")
    .orderBy(F.col("cancellation_rate").desc(), "destination", "check_in_month")
    .limit(5)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### La soglia è una decisione

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC status_threshold_40  combination_count
# MAGIC critico              59
# MAGIC non valutabile       152
# MAGIC ok                   106
# MAGIC ```

# COMMAND ----------

display(
    report_table_df
    .withColumn("status_threshold_40", cancellation_status_column(threshold=40.0))
    .groupBy("status_threshold_40")
    .agg(F.count("*").alias("combination_count"))
    .orderBy("status_threshold_40")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.9 La verifica indipendente

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 317 317 317 0
# MAGIC ```

# COMMAND ----------

check_query = f"""
SELECT d.destination,
       month(b.check_in)                                       AS check_in_month,
       COUNT(*)                                                AS chk_booking_count,
       SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS chk_cancelled_count,
       ROUND(SUM(b.total_amount), 2)                           AS chk_revenue
FROM {CLEAN_BOOKINGS_TABLE} b
JOIN {PROPERTIES_TABLE} p ON b.property_id = p.property_id
JOIN {DESTINATIONS_TABLE} d ON p.destination_id = d.destination_id
GROUP BY d.destination, month(b.check_in)
"""
check_df = spark.sql(check_query)

comparison_df = report_table_df.join(check_df, on=["destination", "check_in_month"], how="inner")
differences_df = comparison_df.filter(
    (F.col("booking_count") != F.col("chk_booking_count"))
    | (F.col("cancelled_count") != F.col("chk_cancelled_count"))
    | (F.col("revenue") != F.col("chk_revenue"))
)
print(report_table_df.count(), check_df.count(), comparison_df.count(), differences_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.10 I controlli finali e lo storico

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC righe = chiavi              13590   13590  OK
# MAGIC righe = chiavi + nuove      13590   13590  OK
# MAGIC righe da aggiornamenti       9133    9133  OK
# MAGIC importo negativo                0       0  OK
# MAGIC date invertite                  0       0  OK
# MAGIC prenotazioni nel report     13590   13590  OK
# MAGIC ```

# COMMAND ----------

final_checks = {
    "righe = chiavi": (merged_df.count(), merged_df.select("booking_id").distinct().count()),
    "righe = chiavi + nuove": (
        merged_df.count(),
        booking_profile["chiavi (booking_id)"] + update_profile["prenotazioni nuove"],
    ),
    "righe da aggiornamenti": (
        merged_df.filter(F.col("source") == "aggiornamento").count(),
        update_profile["chiavi (booking_id)"],
    ),
    "importo negativo": (merged_df.filter(F.col("total_amount") < 0).count(), 0),
    "date invertite": (merged_df.filter(F.col("check_out") < F.col("check_in")).count(), 0),
    "prenotazioni nel report": (
        report_table_df.agg(F.sum("booking_count")).collect()[0][0],
        merged_df.count(),
    ),
}

for check_name, (value, expected) in final_checks.items():
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    print(f"{check_name:<25}{value:>8}{expected:>8}  {outcome}")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC version  operation
# MAGIC 0        CREATE OR REPLACE TABLE AS SELECT
# MAGIC 1        MERGE
# MAGIC 2        OPTIMIZE
# MAGIC ```

# COMMAND ----------

display(
    spark.sql(f"DESCRIBE HISTORY {CLEAN_BOOKINGS_TABLE}")
    .select("version", "operation")
    .orderBy("version")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.11 Un notebook rieseguibile e un primo grafico

# COMMAND ----------

# MAGIC %md
# MAGIC ### Un primo grafico

# COMMAND ----------

display(
    report_table_df
    .filter(F.col("country") == "Italy")
    .select("destination", "check_in_month", "booking_count", "cancellation_rate", "cancellation_status")
    .orderBy("destination", "check_in_month")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11.12 Errori comuni del progetto

# COMMAND ----------

# MAGIC %md
# MAGIC ### La nota calcolata dopo le correzioni

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC quality_note      booking_count
# MAGIC importo mancante  42
# MAGIC ok                13544
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – la nota è calcolata dopo aver corretto i valori
late_note_df = (
    clean_booking_values(spark.table(BOOKINGS_TABLE).distinct(), "originale")
    .withColumn("quality_note", quality_note_column())
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
display(late_note_df.groupBy("quality_note").agg(F.count("*").alias("booking_count")).orderBy("quality_note"))

# COMMAND ----------

# Correzione: la nota calcolata dalla funzione, prima delle correzioni
display(clean_bookings_df.groupBy("quality_note").agg(F.count("*").alias("booking_count")).orderBy("quality_note"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Un filtro al posto della regola

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 13544
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – gli importi non validi tolti con un filtro
filtered_df = (
    spark.table(BOOKINGS_TABLE)
    .distinct()
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .filter(F.col("total_amount") >= 0)
)
print(filtered_df.count())

# COMMAND ----------

# Correzione: gli importi non validi diventano NULL, le prenotazioni restano
print(clean_bookings_df.count(), clean_bookings_df.filter(F.col("total_amount").isNull()).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Lo scambio delle date con due withColumn

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC 8
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – lo scambio delle date fatto con due withColumn
dates_inverted = F.col("check_out") < F.col("check_in")
swapped_df = (
    spark.table(BOOKINGS_TABLE)
    .distinct()
    .withColumn("check_in", F.when(dates_inverted, F.col("check_out")).otherwise(F.col("check_in")))
    .withColumn("check_out", F.when(dates_inverted, F.col("check_in")).otherwise(F.col("check_out")))
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
print(swapped_df.filter(F.col("check_in") == F.col("check_out")).count())

# COMMAND ----------

# Correzione: lo scambio fatto in un solo select, nella funzione
print(clean_bookings_df.filter(F.col("check_in") == F.col("check_out")).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Il MERGE con i pareggi

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE VOLUTO**: la cella seguente deve fallire; la cella *Correzione* sotto deve funzionare.
# MAGIC Risultato atteso – messaggio (riga di riepilogo):
# MAGIC ```
# MAGIC [DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE] Cannot perform Merge as multiple source rows matched and attempted to modify the same
# MAGIC target row in the Delta table in possibly conflicting ways. By SQL semantics of Merge,
# MAGIC when multiple source rows match on the same target row, the result may be ambiguous
# MAGIC as it is unclear which source row should be used to update or delete the matching
# MAGIC target row. You can preprocess the source table to eliminate the possibility of
# MAGIC multiple matches. Please refer to
# MAGIC https://docs.databricks.com/delta/merge.html#merge-error
# MAGIC  SQLSTATE: 21506
# MAGIC ```

# COMMAND ----------

# ERRORE VOLUTO – la sorgente ha ancora i pareggi sull'ultimo aggiornamento
clean_table = DeltaTable.forName(spark, CLEAN_BOOKINGS_TABLE)
(
    clean_table.alias("t")
    .merge(clean_booking_values(latest_updates_df, "aggiornamento").alias("s"), MERGE_KEY)
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# COMMAND ----------

# Correzione: la sorgente con una riga per prenotazione
(
    clean_table.alias("t")
    .merge(spark.table(CLEAN_UPDATES_TABLE).alias("s"), MERGE_KEY)
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
print(spark.table(CLEAN_BOOKINGS_TABLE).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Una verifica con gli stessi nomi del report

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE VOLUTO**: la cella seguente deve fallire; la cella *Correzione* sotto deve funzionare.
# MAGIC Risultato atteso – messaggio (riga di riepilogo):
# MAGIC ```
# MAGIC [AMBIGUOUS_REFERENCE] Reference `booking_count` is ambiguous, could be: [`booking_count`, `workspace`.`libro_python`.`g_cancellazioni_aggiornate_destinazione_mese`.`booking_count`]. SQLSTATE: 42704
# MAGIC ```

# COMMAND ----------

# ERRORE VOLUTO – le colonne della verifica hanno gli stessi nomi del report
same_names_df = spark.sql(f"""
SELECT d.destination, month(b.check_in) AS check_in_month, COUNT(*) AS booking_count
FROM {CLEAN_BOOKINGS_TABLE} b
JOIN {PROPERTIES_TABLE} p ON b.property_id = p.property_id
JOIN {DESTINATIONS_TABLE} d ON p.destination_id = d.destination_id
GROUP BY d.destination, month(b.check_in)
""")
same_names_comparison_df = report_table_df.join(same_names_df, on=["destination", "check_in_month"], how="inner")
print(same_names_comparison_df.filter(F.col("booking_count") != F.col("booking_count")).count())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Un append al posto del MERGE

# COMMAND ----------

# MAGIC %md
# MAGIC **ERRORE SILENZIOSO**: la cella seguente funziona ma dà un risultato sbagliato; la cella *Correzione* sotto dà quello giusto.
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_pulite_prenotazione (mode=append)
# MAGIC Righe nella tabella: 22,723
# MAGIC 22723 13590
# MAGIC ```

# COMMAND ----------

# ERRORE SILENZIOSO – gli aggiornamenti aggiunti con append invece che con il MERGE
write_table(clean_updates_df, CLEAN_BOOKINGS_TABLE, mode="append")
appended_df = spark.table(CLEAN_BOOKINGS_TABLE)
print(appended_df.count(), appended_df.select("booking_id").distinct().count())

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output:
# MAGIC ```
# MAGIC Scrittura di workspace.libro_python.s_prenotazioni_pulite_prenotazione (mode=overwrite)
# MAGIC Righe nella tabella: 13,586
# MAGIC +-----------------+----------------+----------------+-----------------+
# MAGIC |num_affected_rows|num_updated_rows|num_deleted_rows|num_inserted_rows|
# MAGIC +-----------------+----------------+----------------+-----------------+
# MAGIC |             9133|            9129|               0|                4|
# MAGIC +-----------------+----------------+----------------+-----------------+
# MAGIC
# MAGIC 13590 13590
# MAGIC ```

# COMMAND ----------

# Correzione: la tabella riscritta dalla fonte, poi il MERGE
write_table(clean_bookings_df, CLEAN_BOOKINGS_TABLE)
spark.sql(merge_query).show()
repaired_df = spark.table(CLEAN_BOOKINGS_TABLE)
print(repaired_df.count(), repaired_df.select("booking_id").distinct().count())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Un errore che il notebook non mostra
