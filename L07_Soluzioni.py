# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 7 – Soluzioni
# MAGIC
# MAGIC Soluzioni commentate degli esercizi del Capitolo 7 (le stesse dell'Appendice A). Prerequisiti: notebook collegato a **Serverless**.
# MAGIC Si esegue per prima la cella di preparazione, poi **una cella alla volta**: le celle marcate **ERRORE VOLUTO** ed **ERRORE SILENZIOSO** dell'esercizio 8 sono riportate come nel notebook degli esercizi, con la soluzione subito sotto. Non usare Run all.

# COMMAND ----------

# Cella di preparazione: import, costanti e collezioni usate negli esercizi
# Il modulo math non è caricato qui: lo caricano gli esercizi 1 e 2
from datetime import date, timedelta, datetime

ANALYSIS_YEAR = 2024

# Strutture guida, sempre nell'ordine Roma, Sardegna, Amalfi
property_titles = ["Historic Inn in Rome", "Bungalow in Sardinia", "Beach House in Amalfi"]
base_prices = [284.97, 213.91, 236.95]

# Nomi dei giorni in italiano: la posizione nella lista è il numero del giorno (0 = lunedì)
WEEKDAY_NAMES = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
print("Preparazione completata")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Arrotondare con math
# MAGIC La lista `stay_nights` (cella sotto) contiene le notti di cinque soggiorni di esempio.
# MAGIC 1. Caricare il modulo `math` con `import math`.
# MAGIC 2. Con due list comprehension, calcolare le settimane **occupate** da ogni soggiorno (`math.ceil` delle notti diviso 7) e le settimane **complete** (divisione intera `//`).
# MAGIC 3. Stampare i prezzi base delle strutture guida arrotondati per difetto (`math.floor`) e per eccesso (`math.ceil`).
# MAGIC 4. Per il rimborso di esempio `refund = -15.5`, stampare sulla stessa riga `int(refund)`, `math.floor(refund)` e `math.ceil(refund)`.

# COMMAND ----------

stay_nights = [3, 7, 9, 14, 2]   # valori di esempio

# COMMAND ----------

# Il modulo si carica una volta; le funzioni si usano con il prefisso math.
import math

# Settimane occupate (arrotondamento per eccesso) e settimane complete (divisione intera)
weeks_occupied = [math.ceil(nights / 7) for nights in stay_nights]
full_weeks = [nights // 7 for nights in stay_nights]
print(weeks_occupied)
print(full_weeks)

# Prezzi base arrotondati per difetto e per eccesso
print([math.floor(price) for price in base_prices])
print([math.ceil(price) for price in base_prices])

# Con un negativo int() tronca verso lo zero, floor() va verso il basso
refund = -15.5
print(int(refund), math.floor(refund), math.ceil(refund))

# COMMAND ----------

# Verifica: risultato atteso
print([1, 1, 2, 2, 1])
print([0, 1, 1, 2, 0])
print([284, 213, 236])
print([285, 214, 237])
print(-15, -16, -15)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: gli stessi arrotondamenti in SQL (2, 1, 213, 214, -15, -16)
# MAGIC SELECT ceil(9 / 7)          AS weeks_occupied,
# MAGIC        9 div 7              AS full_weeks,
# MAGIC        floor(213.91)        AS price_floor,
# MAGIC        ceil(213.91)         AS price_ceil,
# MAGIC        CAST(-15.5 AS INT)   AS refund_int,
# MAGIC        floor(-15.5)         AS refund_floor

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Forme di import
# MAGIC Nota: se nell'esercizio 1 il nome `floor` è stato caricato con `from math import floor`, la cella 2a non fallisce, perché il nome è già nella memoria del compute (sezione 7.3).
# MAGIC 1. Eseguire le celle 2a e 2b e annotare nella cella di risposta il **tipo** di ciascun errore.
# MAGIC 2. Scrivere nella cella di correzione: la 2a corretta caricando `floor` con `from math import floor`; la 2b corretta usando per il risultato una variabile con un altro nome (`sardinia_floor`) e ricaricando `floor`.
# MAGIC 3. Infine calcolare `floor(236.95)` nelle due forme: con `import math` e il prefisso, e con il nome caricato da `from math import floor`.

# COMMAND ----------

# ERRORE VOLUTO – cella 2a (il prezzo base della Sardegna arrotondato per difetto)
print(floor(213.91))

# COMMAND ----------

# ERRORE VOLUTO – cella 2b
from math import floor
floor = floor(213.91)
print(floor)
print(floor(236.95))

# COMMAND ----------

# 2a: NameError - floor non è una funzione integrata e non è stato caricato
from math import floor
print(floor(213.91))

# 2b: TypeError ('int' object is not callable) - il nome floor è stato riassegnato a un numero
from math import floor           # si ricarica la funzione
sardinia_floor = floor(213.91)   # il risultato va in una variabile con un altro nome
print(sardinia_floor)
print(floor(236.95))

# Le due forme di import danno lo stesso risultato
import math
print(math.floor(236.95))   # forma con il prefisso del modulo
print(floor(236.95))        # forma con il nome caricato

# COMMAND ----------

# Verifica: risultato atteso
print("2a: NameError - 2b: TypeError ('int' object is not callable)")
print(213)
print(213)
print(236)
print(236)
print(236)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – Ferragosto 2024
# MAGIC 1. Creare la data del 15 agosto 2024 con `date()` e stamparla.
# MAGIC 2. Stampare sulla stessa riga anno, mese e giorno, letti con gli attributi.
# MAGIC 3. Stampare sulla stessa riga il numero del giorno della settimana (`weekday()`) e il suo nome, letto da `WEEKDAY_NAMES`.
# MAGIC 4. Stampare la data in formato italiano con `strftime()`.
# MAGIC 5. Calcolare il numero del giorno nell'anno (1 per il 1° gennaio) e stampare `Giorno dell'anno: ...`.

# COMMAND ----------

ferragosto = date(2024, 8, 15)
print(ferragosto)

# Attributi: si leggono senza parentesi
print(ferragosto.year, ferragosto.month, ferragosto.day)

# Metodo: si chiama con le parentesi; 0 = lunedì, quindi 3 = giovedì
print(ferragosto.weekday(), WEEKDAY_NAMES[ferragosto.weekday()])

# Da data a testo in formato italiano
print(ferragosto.strftime("%d/%m/%Y"))

# Il giorno dell'anno conta anche il 1° gennaio: differenza + 1
day_of_year = (ferragosto - date(2024, 1, 1)).days + 1
print(f"Giorno dell'anno: {day_of_year}")

# COMMAND ----------

# Verifica: risultato atteso
print("2024-08-15")
print(2024, 8, 15)
print(3, "giovedì")
print("15/08/2024")
print("Giorno dell'anno: 228")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: 3, 5, 15/08/2024, 228 (dayofweek parte da 1 = domenica)
# MAGIC SELECT weekday(DATE'2024-08-15')                    AS weekday_num,
# MAGIC        dayofweek(DATE'2024-08-15')                  AS dayofweek_num,
# MAGIC        date_format(DATE'2024-08-15', 'dd/MM/yyyy')  AS italian_text,
# MAGIC        dayofyear(DATE'2024-08-15')                  AS day_of_year

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Date in formato italiano
# MAGIC La lista `italian_dates` (cella sotto) contiene tre date scritte in formato italiano.
# MAGIC 1. Convertire i testi in date con `datetime.strptime(...).date()`, raccogliendole nella lista `converted_dates`.
# MAGIC 2. Con un ciclo su `converted_dates`, stampare per ogni data: la data in formato ISO, il nome del giorno e i giorni trascorsi dalla prima data della lista (0 per la prima).

# COMMAND ----------

italian_dates = ["01/06/2024", "15/08/2024", "31/12/2024"]   # valori di esempio

# COMMAND ----------

# Da testo italiano a data: strptime con il formato, poi date() per togliere l'ora
converted_dates = []
for text in italian_dates:
    converted_dates.append(datetime.strptime(text, "%d/%m/%Y").date())

first_date = converted_dates[0]
for converted in converted_dates:
    days_from_first = (converted - first_date).days
    print(converted, WEEKDAY_NAMES[converted.weekday()], days_from_first)

# COMMAND ----------

# Verifica: risultato atteso
print("2024-06-01 sabato 0")
print("2024-08-15 giovedì 75")
print("2024-12-31 martedì 213")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: le stesse date con to_date (weekday 5, 3, 1; giorni 0, 75, 213)
# MAGIC SELECT to_date(italian_text, 'dd/MM/yyyy')                                AS converted,
# MAGIC        weekday(to_date(italian_text, 'dd/MM/yyyy'))                       AS weekday_num,
# MAGIC        datediff(to_date(italian_text, 'dd/MM/yyyy'), DATE'2024-06-01')    AS days_from_first
# MAGIC FROM VALUES ('01/06/2024'), ('15/08/2024'), ('31/12/2024') AS t(italian_text)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – Un soggiorno in Sardegna
# MAGIC Un soggiorno di esempio al Bungalow in Sardinia arriva il 26 luglio 2024 e dura 9 notti.
# MAGIC 1. Calcolare e stampare la data di partenza.
# MAGIC 2. Calcolare e stampare l'ultimo giorno di cancellazione gratuita, 14 giorni prima dell'arrivo.
# MAGIC 3. Stampare il costo del soggiorno al prezzo base della Sardegna (`base_prices[1]`), con due decimali.
# MAGIC 4. Stampare se l'arrivo è nel 2024, con un confronto concatenato tra il 1° gennaio e il 31 dicembre di `ANALYSIS_YEAR`.
# MAGIC 5. Stampare i giorni di luglio 2024, calcolati con una differenza tra il 1° e il 31 luglio.
# MAGIC 6. Un secondo soggiorno è arrivato come testo: `"2024-09-02"` → `"2024-09-06"`. Convertire i testi con `date.fromisoformat()` e stampare le notti.

# COMMAND ----------

check_in = date(2024, 7, 26)
nights = 9

# Partenza e ultimo giorno di cancellazione gratuita: data ± timedelta
check_out = check_in + timedelta(days=nights)
free_cancellation_until = check_in - timedelta(days=14)
print(check_out)
print(free_cancellation_until)

# Costo al prezzo base della Sardegna
print(f"{nights * base_prices[1]:.2f}")

# Confronto concatenato, come BETWEEN con gli estremi inclusi
print(date(ANALYSIS_YEAR, 1, 1) <= check_in <= date(ANALYSIS_YEAR, 12, 31))

# Giorni di un periodo con gli estremi inclusi: differenza + 1
print((date(2024, 7, 31) - date(2024, 7, 1)).days + 1)

# Notti da due date arrivate come testo: differenza, senza +1
second_check_in = date.fromisoformat("2024-09-02")
second_check_out = date.fromisoformat("2024-09-06")
print((second_check_out - second_check_in).days)

# COMMAND ----------

# Verifica: risultato atteso
print("2024-08-04")
print("2024-07-12")
print("1925.19")
print(True)
print(31)
print(4)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: 2024-08-04, 2024-07-12, 31, 4
# MAGIC SELECT date_add(DATE'2024-07-26', 9)                       AS check_out,
# MAGIC        date_sub(DATE'2024-07-26', 14)                      AS free_cancellation_until,
# MAGIC        datediff(DATE'2024-07-31', DATE'2024-07-01') + 1    AS days_in_july,
# MAGIC        datediff(DATE'2024-09-06', DATE'2024-09-02')        AS second_stay_nights

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Un soggiorno a cavallo dell'anno
# MAGIC La prenotazione di esempio 1007 del capitolo arriva ad Amalfi il 28 dicembre 2024 e riparte il 2 gennaio 2025.
# MAGIC 1. Con `range()` e `timedelta`, stampare ogni notte del soggiorno con il nome del giorno.
# MAGIC 2. Nello stesso ciclo contare le notti del fine settimana (venerdì e sabato) e le notti che cadono in `ANALYSIS_YEAR`.
# MAGIC 3. Stampare `Notti: ... - nel fine settimana: ...` e `Notti nel 2024: ... (costo) - notti nel 2025: ... (costo)`, con il costo al prezzo base di Amalfi (`base_prices[2]`) e due decimali.

# COMMAND ----------

check_in = date(2024, 12, 28)
check_out = date(2025, 1, 2)
nights = (check_out - check_in).days

weekend_nights = 0
nights_in_year = 0
for i in range(nights):
    night = check_in + timedelta(days=i)   # la notte numero i del soggiorno
    print(night, WEEKDAY_NAMES[night.weekday()])
    if night.weekday() in (4, 5):          # venerdì o sabato
        weekend_nights = weekend_nights + 1
    if night.year == ANALYSIS_YEAR:
        nights_in_year = nights_in_year + 1

nights_next_year = nights - nights_in_year
price = base_prices[2]
print(f"Notti: {nights} - nel fine settimana: {weekend_nights}")
print(f"Notti nel 2024: {nights_in_year} ({nights_in_year * price:.2f}) - notti nel 2025: {nights_next_year} ({nights_next_year * price:.2f})")

# COMMAND ----------

# Verifica: risultato atteso
print("2024-12-28 sabato")
print("2024-12-29 domenica")
print("2024-12-30 lunedì")
print("2024-12-31 martedì")
print("2025-01-01 mercoledì")
print("Notti: 5 - nel fine settimana: 1")
print("Notti nel 2024: 4 (947.80) - notti nel 2025: 1 (236.95)")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica: notti per anno (2024: 4, 2025: 1)
# MAGIC SELECT year(date_add(DATE'2024-12-28', CAST(id AS INT)))  AS night_year,
# MAGIC        COUNT(*)                                           AS nights
# MAGIC FROM range(5)
# MAGIC GROUP BY 1
# MAGIC ORDER BY 1

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – L'anticipo delle richieste
# MAGIC La lista `raw_requests` (cella sotto) contiene sette richieste di prenotazione di esempio, con la data e l'ora della richiesta (`created_at`) e la data di arrivo (`check_in`) scritte in formato italiano.
# MAGIC 1. Definire `to_italian_date(text)` e `to_italian_datetime(text)`, gemelle di `to_date`: convertono un testo con `strptime()` (formati `"%d/%m/%Y"` e `"%d/%m/%Y %H:%M"`; la prima restituisce una `date`) e restituiscono `None` se il testo manca o non è valido. Scrivere una docstring per ciascuna.
# MAGIC 2. Con un ciclo, convertire i due valori di ogni riga; se uno dei due è `None`, stampare `Scartata ...` con il `booking_id`, contare lo scarto e passare alla riga successiva.
# MAGIC 3. Per le righe valide calcolare l'anticipo in giorni (arrivo meno data della richiesta) e la fascia: `"ultimo minuto"` se l'anticipo è minore di 7 giorni, altrimenti `"anticipo"`. Stampare `booking_id: giorni di anticipo ... (fascia)`.
# MAGIC 4. Contare le righe per fascia in un dizionario, contare le richieste serali (fatte dalle 18 in poi) e calcolare l'anticipo medio con un decimale.

# COMMAND ----------

raw_requests = [   # valori di esempio
    {"booking_id": 1001, "created_at": "20/02/2024 14:35", "check_in": "15/03/2024"},
    {"booking_id": 1002, "created_at": "02/05/2024 09:10", "check_in": "31/05/2024"},
    {"booking_id": 1003, "created_at": "08/06/2024 22:45", "check_in": "10/06/2024"},
    {"booking_id": 1004, "created_at": "15/02/2024 11:00", "check_in": "30/02/2024"},
    {"booking_id": 1005, "created_at": "28/07/2024 08:20", "check_in": "10/08/2024"},
    {"booking_id": 1006, "created_at": "", "check_in": "14/08/2024"},
    {"booking_id": 1007, "created_at": "27/12/2024 19:05", "check_in": "28/12/2024"},
]

# COMMAND ----------

def to_italian_date(text):
    """Converte un testo GG/MM/AAAA in date; None se manca o non è una data valida."""
    if text is None:
        return None
    try:
        return datetime.strptime(text, "%d/%m/%Y").date()
    except ValueError:
        return None


def to_italian_datetime(text):
    """Converte un testo GG/MM/AAAA HH:MM in datetime; None se manca o non è valido."""
    if text is None:
        return None
    try:
        return datetime.strptime(text, "%d/%m/%Y %H:%M")
    except ValueError:
        return None


rejected_count = 0
lead_times = []
count_by_band = {}
evening_requests = 0
for row in raw_requests:
    created_at = to_italian_datetime(row["created_at"])
    check_in = to_italian_date(row["check_in"])
    if created_at is None or check_in is None:
        rejected_count = rejected_count + 1
        print(f"Scartata {row['booking_id']}")
        continue
    lead_days = (check_in - created_at.date()).days   # due date: date() toglie l'ora
    if lead_days < 7:
        band = "ultimo minuto"
    else:
        band = "anticipo"
    print(f"{row['booking_id']}: giorni di anticipo {lead_days} ({band})")
    lead_times.append(lead_days)
    if band in count_by_band:
        count_by_band[band] = count_by_band[band] + 1
    else:
        count_by_band[band] = 1
    if created_at.hour >= 18:
        evening_requests = evening_requests + 1

print(f"Valide: {len(lead_times)} - scartate: {rejected_count}")
print(count_by_band)
print(f"Richieste serali (dalle 18): {evening_requests}")
print(f"Anticipo medio: {sum(lead_times) / len(lead_times):.1f} giorni")

# COMMAND ----------

# Verifica: risultato atteso
print("1001: giorni di anticipo 24 (anticipo)")
print("1002: giorni di anticipo 29 (anticipo)")
print("1003: giorni di anticipo 2 (ultimo minuto)")
print("Scartata 1004")
print("1005: giorni di anticipo 13 (anticipo)")
print("Scartata 1006")
print("1007: giorni di anticipo 1 (ultimo minuto)")
print("Valide: 5 - scartate: 2")
print({'anticipo': 3, 'ultimo minuto': 2})
print("Richieste serali (dalle 18): 2")
print("Anticipo medio: 13.8 giorni")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verifica sulle cinque righe valide: 5, 2, 2, 13.8
# MAGIC SELECT COUNT(*) AS valid_requests,
# MAGIC        SUM(CASE WHEN datediff(to_date(check_in, 'dd/MM/yyyy'), to_date(created_at, 'dd/MM/yyyy HH:mm')) < 7
# MAGIC                 THEN 1 ELSE 0 END) AS last_minute,
# MAGIC        SUM(CASE WHEN hour(to_timestamp(created_at, 'dd/MM/yyyy HH:mm')) >= 18
# MAGIC                 THEN 1 ELSE 0 END) AS evening_requests,
# MAGIC        ROUND(AVG(datediff(to_date(check_in, 'dd/MM/yyyy'), to_date(created_at, 'dd/MM/yyyy HH:mm'))), 1) AS avg_lead_days
# MAGIC FROM VALUES ('20/02/2024 14:35', '15/03/2024'),
# MAGIC             ('02/05/2024 09:10', '31/05/2024'),
# MAGIC             ('08/06/2024 22:45', '10/06/2024'),
# MAGIC             ('28/07/2024 08:20', '10/08/2024'),
# MAGIC             ('27/12/2024 19:05', '28/12/2024')
# MAGIC      AS t(created_at, check_in)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC Le prime quattro celle seguenti producono un errore, le ultime due un **errore silenzioso**. Eseguirle una per una, annotare tipo, messaggio e riga (o il risultato sbagliato) e scrivere sotto la versione corretta.
# MAGIC
# MAGIC **Risultato atteso delle correzioni**: `2`; `2024-06-14`; `31/12/2024`; `22`; `10/06/2024`; `Arrivi del 10 giugno: 2`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a (le settimane occupate da 9 notti)
import Math
print(Math.ceil(9 / 7))

# COMMAND ----------

# Correzione 8a - ModuleNotFoundError: i nomi dei moduli distinguono le maiuscole
import math
print(math.ceil(9 / 7))

# COMMAND ----------

# ERRORE VOLUTO – cella 8b (la partenza dopo 4 notti)
check_in = date(2024, 6, 10)
check_out = check_in + 4
print(check_out)

# COMMAND ----------

# Correzione 8b - TypeError: a una data si somma un timedelta, non un numero
check_in = date(2024, 6, 10)
check_out = check_in + timedelta(days=4)
print(check_out)

# COMMAND ----------

# ERRORE VOLUTO – cella 8c (il 31 dicembre 2024)
last_day = date(2024, 31, 12)
print(last_day.strftime("%d/%m/%Y"))

# COMMAND ----------

# Correzione 8c - ValueError (month must be in 1..12): l'ordine è anno, mese, giorno
last_day = date(2024, 12, 31)
print(last_day.strftime("%d/%m/%Y"))

# COMMAND ----------

# ERRORE VOLUTO – cella 8d (l'ora di una richiesta)
import datetime
created_at = datetime.strptime("08/06/2024 22:45", "%d/%m/%Y %H:%M")
print(created_at.hour)

# COMMAND ----------

# Correzione 8d - AttributeError: import datetime ha messo il modulo nel nome datetime;
# la forma standard rimette il tipo
from datetime import date, timedelta, datetime
created_at = datetime.strptime("08/06/2024 22:45", "%d/%m/%Y %H:%M")
print(created_at.hour)

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e (la data di arrivo in formato italiano)
check_in = date(2024, 6, 10)
print(check_in.strftime("%d/%M/%Y"))

# COMMAND ----------

# Correzione 8e - %M sono i minuti (00 per una date), %m è il mese
check_in = date(2024, 6, 10)
print(check_in.strftime("%d/%m/%Y"))

# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f (quanti arrivi il 10 giugno 2024)
arrivals = [date(2024, 6, 10), date(2024, 6, 14), date(2024, 6, 10)]
count = 0
for arrival in arrivals:
    if arrival == "2024-06-10":
        count = count + 1
print(f"Arrivi del 10 giugno: {count}")

# COMMAND ----------

# Correzione 8f - una data non è mai uguale a un testo: si confronta con una data
arrivals = [date(2024, 6, 10), date(2024, 6, 14), date(2024, 6, 10)]
count = 0
for arrival in arrivals:
    if arrival == date(2024, 6, 10):
        count = count + 1
print(f"Arrivi del 10 giugno: {count}")
