# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 3 – Soluzioni degli esercizi
# MAGIC
# MAGIC Soluzioni commentate degli esercizi di `L03_Esercizi` (anche nell'Appendice A). Si esegue per prima la cella di preparazione, poi una cella alla volta.
# MAGIC Nell'esercizio 8 le celle con gli errori non sono ripetute: qui ci sono solo le correzioni, con il nome dell'errore nel commento.

# COMMAND ----------

# Cella di preparazione: costanti del libro
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Le liste delle strutture guida

# COMMAND ----------

bookings_2024 = [6, 7, 4]
revenues_2024 = [3966.21, 5139.59, 2896.92]

# Prima struttura: indice 0; ultima: indice -1
print(f"Prima: {bookings_2024[0]} - ultima: {bookings_2024[-1]}")

# Conteggio, somma, minimo e massimo
print(f"Strutture: {len(bookings_2024)} - prenotazioni: {sum(bookings_2024)} - minimo: {min(bookings_2024)} - massimo: {max(bookings_2024)}")

# Ricavi: totale, media per struttura (somma / numero di strutture),
# media per prenotazione (somma dei ricavi / somma delle prenotazioni)
total_revenue = sum(revenues_2024)
average_revenue = total_revenue / len(revenues_2024)
revenue_per_booking = total_revenue / sum(bookings_2024)
print(f"Ricavo totale: {total_revenue:.2f}")
print(f"Ricavo medio per struttura: {average_revenue:.2f}")
print(f"Ricavo medio per prenotazione: {revenue_per_booking:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Indici e slicing sui tipi di struttura

# COMMAND ----------

type_names = ["Urban Year-Round", "Summer Getaway", "Historical Place", "Ski Resort"]
type_counts = [9264, 7068, 1646, 185]

print(type_names[0])      # il più frequente: la lista è ordinata dal più frequente
print(type_names[-1])     # il meno frequente: l'ultimo valore
print(type_names[:2])     # i primi due (come LIMIT 2)
print(type_names[-2:])    # gli ultimi due

total_properties = sum(type_counts)
ski_share = type_counts[-1] / total_properties * 100
print(total_properties)
print(f"{type_names[-1]}: {ski_share:.1f}%")

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

# COMMAND ----------

sardinia = {
    "property_id": 16317,
    "title": "Bungalow in Sardinia",
    "destination_id": 4200,
    "property_type": "Summer Getaway",
    "base_price": 213.91,
}
# Nelle f-string le chiavi tra virgolette singole
print(f"{sardinia['title']}: {sardinia['base_price']}")

# La stessa scrittura aggiorna una chiave esistente e ne aggiunge una nuova
sardinia["base_price"] = 219.0
sardinia["bookings_2024"] = 7
print(sardinia["base_price"])

print(sardinia.get("max_guests"))   # chiave assente: None
print("rating" in sardinia)         # in controlla le chiavi
print(len(sardinia))                # 5 chiavi iniziali + bookings_2024

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Stati attivi e valori distinti

# COMMAND ----------

sample_statuses = ["confirmed", "cancelled", "pending", "completed", "cancelled"]
active_statuses = ["confirmed", "completed"]
status_names = ["pending", "confirmed", "cancelled", "completed"]
status_counts = [31575, 17948, 15285, 7439]

# Primo stato: indice 0; terzo stato: indice 2
print(f"{sample_statuses[0]} attivo: {sample_statuses[0] in active_statuses}")
print(f"{sample_statuses[2]} attivo: {sample_statuses[2] in active_statuses}")
print(f"refunded presente: {'refunded' in sample_statuses}")

# Il set toglie le ripetizioni ("cancelled" compare due volte)
print(f"Stati distinti: {len(set(sample_statuses))}")

# confirmed in posizione 1, completed in posizione 3
print(f"Prenotazioni attive: {status_counts[1] + status_counts[3]}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: prenotazioni attive (25387)
# MAGIC SELECT COUNT(*) AS active_bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE status IN ('confirmed', 'completed')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Decodificare le destinazioni

# COMMAND ----------

destination_names = {
    1100: "Amalfi",
    2300: "Florence",
    3900: "Rome",
    4200: "Sardinia",
}
guide_destination_ids = [3900, 4200, 1100]

# Il valore letto dalla lista diventa la chiave del dizionario
print(destination_names[guide_destination_ids[0]])
print(destination_names[guide_destination_ids[1]])
print(destination_names[guide_destination_ids[2]])

# Un codice non presente: get() restituisce None invece di un KeyError
guide_destination_ids.append(9999)
last_id = guide_destination_ids[-1]
last_name = destination_names.get(last_id)
if last_name is None:
    last_name = "n.d."
print(f"{last_id}: {last_name}")

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

# COMMAND ----------

guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]

# Prima la riga (indice), poi la colonna (chiave)
total_bookings = guide_properties[0]["bookings_2024"] + guide_properties[1]["bookings_2024"] + guide_properties[2]["bookings_2024"]
print(f"Prenotazioni totali: {total_bookings}")

sardinia_row = guide_properties[1]
sardinia_rate = sardinia_row["cancelled_2024"] / sardinia_row["bookings_2024"] * 100
print(f"{sardinia_row['title']}: {sardinia_rate:.1f}%")

amalfi_row = guide_properties[2]
amalfi_rate = amalfi_row["cancelled_2024"] / amalfi_row["bookings_2024"] * 100
print(f"{amalfi_row['title']}: {amalfi_rate:.1f}%")

# amalfi_row e guide_properties[2] sono lo stesso dizionario
amalfi_row["is_critical"] = amalfi_rate > CANCELLATION_RATE_THRESHOLD
print(guide_properties[2]["is_critical"])

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

# COMMAND ----------

status_counts_by_name = {
    "pending": 31575,
    "confirmed": 17948,
    "cancelled": 15285,
    "completed": 7439,
}

# Totale: somma dei quattro valori letti per chiave
total_bookings = (
    status_counts_by_name["pending"]
    + status_counts_by_name["confirmed"]
    + status_counts_by_name["cancelled"]
    + status_counts_by_name["completed"]
)
cancellation_rate = status_counts_by_name["cancelled"] / total_bookings * 100
active_share = (status_counts_by_name["confirmed"] + status_counts_by_name["completed"]) / total_bookings * 100

# Classificazione in quattro stati (Capitolo 2): prima il controllo su None
if cancellation_rate is None:
    cancellation_status = "dato mancante"
elif cancellation_rate < 0 or cancellation_rate > 100:
    cancellation_status = "valore impossibile"
elif cancellation_rate > CANCELLATION_RATE_THRESHOLD:
    cancellation_status = "critico"
else:
    cancellation_status = "ok"

# Uno stato che non c'è: get() restituisce None
refunded_count = status_counts_by_name.get("refunded")
if refunded_count is None:
    refunded_text = "n.d."
else:
    refunded_text = str(refunded_count)

print(f"Totale: {total_bookings}")
print(f"Tasso di cancellazione: {cancellation_rate:.1f}% ({cancellation_status})")
print(f"Quota attive: {active_share:.1f}%")
print(f"refunded: {refunded_text}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: tasso di cancellazione complessivo (21.2)
# MAGIC SELECT ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS cancellation_rate
# MAGIC FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori (correzioni)

# COMMAND ----------

# Correzione 8a – IndexError: list index out of range
# La lista ha tre valori: l'ultimo indice è 2, oppure -1
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
print(property_titles[-1])

# COMMAND ----------

# Correzione 8b – KeyError: 'Title'
# Le chiavi distinguono maiuscole e minuscole: la chiave è "title"
sardinia = {"property_id": 16317, "title": "Bungalow in Sardinia", "base_price": 213.91}
print(sardinia["title"])

# COMMAND ----------

# Correzione 8c – TypeError: '>' not supported between instances of 'NoneType' and 'int'
# max() non può confrontare None con un numero: si usano solo i valori presenti
bookings_2024 = [6, None, 4]
print(max([bookings_2024[0], bookings_2024[2]]))

# COMMAND ----------

# Correzione 8d – SyntaxError: invalid syntax. Perhaps you forgot a comma?
# Tra due coppie chiave: valore serve una virgola
destination_names = {1100: "Amalfi", 2300: "Florence"}
print(destination_names)

# COMMAND ----------

# Correzione 8e – errore silenzioso: indici contati da 1 (risultato 8714)
# I due tipi più frequenti sono in posizione 0 e 1
type_counts = [9264, 7068, 1646, 185]
first_two_total = type_counts[0] + type_counts[1]
print(first_two_total)

# COMMAND ----------

# Correzione 8f – errore silenzioso: append() restituisce None (output None)
# append() modifica la lista: si scrive su una riga a sé, senza assegnazione
guide_ids = [11670, 16317]
guide_ids.append(16225)
print(guide_ids)
