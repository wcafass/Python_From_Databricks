# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 0 – Orientarsi in Databricks
# MAGIC
# MAGIC Notebook del Capitolo 0 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Eseguire celle SQL, Markdown e Python nello stesso notebook
# MAGIC - Indicare le tabelle con il nome a tre livelli `catalogo.schema.tabella`
# MAGIC - Leggere l'output di una cella e la prima riga di un messaggio di errore
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Notebook collegato al compute **Serverless** (selettore in alto a destra)
# MAGIC - Notebook `L00_Prepara_Dati` già eseguito con Run all (sezione 0.7), necessario per le celle su `b_bookings`
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: la sezione 0.9 contiene errori voluti e Run all si fermerebbe al primo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0.3 Notebook e celle
# MAGIC Una cella che inizia con `%sql` contiene una query SQL; l'output è una griglia, come in un client SQL.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS bookings_count
# MAGIC FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: **72247**.
# MAGIC
# MAGIC Questa cella è una cella Markdown (`%md`): eseguendola il codice scompare e resta il testo formattato.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0.4 Dove stanno i dati: catalogo, schema, tabella
# MAGIC Nome a tre livelli: `samples` (catalogo) . `wanderbricks` (schema) . `bookings` (tabella).
# MAGIC La stessa informazione della pagina delle colonne del Catalog Explorer si ottiene con `DESCRIBE TABLE`.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: 10 colonne (booking_id, user_id, property_id, check_in, check_out, guests_count, total_amount, status, created_at, updated_at).
# MAGIC
# MAGIC ## 0.5 Eseguire, interrompere, leggere l'output
# MAGIC Si provino i tre modi di eseguire una cella: pulsante, Ctrl/Cmd+Invio (resta sulla cella), Maiusc+Invio (passa alla successiva).
# MAGIC Durante un'esecuzione lunga, il pulsante di arresto della cella o il comando **Interrupt** in alto fermano il calcolo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0.6 Python nella stessa pagina: la calcolatrice e l'ultima riga
# MAGIC **Ponte SQL**: una SELECT senza FROM calcola un'espressione; in Python l'espressione si scrive da sola nella cella.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 3966.21 + 5139.59 AS total_revenue

# COMMAND ----------

3966.21 + 5139.59

# COMMAND ----------

# Tasso di cancellazione 2024 della Beach House in Amalfi: 2 cancellate su 4 prenotazioni
2 / 4 * 100

# COMMAND ----------

"Summer Getaway"

# COMMAND ----------

# MAGIC %md
# MAGIC **Solo l'ultima riga**: la cella seguente esegue entrambe le righe, ma l'output mostra solo il valore dell'ultima (1173.38).

# COMMAND ----------

3966.21 + 5139.59
5139.59 - 3966.21

# COMMAND ----------

# Ricavo 2024 delle tre strutture guida
3966.21 + 5139.59 + 2896.92

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0.7 Preparare i dati del libro
# MAGIC Prima di proseguire, il notebook `L00_Prepara_Dati` deve essere stato eseguito **una volta** con Run all.
# MAGIC La cella seguente controlla che le due tabelle create esistano nello schema di lavoro.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN workspace.libro_python

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: almeno le tabelle `b_bookings` e `b_bookings_modifiche`. Se la cella dà errore, si esegua `L00_Prepara_Dati`.
# MAGIC
# MAGIC ## 0.8 Prima esplorazione dei dati

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT status, COUNT(*) AS bookings_count
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC GROUP BY status
# MAGIC ORDER BY bookings_count DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT MIN(check_in) AS first_check_in,
# MAGIC        MAX(check_in) AS last_check_in
# MAGIC FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_type, COUNT(*) AS properties_count
# MAGIC FROM samples.wanderbricks.properties
# MAGIC GROUP BY property_type
# MAGIC ORDER BY properties_count DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT destination_id, destination, country
# MAGIC FROM samples.wanderbricks.destinations
# MAGIC WHERE country = 'Italy'
# MAGIC ORDER BY destination_id

# COMMAND ----------

# MAGIC %md
# MAGIC **Originale e copia di lavoro**: `b_bookings` ha 40 righe in più (le righe duplicate) ma lo stesso numero di prenotazioni distinte.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS rows_count,
# MAGIC        COUNT(DISTINCT booking_id) AS distinct_bookings
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) AS missing_amount,
# MAGIC   SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)     AS negative_amount
# MAGIC FROM workspace.libro_python.b_bookings

# COMMAND ----------

# MAGIC %md
# MAGIC **Un primo grafico**: dopo l'esecuzione della cella seguente, sopra i risultati si sceglie **+ → Visualization**, tipo **Bar**, asse X `check_in_month`, asse Y `bookings_count`, poi **Save**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT month(check_in) AS check_in_month,
# MAGIC        COUNT(*) AS bookings_count
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE year(check_in) = 2024
# MAGIC GROUP BY month(check_in)
# MAGIC ORDER BY check_in_month

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0.9 Leggere un messaggio di errore
# MAGIC Le celle seguenti vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si legge il nome dell'errore e la frase che lo descrive;
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori** e mostrare il risultato.
# MAGIC
# MAGIC Risultati attesi delle correzioni: griglia con la sola colonna `status` (72.247 righe in tutto, ne compaiono le prime); il valore 72247; griglia con `property_id`, `title`, `base_price`.

# COMMAND ----------

# ERRORE VOLUTO – query in una cella Python (manca %sql)
SELECT status FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione: %sql sulla prima riga
# MAGIC SELECT status FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ERRORE VOLUTO – tabella inesistente (booking invece di bookings)
# MAGIC SELECT COUNT(*) FROM samples.wanderbricks.booking

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione
# MAGIC SELECT COUNT(*) FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ERRORE VOLUTO – colonna inesistente (price invece di base_price)
# MAGIC SELECT property_id, title, price
# MAGIC FROM samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione
# MAGIC SELECT property_id, title, base_price
# MAGIC FROM samples.wanderbricks.properties

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - Notebook = sequenza di celle; linguaggio predefinito Python; `%sql` e `%md` sulla prima riga cambiano il linguaggio della cella.
# MAGIC - Il compute Serverless esegue le celle; dopo l'inattività la sessione si chiude: gli output restano, la memoria del compute no.
# MAGIC - Tabelle con il nome a tre livelli; `samples` in sola lettura, il libro scrive solo in `workspace.libro_python`.
# MAGIC - Output di una cella Python = valore dell'ultima riga.
# MAGIC - Run all si ferma al primo errore: i notebook dei capitoli si eseguono una cella alla volta.
# MAGIC - Davanti a un errore: prima il nome dell'errore, poi la frase che lo descrive.
