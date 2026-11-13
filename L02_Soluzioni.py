# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 2 – Soluzioni
# MAGIC
# MAGIC Soluzioni commentate degli esercizi di `L02_Esercizi` (le stesse dell'Appendice A).
# MAGIC Si esegue per prima la cella di preparazione, poi una cella alla volta: l'esercizio 8 contiene errori voluti.

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

# COMMAND ----------

total_bookings = rome_bookings + sardinia_bookings + amalfi_bookings
total_cancelled = rome_cancelled + sardinia_cancelled + amalfi_cancelled
total_revenue = rome_revenue + sardinia_revenue + amalfi_revenue

# Il ricavo medio si calcola sui totali
revenue_per_booking = total_revenue / total_bookings

# Le parentesi sono indispensabili: senza, si dividerebbe per 3 solo l'ultimo prezzo
average_base_price = (284.97 + 213.91 + 236.95) / 3

print(f"Prenotazioni: {total_bookings} - cancellate: {total_cancelled}")
print(f"Ricavo totale: {total_revenue:.2f}")
print(f"Ricavo medio per prenotazione: {revenue_per_booking:.2f}")
print(f"Prezzo base medio: {average_base_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Settimane, ore e minuti

# COMMAND ----------

nights = 9
# // dà le settimane intere, % le notti che avanzano
print(f"{nights} notti: settimane intere {nights // 7}, notti in più {nights % 7}")

nights = 23
print(f"{nights} notti: settimane intere {nights // 7}, notti in più {nights % 7}")

# COMMAND ----------

seconds = 3725
hours = seconds // 3600
# Prima il resto delle ore (le parentesi non servono: % e // hanno la stessa
# precedenza e si eseguono da sinistra a destra, ma le scriviamo per chiarezza)
minutes = (seconds % 3600) // 60
remaining_seconds = seconds % 60
print(f"{seconds} secondi = {hours} h {minutes} min {remaining_seconds} s")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Vero o falso

# COMMAND ----------

print(destination == "Amalfi")              # a) True
print(destination == "AMALFI")              # b) False: maiuscole diverse
print(property_id == "16225")               # c) False: un numero e un testo non sono mai uguali
print(base_price > 200 and base_price < 250) # d) True
print(284.97 * 3 == 854.91)                 # e) False: decimali approssimati
print(0 <= 50.0 <= 100)                     # f) True: confronto concatenato
print(ANALYSIS_YEAR % 4 == 0)               # g) True: resto zero, anno bisestile
print(not (amalfi_bookings > 5))            # h) True: 4 > 5 è falso, not lo rovescia

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Condizioni composte

# COMMAND ----------

booking_status = "confirmed"
total_amount = 1250.0
guests_count = 5

# Con or ogni confronto si scrive per intero
is_active = booking_status == "confirmed" or booking_status == "completed"
is_large = total_amount >= 1000 and guests_count >= 4
needs_check = booking_status == "cancelled" or total_amount < 100
print(f"attiva: {is_active} - grande: {is_large} - da controllare: {needs_check}")

# COMMAND ----------

booking_status = "cancelled"
total_amount = 80.0
guests_count = 2

is_active = booking_status == "confirmed" or booking_status == "completed"
is_large = total_amount >= 1000 and guests_count >= 4
needs_check = booking_status == "cancelled" or total_amount < 100
print(f"attiva: {is_active} - grande: {is_large} - da controllare: {needs_check}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Fasce di prezzo
# MAGIC La cella si esegue quattro volte, cambiando le prime due righe: Roma (284.97), Sardegna (213.91), Amalfi (236.95), struttura di prova (180.0).

# COMMAND ----------

property_title = "Historic Inn in Rome"
base_price = 284.97

# Dalla fascia più alta alla più bassa: vince la prima condizione vera
if base_price >= 250:
    price_band = "alto"
elif base_price >= 200:
    price_band = "medio"
else:
    price_band = "basso"
print(f"{property_title}: {price_band}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: la stessa classificazione con CASE WHEN
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
# MAGIC La cella si esegue sei volte, cambiando la prima riga: `0.0`, `14.3`, `50.0`, `None`, `120.0`, `-5.0`.

# COMMAND ----------

cancellation_rate = 0.0

# Il controllo su None va per primo: gli altri confronti con None darebbero TypeError
if cancellation_rate is None:
    cancellation_status = "dato mancante"
elif cancellation_rate < 0 or cancellation_rate > 100:
    cancellation_status = "valore impossibile"
elif cancellation_rate > CANCELLATION_RATE_THRESHOLD:
    cancellation_status = "critico"
else:
    cancellation_status = "ok"
print(cancellation_rate, cancellation_status)

# Risposta alla domanda: se il controllo su None viene spostato in fondo, con None la
# prima condizione (cancellation_rate < 0) produce
# TypeError: '<' not supported between instances of 'NoneType' and 'int'.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Una scheda da validare
# MAGIC La cella si esegue quattro volte, cambiando le tre righe di testo: (`"4"`, `"2"`, `""`), (`"4"`, `"2"`, `"3.0"`), (`"0"`, `"0"`, `"3.0"`), (`"4"`, `"5"`, `""`).

# COMMAND ----------

property_title = "Beach House in Amalfi"
bookings_text = "4"
cancelled_text = "2"
rating_text = ""

# 1. Conversioni
bookings = int(bookings_text)
cancelled = int(cancelled_text)

# 2. Tasso: si calcola solo se ci sono prenotazioni, altrimenti è un dato mancante
if bookings > 0:
    cancellation_rate = cancelled / bookings * 100
else:
    cancellation_rate = None

# 3. Voto: un testo vuoto significa voto mancante
if rating_text == "":
    rating = None
else:
    rating = float(rating_text)

# 4. Stato del tasso (stessa classificazione dell'esercizio 6)
if cancellation_rate is None:
    cancellation_status = "dato mancante"
elif cancellation_rate < 0 or cancellation_rate > 100:
    cancellation_status = "valore impossibile"
elif cancellation_rate > CANCELLATION_RATE_THRESHOLD:
    cancellation_status = "critico"
else:
    cancellation_status = "ok"

# 5. Testi per il report: "n.d." al posto dei valori mancanti
if cancellation_rate is None:
    rate_label = "n.d."
else:
    rate_label = f"{cancellation_rate:.1f}%"

if rating is None:
    rating_label = "n.d."
else:
    rating_label = f"{rating:.1f}"

print(f"{property_title}: tasso {rate_label} ({cancellation_status}), voto medio {rating_label}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Ogni cella `ERRORE VOLUTO` deve fallire, ogni cella `ERRORE SILENZIOSO` produce un risultato sbagliato; la correzione sotto deve funzionare.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
rome_price = 284.97
if rome_price >= 250
    print("alto")

# COMMAND ----------

# Correzione 8a (SyntaxError: expected ':' – mancano i due punti)
rome_price = 284.97
if rome_price >= 250:
    print("alto")

# COMMAND ----------

# ERRORE VOLUTO – cella 8b
if property_type = "Summer Getaway":
    print("Struttura estiva")

# COMMAND ----------

# Correzione 8b (SyntaxError: invalid syntax. Maybe you meant '==' ... – nella condizione serve ==)
if property_type == "Summer Getaway":
    print("Struttura estiva")

# COMMAND ----------

# ERRORE VOLUTO – cella 8c
amalfi_rate = 50.0
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
print("critico")

# COMMAND ----------

# Correzione 8c (IndentationError: expected an indented block – la riga del blocco va rientrata)
amalfi_rate = 50.0
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print("critico")

# COMMAND ----------

# ERRORE VOLUTO – cella 8d
average_rating = None
if average_rating >= 3.0:
    print("Voto sufficiente")

# COMMAND ----------

# Correzione 8d (TypeError: '>=' not supported between instances of 'NoneType' and 'float')
# Prima il controllo su None; con il voto mancante si stampa un messaggio dedicato
average_rating = None
if average_rating is None:
    print("Voto non disponibile")
elif average_rating >= 3.0:
    print("Voto sufficiente")

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

# Correzione 8e (stampa "attenzione" invece di "critico": la prima condizione vera vince,
# quindi la soglia più alta va controllata per prima)
amalfi_rate = 50.0
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print("critico")
elif amalfi_rate > 15:
    print("attenzione")
else:
    print("ok")

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f
status = "completed"
if status == "cancelled" or "pending":
    print("Da verificare")
else:
    print("Nessuna verifica")

# COMMAND ----------

# Correzione 8f (stampa sempre "Da verificare": "pending" da solo è un testo non vuoto,
# quindi conta come vero; ogni confronto va scritto per intero)
status = "completed"
if status == "cancelled" or status == "pending":
    print("Da verificare")
else:
    print("Nessuna verifica")
