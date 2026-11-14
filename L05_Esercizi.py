# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 5 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**. Gli esercizi 2, 4 e 5 hanno una verifica `%sql` su `samples.wanderbricks`; l'esercizio 7 su `workspace.libro_python.b_bookings` (creata da `L00_Prepara_Dati`).
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L05_Soluzioni`.
# MAGIC
# MAGIC Si lavora su una copia creata con **Clone** (per esempio `L05_Esercizi_svolti`). Si esegue per prima la cella di preparazione, poi una cella alla volta (l'esercizio 8 contiene errori voluti).
# MAGIC Ogni esercizio ha una cella di **verifica** che stampa il risultato atteso, da confrontare con il proprio output. Ogni funzione va provata con le chiamate indicate; dopo ogni modifica a una funzione si riesegue la cella del `def`.
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
# MAGIC ## Esercizio 1 ★ – Una scheda per struttura
# MAGIC 1. Definire la funzione `print_property_card(title, destination, base_price)` che stampa tre righe: il titolo, poi `  Destinazione: ...` e `  Prezzo base: ...` (con due spazi iniziali).
# MAGIC 2. Chiamarla per Roma (`"Historic Inn in Rome"`, `"Rome"`, 284.97) e per Amalfi (`"Beach House in Amalfi"`, `"Amalfi"`, 236.95).
# MAGIC 3. Mettere il risultato di una terza chiamata, per la Sardegna (`"Bungalow in Sardinia"`, `"Sardinia"`, 213.91), in una variabile `card_result` e stamparla. Che cosa contiene, e perché?

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Historic Inn in Rome")
print("  Destinazione: Rome")
print("  Prezzo base: 284.97")
print("Beach House in Amalfi")
print("  Destinazione: Amalfi")
print("  Prezzo base: 236.95")
print("Bungalow in Sardinia")
print("  Destinazione: Sardinia")
print("  Prezzo base: 213.91")
print(None)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Il costo di un soggiorno
# MAGIC 1. Definire la funzione `stay_cost(price, nights)` che **restituisce** il costo del soggiorno arrotondato a due decimali.
# MAGIC 2. Con una list comprehension, calcolare il costo di 3 notti per ciascun prezzo di `base_prices` e stampare la lista.
# MAGIC 3. Calcolare con un accumulatore il costo totale dei tre soggiorni e stamparlo con due decimali (`Totale: ...`).
# MAGIC 4. Stampare il costo di 7 notti ad Amalfi (`Amalfi, 7 notti: ...`).

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print([854.91, 641.73, 710.85])
print("Totale: 2207.49")
print("Amalfi, 7 notti: 1658.65")

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
# MAGIC La funzione `show_average` (cella sotto) stampa la media di una lista, ma non la restituisce.
# MAGIC 1. Riscriverla come `calculate_mean(values)`, che **restituisce** la media.
# MAGIC 2. Usarla per calcolare la media dei prezzi base e stamparla con due decimali (`Prezzo base medio: ...`).
# MAGIC 3. Con un ciclo e un contatore, contare i prezzi base superiori alla media (`Prezzi sopra la media: ...`).
# MAGIC 4. Calcolare la media delle prenotazioni 2024 (`Prenotazioni medie: ...`, due decimali).
# MAGIC
# MAGIC Suggerimento: provare `result = show_average(base_prices)` e `print(result)` per vedere perché `show_average` non basta.

# COMMAND ----------

def show_average(values):
    print(sum(values) / len(values))

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Prezzo base medio: 245.28")
print("Prezzi sopra la media: 1")
print("Prenotazioni medie: 5.67")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Fasce di prezzo con una funzione
# MAGIC 1. Definire `classify_price(price)` che restituisce `"dato mancante"` per `None`, `"alto"` da 250 in su, `"medio"` da 200 in su e `"basso"` sotto 200, con un `return` in ogni ramo e **senza `elif`**.
# MAGIC 2. Applicarla con un ciclo alla lista di esempio `sample_prices` (cella sotto), stampando una riga per prezzo (`284.97: alto`).
# MAGIC 3. Nello stesso ciclo contare con un dizionario quanti prezzi cadono in ogni fascia (come nell'esercizio 7 del Capitolo 4) e stampare il dizionario.

# COMMAND ----------

sample_prices = [284.97, 213.91, 236.95, 189.0, None, 312.5]   # gli ultimi tre sono valori di esempio

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("284.97: alto")
print("213.91: medio")
print("236.95: medio")
print("189.0: basso")
print("None: dato mancante")
print("312.5: alto")
print({'alto': 2, 'medio': 2, 'basso': 1, 'dato mancante': 1})

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
# MAGIC 1. Definire `cancellation_rate(cancelled, bookings)`, che restituisce `None` se le prenotazioni sono zero.
# MAGIC 2. Definire `classify_cancellation_rate(rate, threshold=CANCELLATION_RATE_THRESHOLD)` con i quattro stati del capitolo (`"dato mancante"`, `"valore impossibile"`, `"critico"`, `"ok"`).
# MAGIC 3. Per ogni riga di `guide_properties`, stampare il tasso con un decimale e lo stato con la soglia di default e con una soglia di 10, passata **per nome** (`Historic Inn in Rome: 0.0% - soglia 30: ok - soglia 10: ok`).
# MAGIC 4. Contare le strutture critiche nei due casi.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Historic Inn in Rome: 0.0% - soglia 30: ok - soglia 10: ok")
print("Bungalow in Sardinia: 14.3% - soglia 30: ok - soglia 10: critico")
print("Beach House in Amalfi: 50.0% - soglia 30: critico - soglia 10: critico")
print("Critiche con soglia 30: 1 - con soglia 10: 2")

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
# MAGIC Definire `years_to_reach(price, target, growth_rate=0.05)` che restituisce il numero di anni dopo i quali il prezzo, con una crescita annua costante, **supera** l'obiettivo:
# MAGIC - se il prezzo supera già l'obiettivo, restituisce 0;
# MAGIC - si usa un ciclo `for` su `range(1, 51)` con un `return` dentro il ciclo, nel ramo in cui l'obiettivo è superato;
# MAGIC - se l'obiettivo non viene superato entro 50 anni, restituisce `None`.
# MAGIC
# MAGIC Provarla con: Amalfi 236.95 verso 300 (default); Sardegna 213.91 verso 284.97 all'8% e al 3% (`growth_rate` per nome); Roma 284.97 verso 250; Amalfi verso 300 con crescita 0.0.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Amalfi, 300 al 5%: 5 anni")
print("Sardegna, 284.97 all'8%: 4 anni")
print("Sardegna, 284.97 al 3%: 10 anni")
print("Roma, 250: 0 anni")
print("Amalfi, 300 allo 0%: None")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Un riepilogo degli importi
# MAGIC 1. Definire `is_valid_amount(amount)`, che restituisce `True` se l'importo è presente e non negativo, altrimenti `False`.
# MAGIC 2. Definire `summarize_amounts(amounts)`, che con un solo ciclo conta mancanti, negativi e validi (usando `is_valid_amount`), somma i validi e restituisce un dizionario con le chiavi `missing`, `negative`, `valid`, `total`, `average` (media dei validi, `None` se non ce ne sono).
# MAGIC 3. Applicarla ad `amounts_sample` (cella sotto) e a una seconda lista con soli valori non validi, `[None, -10.0]`; stampare i risultati come nella verifica.
# MAGIC
# MAGIC Scrivere una docstring per entrambe le funzioni.

# COMMAND ----------

amounts_sample = [512.4, -80.0, None, 1250.75, 333.3, None, -15.5, 968.1]

# Scrivere qui la soluzione


# COMMAND ----------

# Verifica: risultato atteso
print("Mancanti: 2 - negativi: 2 - validi: 4")
print("Totale validi: 3064.55 - media: 766.14")
print("Secondo campione: validi 0 - totale 0 - media None")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: nulli e negativi dell'intera copia didattica b_bookings (30 e 13)
# MAGIC SELECT COUNT(*) - COUNT(total_amount)                    AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END) AS negative_amounts
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare il nome dell'errore (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `1658.65` nelle prime tre (provando la funzione con 236.95 e 7 notti); `12002.72` nella quarta e nella quinta; `724.23` nella sesta.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
def stay_cost(price, nights)
    return round(price * nights, 2)

# COMMAND ----------

# Correzione 8a (nome dell'errore: ...; provare la funzione con 236.95 e 7 notti)


# COMMAND ----------

# ERRORE VOLUTO – cella 8b
def stay_cost(price, nights):
    return round(price * nights, 2)

print(stay_cost(236.95))

# COMMAND ----------

# Correzione 8b (nome dell'errore: ...)


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
def stay_cost(price=236.95, nights):
    return round(price * nights, 2)

# COMMAND ----------

# Correzione 8c (nome dell'errore: ...; tenere 236.95 come default del prezzo)


# COMMAND ----------

# ERRORE VOLUTO – cella 8d
def total_revenue(revenues):
    revenue_sum = 0
    for revenue in revenues:
        revenue_sum = revenue_sum + revenue
    return revenue_sum

total_revenue([3966.21, 5139.59, 2896.92])
print(f"{revenue_sum:.2f}")

# COMMAND ----------

# Correzione 8d (nome dell'errore: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (ricavo totale delle strutture guida)
def total_revenue(revenues):
    revenue_sum = 0
    for revenue in revenues:
        revenue_sum = revenue_sum + revenue
        return revenue_sum

print(f"{total_revenue([3966.21, 5139.59, 2896.92]):.2f}")

# COMMAND ----------

# Correzione 8e (che cosa non va: ...)


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (ricavo per prenotazione di Amalfi)
def revenue_per_booking(revenue, bookings):
    result = round(revenue / bookings, 2)

print(revenue_per_booking(2896.92, 4))

# COMMAND ----------

# Correzione 8f (che cosa non va: ...)

