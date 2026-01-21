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


customers = [
    ("Aisha Bello", "aisha@email.com"),
    ("John Okafor", "john@email.com"),
    ("Fatima Musa", "fatima@email.com"),
    ("David Ade", "david@email.com"),
    ("Blessing Obi", "blessing@email.com"),
    ("Sadiq Lawal", "sadiq@email.com"),
    ("Mary Danjuma", "mary@email.com"),
    ("Ibrahim Sule", "ibrahim@email.com"),
    ("Esther King", "esther@email.com"),
    ("Samuel Peters", "samuel@email.com"),
]

cur.executemany("""
INSERT INTO customers (name, email)
VALUES (%s, %s)
ON CONFLICT (email) DO NOTHING;
""", customers)

# Products
products = [
    ("Rice 50kg", 45000),
    ("Beans 50kg", 38000),
    ("Garri 50kg", 25000),
    ("Sugar 25kg", 18000),
    ("Flour 50kg", 32000),
    ("Cooking Oil 25L", 41000),
    ("Salt 10kg", 6000),
    ("Spaghetti Carton", 12000),
    ("Tomato Paste Carton", 15000),
    ("Milk Carton", 17000),
]

cur.executemany("""
INSERT INTO products (product_name, price)
VALUES (%s, %s)
ON CONFLICT DO NOTHING;
""", products)

# Sales
sales = [
    (1, 1, 2),
    (2, 2, 1),
    (3, 3, 5),
    (4, 4, 2),
    (5, 5, 1),
    (6, 6, 3),
    (7, 7, 4),
    (8, 8, 2),
    (9, 9, 1),
    (10, 10, 2),
]

cur.executemany("""
INSERT INTO sales (customer_id, product_id, quantity)
VALUES (%s, %s, %s);
""", sales)

conn.commit()
print("✅ Sample data inserted successfully")

conn.commit()
