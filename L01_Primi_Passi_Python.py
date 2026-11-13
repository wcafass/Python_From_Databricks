# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 1 – Primi passi con Python
# MAGIC
# MAGIC Notebook del Capitolo 1 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Creare e aggiornare variabili con l'assegnazione; dare nomi corretti a variabili e costanti
# MAGIC - Riconoscere i tipi base `int`, `float`, `str`, `bool`, `None` con `type()`
# MAGIC - Mostrare valori con `print()` e con le f-string, scegliendo i decimali
# MAGIC - Convertire valori con `int()`, `float()`, `str()` e arrotondare con `round()`
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitolo 0; notebook collegato al compute **Serverless**
# MAGIC - Nessuna tabella da preparare: i valori delle strutture guida sono scritti a mano
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: le sezioni 1.9 e 1.10 contengono errori voluti.
# MAGIC Ogni sezione crea le variabili che usa: dopo un'interruzione della sessione si riparte dalla prima cella della sezione.
# MAGIC
# MAGIC | property_id | title | destination | property_type | base_price | Prenotazioni 2024 | Cancellate | Ricavo 2024 |
# MAGIC |---|---|---|---|---|---|---|---|
# MAGIC | 11670 | Historic Inn in Rome | Rome | Historical Place | 284.97 | 6 | 0 | 3966.21 |
# MAGIC | 16317 | Bungalow in Sardinia | Sardinia | Summer Getaway | 213.91 | 7 | 1 | 5139.59 |
# MAGIC | 16225 | Beach House in Amalfi | Amalfi | Summer Getaway | 236.95 | 4 | 2 | 2896.92 |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.1 Variabili e assegnazione
# MAGIC `nome = valore` mette un valore in una variabile; il simbolo `=` si legge da destra verso sinistra ("metti"). La cella seguente non mostra nulla.

# COMMAND ----------

revenue_2024 = 3966.21

# COMMAND ----------

revenue_2024 = 3966.21
bookings_2024 = 6
revenue_2024 / bookings_2024

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `661.035` (ricavo medio per prenotazione della struttura di Roma).
# MAGIC
# MAGIC **Ponte SQL**: l'alias `AS` dà un nome a un valore, ma vale solo dentro la query.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 3966.21 AS revenue_2024, 6 AS bookings_2024

# COMMAND ----------

# MAGIC %md
# MAGIC **Riassegnare una variabile**: la nuova assegnazione sostituisce il valore precedente.

# COMMAND ----------

property_title = "Historic Inn in Rome"
property_title = "Bungalow in Sardinia"
property_title

# COMMAND ----------

# MAGIC %md
# MAGIC **Usare il valore attuale**: ogni riga prende il totale attuale, aggiunge un ricavo e rimette il risultato in `total_revenue`. Risultato atteso: `12002.72`.

# COMMAND ----------

total_revenue = 3966.21
total_revenue = total_revenue + 5139.59
total_revenue = total_revenue + 2896.92
total_revenue

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.2 Dare un nome alle variabili
# MAGIC Regole: lettere, cifre e `_`; nessuna cifra all'inizio; niente spazi o trattini; maiuscole e minuscole diverse.
# MAGIC Convenzioni del libro: snake_case in inglese per le variabili, MAIUSCOLO per le **costanti**.

# COMMAND ----------

ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0
WORK_SCHEMA = "workspace.libro_python"
CANCELLATION_RATE_THRESHOLD

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.3 I tipi base
# MAGIC `int`, `float`, `str`, `bool`, `None` (tipo `NoneType`). `type()` mostra il tipo di un valore.

# COMMAND ----------

type(11670)

# COMMAND ----------

property_id = 11670
base_price = 284.97
property_type = "Historical Place"
is_deleted = False
rating = None
type(base_price)

# COMMAND ----------

# MAGIC %md
# MAGIC Si provi a cambiare l'ultima riga della cella precedente in `type(property_type)`, `type(is_deleted)`, `type(rating)`: risultati attesi `str`, `bool`, `NoneType`.
# MAGIC
# MAGIC **Ponte SQL**: i tipi delle colonne con `DESCRIBE TABLE` (colonna `data_type`: `date` per `check_in`, `float` per `total_amount`, `string` per `status`) e il tipo di un'espressione con `typeof()`.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT typeof(6), typeof(3966.21), typeof('Rome'), typeof(true)

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `int`, `decimal(6,2)`, `string`, `boolean`. In SQL 3966.21 è un decimale a precisione fissa, in Python un `float`.
# MAGIC
# MAGIC ## 1.4 Testo e numeri
# MAGIC Le virgolette decidono il tipo: `"11670"` è un testo, `11670` un numero.

# COMMAND ----------

type("11670")

# COMMAND ----------

# MAGIC %md
# MAGIC **Zero, testo vuoto e None** sono tre valori diversi: un conteggio che vale zero, un testo senza caratteri, un valore mancante.

# COMMAND ----------

cancelled_bookings = 0
review_comment = ""
average_rating = None
print(cancelled_bookings, type(cancelled_bookings))
print(review_comment, type(review_comment))
print(average_rating, type(average_rating))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.5 Mostrare i valori: print() e le f-string
# MAGIC Ogni `print()` scrive una riga; i testi compaiono senza apici.

# COMMAND ----------

property_title = "Historic Inn in Rome"
revenue_2024 = 3966.21
bookings_2024 = 6
print(property_title)
print(revenue_2024)
print(bookings_2024)

# COMMAND ----------

print("Ricavo 2024:", revenue_2024, "- prenotazioni:", bookings_2024)

# COMMAND ----------

# MAGIC %md
# MAGIC **f-string**: `f` davanti alle virgolette; ogni nome (o calcolo) tra graffe viene sostituito dal suo valore.

# COMMAND ----------

print(f"{property_title}: {bookings_2024} prenotazioni, ricavo {revenue_2024}")

# COMMAND ----------

print(f"Ricavo medio per prenotazione: {revenue_2024 / bookings_2024}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: lo stesso testo con `||` e `CAST`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Historic Inn in Rome: ' || CAST(6 AS STRING) || ' prenotazioni' AS label

# COMMAND ----------

# MAGIC %md
# MAGIC **Scegliere i decimali**: `:.1f` = un decimale, `:.2f` = due, `:.0f` = nessuno. Il valore della variabile non cambia.

# COMMAND ----------

cancellation_rate = 1 / 7 * 100
print(cancellation_rate)
print(f"Tasso di cancellazione: {cancellation_rate:.1f}%")

# COMMAND ----------

print(f"Ricavo medio: {revenue_2024 / bookings_2024:.2f}")
print(f"Tasso arrotondato all'unità: {cancellation_rate:.0f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `Ricavo medio: 661.03` (non 661.04: vedi sezione 1.6) e `Tasso arrotondato all'unità: 14%`.
# MAGIC
# MAGIC La cella seguente è un **errore silenzioso**: nessun messaggio, ma l'output non è quello voluto. La correzione è nella cella successiva.

# COMMAND ----------

# ERRORE SILENZIOSO – manca la f davanti alle virgolette
print("Ricavo 2024: {revenue_2024}")

# COMMAND ----------

# Correzione
print(f"Ricavo 2024: {revenue_2024}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.6 I decimali approssimati
# MAGIC Risultato atteso: `854.9100000000001`. Non è un errore: i `float` sono memorizzati in forma binaria e alcuni decimali non sono esatti.

# COMMAND ----------

base_price = 284.97
base_price * 3

# COMMAND ----------

print(f"Tre notti al prezzo base: {base_price * 3:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.7 I commenti
# MAGIC Il testo dopo `#` viene ignorato da Python, come `--` in SQL. Ctrl+/ (Cmd+/ su Mac) aggiunge o toglie il `#` sulle righe selezionate.

# COMMAND ----------

# Dati 2024 della struttura guida di Amalfi
cancelled_bookings = 2
bookings_2024 = 4

cancellation_rate = cancelled_bookings / bookings_2024 * 100  # in percentuale
print(f"Tasso di cancellazione: {cancellation_rate:.1f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.8 Conversioni di tipo
# MAGIC `float()`, `int()`, `str()` convertono un valore nel tipo indicato, come `CAST` in SQL. La data resta testo fino al Capitolo 7.

# COMMAND ----------

base_price_text = "284.97"
bookings_text = "6"
check_in_text = "2024-03-15"

base_price = float(base_price_text)
bookings_2024 = int(bookings_text)
print(base_price * 2)
print(bookings_2024 + 1)
print(type(base_price), type(bookings_2024))

# COMMAND ----------

property_id = 11670
property_id_text = str(property_id)
print(property_id_text, type(property_id_text))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le stesse conversioni con `CAST`. In Databricks `CAST(284.97 AS INT)` tronca a 284, come `int()`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT CAST('284.97' AS DOUBLE) AS base_price,
# MAGIC        CAST('6' AS INT)         AS bookings_2024,
# MAGIC        CAST(11670 AS STRING)    AS property_id_text,
# MAGIC        CAST(284.97 AS INT)      AS truncated_price

# COMMAND ----------

# MAGIC %md
# MAGIC **int() tronca, round() arrotonda**. `round(valore, n)` arrotonda a n decimali e produce un nuovo valore (il formato `:.1f` cambia solo la scritta).

# COMMAND ----------

print(int(284.97))
print(round(284.97))

# COMMAND ----------

cancellation_rate = 1 / 7 * 100
rounded_rate = round(cancellation_rate, 1)
print(rounded_rate)

# COMMAND ----------

# MAGIC %md
# MAGIC **Una conversione che riesce passando da float()**: `int("284.97")` fallisce (lo vediamo nella sezione 1.10), `int(float("284.97"))` funziona. Risultato atteso: `284`.

# COMMAND ----------

int(float("284.97"))

# COMMAND ----------

# MAGIC %md
# MAGIC **bool() in breve**: zero, testo vuoto e `None` diventano `False`; gli altri valori `True`.

# COMMAND ----------

print(bool(0), bool(6), bool(""), bool("Rome"), bool(None))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.9 Le variabili vivono nella memoria del compute
# MAGIC Conta l'ordine di esecuzione, non la posizione nel notebook. Prova da fare:
# MAGIC 1. eseguire **per prima** la cella marcata `ERRORE VOLUTO`: deve fallire con `NameError: name 'reviews_count' is not defined`, perché la variabile non esiste ancora;
# MAGIC 2. eseguire la cella con l'assegnazione;
# MAGIC 3. rieseguire la cella `ERRORE VOLUTO`: ora funziona e stampa `11`.
# MAGIC
# MAGIC Lo stesso `NameError` compare su qualunque variabile dopo la chiusura della sessione del compute: in quel caso si rieseguono le celle dall'inizio.

# COMMAND ----------

# ERRORE VOLUTO (se eseguita prima della cella sotto) – variabile non ancora creata
print(reviews_count)

# COMMAND ----------

# Assegnazione: recensioni non cancellate della struttura di Roma
reviews_count = 11

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.10 Leggere gli errori del capitolo
# MAGIC Le celle seguenti vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si legge il nome dell'errore e la descrizione (ultima riga del messaggio);
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori**.
# MAGIC
# MAGIC Risultati attesi delle correzioni: nessun output (assegnazione); `12002.72`; nessun output (assegnazione); due righe `Ricavo 2024: 3966.21`; `6`.

# COMMAND ----------

# ERRORE VOLUTO – nome di variabile che inizia con una cifra
2024_revenue = 3966.21

# COMMAND ----------

# Correzione: l'anno va in fondo al nome
revenue_2024 = 3966.21

# COMMAND ----------

# ERRORE VOLUTO – maiuscola nel nome della variabile
total_revenue = 12002.72
print(Total_revenue)

# COMMAND ----------

# Correzione
total_revenue = 12002.72
print(total_revenue)

# COMMAND ----------

# ERRORE VOLUTO – testo senza virgolette
destination = Rome

# COMMAND ----------

# Correzione
destination = "Rome"

# COMMAND ----------

# ERRORE VOLUTO – testo e numero uniti con +
revenue_2024 = 3966.21
print("Ricavo 2024: " + revenue_2024)

# COMMAND ----------

# Correzione: f-string, oppure valori separati da una virgola
revenue_2024 = 3966.21
print(f"Ricavo 2024: {revenue_2024}")
print("Ricavo 2024:", revenue_2024)

# COMMAND ----------

# ERRORE VOLUTO – int() su un testo con decimali
bookings_2024 = int("6.0")

# COMMAND ----------

# Correzione: prima float(), poi int()
bookings_2024 = int(float("6.0"))
bookings_2024

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - `nome = valore` crea una variabile (si legge "metti"); `total = total + x` la aggiorna usando il valore attuale.
# MAGIC - Nomi in snake_case e in inglese; costanti in MAIUSCOLO; maiuscole e minuscole contano.
# MAGIC - Tipi base: `int`, `float`, `str`, `bool`, `None`; `type()` mostra il tipo. `"11670"` non è `11670`; `0`, `""` e `None` sono diversi.
# MAGIC - `print()` mostra più valori; f-string `f"... {nome:.1f} ..."` per comporre testi e scegliere i decimali.
# MAGIC - I `float` sono approssimati: si formattano con `:.2f`.
# MAGIC - Commenti con `#`.
# MAGIC - `int()`, `float()`, `str()` come `CAST`; `int()` tronca, `round()` arrotonda; conversione impossibile = `ValueError`.
# MAGIC - Le variabili vivono nella memoria del compute: conta l'ordine di esecuzione; `NameError` dopo un'interruzione → rieseguire dall'alto.
