-- =========================
-- DIMENSIONS
-- =========================

SELECT COUNT(*) AS dim_languages   FROM dim_language;
SELECT COUNT(*) AS dim_categories  FROM dim_category;
SELECT COUNT(*) AS dim_genres      FROM dim_genre;
SELECT COUNT(*) AS dim_publishers  FROM dim_publisher;


-- =========================
-- BRIDGES
-- =========================

SELECT COUNT(*) AS bridge_lang        FROM fact_game_language;
SELECT COUNT(*) AS bridge_cat         FROM fact_game_category;
SELECT COUNT(*) AS bridge_gen         FROM fact_game_genre;
SELECT COUNT(*) AS bridge_publisher   FROM fact_game_publisher;