
BEGIN;

-- 2) Rebuild bridge + dim
TRUNCATE fact_game_language;
TRUNCATE dim_language RESTART IDENTITY CASCADE;

INSERT INTO dim_language(language)
SELECT DISTINCT TRIM(language)
FROM stg_game_languages_clean
WHERE language IS NOT NULL AND TRIM(language) <> '';

INSERT INTO fact_game_language(appid, language_id)
SELECT DISTINCT s.appid, d.language_id
FROM stg_game_languages_clean s
JOIN dim_language d ON d.language = TRIM(s.language)
JOIN fact_game_clean f ON f.appid = s.appid;

COMMIT;

-- 3) Checks
SELECT COUNT(*) AS dim_languages FROM dim_language;
SELECT COUNT(*) AS bridge_lang   FROM fact_game_language;

-- Spot check: valeurs "sales" (attendu: 0)
SELECT COUNT(*) AS suspicious_lang_values
FROM dim_language
WHERE language ~ '[,;|#<>]'
   OR language ILIKE '%&%';

