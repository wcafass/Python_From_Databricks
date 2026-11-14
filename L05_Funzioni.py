# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 5 – Funzioni
# MAGIC
# MAGIC Notebook del Capitolo 5 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Definire una funzione con `def` e chiamarla: definire non è eseguire
# MAGIC - Passare valori con parametri e argomenti; restituire un risultato con `return`
# MAGIC - Scrivere funzioni con condizioni e cicli, e funzioni che ne chiamano altre
# MAGIC - Usare valori di default e argomenti per nome; capire le variabili locali
# MAGIC - Documentare una funzione con una docstring e sceglierle un buon nome
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–4; notebook collegato al compute **Serverless**
# MAGIC - Le celle `%sql` leggono `samples.wanderbricks`; nessuna cella scrive tabelle
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: la sezione 5.10 contiene errori voluti ed errori silenziosi.
# MAGIC Si esegue per prima la **cella di preparazione**. Le celle con un `def` vanno eseguite prima delle celle che chiamano la funzione; alcune funzioni vengono ridefinite in versioni successive: vale l'ultima cella eseguita.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione

# COMMAND ----------

# Cella di preparazione: costanti e collezioni usate nelle sezioni
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
base_prices = [284.97, 213.91, 236.95]
bookings_2024 = [6, 7, 4]
ratings_with_gap = [3.2, None, 3.0]   # voto della Sardegna non disponibile (esempio)

# Campione di importi di esempio, con un valore negativo e due mancanti (Capitolo 4)
sample_amounts = [879.15, None, 412.5, -42.76, 655.0, None]

# Le strutture guida come piccola tabella (Capitolo 3)
guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.1 Definire e chiamare una funzione
# MAGIC **Ponte SQL**: due funzioni già note, con nome, parentesi, valori e risultato. Risultato atteso: `Amalfi`, `AMALFI`, `248.80`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT destination,
# MAGIC        UPPER(destination)       AS destination_upper,
# MAGIC        ROUND(236.95 * 1.05, 2)  AS new_price
# MAGIC FROM samples.wanderbricks.destinations
# MAGIC WHERE destination_id = 1100

# COMMAND ----------

# MAGIC %md
# MAGIC Le funzioni già pronte di Python hanno la stessa forma. Risultati attesi: `248.8`, `3`, `284.97`.

# COMMAND ----------

print(round(236.95 * 1.05, 2))
print(len(property_titles))
print(max(base_prices))

# COMMAND ----------

# MAGIC %md
# MAGIC La prima funzione: la cella **definisce** la funzione e non produce nessun output.

# COMMAND ----------

def print_report_header():
    print("Report delle strutture guida")
    print(f"Anno di analisi: {ANALYSIS_YEAR}")
    print("-" * 30)

# COMMAND ----------

# MAGIC %md
# MAGIC La **chiamata** esegue il corpo. Risultato atteso: `Report delle strutture guida`, `Anno di analisi: 2024` e trenta trattini.

# COMMAND ----------

print_report_header()

# COMMAND ----------

# MAGIC %md
# MAGIC Una funzione si chiama tutte le volte che si vuole. Risultato atteso: due intestazioni, ciascuna seguita da una riga con il numero di strutture (`3` e `18163`), separate da una riga vuota.

# COMMAND ----------

print_report_header()
print("Strutture analizzate: 3")
print()
print_report_header()
print("Strutture analizzate: 18163")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.2 Parametri e argomenti
# MAGIC Due parametri nella definizione. La cella non produce output.

# COMMAND ----------

def print_bookings(title, bookings):
    print(f"{title}: {bookings} prenotazioni")

# COMMAND ----------

# MAGIC %md
# MAGIC Gli argomenti si abbinano ai parametri per posizione. Risultati attesi: `Historic Inn in Rome: 6 prenotazioni` e `Bungalow in Sardinia: 7 prenotazioni`.

# COMMAND ----------

print_bookings("Historic Inn in Rome", 6)
print_bookings("Bungalow in Sardinia", 7)

# COMMAND ----------

# MAGIC %md
# MAGIC Gli argomenti possono essere variabili con nomi diversi dai parametri. Risultato atteso: `Beach House in Amalfi: 4 prenotazioni`.

# COMMAND ----------

amalfi_title = "Beach House in Amalfi"
amalfi_bookings = 4
print_bookings(amalfi_title, amalfi_bookings)

# COMMAND ----------

# MAGIC %md
# MAGIC La chiamata dentro un ciclo, con argomenti diversi a ogni giro. Risultato atteso: le tre righe delle strutture guida.

# COMMAND ----------

for position in range(len(property_titles)):
    print_bookings(property_titles[position], bookings_2024[position])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.3 Restituire un risultato: return
# MAGIC `return` consegna il valore a chi chiama la funzione. La cella non produce output.

# COMMAND ----------

def increase_price(price):
    new_price = round(price * 1.05, 2)
    return new_price

# COMMAND ----------

# MAGIC %md
# MAGIC La chiamata "vale" il valore restituito. Risultati attesi: `248.8`, `Aumento: 11.85`, `[299.22, 224.61, 248.8]`.

# COMMAND ----------

amalfi_new_price = increase_price(236.95)
print(amalfi_new_price)
print(f"Aumento: {amalfi_new_price - 236.95:.2f}")
new_prices = [increase_price(price) for price in base_prices]
print(new_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC Stampare o restituire: una funzione senza `return` restituisce `None`. Risultati attesi: `248.8`, poi `None`.

# COMMAND ----------

def print_increased_price(price):
    print(round(price * 1.05, 2))

result = print_increased_price(236.95)
print(result)

# COMMAND ----------

# MAGIC %md
# MAGIC Return anticipato per il caso particolare (`None`, come `NULL * 1.05` in SQL). La cella ridefinisce `increase_price`. Risultati attesi: `248.8` e `None`.

# COMMAND ----------

def increase_price(price):
    if price is None:
        return None
    return round(price * 1.05, 2)

print(increase_price(236.95))
print(increase_price(None))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: una funzione temporanea definita in SQL. La cella non restituisce righe.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY FUNCTION increase_price(price DOUBLE)
# MAGIC RETURNS DOUBLE
# MAGIC RETURN ROUND(price * 1.05, 2)

# COMMAND ----------

# MAGIC %md
# MAGIC La funzione SQL si usa come `ROUND`. Risultato atteso: 11670 284.97 299.22; 16225 236.95 248.8; 16317 213.91 224.61.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, base_price, increase_price(base_price) AS new_price
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC Con `NULL` la funzione SQL restituisce `NULL`. Risultato atteso: `248.8` e `null`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT increase_price(236.95) AS amalfi, increase_price(NULL) AS missing

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.4 Funzioni con condizioni
# MAGIC La classificazione del Capitolo 2 con un nome: un `return` in ogni ramo. La cella non produce output.

# COMMAND ----------

def classify_cancellation_rate(rate):
    if rate is None:
        return "dato mancante"
    if rate < 0 or rate > 100:
        return "valore impossibile"
    if rate > CANCELLATION_RATE_THRESHOLD:
        return "critico"
    return "ok"

# COMMAND ----------

# MAGIC %md
# MAGIC La funzione dentro un ciclo. Risultati attesi: `0.0: ok`, `14.3: ok`, `50.0: critico`, `None: dato mancante`, `120.0: valore impossibile`.

# COMMAND ----------

sample_rates = [0.0, 14.3, 50.0, None, 120.0]
for rate in sample_rates:
    print(f"{rate}: {classify_cancellation_rate(rate)}")

# COMMAND ----------

# MAGIC %md
# MAGIC Il tasso di cancellazione, con `None` se le prenotazioni sono zero. Risultati attesi: `50.0`, `14.285714285714285`, `None`.

# COMMAND ----------

def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

print(cancellation_rate(2, 4))
print(cancellation_rate(1, 7))
print(cancellation_rate(0, 0))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.5 Funzioni con un ciclo
# MAGIC `SUM` e `COUNT(colonna)` scritti a mano: l'accumulatore si prepara nel corpo, il `return` va dopo il ciclo. Le due celle non producono output.

# COMMAND ----------

def calculate_total(values):
    total = 0
    for value in values:
        if value is not None:
            total = total + value
    return total

# COMMAND ----------

def count_present(values):
    count = 0
    for value in values:
        if value is not None:
            count = count + 1
    return count

# COMMAND ----------

# MAGIC %md
# MAGIC Le stesse due funzioni su tre liste diverse. Risultati attesi: `6.2` su `2`; `1903.89` su `4`; `17` su `3`.

# COMMAND ----------

print(f"Voti: somma {calculate_total(ratings_with_gap):.1f} su {count_present(ratings_with_gap)} valori presenti")
print(f"Importi: somma {calculate_total(sample_amounts):.2f} su {count_present(sample_amounts)} valori presenti")
print(f"Prenotazioni: somma {calculate_total(bookings_2024)} su {count_present(bookings_2024)} valori presenti")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `SUM`, `COUNT` e `AVG` sugli stessi sei importi. Risultato atteso: `1903.89`, `4`, `475.972500`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT SUM(amount)   AS amount_sum,
# MAGIC        COUNT(amount) AS amount_count,
# MAGIC        AVG(amount)   AS amount_avg
# MAGIC FROM VALUES (879.15), (NULL), (412.5), (-42.76), (655.0), (NULL) AS t(amount)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.6 Funzioni che chiamano altre funzioni
# MAGIC La media dei valori presenti usa le due funzioni della sezione 5.5 (eseguite prima). Risultati attesi: `Media dei voti: 3.1`, `Media degli importi: 475.97`, `None`.

# COMMAND ----------

def calculate_average(values):
    count = count_present(values)
    if count == 0:
        return None
    return calculate_total(values) / count

print(f"Media dei voti: {calculate_average(ratings_with_gap):.1f}")
print(f"Media degli importi: {calculate_average(sample_amounts):.2f}")
print(calculate_average([None, None]))

# COMMAND ----------

# MAGIC %md
# MAGIC Il ciclo del Capitolo 4 in due righe (servono `cancellation_rate` e `classify_cancellation_rate` della sezione 5.4). Risultati attesi: `Historic Inn in Rome: 0.0% (ok)`, `Bungalow in Sardinia: 14.3% (ok)`, `Beach House in Amalfi: 50.0% (critico)`.

# COMMAND ----------

def describe_property(row):
    rate = cancellation_rate(row["cancelled_2024"], row["bookings_2024"])
    status = classify_cancellation_rate(rate)
    return f"{row['title']}: {rate:.1f}% ({status})"

for row in guide_properties:
    print(describe_property(row))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.7 Valori di default e argomenti per nome
# MAGIC **Ponte SQL**: il secondo valore di `ROUND` è facoltativo. Risultato atteso: `214` e `213.9`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ROUND(213.91) AS no_digits, ROUND(213.91, 1) AS one_digit

# COMMAND ----------

# MAGIC %md
# MAGIC Parametri con valore di default. Risultati attesi: `248.8`, `302.41`, `348.16`.

# COMMAND ----------

def project_price(price, years=1, growth_rate=0.05):
    projected_price = price
    for year in range(years):
        projected_price = projected_price * (1 + growth_rate)
    return round(projected_price, 2)

print(project_price(236.95))
print(project_price(236.95, 5))
print(project_price(236.95, 5, 0.08))

# COMMAND ----------

# MAGIC %md
# MAGIC Argomenti per nome: si cambia un solo default. Risultati attesi: `255.91`, `274.69`, `302.41`.

# COMMAND ----------

print(project_price(236.95, growth_rate=0.08))
print(project_price(236.95, years=5, growth_rate=0.03))
print(project_price(price=236.95, years=5))

# COMMAND ----------

# MAGIC %md
# MAGIC La soglia come parametro con default (la cella ridefinisce `classify_cancellation_rate`). Risultati attesi: `ok`, `critico`, `critico`.

# COMMAND ----------

def classify_cancellation_rate(rate, threshold=CANCELLATION_RATE_THRESHOLD):
    if rate is None:
        return "dato mancante"
    if rate < 0 or rate > 100:
        return "valore impossibile"
    if rate > threshold:
        return "critico"
    return "ok"

print(classify_cancellation_rate(14.3))
print(classify_cancellation_rate(14.3, 10.0))
print(classify_cancellation_rate(14.3, threshold=10.0))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.8 Variabili dentro e fuori dalle funzioni
# MAGIC Un'assegnazione dentro la funzione crea una variabile locale e non tocca quella esterna. Risultati attesi: `Dentro la funzione: da verificare` e `Fuori dalla funzione: ok`.

# COMMAND ----------

status = "ok"

def reset_status():
    status = "da verificare"
    print(f"Dentro la funzione: {status}")

reset_status()
print(f"Fuori dalla funzione: {status}")

# COMMAND ----------

# MAGIC %md
# MAGIC Si entra dai parametri, si esce con `return`: la variabile esterna non cambia. Risultati attesi: `256.47` e `284.97`.

# COMMAND ----------

def apply_discount(price, discount=0.10):
    discounted_price = price * (1 - discount)
    return round(discounted_price, 2)

rome_price = 284.97
print(apply_discount(rome_price))
print(rome_price)

# COMMAND ----------

# MAGIC %md
# MAGIC Un dizionario ricevuto come argomento: le modifiche al contenuto si vedono fuori. Risultato atteso: la riga di Amalfi con `'cancellation_rate': 50.0` e `'cancellation_status': 'critico'`.

# COMMAND ----------

def add_cancellation_status(row):
    rate = cancellation_rate(row["cancelled_2024"], row["bookings_2024"])
    row["cancellation_rate"] = rate
    row["cancellation_status"] = classify_cancellation_rate(rate)

for row in guide_properties:
    add_cancellation_status(row)
print(guide_properties[2])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.9 Docstring e buoni nomi
# MAGIC Una docstring di una riga, mostrata da `help()`. Risultato atteso: `Help on function cancellation_rate in module __main__:`, la riga `cancellation_rate(cancelled, bookings)` e la docstring.

# COMMAND ----------

def cancellation_rate(cancelled, bookings):
    """Restituisce il tasso di cancellazione in percentuale, o None se non ci sono prenotazioni."""
    if bookings == 0:
        return None
    return cancelled / bookings * 100

help(cancellation_rate)

# COMMAND ----------

# MAGIC %md
# MAGIC Una docstring su più righe (servono le funzioni della sezione 5.5). Risultato atteso: l'aiuto di `calculate_average` con le tre righe di descrizione.

# COMMAND ----------

def calculate_average(values):
    """Calcola la media dei valori presenti di una lista.

    I valori None vengono ignorati, come fa AVG in SQL.
    Restituisce None se la lista non contiene valori presenti.
    """
    count = count_present(values)
    if count == 0:
        return None
    return calculate_total(values) / count

help(calculate_average)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.10 Leggere gli errori del capitolo
# MAGIC Le celle seguenti vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si legge il nome dell'errore e la descrizione;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori**.
# MAGIC
# MAGIC Ogni cella contiene la definizione della funzione che usa; le correzioni riportano le funzioni alla forma giusta.
# MAGIC
# MAGIC Risultati attesi delle correzioni, nell'ordine: `248.8`; `248.8`; `302.41`; `50.0`; `248.8`; `256.47`; `497.6`; l'intestazione del report; `248.8`; `17`; `50.0`.

# COMMAND ----------

# ERRORE VOLUTO – mancano i due punti dopo la riga di definizione
def increase_price(price)
    return round(price * 1.05, 2)

# COMMAND ----------

# Correzione: la riga di definizione termina con i due punti
def increase_price(price):
    return round(price * 1.05, 2)

print(increase_price(236.95))

# COMMAND ----------

# ERRORE VOLUTO – il corpo della funzione non è rientrato
def increase_price(price):
return round(price * 1.05, 2)

# COMMAND ----------

# Correzione: il corpo è rientrato di 4 spazi
def increase_price(price):
    return round(price * 1.05, 2)

print(increase_price(236.95))

# COMMAND ----------

# ERRORE VOLUTO – growth_rate non ha un default ma segue years, che lo ha
def project_price(price, years=1, growth_rate):
    return round(price * (1 + growth_rate) ** years, 2)

# COMMAND ----------

# Correzione: anche growth_rate ha un default
def project_price(price, years=1, growth_rate=0.05):
    return round(price * (1 + growth_rate) ** years, 2)

print(project_price(236.95, 5))

# COMMAND ----------

# ERRORE VOLUTO – la chiamata passa un solo argomento, la funzione ne richiede due
def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

print(cancellation_rate(2))

# COMMAND ----------

# Correzione: si passano entrambi gli argomenti
def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

print(cancellation_rate(2, 4))

# COMMAND ----------

# ERRORE VOLUTO – la chiamata passa due argomenti, la funzione ne accetta uno
def increase_price(price):
    return round(price * 1.05, 2)

print(increase_price(236.95, 0.10))

# COMMAND ----------

# Correzione: la chiamata passa il solo prezzo
def increase_price(price):
    return round(price * 1.05, 2)

print(increase_price(236.95))

# COMMAND ----------

# ERRORE VOLUTO – discounted_price esiste solo dentro la funzione
def apply_discount(price, discount=0.10):
    discounted_price = price * (1 - discount)
    return round(discounted_price, 2)

apply_discount(284.97)
print(discounted_price)

# COMMAND ----------

# Correzione: il risultato si ottiene dal valore restituito
def apply_discount(price, discount=0.10):
    discounted_price = price * (1 - discount)
    return round(discounted_price, 2)

rome_discounted = apply_discount(284.97)
print(rome_discounted)

# COMMAND ----------

# ERRORE VOLUTO – la funzione stampa ma non restituisce: il risultato è None
def print_increased_price(price):
    print(round(price * 1.05, 2))

new_price = print_increased_price(236.95)
print(new_price * 2)

# COMMAND ----------

# Correzione: la funzione che calcola restituisce il risultato, la stampa si fa fuori
def increase_price(price):
    return round(price * 1.05, 2)

new_price = increase_price(236.95)
print(new_price * 2)

# COMMAND ----------

# ERRORE SILENZIOSO – senza parentesi la funzione non viene chiamata
def print_report_header():
    print("Report delle strutture guida")
    print("-" * 30)

print_report_header

# COMMAND ----------

# Correzione: la chiamata ha le parentesi
def print_report_header():
    print("Report delle strutture guida")
    print("-" * 30)

print_report_header()

# COMMAND ----------

# ERRORE SILENZIOSO – la funzione calcola ma non restituisce il risultato
def increase_price(price):
    new_price = round(price * 1.05, 2)

print(increase_price(236.95))

# COMMAND ----------

# Correzione: il corpo termina con return
def increase_price(price):
    new_price = round(price * 1.05, 2)
    return new_price

print(increase_price(236.95))

# COMMAND ----------

# ERRORE SILENZIOSO – il return è dentro il ciclo: la funzione termina al primo giro
def calculate_total(values):
    total = 0
    for value in values:
        if value is not None:
            total = total + value
        return total

print(calculate_total(bookings_2024))

# COMMAND ----------

# Correzione: il return è allo stesso livello del for, dopo il ciclo
def calculate_total(values):
    total = 0
    for value in values:
        if value is not None:
            total = total + value
    return total

print(calculate_total(bookings_2024))

# COMMAND ----------

# ERRORE SILENZIOSO – argomenti nell'ordine sbagliato: prenotazioni e cancellate scambiate
def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

print(cancellation_rate(4, 2))

# COMMAND ----------

# Correzione: argomenti per nome, l'ordine non conta più
def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

print(cancellation_rate(cancelled=2, bookings=4))

# COMMAND ----------

# MAGIC %md
# MAGIC **Errore silenzioso: def modificato ma non rieseguito** (non riproducibile in una cella). Si corregge il corpo di una funzione nella cella del `def`, ma si riesegue solo la cella con la chiamata: Python continua a usare la versione in memoria e il risultato non cambia. **Correzione**: dopo ogni modifica si riesegue la cella del `def`, poi le celle che chiamano la funzione.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - `def nome(parametri):` e il corpo rientrato **definiscono** la funzione senza eseguirla; `nome(argomenti)` la **chiama**. La cella del `def` si esegue prima delle chiamate e si riesegue dopo ogni modifica; un nuovo `def` con lo stesso nome sostituisce la funzione.
# MAGIC - Parametri (nella definizione) e argomenti (nella chiamata) si abbinano per posizione; il numero deve corrispondere.
# MAGIC - `return` consegna il valore e termina la funzione; senza `return` il risultato è `None`. Chi calcola restituisce, la stampa si fa fuori. Return anticipato per i casi particolari.
# MAGIC - Funzione con condizioni = `CASE WHEN` con un nome; funzione con un ciclo: accumulatore nel corpo, `return` dopo il ciclo (`calculate_total`, `count_present`, `calculate_average` come `SUM`, `COUNT`, `AVG`).
# MAGIC - Le funzioni possono chiamarne altre: ognuna fa una cosa sola.
# MAGIC - Default (`parametro=valore`) dopo i parametri senza default; argomenti per nome (`nome=valore`) dopo quelli per posizione. Il default si legge quando si esegue il `def`.
# MAGIC - Variabili locali: esistono solo durante la chiamata. Le modifiche al contenuto di liste e dizionari ricevuti come argomento si vedono fuori.
# MAGIC - Docstring tra `"""` nella prima riga del corpo, mostrata da `help()`; nomi con un verbo, in inglese, `is_` per vero/falso, `print_` per le funzioni che stampano, mai i nomi già pronti di Python.
