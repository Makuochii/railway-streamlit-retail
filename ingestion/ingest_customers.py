from utils import get_db_connection

customers = [
    "Shoprite Abuja",
    "Next Cash & Carry",
    "Local Retailer"
]

def ingest_customers():
    conn = get_db_connection()
    cur = conn.cursor()

    for name in customers:
        cur.execute(
            """
            INSERT INTO customers (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            """,
            (name,)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ingest_customers()
