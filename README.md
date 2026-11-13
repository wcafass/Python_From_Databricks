# Libro_Python – Python per Databricks

Notebook del libro *Python per Databricks*: codice dei capitoli, esercizi e soluzioni.
Tutti gli esempi usano la base dati `samples.wanderbricks`, già presente in ogni account
Databricks Free Edition.

## Come ottenere i notebook nel proprio workspace

1. In Databricks si apre **Workspace → Users →** *proprio indirizzo email*.
2. Si sceglie **Create → Git folder**.
3. In **Git repository URL** si incolla l'indirizzo di questo repository; il provider è **GitHub**.
4. Si lascia come nome della cartella `Libro_Python` e si conferma con **Create Git folder**.

Non servono credenziali GitHub: il repository è pubblico.

## Prima di iniziare

Si apre `L00_Prepara_Dati` e lo si esegue **una sola volta** con **Run all** (Capitolo 0, sezione 0.7).
Gli altri notebook si eseguono una cella alla volta.

## Contenuto

| Notebook | Capitolo |
|-|-|
| `L00_Prepara_Dati` | Preparazione dei dati (si esegue una volta) |
| `L00_Orientarsi_Databricks`, `L00_Esercizi`, `L00_Soluzioni` | Capitolo 0 – Orientarsi in Databricks |

I notebook dei capitoli successivi si aggiungono man mano. Per ricevere gli aggiornamenti si
apre il Git folder e si usa **Pull**.

## Attenzione agli esercizi

Prima di svolgere gli esercizi conviene farne una copia con un nome diverso, nella stessa cartella
(menu del notebook → **Clone**, per esempio `L00_Esercizi_svolti`). Si lavora sulla copia: l'originale
resta intatto e un successivo **Pull** non entra in conflitto con le proprie modifiche. La stessa
cartella è necessaria perché dal Capitolo 10 i notebook caricano `utils` con `%run ./utils`.
