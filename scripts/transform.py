# scripts/transform.py
import json
from pathlib import Path

import numpy as np
import pandas as pd


RAW_JSON = Path("data/raw/games.json")
OUT_DIR = Path("data/cleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def owners_mid_to_int(s: str) -> int | None:
    """
    Convertit "20000 - 50000" -> 35000 (milieu).
    Retourne None si non parsable.
    """
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return None
    s = str(s).strip().replace(",", "")
    if " - " not in s:
        return None
    low_str, high_str = s.split(" - ", 1)
    try:
        low = int(float(low_str))
        high = int(float(high_str))
        return int((low + high) / 2)
    except ValueError:
        return None


def safe_len(x) -> int:
    """
    - list -> len(list)
    - dict -> len(dict)
    - None/NaN/other -> 0
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return 0
    if isinstance(x, (list, dict)):
        return len(x)
    return 0


def main():
    # 1) Read JSON (dict {appid: {...}})
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient="index").reset_index()
    df.rename(columns={"index": "appid"}, inplace=True)

    # 2) Rule 1 — Exclude "0 - 0"
    df = df[df["estimated_owners"] != "0 - 0"].copy()

    # 3) Rule 2 — Estimated owners numeric (milieu)
    df["estimated_owners_numeric"] = df["estimated_owners"].apply(owners_mid_to_int).astype("Int64")

    # 4) Rule 3 — positive_ratio = NULL si pas d’avis
    # (NULL -> NaN/NA côté pandas)
    pos = pd.to_numeric(df.get("positive", 0), errors="coerce").fillna(0).astype("int64")
    neg = pd.to_numeric(df.get("negative", 0), errors="coerce").fillna(0).astype("int64")
    total = pos + neg
    df["positive_ratio"] = np.where(total > 0, pos / total, np.nan)

    # 5) Rule 4 — release_date -> datetime + release_year (on garde les lignes même si NaT)
    df["release_date_dt"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date_dt"].dt.year.astype("Int64")

    # 6) Rule 5 — counts
    # tags can be dict or list -> count keys/elements
    df["tag_count"] = df["tags"].apply(safe_len).astype("int64")
    df["category_count"] = df["categories"].apply(safe_len).astype("int64")
    df["genre_count"] = df["genres"].apply(safe_len).astype("int64")
    df["developer_count"] = df["developers"].apply(safe_len).astype("int64")
    df["publisher_count"] = df["publishers"].apply(safe_len).astype("int64")

    # (Optionnel mais utile) Convert appid to int
    df["appid"] = pd.to_numeric(df["appid"], errors="coerce").astype("Int64")

    # 7) Sorties clean (Parquet + CSV)
    # On garde release_date originale + une date propre (release_date_dt)
    parquet_path = OUT_DIR / "games_clean.parquet"
    csv_path = OUT_DIR / "games_clean.csv"
    
    
    # --- FIX pyarrow: colonnes "object" mixtes ---
    if "score_rank" in df.columns:
        df["score_rank"] = df["score_rank"].astype("string")

    # (optionnel mais recommandé) mêmes problèmes possibles sur d'autres champs
    for col in ["notes", "reviews", "website", "support_url", "support_email", "metacritic_url"]:
        if col in df.columns:
            df[col] = df[col].astype("string")

        # --- FIX pyarrow: tags est parfois dict, parfois list -> on ne garde que tag_count ---
    df["tag_count"] = df["tags"].apply(safe_len).astype("int64")
    df.drop(columns=["tags"], inplace=True)

    # (recommandé) si tu ne veux pas stocker les listes en parquet/CSV :
    drop_nested = ["categories", "genres", "developers", "publishers", "packages", "screenshots", "movies", "supported_languages", "full_audio_languages"]
    df.drop(columns=[c for c in drop_nested if c in df.columns], inplace=True)


    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # 8) Quick checks
    print("Saved:", parquet_path, "and", csv_path)
    print("Shape:", df.shape)
    print("Top owners classes:\n", df["estimated_owners"].value_counts().head(5))
    print("release_year NULL:", int(df["release_year"].isna().sum()))


if __name__ == "__main__":
    main()
