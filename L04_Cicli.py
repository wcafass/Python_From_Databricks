# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 4 – Cicli
# MAGIC
# MAGIC Notebook del Capitolo 4 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Ripetere un blocco di codice per ogni valore di una lista con il ciclo `for`
# MAGIC - Sommare, contare e costruire liste con un accumulatore; filtrare e classificare con `if` dentro il ciclo
# MAGIC - Calcolare somme e medie sui soli valori presenti, come `SUM` e `AVG`
# MAGIC - Usare `range()`, scorrere dizionari e liste di dizionari
# MAGIC - Riconoscere `while`, `break`, `continue` e la list comprehension in forma semplice
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–3; notebook collegato al compute **Serverless**
# MAGIC - Le celle `%sql` leggono `samples.wanderbricks`; una cella della sezione 4.4 legge `workspace.libro_python.b_bookings`, creata da `L00_Prepara_Dati` (Capitolo 0)
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: la sezione 4.11 contiene errori voluti, errori silenziosi e un ciclo infinito da fermare con **Interrupt**.
# MAGIC Si esegue per prima la **cella di preparazione**, che crea le costanti e le collezioni usate nelle sezioni.

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

# Prenotazioni per stato nella tabella bookings
status_counts_by_name = {
    "pending": 31575,
    "confirmed": 17948,
    "cancelled": 15285,
    "completed": 7439,
}

# Tabella di decodifica delle destinazioni italiane
destination_names = {
    1100: "Amalfi",
    2300: "Florence",
    3900: "Rome",
    4200: "Sardinia",
}

# Campione di importi di esempio, con un valore negativo e due mancanti
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
# MAGIC ## 4.1 Il ciclo for
# MAGIC Il blocco rientrato si ripete una volta per ogni valore della lista (un **giro** per valore). Risultati attesi: `284.97`, `213.91`, `236.95`.

# COMMAND ----------

for price in base_prices:
    print(price)

# COMMAND ----------

# MAGIC %md
# MAGIC Dentro e fuori dal ciclo: le righe rientrate si ripetono, quelle prima e dopo si eseguono una volta. Risultati attesi: `284.97 -> 299.22`, `213.91 -> 224.61`, `236.95 -> 248.80`, tra un'intestazione e una riga finale.

# COMMAND ----------

print("Prezzi base con un aumento del 5%:")
for price in base_prices:
    new_price = price * 1.05
    print(f"{price} -> {new_price:.2f}")
print("Fine dell'elenco")

# COMMAND ----------

# MAGIC %md
# MAGIC Dopo il ciclo la variabile del ciclo contiene l'ultimo valore. Risultato atteso: i tre titoli, poi `Dopo il ciclo title vale: Beach House in Amalfi`.

# COMMAND ----------

for title in property_titles:
    print(title)
print(f"Dopo il ciclo title vale: {title}")

# COMMAND ----------

# MAGIC %md
# MAGIC Con una lista vuota il blocco non si esegue mai. Risultato atteso: solo `Il ciclo è terminato`.

# COMMAND ----------

flagged_properties = []
for title in flagged_properties:
    print(title)
print("Il ciclo è terminato")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: SQL calcola la colonna per tutte le righe insieme. Risultato atteso: 11670 284.97 299.22; 16225 236.95 248.8; 16317 213.91 224.61.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, base_price, ROUND(base_price * 1.05, 2) AS new_price
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.2 L'accumulatore: sommare, contare, costruire una lista
# MAGIC Schema in tre tempi: prima del ciclo si prepara il totale, dentro lo si aggiorna, dopo si usa. Risultato atteso: `Prenotazioni totali: 17`.

# COMMAND ----------

total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# MAGIC %md
# MAGIC Lo stesso ciclo con i totali parziali, giro per giro. Risultati attesi: `6`, `13`, `17`, poi il totale.

# COMMAND ----------

total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
    print(f"aggiunto {bookings}, totale parziale {total_bookings}")
print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# MAGIC %md
# MAGIC Accumulatore con i decimali: il risultato grezzo può differire da `sum()` nelle ultime cifre. Risultati attesi: `735.8299999999999`, `735.83`, `Somma dei prezzi base: 735.83`.

# COMMAND ----------

total_price = 0
for price in base_prices:
    total_price = total_price + price
print(total_price)
print(sum(base_prices))
print(f"Somma dei prezzi base: {total_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC Contatore: aumenta di 1 a ogni giro. Risultati attesi: `3` e `3`.

# COMMAND ----------

property_count = 0
for price in base_prices:
    property_count = property_count + 1
print(f"Strutture contate: {property_count}")
print(f"len() restituisce: {len(base_prices)}")

# COMMAND ----------

# MAGIC %md
# MAGIC Costruire una lista: si parte da una lista vuota e si aggiunge un valore a ogni giro. Risultato atteso: `[299.22, 224.61, 248.8]`.

# COMMAND ----------

new_prices = []
for price in base_prices:
    new_prices.append(round(price * 1.05, 2))
print(new_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC Forma abbreviata `+=` (nel libro si usa la forma estesa). Risultato atteso: `17`.

# COMMAND ----------

total_bookings = 0
for bookings in bookings_2024:
    total_bookings += bookings
print(total_bookings)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.3 Condizioni dentro il ciclo
# MAGIC Filtrare (come `WHERE`): solo i prezzi sopra 230 finiscono nella nuova lista. Risultati attesi: `[284.97, 236.95]` e `Prezzi sopra 230: 2`.

# COMMAND ----------

high_prices = []
for price in base_prices:
    if price > 230:
        high_prices.append(price)
print(high_prices)
print(f"Prezzi sopra 230: {len(high_prices)}")

# COMMAND ----------

# MAGIC %md
# MAGIC Contare con una condizione, anche con `in`. Risultati attesi: `Cancellate: 2 su 6` e `Attive: 2 su 6`.

# COMMAND ----------

sample_statuses = ["confirmed", "cancelled", "pending", "completed", "cancelled", "pending"]
active_statuses = ["confirmed", "completed"]
cancelled_count = 0
active_count = 0
for status in sample_statuses:
    if status == "cancelled":
        cancelled_count = cancelled_count + 1
    if status in active_statuses:
        active_count = active_count + 1
print(f"Cancellate: {cancelled_count} su {len(sample_statuses)}")
print(f"Attive: {active_count} su {len(sample_statuses)}")

# COMMAND ----------

# MAGIC %md
# MAGIC Classificare ogni valore (come `CASE WHEN`): `if` / `elif` / `else` dentro il ciclo. Risultati attesi: `284.97: alto`, `213.91: medio`, `236.95: medio`.

# COMMAND ----------

for price in base_prices:
    if price >= 250:
        price_band = "alto"
    elif price >= 200:
        price_band = "medio"
    else:
        price_band = "basso"
    print(f"{price}: {price_band}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: lo stesso filtro con `WHERE` e `COUNT(*)`. Risultato atteso: `2`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS high_price_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND base_price > 230

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.4 Valori mancanti: somme e medie sui valori presenti
# MAGIC Si sommano e si contano solo i valori diversi da `None`, come fanno `SUM` e `AVG`. Risultati attesi: `Voti presenti: 2 su 3` e `Somma: 6.2 - media: 3.1`.

# COMMAND ----------

total_rating = 0
rating_count = 0
for rating in ratings_with_gap:
    if rating is not None:
        total_rating = total_rating + rating
        rating_count = rating_count + 1
average_rating = total_rating / rating_count
print(f"Voti presenti: {rating_count} su {len(ratings_with_gap)}")
print(f"Somma: {total_rating:.1f} - media: {average_rating:.1f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le stesse tre righe scritte con `VALUES`; `COUNT`, `SUM` e `AVG` ignorano il `NULL`. Risultato atteso: `3`, `2`, `6.2`, `3.10000`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)      AS row_count,
# MAGIC        COUNT(rating) AS rating_count,
# MAGIC        SUM(rating)   AS rating_sum,
# MAGIC        AVG(rating)   AS rating_avg
# MAGIC FROM VALUES (3.2), (NULL), (3.0) AS t(rating)

# COMMAND ----------

# MAGIC %md
# MAGIC Tre accumulatori e una classificazione: mancanti, negativi, somma degli importi validi. Risultati attesi: `2`, `1`, `1946.65`.

# COMMAND ----------

missing_count = 0
negative_count = 0
valid_total = 0
for amount in sample_amounts:
    if amount is None:
        missing_count = missing_count + 1
    elif amount < 0:
        negative_count = negative_count + 1
    else:
        valid_total = valid_total + amount
print(f"Importi mancanti: {missing_count}")
print(f"Importi negativi: {negative_count}")
print(f"Totale degli importi validi: {valid_total:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: gli stessi due conteggi sull'intera copia didattica `b_bookings` (Capitolo 0). Risultato atteso: `30` e `13`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) - COUNT(total_amount)                    AS missing_amounts,
# MAGIC        SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END) AS negative_amounts
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.5 range()
# MAGIC `range(5)` produce i numeri da 0 a 4: la fine è esclusa. Risultati attesi: `0`, `1`, `2`, `3`, `4`.

# COMMAND ----------

for number in range(5):
    print(number)

# COMMAND ----------

# MAGIC %md
# MAGIC `list()` mostra i numeri di un `range`; inizio, fine e passo. Risultati attesi: `[0, 1, 2, 3, 4]`, `[1, 2, 3, 4, 5, 6, 7, 8, 9]`, `[1, 3, 5, 7, 9]`.

# COMMAND ----------

print(list(range(5)))
print(list(range(1, 10)))
print(list(range(1, 10, 2)))

# COMMAND ----------

# MAGIC %md
# MAGIC Gli anni delle prenotazioni (`check_in` dal 2022 al 2025). Risultato atteso: solo il 2024 è bisestile.

# COMMAND ----------

for year in range(2022, 2026):
    if year % 4 == 0:
        print(f"{year}: bisestile")
    else:
        print(f"{year}: non bisestile")

# COMMAND ----------

# MAGIC %md
# MAGIC `range(len(lista))` per lavorare con la posizione e leggere due liste allineate. Risultati attesi: `0: Historic Inn in Rome - 284.97` e le altre due righe.

# COMMAND ----------

for position in range(len(property_titles)):
    print(f"{position}: {property_titles[position]} - {base_prices[position]}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: anche Databricks SQL ha una funzione `range`, con la fine esclusa. Risultati attesi: `0`–`4` e `2022`–`2025`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT id FROM range(5)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT id FROM range(2022, 2026)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.6 Cicli sui dizionari
# MAGIC Un ciclo su un dizionario restituisce le chiavi, nell'ordine di inserimento. Risultati attesi: `pending`, `confirmed`, `cancelled`, `completed`.

# COMMAND ----------

for status in status_counts_by_name:
    print(status)

# COMMAND ----------

# MAGIC %md
# MAGIC `values()` restituisce i valori. Risultato atteso: `Prenotazioni totali: 72247`.

# COMMAND ----------

total_bookings = 0
for count in status_counts_by_name.values():
    total_bookings = total_bookings + count
print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# MAGIC %md
# MAGIC `items()` restituisce le coppie: due variabili del ciclo. Si esegue prima la cella precedente (`total_bookings`). Risultati attesi: `pending: 31575 (43.7%)`, `confirmed: 17948 (24.8%)`, `cancelled: 15285 (21.2%)`, `completed: 7439 (10.3%)`.

# COMMAND ----------

for status, count in status_counts_by_name.items():
    share = count / total_bookings * 100
    print(f"{status}: {count} ({share:.1f}%)")

# COMMAND ----------

# MAGIC %md
# MAGIC Una tabella di decodifica usata a ogni giro, come un `JOIN` riga per riga. Risultati attesi: `3900 -> Rome`, `4200 -> Sardinia`, `1100 -> Amalfi`.

# COMMAND ----------

guide_destination_ids = [3900, 4200, 1100]
for destination_id in guide_destination_ids:
    print(f"{destination_id} -> {destination_names[destination_id]}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: conteggi e quote per stato. Risultato atteso: pending 31575 43.7; confirmed 17948 24.8; cancelled 15285 21.2; completed 7439 10.3.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status,
# MAGIC        COUNT(*)                           AS bookings,
# MAGIC        ROUND(COUNT(*) * 100.0 / 72247, 1) AS share
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC GROUP BY status
# MAGIC ORDER BY bookings DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.7 Cicli su una lista di dizionari
# MAGIC Un giro per ogni riga della piccola tabella. Risultati attesi: `Prenotazioni totali: 17` e `Ricavo totale: 12002.72`.

# COMMAND ----------

total_bookings = 0
total_revenue = 0
for row in guide_properties:
    total_bookings = total_bookings + row["bookings_2024"]
    total_revenue = total_revenue + row["revenue_2024"]
print(f"Prenotazioni totali: {total_bookings}")
print(f"Ricavo totale: {total_revenue:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC Una nuova colonna per ogni riga: tasso e stato di cancellazione. Risultati attesi: `Historic Inn in Rome: 0.0% (ok)`, `Bungalow in Sardinia: 14.3% (ok)`, `Beach House in Amalfi: 50.0% (critico)`.

# COMMAND ----------

for row in guide_properties:
    rate = row["cancelled_2024"] / row["bookings_2024"] * 100
    row["cancellation_rate"] = rate
    if rate > CANCELLATION_RATE_THRESHOLD:
        row["cancellation_status"] = "critico"
    else:
        row["cancellation_status"] = "ok"

for row in guide_properties:
    print(f"{row['title']}: {row['cancellation_rate']:.1f}% ({row['cancellation_status']})")

# COMMAND ----------

# MAGIC %md
# MAGIC Filtrare le righe con la nuova colonna (si esegue prima la cella precedente). Risultato atteso: `['Beach House in Amalfi']`.

# COMMAND ----------

critical_titles = []
for row in guide_properties:
    if row["cancellation_status"] == "critico":
        critical_titles.append(row["title"])
print(critical_titles)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: la stessa tabella calcolata da `bookings`, con tasso e stato. Risultato atteso: 11670 6 0 0.0 ok; 16225 4 2 50.0 critico; 16317 7 1 14.3 ok.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                                           AS bookings_2024,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)              AS cancelled_2024,
# MAGIC        ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)
# MAGIC              * 100.0 / COUNT(*), 1)                                       AS cancellation_rate,
# MAGIC        CASE WHEN SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)
# MAGIC                  * 100.0 / COUNT(*) > 30 THEN 'critico'
# MAGIC             ELSE 'ok'
# MAGIC        END                                                                AS cancellation_status
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.8 Il ciclo while
# MAGIC Il blocco si ripete finché la condizione resta vera: il numero di giri non è noto in partenza. Risultati attesi: `Anni necessari: 5` e `Prezzo raggiunto: 302.41`.

# COMMAND ----------

projected_price = 236.95
years = 0
while projected_price <= 300:
    projected_price = projected_price * 1.05
    years = years + 1
print(f"Anni necessari: {years}")
print(f"Prezzo raggiunto: {projected_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.9 break e continue
# MAGIC `break` esce subito dal ciclo: 16225 non viene controllato. Risultati attesi: `Controllo 11670`, `Controllo 16317`, `Trovata: 16317`, `Ricerca terminata`.

# COMMAND ----------

guide_property_ids = [11670, 16317, 16225]
searched_id = 16317
for property_id in guide_property_ids:
    print(f"Controllo {property_id}")
    if property_id == searched_id:
        print(f"Trovata: {property_id}")
        break
print("Ricerca terminata")

# COMMAND ----------

# MAGIC %md
# MAGIC Il calcolo della sezione 4.8 con `for`, `range` e `break`: al massimo 20 giri. Risultati attesi: `Anni necessari: 5` e `Prezzo raggiunto: 302.41`.

# COMMAND ----------

projected_price = 236.95
for year in range(1, 21):
    projected_price = projected_price * 1.05
    if projected_price > 300:
        break
print(f"Anni necessari: {year}")
print(f"Prezzo raggiunto: {projected_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC `continue` salta al giro successivo: i `None` non arrivano alla somma. Risultato atteso: `Totale degli importi presenti: 1903.89`.

# COMMAND ----------

present_total = 0
for amount in sample_amounts:
    if amount is None:
        continue
    present_total = present_total + amount
print(f"Totale degli importi presenti: {present_total:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.10 La list comprehension
# MAGIC Una lista costruita da un'altra in una riga. Risultato atteso: `[299.22, 224.61, 248.8]`, come il ciclo della sezione 4.2.

# COMMAND ----------

new_prices = [round(price * 1.05, 2) for price in base_prices]
print(new_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC Con `if` in fondo si tengono solo alcuni valori. Risultati attesi: `[284.97, 236.95]`, poi `[3.2, 3.0]` e `Media dei voti presenti: 3.1`.

# COMMAND ----------

high_prices = [price for price in base_prices if price > 230]
print(high_prices)

# COMMAND ----------

present_ratings = [rating for rating in ratings_with_gap if rating is not None]
print(present_ratings)
print(f"Media dei voti presenti: {sum(present_ratings) / len(present_ratings):.1f}")

# COMMAND ----------

# MAGIC %md
# MAGIC Da una lista di dizionari, una colonna. Risultato atteso: i tre titoli.

# COMMAND ----------

titles = [row["title"] for row in guide_properties]
print(titles)

# COMMAND ----------

# MAGIC %md
# MAGIC Su più righe, come una query: espressione, origine, condizione. Risultato atteso: `[299.22, 248.8]`.

# COMMAND ----------

expensive_new_prices = [
    round(price * 1.05, 2)
    for price in base_prices
    if price > 230
]
print(expensive_new_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `SELECT` (espressione) / `FROM` (origine) / `WHERE` (condizione). Risultato atteso: 11670 299.22; 16225 248.8.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, ROUND(base_price * 1.05, 2) AS new_price
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND base_price > 230
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.11 Leggere gli errori del capitolo
# MAGIC Le celle seguenti vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si legge il nome dell'errore e la descrizione;
# MAGIC - la cella del **ciclo infinito** non finisce da sola: la si ferma con **Interrupt**;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori**.
# MAGIC
# MAGIC Risultati attesi delle correzioni, nell'ordine: i tre prezzi (due volte); `0`, `1`, `2`; `Somma dei voti presenti: 6.2`; le quattro righe stato e conteggio; `Anni necessari: 5`; `Prenotazioni totali: 17` (due volte); `[299.22, 224.61, 248.8]`; i tre titoli.

# COMMAND ----------

# ERRORE VOLUTO – mancano i due punti dopo for
for price in base_prices
    print(price)

# COMMAND ----------

# Correzione: la riga del for termina con i due punti
for price in base_prices:
    print(price)

# COMMAND ----------

# ERRORE VOLUTO – il blocco del ciclo non è rientrato
for price in base_prices:
print(price)

# COMMAND ----------

# Correzione: il blocco del ciclo è rientrato di 4 spazi
for price in base_prices:
    print(price)

# COMMAND ----------

# ERRORE VOLUTO – len() restituisce un numero, non una sequenza
for position in len(base_prices):
    print(position)

# COMMAND ----------

# Correzione: range(len(...)) produce le posizioni
for position in range(len(base_prices)):
    print(position)

# COMMAND ----------

# ERRORE VOLUTO – il ciclo somma anche il valore None
total_rating = 0
for rating in ratings_with_gap:
    total_rating = total_rating + rating
print(total_rating)

# COMMAND ----------

# Correzione: si sommano solo i valori presenti
total_rating = 0
for rating in ratings_with_gap:
    if rating is not None:
        total_rating = total_rating + rating
print(f"Somma dei voti presenti: {total_rating:.1f}")

# COMMAND ----------

# ERRORE VOLUTO – senza items() il ciclo restituisce solo le chiavi
for status, count in status_counts_by_name:
    print(status, count)

# COMMAND ----------

# Correzione: items() restituisce le coppie chiave e valore
for status, count in status_counts_by_name.items():
    print(status, count)

# COMMAND ----------

# ERRORE VOLUTO – ciclo infinito: il prezzo non cambia mai (fermare la cella con Interrupt)
projected_price = 236.95
years = 0
while projected_price <= 300:
    years = years + 1

# COMMAND ----------

# Correzione: a ogni giro si aggiorna la variabile della condizione
projected_price = 236.95
years = 0
while projected_price <= 300:
    projected_price = projected_price * 1.05
    years = years + 1
print(f"Anni necessari: {years}")

# COMMAND ----------

# ERRORE SILENZIOSO – il totale viene azzerato a ogni giro
for bookings in bookings_2024:
    total_bookings = 0
    total_bookings = total_bookings + bookings
print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# Correzione: il totale si prepara una sola volta, prima del ciclo
total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# ERRORE SILENZIOSO – la print è dentro il ciclo
total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
    print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# Correzione: la print del risultato finale è fuori dal ciclo
total_bookings = 0
for bookings in bookings_2024:
    total_bookings = total_bookings + bookings
print(f"Prenotazioni totali: {total_bookings}")

# COMMAND ----------

# ERRORE SILENZIOSO – cambiare la variabile del ciclo non cambia la lista
for price in base_prices:
    price = round(price * 1.05, 2)
print(base_prices)

# COMMAND ----------

# Correzione: i nuovi valori si raccolgono in una nuova lista
new_prices = []
for price in base_prices:
    new_prices.append(round(price * 1.05, 2))
print(new_prices)

# COMMAND ----------

# ERRORE SILENZIOSO – range(1, ...) salta la posizione 0
for position in range(1, len(property_titles)):
    print(property_titles[position])

# COMMAND ----------

# Correzione: le posizioni partono da 0
for position in range(len(property_titles)):
    print(property_titles[position])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - `for variabile in lista:` ripete il blocco rientrato una volta per valore (un giro); la variabile del ciclo resta con l'ultimo valore; lista vuota = nessun giro.
# MAGIC - Accumulatore in tre tempi: prima (totale a 0, contatore a 0, lista vuota), dentro (aggiornamento), dopo (uso del risultato). Totali di `float` sempre formattati.
# MAGIC - `if` dentro il ciclo filtra (`WHERE`), conta, classifica (`CASE WHEN`); `is not None` per sommare e contare solo i valori presenti, come `SUM` e `AVG`.
# MAGIC - `range(n)`, `range(inizio, fine)`, `range(inizio, fine, passo)`: fine esclusa; `list(range(...))`; `range(len(lista))` per la posizione.
# MAGIC - Dizionari: il ciclo dà le chiavi; `values()` i valori; `items()` le coppie, con due variabili del ciclo.
# MAGIC - Lista di dizionari: un giro per riga; `row["chiave"] = ...` aggiunge una colonna a ogni riga.
# MAGIC - `while condizione:` per un numero di giri non noto; la condizione deve poter diventare falsa (altrimenti **Interrupt**). Di norma si preferisce `for`.
# MAGIC - `break` esce dal ciclo (come `LIMIT 1`), `continue` salta al giro successivo (come `WHERE ... IS NOT NULL`).
# MAGIC - List comprehension: `[espressione for valore in lista if condizione]`, come `SELECT` / `FROM` / `WHERE`.
