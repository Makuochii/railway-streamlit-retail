from dotenv import load_dotenv
load_dotenv()


import os
import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Sample Retail Analytics Dashboard By Makuochi Using Python, PostgresSQL & Railway Cloud",
    page_icon="📊",
    layout="wide",
)

# ----------------------------
# ENVIRONMENT VARIABLES
# ----------------------------
REQUIRED_VARS = ["PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD", "PGPORT"]
missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
if missing:
    st.error(f"Missing environment variables: {', '.join(missing)}")
    st.stop()

# ----------------------------
# DATABASE CONNECTION (CACHED)
# ----------------------------
@st.cache_resource(show_spinner=False)
def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT"),
    )

# ----------------------------
# AGGREGATED DATA (CACHED)
# ----------------------------
@st.cache_data(ttl=300, show_spinner=True)
def load_kpis():
    query = """
        SELECT
            COUNT(*) AS total_sales,
            SUM(s.quantity * p.price) AS total_revenue,
            COUNT(DISTINCT s.customer_id) AS total_customers,
            COUNT(DISTINCT p.product_id) AS total_products
        FROM sales s
        JOIN products p ON s.product_id = p.product_id;
    """
    return pd.read_sql(query, get_connection()).iloc[0]

@st.cache_data(ttl=300, show_spinner=True)
def load_top_products(limit=5):
    query = f"""
        SELECT
            p.product_name,
            SUM(s.quantity) AS units_sold,
            SUM(s.quantity * p.price) AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, get_connection())

@st.cache_data(ttl=300, show_spinner=True)
def load_top_customers(limit=5):
    query = f"""
        SELECT
            c.name AS customer,
            SUM(s.quantity * p.price) AS total_spent
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        JOIN products p ON s.product_id = p.product_id
        GROUP BY c.name
        ORDER BY total_spent DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, get_connection())

# ----------------------------
# HEADER
# ----------------------------
st.title("📊 Retail Aggregated Dashboard By Makuochi")
st.caption("Aggregated KPIs with responsive charts • Cached for speed")

# ----------------------------
# KPI CARDS (STACKABLE ON MOBILE)
# ----------------------------
kpis = load_kpis()
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₦{kpis.total_revenue:,.0f}")
col2.metric("🛒 Total Sales", int(kpis.total_sales))
col3.metric("👥 Customers", int(kpis.total_customers))
col4.metric("📦 Products", int(kpis.total_products))

st.divider()

# ----------------------------
# TOP PRODUCTS BAR CHART
# ----------------------------
top_products = load_top_products()

fig_products = px.bar(
    top_products,
    x="product_name",
    y="revenue",
    text="revenue",
    title="Top Products by Revenue",
)
fig_products.update_traces(texttemplate="₦%{text:,.0f}", textposition="outside")
fig_products.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(fig_products, use_container_width=True)

# ----------------------------
# TOP CUSTOMERS BAR CHART
# ----------------------------
top_customers = load_top_customers()

fig_customers = px.bar(
    top_customers,
    x="customer",
    y="total_spent",
    text="total_spent",
    title="Top Customers by Spend",
)
fig_customers.update_traces(texttemplate="₦%{text:,.0f}", textposition="outside")
fig_customers.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(fig_customers, use_container_width=True)

# ----------------------------
# FOOTER
# ----------------------------
st.caption("Optimized for mobile & desktop • Aggregations only • Fast-loading")
