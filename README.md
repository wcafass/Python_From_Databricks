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
| `L00_Orientarsi_Databricks`, `L00_Esercizi`, `L00_Soluzioni` | Capitolo 0 – Orientarsi in Databricks |
| `L01_Primi_Passi_Python`, `L01_Esercizi`, `L01_Soluzioni` | Capitolo 1 – Primi passi con Python |
| `L02_Operatori_Condizioni`, `L02_Esercizi`, `L02_Soluzioni` | Capitolo 2 – Operatori e condizioni |
| `L03_Liste_Dizionari`, `L03_Esercizi`, `L03_Soluzioni` | Capitolo 3 – Collezioni: liste e dizionari |
| `L04_Cicli`, `L04_Esercizi`, `L04_Soluzioni` | Capitolo 4 – Cicli |

I notebook dei capitoli successivi si aggiungono man mano. Per ricevere gli aggiornamenti si
apre il Git folder e si usa **Pull**.

## Attenzione agli esercizi

Prima di svolgere gli esercizi conviene farne una copia con un nome diverso, nella stessa cartella
(menu del notebook → **Clone**, per esempio `L00_Esercizi_svolti`). Si lavora sulla copia: l'originale
resta intatto e un successivo **Pull** non entra in conflitto con le proprie modifiche. La stessa
cartella è necessaria perché dal Capitolo 10 i notebook caricano `utils` con `%run ./utils`.
