import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()




conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    database=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    port=os.getenv("PGPORT"),
    sslmode = 'require'
)

cur = conn.cursor()

# drop tables

cur.execute(
    """
    DROP TABLE customers CASCADE
"""
)





cur.execute(
    """
    DROP TABLE products CASCADE
"""
)




cur.execute(
    """
    DROP TABLE sales CASCADE
"""
)



# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS public.customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS public.products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS public.sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL
);
""")

conn.commit()
print("✅ Tables dropped and created correspondingly and successfully")

cur.close()
conn.close()
