from pathlib import Path
import pandas as pd


# =========================
# Paths
# =========================
ROOT = Path(__file__).resolve().parents[1]
IN_CSV = ROOT / "data" / "cleaned" / "games_clean.csv"
OUT_CSV = ROOT / "data" / "cleaned" / "games_clean_sql.csv"


# =========================
# Colonnes attendues par ta table Postgres games_clean
# =========================
PG_COLS = [
    "appid", "name", "release_date", "release_year",
    "price", "required_age", "dlc_count",
    "windows", "mac", "linux",
    "metacritic_score", "positive", "negative", "positive_ratio",
    "peak_ccu", "average_playtime_forever",
    "estimated_owners", "estimated_owners_numeric",
    "tag_count", "category_count", "genre_count", "developer_count", "publisher_count"
]


def main() -> None:
    if not IN_CSV.exists():
        raise FileNotFoundError(f"Fichier introuvable: {IN_CSV}")

    df = pd.read_csv(IN_CSV)

    # --- Choix de la source date ---
    # Tu as souvent release_date_dt dans ton dataset ; sinon release_date.
    date_src = None
    for candidate in ["release_date_dt", "release_date"]:
        if candidate in df.columns:
            date_src = candidate
            break
    if date_src is None:
        raise ValueError("Aucune colonne date trouvée (release_date_dt ou release_date).")

    # --- Normalisation date au format YYYY-MM-DD (Postgres DATE) ---
    df["release_date"] = pd.to_datetime(df[date_src], errors="coerce").dt.strftime("%Y-%m-%d")

    # --- Vérif colonnes nécessaires ---
    missing = [c for c in PG_COLS if c not in df.columns and c != "release_date"]
    # release_date est créée ci-dessus, donc on l'exclut du test "missing"
    missing = [c for c in missing if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV source: {missing}")

    # --- Sélection & ordre exact pour l'import PG ---
    out = df[PG_COLS].copy()

    # --- Types conseillés (sécurise l'import) ---
    int_cols = [
        "appid", "release_year", "required_age", "dlc_count",
        "metacritic_score", "positive", "negative",
        "peak_ccu", "average_playtime_forever",
        "estimated_owners_numeric", "tag_count", "category_count",
        "genre_count", "developer_count", "publisher_count"
    ]
    for c in int_cols:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")

    out["price"] = pd.to_numeric(out["price"], errors="coerce")
    out["positive_ratio"] = pd.to_numeric(out["positive_ratio"], errors="coerce")

    # bools -> True/False propres
    for c in ["windows", "mac", "linux"]:
        out[c] = out[c].astype(bool)

    # --- Export CSV importable ---
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8")

    # --- Logs rapides utiles ---
    print("Export Postgres prêt :")
    print(" - Input :", IN_CSV)
    print(" - Output:", OUT_CSV)
    print(" - Shape :", out.shape)
    print(" - Null release_date:", int(out["release_date"].isna().sum()))
    print(" - Null positive_ratio:", int(out["positive_ratio"].isna().sum()))


if __name__ == "__main__":
    main()
