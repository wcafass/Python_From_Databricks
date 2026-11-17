# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 6 – Errori e debug
# MAGIC
# MAGIC Notebook del Capitolo 6 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Leggere un messaggio di errore completo: tipo, messaggio, riga, traceback
# MAGIC - Distinguere gli errori di sintassi dagli errori durante l'esecuzione
# MAGIC - Riconoscere le cause tipiche di NameError, TypeError, ValueError, ZeroDivisionError, IndexError, KeyError e AttributeError
# MAGIC - Trovare un errore silenzioso con un metodo: risultato atteso, print di controllo, `type()`
# MAGIC - Gestire i valori non convertibili con `try` / `except`, come `try_cast` in SQL
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–5; notebook collegato al compute **Serverless**
# MAGIC - Le celle `%sql` non leggono tabelle; nessuna cella scrive tabelle
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio. **Non usare Run all**: quasi tutte le sezioni contengono errori voluti.
# MAGIC Si esegue per prima la **cella di preparazione**. Le celle vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si leggono il tipo, il messaggio e la riga;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** subito sotto deve funzionare **senza errori**, con il risultato indicato.

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

# Le strutture guida come piccola tabella (Capitolo 3)
guide_properties = [
    {"property_id": 11670, "title": "Historic Inn in Rome", "bookings_2024": 6, "cancelled_2024": 0, "revenue_2024": 3966.21},
    {"property_id": 16317, "title": "Bungalow in Sardinia", "bookings_2024": 7, "cancelled_2024": 1, "revenue_2024": 5139.59},
    {"property_id": 16225, "title": "Beach House in Amalfi", "bookings_2024": 4, "cancelled_2024": 2, "revenue_2024": 2896.92},
]

# Gli importi di esempio del Capitolo 4, arrivati come testo (per esempio da un file)
raw_amounts = ["879.15", "n.d.", "412.5", "-42.76", "", "655.0"]
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.1 Anatomia di un messaggio di errore
# MAGIC Un errore durante l'esecuzione: si leggono il **tipo** (`TypeError`), il **messaggio** e la **riga** indicata dalla freccia `---->` (qui la 4).

# COMMAND ----------

# ERRORE VOLUTO – un numero sommato a un testo
amalfi_revenue = 2896.92
sardinia_revenue = "5139.59"   # valore arrivato come testo
total_revenue = amalfi_revenue + sardinia_revenue
print(total_revenue)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il testo si converte con `float()` prima della somma. Risultato atteso: `Ricavo di Amalfi e Sardegna: 8036.51`.

# COMMAND ----------

# Correzione: il testo si converte in numero prima della somma
amalfi_revenue = 2896.92
sardinia_revenue = "5139.59"   # valore arrivato come testo
total_revenue = amalfi_revenue + float(sardinia_revenue)
print(f"Ricavo di Amalfi e Sardegna: {total_revenue:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: anche Databricks SQL ha errori con un nome. La cella seguente deve fallire con `CAST_INVALID_INPUT`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ERRORE VOLUTO – un testo che non rappresenta un numero
# MAGIC SELECT CAST('n.d.' AS DOUBLE) AS price

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: un testo che rappresenta un numero. Risultato atteso: `236.95`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione: il testo rappresenta un numero
# MAGIC SELECT CAST('236.95' AS DOUBLE) AS price

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.2 Errori di sintassi ed errori durante l'esecuzione
# MAGIC Due celle con la stessa prima riga. Nella prima c'è un errore di sintassi: **nessuna riga viene eseguita**, nemmeno la `print` iniziale.

# COMMAND ----------

# ERRORE VOLUTO – errore di sintassi: la cella non viene eseguita
print("Inizio della cella")
if 50.0 > CANCELLATION_RATE_THRESHOLD
    print("critico")

# COMMAND ----------

# MAGIC %md
# MAGIC Nella seconda l'errore avviene durante l'esecuzione: le righe prima dell'errore vengono eseguite. Output atteso prima del messaggio: `Inizio della cella` e `Tasso di Amalfi: 50.0`.

# COMMAND ----------

# ERRORE VOLUTO – errore durante l'esecuzione: le righe precedenti vengono eseguite
print("Inizio della cella")
amalfi_rate = 2 / 4 * 100
print(f"Tasso di Amalfi: {amalfi_rate}")
print(amalfi_rate > "30")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il confronto si fa con un numero, la costante della soglia. Risultato atteso: `Inizio della cella`, `Tasso di Amalfi: 50.0`, `True`.

# COMMAND ----------

# Correzione: la soglia è un numero, non un testo
print("Inizio della cella")
amalfi_rate = 2 / 4 * 100
print(f"Tasso di Amalfi: {amalfi_rate}")
print(amalfi_rate > CANCELLATION_RATE_THRESHOLD)

# COMMAND ----------

# MAGIC %md
# MAGIC Un altro errore di sintassi frequente: una parentesi aperta e mai chiusa.

# COMMAND ----------

# ERRORE VOLUTO – una parentesi aperta e mai chiusa
total_bookings = sum(bookings_2024
print(total_bookings)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: ogni parentesi aperta si chiude. Risultato atteso: `17`.

# COMMAND ----------

# Correzione: la parentesi di sum() è chiusa
total_bookings = sum(bookings_2024)
print(total_bookings)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.3 Leggere un traceback
# MAGIC Un errore dentro una funzione chiamata da un'altra funzione. Output atteso prima del messaggio: `Strutture guida: voto medio 3.1`; poi un `ZeroDivisionError` con **tre** blocchi `File <command-…>`: il traceback si legge **dal fondo**.

# COMMAND ----------

# ERRORE VOLUTO – la divisione per zero avviene dentro una funzione chiamata da un'altra
def average_of_present(values):
    total = 0
    count = 0
    for value in values:
        if value is not None:
            total = total + value
            count = count + 1
    return total / count

def describe_ratings(title, ratings):
    average = average_of_present(ratings)
    return f"{title}: voto medio {average:.1f}"

print(describe_ratings("Strutture guida", ratings_with_gap))
print(describe_ratings("Struttura senza recensioni", [None, None]))

# COMMAND ----------

# MAGIC %md
# MAGIC Una correzione a metà: `average_of_present` restituisce `None` se non ci sono valori, ma `describe_ratings` non lo prevede. L'errore **si sposta** nella funzione che chiama: ora è un `TypeError` alla riga del formato `:.1f`.

# COMMAND ----------

# ERRORE VOLUTO – correzione a metà: il None arriva nel formato :.1f
def average_of_present(values):
    total = 0
    count = 0
    for value in values:
        if value is not None:
            total = total + value
            count = count + 1
    if count == 0:
        return None
    return total / count

def describe_ratings(title, ratings):
    average = average_of_present(ratings)
    return f"{title}: voto medio {average:.1f}"

print(describe_ratings("Strutture guida", ratings_with_gap))
print(describe_ratings("Struttura senza recensioni", [None, None]))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione completa: anche `describe_ratings` gestisce il caso senza voti. Risultato atteso: `Strutture guida: voto medio 3.1` e `Struttura senza recensioni: voto medio n.d.`.

# COMMAND ----------

# Correzione: entrambe le funzioni gestiscono il caso senza valori presenti
def average_of_present(values):
    total = 0
    count = 0
    for value in values:
        if value is not None:
            total = total + value
            count = count + 1
    if count == 0:
        return None
    return total / count

def describe_ratings(title, ratings):
    average = average_of_present(ratings)
    if average is None:
        return f"{title}: voto medio n.d."
    return f"{title}: voto medio {average:.1f}"

print(describe_ratings("Strutture guida", ratings_with_gap))
print(describe_ratings("Struttura senza recensioni", [None, None]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.4 NameError: un nome che Python non conosce
# MAGIC Tre cause frequenti, una per cella: un nome scritto male, un testo senza virgolette, una funzione definita in un altro notebook.

# COMMAND ----------

# ERRORE VOLUTO – il nome della lista è scritto al singolare
print(max(base_price))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il nome giusto è `base_prices`. Risultato atteso: `284.97`.

# COMMAND ----------

# Correzione: il nome è quello della cella di preparazione
print(max(base_prices))

# COMMAND ----------

# ERRORE VOLUTO – un testo senza virgolette viene letto come un nome
destination = Rome
print(destination)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: i testi vanno tra virgolette. Risultato atteso: `Rome`.

# COMMAND ----------

# Correzione: il testo è tra virgolette
destination = "Rome"
print(destination)

# COMMAND ----------

# ERRORE VOLUTO – calculate_average è stata definita nel notebook del Capitolo 5, non in questo
print(calculate_average(ratings_with_gap))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: in questo notebook si usa la funzione definita nella sezione 6.3 (eseguire prima la sua cella di correzione). Risultato atteso: `3.1`.

# COMMAND ----------

# Correzione: si usa una funzione definita in questo notebook (sezione 6.3)
print(average_of_present(ratings_with_gap))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.5 TypeError e ValueError: tipo sbagliato, valore sbagliato
# MAGIC `TypeError`: un'operazione riceve un valore del **tipo** sbagliato. Il nome `NoneType` nel messaggio indica un `None`.

# COMMAND ----------

# ERRORE VOLUTO – il voto della Sardegna è None
sardinia_rating = ratings_with_gap[1]
print(sardinia_rating * 2)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: prima del calcolo si controlla il `None`. Risultato atteso: `Voto non disponibile`.

# COMMAND ----------

# Correzione: il caso None si controlla prima del calcolo
sardinia_rating = ratings_with_gap[1]
if sardinia_rating is None:
    print("Voto non disponibile")
else:
    print(sardinia_rating * 2)

# COMMAND ----------

# MAGIC %md
# MAGIC `ValueError`: il tipo è giusto (un testo), ma il **valore** non si può convertire. Tre celle, tre testi diversi.

# COMMAND ----------

# ERRORE VOLUTO – un testo che non rappresenta un numero
print(float("n.d."))

# COMMAND ----------

# ERRORE VOLUTO – la virgola decimale non è riconosciuta da float()
print(float("284,97"))

# COMMAND ----------

# ERRORE VOLUTO – un testo vuoto
print(float(""))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione possibile solo per il valore con la virgola, alla fonte: il numero si scrive con il punto. Risultato atteso: `284.97`. Per `"n.d."` e `""` non esiste un numero giusto: si decide che cosa fare nella sezione 6.8.

# COMMAND ----------

# Correzione: il numero con il punto decimale si converte
print(float("284.97"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.6 ZeroDivisionError e gli errori delle collezioni
# MAGIC Una struttura senza prenotazioni: la divisione per zero ferma la cella.

# COMMAND ----------

# ERRORE VOLUTO – una struttura senza prenotazioni nel 2024
cancelled = 0
bookings = 0
print(cancelled / bookings * 100)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la funzione del Capitolo 5, con il caso particolare gestito da un `if`. Risultati attesi: `None` e `50.0`.

# COMMAND ----------

# Correzione: il denominatore zero si controlla prima della divisione
def cancellation_rate(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

print(cancellation_rate(0, 0))
print(cancellation_rate(2, 4))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: la stessa divisione in SQL. La cella deve fallire con `DIVIDE_BY_ZERO`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ERRORE VOLUTO – divisione per zero
# MAGIC SELECT 0 / 0 * 100 AS cancellation_rate

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `NULLIF` trasforma il denominatore zero in `NULL`, e la divisione restituisce `NULL`. Risultato atteso: `null` e `50.0`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Correzione: NULLIF trasforma lo zero in NULL
# MAGIC SELECT 0 / NULLIF(0, 0) * 100 AS no_bookings,
# MAGIC        2 / NULLIF(4, 0) * 100 AS amalfi

# COMMAND ----------

# MAGIC %md
# MAGIC `IndexError`: una posizione che la lista non ha.

# COMMAND ----------

# ERRORE VOLUTO – la lista ha tre righe: le posizioni sono 0, 1 e 2
print(guide_properties[3])

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: l'ultima riga è in posizione 2, o -1. Risultato atteso: `Beach House in Amalfi`.

# COMMAND ----------

# Correzione: l'ultima riga si legge con l'indice -1
print(guide_properties[-1]["title"])

# COMMAND ----------

# MAGIC %md
# MAGIC `KeyError`: una chiave che il dizionario non ha. Il messaggio contiene **solo la chiave**.

# COMMAND ----------

# ERRORE VOLUTO – le chiavi sono minuscole
amalfi_row = guide_properties[2]
print(amalfi_row["Title"])

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la chiave scritta come nel dizionario. Risultati attesi: `Beach House in Amalfi` e `None` (con `get()`, per una chiave che non c'è).

# COMMAND ----------

# Correzione: la chiave è "title"; get() restituisce None per una chiave assente
amalfi_row = guide_properties[2]
print(amalfi_row["title"])
print(amalfi_row.get("base_price"))

# COMMAND ----------

# MAGIC %md
# MAGIC `AttributeError`: un metodo chiamato su un valore che non lo ha. L'errore è alla riga 4, ma la riga sbagliata è la 3.

# COMMAND ----------

# ERRORE VOLUTO – append() restituisce None: dopo la riga 3 la lista non c'è più
critical_titles = []
critical_titles = critical_titles.append("Beach House in Amalfi")
critical_titles = critical_titles.append("Bungalow in Sardinia")
print(critical_titles)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `append()` modifica la lista e non si assegna. Risultato atteso: `['Beach House in Amalfi', 'Bungalow in Sardinia']`.

# COMMAND ----------

# Correzione: append() si chiama senza assegnare il risultato
critical_titles = []
critical_titles.append("Beach House in Amalfi")
critical_titles.append("Bungalow in Sardinia")
print(critical_titles)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.7 Errori silenziosi e metodo di debug
# MAGIC Passo zero: sapere il risultato atteso. La media dei voti presenti delle strutture guida è (3.2 + 3.0) / 2 = **3.1**.

# COMMAND ----------

# ERRORE SILENZIOSO – la media divide per tutti i valori, anche quelli mancanti
def average_rating(ratings):
    total = 0
    for rating in ratings:
        if rating is not None:
            total = total + rating
    return total / len(ratings)

print(f"Voto medio: {average_rating(ratings_with_gap):.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC Debug: si ripete il calcolo fuori dalla funzione con **print di controllo** dei valori intermedi. Risultati attesi: `total: 6.2` (giusto) e `len: 3` (sbagliato: conta anche il `None`).

# COMMAND ----------

# Debug: print di controllo dei valori intermedi
total = 0
for rating in ratings_with_gap:
    if rating is not None:
        total = total + rating
print("total:", total)
print("len:", len(ratings_with_gap))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il denominatore conta solo i valori presenti. Risultato atteso: `Voto medio: 3.10`.

# COMMAND ----------

# Correzione: un contatore dei soli valori presenti
def average_rating(ratings):
    total = 0
    count = 0
    for rating in ratings:
        if rating is not None:
            total = total + rating
            count = count + 1
    return total / count

print(f"Voto medio: {average_rating(ratings_with_gap):.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `AVG` contro `SUM / COUNT(*)` sugli stessi tre voti. Risultato atteso: `3.10` e `2.07`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ROUND(AVG(rating), 2)              AS avg_rating,
# MAGIC        ROUND(SUM(rating) / COUNT(*), 2)   AS sum_over_all_rows
# MAGIC FROM VALUES (3.2), (NULL), (3.0) AS t(rating)

# COMMAND ----------

# MAGIC %md
# MAGIC Un secondo errore silenzioso: i prezzi sono testi, e il massimo è calcolato in ordine alfabetico. Risultato (sbagliato): `99.5`.

# COMMAND ----------

# ERRORE SILENZIOSO – i prezzi sono testi: il massimo è quello alfabetico
raw_prices = ["284.97", "1250.0", "213.91", "99.5"]   # valori di esempio
print(max(raw_prices))

# COMMAND ----------

# MAGIC %md
# MAGIC Debug: `type()` mostra il tipo dei valori. Risultati attesi: `<class 'str'>` e `<class 'str'>`.

# COMMAND ----------

# Debug: il tipo dei valori e del risultato
print(type(raw_prices[0]))
print(type(max(raw_prices)))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: i testi si convertono in numeri prima del confronto. Risultato atteso: `1250.0`.

# COMMAND ----------

# Correzione: si convertono i testi in numeri, poi si calcola il massimo
prices = [float(raw_price) for raw_price in raw_prices]
print(max(prices))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.8 try / except
# MAGIC **Ponte SQL**: `try_cast` e `try_divide` restituiscono `NULL` invece di fermarsi. Risultato atteso: `null`, `236.95`, `null`, `50.0`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT try_cast('n.d.' AS DOUBLE)   AS price_nd,
# MAGIC        try_cast('236.95' AS DOUBLE) AS price_ok,
# MAGIC        try_divide(0, 0) * 100       AS rate_no_bookings,
# MAGIC        try_divide(2, 4) * 100       AS rate_amalfi

# COMMAND ----------

# MAGIC %md
# MAGIC Il valore non è convertibile: il resto del blocco `try` viene saltato e si esegue il blocco `except`. Risultati attesi: `Valore non convertibile` e `Prezzo: None`.

# COMMAND ----------

raw_price = "n.d."
try:
    price = float(raw_price)
    print("Conversione riuscita")
except ValueError:
    price = None
    print("Valore non convertibile")
print(f"Prezzo: {price}")

# COMMAND ----------

# MAGIC %md
# MAGIC Il valore è convertibile: il blocco `try` arriva in fondo e il blocco `except` viene saltato. Risultati attesi: `Conversione riuscita` e `Prezzo: 236.95`.

# COMMAND ----------

raw_price = "236.95"
try:
    price = float(raw_price)
    print("Conversione riuscita")
except ValueError:
    price = None
    print("Valore non convertibile")
print(f"Prezzo: {price}")

# COMMAND ----------

# MAGIC %md
# MAGIC `except ValueError` cattura solo i `ValueError`: un errore di un altro tipo ferma la cella come sempre.

# COMMAND ----------

# ERRORE VOLUTO – except ValueError non cattura un TypeError
raw_price = None
try:
    price = float(raw_price)
except ValueError:
    price = None
print(f"Prezzo: {price}")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: un secondo blocco `except` per il `TypeError`. Risultati attesi: `Valore mancante` e `Prezzo: None`.

# COMMAND ----------

# Correzione: un blocco except per ciascun tipo di errore previsto
raw_price = None
try:
    price = float(raw_price)
except ValueError:
    price = None
    print("Testo non convertibile")
except TypeError:
    price = None
    print("Valore mancante")
print(f"Prezzo: {price}")

# COMMAND ----------

# MAGIC %md
# MAGIC `except ... as error`: il messaggio dell'errore catturato in una variabile. Risultato atteso: `Scartato: could not convert string to float: '284,97'` e `Prezzo: None`.

# COMMAND ----------

raw_price = "284,97"
try:
    price = float(raw_price)
except ValueError as error:
    price = None
    print(f"Scartato: {error}")
print(f"Prezzo: {price}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.9 Una funzione di conversione: to_float
# MAGIC Il `try_cast` del libro, scritto in Python. La cella non produce output.

# COMMAND ----------

def to_float(text):
    """Converte un testo in float, come try_cast in SQL.

    Restituisce None se il testo manca (None) o non rappresenta un numero.
    """
    if text is None:
        return None
    try:
        return float(text)
    except ValueError:
        return None

# COMMAND ----------

# MAGIC %md
# MAGIC Cinque prove con risultato noto. Risultati attesi: `236.95`, `None`, `None`, `None`, `None`.

# COMMAND ----------

print(to_float("236.95"))
print(to_float("n.d."))
print(to_float(""))
print(to_float("284,97"))
print(to_float(None))

# COMMAND ----------

# MAGIC %md
# MAGIC La funzione in un ciclo, con il conteggio degli scarti. Risultati attesi: `Scartato: 'n.d.'`, `Scartato: ''`, `[879.15, 412.5, -42.76, 655.0]`, `Validi: 4 - scartati: 2 - totale: 1903.89`.

# COMMAND ----------

valid_amounts = []
rejected_count = 0
for raw_amount in raw_amounts:
    amount = to_float(raw_amount)
    if amount is None:
        rejected_count = rejected_count + 1
        print(f"Scartato: '{raw_amount}'")
    else:
        valid_amounts.append(amount)

print(valid_amounts)
print(f"Validi: {len(valid_amounts)} - scartati: {rejected_count} - totale: {sum(valid_amounts):.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: lo stesso calcolo con `try_cast`. Risultato atteso: `1903.89`, `4`, `2`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ROUND(SUM(try_cast(raw_amount AS DOUBLE)), 2)  AS total_valid,
# MAGIC        COUNT(try_cast(raw_amount AS DOUBLE))            AS valid_count,
# MAGIC        COUNT(*) - COUNT(try_cast(raw_amount AS DOUBLE)) AS rejected_count
# MAGIC FROM VALUES ('879.15'), ('n.d.'), ('412.5'), ('-42.76'), (''), ('655.0') AS t(raw_amount)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6.10 Errori comuni con try / except
# MAGIC `except` senza tipo cattura **tutti** gli errori, anche quelli di battitura. Risultato (sbagliato): `[None, None, None, None, None, None]`.

# COMMAND ----------

# ERRORE SILENZIOSO – except senza tipo nasconde un NameError (flaot al posto di float)
converted = []
for raw_amount in raw_amounts:
    try:
        converted.append(flaot(raw_amount))
    except:
        converted.append(None)
print(converted)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `except ValueError` e il nome della funzione scritto bene. Risultato atteso: `[879.15, None, 412.5, -42.76, None, 655.0]`.

# COMMAND ----------

# Correzione: si cattura solo il ValueError previsto
converted = []
for raw_amount in raw_amounts:
    try:
        converted.append(float(raw_amount))
    except ValueError:
        converted.append(None)
print(converted)

# COMMAND ----------

# MAGIC %md
# MAGIC Un blocco `try` troppo grande: il primo errore salta tutto il resto del ciclo. Risultato (sbagliato): `Valore non convertibile` e `[879.15]`.

# COMMAND ----------

# ERRORE SILENZIOSO – il try contiene tutto il ciclo: il primo errore ferma le conversioni
converted = []
try:
    for raw_amount in raw_amounts:
        converted.append(float(raw_amount))
except ValueError:
    print("Valore non convertibile")
print(converted)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il `try` contiene solo la conversione, dentro `to_float` (sezione 6.9, da eseguire prima). Risultato atteso: `[879.15, None, 412.5, -42.76, None, 655.0]`.

# COMMAND ----------

# Correzione: il try avvolge una sola conversione, a ogni giro
converted = []
for raw_amount in raw_amounts:
    converted.append(to_float(raw_amount))
print(converted)

# COMMAND ----------

# MAGIC %md
# MAGIC Un errore di sintassi non si cattura: la cella non viene eseguita, e il blocco `try` non parte nemmeno.

# COMMAND ----------

# ERRORE VOLUTO – un errore di sintassi non si cattura con try
try:
    price = float("236.95"
except SyntaxError:
    price = None

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: gli errori di sintassi si correggono nel codice. Risultato atteso: `236.95`.

# COMMAND ----------

# Correzione: la parentesi è chiusa
try:
    price = float("236.95")
except ValueError:
    price = None
print(price)

# COMMAND ----------

# MAGIC %md
# MAGIC Quando il caso particolare si riconosce prima, un `if` è più chiaro di `try` / `except`. Le due funzioni danno lo stesso risultato. Risultati attesi: `None None` e `50.0 50.0`.

# COMMAND ----------

def rate_with_if(cancelled, bookings):
    if bookings == 0:
        return None
    return cancelled / bookings * 100

def rate_with_try(cancelled, bookings):
    try:
        return cancelled / bookings * 100
    except ZeroDivisionError:
        return None

print(rate_with_if(0, 0), rate_with_try(0, 0))
print(rate_with_if(2, 4), rate_with_try(2, 4))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - Un errore ha un **tipo**, un **messaggio** e una **riga** (freccia `---->`); si legge in questo ordine. Databricks mostra il riepilogo in cima e il **traceback** completo sotto, che termina con la stessa riga.
# MAGIC - Errore di sintassi: la cella non viene eseguita, il messaggio è di una riga. Errore durante l'esecuzione: le righe precedenti sono state eseguite.
# MAGIC - Il traceback si legge **dal fondo**: l'ultimo blocco indica dove è successo, i blocchi sopra chi ha chiamato. La riga dell'errore non è sempre la riga sbagliata.
# MAGIC - NameError: nome scritto male, testo senza virgolette, cella non eseguita, funzione di un altro notebook. TypeError: tipo sbagliato (spesso `NoneType`). ValueError: valore non convertibile. ZeroDivisionError, IndexError, KeyError (solo la chiave), AttributeError (spesso un `None` inatteso).
# MAGIC - Errori silenziosi: passo zero, il risultato atteso; poi print di controllo dei valori intermedi, `type()`, una correzione alla volta, verifica con un caso noto o con SQL.
# MAGIC - `try` / `except Tipo:` prova un blocco e, se arriva quell'errore, esegue il blocco alternativo; il resto del `try` viene saltato; gli errori di altri tipi non vengono catturati. Più `except`, `except ... as error`.
# MAGIC - `to_float` è il `try_cast` del libro: un `try` piccolo, un tipo preciso, gli scarti contati. Mai `except` senza tipo; un `if` quando basta.
