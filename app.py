# streamlit_app.py
import streamlit as st

st.set_page_config(
    page_title="Projet 3 — Roadmap (Télécom fixe France)",
    page_icon="🗺️",
    layout="centered",
)

# -----------------------------
# Navigation state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -----------------------------
# Routeur (DOIT être avant le rendu home)
# -----------------------------
if st.session_state.page == "week_1":
    from week.week_1 import render_week_1
    render_week_1()
    st.stop()

# -----------------------------
# HOME
# -----------------------------
st.title("🗺️ Projet 3 — Roadmap (1 mois)")
st.caption(
    "Sujet : étude du marché de l’internet fixe en France (qualité de service, ressenti utilisateur) "
    "et implications pour un SAV performant et rentable. ML léger : seuils critiques. "
    "Bonus : simulation + analyse qualitative (nuages de mots)."
)

# -----------------------------
# HOME (Roadmap)
# -----------------------------
st.title("🗺️ Projet 3 — Roadmap (1 mois)")
st.caption(
    "Sujet : étude du marché de l’internet fixe en France (qualité de service, ressenti utilisateur) "
    "et implications pour un SAV performant et rentable. ML léger : seuils critiques. "
    "Bonus : simulation + analyse qualitative (nuages de mots)."
)

st.divider()

st.header("🎯 Objectif final")
st.markdown(
    """
Livrer une **analyse data claire et défendable** basée sur des **données publiques réelles** :
- Qualité de service **fixe** (incidents, délais de rétablissement…)
- Ressenti utilisateur (réclamations / satisfaction selon sources publiques)
- Traduction en **principes génériques** d’un SAV performant (**satisfaction + rentabilité**)
- **ML léger (bonus)** : détection de **seuils critiques** / ruptures d’impact
- **Bonus (dynamisation)** : **simulation de scénarios SAV** + **scraping de commentaires publics** pour produire des **nuages de mots** (illustratif)
"""
)

st.header("📦 Livrables attendus — couverture")
st.markdown(
    """
- ✅ Scripts de collecte / extraction  
- ✅ Pipeline de nettoyage & prétraitement  
- ✅ ETL opérationnel (version Data Analyst : Extract → Transform → Load vers SQLite/Postgres)  
- ✅ Base de données optimisée & documentée  
- ✅ Tableaux de bord interactifs  
- ✅ Interface utilisateur simple & intuitive (dashboard Streamlit)  
- ✅ Documentation technique + guide utilisateur
"""
)

st.divider()

st.header("🗓️ Roadmap détaillée (4 semaines)")

with st.expander("Semaine 1 — Cadrage final & Données", expanded=True):
    st.markdown(
        """
**Objectif :** données propres, comprises, exploitables.

**Actions :**
- Valider : périmètre (fixe), période, KPI (3–4 max)
- Identifier les jeux de données publics (qualité + ressenti)
- Télécharger / importer les fichiers (CSV/XLS)
- Vérifier cohérence (dates, opérateurs, unités, valeurs manquantes)
- Premier nettoyage léger (normalisation & formats)

**Livrables :**
- Dossier `data/` structuré
- Note méthodologique (sources, limites, hypothèses)
"""
    )

    # ✅ Bouton navigation (valeur EXACTE)
    if st.button("➡️ Ouvrir le détail de la Semaine 1", key="btn_week_1"):
        st.session_state.page = "week_1"
        st.rerun()


with st.expander("Semaine 2 — Analyse descriptive & Comparaison", expanded=True):
    st.markdown(
        """
**Objectif :** comprendre ce que disent les données (constats factuels).

**Actions :**
- Calcul des KPI clés (incidents, délais, ressenti)
- Visualisations simples :
  - évolutions temporelles
  - comparaisons entre opérateurs (sans classement)
- Extraction des constats (faits + ordres de grandeur)

**Livrables :**
- 4–5 graphiques clairs
- Liste de constats factuels (sans jugement)
"""
    )

with st.expander("Semaine 3 — Analyse croisée & ML léger (seuils critiques) + Bonus qualitatif", expanded=True):
    st.markdown(
        """
**Objectif :** passer à l’analyse à valeur ajoutée (qualité ↔ ressenti ↔ pression SAV) et illustrer les situations critiques.

**Actions :**
- Croiser qualité vs ressenti (corrélations/relations simples)
- Identifier les situations à fort impact (délais longs, incidents récurrents)
- **ML léger (Option C) :**
  - quantiles (p75/p90/p95)
  - outliers / distributions
  - détection de seuils critiques (ruptures d’impact)
- Interprétation métier orientée SAV (sans interne/opérationnel détaillé)

**Bonus (illustratif, pour dynamiser la restitution) :**
- **Simulation de scénarios SAV** (ex. “délai long”, “incident répété”, “résolution rapide”) à partir des catégories identifiées
- **Scraping de commentaires publics** (données accessibles, anonymes, agrégées) liés au **fixe**
- **Nuages de mots** pour faire ressortir les thèmes/mots récurrents
- Comparaison **avant / après seuil critique** (ex. vocabulaire associé à un délai > p90)

**Livrables :**
- 2–3 graphiques analytiques (seuils/ruptures)
- Seuil(s) critique(s) identifiés + lecture métier
- **(Bonus)** 1–2 nuages de mots + synthèse des thèmes dominants (illustratif)
"""
    )

with st.expander("Semaine 4 — Restitution & Storytelling (dashboard + narration)", expanded=True):
    st.markdown(
        """
**Objectif :** produire un rendu pro (dashboard + narration).

**Actions :**
- Construire le dashboard (filtres simples : opérateur, période)
- Rédiger conclusions & limites (hypothèses explicites)
- Formaliser **4 principes SAV max** (niveau stratégique/analytique)
- Intégrer les éléments **bonus** de façon encadrée (onglet/section “Exploratoire”) :
  - scénarios simulés (lecture pédagogique)
  - nuages de mots (illustratif, non probant seul)
- Préparer pitch oral (2–3 minutes) + support

**Livrables :**
- Dashboard final
- Documentation (technique + guide utilisateur)
- Synthèse conclusions (actionnable, non technique)
"""
    )

st.divider()

st.header("📊 Répartition de l’effort (réaliste)")
st.markdown(
    """
- Données & nettoyage : **~30%**  
- Analyse : **~40%**  
- ML léger (bonus) : **~10%**  
- Restitution : **~20%**  

**Note :** le projet reste valide même si la partie ML est réduite (bonus).  
**Bonus (simulation + nuages de mots) :** à intégrer uniquement si le socle quanti est solide.
"""
)

st.header("✅ Critères de réussite")
st.markdown(
    """
Le projet est réussi si :
- Les graphiques racontent une histoire **compréhensible par un non-tech**
- Les conclusions sont **factuelles** et **défendables**
- Les limites sont **assumées**
- Les principes SAV restent **génériques** (pas d’interne opérateur)
- Les éléments qualitatifs (nuages de mots / simulation) restent **illustratifs** et ne remplacent pas les constats quantitatifs
"""
)
