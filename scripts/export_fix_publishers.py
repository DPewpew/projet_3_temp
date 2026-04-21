from pathlib import Path
import pandas as pd

IN_DIR = Path("data/cleaned")
OUT_DIR = Path("data/cleaned_csv")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(IN_DIR / "game_publishers_clean.parquet")
df.to_csv(OUT_DIR / "game_publishers_clean.csv", index=False, encoding="utf-8")

print("CSV written:", OUT_DIR / "game_publishers_clean.csv")
print("Rows:", len(df))