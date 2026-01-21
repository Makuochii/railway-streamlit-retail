from dotenv import load_dotenv
load_dotenv()


import os
import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------
# PAGE CONFIG (MOBILE FRIENDLY)
# ----------------------------
st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide"
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
        port=os.getenv("PGPORT")
    )

# ----------------------------
# DATA QUERIES (CACHED)
# ----------------------------
@st.cache_data(ttl=300, show_spinner=True)
def load_sales_summary():
    query = """
        SELECT
            DATE(s.sale_date) AS date,
            SUM(s.quantity * p.price) AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY DATE(s.sale_date)
        ORDER BY date;
    """
    return pd.read_sql(query, get_connection())


@st.cache_data(ttl=300, show_spinner=True)
def load_kpis():
    query = """
        SELECT
            COUNT(*) AS total_sales,
            SUM(s.quantity * p.price) AS total_revenue,
            COUNT(DISTINCT s.customer_id) AS total_customers
        FROM sales s
        JOIN products p ON s.product_id = p.product_id;
    """
    return pd.read_sql(query, get_connection()).iloc[0]


@st.cache_data(ttl=300, show_spinner=True)
def load_top_products():
    query = """
        SELECT
            p.product_name,
            SUM(s.quantity) AS units_sold
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY units_sold DESC
        LIMIT 5;
    """
    return pd.read_sql(query, get_connection())


# ----------------------------
# HEADER
# ----------------------------
st.title("📊 Retail Performance Dashboard")
st.caption("Live analytics powered by PostgreSQL & Railway")

# ----------------------------
# KPI SECTION (MOBILE STACKABLE)
# ----------------------------
kpis = load_kpis()

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("💰 Total Revenue", f"₦{kpis.total_revenue:,.0f}")
kpi2.metric("🛒 Total Sales", int(kpis.total_sales))
kpi3.metric("👥 Customers", int(kpis.total_customers))

st.divider()

# ----------------------------
# SALES TREND (RESPONSIVE)
# ----------------------------
sales_df = load_sales_summary()

fig_sales = px.line(
    sales_df,
    x="date",
    y="revenue",
    markers=True,
    title="Revenue Over Time"
)

fig_sales.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_sales, use_container_width=True)

# ----------------------------
# TOP PRODUCTS
# ----------------------------
top_products = load_top_products()

fig_products = px.bar(
    top_products,
    x="product_name",
    y="units_sold",
    title="Top Selling Products"
)

fig_products.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_products, use_container_width=True)

# ----------------------------
# FOOTER
# ----------------------------
st.caption("Optimized for mobile • Cached for performance • Production-ready")
