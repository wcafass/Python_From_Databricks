# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 7 – Moduli e librerie
# MAGIC
# MAGIC Notebook del Capitolo 7 del libro. Le sezioni hanno gli stessi numeri del testo.
# MAGIC
# MAGIC **Obiettivi**
# MAGIC - Distinguere le funzioni integrate da quelle da caricare con `import`
# MAGIC - Usare `import modulo`, `from modulo import nome` e l'alias `as`
# MAGIC - Creare e leggere date con `date`, convertire tra testo e data (`fromisoformat`, `strptime`, `strftime`)
# MAGIC - Calcolare con le date (`timedelta`, differenze, confronti, sequenze di giorni) e usare `datetime` per data e ora
# MAGIC - Riconoscere gli errori tipici di `import` e delle date
# MAGIC
# MAGIC **Prerequisiti**
# MAGIC - Capitoli 0–6; notebook collegato al compute **Serverless**
# MAGIC - `L00_Prepara_Dati` già eseguito (una cella `%sql` della sezione 7.9 legge `workspace.libro_python.b_bookings`); nessuna cella scrive tabelle
# MAGIC
# MAGIC **Eccezione di questo capitolo**: gli `import` non sono nella cella di preparazione ma nelle sezioni, perché sono l'argomento del capitolo. Dal Capitolo 8 tornano nella cella di preparazione.
# MAGIC
# MAGIC **Come eseguire questo notebook**: una cella alla volta, con Maiusc+Invio, **dall'alto in basso**. **Non usare Run all**: alcune celle contengono errori voluti.
# MAGIC Si esegue per prima la **cella di preparazione**. Le celle vanno a coppie:
# MAGIC - la cella marcata **ERRORE VOLUTO** deve fallire: si leggono il tipo, il messaggio e la riga;
# MAGIC - la cella marcata **ERRORE SILENZIOSO** non dà errori ma produce un risultato sbagliato;
# MAGIC - la cella **Correzione** (o la cella indicata nella nota) deve funzionare **senza errori**, con il risultato indicato.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparazione

# COMMAND ----------

# Cella di preparazione: costanti e collezioni usate nelle sezioni
# In questo capitolo gli import non sono qui: sono l'argomento delle sezioni
ANALYSIS_YEAR = 2024
CANCELLATION_RATE_THRESHOLD = 30.0   # soglia del tasso di cancellazione, in %

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
base_prices = [284.97, 213.91, 236.95]
bookings_2024 = [6, 7, 4]

# Nomi dei giorni in italiano: la posizione nella lista è il numero del giorno (0 = lunedì)
WEEKDAY_NAMES = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]

# Prenotazioni di esempio della struttura di Amalfi, con le date arrivate come testo
raw_bookings = [
    {"booking_id": 1001, "check_in": "2024-03-15", "check_out": "2024-03-18"},
    {"booking_id": 1002, "check_in": "2024-05-31", "check_out": "2024-06-07"},
    {"booking_id": 1003, "check_in": "2024-06-10", "check_out": "2024-06-14"},
    {"booking_id": 1004, "check_in": "2024-02-30", "check_out": "2024-03-02"},
    {"booking_id": 1005, "check_in": "2024-08-10", "check_out": "2024-08-08"},
    {"booking_id": 1006, "check_in": "2024-08-14", "check_out": ""},
    {"booking_id": 1007, "check_in": "2024-12-28", "check_out": "2025-01-02"},
]
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.1 Funzioni sempre pronte e funzioni da caricare
# MAGIC **Ponte SQL**: in SQL le funzioni sono tutte disponibili senza dichiarazioni. Risultato atteso: `2`, `284`, `2024`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ceil(9 / 7)             AS weeks_needed,
# MAGIC        floor(284.97)           AS price_floor,
# MAGIC        year(DATE'2024-03-15')  AS check_in_year

# COMMAND ----------

# MAGIC %md
# MAGIC Proviamo `ceil` come in SQL: la cella deve fallire con un `NameError`, perché `ceil` non è una funzione integrata.

# COMMAND ----------

# ERRORE VOLUTO – ceil non è una funzione integrata di Python
print(ceil(9 / 7))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.2 import: caricare un modulo
# MAGIC `import math` carica il modulo; le sue funzioni si usano con `math.` davanti. Risultati attesi: `2` e `1`.

# COMMAND ----------

import math

print(math.ceil(9 / 7))
print(9 // 7)

# COMMAND ----------

# MAGIC %md
# MAGIC `floor` e `ceil` sui prezzi; `int()` e `floor()` sui numeri negativi. Risultati attesi: `284`, `285`, `-42`, `-43`.

# COMMAND ----------

print(math.floor(284.97))
print(math.ceil(284.97))
print(int(-42.76))
print(math.floor(-42.76))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `CAST` a intero tronca, `floor` va verso il basso. Risultato atteso: `284`, `285`, `-42`, `-43`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT floor(284.97)         AS price_floor,
# MAGIC        ceil(284.97)          AS price_ceil,
# MAGIC        CAST(-42.76 AS INT)   AS amount_int,
# MAGIC        floor(-42.76)         AS amount_floor

# COMMAND ----------

# MAGIC %md
# MAGIC `help()` funziona anche sulle funzioni dei moduli.

# COMMAND ----------

help(math.ceil)

# COMMAND ----------

# MAGIC %md
# MAGIC Dopo `import math` il nome `ceil` da solo non esiste ancora. La cella deve fallire con un `NameError`.

# COMMAND ----------

# ERRORE VOLUTO – import math carica il nome math, non il nome ceil
import math
print(ceil(9 / 7))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: la funzione si raggiunge attraverso il modulo. Risultato atteso: `2`.

# COMMAND ----------

# Correzione: il nome del modulo, un punto, il nome della funzione
print(math.ceil(9 / 7))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.3 from ... import e alias
# MAGIC `from math import ceil, floor` carica due nomi, che si usano senza `math.`. Risultati attesi: `2` e `-43`.

# COMMAND ----------

from math import ceil, floor

print(ceil(9 / 7))
print(floor(-42.76))

# COMMAND ----------

# MAGIC %md
# MAGIC Un alias con `as`: il modulo `math` caricato con il nome `m`. Risultato atteso: `285`.

# COMMAND ----------

import math as m

print(m.ceil(284.97))

# COMMAND ----------

# MAGIC %md
# MAGIC Un nome caricato riusato come variabile: la seconda chiamata deve fallire con un `TypeError`. Output atteso prima del messaggio: `2`.

# COMMAND ----------

# ERRORE VOLUTO – il nome ceil viene riusato per una variabile
ceil = ceil(9 / 7)
print(ceil)
print(ceil(10 / 7))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: si ricarica `ceil` e il risultato va in una variabile con un altro nome. Risultati attesi: `2` e `2`.

# COMMAND ----------

# Correzione: si ricarica la funzione e si usa un altro nome per il risultato
from math import ceil

weeks_needed = ceil(9 / 7)
print(weeks_needed)
print(ceil(10 / 7))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.4 Il tipo date
# MAGIC Il tipo `date` si carica dal modulo `datetime`. Risultati attesi: `2024-03-15` e `<class 'datetime.date'>`.

# COMMAND ----------

from datetime import date

check_in = date(2024, 3, 15)
print(check_in)
print(type(check_in))

# COMMAND ----------

# MAGIC %md
# MAGIC Una data dentro una lista si mostra nella forma lunga `datetime.date(...)`, come i testi con gli apici nel Capitolo 3.

# COMMAND ----------

stay_dates = [date(2024, 3, 15), date(2024, 3, 18)]
print(stay_dates)

# COMMAND ----------

# MAGIC %md
# MAGIC Gli **attributi** `year`, `month`, `day` si scrivono dopo il punto, **senza parentesi**. Risultati attesi: `2024`, `3`, `15`.

# COMMAND ----------

print(check_in.year)
print(check_in.month)
print(check_in.day)

# COMMAND ----------

# MAGIC %md
# MAGIC Il metodo `weekday()` restituisce il giorno della settimana, da **0 = lunedì** a 6 = domenica. Con la lista `WEEKDAY_NAMES` si ottiene il nome. Risultati attesi: `4` e `venerdì`.

# COMMAND ----------

print(check_in.weekday())
print(WEEKDAY_NAMES[check_in.weekday()])

# COMMAND ----------

# MAGIC %md
# MAGIC Le parentesi dopo un attributo: la cella deve fallire con un `TypeError`.

# COMMAND ----------

# ERRORE VOLUTO – year è un attributo, non un metodo
print(check_in.year())

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: l'attributo si legge senza parentesi. Risultato atteso: `2024`.

# COMMAND ----------

# Correzione: year è un attributo, senza parentesi
print(check_in.year)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `weekday` parte da 0 = lunedì, `dayofweek` da 1 = domenica. Risultato atteso: `2024`, `3`, `15`, `4`, `6`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT year(DATE'2024-03-15')       AS check_in_year,
# MAGIC        month(DATE'2024-03-15')      AS check_in_month,
# MAGIC        day(DATE'2024-03-15')        AS check_in_day,
# MAGIC        weekday(DATE'2024-03-15')    AS weekday_num,
# MAGIC        dayofweek(DATE'2024-03-15')  AS dayofweek_num

# COMMAND ----------

# MAGIC %md
# MAGIC `date.today()` restituisce la data di oggi, come `current_date()` in SQL: l'output dipende dal giorno in cui si esegue la cella.

# COMMAND ----------

today = date.today()
print(today)
print(today.year)

# COMMAND ----------

# MAGIC %md
# MAGIC Una data che non esiste: la cella deve fallire con un `ValueError`.

# COMMAND ----------

# ERRORE VOLUTO – febbraio non ha 30 giorni
deadline = date(2024, 2, 30)
print(deadline)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: l'ultimo giorno di febbraio 2024 è il 29 (anno bisestile). Risultato atteso: `2024-02-29`.

# COMMAND ----------

# Correzione: il 2024 è bisestile, febbraio ha 29 giorni
deadline = date(2024, 2, 29)
print(deadline)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.5 Il modulo datetime: da testo a data e ritorno
# MAGIC La forma standard del libro per le date: i tre tipi caricati con una sola riga. La cella non produce output.

# COMMAND ----------

from datetime import date, timedelta, datetime

# COMMAND ----------

# MAGIC %md
# MAGIC Da testo a data con `date.fromisoformat()`: chiude il rimando del Capitolo 1. Risultati attesi: `2024-03-15 <class 'datetime.date'>` e `venerdì`.

# COMMAND ----------

check_in_text = "2024-03-15"   # la data della scheda di Roma del Capitolo 1
check_in = date.fromisoformat(check_in_text)
print(check_in, type(check_in))
print(WEEKDAY_NAMES[check_in.weekday()])

# COMMAND ----------

# MAGIC %md
# MAGIC Da testo in formato italiano a data con `datetime.strptime()` e `.date()`. Risultati attesi: `2024-03-15 00:00:00` e `2024-03-15`.

# COMMAND ----------

italian_text = "15/03/2024"
check_in_with_time = datetime.strptime(italian_text, "%d/%m/%Y")
print(check_in_with_time)
check_in = check_in_with_time.date()
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC Da data a testo: `strftime()` con un formato, `str()` e le f-string con il formato ISO. Risultati attesi: `15/03/2024`, `2024-03-15`, `Arrivo: 2024-03-15`.

# COMMAND ----------

print(check_in.strftime("%d/%m/%Y"))
print(str(check_in))
print(f"Arrivo: {check_in}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `to_date` e `date_format` con i codici di formato di Databricks SQL. Risultato atteso: `2024-03-15` e `15/03/2024`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT to_date('15/03/2024', 'dd/MM/yyyy')          AS check_in,
# MAGIC        date_format(DATE'2024-03-15', 'dd/MM/yyyy')  AS check_in_text

# COMMAND ----------

# MAGIC %md
# MAGIC Un testo in formato italiano passato a `fromisoformat()`: la cella deve fallire con un `ValueError`.

# COMMAND ----------

# ERRORE VOLUTO – fromisoformat() accetta solo il formato ISO
check_in = date.fromisoformat("15/03/2024")
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il testo in formato italiano si converte con `strptime()`. Risultato atteso: `2024-03-15`.

# COMMAND ----------

# Correzione: per il formato italiano si usa strptime() con il formato giusto
check_in = datetime.strptime("15/03/2024", "%d/%m/%Y").date()
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC Un testo che non corrisponde al formato di `strptime()`: la cella deve fallire con un `ValueError`. Il traceback ha due blocchi: il secondo (`File /usr/lib/python3.12/_strptime.py`) è codice del modulo, non nostro.

# COMMAND ----------

# ERRORE VOLUTO – il testo usa i trattini, il formato le barre
check_in = datetime.strptime("15-03-2024", "%d/%m/%Y").date()
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il formato descrive il testo, con i trattini. Risultato atteso: `2024-03-15`.

# COMMAND ----------

# Correzione: il formato usa i trattini, come il testo
check_in = datetime.strptime("15-03-2024", "%d-%m-%Y").date()
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.6 Calcoli con le date
# MAGIC Data + `timedelta` = data. Risultati attesi: `2024-03-18` e `2024-03-01`.

# COMMAND ----------

check_in = date(2024, 3, 15)
nights = 3
check_out = check_in + timedelta(days=nights)
print(check_out)

free_cancellation_until = check_in - timedelta(days=14)
print(free_cancellation_until)

# COMMAND ----------

# MAGIC %md
# MAGIC Una data più un numero: la cella deve fallire con un `TypeError`.

# COMMAND ----------

# ERRORE VOLUTO – a una data si somma un timedelta, non un numero
check_out = check_in + 3
print(check_out)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: i giorni si aggiungono con un `timedelta`. Risultato atteso: `2024-03-18`.

# COMMAND ----------

# Correzione: a una data si somma un timedelta
check_out = check_in + timedelta(days=3)
print(check_out)

# COMMAND ----------

# MAGIC %md
# MAGIC Data − data = `timedelta`; l'attributo `days` contiene il numero di giorni. Risultati attesi: `3 days, 0:00:00`, `<class 'datetime.timedelta'>`, `3`.

# COMMAND ----------

stay_length = check_out - check_in
print(stay_length)
print(type(stay_length))
print(stay_length.days)

# COMMAND ----------

# MAGIC %md
# MAGIC Giorni del 2024: la differenza conta gli intervalli; per un periodo con entrambi gli estremi inclusi si aggiunge 1. Risultati attesi: `365` e `366`.

# COMMAND ----------

first_day = date(ANALYSIS_YEAR, 1, 1)
last_day = date(ANALYSIS_YEAR, 12, 31)
print((last_day - first_day).days)
print((last_day - first_day).days + 1)

# COMMAND ----------

# MAGIC %md
# MAGIC Confronti tra date, anche concatenati come `BETWEEN`. Risultati attesi: `True`, `True`, `True`.

# COMMAND ----------

print(check_in < date(2024, 6, 1))
print(first_day <= check_in <= last_day)
print(check_in.year == ANALYSIS_YEAR)

# COMMAND ----------

# MAGIC %md
# MAGIC Una data confrontata con un testo: la cella deve fallire con un `TypeError`.

# COMMAND ----------

# ERRORE VOLUTO – una data si confronta con una data, non con un testo
print(check_in < "2024-06-01")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: si confrontano due date. Risultati attesi: `True` e `True`.

# COMMAND ----------

# Correzione: il testo si converte in data prima del confronto
print(check_in < date(2024, 6, 1))
print(check_in < date.fromisoformat("2024-06-01"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: gli stessi calcoli con `date_add`, `date_sub`, `datediff` e `BETWEEN`. Risultato atteso: `2024-03-18`, `2024-03-01`, `3`, `366`, `true`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT date_add(DATE'2024-03-15', 3)                       AS check_out,
# MAGIC        date_sub(DATE'2024-03-15', 14)                      AS free_cancellation_until,
# MAGIC        datediff(DATE'2024-03-18', DATE'2024-03-15')        AS nights,
# MAGIC        datediff(DATE'2024-12-31', DATE'2024-01-01') + 1    AS days_2024,
# MAGIC        DATE'2024-03-15' BETWEEN DATE'2024-01-01' AND DATE'2024-12-31' AS in_2024

# COMMAND ----------

# MAGIC %md
# MAGIC Le stesse funzioni sulle colonne di `bookings`. Risultato atteso: `2022-12-29`, `2025-07-30`, `9`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT MIN(check_in)                        AS first_check_in,
# MAGIC        MAX(check_in)                        AS last_check_in,
# MAGIC        MAX(datediff(check_out, check_in))   AS max_nights
# MAGIC FROM samples.wanderbricks.bookings

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.7 La sequenza dei giorni di un soggiorno
# MAGIC Le notti di un soggiorno con `range()` e `timedelta`: una data per giro. Risultato atteso: sette righe, da `2024-05-31 venerdì` a `2024-06-06 giovedì`.

# COMMAND ----------

check_in = date(2024, 5, 31)
check_out = date(2024, 6, 7)
nights = (check_out - check_in).days

for i in range(nights):
    night = check_in + timedelta(days=i)
    print(night, WEEKDAY_NAMES[night.weekday()])

# COMMAND ----------

# MAGIC %md
# MAGIC Un contatore delle notti del fine settimana (venerdì e sabato, `weekday()` 4 e 5). Risultati attesi: `Notti: 7 - di cui nel fine settimana: 2` e `Costo al prezzo base di Amalfi: 1658.65`.

# COMMAND ----------

weekend_nights = 0
for i in range(nights):
    night = check_in + timedelta(days=i)
    if night.weekday() in (4, 5):   # venerdì o sabato
        weekend_nights = weekend_nights + 1

print(f"Notti: {nights} - di cui nel fine settimana: {weekend_nights}")
print(f"Costo al prezzo base di Amalfi: {nights * base_prices[2]:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: la sequenza delle notti con `range(7)`. Risultato atteso: sette righe dal `2024-05-31` (weekday 4) al `2024-06-06` (weekday 3).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT date_add(DATE'2024-05-31', CAST(id AS INT))           AS night,
# MAGIC        weekday(date_add(DATE'2024-05-31', CAST(id AS INT)))  AS weekday_num
# MAGIC FROM range(7)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.8 Data e ora: il tipo datetime
# MAGIC **Ponte SQL**: il tipo delle colonne di data e di data e ora. Risultato atteso: `date` e `timestamp`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT typeof(check_in)    AS check_in_type,
# MAGIC        typeof(created_at)  AS created_at_type
# MAGIC FROM samples.wanderbricks.bookings
# MAGIC LIMIT 1

# COMMAND ----------

# MAGIC %md
# MAGIC Un `datetime`: data e ora. Attributi `hour` e `minute`; il metodo `date()` estrae la data. Risultati attesi: `2024-02-20 14:35:00`, `14 35`, `2024-02-20`.

# COMMAND ----------

created_at = datetime(2024, 2, 20, 14, 35)
print(created_at)
print(created_at.hour, created_at.minute)
print(created_at.date())

# COMMAND ----------

# MAGIC %md
# MAGIC Una data meno un `datetime`: la cella deve fallire con un `TypeError`.

# COMMAND ----------

# ERRORE VOLUTO – una data e un datetime non si sottraggono
check_in = date(2024, 3, 15)
lead_time = check_in - created_at
print(lead_time)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: si sottraggono due date. Risultato atteso: `Anticipo della prenotazione: 24 giorni`.

# COMMAND ----------

# Correzione: la data di creazione senza l'ora
lead_time = check_in - created_at.date()
print(f"Anticipo della prenotazione: {lead_time.days} giorni")

# COMMAND ----------

# MAGIC %md
# MAGIC Differenza tra due `datetime` e durata in ore con `total_seconds()`. Risultati attesi: `1 day, 18:30:00` e `Modificata dopo 42.5 ore`.

# COMMAND ----------

updated_at = datetime(2024, 2, 22, 9, 5)
time_to_update = updated_at - created_at
print(time_to_update)
print(f"Modificata dopo {time_to_update.total_seconds() / 3600} ore")

# COMMAND ----------

# MAGIC %md
# MAGIC `datetime.now()` restituisce data e ora del compute, di solito in UTC: l'output dipende dal momento dell'esecuzione.

# COMMAND ----------

now = datetime.now()
print(now)
print(now.hour)

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: data e ora della sessione SQL. Risultato atteso: data e ora dell'esecuzione, `Etc/UTC` (di solito) e `14`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_timestamp()  AS now,
# MAGIC        current_timezone()   AS timezone,
# MAGIC        hour(TIMESTAMP'2024-02-20 14:35:00') AS created_hour

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.9 Una funzione di conversione: to_date
# MAGIC `to_date`, gemella di `to_float` del Capitolo 6: come `try_cast(... AS DATE)` in SQL. La cella non produce output.

# COMMAND ----------

def to_date(text):
    """Converte un testo in formato ISO (AAAA-MM-GG) in date, come try_cast in SQL.

    Restituisce None se il testo manca (None) o non è una data valida.
    """
    if text is None:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None

# COMMAND ----------

# MAGIC %md
# MAGIC Cinque prove con risultato noto. Risultati attesi: `2024-03-15`, `None`, `None`, `None`, `None`.

# COMMAND ----------

print(to_date("2024-03-15"))
print(to_date("2024-02-30"))
print(to_date(""))
print(to_date("15/03/2024"))
print(to_date(None))

# COMMAND ----------

# MAGIC %md
# MAGIC Conversione delle date di `raw_bookings`, con scarti e date invertite contati. Risultati attesi: due righe scartate (1004, 1006), una da controllare (1005, -2 notti), `Soggiorni validi: 4 - scartati: 2 - date invertite: 1`.

# COMMAND ----------

valid_stays = []
rejected_count = 0
inverted_count = 0
for row in raw_bookings:
    check_in = to_date(row["check_in"])
    check_out = to_date(row["check_out"])
    if check_in is None or check_out is None:
        rejected_count = rejected_count + 1
        print(f"Scartata {row['booking_id']}: date mancanti o non valide")
        continue
    nights = (check_out - check_in).days
    if nights < 0:
        inverted_count = inverted_count + 1
        print(f"Da controllare {row['booking_id']}: date invertite ({nights} notti)")
        continue
    valid_stays.append({"booking_id": row["booking_id"], "check_in": check_in, "nights": nights})

print(f"Soggiorni validi: {len(valid_stays)} - scartati: {rejected_count} - date invertite: {inverted_count}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: le prenotazioni con le date invertite nella copia didattica. Risultato atteso: `8`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS inverted_dates
# MAGIC FROM workspace.libro_python.b_bookings
# MAGIC WHERE check_out < check_in

# COMMAND ----------

# MAGIC %md
# MAGIC **Ponte SQL**: `try_cast` come `to_date`. Risultato atteso: quattro righe; `null` per la data inesistente e per il testo vuoto; `-2` notti per la 1005.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT booking_id,
# MAGIC        try_cast(check_in AS DATE)   AS check_in,
# MAGIC        try_cast(check_out AS DATE)  AS check_out,
# MAGIC        datediff(try_cast(check_out AS DATE), try_cast(check_in AS DATE)) AS nights
# MAGIC FROM VALUES (1001, '2024-03-15', '2024-03-18'),
# MAGIC             (1004, '2024-02-30', '2024-03-02'),
# MAGIC             (1005, '2024-08-10', '2024-08-08'),
# MAGIC             (1006, '2024-08-14', '')
# MAGIC      AS t(booking_id, check_in, check_out)

# COMMAND ----------

# MAGIC %md
# MAGIC Il report dei soggiorni validi: data in formato italiano, giorno di arrivo, notti, arrivi nel fine settimana. Risultato atteso: quattro righe, `Notti totali: 19 - arrivi nel fine settimana: 3`.

# COMMAND ----------

total_nights = 0
weekend_arrivals = 0
for stay in valid_stays:
    arrival = stay["check_in"]
    weekday_name = WEEKDAY_NAMES[arrival.weekday()]
    print(f"{stay['booking_id']}: arrivo {arrival.strftime('%d/%m/%Y')} ({weekday_name}), {stay['nights']} notti")
    total_nights = total_nights + stay["nights"]
    if arrival.weekday() in (4, 5):
        weekend_arrivals = weekend_arrivals + 1

print(f"Notti totali: {total_nights} - arrivi nel fine settimana: {weekend_arrivals}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7.10 Errori comuni con moduli e date
# MAGIC Un modulo con il nome sbagliato: la cella deve fallire con un `ModuleNotFoundError`.

# COMMAND ----------

# ERRORE VOLUTO – il modulo si chiama math, non maths
import maths

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: il nome del modulo è `math`. Risultato atteso: `2`.

# COMMAND ----------

# Correzione: il modulo si chiama math
import math
print(math.ceil(9 / 7))

# COMMAND ----------

# MAGIC %md
# MAGIC `import datetime` dopo la forma standard: il nome `datetime` torna a indicare il modulo. La cella deve fallire con un `AttributeError`.

# COMMAND ----------

# ERRORE VOLUTO – import datetime sostituisce il tipo datetime con il modulo
import datetime
created_at = datetime.strptime("2024-02-20 14:35", "%Y-%m-%d %H:%M")
print(created_at)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: si riesegue la forma standard. Risultato atteso: `2024-02-20 14:35:00`.

# COMMAND ----------

# Correzione: la forma standard rimette nel nome datetime il tipo
from datetime import date, timedelta, datetime

created_at = datetime.strptime("2024-02-20 14:35", "%Y-%m-%d %H:%M")
print(created_at)

# COMMAND ----------

# MAGIC %md
# MAGIC Il nome `date` usato per una variabile: la seconda assegnazione deve fallire con un `TypeError`.

# COMMAND ----------

# ERRORE VOLUTO – il nome date viene riusato per un testo
date = "2024-03-15"
check_out = date(2024, 3, 18)
print(check_out)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: un nome che descrive la data e la forma standard rieseguita. Risultato atteso: `2024-03-15 2024-03-18`.

# COMMAND ----------

# Correzione: si ricarica il tipo date e si usa un nome descrittivo
from datetime import date, timedelta, datetime

check_in_text = "2024-03-15"
check_out = date(2024, 3, 18)
print(check_in_text, check_out)

# COMMAND ----------

# MAGIC %md
# MAGIC Giorno e mese scambiati: la cella deve fallire con un `ValueError`.

# COMMAND ----------

# ERRORE VOLUTO – l'ordine degli argomenti è anno, mese, giorno
check_in = date(2024, 15, 3)
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: anno, mese, giorno. Risultato atteso: `2024-03-15`.

# COMMAND ----------

# Correzione: l'ordine è anno, mese, giorno
check_in = date(2024, 3, 15)
print(check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC Una data confrontata con `==` a un testo: nessun errore, ma il risultato è sempre `False`.

# COMMAND ----------

# ERRORE SILENZIOSO – una data e un testo non sono mai uguali
check_in = date(2024, 3, 15)
if check_in == "2024-03-15":
    print("Arrivo del 15 marzo")
print(check_in == "2024-03-15")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: si confrontano due date. Risultati attesi: `Arrivo del 15 marzo` e `True`.

# COMMAND ----------

# Correzione: una data si confronta con una data
check_in = date(2024, 3, 15)
if check_in == date(2024, 3, 15):
    print("Arrivo del 15 marzo")
print(check_in == date(2024, 3, 15))

# COMMAND ----------

# MAGIC %md
# MAGIC `%M` (minuti) al posto di `%m` (mese): nessun errore, ma il mese diventa `00`.

# COMMAND ----------

# ERRORE SILENZIOSO – %M sono i minuti, %m è il mese
check_in = date(2024, 3, 15)
print(check_in.strftime("%d/%M/%Y"))

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: `%m` è il mese. Risultato atteso: `15/03/2024`.

# COMMAND ----------

# Correzione: %m è il mese
check_in = date(2024, 3, 15)
print(check_in.strftime("%d/%m/%Y"))

# COMMAND ----------

# MAGIC %md
# MAGIC I giorni di giugno senza +1: nessun errore, ma un giorno in meno.

# COMMAND ----------

# ERRORE SILENZIOSO – la differenza conta gli intervalli, non i giorni del periodo
first_day = date(2024, 6, 1)
last_day = date(2024, 6, 30)
print(f"Giorni di giugno: {(last_day - first_day).days}")

# COMMAND ----------

# MAGIC %md
# MAGIC Correzione: per un periodo con gli estremi inclusi si aggiunge 1. Risultato atteso: `Giorni di giugno: 30`.

# COMMAND ----------

# Correzione: i giorni di un periodo con gli estremi inclusi
first_day = date(2024, 6, 1)
last_day = date(2024, 6, 30)
print(f"Giorni di giugno: {(last_day - first_day).days + 1}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Riepilogo
# MAGIC - Le **funzioni integrate** (`print`, `len`, `round`...) sono sempre disponibili; le altre stanno nei **moduli** e si caricano con `import`. Un nome non caricato dà `NameError`, un modulo che non esiste `ModuleNotFoundError`.
# MAGIC - `import math` → `math.ceil(...)`; `from math import ceil` → `ceil(...)`; `import math as m` → alias, solo se è una convenzione diffusa. Gli import vivono nella memoria del compute: si scrivono nella cella di preparazione (eccezione in questo capitolo).
# MAGIC - Un nome caricato o un tipo riassegnato a una variabile: `'int' object is not callable`, `'str' object is not callable`.
# MAGIC - Forma standard per le date: `from datetime import date, timedelta, datetime`. `date(anno, mese, giorno)`; attributi `year`, `month`, `day` senza parentesi; `weekday()` da 0 = lunedì (in SQL `dayofweek` parte da 1 = domenica).
# MAGIC - Testo → data: `date.fromisoformat()` (formato ISO), `datetime.strptime(testo, formato).date()`. Data → testo: `strftime(formato)`. Codici `%d %m %Y %H %M %S`; in SQL i codici sono diversi.
# MAGIC - Data ± `timedelta(days=n)`; data − data = `timedelta`, attributo `days`. Notti = differenza; giorni di un periodo = differenza + 1. Le date si confrontano con le date, mai con i testi.
# MAGIC - `datetime` per data e ora; `date()` ne estrae la data; `total_seconds()` per le durate; `datetime.now()` usa l'orologio del compute (di solito UTC).
# MAGIC - `to_date` è il `try_cast` del libro per le date; le date invertite si contano a parte.
