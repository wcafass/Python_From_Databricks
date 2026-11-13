# Databricks notebook source
# MAGIC %md
# MAGIC # L00 – Prepara i dati del libro
# MAGIC
# MAGIC Questo notebook si esegue **una sola volta**, all'inizio, con **Run all**, sul compute Serverless.
# MAGIC
# MAGIC Cosa fa:
# MAGIC 1. Crea lo schema di lavoro `workspace.libro_python`, l'unico in cui scriveremo.
# MAGIC 2. Crea `b_bookings`, la copia didattica di `samples.wanderbricks.bookings`, con gli importi arrotondati a 2 decimali.
# MAGIC 3. Inserisce nella copia alcune anomalie **deterministiche** (identiche per ogni lettore), che servono agli esercizi di pulizia.
# MAGIC 4. Crea `b_bookings_modifiche`, l'elenco delle righe modificate, così è sempre chiaro quali dati sono originali e quali no.
# MAGIC
# MAGIC Le altre tabelle (`properties`, `destinations`, `countries`, `reviews`, `booking_updates`) si leggono direttamente da `samples.wanderbricks`, senza copiarle.
# MAGIC
# MAGIC Se `b_bookings` viene sovrascritta per errore, basta rieseguire questo notebook: il risultato è sempre lo stesso.

# COMMAND ----------

# Cella 1 – setup e schema di lavoro
import pyspark.sql.functions as F

SOURCE_SCHEMA = "samples.wanderbricks"
WORK_SCHEMA = "workspace.libro_python"
BOOKINGS_TABLE = f"{WORK_SCHEMA}.b_bookings"
CHANGES_TABLE = f"{WORK_SCHEMA}.b_bookings_modifiche"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {WORK_SCHEMA}")
print(f"Schema di lavoro pronto: {WORK_SCHEMA}")

# COMMAND ----------

# Cella 2 – copia della tabella originale con importi arrotondati a 2 decimali
# Nell'originale total_amount è un float (es. 879.1500244140625): l'arrotondamento rende leggibili gli output.
source_df = (
    spark.table(f"{SOURCE_SCHEMA}.bookings")
    .withColumn("total_amount", F.round(F.col("total_amount").cast("double"), 2))
)
original_columns = source_df.columns
print(f"Righe originali: {source_df.count():,}")

# COMMAND ----------

# Cella 3 – scelta deterministica delle righe da modificare
# Solo prenotazioni con check-in nel 2024 e importo positivo; gruppi disgiunti (resto diverso della divisione per 13).
def pick_booking_ids(df, remainder, how_many):
    rows = (
        df
        .filter(
            (F.year("check_in") == 2024)
            & (F.col("total_amount") > 0)
            & (F.col("booking_id") % 13 == remainder)
        )
        .orderBy("booking_id")
        .limit(how_many)
        .select("booking_id")
        .collect()
    )
    return [row["booking_id"] for row in rows]

null_amount_ids = pick_booking_ids(source_df, 1, 30)
negative_amount_ids = pick_booking_ids(source_df, 2, 12)
swapped_dates_ids = pick_booking_ids(source_df, 3, 8)
duplicate_ids = pick_booking_ids(source_df, 4, 40)

print(f"Importo nullo:        {len(null_amount_ids)} prenotazioni")
print(f"Importo negativo:     {len(negative_amount_ids)} prenotazioni")
print(f"Date invertite:       {len(swapped_dates_ids)} prenotazioni")
print(f"Righe duplicate:      {len(duplicate_ids)} prenotazioni")

# COMMAND ----------

# Cella 4 – applicazione delle anomalie e scrittura di b_bookings
modified_df = (
    source_df
    .withColumn(
        "total_amount",
        F.when(F.col("booking_id").isin(null_amount_ids), F.lit(None).cast("double"))
        .when(F.col("booking_id").isin(negative_amount_ids), -F.col("total_amount"))
        .otherwise(F.col("total_amount"))
    )
    .withColumn(
        "new_check_in",
        F.when(F.col("booking_id").isin(swapped_dates_ids), F.col("check_out")).otherwise(F.col("check_in"))
    )
    .withColumn(
        "new_check_out",
        F.when(F.col("booking_id").isin(swapped_dates_ids), F.col("check_in")).otherwise(F.col("check_out"))
    )
    .drop("check_in", "check_out")
    .withColumnRenamed("new_check_in", "check_in")
    .withColumnRenamed("new_check_out", "check_out")
    .select(original_columns)
)

# Le righe duplicate sono copie identiche di righe non modificate
duplicates_df = modified_df.filter(F.col("booking_id").isin(duplicate_ids))
bookings_df = modified_df.unionByName(duplicates_df)

print(f"Scrittura di {BOOKINGS_TABLE}")
(
    bookings_df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(BOOKINGS_TABLE)
)
print(f"Righe scritte: {spark.table(BOOKINGS_TABLE).count():,}")

# COMMAND ----------

# Cella 5 – elenco delle modifiche (b_bookings_modifiche)
changes = (
    [(booking_id, "importo_nullo", "total_amount impostato a NULL") for booking_id in null_amount_ids]
    + [(booking_id, "importo_negativo", "total_amount cambiato di segno") for booking_id in negative_amount_ids]
    + [(booking_id, "date_invertite", "check_in e check_out scambiati") for booking_id in swapped_dates_ids]
    + [(booking_id, "riga_duplicata", "riga copiata due volte, identica") for booking_id in duplicate_ids]
)
changes_df = spark.createDataFrame(changes, "booking_id bigint, change_type string, description string")

print(f"Scrittura di {CHANGES_TABLE}")
(
    changes_df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(CHANGES_TABLE)
)
print(f"Righe scritte: {spark.table(CHANGES_TABLE).count():,}")

# COMMAND ----------

# Cella 6 – verifica finale: i valori ottenuti devono coincidere con quelli attesi
check_df = spark.table(BOOKINGS_TABLE)

checks = {
    "righe":                         (check_df.count(), 72287),
    "righe distinte":                (check_df.distinct().count(), 72247),
    "booking_id distinti":           (check_df.select("booking_id").distinct().count(), 72247),
    "total_amount nullo":            (check_df.filter(F.col("total_amount").isNull()).count(), 30),
    "total_amount negativo":         (check_df.filter(F.col("total_amount") < 0).count(), 13),
    "check_out prima del check_in":  (check_df.filter(F.col("check_out") < F.col("check_in")).count(), 8),
    "modifiche registrate":          (spark.table(CHANGES_TABLE).count(), 90),
}

all_ok = True
for name, (value, expected) in checks.items():
    status = "OK" if value == expected else "DIVERSO"
    if value != expected:
        all_ok = False
    print(f"{name:<30} {value:>8,}   atteso {expected:>8,}   {status}")

print()
print("Preparazione completata." if all_ok else "ATTENZIONE: alcuni valori sono diversi da quelli attesi.")
# Nota: dei 13 importi negativi, 1 è già presente nei dati originali e 12 sono aggiunti da questo notebook.
