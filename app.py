from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import psycopg2
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

from analytics.queries import load_sales
from analytics.metrics import compute_kpis

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Retail Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Retail Analytics Dashboard")

# -------------------------------------------------
# ENVIRONMENT VARIABLES CHECK
# -------------------------------------------------
REQUIRED_ENV_VARS = ["PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD", "PGPORT"]
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    st.error(f"Missing environment variables: {', '.join(missing_vars)}")
    st.stop()

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=int(os.getenv("PGPORT"))
    )

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
with st.sidebar:
    st.header("⚙️ Dashboard Controls")

    auto_refresh = st.toggle("🔄 Auto Refresh (5 mins)", value=False)

    st.markdown("---")
    st.header("🔎 Filters")

# -------------------------------------------------
# AUTO REFRESH (SAFE FOR RAILWAY)
# -------------------------------------------------
if auto_refresh:
    st.cache_data.clear()
    st.rerun()

# -------------------------------------------------
# CACHED DATA LOADING
# -------------------------------------------------
@st.cache_data(ttl=300)  # 5 minutes
def load_data():
    conn = get_connection()
    df = load_sales(conn)
    conn.close()
    return df, datetime.utcnow()

df, last_refresh = load_data()
df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.date

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
with st.sidebar:
    min_date = df["sale_date"].min()
    max_date = df["sale_date"].max()

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    products = st.multiselect(
        "Products",
        sorted(df["product_name"].unique()),
        default=sorted(df["product_name"].unique())
    )

    customers = st.multiselect(
        "Customers",
        sorted(df["customer"].unique()),
        default=sorted(df["customer"].unique())
    )

# -------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------
filtered_df = df[
    (df["sale_date"] >= date_range[0]) &
    (df["sale_date"] <= date_range[1]) &
    (df["product_name"].isin(products)) &
    (df["customer"].isin(customers))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# -------------------------------------------------
# LAST REFRESH INDICATOR
# -------------------------------------------------
st.caption(f"🕒 Last refreshed: {last_refresh.strftime('%Y-%m-%d %H:%M:%S')} UTC")

# -------------------------------------------------
# KPIs
# -------------------------------------------------
kpis = compute_kpis(filtered_df)

st.markdown("### 📌 Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue", f"₦{kpis['total_revenue']:,.0f}")
c2.metric("🧾 Total Sales", kpis["total_sales"])
c3.metric("📦 Avg Order Value", f"₦{kpis['avg_order_value']:,.0f}")
c4.metric("👥 Unique Customers", kpis["unique_customers"])

# -------------------------------------------------
# CHARTS (RESPONSIVE)
# -------------------------------------------------
st.markdown("### 📈 Revenue Over Time")
daily_revenue = filtered_df.groupby("sale_date", as_index=False)["revenue"].sum()
fig = px.line(daily_revenue, x="sale_date", y="revenue", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🏆 Top Products")
top_products = filtered_df.groupby("product_name", as_index=False)["revenue"].sum()
fig2 = px.bar(top_products, x="product_name", y="revenue", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 👤 Customer Revenue")
customer_rev = filtered_df.groupby("customer", as_index=False)["revenue"].sum()
st.dataframe(customer_rev, use_container_width=True)
