🎮 Projet 3 – Analyse du succès des jeux Steam
📌 Objectif

Analyser les facteurs expliquant le succès d’un jeu sur Steam en utilisant :

Analyse descriptive

Construction d’indicateurs clés

Validation via modèle ML explicatif

🔄 Pipeline de données
1️⃣ Extract

Les données proviennent du dataset Kaggle :

Steam Games Dataset
https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data

Téléchargement manuel puis stockage dans :

data/raw/

2️⃣ Transform

Script principal :

scripts/transform.py


Étapes réalisées :

Nettoyage des valeurs manquantes

Suppression des incohérences

Création des variables :

positive_ratio

peak_ccu

playtime

recommendations

Production de :

data/cleaned/games_clean.csv
data/cleaned/games_clean_sql.csv
data/cleaned/games_clean.parquet

3️⃣ Load

Import dans PostgreSQL effectué manuellement via pgAdmin à partir de :

games_clean_sql.csv


La base sert ensuite à :

Analyse SQL

Visualisation Power BI

🛠 Stack technique

Python (Pandas / NumPy)

PostgreSQL

Power BI

Scikit-learn

Git

📊 Méthodologie analytique

Le projet repose sur :

Analyse des indicateurs clés

Définition d’un seuil de succès

Modèle ML explicatif (validation des corrélations)

Le modèle n’est pas prédictif avant sortie.
Il sert à confirmer les résultats de l’analyse descriptive.

⚠️ Remarques techniques

Les données brutes ne sont pas versionnées (taille importante)

L’import en base est réalisé manuellement

Le projet se concentre sur l’analyse et la structuration des données