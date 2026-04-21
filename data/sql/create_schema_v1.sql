-- sql/create_schema_v1.sql

-- (Optionnel) schéma dédié
-- CREATE SCHEMA IF NOT EXISTS steam;
-- SET search_path TO steam;

-- =========================
-- FACT (1 ligne par jeu)
-- =========================
DROP TABLE IF EXISTS fact_game_genre;
DROP TABLE IF EXISTS fact_game_category;
DROP TABLE IF EXISTS fact_game_language;

DROP TABLE IF EXISTS stg_game_genres_clean;
DROP TABLE IF EXISTS stg_game_categories_clean;
DROP TABLE IF EXISTS stg_game_languages_clean;

DROP TABLE IF EXISTS dim_genre;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_language;

DROP TABLE IF EXISTS fact_game_clean;

CREATE TABLE fact_game_clean (
  appid                    INT PRIMARY KEY,
  name                     TEXT NOT NULL,
  release_date             DATE,
  release_year             INT,
  estimated_owners          TEXT,
  estimated_owners_numeric  BIGINT,
  required_age             INT,
  windows                  BOOLEAN,
  mac                      BOOLEAN,
  linux                    BOOLEAN,
  positive                 BIGINT,
  negative                 BIGINT,
  user_score               DOUBLE PRECISION,
  recommendations          BIGINT
);

-- =========================
-- STAGING 
-- =========================
CREATE TABLE stg_game_languages_clean (
  appid     INT NOT NULL,
  language  TEXT NOT NULL
);

CREATE TABLE stg_game_categories_clean (
  appid     INT NOT NULL,
  category  TEXT NOT NULL
);

CREATE TABLE stg_game_genres_clean (
  appid     INT NOT NULL,
  genre     TEXT NOT NULL
);

-- =========================
-- DIMENSIONS
-- =========================
CREATE TABLE dim_language (
  language_id SERIAL PRIMARY KEY,
  language    TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_category (
  category_id SERIAL PRIMARY KEY,
  category    TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_genre (
  genre_id SERIAL PRIMARY KEY,
  genre    TEXT NOT NULL UNIQUE
);

-- =========================
-- BRIDGES (N-N)
-- =========================
CREATE TABLE fact_game_language (
  appid       INT NOT NULL,
  language_id INT NOT NULL,
  PRIMARY KEY (appid, language_id),
  FOREIGN KEY (appid) REFERENCES fact_game_clean(appid),
  FOREIGN KEY (language_id) REFERENCES dim_language(language_id)
);

CREATE TABLE fact_game_category (
  appid        INT NOT NULL,
  category_id  INT NOT NULL,
  PRIMARY KEY (appid, category_id),
  FOREIGN KEY (appid) REFERENCES fact_game_clean(appid),
  FOREIGN KEY (category_id) REFERENCES dim_category(category_id)
);

CREATE TABLE fact_game_genre (
  appid     INT NOT NULL,
  genre_id  INT NOT NULL,
  PRIMARY KEY (appid, genre_id),
  FOREIGN KEY (appid) REFERENCES fact_game_clean(appid),
  FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id)
);

-- Index utiles
CREATE INDEX idx_stg_lang_appid ON stg_game_languages_clean(appid);
CREATE INDEX idx_stg_cat_appid  ON stg_game_categories_clean(appid);
CREATE INDEX idx_stg_gen_appid  ON stg_game_genres_clean(appid);