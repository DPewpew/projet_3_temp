-- 1) Dims
INSERT INTO dim_language(language)
SELECT DISTINCT language
FROM stg_game_languages_clean
ON CONFLICT (language) DO NOTHING;

INSERT INTO dim_category(category)
SELECT DISTINCT category
FROM stg_game_categories_clean
ON CONFLICT (category) DO NOTHING;

INSERT INTO dim_genre(genre)
SELECT DISTINCT genre
FROM stg_game_genres_clean
ON CONFLICT (genre) DO NOTHING;

-- 2) Bridges (mapping texte -> id)
INSERT INTO fact_game_language(appid, language_id)
SELECT s.appid, d.language_id
FROM stg_game_languages_clean s
JOIN dim_language d ON d.language = s.language
JOIN fact_game_clean f ON f.appid = s.appid
ON CONFLICT DO NOTHING;

INSERT INTO fact_game_category(appid, category_id)
SELECT s.appid, d.category_id
FROM stg_game_categories_clean s
JOIN dim_category d ON d.category = s.category
JOIN fact_game_clean f ON f.appid = s.appid
ON CONFLICT DO NOTHING;

INSERT INTO fact_game_genre(appid, genre_id)
SELECT s.appid, d.genre_id
FROM stg_game_genres_clean s
JOIN dim_genre d ON d.genre = s.genre
JOIN fact_game_clean f ON f.appid = s.appid
ON CONFLICT DO NOTHING;