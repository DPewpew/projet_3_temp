import pandas as pd
from pathlib import Path

IN = Path("data/cleaned/game_languages_clean.parquet")
OUT = Path("data/cleaned_csv/game_languages_clean.csv")

df = pd.read_parquet(IN)
df.to_csv(OUT, index=False, encoding="utf-8")

print("CSV regenerated:", OUT)
print("Rows:", len(df))