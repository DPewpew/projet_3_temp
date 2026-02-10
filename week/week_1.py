import streamlit as st
import streamlit.components.v1 as components


def render_week_1():
    # (Optionnel) tentative scroll top — tu peux laisser ou enlever
    components.html(
        """
        <script>
          setTimeout(() => {
            window.scrollTo(0, 0);
            window.parent.scrollTo(0, 0);
          }, 50);
        </script>
        """,
        height=0,
    )

    st.title("📅 Projet 3 — Semaine 1 : Cadrage final & Données")
    st.caption(
        "Objectif : données propres, comprises, exploitables. "
        "Périmètre : SAV télécom **FIXE** (ADSL/VDSL/FTTH) — France — 4 grands opérateurs — période 2021–2024."
    )

    st.divider()

    # ✅ Retour
    if st.button("⬅️ Retour à la roadmap", key="back_to_home"):
        st.session_state.page = "home"
        st.rerun()

    # -----------------------------
    # 0) Point d'étape Semaine 1
    # -----------------------------
    st.header("0) Point d’étape — Semaine 1")
    st.success(
        "✅ Périmètre, période et méthode de comparaison verrouillés. "
        "✅ Structure `data/` créée. ✅ Sources publiques identifiées (quantitatif + contexte + ressenti)."
    )
    st.warning(
        "⚠️ Constat important : il n’existe pas de source open data française exploitable (CSV/API) recensant "
        "les **incidents/pannes** et les **délais de rétablissement** du fixe sur 2021–2024. "
        "L’analyse reposera donc sur des **indicateurs publics agrégés** et des **proxies SAV** (ressenti, contexte réseau)."
    )

    st.divider()

    # -----------------------------
    # 1) Périmètre & période
    # -----------------------------
    st.header("1) Périmètre & période")

    st.subheader("🎯 Périmètre (verrouillé)")
    st.markdown(
        """
- Analyse centrée sur le **SAV télécom FIXE** (ADSL / VDSL / FTTH)
- Basée sur des **données publiques agrégées**
- **Exclusions** : mobile, données opérationnelles internes, données individuelles/personnelles
"""
    )

    st.subheader("📆 Période (verrouillée) : 2021–2024")
    st.markdown(
        """
**Justification :** période **post-COVID**, plus représentative des usages stabilisés.  
La période COVID est exclue car elle correspond à des usages exceptionnels (confinements, télétravail contraint),
susceptibles de **biaiser** l’analyse.  
La période 2021–2024 permet d’observer des **évolutions structurelles** (télétravail plus courant) et leurs
implications sur la qualité perçue et la pression SAV.
"""
    )

    st.divider()

    # -----------------------------
    # 2) KPI (3–4 max) + méthode de comparaison
    # -----------------------------
    st.header("2) KPI (3–4 max) + approche de comparaison")

    st.subheader("✅ KPI cibles (SAV FIXE) — version réaliste (données disponibles)")
    st.markdown(
        """
**KPI 1 — Indicateurs quantitatifs “fixe” par opérateur (proxy qualité / pression SAV)**  
- Mesure : indicateurs publics disponibles (par opérateur) sur le **marché fixe** (ex. volumes/parts, métriques publiées)  
- Lecture SAV : sert de **socle chiffré** pour comparer des tendances sans classement

**KPI 2 — Ressenti utilisateur (par opérateur)**  
- Mesure : satisfaction/ressenti via indicateurs ARCEP (étude officielle)  
- Lecture SAV : traduit l’impact côté usager et sert de **proxy** de pression SAV

**KPI 3 — Contexte technique réseau fixe (géographie / déploiements / techno)**  
- Mesure : état du déploiement (FTTH/THD), contexte géographique/technique  
- Lecture SAV : contextualise les constats (attentes, contraintes d’accès)

**KPI 4 (optionnel) — “Seuils critiques” sur distributions (bonus Semaine 3)**  
- Mesure : quantiles (p75/p90/p95) / outliers sur les indicateurs disponibles  
- Lecture SAV : identifier des **zones/périodes** où l’impact “ressenti” semble basculer
"""
    )

    st.subheader("🔎 Important : comparabilité entre opérateurs")
    st.markdown(
        """
Les indicateurs ne sont pas toujours comparables “bruts” entre opérateurs (périmètres, techno, historique).  
**Conséquence méthodologique :**
- analyse **par opérateur**
- comparaison = **lecture transversale** (ordres de grandeur, tendances), **sans classement**
- focus sur **évolutions** et **distributions** plutôt que sur une moyenne unique
"""
    )

    st.divider()

    # -----------------------------
    # 3) Données (sources) & contrôles qualité
    # -----------------------------
    st.header("3) Données — sources validées (Semaine 1)")

    st.subheader("📌 Sources retenues et rôle dans le projet")
    st.markdown(
        f"""
### A) Source principale (quantitatif par opérateur)
- **Observatoire des communications électroniques (data.gouv / ARCEP)**  
  Lien : https://www.data.gouv.fr/datasets/observatoire-des-communications-electroniques  
  **Rôle :** base chiffrée structurante (indicateurs **par opérateur**, séries temporelles), utilisée pour la **Semaine 2** (analyse descriptive).

### B) Source contexte (infrastructure / déploiements)
- **Marché du haut et très haut débit fixe — Déploiements (data.gouv / ARCEP)**  
  Lien : https://www.data.gouv.fr/datasets/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements  
  **Rôle :** contexte technique/géographique (FTTH/THD…), utile pour **expliquer** et **contextualiser** (Semaine 2–4), pas un KPI SAV direct.

### C) Source ressenti (proxy SAV, par opérateur)
- **Observatoire de la satisfaction client — ARCEP (édition 2025)**  
  Lien : https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/satisfaction-client/observatoire-de-la-satisfaction-client-edition-2025.html  
  **Rôle :** KPI “ressenti utilisateur” (résultats officiels par opérateur). Données souvent sous forme de graphiques/indicateurs (pas toujours en CSV).

### D) Source complémentaire (optionnel) — API contexte réseau
- **API “contexte réseau fixe”** (technologies / classes de débits / granularité géographique)  
  **Rôle :** enrichissement “contexte” (non opérateur), à utiliser en support si besoin (bonus).
"""
    )

    st.subheader("🧪 Contrôles de cohérence à réaliser à l’import (Semaine 1)")
    st.markdown(
        """
Checklist minimale :
- formats de dates cohérents (annuel / trimestriel / mensuel)
- unités homogènes et compréhensibles
- libellés opérateurs stables (normalisation)
- valeurs manquantes identifiées (documentées)
- doublons critiques repérés
"""
    )

    st.subheader("🧼 Nettoyage léger autorisé (Semaine 1)")
    st.markdown(
        """
- normaliser noms de colonnes
- convertir dates / numériques
- harmoniser libellés simples (opérateurs, territoires, techno)
- retirer lignes inutilisables évidentes

**Interdit (Semaine 1) :** feature engineering complexe, agrégations lourdes, ML
"""
    )

    st.divider()

    # -----------------------------
    # 4) Livrables Semaine 1
    # -----------------------------
    st.header("4) Livrables — fin de Semaine 1")

    st.subheader("📁 Structure du dossier data/")
    st.code(
        "data/\n"
        " ├── raw/\n"
        " │   ├── qualite_fixe/\n"
        " │   └── ressenti/\n"
        " ├── cleaned/\n"
        " │   ├── qualite_fixe/\n"
        " │   └── ressenti/\n"
        " └── README.md\n"
    )

    st.subheader("📝 Note méthodologique (sources, limites, hypothèses)")
    st.markdown(
        """
Contenu attendu (à finaliser fin de semaine) :
- sources utilisées + liens (A/B/C/D)
- périmètre & exclusions
- période 2021–2024 + justification post-COVID
- KPI retenus + justification (proxies si besoin)
- limites (notamment : absence d’incidents/délais techniques bruts en open data)
- hypothèses de traitement (normalisation, exclusions de lignes, etc.)
"""
    )
