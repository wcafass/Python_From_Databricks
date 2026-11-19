# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 11 – Soluzioni
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito; il notebook `utils` nella stessa cartella `Libro_Python`. Gli esercizi **scrivono tabelle** nello schema `workspace.libro_python`.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Commenti alle soluzioni: Appendice A.
# MAGIC
# MAGIC Gli esercizi ripercorrono il progetto del capitolo sulle prenotazioni 2024 delle quattro destinazioni italiane (Amalfi, Florence, Rome, Sardinia). Si eseguono per prime la cella con `%run` e la cella di preparazione, poi **una cella alla volta e in ordine**: gli esercizi dal 2 all'8 usano le tabelle scritte negli esercizi precedenti. L'esercizio 8 contiene celle che devono fallire (**ERRORE VOLUTO**) o che producono un risultato sbagliato (**ERRORE SILENZIOSO**); le celle 8e e 8f modificano la tabella pulita italiana, e la correzione della cella 8f la ripara. Non usare Run all.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione
# MAGIC La prima cella contiene solo `%run ./utils`; la seconda definisce le costanti degli esercizi, i DataFrame delle prenotazioni e degli aggiornamenti italiani e le due funzioni del capitolo. Risultato atteso: `Preparazione completata`.

# COMMAND ----------

# MAGIC %run ./utils

# COMMAND ----------

# Cella di preparazione: le tabelle che gli esercizi scrivono
ITALY_CLEAN_TABLE = build_table_name("prenotazioni_pulite_italia", "prenotazione")
ITALY_UPDATES_TABLE = build_table_name("aggiornamenti_puliti_italia", "prenotazione")
ITALY_REPORT_TABLE = build_table_name("cancellazioni_italia", "destinazione_tipo_arrivo", layer="g")
CHECKS_TABLE = build_table_name("controlli_italia", "controllo")

# Strutture italiane con la loro destinazione
properties_df = spark.table(PROPERTIES_TABLE)
destinations_df = spark.table(DESTINATIONS_TABLE)
italy_properties_df = (
    properties_df.select("property_id", "destination_id")
    .join(
        destinations_df.filter(F.col("country") == "Italy").select("destination_id", "destination"),
        on="destination_id",
        how="inner",
    )
    .select("property_id", "destination")
)

# Prenotazioni italiane della copia didattica (tutti gli anni) e aggiornamenti italiani del 2024
italy_bookings_df = spark.table(BOOKINGS_TABLE).join(italy_properties_df.select("property_id"), on="property_id", how="inner")
italy_updates_df = (
    spark.table(BOOKING_UPDATES_TABLE)
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .join(italy_properties_df.select("property_id"), on="property_id", how="inner")
)


# Le due funzioni del Capitolo 11 (sezione 11.4)
def quality_note_column():
    """Nota di qualità di una prenotazione, calcolata sui valori non ancora corretti."""
    return (
        F.when(F.col("total_amount").isNull(), "importo mancante")
        .when(F.col("total_amount") < 0, "importo negativo")
        .when(F.col("check_out") < F.col("check_in"), "date invertite")
        .otherwise("ok")
    )


def clean_booking_values(df, source):
    """Applica le regole di pulizia del progetto a un DataFrame di prenotazioni."""
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


print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Il profilo delle prenotazioni italiane
# MAGIC 1. Da `italy_bookings_df` tenere le prenotazioni con arrivo nel 2024 (`italy_bookings_2024_df`).
# MAGIC 2. Costruire il dizionario `italy_profile` con le voci `righe`, `righe distinte`, `chiavi (booking_id)`, `importo mancante`, `importo negativo`, `date invertite`, e stamparlo con un ciclo su `items()` (formato `{nome:<25}{valore:>8}`).
# MAGIC 3. In un commento: `distinct()` basta per i duplicati?

# COMMAND ----------

# Soluzione
italy_bookings_2024_df = italy_bookings_df.filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)

italy_profile = {
    "righe": italy_bookings_2024_df.count(),
    "righe distinte": italy_bookings_2024_df.distinct().count(),
    "chiavi (booking_id)": italy_bookings_2024_df.select("booking_id").distinct().count(),
    "importo mancante": italy_bookings_2024_df.filter(F.col("total_amount").isNull()).count(),
    "importo negativo": italy_bookings_2024_df.filter(F.col("total_amount") < 0).count(),
    "date invertite": italy_bookings_2024_df.filter(F.col("check_out") < F.col("check_in")).count(),
}

for check_name, value in italy_profile.items():
    print(f"{check_name:<25}{value:>8}")

# Righe distinte (714) = chiavi (714): le 2 righe in più sono copie identiche, distinct() basta.

# COMMAND ----------

# Verifica: risultato atteso
print("righe                         716")
print("righe distinte                714")
print("chiavi (booking_id)           714")
print("importo mancante                0")
print("importo negativo                2")
print("date invertite                  1")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica SQL (atteso: 716 714 0 2 1)
# MAGIC SELECT COUNT(*)                                              AS row_count,
# MAGIC        COUNT(DISTINCT b.booking_id)                          AS key_count,
# MAGIC        SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) AS missing_amount,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)     AS negative_amount,
# MAGIC        SUM(CASE WHEN check_out < check_in THEN 1 ELSE 0 END) AS inverted_dates
# MAGIC FROM workspace.libro_python.b_bookings b
# MAGIC JOIN samples.wanderbricks.properties p USING (property_id)
# MAGIC JOIN samples.wanderbricks.destinations d USING (destination_id)
# MAGIC WHERE year(b.check_in) = 2024 AND d.country = 'Italy'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – La tabella pulita italiana
# MAGIC 1. Preparare `italy_clean_df`: `italy_bookings_df` con `distinct()`, poi `clean_booking_values(..., "originale")`, poi il filtro sull'anno `ANALYSIS_YEAR`.
# MAGIC 2. Scriverlo in `ITALY_CLEAN_TABLE` con `write_table` e mostrare il numero delle righe per `quality_note` (colonna `booking_count`), in ordine di nota.
# MAGIC 3. Con un dizionario di controlli (valore misurato, valore atteso) verificare: righe della tabella = chiavi del profilo; chiavi della tabella = chiavi del profilo; importi negativi = 0; date invertite = 0. Stampare `OK` o `DIVERSO` per ogni controllo.

# COMMAND ----------

# Soluzione
italy_clean_df = (
    clean_booking_values(italy_bookings_df.distinct(), "originale")
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
write_table(italy_clean_df, ITALY_CLEAN_TABLE)
display(
    spark.table(ITALY_CLEAN_TABLE)
    .groupBy("quality_note")
    .agg(F.count("*").alias("booking_count"))
    .orderBy("quality_note")
)

italy_clean_table_df = spark.table(ITALY_CLEAN_TABLE)
italy_clean_checks = {
    "righe": (italy_clean_table_df.count(), italy_profile["chiavi (booking_id)"]),
    "chiavi (booking_id)": (italy_clean_table_df.select("booking_id").distinct().count(), italy_profile["chiavi (booking_id)"]),
    "importo negativo": (italy_clean_table_df.filter(F.col("total_amount") < 0).count(), 0),
    "date invertite": (italy_clean_table_df.filter(F.col("check_out") < F.col("check_in")).count(), 0),
}
for check_name, (value, expected) in italy_clean_checks.items():
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    print(f"{check_name:<25}{value:>8}{expected:>8}  {outcome}")

# COMMAND ----------

# Verifica: risultato atteso
print("Scrittura di workspace.libro_python.s_prenotazioni_pulite_italia_prenotazione (mode=overwrite)")
print("Righe nella tabella: 714")
print("quality_note      booking_count")
print("date invertite    1")
print("importo negativo  2")
print("ok                711")
print("righe                         714     714  OK")
print("chiavi (booking_id)           714     714  OK")
print("importo negativo                0       0  OK")
print("date invertite                  0       0  OK")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Gli aggiornamenti italiani
# MAGIC 1. Stampare righe e prenotazioni distinte di `italy_updates_df`.
# MAGIC 2. Applicare la regola dell'aggiornamento più recente (`italy_latest_updates_df`) e stampare righe e chiavi.
# MAGIC 3. Applicare la regola di spareggio con un join su `["booking_id", "booking_update_id"]` (`italy_chosen_updates_df`) e stampare righe e chiavi.
# MAGIC 4. Pulire il risultato con `clean_booking_values(..., "aggiornamento")` e scriverlo in `ITALY_UPDATES_TABLE` con `write_table`.

# COMMAND ----------

# Soluzione
print(italy_updates_df.count(), italy_updates_df.select("booking_id").distinct().count())

italy_last_update_df = (
    italy_updates_df
    .groupBy("booking_id")
    .agg(F.max("updated_at").alias("last_updated_at"))
)
italy_latest_updates_df = (
    italy_updates_df
    .join(italy_last_update_df, on="booking_id", how="inner")
    .filter(F.col("updated_at") == F.col("last_updated_at"))
)
print(italy_latest_updates_df.count(), italy_latest_updates_df.select("booking_id").distinct().count())

italy_last_update_id_df = (
    italy_latest_updates_df
    .groupBy("booking_id")
    .agg(F.max("booking_update_id").alias("booking_update_id"))
)
italy_chosen_updates_df = italy_latest_updates_df.join(
    italy_last_update_id_df,
    on=["booking_id", "booking_update_id"],
    how="inner",
)
print(italy_chosen_updates_df.count(), italy_chosen_updates_df.select("booking_id").distinct().count())

write_table(clean_booking_values(italy_chosen_updates_df, "aggiornamento"), ITALY_UPDATES_TABLE)

# COMMAND ----------

# Verifica: risultato atteso
print("791 484")
print("485 484")
print("484 484")
print("Scrittura di workspace.libro_python.s_aggiornamenti_puliti_italia_prenotazione (mode=overwrite)")
print("Righe nella tabella: 484")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Il MERGE italiano
# MAGIC 1. Eseguire con `spark.sql()` il `MERGE` di `ITALY_UPDATES_TABLE` in `ITALY_CLEAN_TABLE` (chiave `booking_id`, `UPDATE SET *`, `INSERT *`) e mostrarne i contatori.
# MAGIC 2. Stampare righe e chiavi della tabella pulita italiana.
# MAGIC 3. Stampare le prenotazioni cancellate prima del `MERGE` (dalla ricetta `italy_clean_df` dell'esercizio 2) e dopo (dalla tabella).

# COMMAND ----------

# Soluzione
italy_merge_query = f"""
MERGE INTO {ITALY_CLEAN_TABLE} AS t
USING {ITALY_UPDATES_TABLE} AS s
ON t.booking_id = s.booking_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""
display(spark.sql(italy_merge_query))

italy_merged_df = spark.table(ITALY_CLEAN_TABLE)
print(italy_merged_df.count(), italy_merged_df.select("booking_id").distinct().count())
print(
    italy_clean_df.filter(F.col("status") == "cancelled").count(),
    italy_merged_df.filter(F.col("status") == "cancelled").count(),
)

# COMMAND ----------

# Verifica: risultato atteso
print("num_affected_rows 484, num_updated_rows 484, num_deleted_rows 0, num_inserted_rows 0")
print("714 714")
print("142 270")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Il report per tipo di arrivo
# MAGIC 1. Dalla tabella pulita italiana, con un join su `italy_properties_df`, costruire il report per `destination` e `arrival_type` (`fine settimana` se `F.dayofweek(check_in)` vale 6 o 7, altrimenti `infrasettimanale`) con `booking_count`, `cancelled_count`, `revenue` (arrotondato a 2 decimali), `cancellation_rate` (in %, un decimale) e `cancellation_status` (con `cancellation_status_column()`).
# MAGIC 2. Scriverlo in `ITALY_REPORT_TABLE` con `write_table` e mostrarlo in ordine di destinazione e tipo di arrivo.

# COMMAND ----------

# Soluzione
weekend_arrival = (F.dayofweek(F.col("check_in")) == 6) | (F.dayofweek(F.col("check_in")) == 7)

italy_report_df = (
    spark.table(ITALY_CLEAN_TABLE)
    .select("booking_id", "property_id", "check_in", "status", "total_amount")
    .join(italy_properties_df, on="property_id", how="inner")
    .withColumn("arrival_type", F.when(weekend_arrival, "fine settimana").otherwise("infrasettimanale"))
    .groupBy("destination", "arrival_type")
    .agg(
        F.count("*").alias("booking_count"),
        F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
    )
    .withColumn("cancellation_rate", F.round(F.col("cancelled_count") / F.col("booking_count") * 100, 1))
    .withColumn("cancellation_status", cancellation_status_column())
)
write_table(italy_report_df, ITALY_REPORT_TABLE)
display(spark.table(ITALY_REPORT_TABLE).orderBy("destination", "arrival_type"))

# COMMAND ----------

# Verifica: risultato atteso
print("Scrittura di workspace.libro_python.g_cancellazioni_italia_destinazione_tipo_arrivo (mode=overwrite)")
print("Righe nella tabella: 8")
print("destination  arrival_type      booking_count  cancelled_count  revenue    cancellation_rate  cancellation_status")
print("Amalfi       fine settimana    14             6                7555.12    42.9               non valutabile")
print("Amalfi       infrasettimanale  37             15               21948.84   40.5               critico")
print("Florence     fine settimana    15             4                6880.48    26.7               non valutabile")
print("Florence     infrasettimanale  43             16               26210.82   37.2               critico")
print("Rome         fine settimana    80             30               47311.96   37.5               critico")
print("Rome         infrasettimanale  214            78               122433.9   36.4               critico")
print("Sardinia     fine settimana    105            44               58676.55   41.9               critico")
print("Sardinia     infrasettimanale  206            77               117521.1   37.4               critico")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – La verifica indipendente
# MAGIC 1. Scrivere da zero una query SQL che ricalcoli dalla tabella pulita italiana prenotazioni, cancellate e ricavo per destinazione e tipo di arrivo, con colonne `chk_booking_count`, `chk_cancelled_count`, `chk_revenue`; eseguirla con `spark.sql()`.
# MAGIC 2. Unire il report (riletto dalla tabella) e la verifica con un join su `["destination", "arrival_type"]`, filtrare le righe con almeno una differenza e stampare le righe del report, della verifica, del confronto e delle differenze.

# COMMAND ----------

# Soluzione
italy_check_query = f"""
SELECT d.destination,
       CASE WHEN dayofweek(b.check_in) IN (6, 7) THEN 'fine settimana' ELSE 'infrasettimanale' END AS arrival_type,
       COUNT(*)                                                AS chk_booking_count,
       SUM(CASE WHEN b.status = 'cancelled' THEN 1 ELSE 0 END) AS chk_cancelled_count,
       ROUND(SUM(b.total_amount), 2)                           AS chk_revenue
FROM {ITALY_CLEAN_TABLE} b
JOIN {PROPERTIES_TABLE} p ON b.property_id = p.property_id
JOIN {DESTINATIONS_TABLE} d ON p.destination_id = d.destination_id
GROUP BY d.destination, arrival_type
"""
italy_check_df = spark.sql(italy_check_query)
italy_report_table_df = spark.table(ITALY_REPORT_TABLE)

italy_comparison_df = italy_report_table_df.join(italy_check_df, on=["destination", "arrival_type"], how="inner")
italy_differences_df = italy_comparison_df.filter(
    (F.col("booking_count") != F.col("chk_booking_count"))
    | (F.col("cancelled_count") != F.col("chk_cancelled_count"))
    | (F.col("revenue") != F.col("chk_revenue"))
)
print(italy_report_table_df.count(), italy_check_df.count(), italy_comparison_df.count(), italy_differences_df.count())

# COMMAND ----------

# Verifica: risultato atteso
print("8 8 8 0")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Il registro dei controlli
# MAGIC 1. Raccogliere in un dizionario `italy_final_checks` sei controlli (valore misurato, valore atteso): righe pulite prima del `MERGE` (dalla ricetta `italy_clean_df`) = chiavi del profilo; importi negativi della tabella = 0; date invertite della tabella = 0; righe di `ITALY_UPDATES_TABLE` = chiavi di `italy_updates_df`; righe della tabella dopo il `MERGE` = chiavi del profilo + prenotazioni nuove (le chiavi degli aggiornamenti che non sono tra quelle del profilo: 0); prenotazioni nel report = righe della tabella pulita.
# MAGIC 2. Con un ciclo costruire una lista di dizionari con le chiavi `check_name`, `value`, `expected`, `outcome`, trasformarla in un DataFrame con `spark.createDataFrame()`, riordinare le colonne con `select` e scriverla in `CHECKS_TABLE` con `write_table`.
# MAGIC 3. Mostrare la tabella.

# COMMAND ----------

# Soluzione
italy_update_keys = italy_updates_df.select("booking_id").distinct().count()
italy_new_bookings = (
    italy_updates_df.select("booking_id").distinct()
    .join(
        italy_clean_df.select("booking_id").withColumn("is_known_booking", F.lit(True)),
        on="booking_id",
        how="left",
    )
    .filter(F.col("is_known_booking").isNull())
    .count()
)
italy_merged_df = spark.table(ITALY_CLEAN_TABLE)
italy_final_checks = {
    "righe pulite = chiavi": (italy_clean_df.count(), italy_profile["chiavi (booking_id)"]),
    "importo negativo": (italy_merged_df.filter(F.col("total_amount") < 0).count(), 0),
    "date invertite": (italy_merged_df.filter(F.col("check_out") < F.col("check_in")).count(), 0),
    "righe aggiornamenti": (spark.table(ITALY_UPDATES_TABLE).count(), italy_update_keys),
    "righe dopo il MERGE": (italy_merged_df.count(), italy_profile["chiavi (booking_id)"] + italy_new_bookings),
    "prenotazioni nel report": (
        spark.table(ITALY_REPORT_TABLE).agg(F.sum("booking_count")).collect()[0][0],
        italy_merged_df.count(),
    ),
}

check_rows = []
for check_name, (value, expected) in italy_final_checks.items():
    if value == expected:
        outcome = "OK"
    else:
        outcome = "DIVERSO"
    check_rows.append({"check_name": check_name, "value": value, "expected": expected, "outcome": outcome})

checks_df = spark.createDataFrame(check_rows).select("check_name", "value", "expected", "outcome")
write_table(checks_df, CHECKS_TABLE)
display(spark.table(CHECKS_TABLE))

# COMMAND ----------

# Verifica: risultato atteso
print("Scrittura di workspace.libro_python.s_controlli_italia_controllo (mode=overwrite)")
print("Righe nella tabella: 6")
print("check_name               value  expected  outcome")
print("righe pulite = chiavi    714    714       OK")
print("importo negativo         0      0         OK")
print("date invertite           0      0         OK")
print("righe aggiornamenti      484    484       OK")
print("righe dopo il MERGE      714    714       OK")
print("prenotazioni nel report  714    714       OK")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le celle 8a e 8b producono un errore, le celle da 8c a 8f un **errore silenzioso**. Eseguirle una per una, annotare il tipo dell'errore e il messaggio (o il risultato sbagliato) e scrivere sotto la versione corretta. Le celle 8e e 8f usano o modificano la tabella pulita italiana: la correzione della cella 8f la ripara.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: 8a contatori `484 484 0 0`; 8b `0` differenze; 8c note `date invertite 1`, `importo negativo 2`, `ok 711`; 8d `714`; 8e `0`; 8f `714 714`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (il MERGE con l'aggiornamento più recente)
italy_latest_df = (
    italy_updates_df
    .join(italy_updates_df.groupBy("booking_id").agg(F.max("updated_at").alias("last_updated_at")), on="booking_id", how="inner")
    .filter(F.col("updated_at") == F.col("last_updated_at"))
)
italy_clean_table = DeltaTable.forName(spark, ITALY_CLEAN_TABLE)
(
    italy_clean_table.alias("t")
    .merge(clean_booking_values(italy_latest_df, "aggiornamento").alias("s"), "t.booking_id = s.booking_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# COMMAND ----------

# Correzione 8a – DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE: la sorgente ha 485 righe per 484 prenotazioni
# (un pareggio sull'ultimo aggiornamento). Si usa la sorgente con la regola di spareggio (esercizio 3).
print(italy_latest_df.count(), italy_latest_df.select("booking_id").distinct().count())
display(spark.sql(italy_merge_query))

# COMMAND ----------

# ERRORE VOLUTO – cella 8b (il confronto con la verifica)
italy_check_df = spark.sql(f"""
SELECT destination,
       CASE WHEN dayofweek(check_in) IN (6, 7) THEN 'fine settimana' ELSE 'infrasettimanale' END AS arrival_type,
       COUNT(*) AS booking_count
FROM {ITALY_CLEAN_TABLE} JOIN {PROPERTIES_TABLE} USING (property_id) JOIN {DESTINATIONS_TABLE} USING (destination_id)
GROUP BY destination, arrival_type
""")
italy_comparison_df = spark.table(ITALY_REPORT_TABLE).join(italy_check_df, on=["destination", "arrival_type"], how="inner")
print(italy_comparison_df.filter(F.col("booking_count") != F.col("booking_count")).count())

# COMMAND ----------

# Correzione 8b – AMBIGUOUS_REFERENCE: dopo il join ci sono due colonne booking_count.
# Le colonne della verifica hanno il prefisso chk_.
italy_check_df = spark.sql(f"""
SELECT destination,
       CASE WHEN dayofweek(check_in) IN (6, 7) THEN 'fine settimana' ELSE 'infrasettimanale' END AS arrival_type,
       COUNT(*) AS chk_booking_count
FROM {ITALY_CLEAN_TABLE} JOIN {PROPERTIES_TABLE} USING (property_id) JOIN {DESTINATIONS_TABLE} USING (destination_id)
GROUP BY destination, arrival_type
""")
italy_comparison_df = spark.table(ITALY_REPORT_TABLE).join(italy_check_df, on=["destination", "arrival_type"], how="inner")
print(italy_comparison_df.filter(F.col("booking_count") != F.col("chk_booking_count")).count())

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8c (le note delle prenotazioni italiane)
italy_late_note_df = (
    clean_booking_values(italy_bookings_df.distinct(), "originale")
    .withColumn("quality_note", quality_note_column())
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
display(italy_late_note_df.groupBy("quality_note").agg(F.count("*").alias("booking_count")).orderBy("quality_note"))

# COMMAND ----------

# Correzione 8c – la nota ricalcolata dopo le correzioni vede importi già NULL e date già scambiate
# (importo mancante 2, ok 712). La nota si calcola una volta sola, dentro clean_booking_values.
display(italy_clean_df.groupBy("quality_note").agg(F.count("*").alias("booking_count")).orderBy("quality_note"))

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8d (le prenotazioni italiane con un importo valido)
italy_filtered_df = (
    italy_bookings_df
    .distinct()
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
    .filter(F.col("total_amount") >= 0)
)
print(italy_filtered_df.count())

# COMMAND ----------

# Correzione 8d – il filter toglie le 2 prenotazioni con importo negativo (712 invece di 714).
# Regola guida: l'importo diventa NULL, la prenotazione resta.
print(italy_clean_df.count(), italy_clean_df.filter(F.col("total_amount").isNull()).count())

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (le date scambiate)
italy_dates_inverted = F.col("check_out") < F.col("check_in")
italy_swapped_df = (
    italy_bookings_df
    .distinct()
    .withColumn("check_in", F.when(italy_dates_inverted, F.col("check_out")).otherwise(F.col("check_in")))
    .withColumn("check_out", F.when(italy_dates_inverted, F.col("check_in")).otherwise(F.col("check_out")))
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
print(italy_swapped_df.filter(F.col("check_in") == F.col("check_out")).count())

# COMMAND ----------

# Correzione 8e – il secondo withColumn legge il check_in già modificato: 1 prenotazione con zero notti.
# Lo scambio si fa in un solo select, come in clean_booking_values.
print(italy_clean_df.filter(F.col("check_in") == F.col("check_out")).count())

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (gli aggiornamenti applicati di nuovo)
write_table(spark.table(ITALY_UPDATES_TABLE), ITALY_CLEAN_TABLE, mode="append")
italy_appended_df = spark.table(ITALY_CLEAN_TABLE)
print(italy_appended_df.count(), italy_appended_df.select("booking_id").distinct().count())

# COMMAND ----------

# Correzione 8f – append aggiunge le 484 righe senza guardare la chiave (1198 righe, 714 chiavi).
# Si ripara come si costruisce: overwrite dalla fonte, poi il MERGE.
write_table(italy_clean_df, ITALY_CLEAN_TABLE)
display(spark.sql(italy_merge_query))
italy_repaired_df = spark.table(ITALY_CLEAN_TABLE)
print(italy_repaired_df.count(), italy_repaired_df.select("booking_id").distinct().count())
