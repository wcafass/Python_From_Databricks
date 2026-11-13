# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 3 – Collezioni: liste e dizionari
# MAGIC
# MAGIC Notebook del Capitolo 3 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Creare liste, leggerne i valori con gli indici e prenderne una parte con lo slicing
# MAGIC - Modificare una lista e aggiungere valori con `append()` (il primo metodo)
# MAGIC - Usare `len()`, `sum()`, `min()`, `max()` e l'operatore `in`
# MAGIC - Rappresentare una riga con un dizionario e usare un dizionario come tabella di decodifica
# MAGIC - Riconoscere tuple e set; copiare una lista con `copy()`
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–2; notebook collegato al compute **Serverless**
# MAGIC - Le celle `%sql` leggono solo `samples.wanderbricks`
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: la sezione 3.12 contiene errori voluti e silenziosi.
# MAGIC Si esegue per prima la **cella di preparazione**. Le liste e i dizionari si creano nelle sezioni: ogni sezione crea le collezioni che usa.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione

# COMMAND ----------

# Cella di preparazione: costanti del libro
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.1 Le liste
# MAGIC Una lista è una sequenza ordinata di valori tra parentesi quadre. Risultati attesi: `[284.97, 213.91, 236.95]` e `<class 'list'>`.

# COMMAND ----------

base_prices = [284.97, 213.91, 236.95]
print(base_prices)
print(type(base_prices))

# COMMAND ----------

# MAGIC %md
# MAGIC Liste di testi: l'ordine resta quello scritto, le ripetizioni sono ammesse (`"Summer Getaway"` due volte).

# COMMAND ----------

property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
property_types = ["Historical Place", "Summer Getaway", "Summer Getaway"]
print(property_titles)
print(property_types)

# COMMAND ----------

# MAGIC %md
# MAGIC Lista vuota e lista con un valore mancante (`None`). Risultati attesi: `[]` e `[3.2, None, 3.0]`.

# COMMAND ----------

flagged_properties = []
print(flagged_properties)

# COMMAND ----------

ratings_with_gap = [3.2, None, 3.0]
print(ratings_with_gap)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: una colonna del risultato è una lista. Risultato atteso: pending 31575, confirmed 17948, cancelled 15285, completed 7439.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status, COUNT(*) AS bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC GROUP BY status
# MAGIC ORDER BY bookings DESC

# COMMAND ----------

status_names = ["pending", "confirmed", "cancelled", "completed"]
status_counts = [31575, 17948, 15285, 7439]

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.2 Gli indici
# MAGIC Il primo valore ha indice 0. Risultati attesi: `pending`, `confirmed`, `completed`.

# COMMAND ----------

status_names = ["pending", "confirmed", "cancelled", "completed"]
print(status_names[0])
print(status_names[1])
print(status_names[3])

# COMMAND ----------

# MAGIC %md
# MAGIC Indici negativi: `-1` è l'ultimo valore. Risultati attesi: `completed`, `cancelled`.

# COMMAND ----------

print(status_names[-1])
print(status_names[-2])

# COMMAND ----------

# MAGIC %md
# MAGIC Due liste allineate, lette nella stessa posizione. Risultato atteso: `cancelled: 15285 prenotazioni`.

# COMMAND ----------

status_counts = [31575, 17948, 15285, 7439]
print(f"{status_names[2]}: {status_counts[2]} prenotazioni")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.3 Lo slicing
# MAGIC `[inizio:fine]`: l'inizio è incluso, la fine è esclusa. Risultati attesi: `['confirmed', 'cancelled']` e `[31575, 17948, 15285]`.

# COMMAND ----------

print(status_names[1:3])
print(status_counts[0:3])

# COMMAND ----------

# MAGIC %md
# MAGIC Inizio o fine omessi: `[:3]` come `LIMIT 3`, `[2:]` fino alla fine, `[-2:]` gli ultimi due.

# COMMAND ----------

print(status_counts[:3])
print(status_names[2:])
print(status_names[-2:])

# COMMAND ----------

# MAGIC %md
# MAGIC Lo slicing oltre i limiti non dà errori. Risultati attesi: la lista intera e `[]`.

# COMMAND ----------

print(status_names[:10])
print(status_names[5:])

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `LIMIT 3` restituisce gli stessi stati di `status_names[:3]`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status, COUNT(*) AS bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC GROUP BY status
# MAGIC ORDER BY bookings DESC
# MAGIC LIMIT 3

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.4 Modificare una lista: il primo metodo
# MAGIC Sostituire un valore per posizione. Risultato atteso: `[284.97, 213.91, 249.0]`.

# COMMAND ----------

base_prices = [284.97, 213.91, 236.95]
base_prices[2] = 249.0
print(base_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC **`append()`**: il primo metodo (valore, punto, nome, parentesi). Aggiunge un valore in fondo e si scrive su una riga a sé. Risultati attesi: `['Beach House in Amalfi']` e `1`.

# COMMAND ----------

flagged_properties = []
amalfi_rate = 2 / 4 * 100
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    flagged_properties.append("Beach House in Amalfi")
print(flagged_properties)
print(len(flagged_properties))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.5 Contare, sommare, trovare minimo e massimo
# MAGIC `len()`, `sum()`, `min()`, `max()`. Risultati attesi: `3`, `17`, `4`, `7`.

# COMMAND ----------

bookings_2024 = [6, 7, 4]
print(len(bookings_2024))
print(sum(bookings_2024))
print(min(bookings_2024))
print(max(bookings_2024))

# COMMAND ----------

# MAGIC %md
# MAGIC La media è `sum() / len()`. Risultati attesi: `5.666666666666667` e `5.7`.

# COMMAND ----------

average_bookings = sum(bookings_2024) / len(bookings_2024)
print(average_bookings)
print(f"Prenotazioni medie per struttura: {average_bookings:.1f}")

# COMMAND ----------

# MAGIC %md
# MAGIC Liste di `float`: i risultati si mostrano con due decimali. Risultati attesi: `735.83`, `245.28`, `213.91`, `284.97`.

# COMMAND ----------

base_prices = [284.97, 213.91, 236.95]
total_price = sum(base_prices)
average_price = sum(base_prices) / len(base_prices)
print(f"Somma: {total_price:.2f}")
print(f"Media: {average_price:.2f}")
print(f"Minimo: {min(base_prices)} - massimo: {max(base_prices)}")

# COMMAND ----------

# MAGIC %md
# MAGIC Totale delle prenotazioni e quota delle cancellate. Risultati attesi: `72247` e `21.2%`.

# COMMAND ----------

status_counts = [31575, 17948, 15285, 7439]
total_bookings = sum(status_counts)
cancelled_share = status_counts[2] / total_bookings * 100
print(total_bookings)
print(f"Quota di prenotazioni cancellate: {cancelled_share:.1f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le stesse aggregazioni sulle tre strutture guida. Risultato atteso: `3`, `735.83`, `213.91`, `284.97`, `245.28`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)                 AS property_count,
# MAGIC        ROUND(SUM(base_price), 2) AS total_price,
# MAGIC        MIN(base_price)           AS min_price,
# MAGIC        MAX(base_price)           AS max_price,
# MAGIC        ROUND(AVG(base_price), 2) AS average_price
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)

# COMMAND ----------

# MAGIC %md
# MAGIC **Liste con `None`**: `sum()` si ferma con `TypeError` (cella nella sezione 3.12). In SQL le aggregazioni ignorano i `NULL`. Risultato atteso: `99793` e `99317`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)      AS review_count,
# MAGIC        COUNT(rating) AS rating_count
# MAGIC FROM samples.wanderbricks.reviews

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.6 L'operatore in
# MAGIC `in` / `not in` controllano se un valore è in una lista, come `IN` / `NOT IN`. Risultati attesi: `True`, `False`, `True`.

# COMMAND ----------

active_statuses = ["confirmed", "completed"]
status = "completed"
print(status in active_statuses)
print("pending" in active_statuses)
print("pending" not in active_statuses)

# COMMAND ----------

# MAGIC %md
# MAGIC `in` dopo un `if`. Risultato atteso: `16225 è una struttura guida`.

# COMMAND ----------

guide_property_ids = [11670, 16317, 16225]
property_id = 16225
if property_id in guide_property_ids:
    print(f"{property_id} è una struttura guida")

# COMMAND ----------

# MAGIC %md
# MAGIC Tra due testi `in` cerca il primo dentro il secondo, come `LIKE '%Amalfi%'`. Risultati attesi: `True`, `False`.

# COMMAND ----------

property_title = "Beach House in Amalfi"
print("Amalfi" in property_title)
print("Rome" in property_title)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: prenotazioni attive con `IN`. Risultato atteso: `25387`, lo stesso della cella Python successiva.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS active_bookings
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE status IN ('confirmed', 'completed')

# COMMAND ----------

status_counts = [31575, 17948, 15285, 7439]
print(status_counts[1] + status_counts[3])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.7 I dizionari
# MAGIC Un dizionario associa chiavi e valori: una riga della tabella `properties`, con i nomi delle colonne come chiavi.

# COMMAND ----------

amalfi_property = {
    "property_id": 16225,
    "title": "Beach House in Amalfi",
    "destination_id": 1100,
    "property_type": "Summer Getaway",
    "base_price": 236.95,
}
print(amalfi_property)
print(type(amalfi_property))

# COMMAND ----------

# MAGIC %md
# MAGIC Lettura per chiave; nelle f-string le chiavi tra virgolette singole. Una chiave inesistente produce `KeyError` (sezione 3.12).

# COMMAND ----------

print(amalfi_property["title"])
print(amalfi_property["base_price"])
print(f"{amalfi_property['title']}: prezzo base {amalfi_property['base_price']}")

# COMMAND ----------

# MAGIC %md
# MAGIC `get()` restituisce `None` se la chiave manca. Risultati attesi: `236.95` e `None`.

# COMMAND ----------

print(amalfi_property.get("base_price"))
print(amalfi_property.get("max_guests"))

# COMMAND ----------

# MAGIC %md
# MAGIC La stessa scrittura aggiorna una chiave esistente e aggiunge una chiave nuova. Risultati attesi: `249.0` e il dizionario con `bookings_2024`.

# COMMAND ----------

amalfi_property["base_price"] = 249.0
amalfi_property["bookings_2024"] = 4
print(amalfi_property["base_price"])
print(amalfi_property)

# COMMAND ----------

# MAGIC %md
# MAGIC `in` controlla le chiavi; `len()` conta le coppie. Risultati attesi: `True`, `False`, `6`, poi `Voto non disponibile`.

# COMMAND ----------

print("base_price" in amalfi_property)
print("rating" in amalfi_property)
print(len(amalfi_property))

# COMMAND ----------

if "rating" in amalfi_property:
    print(amalfi_property["rating"])
else:
    print("Voto non disponibile")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: la riga corrispondente al dizionario (con il prezzo base originale, 236.95).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id, title, destination_id, property_type, base_price
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id = 16225

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.8 Il dizionario come tabella di decodifica
# MAGIC Codice → nome, come un `JOIN` con `destinations`. Si esegue prima la cella del dizionario `amalfi_property` (sezione 3.7). Risultati attesi: `Amalfi` due volte.

# COMMAND ----------

destination_names = {
    1100: "Amalfi",
    2300: "Florence",
    3900: "Rome",
    4200: "Sardinia",
}
print(destination_names[1100])
print(destination_names[amalfi_property["destination_id"]])

# COMMAND ----------

# MAGIC %md
# MAGIC Il tipo della chiave conta: `"1100"` non è `1100`. Risultati attesi: `None` e `Amalfi`.

# COMMAND ----------

print(destination_names.get("1100"))
print(destination_names.get(int("1100")))

# COMMAND ----------

# MAGIC %md
# MAGIC Un codice assente con `get()`. Risultato atteso: `Destinazione non trovata`.

# COMMAND ----------

unknown_destination = destination_names.get(9999)
if unknown_destination is None:
    print("Destinazione non trovata")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le destinazioni italiane. Risultato atteso: 1100 Amalfi, 2300 Florence, 3900 Rome, 4200 Sardinia.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT destination_id, destination
# MAGIC FROM samples.wanderbricks.destinations
# MAGIC WHERE country = 'Italy'
# MAGIC ORDER BY destination_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.9 Le liste di dizionari
# MAGIC Una lista di dizionari è una piccola tabella: ogni dizionario è una riga. Risultati attesi: `3` e la riga di Roma.

# COMMAND ----------

guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]
print(len(guide_properties))
print(guide_properties[0])

# COMMAND ----------

# MAGIC %md
# MAGIC Doppio accesso: prima la riga, poi la chiave. Risultati attesi: `Beach House in Amalfi` e `2`.

# COMMAND ----------

print(guide_properties[2]["title"])
print(guide_properties[-1]["cancelled_2024"])

# COMMAND ----------

# MAGIC %md
# MAGIC Una nuova chiave in una riga, come una nuova colonna. `amalfi_row` e `guide_properties[2]` sono lo stesso dizionario (sezione 3.11). Risultati attesi: `Beach House in Amalfi: 50.0%` e `50.0`.

# COMMAND ----------

amalfi_row = guide_properties[2]
amalfi_row["cancellation_rate"] = amalfi_row["cancelled_2024"] / amalfi_row["bookings_2024"] * 100
print(f"{amalfi_row['title']}: {amalfi_row['cancellation_rate']:.1f}%")
print(guide_properties[2]["cancellation_rate"])

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le stesse tre righe ricalcolate da `bookings`. Risultato atteso: 11670 6 0 3966.21; 16225 4 2 2896.92; 16317 7 1 5139.59.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id,
# MAGIC        COUNT(*)                                              AS bookings_2024,
# MAGIC        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_2024,
# MAGIC        ROUND(SUM(total_amount), 2)                           AS revenue_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id IN (11670, 16317, 16225)
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'
# MAGIC GROUP BY property_id
# MAGIC ORDER BY property_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.10 Tuple e set
# MAGIC **Tupla**: sequenza tra parentesi tonde, non modificabile (errore nella sezione 3.12). Risultati attesi: `(213.91, 284.97)`, `213.91`, `<class 'tuple'>`.

# COMMAND ----------

price_range = (213.91, 284.97)
print(price_range)
print(price_range[0])
print(type(price_range))

# COMMAND ----------

# MAGIC %md
# MAGIC Un decimale scritto con la virgola crea una tupla. Risultati attesi: `(284, 97)` e `<class 'tuple'>`.

# COMMAND ----------

price_with_comma = 284,97
print(price_with_comma)
print(type(price_with_comma))

# COMMAND ----------

# MAGIC %md
# MAGIC **Set**: valori senza ripetizioni e senza ordine, come `DISTINCT`. Risultati attesi: i due tipi (in un ordine qualunque) e `2`.

# COMMAND ----------

property_types = ["Historical Place", "Summer Getaway", "Summer Getaway"]
distinct_types = set(property_types)
print(distinct_types)
print(len(distinct_types))

# COMMAND ----------

# MAGIC %md
# MAGIC `{}` è un dizionario vuoto; il set vuoto è `set()`. Risultati attesi: `<class 'dict'>` e `<class 'set'>`.

# COMMAND ----------

print(type({}))
print(type(set()))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `DISTINCT` sui tipi delle strutture guida (2 righe) e `COUNT(DISTINCT)` sull'intera tabella (`4`).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT property_type
# MAGIC FROM samples.wanderbricks.properties
# MAGIC WHERE property_id IN (11670, 16317, 16225)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(DISTINCT property_type) AS type_count
# MAGIC FROM samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.11 Copiare una lista
# MAGIC `new_prices = base_prices` non copia: i due nomi indicano la stessa lista. Risultato atteso: due righe uguali, con `249.0`.

# COMMAND ----------

base_prices = [284.97, 213.91, 236.95]
new_prices = base_prices
new_prices[2] = 249.0
print(new_prices)
print(base_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC `copy()` crea una lista indipendente. Risultati attesi: `[284.97, 213.91, 249.0]` e `[284.97, 213.91, 236.95]`.

# COMMAND ----------

base_prices = [284.97, 213.91, 236.95]
new_prices = base_prices.copy()
new_prices[2] = 249.0
print(new_prices)
print(base_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.12 Leggere gli errori del capitolo
# MAGIC Le celle seguenti vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si legge il nome dell'errore e la descrizione;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori**.
# MAGIC
# MAGIC Risultati attesi delle correzioni, nell'ordine: `[284.97, 213.91, 236.95]`; `completed`; `236.95` e `None`; `6.2`; `(213.91, 300.0)` e `[213.91, 300.0]`; `Stato più frequente: pending`; `[31575, 17948, 15285]`; `['Beach House in Amalfi']`; `[284.97, 213.91, 236.95]`.

# COMMAND ----------

# ERRORE VOLUTO – manca una virgola tra due valori della lista
base_prices = [284.97 213.91, 236.95]

# COMMAND ----------

# Correzione: una virgola tra ogni coppia di valori
base_prices = [284.97, 213.91, 236.95]
print(base_prices)

# COMMAND ----------

# ERRORE VOLUTO – la lista ha quattro valori: l'ultimo indice è 3
status_names = ["pending", "confirmed", "cancelled", "completed"]
print(status_names[4])

# COMMAND ----------

# Correzione: l'ultimo valore ha indice -1 (oppure 3)
status_names = ["pending", "confirmed", "cancelled", "completed"]
print(status_names[-1])

# COMMAND ----------

# ERRORE VOLUTO – la chiave si chiama base_price, non price
amalfi_property = {"property_id": 16225, "title": "Beach House in Amalfi", "base_price": 236.95}
print(amalfi_property["price"])

# COMMAND ----------

# Correzione: la chiave esatta; get() se la chiave può mancare
amalfi_property = {"property_id": 16225, "title": "Beach House in Amalfi", "base_price": 236.95}
print(amalfi_property["base_price"])
print(amalfi_property.get("price"))

# COMMAND ----------

# ERRORE VOLUTO – sum() non può sommare un valore None
ratings_with_gap = [3.2, None, 3.0]
print(sum(ratings_with_gap))

# COMMAND ----------

# Correzione: si sommano solo i valori presenti (nel Capitolo 4 per liste di qualunque lunghezza)
ratings_with_gap = [3.2, None, 3.0]
print(ratings_with_gap[0] + ratings_with_gap[2])

# COMMAND ----------

# ERRORE VOLUTO – una tupla non si può modificare
price_range = (213.91, 284.97)
price_range[1] = 300.0

# COMMAND ----------

# Correzione: una nuova tupla, oppure una lista che si può modificare
price_range = (213.91, 300.0)
print(price_range)
price_range = [213.91, 284.97]
price_range[1] = 300.0
print(price_range)

# COMMAND ----------

# ERRORE SILENZIOSO – l'indice 1 è il secondo valore, non il primo
status_names = ["pending", "confirmed", "cancelled", "completed"]
print(f"Stato più frequente: {status_names[1]}")

# COMMAND ----------

# Correzione: il primo valore ha indice 0
status_names = ["pending", "confirmed", "cancelled", "completed"]
print(f"Stato più frequente: {status_names[0]}")

# COMMAND ----------

# ERRORE SILENZIOSO – [0:2] prende due valori, non tre
status_counts = [31575, 17948, 15285, 7439]
top_three = status_counts[0:2]
print(top_three)

# COMMAND ----------

# Correzione: la fine è esclusa, per i primi tre si scrive [:3]
status_counts = [31575, 17948, 15285, 7439]
top_three = status_counts[:3]
print(top_three)

# COMMAND ----------

# ERRORE SILENZIOSO – append() modifica la lista e restituisce None
flagged_properties = []
flagged_properties = flagged_properties.append("Beach House in Amalfi")
print(flagged_properties)

# COMMAND ----------

# Correzione: append() su una riga a sé, senza assegnazione
flagged_properties = []
flagged_properties.append("Beach House in Amalfi")
print(flagged_properties)

# COMMAND ----------

# ERRORE SILENZIOSO – new_prices è un secondo nome per la stessa lista
base_prices = [284.97, 213.91, 236.95]
new_prices = base_prices
new_prices[0] = 299.0
print(base_prices)

# COMMAND ----------

# Correzione: copy() crea una lista indipendente
base_prices = [284.97, 213.91, 236.95]
new_prices = base_prices.copy()
new_prices[0] = 299.0
print(base_prices)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - Lista: `[...]`, ordinata, con ripetizioni; indice da 0, `-1` per l'ultimo; `IndexError` fuori dai limiti.
# MAGIC - Slicing `[inizio:fine]`: fine esclusa; `[:3]` come `LIMIT 3`; nessun errore oltre i limiti.
# MAGIC - `lista[i] = valore` sostituisce; `append()` (metodo) aggiunge in fondo, su una riga a sé.
# MAGIC - `len`, `sum`, `min`, `max` come `COUNT(*)`, `SUM`, `MIN`, `MAX`; media = `sum / len`; con `None` → `TypeError` (SQL ignora i `NULL`).
# MAGIC - `in` / `not in` come `IN` / `NOT IN`; tra testi come `LIKE '%...%'`.
# MAGIC - Dizionario `{chiave: valore}` = una riga; `d[chiave]` (`KeyError`) o `d.get(chiave)` (`None`); la stessa scrittura aggiorna o aggiunge; `in` controlla le chiavi.
# MAGIC - Dizionario di decodifica come `JOIN`; il tipo della chiave conta.
# MAGIC - Lista di dizionari = piccola tabella: `lista[riga][chiave]`.
# MAGIC - Tupla `(...)` non modificabile (attenzione a `284,97`); set senza ripetizioni né ordine, come `DISTINCT`; `{}` è un dizionario.
# MAGIC - `b = a` non copia; `copy()` sì.
