def compute_kpis(df):
    return {
        "total_revenue": df["revenue"].sum(),
        "total_sales": len(df),
        "avg_order_value": df["revenue"].mean(),
        "unique_customers": df["customer"].nunique()
    }
