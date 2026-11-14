# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 4 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**. Gli esercizi 2, 3, 5 e 7 hanno una verifica `%sql` su `samples.wanderbricks`; l'esercizio 4 su `workspace.libro_python.b_bookings` (creata da `L00_Prepara_Dati`).
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L04_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L04_Esercizi_svolti`). Si esegue per prima la cella di preparazione, poi una cella alla volta (l'esercizio 8 contiene errori voluti).
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso, da confrontare con il proprio output.
# MAGIC Gli esercizi chiedono di usare i cicli anche dove una funzione già pronta (`sum()`, `len()`) darebbe lo stesso risultato: lo scopo è esercitarsi con gli accumulatori.
# MAGIC
# MAGIC | property_id | title | base_price | Prenotazioni 2024 | Cancellate | Ricavo 2024 |
# MAGIC |---|---|---|---|---|---|
# MAGIC | 11670 | Historic Inn in Rome | 284.97 | 6 | 0 | 3966.21 |
# MAGIC | 16317 | Bungalow in Sardinia | 213.91 | 7 | 1 | 5139.59 |
# MAGIC | 16225 | Beach House in Amalfi | 236.95 | 4 | 2 | 2896.92 |

# COMMAND ----------

# Cella di preparazione: costanti e collezioni usate negli esercizi
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
base_prices = [284.97, 213.91, 236.95]
bookings_2024 = [6, 7, 4]

# Le strutture guida come piccola tabella (Capitolo 3)
guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Un ciclo sulle prenotazioni
# MAGIC Con le liste della cella sotto:
# MAGIC 1. con un ciclo, stampare una riga per ogni valore di prenotazioni (`Prenotazioni: 6`);
# MAGIC 2. con un secondo ciclo e tre accumulatori, calcolare il numero di strutture (con un contatore), il totale delle prenotazioni e il ricavo totale;
# MAGIC 3. calcolare il ricavo medio per prenotazione; stampare i risultati con due decimali dove servono.

# COMMAND ----------

bookings_2024 = [6, 7, 4]
revenues_2024 = [3966.21, 5139.59, 2896.92]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Prenotazioni: 6")
print("Prenotazioni: 7")
print("Prenotazioni: 4")
print("Strutture: 3 - prenotazioni: 17")
print("Ricavo totale: 12002.72")
print("Ricavo medio per prenotazione: 706.04")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Notti e posizioni con range()
# MAGIC 1. Stampare con `list()` e `range()` le notti possibili di una prenotazione, da 1 a 9, e il loro numero (`Notti possibili: 9`).
# MAGIC 2. Con un ciclo su `range()` con passo 2, stampare il costo di 1, 3, 5, 7 e 9 notti al prezzo base di Amalfi, 236.95, con due decimali (`notti: 1 - costo: 236.95`).
# MAGIC 3. Con `range(len(property_titles))`, stampare i titoli delle strutture guida numerati da 1 (`1 - Historic Inn in Rome`).

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print([1, 2, 3, 4, 5, 6, 7, 8, 9])
print("Notti possibili: 9")
print("notti: 1 - costo: 236.95")
print("notti: 3 - costo: 710.85")
print("notti: 5 - costo: 1184.75")
print("notti: 7 - costo: 1658.65")
print("notti: 9 - costo: 2132.55")
print("1 - Historic Inn in Rome")
print("2 - Bungalow in Sardinia")
print("3 - Beach House in Amalfi")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: costo di 1, 3, 5, 7, 9 notti al prezzo base di Amalfi
# MAGIC SELECT id AS nights, ROUND(id * 236.95, 2) AS cost
# MAGIC FROM range(1, 10, 2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – I tipi di struttura in un dizionario
# MAGIC Con il dizionario `type_counts_by_name` (cella sotto):
# MAGIC 1. calcolare con `values()` e un accumulatore il numero totale di strutture;
# MAGIC 2. con `items()`, stampare per ogni tipo il conteggio e la quota con un decimale (`Urban Year-Round: 9264 (51.0%)`);
# MAGIC 3. costruire con un ciclo la lista dei tipi con più di 5000 strutture.

# COMMAND ----------

type_counts_by_name = {
    "Urban Year-Round": 9264,
    "Summer Getaway": 7068,
    "Historical Place": 1646,
    "Ski Resort": 185,
}

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Strutture totali: 18163")
print("Urban Year-Round: 9264 (51.0%)")
print("Summer Getaway: 7068 (38.9%)")
print("Historical Place: 1646 (9.1%)")
print("Ski Resort: 185 (1.0%)")
print(['Urban Year-Round', 'Summer Getaway'])

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: strutture e quote per tipo (51.0, 38.9, 9.1, 1.0)
# MAGIC SELECT property_type,
# MAGIC        COUNT(*)                           AS property_count,
# MAGIC        ROUND(COUNT(*) * 100.0 / 18163, 1) AS share
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY property_type
# MAGIC ORDER BY property_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Un campione di importi con anomalie
# MAGIC Con la lista `amounts_sample` (cella sotto) e **un solo ciclo**:
# MAGIC 1. contare gli importi mancanti, gli importi negativi e gli importi validi;
# MAGIC 2. raccogliere gli importi negativi in una lista;
# MAGIC 3. sommare i soli importi validi.
# MAGIC
# MAGIC Dopo il ciclo calcolare la media degli importi validi. Suggerimento: il controllo su `None` va per primo.

# COMMAND ----------

amounts_sample = [512.4, -80.0, None, 1250.75, 333.3, None, -15.5, 968.1]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Mancanti: 2 - negativi: 2 - validi: 4")
print("Importi negativi: [-80.0, -15.5]")
print("Totale validi: 3064.55")
print("Media validi: 766.14")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: la stessa classificazione sull'intera copia didattica b_bookings (30 nulli, 13 negativi)
# MAGIC SELECT COUNT(*) - COUNT(total_amount)                    AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END) AS negative_amounts
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Fasce di prezzo per ogni riga
# MAGIC Con la lista di dizionari `guide_rows` (cella sotto), con un ciclo:
# MAGIC 1. aggiungere a ogni riga la chiave `price_band` (`"alto"` da 250 in su, `"medio"` da 200 in su, `"basso"` sotto 200);
# MAGIC 2. aggiungere a ogni riga la chiave `revenue_per_booking` (ricavo diviso prenotazioni);
# MAGIC 3. stampare una riga per struttura nel formato `Historic Inn in Rome: alto - 661.03 per prenotazione`.
# MAGIC
# MAGIC Costruire infine, con un secondo ciclo, la lista dei titoli in fascia `"medio"`.

# COMMAND ----------

guide_rows = [
    {"title": "Historic Inn in Rome", "base_price": 284.97, "bookings_2024": 6, "revenue_2024": 3966.21},
    {"title": "Bungalow in Sardinia", "base_price": 213.91, "bookings_2024": 7, "revenue_2024": 5139.59},
    {"title": "Beach House in Amalfi", "base_price": 236.95, "bookings_2024": 4, "revenue_2024": 2896.92},
]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Historic Inn in Rome: alto - 661.03 per prenotazione")
print("Bungalow in Sardinia: medio - 734.23 per prenotazione")
print("Beach House in Amalfi: medio - 724.23 per prenotazione")
print(['Bungalow in Sardinia', 'Beach House in Amalfi'])

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: fasce di prezzo delle strutture guida (alto, medio, medio)
# MAGIC SELECT property_id, title, base_price,
# MAGIC        CASE WHEN base_price >= 250 THEN 'alto'
# MAGIC             WHEN base_price >= 200 THEN 'medio'
# MAGIC             ELSE 'basso'
# MAGIC        END AS price_band
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Quanti anni servono?
# MAGIC Il prezzo base della struttura in Sardegna, 213.91, cresce dell'8% all'anno.
# MAGIC 1. Con un ciclo `while`, calcolare dopo quanti anni supera il prezzo base della struttura di Roma, 284.97, e quale prezzo raggiunge.
# MAGIC 2. Ripetere il calcolo con una crescita del 3%.
# MAGIC 3. Riscrivere il primo calcolo con un `for` su `range(1, 21)` e `break`.
# MAGIC
# MAGIC Attenzione: se la cella non termina, fermarla con **Interrupt** e controllare che il blocco aggiorni il prezzo.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("8%: 4 anni - prezzo 291.02")
print("3%: 10 anni - prezzo 287.48")
print("Con for e break: 4 anni - prezzo 291.02")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Contare per categoria
# MAGIC Con la lista `sample_statuses` di dieci stati (cella sotto):
# MAGIC 1. costruire con un ciclo il dizionario `status_counts` con il numero di prenotazioni per stato: si parte da un dizionario vuoto e, per ogni stato, si usa `in` per sapere se è già tra le chiavi (se sì si aumenta il conteggio, altrimenti si aggiunge la chiave con valore 1); stampare il dizionario;
# MAGIC 2. con `items()`, calcolare il totale e il tasso di cancellazione del campione, e classificarlo con `CANCELLATION_RATE_THRESHOLD` (`"critico"` se la supera, altrimenti `"ok"`);
# MAGIC 3. con `range(len(sample_statuses))` e `break`, trovare la posizione della prima prenotazione `"completed"`.

# COMMAND ----------

sample_statuses = ["confirmed", "cancelled", "pending", "pending", "completed", "cancelled", "pending", "confirmed", "cancelled", "pending"]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print({'confirmed': 2, 'cancelled': 3, 'pending': 4, 'completed': 1})
print("Totale: 10")
print("Tasso di cancellazione del campione: 30.0% (ok)")
print("Prima prenotazione completed in posizione: 4")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: lo stesso conteggio per stato, fatto da GROUP BY sull'intera tabella
# MAGIC SELECT status, COUNT(*) AS bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC GROUP BY status
# MAGIC ORDER BY bookings DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare il nome dell'errore (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: i tre titoli; `17`; i tre titoli; `17`; `Cancellate: 2`; gli anni dal 2022 al 2025.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
for title in property_titles
    print(title)

# COMMAND ----------

# Correzione 8a (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8b
total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
        print(total_bookings)

# COMMAND ----------

# Correzione 8b (nome dell'errore: ...; stampare il totale una volta sola, dopo il ciclo)


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
for position in len(property_titles):
    print(property_titles[position])

# COMMAND ----------

# Correzione 8c (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8d
total_bookings = 0
for row in guide_properties:
    total_bookings = total_bookings + row["Bookings_2024"]
print(total_bookings)

# COMMAND ----------

# Correzione 8d (nome dell'errore: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (prenotazioni cancellate del campione)
sample_statuses = ["confirmed", "cancelled", "pending", "completed", "cancelled", "pending"]
for status in sample_statuses:
    cancelled_count = 0
    if status == "cancelled":
        cancelled_count = cancelled_count + 1
print(f"Cancellate: {cancelled_count}")

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (anni dal 2022 al 2025)
for year in range(2022, 2025):
    print(year)

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)

