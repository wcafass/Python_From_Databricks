# Databricks notebook source
# MAGIC %md
# MAGIC # Capitolo 13 – Esercizi
# MAGIC
# MAGIC Esercizi del Capitolo 13 di *Oltre la SELECT* (Introduzione al Machine Learning). Si svolgono su una copia creata con **Clone** (per esempio `L13_Esercizi_svolti`), nella cartella `Libro_Python`. Prerequisiti: Serverless; `L11_Progetto_Finale` eseguito almeno una volta; `utils` nella stessa cartella.
# MAGIC
# MAGIC Si esegue prima la cella `%run ./utils`, poi la cella di preparazione, poi gli esercizi, una cella alla volta. Le soluzioni sono nell'Appendice A e nel notebook `L13_Soluzioni`.

# COMMAND ----------

# MAGIC %run ./utils

# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (alla prima esecuzione di `set_experiment` in assoluto può comparire anche la riga `INFO` di creazione dell'esperimento):
# MAGIC ```
# MAGIC (18163, 9) (18163, 23)
# MAGIC ```

# COMMAND ----------

# Librerie, costanti e dati degli esercizi (come nel notebook del capitolo)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score
import mlflow

PRICE_TARGET = "base_price"
NUMERIC_FEATURES = ["bedrooms", "bathrooms", "max_guests"]
CATEGORICAL_FEATURES = ["property_type", "country"]
TEST_SIZE = 0.2
RANDOM_STATE = 42
current_user = spark.sql("SELECT current_user()").collect()[0][0]
EXPERIMENT_PATH = f"/Users/{current_user}/libro_python_capitolo_13"

properties_ml_df = (
    spark.table(PROPERTIES_TABLE)
    .join(
        spark.table(DESTINATIONS_TABLE).select("destination_id", "destination", "country"),
        on="destination_id",
        how="inner",
    )
    .withColumn("base_price", F.round(F.col("base_price").cast("double"), 2))
    .select("property_id", "title", "property_type", "bedrooms", "bathrooms",
            "max_guests", "destination", "country", "base_price")
    .orderBy("property_id")
)
properties_pd = properties_ml_df.toPandas()
y = properties_pd[PRICE_TARGET]
X_full = pd.get_dummies(
    properties_pd[NUMERIC_FEATURES + CATEGORICAL_FEATURES],
    columns=CATEGORICAL_FEATURES,
    drop_first=True,
    dtype=int,
)

def evaluate_regression(model, X_eval, y_eval):
    """Restituisce MAE e R² di un modello di regressione su un insieme di dati."""
    predictions = model.predict(X_eval)
    return {
        "mae": round(mean_absolute_error(y_eval, predictions), 2),
        "r2": round(r2_score(y_eval, predictions), 3),
    }

def train_and_log(features_df, target, run_name):
    """Divide i dati, addestra una regressione lineare, la valuta sul test e registra il run in MLflow."""
    X_train, X_test, y_train, y_test = train_test_split(
        features_df, target, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    metrics = evaluate_regression(model, X_test, y_test)
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("model", "LinearRegression")
        mlflow.log_param("n_features", features_df.shape[1])
        mlflow.log_metric("mae", metrics["mae"])
        mlflow.log_metric("r2", metrics["r2"])
    print(f"{run_name:<28}{features_df.shape[1]:>4}{metrics['mae']:>8}{metrics['r2']:>8}")

mlflow.set_experiment(EXPERIMENT_PATH)
print(properties_pd.shape, X_full.shape)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 1 ★ – Le strutture italiane in pandas
# MAGIC
# MAGIC Si filtrino in Spark le strutture con `country` uguale a `Italy`, le si porti in pandas in `italy_pd` e si stampino la forma della tabella e il prezzo base medio (arrotondato a due decimali), minimo e massimo. *Risultato atteso:* `(1008, 9)` e `192.34 110.06 517.6`; la cella di verifica in Spark dà `1008` e `192.34`.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output (griglia):
# MAGIC ```
# MAGIC property_count  average_price
# MAGIC 1008            192.34
# MAGIC ```

# COMMAND ----------

# Verifica
display(
    properties_ml_df
    .filter(F.col("country") == "Italy")
    .agg(F.count("*").alias("property_count"), F.round(F.avg("base_price"), 2).alias("average_price"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 2 ★ – Un'altra divisione
# MAGIC
# MAGIC Con le tre variabili numeriche, si dividano i dati tenendo per il test il 25% delle righe (con `random_state=RANDOM_STATE`). Si stampino le forme delle tabelle delle variabili, il prezzo medio dei dati di addestramento e il MAE del modello di riferimento. *Risultato atteso:* `(13622, 3) (4541, 3)`, `181.72`, `40.46`.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 3 ★ – La mediana come riferimento
# MAGIC
# MAGIC Con la divisione del capitolo (20% di test), si calcolino la media e la **mediana** (metodo `median()` di una Series) dei prezzi di addestramento, e il MAE dei due modelli di riferimento che danno a tutte le strutture l'una o l'altra. Quale dei due sbaglia meno? *Risultato atteso:* `181.53 171.71`; MAE `40.6` con la media e `39.95` con la mediana. La mediana è più bassa della media perché pochi prezzi molto alti alzano la media; per il MAE è la scelta migliore.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 4 ★★ – Il modello dei bagni
# MAGIC
# MAGIC Si addestri una regressione lineare con la sola variabile `bathrooms` e se ne stampino l'intercetta, il coefficiente e la valutazione sul test. È migliore o peggiore del modello delle camere? *Risultato atteso:* intercetta `139.27`, coefficiente `33.57`, `{'mae': 38.36, 'r2': 0.126}`: peggiore del modello delle camere (33.94 e 0.326), perché quasi otto strutture su dieci hanno un solo bagno.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 5 ★★ – La destinazione al posto del paese
# MAGIC
# MAGIC Si costruisca la tabella delle variabili con le tre numeriche, il tipo di struttura e la **destinazione** al posto del paese, la si divida, si addestri il modello e lo si valuti; poi si calcolino le previsioni per le tre strutture guida, preparandole con `pd.get_dummies` e `reindex` sulle colonne della nuova tabella. *Risultato atteso:* `(18163, 47)`; `{'mae': 10.73, 'r2': 0.925}`; previsioni `287.09` (Roma), `237.65` (Amalfi), `224.43` (Sardegna). Con la destinazione il modello distingue Amalfi dal resto d'Italia, e la previsione per la casa di Amalfi si avvicina molto al prezzo reale (236.95).

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 6 ★★ – Tre run in MLflow
# MAGIC
# MAGIC Con la funzione `train_and_log` si registrino nell'esperimento del capitolo tre run: `solo_bagni` (la sola variabile `bathrooms`), `numeriche_e_tipo` (le tre numeriche e il tipo di struttura, codificato con `pd.get_dummies`) e `numeriche_tipo_destinazione` (la tabella dell'esercizio 5). Si aprano i run nell'interfaccia e li si confronti; nel notebook si leggano gli ultimi tre run con `mlflow.search_runs`. *Risultato atteso:* `solo_bagni 1 38.36 0.126`, `numeriche_e_tipo 6 28.52 0.506`, `numeriche_tipo_destinazione 47 10.73 0.925`; la verifica stampa `True` e la griglia dei tre run, dal più recente.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC Risultato atteso – output: `True`, poi la griglia dei tre run più recenti (se l'esercizio è stato eseguito una volta sola):
# MAGIC ```
# MAGIC tags.mlflow.runName          params.n_features  metrics.mae  metrics.r2
# MAGIC numeriche_tipo_destinazione  47                 10.73        0.925
# MAGIC numeriche_e_tipo             6                  28.52        0.506
# MAGIC solo_bagni                   1                  38.36        0.126
# MAGIC ```

# COMMAND ----------

# Verifica: i run dell'esperimento, dal più recente
runs_pd = mlflow.search_runs(experiment_names=[EXPERIMENT_PATH])
print(len(runs_pd) >= 3)
display(runs_pd[["tags.mlflow.runName", "params.n_features", "metrics.mae", "metrics.r2"]].head(3))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 7 ★★★ – Una classificazione che funziona
# MAGIC
# MAGIC Si costruisca l'obiettivo `is_high_price`, 1 per le strutture con prezzo base di almeno 250 (la fascia alta del Capitolo 2) e 0 per le altre, con una list comprehension. Si divida `X_full` con questo obiettivo, si calcoli l'accuratezza del modello di riferimento, si addestri una regressione logistica e se ne calcolino l'accuratezza, il numero delle strutture previste in fascia alta e il numero di quelle previste correttamente in fascia alta. Si confronti il risultato con quello delle cancellazioni. *Risultato atteso:* `1894 10.4` (strutture in fascia alta e percentuale); `389 3633` nei dati di test; accuratezza di riferimento `0.8929`, del modello `0.9557`; `288` previste in fascia alta, di cui `258` corrette. Qui il modello batte il riferimento, perché le variabili contengono informazione sul prezzo; ma l'accuratezza di riferimento, già all'89%, mostra quanto questa misura inganni quando una delle due risposte è rara.

# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# Scrivere qui la soluzione


# COMMAND ----------

# MAGIC %md
# MAGIC ## Esercizio 8 ★★★ – Trova gli errori
# MAGIC
# MAGIC Il notebook contiene tre celle che producono un errore e tre che producono un errore silenzioso. Per ciascuna si esegua la cella, si annotino il tipo dell'errore e il messaggio (o il risultato sbagliato) e si scriva sotto la versione corretta.
# MAGIC
# MAGIC *Risultato atteso:* 8a `KeyError: "['bedroom'] not in index"`; 8b `ValueError: could not convert string to float: 'Spain'`; 8c `ValueError: Expected a 2-dimensional container but got  instead...` (sopra il messaggio può comparire l'avviso `UserWarning: X does not have valid feature names, but LinearRegression was fitted with feature names`); 8d nessun errore ma `{'mae': 0.0, 'r2': 1.0}`, un modello perfetto perché tra le variabili c'è il prezzo stesso; 8e nessun errore ma `-0.803` invece di `0.326`, perché i valori reali e le previsioni sono scambiati; 8f nessun errore ma `{'mae': 33.24, 'r2': 0.369}`, la valutazione sui dati di addestramento, migliore di quella vera. Le celle corrette danno: 8a `(18163, 3)`; 8b `(18163, 18)` (la tabella con le camere e i 17 paesi codificati); 8c `[198.27 235.68]`; 8d `{'mae': 12.67, 'r2': 0.89}`; 8e `0.326`; 8f `{'mae': 33.94, 'r2': 0.326}`.

# COMMAND ----------

# ERRORE VOLUTO – cella 8a
X_rooms = properties_pd[["bedroom", "bathrooms", "max_guests"]]

# COMMAND ----------

# Correzione 8a


# COMMAND ----------

# ERRORE VOLUTO – cella 8b
country_X = properties_pd[["bedrooms", "country"]]
LinearRegression().fit(country_X, y)

# COMMAND ----------

# Correzione 8b


# COMMAND ----------

# ERRORE VOLUTO – cella 8c
rooms_model = LinearRegression().fit(properties_pd[["bedrooms"]], y)
new_rooms = pd.DataFrame({"bedrooms": [2, 3]})
rooms_model.predict(new_rooms["bedrooms"])

# COMMAND ----------

# Correzione 8c


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8d
target_X = X_full.copy()
target_X["base_price"] = y
t_X_train, t_X_test, t_y_train, t_y_test = train_test_split(
    target_X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
target_model = LinearRegression().fit(t_X_train, t_y_train)
print(evaluate_regression(target_model, t_X_test, t_y_test))

# COMMAND ----------

# Correzione 8d


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8e
X_train, X_test, y_train, y_test = train_test_split(
    properties_pd[["bedrooms"]], y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
rooms_model = LinearRegression().fit(X_train, y_train)
rooms_predictions = rooms_model.predict(X_test)
print(round(r2_score(rooms_predictions, y_test), 3))

# COMMAND ----------

# Correzione 8e


# COMMAND ----------

# ERRORE SILENZIOSO – cella 8f
print(evaluate_regression(rooms_model, X_train, y_train))

# COMMAND ----------

# Correzione 8f

