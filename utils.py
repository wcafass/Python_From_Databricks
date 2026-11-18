# Databricks notebook source
# MAGIC %md
# MAGIC # utils – definizioni comuni del libro
# MAGIC
# MAGIC Si carica dal Capitolo 10 in poi con una cella che contiene solo `%run ./utils`.
# MAGIC Contiene **solo definizioni** (import, costanti, funzioni): nessuna scrittura su tabelle,
# MAGIC perché `%run` lo esegue tutto ogni volta.
# MAGIC
# MAGIC Prerequisito: aver eseguito una volta `L00_Prepara_Dati`.
# MAGIC Non si modifica per i propri esperimenti: le proprie costanti e funzioni stanno nel notebook che carica utils, dopo la cella `%run`.

# COMMAND ----------

# Import
import pyspark.sql.functions as F
from datetime import date, timedelta, datetime
from delta.tables import DeltaTable

# COMMAND ----------

# Schemi
SOURCE_SCHEMA = "samples.wanderbricks"     # in sola lettura
WORK_SCHEMA = "workspace.libro_python"     # schema di lavoro del lettore

# Tabelle di riferimento: si leggono, non si usano mai in una scrittura
SOURCE_BOOKINGS_TABLE = f"{SOURCE_SCHEMA}.bookings"           # prenotazioni originali
BOOKINGS_TABLE = f"{WORK_SCHEMA}.b_bookings"                  # copia didattica creata da L00_Prepara_Dati
BOOKING_UPDATES_TABLE = f"{SOURCE_SCHEMA}.booking_updates"
PROPERTIES_TABLE = f"{SOURCE_SCHEMA}.properties"
DESTINATIONS_TABLE = f"{SOURCE_SCHEMA}.destinations"
COUNTRIES_TABLE = f"{SOURCE_SCHEMA}.countries"
REVIEWS_TABLE = f"{SOURCE_SCHEMA}.reviews"
SUPPORT_LOGS_TABLE = f"{SOURCE_SCHEMA}.customer_support_logs"

# Parametri di analisi
ANALYSIS_YEAR = 2024                 # finestra degli esempi: check-in nel 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %
MIN_BOOKINGS = 20                    # prenotazioni minime perché un tasso sia valutabile

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
GUIDE_PROPERTY_IDS = [11670, 16317, 16225]

# COMMAND ----------

def build_table_name(topic, granularity, layer="s"):
    """Costruisce il nome completo di una tabella nello schema di lavoro.
    Esempio: build_table_name("prenotazioni", "giornaliere") -> workspace.libro_python.s_prenotazioni_giornaliere
    """
    return f"{WORK_SCHEMA}.{layer}_{topic}_{granularity}"


def read_clean_bookings():
    """Legge b_bookings applicando le regole di pulizia di base:
    - righe ripetute identiche: eliminate con distinct();
    - importo negativo: diventa NULL (la riga resta).
    (Regole da confermare nel Capitolo 11, in particolare per le date invertite.)
    """
    return (
        spark.table(BOOKINGS_TABLE)
        .distinct()
        .withColumn(
            "total_amount",
            F.when(F.col("total_amount") >= 0, F.col("total_amount"))
        )
    )


def cancellation_status_column(threshold=CANCELLATION_RATE_THRESHOLD, min_bookings=MIN_BOOKINGS):
    """Colonna di stato calcolata dalle colonne booking_count e cancellation_rate:
    "non valutabile" con meno di min_bookings prenotazioni,
    "critico" con il tasso sopra la soglia, "ok" altrimenti.
    """
    return (
        F.when(F.col("booking_count") < min_bookings, "non valutabile")
        .when(F.col("cancellation_rate") > threshold, "critico")
        .otherwise("ok")
    )


def write_table(df, table_name, mode="overwrite"):
    """Scrive un DataFrame in una tabella Delta, poi la rilegge e ne stampa le righe."""
    print(f"Scrittura di {table_name} (mode={mode})")
    (
        df.write
        .mode(mode)
        .saveAsTable(table_name)
    )
    print(f"Righe nella tabella: {spark.table(table_name).count():,}")
