# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 2 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**. I valori sono quelli delle strutture guida, nella cella di preparazione; l'esercizio 5 ha una verifica `%sql` su `samples.wanderbricks.properties`.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L02_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L02_Esercizi_svolti`). Si esegue per prima la cella di preparazione, poi una cella alla volta (l'esercizio 8 contiene errori voluti).
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso, da confrontare con il proprio output.
# MAGIC
# MAGIC | property_id | title | destination | property_type | base_price | Prenotazioni 2024 | Cancellate | Ricavo 2024 |
# MAGIC |---|---|---|---|---|---|---|---|
# MAGIC | 11670 | Historic Inn in Rome | Rome | Historical Place | 284.97 | 6 | 0 | 3966.21 |
# MAGIC | 16317 | Bungalow in Sardinia | Sardinia | Summer Getaway | 213.91 | 7 | 1 | 5139.59 |
# MAGIC | 16225 | Beach House in Amalfi | Amalfi | Summer Getaway | 236.95 | 4 | 2 | 2896.92 |

# COMMAND ----------

# Cella di preparazione: costanti e valori delle strutture guida
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

rome_bookings = 6
rome_cancelled = 0
rome_revenue = 3966.21
sardinia_bookings = 7
sardinia_cancelled = 1
sardinia_revenue = 5139.59
amalfi_bookings = 4
amalfi_cancelled = 2
amalfi_revenue = 2896.92

property_id = 16225
property_title = "Beach House in Amalfi"
destination = "Amalfi"
property_type = "Summer Getaway"
base_price = 236.95
average_rating = 3.0

print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Calcoli sulle strutture guida
# MAGIC Con le variabili della cella di preparazione calcolare: prenotazioni e cancellazioni totali delle tre strutture, ricavo totale (due decimali), ricavo medio per prenotazione delle tre strutture insieme (due decimali) e prezzo base medio (284.97, 213.91, 236.95; due decimali). Attenzione alle parentesi.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Prenotazioni: 17 - cancellate: 3")
print("Ricavo totale: 12002.72")
print("Ricavo medio per prenotazione: 706.04")
print("Prezzo base medio: 245.28")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Settimane, ore e minuti
# MAGIC 1. Con `//` e `%` calcolare settimane intere e notti in più per soggiorni di 9 e di 23 notti.
# MAGIC 2. Il tempo di risposta di un messaggio al servizio clienti è di 3725 secondi: scriverlo in ore, minuti e secondi. Suggerimento: i minuti si calcolano dal resto della divisione per 3600.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("9 notti: settimane intere 1, notti in più 2")
print("23 notti: settimane intere 3, notti in più 2")
print("3725 secondi = 1 h 2 min 5 s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Vero o falso
# MAGIC Per ciascuna espressione scrivere prima, in un commento, il risultato atteso (`True` o `False`); poi verificarlo con `print()`:
# MAGIC
# MAGIC a) `destination == "Amalfi"` · b) `destination == "AMALFI"` · c) `property_id == "16225"` · d) `base_price > 200 and base_price < 250` · e) `284.97 * 3 == 854.91` · f) `0 <= 50.0 <= 100` · g) `ANALYSIS_YEAR % 4 == 0` · h) `not (amalfi_bookings > 5)`

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("a) True  b) False  c) False  d) True  e) False  f) True  g) True  h) True")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Condizioni composte
# MAGIC Per una prenotazione con `booking_status = "confirmed"`, `total_amount = 1250.0`, `guests_count = 5` calcolare tre variabili `bool`:
# MAGIC - `is_active`: lo stato è `"confirmed"` oppure `"completed"`;
# MAGIC - `is_large`: importo di almeno 1000 **e** almeno 4 ospiti;
# MAGIC - `needs_check`: lo stato è `"cancelled"` oppure l'importo è inferiore a 100.
# MAGIC
# MAGIC Stamparle su una riga; ripetere con `booking_status = "cancelled"`, `total_amount = 80.0`, `guests_count = 2`.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("attiva: True - grande: True - da controllare: False")
print("attiva: False - grande: False - da controllare: True")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Fasce di prezzo
# MAGIC Scrivere in una cella la classificazione del prezzo base: almeno 250 → `"alto"`, almeno 200 → `"medio"`, altrimenti `"basso"`, stampando titolo e fascia.
# MAGIC Eseguire la cella quattro volte, cambiando le prime due righe: Roma (284.97), Sardegna (213.91), Amalfi (236.95) e una struttura di prova (180.0). Confrontare poi con la verifica `%sql`.

# COMMAND ----------

property_title = "Historic Inn in Rome"
base_price = 284.97

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Historic Inn in Rome: alto")
print("Bungalow in Sardinia: medio")
print("Beach House in Amalfi: medio")
print("Struttura di prova: basso")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: le tre strutture guida classificate con CASE WHEN (alto, medio, medio)
# MAGIC SELECT property_id,
# MAGIC        title,
# MAGIC        CASE
# MAGIC          WHEN base_price >= 250 THEN 'alto'
# MAGIC          WHEN base_price >= 200 THEN 'medio'
# MAGIC          ELSE 'basso'
# MAGIC        END AS price_band
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Il tasso in quattro stati
# MAGIC Scrivere la classificazione di `cancellation_rate` in quattro stati: `"dato mancante"` (None), `"valore impossibile"` (sotto 0 o sopra 100), `"critico"` (sopra `CANCELLATION_RATE_THRESHOLD`), `"ok"`.
# MAGIC Eseguire la cella sei volte con `0.0`, `14.3`, `50.0`, `None`, `120.0`, `-5.0`. Rispondere in un commento: che cosa succede con `None` se il controllo su `None` viene spostato in fondo?

# COMMAND ----------

cancellation_rate = 0.0

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("0.0 ok")
print("14.3 ok")
print("50.0 critico")
print("None dato mancante")
print("120.0 valore impossibile")
print("-5.0 valore impossibile")
print("Con il controllo su None in fondo: TypeError: '<' not supported between instances of 'NoneType' and 'int'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Una scheda da validare
# MAGIC I dati di una struttura arrivano come testo (cella sotto). Scrivere una cella che:
# MAGIC 1. converte prenotazioni e cancellazioni in numeri interi;
# MAGIC 2. calcola il tasso di cancellazione solo se le prenotazioni sono più di zero, altrimenti lo imposta a `None`;
# MAGIC 3. imposta il voto a `None` se il testo è vuoto, altrimenti lo converte in `float`;
# MAGIC 4. classifica il tasso nei quattro stati dell'esercizio 6;
# MAGIC 5. stampa una riga di report con `n.d.` al posto dei valori mancanti (tasso con un decimale e `%`, voto con un decimale).
# MAGIC
# MAGIC Eseguire la cella quattro volte con (`"4"`, `"2"`, `""`), (`"4"`, `"2"`, `"3.0"`), (`"0"`, `"0"`, `"3.0"`), (`"4"`, `"5"`, `""`).

# COMMAND ----------

property_title = "Beach House in Amalfi"
bookings_text = "4"
cancelled_text = "2"
rating_text = ""

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Beach House in Amalfi: tasso 50.0% (critico), voto medio n.d.")
print("Beach House in Amalfi: tasso 50.0% (critico), voto medio 3.0")
print("Beach House in Amalfi: tasso n.d. (dato mancante), voto medio 3.0")
print("Beach House in Amalfi: tasso 125.0% (valore impossibile), voto medio n.d.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una (dopo la cella di preparazione), annotare il nome dell'errore (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `alto`, `Struttura estiva`, `critico`, `Voto non disponibile`, `critico`, `Nessuna verifica`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
rome_price = 284.97
if rome_price >= 250
    print("alto")

# COMMAND ----------

# Correzione 8a (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8b
if property_type = "Summer Getaway":
    print("Struttura estiva")

# COMMAND ----------

# Correzione 8b (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
amalfi_rate = 50.0
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
print("critico")

# COMMAND ----------

# Correzione 8c (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8d
average_rating = None
if average_rating >= 3.0:
    print("Voto sufficiente")

# COMMAND ----------

# Correzione 8d (nome dell'errore: ...; con il voto mancante stampare "Voto non disponibile")


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e
amalfi_rate = 50.0
if amalfi_rate > 15:
    print("attenzione")
elif amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print("critico")
else:
    print("ok")

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f
status = "completed"
if status == "cancelled" or "pending":
    print("Da verificare")
else:
    print("Nessuna verifica")

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)

