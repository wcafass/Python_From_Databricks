# Oltre la SELECT – notebook del libro

Notebook del libro *Oltre la SELECT. Imparare Python con Databricks, partendo da ciò che si conosce*: codice dei capitoli, esercizi e soluzioni.
Tutti gli esempi usano la base dati `samples.wanderbricks`, già presente in ogni account
Databricks Free Edition.

## Come ottenere i notebook nel proprio workspace

1. In Databricks si apre **Workspace → Users →** *proprio indirizzo email*.
2. Si sceglie **Create → Git folder**.
3. In **Git repository URL** si incolla l'indirizzo di questo repository
   (`https://github.com/wcafass/Python_From_Databricks.git`); il provider è **GitHub**.
4. In **Git folder name** si scrive `Libro_Python` al posto del nome proposto e si conferma
   con **Create Git folder**.

Non servono credenziali GitHub: il repository è pubblico.

## Prima di iniziare

Si apre `L00_Prepara_Dati` e lo si esegue **una sola volta** con **Run all** (Capitolo 0, sezione 0.7).
Gli altri notebook si eseguono una cella alla volta.

## Contenuto

| Notebook | Capitolo |
|-|-|
| `L00_Prepara_Dati` | Preparazione dei dati (si esegue una volta) |
| `utils` | Notebook comune con import, costanti e funzioni (dal Capitolo 10, si carica con `%run ./utils`) |
| `L00_Orientarsi_Databricks`, `L00_Esercizi`, `L00_Soluzioni` | Capitolo 0 – Orientarsi in Databricks |
| `L01_Primi_Passi_Python`, `L01_Esercizi`, `L01_Soluzioni` | Capitolo 1 – Primi passi con Python |
| `L02_Operatori_Condizioni`, `L02_Esercizi`, `L02_Soluzioni` | Capitolo 2 – Operatori e condizioni |
| `L03_Liste_Dizionari`, `L03_Esercizi`, `L03_Soluzioni` | Capitolo 3 – Collezioni: liste e dizionari |
| `L04_Cicli`, `L04_Esercizi`, `L04_Soluzioni` | Capitolo 4 – Cicli |
| `L05_Funzioni`, `L05_Esercizi`, `L05_Soluzioni` | Capitolo 5 – Funzioni |
| `L06_Errori_Debug`, `L06_Esercizi`, `L06_Soluzioni` | Capitolo 6 – Errori e debug |
| `L07_Moduli_Librerie`, `L07_Esercizi`, `L07_Soluzioni` | Capitolo 7 – Moduli e librerie |
| `L08_Da_SQL_a_PySpark`, `L08_Esercizi`, `L08_Soluzioni` | Capitolo 8 – Da SQL a PySpark |
| `L09_Trasformazioni_PySpark`, `L09_Esercizi`, `L09_Soluzioni` | Capitolo 9 – Trasformazioni con PySpark |
| `L10_Tabelle_Delta`, `L10_Esercizi`, `L10_Soluzioni` | Capitolo 10 – Leggere e scrivere tabelle Delta |
| `L11_Progetto_Finale`, `L11_Esercizi`, `L11_Soluzioni` | Capitolo 11 – Progetto finale |

I notebook dei capitoli successivi si aggiungono man mano. Per ricevere gli aggiornamenti si
apre il Git folder e si usa **Pull**.

## Attenzione agli esercizi

Prima di svolgere gli esercizi conviene farne una copia con un nome diverso, nella stessa cartella
(menu del notebook → **Clone**, per esempio `L00_Esercizi_svolti`). Si lavora sulla copia: l'originale
resta intatto e un successivo **Pull** non entra in conflitto con le proprie modifiche. La stessa
cartella è necessaria perché dal Capitolo 10 i notebook caricano `utils` con `%run ./utils`.

Dal Capitolo 10 i notebook scrivono tabelle, solo nello schema `workspace.libro_python`. Il notebook
`utils` è comune a tutti i capitoli e non va modificato: le proprie costanti e funzioni si scrivono
nel proprio notebook, dopo la cella `%run ./utils`.
