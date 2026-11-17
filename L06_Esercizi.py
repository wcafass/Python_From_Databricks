# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 6 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**. L'esercizio 5 ha una verifica `%sql` su `samples.wanderbricks.bookings`; l'esercizio 6 una verifica `%sql` con `try_cast`.
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L06_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L06_Esercizi_svolti`). Si esegue per prima la cella di preparazione, poi **una cella alla volta**: quasi tutti gli esercizi contengono celle che devono fallire (**ERRORE VOLUTO**) o che producono un risultato sbagliato (**ERRORE SILENZIOSO**). Non usare Run all.
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso, da confrontare con il proprio output. Per ogni errore si annotano il **tipo**, il **messaggio** e la **riga** (freccia `---->`), prima di correggere.

# COMMAND ----------

# Cella di preparazione: costanti e collezioni usate negli esercizi
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
base_prices = [284.97, 213.91, 236.95]
bookings_2024 = [6, 7, 4]
ratings_with_gap = [3.2, None, 3.0]   # voto della Sardegna non disponibile (esempio)

# Le strutture guida come piccola tabella (Capitolo 3)
guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]

# Gli importi di esempio del Capitolo 4, arrivati come testo
raw_amounts = ["879.15", "n.d.", "412.5", "-42.76", "", "655.0"]
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Leggere tre messaggi
# MAGIC 1. Eseguire le tre celle 1a, 1b, 1c. Per ciascuna annotare nella cella di risposta il **tipo** dell'errore e il **numero della riga** indicata dalla freccia.
# MAGIC 2. Scrivere nella cella di correzione la versione corretta delle tre celle: la 1a stampa il totale delle prenotazioni di Roma e Sardegna, la 1b la riga `Beach House in Amalfi: 4 prenotazioni`, la 1c il ricavo come numero (la virgola del testo si corregge scrivendo il testo con il punto).

# COMMAND ----------

# ERRORE VOLUTO – cella 1a
rome_bookings = 6
sardinia_bookings = 7
total_bookings = rome_bookings + sardinia_booking
print(total_bookings)

# COMMAND ----------

# ERRORE VOLUTO – cella 1b
amalfi_title = "Beach House in Amalfi"
amalfi_bookings = 4
print(amalfi_title + ": " + amalfi_bookings + " prenotazioni")

# COMMAND ----------

# ERRORE VOLUTO – cella 1c
raw_revenue = "2896,92"
amalfi_revenue = float(raw_revenue)
print(amalfi_revenue)

# COMMAND ----------

# Risposte (tipo dell'errore e riga indicata dalla freccia)
# 1a: tipo ..., riga ...
# 1b: tipo ..., riga ...
# 1c: tipo ..., riga ...

# Scrivere qui le tre correzioni


# COMMAND ----------

# Verifica: risultato atteso
print("1a: NameError, riga 4 - 1b: TypeError, riga 4 - 1c: ValueError, riga 3")
print(13)
print("Beach House in Amalfi: 4 prenotazioni")
print(2896.92)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Sintassi o esecuzione?
# MAGIC Le due celle seguenti cominciano con la stessa `print`. **Prima di eseguirle**, si scriva nella cella di risposta se la riga `Controllo dei prezzi` comparirà nell'output, e perché. Poi le si esegua e si correggano: la 2a deve stampare i tre prezzi, la 2b i tre prezzi e poi l'ultimo prezzo della lista.

# COMMAND ----------

# ERRORE VOLUTO – cella 2a
print("Controllo dei prezzi")
for price in base_prices
    print(price)

# COMMAND ----------

# ERRORE VOLUTO – cella 2b
print("Controllo dei prezzi")
for price in base_prices:
    print(price)
print(base_prices[3])

# COMMAND ----------

# Risposte (la print iniziale viene eseguita? perché?)
# 2a: ...
# 2b: ...

# Scrivere qui le due correzioni


# COMMAND ----------

# Verifica: risultato atteso
print("2a: no, errore di sintassi (SyntaxError): nessuna riga viene eseguita")
print("2b: sì, errore durante l'esecuzione (IndexError) alla riga 5: le righe precedenti vengono eseguite")
print("Correzione 2a: Controllo dei prezzi, 284.97, 213.91, 236.95")
print("Correzione 2b: Controllo dei prezzi, 284.97, 213.91, 236.95, 236.95")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Errori delle collezioni
# MAGIC Eseguire le tre celle, annotare il tipo dell'errore e correggerle:
# MAGIC - la 3a deve stampare il ricavo 2024 di Amalfi;
# MAGIC - la 3b deve stampare il titolo dell'ultima struttura;
# MAGIC - la 3c deve aggiungere il prezzo di esempio 250.0 in fondo a `extra_prices` e stampare la lista.

# COMMAND ----------

# ERRORE VOLUTO – cella 3a
amalfi_row = guide_properties[2]
print(amalfi_row["revenue"])

# COMMAND ----------

# ERRORE VOLUTO – cella 3b
print(property_titles[3])

# COMMAND ----------

# ERRORE VOLUTO – cella 3c
extra_prices = base_prices.copy()
extra_prices.add(250.0)
print(extra_prices)

# COMMAND ----------

# Risposte (tipo dell'errore)
# 3a: ...
# 3b: ...
# 3c: ...

# Scrivere qui le tre correzioni


# COMMAND ----------

# Verifica: risultato atteso
print("3a: KeyError - 3b: IndexError - 3c: AttributeError")
print(2896.92)
print("Beach House in Amalfi")
print([284.97, 213.91, 236.95, 250.0])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Un traceback a due livelli
# MAGIC 1. Eseguire la cella 4 e leggere il traceback **dal fondo**: in quale funzione e in quale riga avviene l'errore? Da quale riga dell'altra funzione è stata chiamata? Quale riga di `report_rows` lo provoca (guardare l'output stampato prima del messaggio)?
# MAGIC 2. Correggere: `revenue_per_booking` restituisce `None` se le prenotazioni sono zero; `print_revenue_report` stampa `n.d.` quando il valore è `None`.

# COMMAND ----------

# ERRORE VOLUTO – cella 4
def revenue_per_booking(revenue, bookings):
    return round(revenue / bookings, 2)

def print_revenue_report(rows):
    for row in rows:
        value = revenue_per_booking(row["revenue_2024"], row["bookings_2024"])
        print(f"{row['title']}: {value:.2f}")

report_rows = guide_properties.copy()
report_rows.append({"property_id": 99999, "title": "Struttura di esempio", "bookings_2024": 0, "cancelled_2024": 0, "revenue_2024": 0.0})
print_revenue_report(report_rows)

# COMMAND ----------

# Risposte
# Funzione e riga dell'errore: ...
# Riga della funzione chiamante: ...
# Riga di report_rows che lo provoca: ...

# Scrivere qui la correzione


# COMMAND ----------

# Verifica: risultato atteso
print("Errore: ZeroDivisionError in revenue_per_booking, riga 3, chiamata dalla riga 7 di print_revenue_report; riga: Struttura di esempio")
print("Historic Inn in Rome: 661.03")
print("Bungalow in Sardinia: 734.23")
print("Beach House in Amalfi: 724.23")
print("Struttura di esempio: n.d.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Un errore silenzioso, con metodo
# MAGIC La funzione della cella 5 dovrebbe calcolare il tasso di cancellazione complessivo delle tre strutture guida.
# MAGIC 1. **Passo zero**: calcolare a mano il risultato atteso (cancellate totali diviso prenotazioni totali, per cento) e scriverlo nella cella di risposta.
# MAGIC 2. Eseguire la cella 5 e confrontare.
# MAGIC 3. Ripetere il calcolo fuori dalla funzione con **print di controllo** di `total_cancelled`, `total_bookings` e del denominatore usato.
# MAGIC 4. Correggere la funzione e verificarla con il risultato atteso e con la cella `%sql`.

# COMMAND ----------

# ERRORE SILENZIOSO – cella 5
def overall_cancellation_rate(rows):
    total_cancelled = 0
    total_bookings = 0
    for row in rows:
        total_cancelled = total_cancelled + row["cancelled_2024"]
        total_bookings = total_bookings + row["bookings_2024"]
    return total_cancelled / len(rows) * 100

print(f"Tasso complessivo: {overall_cancellation_rate(guide_properties):.1f}%")

# COMMAND ----------

# Risposta (passo zero): ...

# Scrivere qui i print di controllo e la correzione


# COMMAND ----------

# Verifica: risultato atteso
print("Risultato sbagliato: 100.0% (3 cancellate divise per 3 righe)")
print("total_cancelled: 3 - total_bookings: 17 - len(rows): 3")
print("Tasso complessivo: 17.6%")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: tasso complessivo delle tre strutture guida nel 2024 (17.6)
# MAGIC SELECT SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS total_cancelled,
# MAGIC        COUNT(*)                                             AS total_bookings,
# MAGIC        ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS overall_rate
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Notti arrivate come testo
# MAGIC La lista `raw_nights` (cella sotto) contiene le notti di sei soggiorni di esempio, arrivate come testo.
# MAGIC 1. Con un ciclo, convertire ogni valore con `int()` dentro un `try` / `except ValueError as error`, raccogliendo i valori validi in una lista e contando gli scarti.
# MAGIC 2. Per ogni scarto stampare `Scartato: ` seguito dal messaggio dell'errore.
# MAGIC 3. Stampare la lista dei valori validi e la riga `Validi: ... - scartati: ... - notti totali: ... - media: ...` (media con un decimale).

# COMMAND ----------

raw_nights = ["3", "7", "n.d.", "2", "", "4"]   # valori di esempio

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Scartato: invalid literal for int() with base 10: 'n.d.'")
print("Scartato: invalid literal for int() with base 10: ''")
print([3, 7, 2, 4])
print("Validi: 4 - scartati: 2 - notti totali: 16 - media: 4.0")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: lo stesso calcolo con try_cast (16, 4, 2, 4.0)
# MAGIC SELECT SUM(try_cast(raw_nights AS INT))            AS total_nights,
# MAGIC        COUNT(try_cast(raw_nights AS INT))          AS valid_count,
# MAGIC        COUNT(*) - COUNT(try_cast(raw_nights AS INT)) AS rejected_count,
# MAGIC        ROUND(AVG(try_cast(raw_nights AS INT)), 1)   AS average_nights
# MAGIC FROM VALUES ('3'), ('7'), ('n.d.'), ('2'), (''), ('4') AS t(raw_nights)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Righe arrivate come testo
# MAGIC La lista `raw_booking_rows` (cella sotto) contiene sei prenotazioni di esempio arrivate come testo; in una manca la chiave `total_amount`.
# MAGIC 1. Definire `to_float(text)` come nella sezione 6.9 e `to_int(text)`, gemella per i numeri interi. Entrambe restituiscono `None` per un testo mancante o non convertibile; scrivere una docstring per ciascuna.
# MAGIC 2. Definire `clean_booking_row(row)`, che restituisce un **nuovo** dizionario con `booking_id` (intero), `nights` (intero o `None`) e `total_amount` (float o `None`). Per la chiave che può mancare si usa `get()`.
# MAGIC 3. Con un ciclo, pulire tutte le righe e contare: notti mancanti, importi mancanti, righe complete (notti e importo presenti). Sommare gli importi presenti.
# MAGIC 4. Per le sole righe complete, calcolare l'importo medio per notte (somma degli importi diviso somma delle notti, due decimali).

# COMMAND ----------

raw_booking_rows = [   # valori di esempio
    {"booking_id": "1001", "nights": "3", "total_amount": "854.91"},
    {"booking_id": "1002", "nights": "7", "total_amount": "n.d."},
    {"booking_id": "1003", "nights": "", "total_amount": "641.73"},
    {"booking_id": "1004", "nights": "2"},
    {"booking_id": "1005", "nights": "4", "total_amount": "947.80"},
    {"booking_id": "1006", "nights": "3,5", "total_amount": "710,85"},
]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print({'booking_id': 1004, 'nights': 2, 'total_amount': None})
print("Notti mancanti: 2 - importi mancanti: 3 - righe complete: 2")
print("Totale importi presenti: 2444.44")
print("Importo medio per notte (righe complete): 257.53")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare tipo, messaggio e riga (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `Prezzo medio: 245.28`; `3.2`; `236.95` e `None`; `[3.2, 3.0]`; `[284.97, 213.91, None]`; `Totale: 1903.89`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
average_price = sum(base_prices) / len(base_prices
print(f"Prezzo medio: {average_price:.2f}")

# COMMAND ----------

# Correzione 8a (tipo dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8b (il voto più alto tra quelli presenti)
best_rating = max(ratings_with_gap)
print(best_rating)

# COMMAND ----------

# Correzione 8b (tipo dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
def to_number(text):
    try:
        return float(text)
    except ValueError:
        return None

print(to_number("236.95"))
print(to_number(None))

# COMMAND ----------

# Correzione 8c (tipo dell'errore: ...; in quale funzione e riga?)


# COMMAND ----------

# ERRORE VOLUTO – cella 8d (i voti presenti in una nuova lista)
present_ratings = []
for rating in ratings_with_gap:
    if rating is not None:
        present_ratings = present_ratings.append(rating)
print(present_ratings)

# COMMAND ----------

# Correzione 8d (tipo dell'errore: ...; qual è la riga sbagliata?)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e
def to_number(text):
    try:
        return flaot(text)
    except:
        return None

print([to_number(value) for value in ["284.97", "213.91", "n.d."]])

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (totale degli importi validi)
total = 0
try:
    for raw_amount in raw_amounts:
        total = total + float(raw_amount)
except ValueError:
    print("Importo non valido")
print(f"Totale: {total:.2f}")

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)

