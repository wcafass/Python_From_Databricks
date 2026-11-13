# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 1 – Soluzioni
# MAGIC
# MAGIC Soluzioni commentate degli esercizi di `L01_Esercizi` (le stesse dell'Appendice A).
# MAGIC Si esegue una cella alla volta: l'esercizio 8 contiene errori voluti.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Le variabili della seconda struttura

# COMMAND ----------

# Valori del Bungalow in Sardinia: l'identificativo è un numero intero, come la colonna property_id
property_id = 16317
property_title = "Bungalow in Sardinia"
destination = "Sardinia"
base_price = 213.91

# print() con due valori: il valore e il suo tipo, separati da uno spazio
print(property_id, type(property_id))
print(property_title, type(property_title))
print(destination, type(destination))
print(base_price, type(base_price))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Indovina il tipo
# MAGIC Le virgolette rendono testo anche `"2024"` e `"True"`; la divisione restituisce sempre un `float`.

# COMMAND ----------

# 2024 – tipo atteso: int
type(2024)

# COMMAND ----------

# "2024" – tipo atteso: str (le virgolette lo rendono un testo)
type("2024")

# COMMAND ----------

# 30.0 – tipo atteso: float (c'è il punto decimale)
type(30.0)

# COMMAND ----------

# True – tipo atteso: bool
type(True)

# COMMAND ----------

# "True" – tipo atteso: str (tra virgolette non è un valore vero/falso)
type("True")

# COMMAND ----------

# None – tipo atteso: NoneType
type(None)

# COMMAND ----------

# 4 / 2 – tipo atteso: float (vale 2.0: la divisione dà sempre un float)
type(4 / 2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Una riga di report

# COMMAND ----------

property_title = "Beach House in Amalfi"
destination = "Amalfi"
bookings_2024 = 4
revenue_2024 = 2896.92

# Una sola f-string: le parentesi tonde intorno a {destination} sono testo
print(f"{property_title} ({destination}): {bookings_2024} prenotazioni, ricavo {revenue_2024}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Tre tassi di cancellazione

# COMMAND ----------

CANCELLATION_RATE_THRESHOLD = 30.0

# Roma: 0 cancellate su 6 (uno zero vero, non un valore mancante)
rome_rate = 0 / 6 * 100
# Sardegna: 1 su 7
sardinia_rate = 1 / 7 * 100
# Amalfi: 2 su 4
amalfi_rate = 2 / 4 * 100

# :.1f mostra un decimale; la soglia è un float e compare come 30.0
print(f"Historic Inn in Rome: {rome_rate:.1f}% (soglia {CANCELLATION_RATE_THRESHOLD}%)")
print(f"Bungalow in Sardinia: {sardinia_rate:.1f}% (soglia {CANCELLATION_RATE_THRESHOLD}%)")
print(f"Beach House in Amalfi: {amalfi_rate:.1f}% (soglia {CANCELLATION_RATE_THRESHOLD}%)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Una scheda arrivata come testo

# COMMAND ----------

base_price_text = "236.95"
bookings_text = "4"
revenue_text = "2896.92"

# 1. Conversioni: prezzo e ricavo hanno decimali (float), le prenotazioni sono un intero (int)
base_price = float(base_price_text)
bookings_2024 = int(bookings_text)
revenue_2024 = float(revenue_text)

# 2. Calcoli
revenue_per_booking = revenue_2024 / bookings_2024
nights_at_base_price = revenue_per_booking / base_price
print(f"Ricavo medio per prenotazione: {revenue_per_booking:.2f}")
print(f"Notti al prezzo base: {nights_at_base_price:.1f}")

# 3. int() tronca (236), round() arrotonda (237)
print(f"int: {int(base_price)} - round: {round(base_price)}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Totali passo per passo

# COMMAND ----------

total_bookings = 0
total_cancelled = 0

# Roma
total_bookings = total_bookings + 6
total_cancelled = total_cancelled + 0
# Sardegna
total_bookings = total_bookings + 7
total_cancelled = total_cancelled + 1
# Amalfi
total_bookings = total_bookings + 4
total_cancelled = total_cancelled + 2

# Il tasso complessivo si calcola sui totali, non come media dei tre tassi
total_rate = total_cancelled / total_bookings * 100
print(f"Prenotazioni: {total_bookings} - cancellate: {total_cancelled} - tasso complessivo: {total_rate:.1f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Il prezzo base medio

# COMMAND ----------

total_base_price = 284.97 + 213.91 + 236.95
print(total_base_price)  # 735.8299999999999: decimali approssimati dei float, non un errore

average_base_price = total_base_price / 3
print(average_base_price)                # valore completo
print(f"{average_base_price:.2f}")       # formato: cambia solo la scritta
print(round(average_base_price, 2))      # nuovo valore arrotondato, utilizzabile nei calcoli
print(int(average_base_price))           # int() tronca: scarta i decimali

# Spiegazione: i float sono memorizzati in forma binaria e 284.97, 213.91, 236.95 non hanno
# una rappresentazione esatta; la somma mostra la piccola differenza. Il valore da usare nei
# calcoli successivi con due decimali è quello di round(..., 2); il formato :.2f serve solo a mostrarlo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Ogni cella `ERRORE VOLUTO` deve fallire; la correzione sotto deve funzionare.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
property title = "Historic Inn in Rome"

# COMMAND ----------

# Correzione 8a (SyntaxError: invalid syntax – un nome non può contenere spazi)
property_title = "Historic Inn in Rome"
print(property_title)

# COMMAND ----------

# ERRORE VOLUTO – cella 8b
rating = 3.2
print(f"Voto medio: {Rating}")

# COMMAND ----------

# Correzione 8b (NameError: name 'Rating' is not defined – maiuscole e minuscole contano)
rating = 3.2
print(f"Voto medio: {rating}")

# COMMAND ----------

# ERRORE VOLUTO – cella 8c
print("Prenotazioni: " + 6)

# COMMAND ----------

# Correzione 8c (TypeError: can only concatenate str (not "int") to str – si usa una f-string)
print(f"Prenotazioni: {6}")

# COMMAND ----------

# ERRORE VOLUTO – cella 8d
base_price = int("213,91")

# COMMAND ----------

# Correzione 8d (ValueError: invalid literal for int() with base 10: '213,91')
# Due problemi: la virgola decimale e int() al posto di float()
base_price = float("213.91")
print(base_price)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e
revenue_2024 = 5139.59
print("Ricavo 2024: {revenue_2024}")

# COMMAND ----------

# Correzione 8e (nessun messaggio, ma le graffe compaiono così come sono: manca la f)
revenue_2024 = 5139.59
print(f"Ricavo 2024: {revenue_2024}")
