# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 1 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**. Nessuna tabella da preparare: i valori sono quelli delle strutture guida, scritti a mano.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L01_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L01_Esercizi_svolti`). Si esegue una cella alla volta (l'esercizio 8 contiene errori voluti).
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso, da confrontare con il proprio output.
# MAGIC
# MAGIC | property_id | title | destination | base_price | Prenotazioni 2024 | Cancellate | Ricavo 2024 |
# MAGIC |---|---|---|---|---|---|---|
# MAGIC | 11670 | Historic Inn in Rome | Rome | 284.97 | 6 | 0 | 3966.21 |
# MAGIC | 16317 | Bungalow in Sardinia | Sardinia | 213.91 | 7 | 1 | 5139.59 |
# MAGIC | 16225 | Beach House in Amalfi | Amalfi | 236.95 | 4 | 2 | 2896.92 |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Le variabili della seconda struttura
# MAGIC Creare le variabili `property_id`, `property_title`, `destination` e `base_price` con i valori del Bungalow in Sardinia e stampare ciascuna insieme al suo tipo, con un `print()` per variabile.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("16317 <class 'int'>")
print("Bungalow in Sardinia <class 'str'>")
print("Sardinia <class 'str'>")
print("213.91 <class 'float'>")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Indovina il tipo
# MAGIC Per ciascun valore scrivere prima, in un commento, il tipo atteso; poi verificarlo con `type()`, un valore per cella:
# MAGIC `2024`, `"2024"`, `30.0`, `True`, `"True"`, `None`, `4 / 2`.

# COMMAND ----------

# 2024 – tipo atteso: ...


# COMMAND ----------

# "2024" – tipo atteso: ...


# COMMAND ----------

# 30.0 – tipo atteso: ...


# COMMAND ----------

# True – tipo atteso: ...


# COMMAND ----------

# "True" – tipo atteso: ...


# COMMAND ----------

# None – tipo atteso: ...


# COMMAND ----------

# 4 / 2 – tipo atteso: ...


# COMMAND ----------

# Verifica: risultato atteso
print("int, str, float, bool, str, NoneType, float")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Una riga di report
# MAGIC Con le variabili della Beach House in Amalfi (`property_title`, `destination`, `bookings_2024`, `revenue_2024`) stampare la riga di report con **una sola f-string**.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Beach House in Amalfi (Amalfi): 4 prenotazioni, ricavo 2896.92")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Tre tassi di cancellazione
# MAGIC Definire la costante `CANCELLATION_RATE_THRESHOLD = 30.0`. Per ciascuna struttura guida calcolare il tasso di cancellazione (cancellate / prenotazioni × 100) e stamparlo con un decimale, insieme alla soglia.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Historic Inn in Rome: 0.0% (soglia 30.0%)")
print("Bungalow in Sardinia: 14.3% (soglia 30.0%)")
print("Beach House in Amalfi: 50.0% (soglia 30.0%)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Una scheda arrivata come testo
# MAGIC La scheda della Beach House in Amalfi arriva con tutti i valori come testo (cella sotto).
# MAGIC 1. Convertire i tre valori nel tipo adatto.
# MAGIC 2. Calcolare il ricavo medio per prenotazione (due decimali) e a quante notti al prezzo base corrisponde (ricavo medio / prezzo base, un decimale).
# MAGIC 3. Stampare `int()` e `round()` del prezzo base.

# COMMAND ----------

base_price_text = "236.95"
bookings_text = "4"
revenue_text = "2896.92"

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Ricavo medio per prenotazione: 724.23")
print("Notti al prezzo base: 3.1")
print("int: 236 - round: 237")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Totali passo per passo
# MAGIC Partendo da `total_bookings = 0` e `total_cancelled = 0`, aggiungere una struttura alla volta, con riassegnazioni, le prenotazioni (6, 7, 4) e le cancellazioni (0, 1, 2). Calcolare poi il tasso di cancellazione complessivo con un decimale.

# COMMAND ----------

total_bookings = 0
total_cancelled = 0

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Prenotazioni: 17 - cancellate: 3 - tasso complessivo: 17.6%")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Il prezzo base medio
# MAGIC Calcolare il prezzo base medio delle tre strutture guida (284.97, 213.91, 236.95) e mostrarlo in quattro modi: valore completo, formato `:.2f`, `round(..., 2)`, `int()`.
# MAGIC Spiegare in un commento perché la somma dei tre prezzi compare come `735.8299999999999` e quale dei quattro risultati è un valore utilizzabile nei calcoli successivi con due decimali.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("245.27666666666664")
print("245.28")
print("245.28")
print("245")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, la quinta un **errore silenzioso**. Eseguirle una per una, annotare il nome dell'errore (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `Historic Inn in Rome`, `Voto medio: 3.2`, `Prenotazioni: 6`, `213.91`, `Ricavo 2024: 5139.59`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
property title = "Historic Inn in Rome"

# COMMAND ----------

# Correzione 8a (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8b
rating = 3.2
print(f"Voto medio: {Rating}")

# COMMAND ----------

# Correzione 8b (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
print("Prenotazioni: " + 6)

# COMMAND ----------

# Correzione 8c (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8d
base_price = int("213,91")

# COMMAND ----------

# Correzione 8d (nome dell'errore: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e
revenue_2024 = 5139.59
print("Ricavo 2024: {revenue_2024}")

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)

