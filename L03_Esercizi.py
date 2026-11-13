# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 3 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**. Gli esercizi 2, 4, 5, 6 e 7 hanno una verifica `%sql` su `samples.wanderbricks`.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L03_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L03_Esercizi_svolti`). Si esegue per prima la cella di preparazione, poi una cella alla volta (l'esercizio 8 contiene errori voluti).
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso, da confrontare con il proprio output.
# MAGIC
# MAGIC | property_id | title | destination_id | property_type | base_price | Prenotazioni 2024 | Cancellate | Ricavo 2024 |
# MAGIC |---|---|---|---|---|---|---|---|
# MAGIC | 11670 | Historic Inn in Rome | 3900 | Historical Place | 284.97 | 6 | 0 | 3966.21 |
# MAGIC | 16317 | Bungalow in Sardinia | 4200 | Summer Getaway | 213.91 | 7 | 1 | 5139.59 |
# MAGIC | 16225 | Beach House in Amalfi | 1100 | Summer Getaway | 236.95 | 4 | 2 | 2896.92 |

# COMMAND ----------

# Cella di preparazione: costanti del libro
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Le liste delle strutture guida
# MAGIC Creare le liste `bookings_2024 = [6, 7, 4]` e `revenues_2024 = [3966.21, 5139.59, 2896.92]` (Roma, Sardegna, Amalfi). Stampare:
# MAGIC 1. con gli indici, le prenotazioni della prima e dell'ultima struttura;
# MAGIC 2. con `len()`, `sum()`, `min()`, `max()`, il numero di strutture, il totale e gli estremi delle prenotazioni;
# MAGIC 3. il ricavo totale, il ricavo medio per struttura e il ricavo medio per prenotazione, con due decimali.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Prima: 6 - ultima: 4")
print("Strutture: 3 - prenotazioni: 17 - minimo: 4 - massimo: 7")
print("Ricavo totale: 12002.72")
print("Ricavo medio per struttura: 4000.91")
print("Ricavo medio per prenotazione: 706.04")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Indici e slicing sui tipi di struttura
# MAGIC I quattro tipi di struttura di `properties`, dal più frequente al meno frequente: `"Urban Year-Round"` (9264), `"Summer Getaway"` (7068), `"Historical Place"` (1646), `"Ski Resort"` (185).
# MAGIC Creare le liste `type_names` e `type_counts` e stampare: il tipo più frequente; il meno frequente (con un indice negativo); i due più frequenti e i due meno frequenti (con lo slicing); il numero totale di strutture; la quota di `"Ski Resort"` con un decimale.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Urban Year-Round")
print("Ski Resort")
print(['Urban Year-Round', 'Summer Getaway'])
print(['Historical Place', 'Ski Resort'])
print(18163)
print("Ski Resort: 1.0%")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: strutture per tipo (9264, 7068, 1646, 185)
# MAGIC SELECT property_type, COUNT(*) AS property_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY property_type
# MAGIC ORDER BY property_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Il dizionario di una struttura
# MAGIC Creare il dizionario `sardinia` con le chiavi `property_id` (16317), `title` (`"Bungalow in Sardinia"`), `destination_id` (4200), `property_type` (`"Summer Getaway"`), `base_price` (213.91).
# MAGIC 1. Stampare titolo e prezzo in una f-string (`Bungalow in Sardinia: 213.91`).
# MAGIC 2. Aggiornare il prezzo a 219.0, aggiungere la chiave `bookings_2024` con valore 7 e stampare il nuovo prezzo.
# MAGIC 3. Stampare il risultato di `get("max_guests")`, il controllo `"rating" in sardinia` e il numero di coppie.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Bungalow in Sardinia: 213.91")
print(219.0)
print(None)
print(False)
print(6)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Stati attivi e valori distinti
# MAGIC Date le liste qui sotto:
# MAGIC 1. controllare con `in` se il primo e il terzo stato del campione sono attivi;
# MAGIC 2. controllare se `"refunded"` compare nel campione;
# MAGIC 3. calcolare il numero di stati distinti del campione con un set;
# MAGIC 4. calcolare dalla lista `status_counts` il numero di prenotazioni attive (`confirmed` e `completed`) e confrontarlo con la verifica `%sql`.

# COMMAND ----------

sample_statuses = ["confirmed", "cancelled", "pending", "completed", "cancelled"]
active_statuses = ["confirmed", "completed"]
status_names = ["pending", "confirmed", "cancelled", "completed"]
status_counts = [31575, 17948, 15285, 7439]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("confirmed attivo: True")
print("pending attivo: False")
print("refunded presente: False")
print("Stati distinti: 4")
print("Prenotazioni attive: 25387")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: prenotazioni attive (25387)
# MAGIC SELECT COUNT(*) AS active_bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE status IN ('confirmed', 'completed')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Decodificare le destinazioni
# MAGIC 1. Con `destination_names` e `guide_destination_ids` (cella sotto) stampare il nome della destinazione di ciascuna struttura guida, usando gli indici della lista come chiavi del dizionario.
# MAGIC 2. Aggiungere il codice 9999 in fondo alla lista con `append()` e stampare la sua decodifica con `get()`, scrivendo `n.d.` quando la destinazione non è nota (formato `9999: n.d.`).

# COMMAND ----------

destination_names = {
    1100: "Amalfi",
    2300: "Florence",
    3900: "Rome",
    4200: "Sardinia",
}
guide_destination_ids = [3900, 4200, 1100]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Rome")
print("Sardinia")
print("Amalfi")
print("9999: n.d.")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: le destinazioni italiane
# MAGIC SELECT destination_id, destination
# MAGIC FROM samples.wanderbricks.destinations
# MAGIC WHERE country = 'Italy'
# MAGIC ORDER BY destination_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Una piccola tabella
# MAGIC Con la lista di dizionari `guide_properties` (cella sotto) e il doppio accesso riga → chiave:
# MAGIC 1. calcolare il totale delle prenotazioni sommando i tre valori;
# MAGIC 2. calcolare e stampare il tasso di cancellazione della Sardegna e di Amalfi, con un decimale (`Bungalow in Sardinia: 14.3%`);
# MAGIC 3. aggiungere alla riga di Amalfi la chiave `is_critical` con il risultato del confronto tra il suo tasso e `CANCELLATION_RATE_THRESHOLD`, e stamparla.

# COMMAND ----------

guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Prenotazioni totali: 17")
print("Bungalow in Sardinia: 14.3%")
print("Beach House in Amalfi: 50.0%")
print(True)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: le tre righe ricalcolate dalla tabella bookings
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                              AS bookings_2024,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_2024,
# MAGIC        ROUND(SUM(total_amount), 2)                           AS revenue_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Il tasso di cancellazione complessivo
# MAGIC 1. Creare il dizionario `status_counts_by_name` con i quattro stati come chiavi e i conteggi come valori (pending 31575, confirmed 17948, cancelled 15285, completed 7439).
# MAGIC 2. Leggendo i valori per chiave, calcolare il totale delle prenotazioni, il tasso di cancellazione complessivo e la quota di prenotazioni attive (`confirmed` e `completed`), con un decimale.
# MAGIC 3. Leggere lo stato `"refunded"` con `get()`, stampando `n.d.` se manca.
# MAGIC 4. Classificare il tasso complessivo con i quattro stati del Capitolo 2 (`"dato mancante"`, `"valore impossibile"`, `"critico"`, `"ok"`) e confrontarlo con la verifica `%sql`.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Totale: 72247")
print("Tasso di cancellazione: 21.2% (ok)")
print("Quota attive: 35.1%")
print("refunded: n.d.")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: tasso di cancellazione complessivo (21.2)
# MAGIC SELECT ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS cancellation_rate
# MAGIC FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare il nome dell'errore (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `Beach House in Amalfi`, `Bungalow in Sardinia`, `6`, `{1100: 'Amalfi', 2300: 'Florence'}`, `16332`, `[11670, 16317, 16225]`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
print(property_titles[3])

# COMMAND ----------

# Correzione 8a (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8b
sardinia = {"property_id": 16317, "title": "Bungalow in Sardinia", "base_price": 213.91}
print(sardinia["Title"])

# COMMAND ----------

# Correzione 8b (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
bookings_2024 = [6, None, 4]
print(max(bookings_2024))

# COMMAND ----------

# Correzione 8c (nome dell'errore: ...; stampare il massimo dei soli valori presenti, letti con gli indici)


# COMMAND ----------

# ERRORE VOLUTO – cella 8d
destination_names = {1100: "Amalfi" 2300: "Florence"}

# COMMAND ----------

# Correzione 8d (nome dell'errore: ...; stampare il dizionario corretto)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (totale dei due tipi più frequenti)
type_counts = [9264, 7068, 1646, 185]
first_two_total = type_counts[1] + type_counts[2]
print(first_two_total)

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f
guide_ids = [11670, 16317]
guide_ids = guide_ids.append(16225)
print(guide_ids)

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)

