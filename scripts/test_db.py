import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="steam_project",
    user="postgres",
    password="1111"
)

cur = conn.cursor()
cur.execute("SELECT 1;")
print(cur.fetchone())

cur.close()
conn.close()
