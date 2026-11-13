# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 0 – Soluzioni
# MAGIC
# MAGIC Soluzioni commentate degli esercizi del Capitolo 0 (testo completo nell'Appendice A).
# MAGIC Si esegue una cella alla volta.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Un notebook ordinato
# MAGIC Contenuto della prima cella di `L00_Primo_Notebook` (la data è un esempio):
# MAGIC
# MAGIC ```
# MAGIC %md
# MAGIC # L00 – Primo notebook
# MAGIC 13/11/2026
# MAGIC ```
# MAGIC Il comando `%md` deve essere sulla prima riga; `#` seguito da uno spazio crea il titolo di primo livello.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Esplorare una tabella nel Catalog Explorer
# MAGIC Catalog → samples → wanderbricks → properties, pagina delle colonne. La verifica in SQL:

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC Il numero di colonne è quello delle righe dell'output (una riga per colonna); `base_price` ha tipo `float`.
# MAGIC
# MAGIC ## Esercizio 3 ★ – Python come calcolatrice

# COMMAND ----------

# Numero totale di prenotazioni 2024 delle tre strutture guida
6 + 7 + 4

# COMMAND ----------

# Ricavo totale 2024 delle tre strutture guida
3966.21 + 5139.59 + 2896.92

# COMMAND ----------

# MAGIC %md
# MAGIC Due celle perché l'output automatico di una cella Python mostra solo il valore dell'ultima riga.
# MAGIC
# MAGIC ## Esercizio 4 ★★ – Contare destinazioni e paesi

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS destinations_count,
# MAGIC        COUNT(DISTINCT country) AS countries_count
# MAGIC FROM samples.wanderbricks.destinations

# COMMAND ----------

# MAGIC %md
# MAGIC Atteso: 42 e 18.
# MAGIC
# MAGIC ## Esercizio 5 ★★ – Una cella, due righe

# COMMAND ----------

# Entrambe le righe vengono eseguite, ma l'output mostra solo l'ultima
2 / 4 * 100
1 / 7 * 100

# COMMAND ----------

# Amalfi
2 / 4 * 100

# COMMAND ----------

# Sardinia
1 / 7 * 100

# COMMAND ----------

# MAGIC %md
# MAGIC `50.0` ha il decimale perché la divisione restituisce sempre un numero con decimali; `14.285714285714285` non è arrotondato
# MAGIC (l'arrotondamento si vedrà nel Capitolo 1). Solo Amalfi (50%) supera la soglia del 30%.
# MAGIC
# MAGIC ## Esercizio 6 ★★ – Il primo grafico

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_type, COUNT(*) AS properties_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY property_type
# MAGIC ORDER BY properties_count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC Dopo l'esecuzione: **+ → Visualization**, tipo **Bar**, asse X `property_type`, asse Y `properties_count`, **Save**.
# MAGIC Somma delle barre: 9264 + 7068 + 1646 + 185 = 18163, il numero di righe di `properties`.
# MAGIC
# MAGIC ## Esercizio 7 ★★★ – Il profilo della copia di lavoro

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*)                                                AS rows_count,
# MAGIC   COUNT(DISTINCT booking_id)                              AS distinct_bookings,
# MAGIC   SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END)   AS missing_amount,
# MAGIC   SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)       AS negative_amount,
# MAGIC   SUM(CASE WHEN check_out < check_in THEN 1 ELSE 0 END)   AS swapped_dates
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT change_type, COUNT(*) AS changes_count
# MAGIC FROM workspace.libro_python.b_bookings_modifiche
# MAGIC GROUP BY change_type
# MAGIC ORDER BY change_type

# COMMAND ----------

# MAGIC %md
# MAGIC Atteso: 72287 / 72247 / 30 / 13 / 8 e, per tipo, date_invertite 8, importo_negativo 12, importo_nullo 30, riga_duplicata 40.
# MAGIC
# MAGIC Gli importi negativi sono 13 in `b_bookings` ma 12 nelle modifiche: una prenotazione ha un importo negativo già nei dati originali
# MAGIC di `samples.wanderbricks.bookings`, quindi non è una modifica. Le 40 righe duplicate spiegano la differenza tra righe (72287) e prenotazioni distinte (72247).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC **8a** – `SyntaxError: invalid syntax`: manca `%sql`, la query è letta come Python.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT destination, country FROM samples.wanderbricks.destinations

# COMMAND ----------

# MAGIC %md
# MAGIC **8b** – `TABLE_OR_VIEW_NOT_FOUND`: il messaggio mostra `samples`.`wanderbrick`.`properties`; lo schema si chiama `wanderbricks`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC **8c** – `UNRESOLVED_COLUMN`: la colonna `amount` non esiste in `bookings`; il messaggio suggerisce `total_amount`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT booking_id, total_amount
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC LIMIT 5
