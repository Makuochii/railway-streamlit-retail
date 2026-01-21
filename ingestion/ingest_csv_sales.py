import pandas as pd
from utils import get_db_connection

def ingest_sales():
    df = pd.read_csv("data/sales.csv")  # example source

    conn = get_db_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO sales (customer_id, product_id, quantity)
            VALUES (%s, %s, %s)
            """,
            (row.customer_id, row.product_id, row.quantity)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ingest_sales()
