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

# What database am I connected to?
cur.execute("SELECT current_database();")
print("Database:", cur.fetchone()[0])

# What schemas exist?
cur.execute("SELECT schema_name FROM information_schema.schemata;")
print("Schemas:")
for row in cur.fetchall():
    print(" -", row[0])

# What tables exist (all schemas)?
cur.execute("""
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type='BASE TABLE'
ORDER BY table_schema, table_name;
""")

print("\nTables:")
rows = cur.fetchall()
if not rows:
    print("❌ NO TABLES FOUND")
else:
    for r in rows:
        print(r)

cur.close()
conn.close()
