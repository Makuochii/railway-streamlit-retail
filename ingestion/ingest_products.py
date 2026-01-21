from utils import get_db_connection

products = [
    ("Laptop", 450000),
    ("Phone", 300000),
    ("Headphones", 75000)
]

def ingest_products():
    conn = get_db_connection()
    cur = conn.cursor()

    for name, price in products:
        cur.execute(
            """
            INSERT INTO products (product_name, price)
            VALUES (%s, %s)
            ON CONFLICT (product_name) DO NOTHING
            """,
            (name, price)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ingest_products()
