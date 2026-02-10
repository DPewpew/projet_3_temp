# Data — Projet 3 (Télécom fixe France)

## Périmètre
- Sujet : Service après-vente (SAV) des opérateurs télécoms — **FIXE uniquement** (ADSL / VDSL / FTTH)
- Période étudiée : **2021–2024** (post-COVID)
- Données : **publiques, agrégées, externes**
- Zone : France
- Exclusions : mobile, données opérationnelles internes, données individuelles/personnelles

---

## Inventaire des sources

### Source 1 — Observatoire des communications électroniques
- Producteur : ARCEP (via data.gouv.fr)
- Type : **Quantitatif structurant** (marché fixe, indicateurs par opérateur)
- Période couverte : 2021–2024 (selon indicateurs)
- Granularité :
  - temporelle : annuelle / trimestrielle
  - analytique : **par opérateur**
- Variables clés :
  - indicateurs liés au marché de l’internet fixe
  - métriques publiées par opérateur
- KPI couverts :
  - socle quantitatif par opérateur (proxy qualité / pression SAV)
- Lien :
  - https://www.data.gouv.fr/datasets/observatoire-des-communications-electroniques
- Limites connues :
  - pas de données d’incidents techniques brutes
  - pas de délais de rétablissement
  - indicateurs parfois indirects vis-à-vis du SAV

---

### Source 2 — Marché du haut et très haut débit fixe (déploiements)
- Producteur : ARCEP (via data.gouv.fr)
- Type : **Contexte technique / infrastructure**
- Période couverte : 2021–2024 (selon jeux)
- Granularité :
  - géographique : commune / département / région
- Variables clés :
  - déploiements FTTH / THD
  - couverture et éligibilité
- KPI couverts :
  - aucun KPI SAV direct
  - indicateurs de contexte réseau
- Lien :
  - https://www.data.gouv.fr/datasets/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements
- Limites connues :
  - pas de données par opérateur exploitables pour le SAV
  - pas d’incidents ni de délais

---

### Source 3 — Observatoire de la satisfaction client
- Producteur : ARCEP
- Type : **Ressenti utilisateur / proxy SAV**
- Période couverte : dernières éditions disponibles (incluant la période récente)
- Granularité :
  - analytique : **par opérateur**
- Variables clés :
  - indicateurs de satisfaction client
  - perception de la qualité de service et de la relation client
- KPI couverts :
  - ressenti utilisateur (proxy de pression SAV)
- Lien :
  - https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/satisfaction-client/observatoire-de-la-satisfaction-client-edition-2025.html
- Limites connues :
  - données principalement sous voir forme de graphiques / indicateurs agrégés
  - pas de fichiers CSV/XLS systématiquement disponibles
  - pas de mesure directe d’incidents ou de délais techniques

---

### Source 4 — API contexte réseau fixe (optionnelle)
- Producteur : source open data spécialisée
- Type : Contexte réseau (technologies, débits, zones)
- Période couverte : variable selon endpoints
- Granularité :
  - géographique (commune / département / région)
- Variables clés :
  - technologies d’accès
  - classes de débits
- KPI couverts :
  - aucun KPI SAV direct
- Limites connues :
  - pas de données par opérateur
  - usage limité à l’enrichissement contextuel

---

## Hypothèses de traitement (Semaine 1)
- Normalisation des noms de colonnes
- Conversion des dates et valeurs numériques dans des formats exploitables
- Harmonisation des libellés opérateurs
- Gestion des valeurs manquantes :
  - conservation si non bloquant
  - exclusion documentée si critique
- Exclusions :
  - lignes hors période 2021–2024
  - indicateurs non liés au fixe

---

## Limites & biais
- **Absence de données publiques brutes** sur :
  - incidents réseau fixe
  - pannes
  - délais de rétablissement / d’intervention  
  (données non publiées pour des raisons de sécurité et de confidentialité des infrastructures)
- Analyse reposant sur :
  - indicateurs agrégés officiels
  - proxies SAV (ressenti utilisateur, contexte réseau)
- Comparabilité inter-opérateurs :
  - analyse par opérateur
  - **sans classement**
- Granularités hétérogènes :
  - temporelles et géographiques différentes selon les sources
