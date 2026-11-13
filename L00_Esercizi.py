# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 0 – Esercizi
# MAGIC
# MAGIC Prerequisiti: notebook collegato a **Serverless**; `L00_Prepara_Dati` già eseguito (esercizio 7).
# MAGIC Difficoltà: ★ base, ★★ intermedio, ★★★ sfida. Soluzioni: Appendice A e notebook `L00_Soluzioni`.
# MAGIC
# MAGIC Si esegue una cella alla volta (l'esercizio 8 contiene errori voluti).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Un notebook ordinato
# MAGIC Nella cartella `Libro_Python` creare un nuovo notebook `L00_Primo_Notebook` (linguaggio predefinito Python).
# MAGIC La prima cella deve essere una cella Markdown con il titolo di primo livello `L00 – Primo notebook` e, sotto, una riga con la data di oggi.
# MAGIC
# MAGIC **Risultato atteso**: eseguendo la cella compare il titolo formattato e il codice `%md` non è più visibile.
# MAGIC
# MAGIC (Questo esercizio si svolge nel nuovo notebook, non qui.)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Esplorare una tabella nel Catalog Explorer
# MAGIC Usando solo il Catalog Explorer: quante colonne ha `samples.wanderbricks.properties`? Di che tipo è `base_price`?
# MAGIC Verificare poi con `DESCRIBE TABLE` nella cella sotto.
# MAGIC
# MAGIC **Risultato atteso**: stesso elenco di colonne nei due strumenti; `base_price` è un numero con decimali (`float`).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Scrivere qui la query DESCRIBE TABLE


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Python come calcolatrice
# MAGIC Le tre strutture guida hanno avuto nel 2024 6, 7 e 4 prenotazioni, con ricavi 3966.21, 5139.59 e 2896.92.
# MAGIC In due celle Python separate calcolare il numero totale di prenotazioni e il ricavo totale.
# MAGIC
# MAGIC **Risultato atteso**: `17` e `12002.72`.

# COMMAND ----------

# Numero totale di prenotazioni


# COMMAND ----------

# Ricavo totale


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Contare destinazioni e paesi
# MAGIC Con una sola query su `samples.wanderbricks.destinations` calcolare il numero di destinazioni e il numero di paesi distinti.
# MAGIC
# MAGIC **Risultato atteso**: 42 destinazioni, 18 paesi.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Scrivere qui la query


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Una cella, due righe
# MAGIC Nella cella sotto scrivere, su due righe, il tasso di cancellazione (× 100) della Beach House in Amalfi (2 su 4) e del Bungalow in Sardinia (1 su 7).
# MAGIC Eseguire e spiegare perché compare un solo risultato. Poi spostare i due calcoli in due celle distinte.
# MAGIC
# MAGIC **Risultato atteso**: nella cella unica solo `14.285714285714285`; nelle due celle `50.0` e `14.285714285714285`. Rispetto alla soglia del 30% solo Amalfi la supera.

# COMMAND ----------

# Due calcoli nella stessa cella


# COMMAND ----------

# Amalfi


# COMMAND ----------

# Sardinia


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Il primo grafico
# MAGIC Contare le strutture per `property_type` in `samples.wanderbricks.properties` e trasformare il risultato in un grafico a barre con **+ → Visualization**.
# MAGIC
# MAGIC **Risultato atteso**: Urban Year-Round 9264, Summer Getaway 7068, Historical Place 1646, Ski Resort 185 (totale 18163).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Scrivere qui la query


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Il profilo della copia di lavoro
# MAGIC 1. Con una sola query su `workspace.libro_python.b_bookings` calcolare: righe, `booking_id` distinti, importi mancanti, importi negativi, prenotazioni con `check_out` precedente a `check_in`.
# MAGIC 2. Con una seconda query contare le righe di `workspace.libro_python.b_bookings_modifiche` per `change_type`.
# MAGIC 3. Spiegare perché gli importi negativi non coincidono nelle due query.
# MAGIC
# MAGIC **Risultato atteso**: 72287 / 72247 / 30 / 13 / 8; modifiche: importo_nullo 30, importo_negativo 12, date_invertite 8, riga_duplicata 40.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 1: profilo di b_bookings


# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 2: modifiche per tipo


# COMMAND ----------

# MAGIC %md
# MAGIC Spiegazione (punto 3):
# MAGIC
# MAGIC ...

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Ognuna delle tre celle seguenti produce un errore. Eseguirle una per una, annotare il nome dell'errore e la parte di codice indicata, e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso**: le celle corrette restituiscono 42 righe, il valore 18163 e cinque prenotazioni.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
SELECT destination, country FROM samples.wanderbricks.destinations

# COMMAND ----------

# Correzione 8a (nome dell'errore: ...)


# COMMAND ----------

# MAGIC %sql
# MAGIC -- ERRORE VOLUTO – cella 8b
# MAGIC SELECT COUNT(*) FROM samples.wanderbrick.properties

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione 8b (nome dell'errore: ...)


# COMMAND ----------

# MAGIC %sql
# MAGIC -- ERRORE VOLUTO – cella 8c
# MAGIC SELECT booking_id, amount
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC LIMIT 5

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione 8c (nome dell'errore: ...)
