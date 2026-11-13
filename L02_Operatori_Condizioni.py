# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 2 – Operatori e condizioni
# MAGIC
# MAGIC Notebook del Capitolo 2 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Calcolare con gli operatori aritmetici, compresi `//`, `%` e `**`, rispettando la precedenza
# MAGIC - Unire e ripetere testi con `+` e `*`
# MAGIC - Scrivere condizioni con gli operatori di confronto e con `and`, `or`, `not`; controllare `None` con `is None`
# MAGIC - Far prendere decisioni al codice con `if`, `elif`, `else`, rispettando l'indentazione
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0 e 1; notebook collegato al compute **Serverless**
# MAGIC - `L00_Prepara_Dati` eseguito una volta (Cap. 0, sezione 0.7): le celle `%sql` leggono solo `samples.wanderbricks`, ma il libro presuppone la preparazione già fatta
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: le sezioni 2.2 e 2.10 contengono errori voluti e silenziosi.
# MAGIC Si esegue per prima la **cella di preparazione** qui sotto; dopo un'interruzione della sessione basta rieseguire quella cella.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione
# MAGIC Costanti e valori delle strutture guida usati nelle sezioni del capitolo.

# COMMAND ----------

# Cella di preparazione: costanti e valori delle strutture guida
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

# Prenotazioni, cancellate e ricavo 2024 delle tre strutture guida
rome_bookings = 6
rome_cancelled = 0
rome_revenue = 3966.21
sardinia_bookings = 7
sardinia_cancelled = 1
sardinia_revenue = 5139.59
amalfi_bookings = 4
amalfi_cancelled = 2
amalfi_revenue = 2896.92

# Dati descrittivi della struttura di Amalfi
property_id = 16225
property_title = "Beach House in Amalfi"
destination = "Amalfi"
property_type = "Summer Getaway"
base_price = 236.95
average_rating = 3.0

print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.1 Operatori aritmetici
# MAGIC `+` `-` `*` `/` come in SQL. Risultati attesi: `17`, `2242.67`, `710.8499999999999` (decimali approssimati, Capitolo 1), `724.23`.

# COMMAND ----------

total_bookings = rome_bookings + sardinia_bookings + amalfi_bookings
revenue_gap = sardinia_revenue - amalfi_revenue
three_nights = base_price * 3
revenue_per_booking = amalfi_revenue / amalfi_bookings
print(total_bookings)
print(revenue_gap)
print(three_nights)
print(revenue_per_booking)

# COMMAND ----------

# MAGIC %md
# MAGIC **La divisione `/` restituisce sempre un `float`**, anche quando il risultato è intero. Risultato atteso: `2.0` e `<class 'float'>`.

# COMMAND ----------

half_bookings = amalfi_bookings / 2
print(half_bookings, type(half_bookings))

# COMMAND ----------

# MAGIC %md
# MAGIC **Divisione intera `//` e resto `%`**: quante settimane intere e quante notti in più ci sono in un soggiorno di 9 notti.

# COMMAND ----------

nights = 9
full_weeks = nights // 7
extra_nights = nights % 7
print(f"{nights} notti: settimane intere {full_weeks}, notti in più {extra_nights}")

# COMMAND ----------

# MAGIC %md
# MAGIC Il resto serve anche a capire se un numero è divisibile per un altro: resto 0. L'anno 2024 è divisibile per 4 (anno bisestile). Risultato atteso: `0`.

# COMMAND ----------

ANALYSIS_YEAR % 4

# COMMAND ----------

# MAGIC %md
# MAGIC **Potenza `**`**: il prezzo base dopo due aumenti annuali del 5%. Risultati attesi: `1.1025`, `261.237375`, `261.24`.

# COMMAND ----------

growth_factor = 1.05 ** 2
new_price = base_price * growth_factor
print(growth_factor)
print(new_price)
print(f"{new_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `div`, `%` (o `mod`), `power`; in SQL di Databricks anche `7 / 2` restituisce un numero con decimali.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 9 div 7        AS full_weeks,
# MAGIC        9 % 7          AS extra_nights,
# MAGIC        mod(9, 7)      AS extra_nights_mod,
# MAGIC        power(1.05, 2) AS growth_factor,
# MAGIC        7 / 2          AS division

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `1`, `2`, `2`, `1.1025`, `3.5`.
# MAGIC
# MAGIC ## 2.2 Precedenza e parentesi
# MAGIC Ordine: `**`, poi `*` `/` `//` `%`, poi `+` `-`; a parità di livello, da sinistra a destra. Le parentesi cambiano l'ordine.
# MAGIC
# MAGIC La cella seguente è un **errore silenzioso**: nessun messaggio, ma `577.8633333333333` non è il prezzo medio. La correzione è nella cella successiva (risultato atteso `245.27666666666664`).

# COMMAND ----------

# ERRORE SILENZIOSO – manca la parentesi intorno alla somma
average_price = 284.97 + 213.91 + 236.95 / 3
print(average_price)

# COMMAND ----------

# Correzione: prima la somma, poi la divisione
average_price = (284.97 + 213.91 + 236.95) / 3
print(average_price)
print(f"{average_price:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC Il tasso di cancellazione si calcola da sinistra a destra: prima la divisione, poi la moltiplicazione. Le parentesi nella seconda riga cambiano il significato. Risultati attesi: `50.0`, `50.0`, `0.005`.

# COMMAND ----------

amalfi_rate = amalfi_cancelled / amalfi_bookings * 100
print(amalfi_rate)
print((amalfi_cancelled / amalfi_bookings) * 100)
print(amalfi_cancelled / (amalfi_bookings * 100))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.3 Operatori con le stringhe
# MAGIC `+` unisce due testi, `*` ripete un testo. Risultati attesi: `Amalfi - Summer Getaway` e una riga di 30 trattini.

# COMMAND ----------

label = destination + " - " + property_type
separator = "-" * 30
print(label)
print(separator)

# COMMAND ----------

# MAGIC %md
# MAGIC Un numero va convertito con `str()` prima di unirlo a un testo (o si usa una f-string). Due testi che contengono cifre si uniscono, non si sommano: risultati attesi `Analisi 2024`, `305`, `35`.

# COMMAND ----------

print("Analisi " + str(ANALYSIS_YEAR))
print("30" + "5")
print(30 + 5)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `||` unisce, `repeat` ripete.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Amalfi' || ' - ' || 'Summer Getaway' AS label,
# MAGIC        repeat('-', 30)                       AS separator

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.4 Operatori di confronto
# MAGIC `==` `!=` `<` `>` `<=` `>=` confrontano due valori e restituiscono `True` o `False`. Risultati attesi: `True`, `True`, `True`.

# COMMAND ----------

amalfi_rate = amalfi_cancelled / amalfi_bookings * 100
print(amalfi_rate > CANCELLATION_RATE_THRESHOLD)
print(amalfi_rate == 50.0)
print(amalfi_bookings != 0)

# COMMAND ----------

# MAGIC %md
# MAGIC Il risultato di un confronto è un valore `bool` e si può salvare in una variabile. `=` mette, `==` domanda. Risultati attesi: `True <class 'bool'>` e `False`.

# COMMAND ----------

is_critical = amalfi_rate > CANCELLATION_RATE_THRESHOLD
print(is_critical, type(is_critical))

sardinia_rate = sardinia_cancelled / sardinia_bookings * 100
print(sardinia_rate > CANCELLATION_RATE_THRESHOLD)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: lo stesso confronto in SQL restituisce un valore `boolean`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 2 / 4 * 100 > 30 AS is_critical,
# MAGIC        1 / 7 * 100 > 30 AS is_critical_sardinia

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso: `true`, `false`.
# MAGIC
# MAGIC **Attenzione ai `float`**: per i decimali approssimati (Capitolo 1) un confronto con `==` può dare `False`. Si confrontano valori arrotondati. Risultati attesi: `False`, `True`.

# COMMAND ----------

print(284.97 * 3 == 854.91)
print(round(284.97 * 3, 2) == 854.91)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.5 Confrontare testi e tipi diversi
# MAGIC Il confronto tra testi distingue maiuscole e minuscole. Risultati attesi: `True`, `False`.

# COMMAND ----------

print(destination == "Amalfi")
print(destination == "amalfi")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: anche in SQL di Databricks il confronto tra testi distingue maiuscole e minuscole. Risultati attesi: `false` e `1`, `0`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Amalfi' = 'amalfi' AS same_text

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM samples.wanderbricks.destinations WHERE destination = 'Amalfi') AS with_capital,
# MAGIC   (SELECT COUNT(*) FROM samples.wanderbricks.destinations WHERE destination = 'amalfi') AS lowercase

# COMMAND ----------

# MAGIC %md
# MAGIC **Testo e numero**: `==` tra un testo e un numero restituisce `False` senza errori; `<` e `>` tra un testo e un numero producono `TypeError` (sezione 2.10). Tra due testi, `<` segue l'ordine alfabetico. Risultati attesi: `False`, `True`, `True`.

# COMMAND ----------

print(property_id == "16225")
print(property_id == int("16225"))
print("Amalfi" < "Rome")

# COMMAND ----------

# MAGIC %md
# MAGIC **Confronti concatenati**: `0 <= x <= 100` equivale a `x BETWEEN 0 AND 100` (estremi inclusi). Risultati attesi: `True`, `False`.

# COMMAND ----------

print(0 <= amalfi_rate <= 100)
print(0 <= 120.0 <= 100)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 50.0 BETWEEN 0 AND 100  AS valid_rate,
# MAGIC        120.0 BETWEEN 0 AND 100 AS invalid_rate

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.6 Operatori logici
# MAGIC `and` (entrambe vere), `or` (almeno una vera), `not` (il contrario), come `AND`, `OR`, `NOT` in `WHERE`. Risultati attesi: `True`, `True`, `False`.

# COMMAND ----------

is_summer = property_type == "Summer Getaway"
is_critical = amalfi_rate > CANCELLATION_RATE_THRESHOLD
print(is_summer and is_critical)
print(is_summer or is_critical)
print(not is_critical)

# COMMAND ----------

# MAGIC %md
# MAGIC Con `or` ogni confronto va scritto per intero. Risultato atteso: `True`.

# COMMAND ----------

status = "completed"
is_active = status == "confirmed" or status == "completed"
print(is_active)

# COMMAND ----------

# MAGIC %md
# MAGIC **`and` prima di `or`**: senza parentesi `and` si valuta per primo. Risultati attesi: `True` (senza parentesi) e `False` (con le parentesi).

# COMMAND ----------

status = "confirmed"
total_amount = 450.0
print(status == "confirmed" or status == "completed" and total_amount > 1000)
print((status == "confirmed" or status == "completed") and total_amount > 1000)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le cancellazioni 2024 della struttura di Amalfi con `AND` e `BETWEEN`. Risultato atteso: `2`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS cancelled_2024
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC WHERE property_id = 16225
# MAGIC   AND status = 'cancelled'
# MAGIC   AND check_in BETWEEN '2024-01-01' AND '2024-12-31'

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.7 Il valore None nelle condizioni
# MAGIC `is None` / `is not None` come `IS NULL` / `IS NOT NULL`. Risultati attesi: `True`, `False`.

# COMMAND ----------

missing_rating = None
print(missing_rating is None)
print(missing_rating is not None)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: in SQL `= NULL` non è mai vero. Risultati attesi: `476` con `IS NULL`, `0` con `= NULL`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS null_ratings
# MAGIC FROM samples.wanderbricks.reviews
# MAGIC WHERE rating IS NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS null_ratings
# MAGIC FROM samples.wanderbricks.reviews
# MAGIC WHERE rating = NULL

# COMMAND ----------

# MAGIC %md
# MAGIC **Prima il controllo su `None`, poi il confronto**: `and` si ferma appena il risultato è noto, quindi il secondo confronto non viene eseguito. Risultati attesi: `False` e `True`.

# COMMAND ----------

missing_rating = None
print(missing_rating is not None and missing_rating >= 3.0)
print(average_rating is not None and average_rating >= 3.0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.8 Prendere decisioni: if, else, elif
# MAGIC **`if`**: il blocco rientrato si esegue solo se la condizione è vera; la riga non rientrata si esegue sempre. Risultato atteso: due righe.

# COMMAND ----------

amalfi_rate = amalfi_cancelled / amalfi_bookings * 100
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print(f"Attenzione: tasso di cancellazione {amalfi_rate:.1f}%, sopra la soglia")
print("Controllo completato")

# COMMAND ----------

# MAGIC %md
# MAGIC Con la struttura in Sardegna (14.3%) la condizione è falsa: risultato atteso solo `Controllo completato`.

# COMMAND ----------

sardinia_rate = sardinia_cancelled / sardinia_bookings * 100
if sardinia_rate > CANCELLATION_RATE_THRESHOLD:
    print(f"Attenzione: tasso di cancellazione {sardinia_rate:.1f}%, sopra la soglia")
print("Controllo completato")

# COMMAND ----------

# MAGIC %md
# MAGIC **`if` / `else`**: uno dei due blocchi si esegue sempre. Risultato atteso: `Bungalow in Sardinia: 14.3% - ok`.

# COMMAND ----------

if sardinia_rate > CANCELLATION_RATE_THRESHOLD:
    status_label = "critico"
else:
    status_label = "ok"
print(f"Bungalow in Sardinia: {sardinia_rate:.1f}% - {status_label}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Attenzione**: un valore usato da solo come condizione segue le regole di `bool()` (Capitolo 1): `0`, `""` e `None` contano come falsi. Funziona, ma nasconde se il valore è zero o mancante: meglio un confronto esplicito. Risultati attesi: `Nessuna cancellazione` due volte.

# COMMAND ----------

if rome_cancelled:
    print("Ci sono cancellazioni")
else:
    print("Nessuna cancellazione")

if rome_cancelled > 0:
    print("Ci sono cancellazioni")
else:
    print("Nessuna cancellazione")

# COMMAND ----------

# MAGIC %md
# MAGIC **`if` / `elif` / `else`**: fasce di prezzo base. Vince la prima condizione vera. Risultato atteso: `Beach House in Amalfi: 236.95 - medio`.

# COMMAND ----------

if base_price >= 250:
    price_band = "alto"
elif base_price >= 200:
    price_band = "medio"
else:
    price_band = "basso"
print(f"{property_title}: {base_price} - {price_band}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: la stessa classificazione con `CASE WHEN` sulle tre strutture guida. Risultato atteso: 11670 `alto`, 16225 `medio`, 16317 `medio`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT property_id,
# MAGIC        base_price,
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
# MAGIC **Classificazione del tasso di cancellazione in quattro stati.** Il controllo su `None` va per primo.
# MAGIC Risultato atteso: `50.0 critico`. Si provi poi a cambiare la prima riga in `cancellation_rate = None`, `cancellation_rate = 120.0`, `cancellation_rate = sardinia_rate`: risultati attesi `None dato mancante`, `120.0 valore impossibile`, `14.285714285714285 ok`.

# COMMAND ----------

cancellation_rate = amalfi_rate
if cancellation_rate is None:
    cancellation_status = "dato mancante"
elif cancellation_rate < 0 or cancellation_rate > 100:
    cancellation_status = "valore impossibile"
elif cancellation_rate > CANCELLATION_RATE_THRESHOLD:
    cancellation_status = "critico"
else:
    cancellation_status = "ok"
print(cancellation_rate, cancellation_status)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: in SQL un `NULL` non soddisfa nessun `WHEN` e finisce nell'`ELSE` senza errori. Risultato atteso: `ok`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT CASE WHEN NULL > 30 THEN 'critico' ELSE 'ok' END AS cancellation_status

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.9 Blocchi e indentazione
# MAGIC Il blocco è formato dalle righe rientrate di 4 spazi dopo i due punti; finisce alla prima riga che torna al margine. Risultato atteso: solo `Fine del controllo`.

# COMMAND ----------

if sardinia_rate > CANCELLATION_RATE_THRESHOLD:
    print("Struttura critica")
    print("Da segnalare al responsabile")
print("Fine del controllo")

# COMMAND ----------

# MAGIC %md
# MAGIC **if annidato** (cenno): un `if` dentro il blocco di un altro, rientrato di altri 4 spazi. Risultati attesi: `Summer Getaway critica` due volte (la seconda con `and`).

# COMMAND ----------

if property_type == "Summer Getaway":
    if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
        print("Summer Getaway critica")
    else:
        print("Summer Getaway nella norma")

if property_type == "Summer Getaway" and amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print("Summer Getaway critica")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.10 Leggere gli errori del capitolo
# MAGIC Le celle seguenti vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si legge il nome dell'errore e la descrizione;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori**.
# MAGIC
# MAGIC Prima di iniziare si riesegua la cella di preparazione. Risultati attesi delle correzioni, nell'ordine: `critico`; `Struttura di Amalfi`; `critico`; `ok`; `False`; `True`; `alto`; `Struttura di Amalfi`; `Prenotazione non attiva`.

# COMMAND ----------

# ERRORE VOLUTO – mancano i due punti dopo la condizione
amalfi_rate = 50.0
if amalfi_rate > CANCELLATION_RATE_THRESHOLD
    print("critico")

# COMMAND ----------

# Correzione: i due punti chiudono la riga dell'if
amalfi_rate = 50.0
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print("critico")

# COMMAND ----------

# ERRORE VOLUTO – = al posto di == nella condizione
if destination = "Amalfi":
    print("Struttura di Amalfi")

# COMMAND ----------

# Correzione: == confronta
if destination == "Amalfi":
    print("Struttura di Amalfi")

# COMMAND ----------

# ERRORE VOLUTO – riga del blocco senza rientro
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
print("critico")

# COMMAND ----------

# Correzione: la riga del blocco è rientrata di 4 spazi
if amalfi_rate > CANCELLATION_RATE_THRESHOLD:
    print("critico")

# COMMAND ----------

# ERRORE VOLUTO – rientro senza un blocco da aprire
status_label = "ok"
    print(status_label)

# COMMAND ----------

# Correzione: nessun rientro fuori da un blocco
status_label = "ok"
print(status_label)

# COMMAND ----------

# ERRORE VOLUTO – il confronto arriva prima del controllo su None
missing_rating = None
print(missing_rating >= 3.0 and missing_rating is not None)

# COMMAND ----------

# Correzione: prima il controllo su None, poi il confronto
missing_rating = None
print(missing_rating is not None and missing_rating >= 3.0)

# COMMAND ----------

# ERRORE VOLUTO – confronto tra un testo e un numero
property_id_text = "16225"
print(property_id_text > 16000)

# COMMAND ----------

# Correzione: si converte il testo in numero prima di confrontare
property_id_text = "16225"
print(int(property_id_text) > 16000)

# COMMAND ----------

# ERRORE SILENZIOSO – condizioni nell'ordine sbagliato
rome_price = 284.97
if rome_price >= 200:
    price_band = "medio"
elif rome_price >= 250:
    price_band = "alto"
else:
    price_band = "basso"
print(price_band)

# COMMAND ----------

# Correzione: dalla condizione più restrittiva alla meno restrittiva
rome_price = 284.97
if rome_price >= 250:
    price_band = "alto"
elif rome_price >= 200:
    price_band = "medio"
else:
    price_band = "basso"
print(price_band)

# COMMAND ----------

# ERRORE SILENZIOSO – maiuscole diverse nel testo confrontato
if destination == "amalfi":
    print("Struttura di Amalfi")
else:
    print("Altra destinazione")

# COMMAND ----------

# Correzione: il testo si scrive esattamente come nel dato
if destination == "Amalfi":
    print("Struttura di Amalfi")
else:
    print("Altra destinazione")

# COMMAND ----------

# ERRORE SILENZIOSO – or tra un confronto e un testo
status = "pending"
if status == "confirmed" or "completed":
    print("Prenotazione attiva")
else:
    print("Prenotazione non attiva")

# COMMAND ----------

# Correzione: ogni confronto va scritto per intero
status = "pending"
if status == "confirmed" or status == "completed":
    print("Prenotazione attiva")
else:
    print("Prenotazione non attiva")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - Operatori aritmetici: `+` `-` `*` `/` (sempre `float`), `//` divisione intera, `%` resto, `**` potenza; precedenza `**` → `*` `/` `//` `%` → `+` `-`; nel dubbio, parentesi.
# MAGIC - Con i testi: `+` unisce, `*` ripete; un numero va convertito con `str()` o messo in una f-string.
# MAGIC - Confronti `==` `!=` `<` `>` `<=` `>=` → `True`/`False`; `=` mette, `==` domanda; testi case-sensitive; `0 <= x <= 100` come `BETWEEN`; i `float` si confrontano arrotondati.
# MAGIC - `and`, `or`, `not` come in `WHERE`; `and` prima di `or`; con `or` ogni confronto per intero.
# MAGIC - `is None` / `is not None` come `IS NULL`; prima il controllo su `None`, poi il confronto (`and` si ferma appena il risultato è noto).
# MAGIC - `if` / `elif` / `else` come `CASE WHEN`: vince la prima condizione vera; il `NULL` in SQL finisce nell'`ELSE`, il `None` in Python produce `TypeError`.
# MAGIC - Due punti alla fine della riga e blocco rientrato di 4 spazi: l'indentazione fa parte della sintassi.
