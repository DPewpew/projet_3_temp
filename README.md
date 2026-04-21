# 🎮 Analyse du Succès des Jeux Steam

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)
![Status](https://img.shields.io/badge/Status-Terminé-brightgreen)

> Analyse des facteurs expliquant le succès d'un jeu sur Steam — pipeline ETL complet, modélisation PostgreSQL, dashboard Power BI interactif et validation par modèle ML.

---

## À propos

Ce projet a été réalisé dans le cadre de ma **formation Data Analyst**. Il illustre un pipeline de données end-to-end : extraction depuis Kaggle, transformation en Python, modélisation et chargement en base PostgreSQL via des scripts SQL, analyse et visualisation Power BI, et validation des résultats via un modèle de machine learning.

Il fait partie de mon portfolio GitHub, conçu pour montrer les compétences acquises tout au long de ma formation.

> 👤 **[Mon profil GitHub →](https://github.com/DPewpew)**

---

## Sommaire

- [Objectif](#objectif)
- [Résultats clés](#résultats-clés)
- [Structure du projet](#structure-du-projet)
- [Pipeline de données](#pipeline-de-données)
- [Modélisation SQL](#modélisation-sql)
- [Dashboard Power BI](#dashboard-power-bi)
- [Installation](#installation)
- [Stack technique](#stack-technique)
- [Remarques techniques](#remarques-techniques)

---

## Objectif

Identifier et quantifier les facteurs qui expliquent le succès d'un jeu sur Steam, défini par un seuil de **100 000 propriétaires** (soit 8,73 % des jeux du catalogue).

L'analyse repose sur trois axes :
1. **Analyse descriptive** du marché et des indicateurs clés
2. **Identification des facteurs de succès** (genre, langue, plateforme, avis)
3. **Validation ML** pour confirmer les corrélations identifiées

---

## Résultats clés

| Indicateur | Valeur |
|------------|--------|
| Jeux analysés | ~101 000 |
| Jeux considérés comme succès (100K+ owners) | 8 815 — 8,73 % du catalogue |
| Croissance des sorties Steam 2013 → 2025 | +3 191 % |
| Meilleur genre (taux de succès) | Massively Multiplayer — 22,96 % |
| Avis positifs moyens d'un jeu à succès | 85,6 % (+5,3 pts vs échec) |
| Langues moyennes d'un jeu à succès | 7,4 langues (1,7× plus que les autres) |
| Plateformes moyennes d'un jeu à succès | 1,55 vs 1,31 pour les échecs |

---

## Structure du projet

```
├── data/
│   ├── raw/                               # Données brutes Kaggle (non versionnées)
│   ├── cleaned/                           # Données nettoyées — format Python
│   └── cleaned_csv/                       # Versions CSV prêtes pour PostgreSQL
│
├── sql/
│   ├── create_schema_v1.sql               # Création du schéma relationnel
│   ├── fix_language.sql                   # Correction des langues en base
│   ├── fix_publishers.sql                 # Correction des éditeurs en base
│   ├── load_dims_and_bridges_v1.sql       # Chargement dimensions & tables de liaison
│   └── load_fix_publishers.sql            # Correctif chargement éditeurs
│
├── scripts/
│   ├── transform.py                       # Pipeline nettoyage v1
│   ├── transform_v2.py                    # Pipeline nettoyage v2 (final)
│   ├── fix_language.py                    # Correction des langues
│   ├── fix_publishers.py                  # Correction des éditeurs
│   ├── export_postgres_ready.py           # Export PostgreSQL v1
│   ├── export_postgres_ready_v2.py        # Export PostgreSQL v2 (final)
│   ├── export_fix_language.py             # Export correctif langues
│   └── export_fix_publishers.py           # Export correctif éditeurs
│
├── power_bi/
│   └── analyse_steam_v2.pbix              # Dashboard Power BI (4 pages)
│
├── visu_temp/
│   └── visu.ipynb                         # Notebook exploratoire
│
├── app.py
├── requirements.txt
└── .gitignore
```

---

## Pipeline de données

### 1. Extract

- **Source** : [Steam Games Dataset — Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data)
- Téléchargement manuel, stocké dans `data/raw/` (non versionné)

### 2. Transform — `scripts/transform_v2.py`

- Nettoyage des valeurs manquantes et suppression des incohérences
- Corrections ciblées sur les langues (`fix_language.py`) et les éditeurs (`fix_publishers.py`)
- Création des variables analytiques :
  - `positive_ratio` — ratio d'avis positifs
  - `peak_ccu` — pic de joueurs simultanés
  - `playtime` — temps de jeu moyen
  - `recommendations` — nombre de recommandations
- Export dans `data/cleaned/` (Parquet) et `data/cleaned_csv/` (CSV PostgreSQL-ready)

### 3. Load — `sql/`

- Création du schéma via `create_schema_v1.sql`
- Import des CSV dans PostgreSQL via pgAdmin
- Correctifs post-import appliqués en SQL (`fix_language.sql`, `fix_publishers.sql`)
- Chargement des dimensions et tables de liaison via `load_dims_and_bridges_v1.sql`

---

## Modélisation SQL

Le dossier `sql/` contient l'ensemble des scripts de structuration et d'alimentation de la base de données :

| Script | Rôle |
|--------|------|
| `create_schema_v1.sql` | Définition du schéma relationnel (tables, types, contraintes) |
| `fix_language.sql` | Nettoyage et normalisation des langues en base |
| `fix_publishers.sql` | Nettoyage et normalisation des éditeurs en base |
| `load_dims_and_bridges_v1.sql` | Chargement des tables de dimensions et de liaison |
| `load_fix_publishers.sql` | Correctif appliqué après chargement des éditeurs |

---

## Dashboard Power BI

Le fichier `power_bi/analyse_steam_v2.pbix` contient 4 pages interactives, filtrables par année (1997–2025), genre et catégorie :

| Page | Contenu |
|------|---------|
| **Marché actuel** | Vue d'ensemble — 101K jeux, taux de succès global 8,73 %, top 10 studios |
| **Dynamique du succès** | Évolution des sorties 2013-2025, +3 191 % de jeux publiés |
| **Facteurs du succès** | Taux de succès par genre, catégorie, langue et plateforme |
| **Validation analytique** | Comparaison métriques clés — jeux à succès vs échec |

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/DPewpew/<nom-du-repo>
cd <nom-du-repo>

# Installer les dépendances Python
pip install -r requirements.txt

# Télécharger les données brutes sur Kaggle et les placer dans data/raw/
# https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data

# Lancer la transformation
python scripts/transform_v2.py

# Préparer l'export PostgreSQL
python scripts/export_postgres_ready_v2.py

# Créer le schéma en base (pgAdmin ou psql)
# psql -U <user> -d <database> -f sql/create_schema_v1.sql
```

---

## Stack technique

| Catégorie | Outils |
|-----------|--------|
| Traitement données | Python, Pandas, NumPy |
| Base de données | PostgreSQL, pgAdmin |
| Visualisation | Power BI, Jupyter |
| Machine Learning | Scikit-learn |
| Versioning | Git |

---

## Remarques techniques

- Les données brutes ne sont pas versionnées (volume trop important) — téléchargement manuel requis
- L'import initial en base PostgreSQL est réalisé manuellement via pgAdmin
- Les scripts en v1/v2 reflètent l'évolution du pipeline — la **v2 est la version finale** utilisée pour l'analyse