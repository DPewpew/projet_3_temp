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
        "Périmètre : SAV télécom **FIXE** (ADSL/VDSL/FTTH) — France — 4 grands opérateurs."
    )

    st.divider()
    st.write("Contenu Semaine 1…")

    st.divider()
    # ✅ Retour
    if st.button("⬅️ Retour à la roadmap", key="back_to_home"):
        st.session_state.page = "home"
        st.rerun()

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

    st.subheader("✅ KPI cibles (SAV FIXE)")
    st.markdown(
        """
**KPI 1 — Incidents réseau fixe (par opérateur)**  
- Mesure : fréquence / volumétrie d’incidents sur le fixe  
- Lecture SAV : plus d’incidents ⇒ plus de sollicitations (appels/tickets/réclamations)

**KPI 2 — Délais de rétablissement / d’intervention (par opérateur)**  
- Mesure : temps de résolution/rétablissement après incident  
- Lecture SAV : délais longs ⇒ risque d’insatisfaction + sur-sollicitation

**KPI 3 — Ressenti utilisateur (par opérateur)**  
- Mesure : plaintes / réclamations / satisfaction (selon sources publiques)  
- Lecture SAV : traduit l’impact “réel” côté usager

**KPI 4 (optionnel, si mesurable) — Récurrence d’incidents (par opérateur)**  
- Mesure : répétition des incidents dans le temps  
- Lecture SAV : la récurrence génère une pression SAV plus forte qu’un incident isolé
"""
    )

    st.subheader("🔎 Important : comparabilité entre opérateurs")
    st.markdown(
        """
Les incidents et les délais **ne sont pas directement comparables “bruts”** entre les 4 opérateurs
(infrastructures, périmètres, historiques, techno).  
**Conséquence méthodologique :**
- analyse **par opérateur**
- comparaison = **lecture transversale** (ordres de grandeur, tendances, ruptures), **sans classement**
- focus sur **distributions** et **quantiles** (p75/p90/p95) plutôt que sur une moyenne unique
"""
    )

    st.divider()

    # -----------------------------
    # 3) Données (sources) & contrôles qualité
    # -----------------------------
    st.header("3) Données (sources) & contrôles qualité")

    st.subheader("📌 Critères de sélection des données publiques")
    st.markdown(
        """
- Source publique identifiable (institution/observatoire/plateforme reconnue)
- Données **agrégées** (pas d’informations personnelles)
- Couverture 2021–2024 (ou sous-période cohérente et justifiable)
- Mesures liées à : **qualité fixe** + **ressenti**
- Granularité exploitable (mensuel / trimestriel / annuel)
"""
    )

    st.subheader("🧪 Contrôles de cohérence à réaliser à l’import")
    st.markdown(
        """
Checklist minimale :
- formats de dates cohérents
- unités homogènes
- libellés opérateurs stables
- valeurs manquantes identifiées
- doublons critiques repérés
"""
    )

    st.subheader("🧼 Nettoyage léger autorisé (Semaine 1)")
    st.markdown(
        """
- normaliser noms de colonnes
- convertir dates / numériques
- harmoniser libellés simples
- retirer lignes inutilisables évidentes

**Interdit (Semaine 1) :** feature engineering, agrégations complexes, ML
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
        " ├── raw/        # données brutes (inchangées)\n"
        " ├── cleaned/    # données nettoyées léger\n"
        " └── README.md   # description + sources + dictionnaire rapide\n"
    )

    st.subheader("📝 Note méthodologique (sources, limites, hypothèses)")
    st.markdown(
        """
Contenu attendu :
- sources utilisées + liens
- périmètre & exclusions
- période 2021–2024 + justification post-COVID
- définitions des KPI
- limites (couverture, granularité, biais potentiels)
- hypothèses de traitement (normalisation, exclusions de lignes, etc.)
"""
    )

