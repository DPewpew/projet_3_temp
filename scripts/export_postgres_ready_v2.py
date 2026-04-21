import pandas as pd
from pathlib import Path

IN_DIR = Path("data/cleaned")
OUT_DIR = Path("data/cleaned_csv")
OUT_DIR.mkdir(parents=True, exist_ok=True)

files = [
    ("games_clean.parquet", "games_clean.csv"),
    ("game_languages_clean.parquet", "game_languages_clean.csv"),
    ("game_categories_clean.parquet", "game_categories_clean.csv"),
    ("game_genres_clean.parquet", "game_genres_clean.csv"),
]

for src, dst in files:
    df = pd.read_parquet(IN_DIR / src)
    df.to_csv(OUT_DIR / dst, index=False, encoding="utf-8")
    print("Wrote", OUT_DIR / dst, df.shape)