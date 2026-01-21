import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load local environment variables (for development)
load_dotenv()

# Connect to Railway PostgreSQL
conn = psycopg2.connect(
    host=os.environ["PGHOST"],
    database=os.environ["PGDATABASE"],
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
    port=os.environ["PGPORT"],
    options="-c search_path=public"
)

# Query to fetch joined sales data
query = """
SELECT
    c.name AS customer,
    p.product_name,
    s.quantity,
    p.price,
    (s.quantity * p.price) AS total_amount,
    s.sale_date
FROM public.sales s
JOIN public.customers c ON s.customer_id = c.customer_id
JOIN public.products p ON s.product_id = p.product_id
ORDER BY s.sale_date DESC;
"""

# Load data into pandas dataframe
df = pd.read_sql(query, conn)

st.title("🛒 Retail Sales Dashboard")

# Show the table
st.dataframe(df)

# Show total revenue metric
st.metric("Total Revenue (₦)", f"{df['total_amount'].sum():,.2f}")

conn.close()
