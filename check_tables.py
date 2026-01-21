import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    database=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    port=os.getenv("PGPORT")
)

cur = conn.cursor()

cur.execute("""
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type='BASE TABLE';
""")

tables = cur.fetchall()
for t in tables:
    print(t)

cur.close()
conn.close()
