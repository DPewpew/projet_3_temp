CREATE TABLE stg_game_publishers_clean (
  appid INT NOT NULL,
  publisher TEXT NOT NULL
);

CREATE TABLE dim_publisher (
  publisher_id SERIAL PRIMARY KEY,
  publisher TEXT UNIQUE NOT NULL
);

CREATE TABLE fact_game_publisher (
  appid INT NOT NULL,
  publisher_id INT NOT NULL,
  PRIMARY KEY (appid, publisher_id),
  FOREIGN KEY (appid) REFERENCES fact_game_clean(appid),
  FOREIGN KEY (publisher_id) REFERENCES dim_publisher(publisher_id)
);