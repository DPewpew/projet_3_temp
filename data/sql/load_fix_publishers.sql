INSERT INTO dim_publisher(publisher)
SELECT DISTINCT publisher
FROM stg_game_publishers_clean
ON CONFLICT (publisher) DO NOTHING;

INSERT INTO fact_game_publisher(appid, publisher_id)
SELECT s.appid, d.publisher_id
FROM stg_game_publishers_clean s
JOIN dim_publisher d ON d.publisher = s.publisher
JOIN fact_game_clean f ON f.appid = s.appid
ON CONFLICT DO NOTHING;