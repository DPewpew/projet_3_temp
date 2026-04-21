# scripts/fix_publishers.py
import json
import ast
from pathlib import Path
import pandas as pd
import numpy as np

RAW_JSON = Path("data/raw/games.json")
OUT_DIR = Path("data/cleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def safe_int(x):
    try:
        return int(x)
    except:
        return None


def parse_to_list(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return []
    if isinstance(x, list):
        items = x
    else:
        s = str(x).strip()
        if not s:
            return []
        if s.startswith("[") and s.endswith("]"):
            try:
                items = ast.literal_eval(s)
            except:
                items = []
        else:
            items = [s]
    return [str(i).strip() for i in items if str(i).strip()]


def main():
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient="index").reset_index()
    df.rename(columns={"index": "appid"}, inplace=True)

    df["appid"] = df["appid"].apply(safe_int)
    df = df[df["appid"].notna()].copy()
    df["appid"] = df["appid"].astype(int)

    pub_col = "publishers" if "publishers" in df.columns else "Publishers"

    publishers = pd.DataFrame({
        "appid": df["appid"],
        "publisher": df[pub_col].apply(parse_to_list)
    })

    publishers = publishers.explode("publisher", ignore_index=True)
    publishers["publisher"] = publishers["publisher"].astype("string").str.strip()

    publishers = publishers[
        publishers["publisher"].notna() &
        (publishers["publisher"] != "")
    ]

    publishers = publishers.drop_duplicates(subset=["appid", "publisher"])

    publishers.to_parquet(OUT_DIR / "game_publishers_clean.parquet", index=False)
    publishers.to_csv(OUT_DIR / "game_publishers_clean.csv", index=False, encoding="utf-8")

    print("Saved game_publishers_clean")
    print("Rows:", len(publishers))


if __name__ == "__main__":
    main()