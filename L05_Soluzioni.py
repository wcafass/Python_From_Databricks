# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 5 – Soluzioni degli esercizi
# MAGIC
# MAGIC Soluzioni commentate degli esercizi del Capitolo 5 (le stesse dell'Appendice A).
# MAGIC Prerequisiti: notebook collegato a **Serverless**; l'esercizio 7 ha una verifica su `workspace.libro_python.b_bookings` (creata da `L00_Prepara_Dati`).
# MAGIC Si esegue per prima la cella di preparazione, poi una cella alla volta.

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
# MAGIC ## Esercizio 1 ★ – Una scheda per struttura
# MAGIC La funzione stampa e non ha `return`: il risultato della chiamata è `None`.

# COMMAND ----------

def print_property_card(title, destination, base_price):
    print(title)
    print(f"  Destinazione: {destination}")
    print(f"  Prezzo base: {base_price}")

print_property_card("Historic Inn in Rome", "Rome", 284.97)
print_property_card("Beach House in Amalfi", "Amalfi", 236.95)

# La chiamata stampa la scheda; il valore restituito è None, perché la funzione non ha return
card_result = print_property_card("Bungalow in Sardinia", "Sardinia", 213.91)
print(card_result)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Il costo di un soggiorno
# MAGIC La funzione restituisce il costo: si può usare in una list comprehension e in un calcolo.

# COMMAND ----------

def stay_cost(price, nights):
    return round(price * nights, 2)

# Costo di 3 notti per ogni prezzo base
three_night_costs = [stay_cost(price, 3) for price in base_prices]
print(three_night_costs)

# Totale dei tre soggiorni: un accumulatore, mostrato con due decimali
total_cost = 0
for cost in three_night_costs:
    total_cost = total_cost + cost
print(f"Totale: {total_cost:.2f}")

print(f"Amalfi, 7 notti: {stay_cost(236.95, 7)}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: costo di 3 notti per le strutture guida (854.91, 710.85, 641.73)
# MAGIC SELECT property_id, base_price, ROUND(base_price * 3, 2) AS three_night_cost
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Da print a return
# MAGIC `show_average` stampa e restituisce `None`; `calculate_mean` restituisce la media, che si può usare nei confronti.

# COMMAND ----------

def show_average(values):
    print(sum(values) / len(values))

def calculate_mean(values):
    return sum(values) / len(values)

mean_price = calculate_mean(base_prices)
print(f"Prezzo base medio: {mean_price:.2f}")

# Contatore con condizione: il valore restituito si confronta con ogni prezzo
above_mean_count = 0
for price in base_prices:
    if price > mean_price:
        above_mean_count = above_mean_count + 1
print(f"Prezzi sopra la media: {above_mean_count}")

print(f"Prenotazioni medie: {calculate_mean(bookings_2024):.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Fasce di prezzo con una funzione
# MAGIC Un `return` in ogni ramo, con il controllo su `None` per primo; il conteggio per fascia usa un dizionario come nell'esercizio 7 del Capitolo 4.

# COMMAND ----------

def classify_price(price):
    if price is None:
        return "dato mancante"
    if price >= 250:
        return "alto"
    if price >= 200:
        return "medio"
    return "basso"

sample_prices = [284.97, 213.91, 236.95, 189.0, None, 312.5]

band_counts = {}
for price in sample_prices:
    band = classify_price(price)
    print(f"{price}: {band}")
    if band in band_counts:
        band_counts[band] = band_counts[band] + 1
    else:
        band_counts[band] = 1
print(band_counts)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: fasce di prezzo delle strutture guida (alto, medio, medio)
# MAGIC SELECT property_id, base_price,
# MAGIC        CASE WHEN base_price >= 250 THEN 'alto'
# MAGIC             WHEN base_price >= 200 THEN 'medio'
# MAGIC             ELSE 'basso'
# MAGIC        END AS price_band
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Una soglia diversa
# MAGIC La soglia è un parametro con default: senza argomento vale la soglia del libro, per nome si sceglie un altro valore.

# COMMAND ----------

def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

def classify_cancellation_rate(rate, threshold=CANCELLATION_RATE_THRESHOLD):
    if rate is None:
        return "dato mancante"
    if rate < 0 or rate > 100:
        return "valore impossibile"
    if rate > threshold:
        return "critico"
    return "ok"

critical_default = 0
critical_low = 0
for row in guide_properties:
    rate = cancellation_rate(row["cancelled_2024"], row["bookings_2024"])
    status_default = classify_cancellation_rate(rate)
    status_low = classify_cancellation_rate(rate, threshold=10.0)
    print(f"{row['title']}: {rate:.1f}% - soglia 30: {status_default} - soglia 10: {status_low}")
    if status_default == "critico":
        critical_default = critical_default + 1
    if status_low == "critico":
        critical_low = critical_low + 1
print(f"Critiche con soglia 30: {critical_default} - con soglia 10: {critical_low}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: stati con soglia 30 e soglia 10 (11670 ok/ok; 16225 critico/critico; 16317 ok/critico)
# MAGIC SELECT property_id,
# MAGIC        ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS cancellation_rate,
# MAGIC        CASE WHEN SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) > 30
# MAGIC             THEN 'critico' ELSE 'ok' END AS status_30,
# MAGIC        CASE WHEN SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) > 10
# MAGIC             THEN 'critico' ELSE 'ok' END AS status_10
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Quanti anni servono?
# MAGIC Qui il `return` dentro il ciclo è voluto: sta nel ramo dell'`if` e termina la funzione al primo anno in cui l'obiettivo è superato. Il `return None` finale si raggiunge solo se il ciclo finisce senza superarlo.

# COMMAND ----------

def years_to_reach(price, target, growth_rate=0.05):
    if price > target:
        return 0
    projected_price = price
    for year in range(1, 51):
        projected_price = projected_price * (1 + growth_rate)
        if projected_price > target:
            return year
    return None

print(f"Amalfi, 300 al 5%: {years_to_reach(236.95, 300)} anni")
print(f"Sardegna, 284.97 all'8%: {years_to_reach(213.91, 284.97, growth_rate=0.08)} anni")
print(f"Sardegna, 284.97 al 3%: {years_to_reach(213.91, 284.97, growth_rate=0.03)} anni")
print(f"Roma, 250: {years_to_reach(284.97, 250)} anni")
print(f"Amalfi, 300 allo 0%: {years_to_reach(236.95, 300, growth_rate=0.0)}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Un riepilogo degli importi
# MAGIC Due funzioni: `is_valid_amount` decide se un importo è valido, `summarize_amounts` la usa nel ciclo e restituisce un dizionario.

# COMMAND ----------

def is_valid_amount(amount):
    """Restituisce True se l'importo è presente e non negativo."""
    return amount is not None and amount >= 0

def summarize_amounts(amounts):
    """Conta mancanti, negativi e validi; somma e media dei soli importi validi.

    Restituisce un dizionario; la media è None se non ci sono importi validi.
    """
    missing = 0
    negative = 0
    valid = 0
    total = 0
    for amount in amounts:
        if amount is None:
            missing = missing + 1
        elif not is_valid_amount(amount):
            negative = negative + 1
        else:
            valid = valid + 1
            total = total + amount
    if valid == 0:
        average = None
    else:
        average = total / valid
    return {"missing": missing, "negative": negative, "valid": valid, "total": total, "average": average}

amounts_sample = [512.4, -80.0, None, 1250.75, 333.3, None, -15.5, 968.1]
summary = summarize_amounts(amounts_sample)
print(f"Mancanti: {summary['missing']} - negativi: {summary['negative']} - validi: {summary['valid']}")
print(f"Totale validi: {summary['total']:.2f} - media: {summary['average']:.2f}")

second_summary = summarize_amounts([None, -10.0])
print(f"Secondo campione: validi {second_summary['valid']} - totale {second_summary['total']} - media {second_summary['average']}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: nulli e negativi dell'intera copia didattica b_bookings (30 e 13)
# MAGIC SELECT COUNT(*) - COUNT(total_amount)                    AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END) AS negative_amounts
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Per ogni cella: il nome dell'errore (o il risultato sbagliato) e la versione corretta.

# COMMAND ----------

# Correzione 8a – SyntaxError: expected ':' (mancano i due punti dopo la riga di definizione)
def stay_cost(price, nights):
    return round(price * nights, 2)

print(stay_cost(236.95, 7))

# COMMAND ----------

# Correzione 8b – TypeError: stay_cost() missing 1 required positional argument: 'nights'
def stay_cost(price, nights):
    return round(price * nights, 2)

print(stay_cost(236.95, 7))

# COMMAND ----------

# Correzione 8c – SyntaxError: parameter without a default follows parameter with a default
# Il parametro con default va dopo quello senza default
def stay_cost(nights, price=236.95):
    return round(price * nights, 2)

print(stay_cost(7))

# COMMAND ----------

# Correzione 8d – NameError: name 'revenue_sum' is not defined
# revenue_sum è una variabile locale: il risultato si ottiene dal valore restituito
def total_revenue(revenues):
    revenue_sum = 0
    for revenue in revenues:
        revenue_sum = revenue_sum + revenue
    return revenue_sum

revenue_2024 = total_revenue([3966.21, 5139.59, 2896.92])
print(f"{revenue_2024:.2f}")

# COMMAND ----------

# Correzione 8e – errore silenzioso: il return era dentro il ciclo (3966.21 invece di 12002.72)
def total_revenue(revenues):
    revenue_sum = 0
    for revenue in revenues:
        revenue_sum = revenue_sum + revenue
    return revenue_sum

print(f"{total_revenue([3966.21, 5139.59, 2896.92]):.2f}")

# COMMAND ----------

# Correzione 8f – errore silenzioso: mancava il return (None invece di 724.23)
def revenue_per_booking(revenue, bookings):
    result = round(revenue / bookings, 2)
    return result

print(revenue_per_booking(2896.92, 4))
