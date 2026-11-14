# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 4 – Soluzioni degli esercizi
# MAGIC
# MAGIC Soluzioni commentate degli esercizi di `L04_Esercizi` (anche nell'Appendice A). Si esegue per prima la cella di preparazione, poi una cella alla volta.
# MAGIC Nell'esercizio 8 le celle con gli errori non sono ripetute: qui ci sono solo le correzioni, con il nome dell'errore nel commento.

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

# COMMAND ----------

bookings_2024 = [6, 7, 4]
revenues_2024 = [3966.21, 5139.59, 2896.92]

# 1. Un giro per ogni valore della lista
for bookings in bookings_2024:
    print(f"Prenotazioni: {bookings}")

# 2. Prima del ciclo: gli accumulatori partono da zero
property_count = 0
total_bookings = 0
for bookings in bookings_2024:
    # Dentro il ciclo: un contatore e un totale
    property_count = property_count + 1
    total_bookings = total_bookings + bookings

total_revenue = 0
for revenue in revenues_2024:
    total_revenue = total_revenue + revenue

# 3. Dopo i cicli: si usano i risultati (i decimali sempre formattati)
revenue_per_booking = total_revenue / total_bookings
print(f"Strutture: {property_count} - prenotazioni: {total_bookings}")
print(f"Ricavo totale: {total_revenue:.2f}")
print(f"Ricavo medio per prenotazione: {revenue_per_booking:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Notti e posizioni con range()

# COMMAND ----------

# 1. range(1, 10): da 1 a 9, la fine è esclusa
possible_nights = list(range(1, 10))
print(possible_nights)
print(f"Notti possibili: {len(possible_nights)}")

# 2. Passo 2: 1, 3, 5, 7, 9
amalfi_price = 236.95
for nights in range(1, 10, 2):
    cost = amalfi_price * nights
    print(f"notti: {nights} - costo: {cost:.2f}")

# 3. Le posizioni partono da 0: per numerare da 1 si stampa position + 1
for position in range(len(property_titles)):
    print(f"{position + 1} - {property_titles[position]}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: costo di 1, 3, 5, 7, 9 notti al prezzo base di Amalfi
# MAGIC SELECT id AS nights, ROUND(id * 236.95, 2) AS cost
# MAGIC FROM range(1, 10, 2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – I tipi di struttura in un dizionario

# COMMAND ----------

type_counts_by_name = {
    "Urban Year-Round": 9264,
    "Summer Getaway": 7068,
    "Historical Place": 1646,
    "Ski Resort": 185,
}

# 1. values(): bastano i conteggi
total_properties = 0
for count in type_counts_by_name.values():
    total_properties = total_properties + count
print(f"Strutture totali: {total_properties}")

# 2. items(): chiave e valore in due variabili del ciclo
for property_type, count in type_counts_by_name.items():
    share = count / total_properties * 100
    print(f"{property_type}: {count} ({share:.1f}%)")

# 3. Un filtro dentro il ciclo: solo i tipi con più di 5000 strutture
large_types = []
for property_type, count in type_counts_by_name.items():
    if count > 5000:
        large_types.append(property_type)
print(large_types)

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

# COMMAND ----------

amounts_sample = [512.4, -80.0, None, 1250.75, 333.3, None, -15.5, 968.1]

missing_count = 0
negative_count = 0
valid_count = 0
valid_total = 0
negative_amounts = []
for amount in amounts_sample:
    # Prima il controllo su None: un confronto None < 0 produrrebbe TypeError
    if amount is None:
        missing_count = missing_count + 1
    elif amount < 0:
        negative_count = negative_count + 1
        negative_amounts.append(amount)
    else:
        valid_count = valid_count + 1
        valid_total = valid_total + amount

# La media si divide per il numero di importi validi, non per la lunghezza della lista
valid_average = valid_total / valid_count
print(f"Mancanti: {missing_count} - negativi: {negative_count} - validi: {valid_count}")
print(f"Importi negativi: {negative_amounts}")
print(f"Totale validi: {valid_total:.2f}")
print(f"Media validi: {valid_average:.2f}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: la stessa classificazione sull'intera copia didattica b_bookings (30 nulli, 13 negativi)
# MAGIC SELECT COUNT(*) - COUNT(total_amount)                    AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END) AS negative_amounts
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Fasce di prezzo per ogni riga

# COMMAND ----------

guide_rows = [
    {"title": "Historic Inn in Rome", "base_price": 284.97, "bookings_2024": 6, "revenue_2024": 3966.21},
    {"title": "Bungalow in Sardinia", "base_price": 213.91, "bookings_2024": 7, "revenue_2024": 5139.59},
    {"title": "Beach House in Amalfi", "base_price": 236.95, "bookings_2024": 4, "revenue_2024": 2896.92},
]

# Due nuove colonne per ogni riga: la classificazione (come CASE WHEN) e un calcolo
for row in guide_rows:
    if row["base_price"] >= 250:
        row["price_band"] = "alto"
    elif row["base_price"] >= 200:
        row["price_band"] = "medio"
    else:
        row["price_band"] = "basso"
    row["revenue_per_booking"] = row["revenue_2024"] / row["bookings_2024"]
    print(f"{row['title']}: {row['price_band']} - {row['revenue_per_booking']:.2f} per prenotazione")

# Un secondo ciclo filtra le righe con la nuova colonna
medium_titles = []
for row in guide_rows:
    if row["price_band"] == "medio":
        medium_titles.append(row["title"])
print(medium_titles)

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

# COMMAND ----------

ROME_PRICE = 284.97

# 1. while: si ripete finché il prezzo non supera quello di Roma
projected_price = 213.91
years = 0
while projected_price <= ROME_PRICE:
    projected_price = projected_price * 1.08   # il blocco aggiorna la variabile della condizione
    years = years + 1
print(f"8%: {years} anni - prezzo {projected_price:.2f}")

# 2. Lo stesso calcolo con una crescita del 3%
projected_price = 213.91
years = 0
while projected_price <= ROME_PRICE:
    projected_price = projected_price * 1.03
    years = years + 1
print(f"3%: {years} anni - prezzo {projected_price:.2f}")

# 3. for con un numero massimo di giri e break: non può girare all'infinito
projected_price = 213.91
for year in range(1, 21):
    projected_price = projected_price * 1.08
    if projected_price > ROME_PRICE:
        break
print(f"Con for e break: {year} anni - prezzo {projected_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Contare per categoria

# COMMAND ----------

sample_statuses = ["confirmed", "cancelled", "pending", "pending", "completed", "cancelled", "pending", "confirmed", "cancelled", "pending"]

# 1. Un dizionario come accumulatore: stato -> conteggio
status_counts = {}
for status in sample_statuses:
    if status in status_counts:
        status_counts[status] = status_counts[status] + 1   # stato già visto: si aumenta
    else:
        status_counts[status] = 1                           # primo incontro: nuova chiave
print(status_counts)

# 2. Totale con items() e tasso di cancellazione del campione
total_count = 0
for status, count in status_counts.items():
    total_count = total_count + count
cancellation_rate = status_counts["cancelled"] / total_count * 100

# 30.0 non è maggiore di 30.0: la soglia si supera solo con un valore più alto
if cancellation_rate > CANCELLATION_RATE_THRESHOLD:
    cancellation_status = "critico"
else:
    cancellation_status = "ok"
print(f"Totale: {total_count}")
print(f"Tasso di cancellazione del campione: {cancellation_rate:.1f}% ({cancellation_status})")

# 3. La posizione della prima prenotazione completed: ci si ferma al primo risultato
for position in range(len(sample_statuses)):
    if sample_statuses[position] == "completed":
        break
print(f"Prima prenotazione completed in posizione: {position}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: lo stesso conteggio per stato, fatto da GROUP BY sull'intera tabella
# MAGIC SELECT status, COUNT(*) AS bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC GROUP BY status
# MAGIC ORDER BY bookings DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori (correzioni)

# COMMAND ----------

# Correzione 8a – SyntaxError: expected ':'
# La riga del for termina con i due punti
for title in property_titles:
    print(title)

# COMMAND ----------

# Correzione 8b – IndentationError: unexpected indent
# La print era rientrata più del blocco: il totale si stampa una volta, dopo il ciclo
total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
print(total_bookings)

# COMMAND ----------

# Correzione 8c – TypeError: 'int' object is not iterable
# len() restituisce un numero: le posizioni si scorrono con range(len(...))
for position in range(len(property_titles)):
    print(property_titles[position])

# COMMAND ----------

# Correzione 8d – KeyError: 'Bookings_2024'
# Le chiavi distinguono maiuscole e minuscole: la chiave è "bookings_2024"
total_bookings = 0
for row in guide_properties:
    total_bookings = total_bookings + row["bookings_2024"]
print(total_bookings)

# COMMAND ----------

# Correzione 8e – errore silenzioso: contatore azzerato a ogni giro (Cancellate: 0)
# Il contatore si prepara una volta, prima del ciclo
sample_statuses = ["confirmed", "cancelled", "pending", "completed", "cancelled", "pending"]
cancelled_count = 0
for status in sample_statuses:
    if status == "cancelled":
        cancelled_count = cancelled_count + 1
print(f"Cancellate: {cancelled_count}")

# COMMAND ----------

# Correzione 8f – errore silenzioso: la fine di range() è esclusa (manca il 2025)
for year in range(2022, 2026):
    print(year)
