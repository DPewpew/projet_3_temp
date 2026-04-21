# scripts/fix_languages_v2.py
import argparse
import ast
import html
import json
import re
from pathlib import Path
from typing import Any, List, Optional, Set

import numpy as np
import pandas as pd

DEFAULT_RAW = Path("data/raw/games.json")
DEFAULT_OUT_DIR = Path("data/cleaned")

TAG_RE = re.compile(r"<[^>]+>")
BR_RE = re.compile(r"(?i)<\s*br\s*/?\s*>")
MULTISPACE_RE = re.compile(r"\s+")
FULL_AUDIO_RE = re.compile(r"(?i)\(.*?full\s*audio.*?\)")
SQUARE_TAG_RE = re.compile(r"\[/?[a-zA-Z]+\]")
ANGLE_EMPTY_RE = re.compile(r"<\s*/?\s*>")

# splitters inclut "||"
SPLIT_RE = re.compile(r"\|\||\||,|;|/|\n|\r|\t")

# remove trailing junk punctuation
TRAIL_JUNK_RE = re.compile(r"[,\;|]+$")

# remove "#lang_xxx"
LANG_HASH_RE = re.compile(r"^#lang_[a-z0-9_]+$", re.IGNORECASE)

# remove parentheses content: "Punjabi (Gurmukhi)" -> "Punjabi"
PARENS_RE = re.compile(r"\s*\(.*?\)\s*")


def safe_int(x: Any) -> Optional[int]:
    try:
        return int(x)
    except Exception:
        return None


def dedupe_preserve_order(items: List[str]) -> List[str]:
    seen: Set[str] = set()
    out: List[str] = []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def normalize_text(s: str) -> str:
    if not s:
        return ""

    # decode multi-level HTML entities
    for _ in range(6):
        new_s = html.unescape(s)
        if new_s == s:
            break
        s = new_s

    # keep <br> as delimiter
    s = BR_RE.sub("|", s)
    s = TAG_RE.sub("", s)

    s = SQUARE_TAG_RE.sub("", s)
    s = ANGLE_EMPTY_RE.sub("", s)
    s = FULL_AUDIO_RE.sub("", s)

    s = MULTISPACE_RE.sub(" ", s).strip()
    return s


def clean_one_token(tok: str) -> str:
    tok = tok.strip().strip("*").strip()
    tok = TRAIL_JUNK_RE.sub("", tok).strip()

    # canonicalize "Spanish - Spain" -> "Spanish"
    if " - " in tok:
        tok = tok.split(" - ", 1)[0].strip()

    # remove parentheses content
    tok = PARENS_RE.sub(" ", tok).strip()
    tok = MULTISPACE_RE.sub(" ", tok).strip()

    return tok


def build_language_vocab() -> Set[str]:
    """
    Base vocab: on met une liste de langues "attendues" (la tienne + variantes courantes).
    Permet de splitter proprement les lignes collées "English Russian Spanish".
    """
    base = {
        "Afrikaans","Albanian","Amharic","Arabic","Armenian","Assamese","Azerbaijani","Bangla",
        "Basque","Belarusian","Bosnian","Bulgarian","Catalan","Cherokee","Croatian","Czech",
        "Danish","Dari","Dutch","English","Estonian","Filipino","Finnish","French","Galician",
        "Georgian","German","Greek","Gujarati","Hausa","Hebrew","Hindi","Hungarian","Icelandic",
        "Igbo","Indonesian","Irish","Italian","Japanese","K'iche'","Kannada","Kazakh","Khmer",
        "Kinyarwanda","Konkani","Korean","Kyrgyz","Latvian","Lithuanian","Luxembourgish",
        "Macedonian","Malay","Malayalam","Maltese","Maori","Marathi","Mongolian","Nepali",
        "Norwegian","Odia","Persian","Polish","Portuguese","Punjabi","Quechua","Romanian",
        "Russian","Scots","Serbian","Simplified Chinese","Sindhi","Sinhala","Slovak",
        "Slovenian","Sorani","Sotho","Spanish","Swahili","Swedish","Tajik","Tamil","Tatar",
        "Telugu","Thai","Tigrinya","Traditional Chinese","Tswana","Turkish","Turkmen",
        "Ukrainian","Urdu","Uyghur","Uzbek","Valencian","Vietnamese","Welsh","Wolof","Xhosa",
        "Yoruba","Zulu",
    }
    return base


VOCAB = build_language_vocab()


def split_glued_if_possible(text: str) -> List[str]:
    """
    Si on a "English Russian Spanish", on split par espace
    UNIQUEMENT si tous les tokens sont dans VOCAB.
    Sinon on retourne [text] (pour éviter de casser "Simplified Chinese").
    """
    tokens = text.split()
    if len(tokens) >= 2 and all(t in VOCAB for t in tokens):
        return tokens
    return [text]


def parse_supported_languages(raw_val: Any) -> List[str]:
    if raw_val is None or (isinstance(raw_val, float) and np.isnan(raw_val)):
        return []

    # list
    if isinstance(raw_val, list):
        out = []
        for it in raw_val:
            txt = normalize_text(str(it))
            for part in SPLIT_RE.split(txt.replace("|", "||")):
                tok = clean_one_token(part)
                if tok and not LANG_HASH_RE.match(tok):
                    # attempt to split glued
                    for g in split_glued_if_possible(tok):
                        g2 = clean_one_token(g)
                        if g2 and not LANG_HASH_RE.match(g2):
                            out.append(g2)
        return dedupe_preserve_order(out)

    s = str(raw_val).strip()
    if not s:
        return []

    # python list string
    if s.startswith("[") and s.endswith("]"):
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return parse_supported_languages(parsed)
        except Exception:
            pass

    # html / delimited string
    cleaned = normalize_text(s)

    # standardize || markers
    cleaned = cleaned.replace("||", "|")

    parts = SPLIT_RE.split(cleaned)

    out: List[str] = []
    for p in parts:
        tok = clean_one_token(p)
        if not tok or LANG_HASH_RE.match(tok):
            continue

        # remove weird leftovers
        tok = tok.replace("||", "").strip()
        tok = MULTISPACE_RE.sub(" ", tok).strip()

        # split glued languages if safe
        for g in split_glued_if_possible(tok):
            g2 = clean_one_token(g)
            if g2 and not LANG_HASH_RE.match(g2):
                out.append(g2)

    return dedupe_preserve_order(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default=str(DEFAULT_RAW))
    parser.add_argument("--out", default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args()

    raw_path = Path(args.raw)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient="index").reset_index()
    df.rename(columns={"index": "appid"}, inplace=True)

    df["appid"] = df["appid"].apply(safe_int)
    df = df[df["appid"].notna()].copy()
    df["appid"] = df["appid"].astype(int)

    col = "supported_languages" if "supported_languages" in df.columns else "Supported languages"
    if col not in df.columns:
        raise KeyError("Colonne supported languages introuvable (supported_languages / Supported languages).")

    clean = pd.DataFrame(
        {
            "appid": df["appid"],
            "language": df[col].apply(parse_supported_languages),
        }
    )

    clean = clean.explode("language", ignore_index=True)
    clean["language"] = clean["language"].astype("string").str.strip()
    clean = clean[clean["language"].notna() & (clean["language"] != "")]
    clean = clean.drop_duplicates(subset=["appid", "language"])

    parquet_path = out_dir / "game_languages_clean.parquet"
    csv_path = out_dir / "game_languages_clean.csv"

    clean.to_parquet(parquet_path, index=False)
    clean.to_csv(csv_path, index=False, encoding="utf-8")

    print("Saved:")
    print(" -", parquet_path)
    print(" -", csv_path)
    print("Rows:", len(clean))
    print("Distinct languages:", clean["language"].nunique())
    print("Top 30 languages:")
    print(clean["language"].value_counts().head(30).to_string())

    # quick: show suspicious rows (tokens with commas/semicolons/pipes should not exist anymore)
    suspicious = clean[clean["language"].str.contains(r"[,\;|#<>]", regex=True, na=False)]
    print("\nSuspicious values (should be 0 rows):", len(suspicious))
    if len(suspicious) > 0:
        print(suspicious["language"].value_counts().head(30).to_string())


if __name__ == "__main__":
    main()