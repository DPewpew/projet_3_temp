# scripts/transform_v2.py
import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# -------------------------
# Config (defaults)
# -------------------------
DEFAULT_RAW_JSON = Path("data/raw/games.json")   # dict {appid: {...}}
DEFAULT_OUT_DIR = Path("data/cleaned")


# -------------------------
# Helpers
# -------------------------
RE_OWNERS = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")


def owners_mid_to_int(s: Any) -> Optional[int]:
    """
    Convertit "20000 - 50000" -> 35000 (milieu).
    Retourne None si non parsable.
    """
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return None
    raw = str(s).strip().replace(",", "")
    m = RE_OWNERS.match(raw)
    if not m:
        return None
    low = int(m.group(1))
    high = int(m.group(2))
    return int((low + high) / 2)


def safe_int(x: Any) -> Optional[int]:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    try:
        return int(float(x))
    except Exception:
        return None


def to_bool(x: Any) -> Optional[bool]:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    if isinstance(x, bool):
        return x
    s = str(x).strip().lower()
    if s in {"true", "1", "yes", "y"}:
        return True
    if s in {"false", "0", "no", "n"}:
        return False
    return None


def parse_release_date(x: Any) -> Optional[pd.Timestamp]:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    s = str(x).strip()
    if not s:
        return None
    dt = pd.to_datetime(s, errors="coerce", format="%b %d, %Y")
    if pd.isna(dt):
        dt = pd.to_datetime(s, errors="coerce")
    if pd.isna(dt):
        return None
    return dt


def parse_to_list(x: Any) -> List[str]:
    """
    Convertit proprement un champ pouvant être :
    - list[str]
    - string style python "['English','French']"
    - string CSV "English,French"
    - None
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return []

    if isinstance(x, list):
        items = x
    elif isinstance(x, tuple):
        items = list(x)
    elif isinstance(x, dict):
        # pour ce projet, on préfère éviter dict->list sauf si dict de strings,
        # mais on garde une logique simple : valeurs si ce sont des strings, sinon keys.
        vals = list(x.values())
        if vals and all(isinstance(v, str) for v in vals):
            items = vals
        else:
            items = list(x.keys())
    else:
        s = str(x).strip()
        if not s:
            return []
        # string qui ressemble à une liste python
        if s.startswith("[") and s.endswith("]"):
            try:
                parsed = ast.literal_eval(s)
                items = parsed if isinstance(parsed, list) else []
            except Exception:
                items = []
        else:
            # CSV fallback
            items = [p.strip() for p in s.split(",")]

    out: List[str] = []
    for it in items:
        if it is None:
            continue
        v = str(it).strip()
        if v:
            out.append(v)
    return out


def build_bridge(app_ids: pd.Series, values_series: pd.Series, value_name: str) -> pd.DataFrame:
    """
    Crée une table bridge (appid, value_name) en explosant une colonne liste.
    - dédoublonne (appid, value)
    - supprime vides
    """
    tmp = pd.DataFrame(
        {
            "appid": app_ids.apply(safe_int),
            value_name: values_series.apply(parse_to_list),
        }
    )
    tmp = tmp[tmp["appid"].notna()].copy()
    tmp["appid"] = tmp["appid"].astype(int)

    tmp = tmp.explode(value_name, ignore_index=True)
    tmp[value_name] = tmp[value_name].astype("string").str.strip()
    tmp = tmp[tmp[value_name].notna() & (tmp[value_name] != "")]
    tmp = tmp.drop_duplicates(subset=["appid", value_name], keep="first")

    return tmp


def write_df(df: pd.DataFrame, out_dir: Path, stem: str, fmt: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if fmt == "parquet":
        path = out_dir / f"{stem}.parquet"
        df.to_parquet(path, index=False)
        return path
    if fmt == "csv":
        path = out_dir / f"{stem}.csv"
        df.to_csv(path, index=False, encoding="utf-8")
        return path
    raise ValueError("fmt must be 'parquet' or 'csv'")


# -------------------------
# Main transform
# -------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Transform raw Steam JSON dict into clean tables (V2).")
    parser.add_argument("--input", default=str(DEFAULT_RAW_JSON), help="Path to raw games.json (dict {appid:{...}}).")
    parser.add_argument("--outdir", default=str(DEFAULT_OUT_DIR), help="Output folder for clean files.")
    parser.add_argument("--format", choices=["parquet", "csv"], default="parquet", help="Output format.")
    args = parser.parse_args()

    raw_path = Path(args.input)
    out_dir = Path(args.outdir)
    fmt = args.format

    # 1) Read JSON (dict {appid: {...}})
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient="index").reset_index()
    df.rename(columns={"index": "appid"}, inplace=True)

    # 2) (option) Exclude "0 - 0" owners like V1
    if "estimated_owners" in df.columns:
        df = df[df["estimated_owners"] != "0 - 0"].copy()

    # 3) appid type
    df["appid"] = pd.to_numeric(df["appid"], errors="coerce").astype("Int64")
    df = df[df["appid"].notna()].copy()
    df["appid"] = df["appid"].astype(int)

    # 4) Scalar table: games_clean (keep only what you decided)
    # Map raw column names (your raw uses snake_case from v1)
    # Required raw fields for this V2:
    # name, release_date, estimated_owners, required_age, windows, mac, linux, positive, negative
    games = pd.DataFrame()
    games["appid"] = df["appid"].astype(int)
    games["name"] = df.get("name", pd.Series([None] * len(df))).astype("string")

    # Release date
    release_dt = df.get("release_date", pd.Series([None] * len(df))).apply(parse_release_date)
    release_dt = pd.to_datetime(release_dt, errors="coerce")
    games["release_date"] = release_dt.dt.date
    games["release_year"] = release_dt.dt.year.astype("Int64")

    # Owners
    owners_raw = df.get("estimated_owners", pd.Series([None] * len(df)))
    games["estimated_owners"] = owners_raw.astype("string")
    games["estimated_owners_numeric"] = owners_raw.apply(owners_mid_to_int).astype("Int64")

    # Required age + platforms
    games["required_age"] = df.get("required_age", pd.Series([None] * len(df))).apply(safe_int).astype("Int64")
    games["windows"] = df.get("windows", pd.Series([None] * len(df))).apply(to_bool).astype("boolean")
    games["mac"] = df.get("mac", pd.Series([None] * len(df))).apply(to_bool).astype("boolean")
    games["linux"] = df.get("linux", pd.Series([None] * len(df))).apply(to_bool).astype("boolean")

    # Reviews
    games["positive"] = df.get("positive", pd.Series([None] * len(df))).apply(safe_int).astype("Int64")
    games["negative"] = df.get("negative", pd.Series([None] * len(df))).apply(safe_int).astype("Int64")

    # Optional fields (kept nullable if present)
    if "user_score" in df.columns:
        games["user_score"] = pd.to_numeric(df["user_score"], errors="coerce")
    if "recommendations" in df.columns:
        games["recommendations"] = df["recommendations"].apply(safe_int).astype("Int64")

    # Deduplicate appid (keep row with most non-null scalar fields)
    completeness = games.notna().sum(axis=1)
    games = games.assign(_score=completeness).sort_values(["appid", "_score"], ascending=[True, False])
    games = games.drop_duplicates(subset=["appid"], keep="first").drop(columns=["_score"])

    valid_ids = set(games["appid"].tolist())

    # 5) Bridges (languages / categories / genres)
    # raw fields from v1 dataset are snake_case: supported_languages, categories, genres
    # but we support fallback names too.
    supported_lang_col = "supported_languages" if "supported_languages" in df.columns else "Supported languages"
    categories_col = "categories" if "categories" in df.columns else "Categories"
    genres_col = "genres" if "genres" in df.columns else "Genres"

    game_languages = (
        build_bridge(df["appid"], df.get(supported_lang_col, pd.Series([None] * len(df))), "language")
        if supported_lang_col in df.columns
        else pd.DataFrame(columns=["appid", "language"])
    )
    game_categories = (
        build_bridge(df["appid"], df.get(categories_col, pd.Series([None] * len(df))), "category")
        if categories_col in df.columns
        else pd.DataFrame(columns=["appid", "category"])
    )
    game_genres = (
        build_bridge(df["appid"], df.get(genres_col, pd.Series([None] * len(df))), "genre")
        if genres_col in df.columns
        else pd.DataFrame(columns=["appid", "genre"])
    )

    # Keep only appids that exist in games
    if not game_languages.empty:
        game_languages = game_languages[game_languages["appid"].isin(valid_ids)].copy()
    if not game_categories.empty:
        game_categories = game_categories[game_categories["appid"].isin(valid_ids)].copy()
    if not game_genres.empty:
        game_genres = game_genres[game_genres["appid"].isin(valid_ids)].copy()

    # 6) Write outputs
    p1 = write_df(games, out_dir, "games_clean", fmt)
    p2 = write_df(game_languages, out_dir, "game_languages_clean", fmt)
    p3 = write_df(game_categories, out_dir, "game_categories_clean", fmt)
    p4 = write_df(game_genres, out_dir, "game_genres_clean", fmt)

    # 7) Quick checks
    print("Saved:")
    print(" -", p1)
    print(" -", p2)
    print(" -", p3)
    print(" -", p4)
    print()
    print("Rows:")
    print(" games_clean:", f"{len(games):,}")
    print(" game_languages_clean:", f"{len(game_languages):,}")
    print(" game_categories_clean:", f"{len(game_categories):,}")
    print(" game_genres_clean:", f"{len(game_genres):,}")
    print()
    print("Null rates (games_clean) [%]:")
    null_rates = (games.isna().mean() * 100).round(2).sort_values(ascending=False)
    print(null_rates.to_string())


if __name__ == "__main__":
    main()