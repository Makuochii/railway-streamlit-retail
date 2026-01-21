import pandas as pd

def load_sales(conn):
    query = """
    SELECT
        s.sale_date::date AS sale_date,
        c.name AS customer,
        p.product_name,
        s.quantity,
        p.price,
        (s.quantity * p.price) AS revenue
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    JOIN products p ON s.product_id = p.product_id
    """
    return pd.read_sql(query, conn)
