import streamlit as st
import plotly.express as px
from data import load_data

st.set_page_config(page_title="Olist Sales Insights", layout="wide")
st.title("Olist Sales Insights")
st.caption("Where does revenue come from, and where is delivery hurting customers?")

df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
months = sorted(df["month"].dt.date.unique())
start, end = st.sidebar.select_slider(
    "Period",
    options=months,
    value=(months[0], months[-1]),
    format_func=lambda d: d.strftime("%b %Y"),
)
states = st.sidebar.multiselect("State", sorted(df["customer_state"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["category"].unique()))

mask = (df["month"].dt.date >= start) & (df["month"].dt.date <= end)
if states:
    mask &= df["customer_state"].isin(states)
if cats:
    mask &= df["category"].isin(cats)
f = df[mask]

if f.empty:
    st.warning("No data for these filters. Try widening them.")
    st.stop()

# ---------- Prepared data ----------
orders_df = f.drop_duplicates("order_id")
monthly = f.groupby("month")["revenue"].sum()
cat_rev = f.groupby("category")["revenue"].sum().sort_values(ascending=False)
state_rev = f.groupby("customer_state")["revenue"].sum().sort_values(ascending=False)

by_state = (
    orders_df.groupby("customer_state")
    .agg(orders=("order_id", "count"),
         late_pct=("is_late", "mean"),
         avg_days=("delivery_days", "mean"))
    .reset_index()
)
by_state["late_pct"] *= 100
by_state = by_state[by_state["orders"] >= 100]  # ignore tiny samples

# ---------- KPIs ----------
revenue = f["revenue"].sum()
orders = orders_df.shape[0]
aov = revenue / orders
late_pct = orders_df["is_late"].mean() * 100
growth = None
if len(monthly) >= 2:
    growth = (monthly.iloc[-1] / monthly.iloc[-2] - 1) * 100

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Revenue", f"R$ {revenue:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Avg order value", f"R$ {aov:,.0f}")
c4.metric("MoM growth", f"{growth:+.1f}%" if growth is not None else "n/a")
c5.metric("Late deliveries", f"{late_pct:.1f}%")

st.divider()

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["Revenue", "Delivery", "Insights"])

with tab1:
    fig = px.line(monthly.reset_index(), x="month", y="revenue",
                  markers=True, title="Monthly revenue (R$)")
    st.plotly_chart(fig, use_container_width=True)

    top_cat = cat_rev.head(10).sort_values().reset_index()
    fig = px.bar(top_cat, x="revenue", y="category", orientation="h",
                 title="Top 10 categories by revenue")
    st.plotly_chart(fig, use_container_width=True)

    top_state = state_rev.head(10).sort_values().reset_index()
    fig = px.bar(top_state, x="revenue", y="customer_state", orientation="h",
                 title="Top 10 states by revenue")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    if by_state.empty:
        st.info("Not enough orders per state for delivery analysis with these filters.")
    else:
        worst = by_state.sort_values("late_pct", ascending=False).head(10)
        fig = px.bar(worst, x="customer_state", y="late_pct",
                     title="States with the highest late-delivery rate (%)")
        st.plotly_chart(fig, use_container_width=True)

        fig = px.scatter(by_state, x="avg_days", y="late_pct", size="orders",
                         hover_name="customer_state",
                         title="Avg delivery days vs late rate (bubble = orders)")
        st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(orders_df[orders_df["delivery_days"] <= 60],
                       x="delivery_days", nbins=40,
                       title="Delivery time distribution (days)")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Key findings (update automatically with filters)")
    peak = monthly.idxmax()
    st.markdown(
        f"- **Top category:** `{cat_rev.index[0]}` brings "
        f"{cat_rev.iloc[0] / revenue:.0%} of revenue.\n"
        f"- **Top state:** `{state_rev.index[0]}` brings "
        f"{state_rev.iloc[0] / revenue:.0%} of revenue.\n"
        f"- **Top 5 categories** together make up "
        f"{cat_rev.head(5).sum() / revenue:.0%} of revenue.\n"
        f"- **Peak month:** {peak:%B %Y} "
        f"(R$ {monthly.max():,.0f})."
    )
    if not by_state.empty:
        w = by_state.sort_values("late_pct", ascending=False).iloc[0]
        b = by_state.sort_values("late_pct").iloc[0]
        st.markdown(
            f"- **Worst delivery state:** `{w['customer_state']}` with "
            f"{w['late_pct']:.1f}% late orders and {w['avg_days']:.0f} avg days.\n"
            f"- **Best delivery state:** `{b['customer_state']}` with "
            f"{b['late_pct']:.1f}% late orders."
        )

    st.subheader("Recommendations")
    st.markdown(
        "- Replace this with 3 recommendations in your own words, "
        "based on the findings above."
    )

st.divider()
st.caption("Data: Olist Brazilian E-Commerce Public Dataset (Kaggle). "
           "Delivered orders only, Jan 2017 to Aug 2018. "
           "Revenue = item price, excluding freight.")
