# streamlit_app/steam_success_overview.py
# Page de présentation (1 page) pour formateur — Projet 3 (Steam / Axe 1)
# L’objectif est d’expliquer le sujet, les données, la méthode et les livrables.
# (Pas besoin de la DB/ETL ici : c’est une page “pitch”.)

import streamlit as st

st.set_page_config(page_title="Projet 3 — Steam | Facteurs de succès", layout="wide")

# -----------------------------
# Header
# -----------------------------
st.title("Projet 3 — Analyse des facteurs du succès commercial sur Steam")
st.caption("Périmètre : analyse globale (post-lancement) + modèle explicable — délai : 20 jours")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Axe", "Facteurs de succès", help="Axe 1 : succès commercial (owners estimés)")
with c2:
    st.metric("Cible", "estimated_owners", help="Transformée en valeur numérique + label succès (top 30%)")
with c3:
    st.metric("ML", "Logistic Regression", help="Modèle simple et interprétable (coefficients)")

st.divider()

# -----------------------------
# Contexte & objectifs
# -----------------------------
left, right = st.columns([1.2, 1])

with left:
    st.subheader("Contexte & problématique")
    st.write(
        """
**Problématique :** *Quels facteurs influencent le succès commercial d’un jeu sur Steam ?*

Le projet vise à :
- identifier les variables les plus associées à un grand volume d’owners (estimation),
- construire un pipeline reproductible (nettoyage → features → label),
- produire un dashboard et un modèle explicable pour appuyer l’analyse.
"""
    )

with right:
    st.subheader("Définition du succès")
    st.write(
        """
- `estimated_owners` est fourni sous forme d’intervalle (ex: `"0 - 20000"`).
- Transformation en **valeur numérique** (milieu de l’intervalle).
- Création d’un **label binaire** :
  - **Succès = 1** si owners > **percentile 70** (Top 30%)
  - **Succès = 0** sinon
"""
    )

st.divider()

# -----------------------------
# Sources de données
# -----------------------------
st.subheader("Données & sources")

colA, colB = st.columns([1.4, 1])
with colA:
    st.write(
        """
**Dataset principal :** Steam Games Dataset (FronkonGames)  
- MAJ régulière (scraper)  
- Contenu : métadonnées store + signaux de marché et engagement.

**Pourquoi ce choix :**
- Données publiques, volumineuses, riches en variables
- Colonne de succès exploitable (`estimated_owners`)
- Variables explicatives directement utilisables (prix, avis, tags, genres, CCU, temps de jeu, etc.)
"""
    )

with colB:
    st.info(
        """
**Entrées principales exploitées (exemples)**
- Prix : `price`, `is_free`
- Réception : `positive`, `negative`, `user_score`, `metacritic_score`
- Engagement : `average_playtime_forever`, `peak_ccu`, `achievements`
- Contenu : `genres`, `categories`, `tags`
- Plateformes : `windows`, `mac`, `linux`
- Temps : `release_date`
""".strip()
    )

st.divider()

# -----------------------------
# Méthode (ETL / DB / Viz / ML)
# -----------------------------
st.subheader("Méthode (workflow Projet 3)")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("### 1) Acquisition")
    st.write(
        """
- Téléchargement dataset (Kaggle/GitHub)
- Stockage **raw**
- Contrôle schéma & volume
"""
    )

with m2:
    st.markdown("### 2) Nettoyage")
    st.write(
        """
- Parsing dates, prix
- Conversion `estimated_owners` → numérique
- Ratios : `positive_ratio`
- Normalisation champs multi-values
"""
    )

with m3:
    st.markdown("### 3) Infra données")
    st.write(
        """
- ETL reproductible (scripts)
- PostgreSQL (tables simples + tables multi-valeurs)
- Data mart pour dashboards
"""
    )

with m4:
    st.markdown("### 4) Analyse & ML")
    st.write(
        """
- KPI & corrélations
- Visualisations interactives
- Logistic Regression (explicable)
- Interprétation des coefficients
"""
    )

st.divider()

# -----------------------------
# KPI proposés (dashboard)
# -----------------------------
st.subheader("KPI & visualisations prévues")

k1, k2 = st.columns(2)
with k1:
    st.markdown("#### KPI Marché")
    st.write(
        """
- Répartition des owners (log scale)
- Succès par **tranches de prix**
- Succès par **année de sortie**
- Succès par **plateforme** (Win/Mac/Linux)
"""
    )

with k2:
    st.markdown("#### KPI Produit / Réception / Engagement")
    st.write(
        """
- `positive_ratio` vs succès
- Metacritic vs succès
- `peak_ccu` vs owners
- `average_playtime_forever` vs succès
- Genres/tags les plus associés au succès
"""
    )

st.divider()

# -----------------------------
# Cadrage ML (simple & explicable)
# -----------------------------
st.subheader("Modélisation (simple, explicable)")

st.write(
    """
**Objectif ML :** estimer la probabilité qu’un jeu soit dans le **Top 30%** (owners).  
**Modèle :** Logistic Regression (baseline robuste, interprétable).  
**Évaluation :** Accuracy + Precision/Recall + matrice de confusion.  
**Interprétation :** coefficients → variables qui augmentent/diminuent la probabilité de succès.
"""
)

st.warning(
    "Note méthodologique : certaines features (avis, peak_ccu, playtime) sont post-lancement. "
    "Le projet est cadré en **analyse des facteurs globaux** (pas une prédiction avant sortie)."
)

st.divider()

# -----------------------------
# Planning 20 jours
# -----------------------------
st.subheader("Planning (20 jours)")

st.write(
    """
- **J1–J3** : EDA + définition de la cible + nettoyage owners  
- **J4–J7** : feature engineering + dataset clean + contrôles qualité  
- **J8–J11** : ETL + base PostgreSQL + tables normalisées (genres/tags)  
- **J12–J15** : dashboard Streamlit (KPI + filtres + vues)  
- **J16–J18** : ML (LogReg) + interprétation + reporting  
- **J19–J20** : finalisation, doc, slides, répétition
"""
)

st.divider()

# -----------------------------
# Livrables
# -----------------------------
st.subheader("Livrables attendus")
st.write(
    """
- Scripts **ETL** (extract / transform / load)
- Base **PostgreSQL** (schéma + data mart)
- Dashboard **Streamlit** (KPI + exploration)
- Notebook / module **ML** (Logistic Regression + interprétation)
- Documentation (README + dictionnaire de données)
"""
)

st.caption("Page de cadrage : destinée à valider le sujet, l’axe, les sources et le plan avant implémentation complète.")
