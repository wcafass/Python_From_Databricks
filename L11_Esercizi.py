# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 11 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito; il notebook `utils` nella stessa cartella `Libro_Python`. Gli esercizi **scrivono tabelle** nello schema `workspace.libro_python`.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L11_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L11_Esercizi_svolti`) **nella stessa cartella**, perché la prima cella carica `utils` con `%run ./utils`. Ogni esercizio ha una cella di **verifica** con il risultato atteso.
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

# Scrivere qui la soluzione

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

# Scrivere qui la soluzione

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

# Scrivere qui la soluzione

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

# Scrivere qui la soluzione

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

# Scrivere qui la soluzione

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

# Scrivere qui la soluzione

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

# Scrivere qui la soluzione

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

# Correzione 8a (tipo dell'errore o che cosa non va: ...)

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

# Correzione 8b (tipo dell'errore o che cosa non va: ...)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8c (le note delle prenotazioni italiane)
italy_late_note_df = (
    clean_booking_values(italy_bookings_df.distinct(), "originale")
    .withColumn("quality_note", quality_note_column())
    .filter(F.year(F.col("check_in")) == ANALYSIS_YEAR)
)
display(italy_late_note_df.groupBy("quality_note").agg(F.count("*").alias("booking_count")).orderBy("quality_note"))

# COMMAND ----------

# Correzione 8c (tipo dell'errore o che cosa non va: ...)

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

# Correzione 8d (tipo dell'errore o che cosa non va: ...)

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

# Correzione 8e (tipo dell'errore o che cosa non va: ...)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (gli aggiornamenti applicati di nuovo)
write_table(spark.table(ITALY_UPDATES_TABLE), ITALY_CLEAN_TABLE, mode="append")
italy_appended_df = spark.table(ITALY_CLEAN_TABLE)
print(italy_appended_df.count(), italy_appended_df.select("booking_id").distinct().count())

# COMMAND ----------

# Correzione 8f (tipo dell'errore o che cosa non va: ...)