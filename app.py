import inspect

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data import load_data

# =========================================================
# PAGE CONFIG (must be the first Streamlit call)
# =========================================================

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

# =========================================================
# CONSTANTS
# =========================================================

INDIGO = "#5B5CE2"
PURPLE = "#7C3AED"
BLUE = "#2563EB"
CYAN = "#06B6D4"
GREEN = "#10B981"
ORANGE = "#F59E0B"
RED = "#EF4444"
PINK = "#EC4899"
DARK = "#111827"
GRID = "#EEF0F5"

CHART_COLORS = [INDIGO, PURPLE, CYAN, GREEN, ORANGE, RED, PINK, BLUE, "#14B8A6", "#8B5CF6"]

SCALE_INDIGO = ["#DDD6FE", "#8B5CF6", "#5B5CE2"]
SCALE_BLUE = ["#DBEAFE", "#3B82F6", "#1D4ED8"]
SCALE_AMBER = ["#FDE68A", "#F59E0B", "#EA580C"]
SCALE_RED = ["#FEE2E2", "#F87171", "#DC2626"]

REQUIRED_COLUMNS = ["order_id", "month", "revenue", "customer_state", "category"]
MIN_STATE_ORDERS = 100

PAGES = [
    "Overview",
    "Revenue Intelligence",
    "Sales & Categories",
    "Delivery Operations",
    "Business Insights",
]

# =========================================================
# GLOBAL CSS
# =========================================================

CSS = """
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(91,92,226,0.08), transparent 25%),
        radial-gradient(circle at 90% 10%, rgba(124,58,237,0.06), transparent 25%),
        #F7F8FC;
}
.block-container { max-width: 1500px; padding-top: 1.5rem; padding-bottom: 3rem; }
h1, h2, h3, h4 { color: #111827 !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #1F2937; }
section[data-testid="stSidebar"] * { color: #E5E7EB; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #F9FAFB !important; }
.sidebar-brand { padding: 10px 4px 25px 4px; }
.brand-logo {
    width: 42px; height: 42px; border-radius: 13px;
    background: linear-gradient(135deg, #5B5CE2, #8B5CF6);
    display: flex; align-items: center; justify-content: center;
    color: white !important; font-size: 20px; font-weight: 800;
}
.brand-name { font-size: 18px; font-weight: 800; color: white !important; margin-top: 10px; }
.brand-sub { font-size: 11px; color: #9CA3AF !important; margin-top: 2px; }

/* HEADER */
.eyebrow {
    color: #5B5CE2 !important; font-size: 12px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 7px;
}
.main-title {
    font-size: 38px; line-height: 1.1; font-weight: 800;
    color: #111827 !important; letter-spacing: -1.5px;
}
.subtitle { color: #6B7280 !important; font-size: 15px; margin-top: 8px; margin-bottom: 20px; }
.live-badge {
    display: inline-flex; align-items: center; gap: 7px; padding: 8px 13px;
    border-radius: 999px; background: #ECFDF5; border: 1px solid #A7F3D0;
    color: #047857 !important; font-size: 12px; font-weight: 800;
}
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #10B981; }

/* KPI */
.kpi-card {
    background: white; border: 1px solid #E7EAF0; border-radius: 20px;
    padding: 22px; min-height: 155px; box-shadow: 0 8px 30px rgba(15,23,42,0.055);
}
.kpi-top { display: flex; justify-content: space-between; align-items: center; }
.kpi-label {
    color: #6B7280 !important; font-size: 11px; font-weight: 800;
    letter-spacing: 1px; text-transform: uppercase;
}
.kpi-icon {
    width: 34px; height: 34px; border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 14px;
    font-weight: 800; color: white !important;
}
.kpi-value {
    color: #111827 !important; font-size: 29px; font-weight: 800;
    margin-top: 18px; letter-spacing: -1px;
}
.kpi-description { color: #9CA3AF !important; font-size: 12px; margin-top: 7px; }

/* SECTIONS */
.section-title {
    color: #111827 !important; font-size: 18px; font-weight: 800;
    margin-top: 24px; margin-bottom: 2px;
}
.section-subtitle { color: #94A3B8 !important; font-size: 12px; margin-bottom: 12px; }

/* INSIGHTS */
.insight-card {
    background: white; border: 1px solid #E7EAF0; border-radius: 18px;
    padding: 20px; height: 100%; box-shadow: 0 7px 25px rgba(15,23,42,0.045);
}
.insight-icon { font-size: 23px; margin-bottom: 10px; }
.insight-title { color: #111827 !important; font-size: 14px; font-weight: 800; margin-bottom: 7px; }
.insight-text { color: #64748B !important; font-size: 12px; line-height: 1.6; }

/* DECISION */
.decision-card {
    background: linear-gradient(135deg, #111827 0%, #25204D 55%, #4338CA 100%);
    border-radius: 22px; padding: 28px; margin: 18px 0;
    box-shadow: 0 15px 45px rgba(67,56,202,0.2);
}
.decision-label {
    color: #C4B5FD !important; font-size: 11px; font-weight: 800;
    letter-spacing: 1.5px; text-transform: uppercase;
}
.decision-title { color: white !important; font-size: 25px; font-weight: 800; margin-top: 7px; }
.decision-text { color: #D1D5DB !important; font-size: 13px; line-height: 1.7; margin-top: 10px; }

/* FOOTER */
.footer {
    text-align: center; color: #94A3B8 !important; font-size: 11px;
    margin-top: 40px; padding-top: 20px; border-top: 1px solid #E5E7EB;
}

@media (max-width: 768px) {
    .block-container { padding: 1rem; }
    .main-title { font-size: 30px; }
    .kpi-card { min-height: 135px; padding: 18px; margin-bottom: 12px; }
    .kpi-value { font-size: 25px; }
    .insight-card { margin-bottom: 12px; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

_PLOTLY_HAS_WIDTH = "width" in inspect.signature(st.plotly_chart).parameters


def html(markup: str) -> None:
    """Render HTML safely.

    Markdown turns lines indented by 4+ spaces (or HTML broken up by blank
    lines) into code blocks, so strip indentation and blank lines first.
    """
    cleaned = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def show_chart(fig: go.Figure) -> None:
    """Plotly chart that works on old and new Streamlit versions."""
    if _PLOTLY_HAS_WIDTH:
        st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(fig, use_container_width=True)


def show_table(data: pd.DataFrame) -> None:
    """Dataframe that works on old and new Streamlit versions."""
    try:
        st.dataframe(data, width="stretch", hide_index=True)
    except Exception:
        st.dataframe(data, use_container_width=True, hide_index=True)


def brl(value: float) -> str:
    return f"R$ {value:,.0f}"


def section(title: str, subtitle: str = "") -> None:
    html(f'<div class="section-title">{title}</div>')
    if subtitle:
        html(f'<div class="section-subtitle">{subtitle}</div>')


def kpi_card(label: str, value: str, description: str, icon: str, gradient: str) -> None:
    html(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">{label}</div>
                <div class="kpi-icon" style="background:{gradient};">{icon}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-description">{description}</div>
        </div>
        """
    )


def insight_card(icon: str, title: str, text: str = "", value: str = "", description: str = "") -> None:
    value_html = f'<div class="kpi-value">{value}</div>' if value else ""
    desc_html = f'<div class="kpi-description">{description}</div>' if description else ""
    text_html = f'<div class="insight-text">{text}</div>' if text else ""
    html(
        f"""
        <div class="insight-card">
            <div class="insight-icon">{icon}</div>
            <div class="insight-title">{title}</div>
            {value_html}
            {desc_html}
            {text_html}
        </div>
        """
    )


def decision_card(label: str, title: str, text: str) -> None:
    html(
        f"""
        <div class="decision-card">
            <div class="decision-label">{label}</div>
            <div class="decision-title">{title}</div>
            <div class="decision-text">{text}</div>
        </div>
        """
    )


def style_fig(fig: go.Figure, height: int, title: str = "") -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=50 if title else 10, b=10),
        font=dict(color=DARK),
    )
    if title:
        fig.update_layout(title=title)
    fig.update_xaxes(gridcolor=GRID)
    fig.update_yaxes(gridcolor=GRID)
    return fig


def hbar(data: pd.DataFrame, x: str, y: str, scale: list, height: int = 420, title: str = "") -> go.Figure:
    fig = px.bar(
        data.sort_values(x),
        x=x,
        y=y,
        orientation="h",
        color=x,
        color_continuous_scale=scale,
    )
    style_fig(fig, height, title)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(title="")
    return fig


def monthly_revenue(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("month", as_index=False)["revenue"].sum().sort_values("month")


def category_revenue(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )


# =========================================================
# LOAD & CLEAN DATA
# =========================================================

raw = load_data()

if raw is None or raw.empty:
    st.error("No data available.")
    st.stop()

missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
if missing:
    st.error(f"Data is missing required columns: {', '.join(missing)}")
    st.stop()

df = raw.copy()  # never mutate a cached dataframe

df["month"] = pd.to_datetime(df["month"], errors="coerce")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
df["customer_state"] = df["customer_state"].fillna("Unknown")
df["category"] = df["category"].fillna("Uncategorized")

HAS_LATE = "is_late" in df.columns
HAS_DAYS = "delivery_days" in df.columns

if HAS_LATE:
    df["is_late"] = pd.to_numeric(df["is_late"], errors="coerce")
if HAS_DAYS:
    df["delivery_days"] = pd.to_numeric(df["delivery_days"], errors="coerce")

df = df.dropna(subset=["month", "revenue"])

if df.empty:
    st.error("No valid rows after cleaning the data.")
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    html(
        """
        <div class="sidebar-brand">
            <div class="brand-logo">OI</div>
            <div class="brand-name">Olist Analytics</div>
            <div class="brand-sub">Revenue Intelligence Platform</div>
        </div>
        """
    )

    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio("Navigation", PAGES, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### Filters")

    min_date = df["month"].min().to_pydatetime()
    max_date = df["month"].max().to_pydatetime()

    if min_date < max_date:
        period = st.slider(
            "Analysis period",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="MMM YYYY",
        )
    else:  # a slider needs min < max
        period = (min_date, max_date)
        st.caption(f"Data covers {min_date:%b %Y} only.")

    states = sorted(df["customer_state"].unique().tolist())
    selected_states = st.multiselect("Customer states", states, default=states)

    categories = sorted(df["category"].unique().tolist())
    selected_categories = st.multiselect("Product categories", categories, default=categories)

    st.markdown("---")
    st.caption("Olist Brazilian E-Commerce Dataset")
    st.caption("Delivered orders • Revenue intelligence")

# =========================================================
# FILTER DATA
# =========================================================

mask = (
    (df["month"] >= pd.Timestamp(period[0]))
    & (df["month"] <= pd.Timestamp(period[1]))
    & (df["customer_state"].isin(selected_states))
    & (df["category"].isin(selected_categories))
)

f = df.loc[mask].copy()

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# =========================================================
# CORE METRICS
# =========================================================

orders_df = f.drop_duplicates("order_id")

total_revenue = float(f["revenue"].sum())
total_orders = int(orders_df["order_id"].nunique())
aov = total_revenue / total_orders if total_orders else 0.0

late_rate = float(orders_df["is_late"].mean() * 100) if HAS_LATE else 0.0
if pd.isna(late_rate):
    late_rate = 0.0

# =========================================================
# HEADER
# =========================================================

html('<div class="eyebrow">OLIST ANALYTICS</div>')

header_left, header_right = st.columns([5, 1])

with header_left:
    html(
        f"""
        <div class="main-title">{page}</div>
        <div class="subtitle">Turn transaction data into commercially useful decisions.</div>
        """
    )

with header_right:
    html(
        """
        <div style="text-align:right;">
            <div class="live-badge"><span class="live-dot"></span>LIVE DATA</div>
        </div>
        """
    )

# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(4)
late_color = RED if late_rate > 10 else ORANGE

with k1:
    kpi_card("Total Revenue", brl(total_revenue), "Delivered order revenue", "R$",
             f"linear-gradient(135deg,{INDIGO},{PURPLE})")
with k2:
    kpi_card("Orders", f"{total_orders:,}", "Unique delivered orders", "↗",
             f"linear-gradient(135deg,{BLUE},{CYAN})")
with k3:
    kpi_card("Average Order Value", brl(aov), "Revenue per order", "R$",
             f"linear-gradient(135deg,{GREEN},#14B8A6)")
with k4:
    kpi_card("Late Delivery Rate", f"{late_rate:.1f}%" if HAS_LATE else "N/A",
             "Orders delivered after estimate", "!",
             f"linear-gradient(135deg,{late_color},#F97316)")

# =========================================================
# PAGES
# =========================================================


def page_overview() -> None:
    section("Revenue performance", "Monthly commercial performance across the selected period")

    monthly = monthly_revenue(f)

    fig = go.Figure(
        go.Scatter(
            x=monthly["month"],
            y=monthly["revenue"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color=INDIGO, width=3),
            marker=dict(size=7, color=PURPLE),
            fill="tozeroy",
            fillcolor="rgba(91,92,226,0.10)",
        )
    )
    style_fig(fig, 380)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title="", showgrid=False)
    fig.update_yaxes(title="Revenue", tickprefix="R$ ")
    show_chart(fig)

    cats = category_revenue(f)
    c1, c2 = st.columns(2)

    with c1:
        section("Revenue by category")
        fig_cat = hbar(cats.head(8), "revenue", "category", SCALE_INDIGO, height=390)
        show_chart(fig_cat)

    with c2:
        section("Revenue mix")
        fig_pie = px.pie(
            cats.head(6),
            names="category",
            values="revenue",
            hole=0.62,
            color_discrete_sequence=CHART_COLORS,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent")
        style_fig(fig_pie, 390)
        fig_pie.update_layout(legend=dict(orientation="h", y=-0.05))
        show_chart(fig_pie)


def page_revenue_intelligence() -> None:
    monthly = monthly_revenue(f)
    peak = monthly.loc[monthly["revenue"].idxmax()]

    latest_growth = 0.0
    if len(monthly) >= 2:
        previous = monthly.iloc[-2]["revenue"]
        latest = monthly.iloc[-1]["revenue"]
        if previous != 0:
            latest_growth = (latest - previous) / previous * 100

    a, b, c = st.columns(3)
    with a:
        insight_card("🚀", "Peak Revenue Month", value=brl(peak["revenue"]),
                     description=f"{peak['month']:%b %Y}")
    with b:
        insight_card("📈", "Latest Monthly Movement", value=f"{latest_growth:+.1f}%",
                     description="Compared with previous month")
    with c:
        insight_card("💰", "Revenue per Order", value=brl(aov), description="Average basket value")

    section("Revenue trend")
    fig = px.area(monthly, x="month", y="revenue", markers=True)
    fig.update_traces(line_color=INDIGO, fillcolor="rgba(91,92,226,0.13)")
    style_fig(fig, 420)
    fig.update_xaxes(title="", showgrid=False)
    fig.update_yaxes(title="Revenue", tickprefix="R$ ")
    show_chart(fig)

    cats = category_revenue(f)
    top5_share = cats.head(5)["revenue"].sum() / total_revenue * 100 if total_revenue > 0 else 0.0

    decision_card(
        "Revenue concentration",
        f"Top 5 categories generate {top5_share:.1f}% of selected revenue",
        "Use this concentration signal to prioritize merchandising, inventory "
        "planning, promotional activity and category-level performance reviews.",
    )

    section("Category revenue ranking")
    show_chart(hbar(cats.head(10), "revenue", "category", SCALE_BLUE, height=450))


def page_sales_categories() -> None:
    category = (
        f.groupby("category")
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
        .reset_index()
    )
    category["aov"] = category["revenue"] / category["orders"]
    category = category.sort_values("revenue", ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig = hbar(category.head(10), "revenue", "category", SCALE_AMBER,
                   height=450, title="Top categories by revenue")
        show_chart(fig)

    with c2:
        fig = px.scatter(
            category,
            x="orders",
            y="aov",
            size="revenue",
            color="revenue",
            hover_name="category",
            color_continuous_scale=SCALE_INDIGO,
        )
        style_fig(fig, 450, "Order volume vs average order value")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(title="Orders")
        fig.update_yaxes(title="Average order value", tickprefix="R$ ")
        show_chart(fig)

    section("Category performance table")

    table = category.rename(
        columns={"category": "Category", "revenue": "Revenue", "orders": "Orders", "aov": "AOV"}
    )
    table["Revenue"] = table["Revenue"].map(brl)
    table["AOV"] = table["AOV"].map(brl)
    table["Orders"] = table["Orders"].map(lambda x: f"{x:,}")
    show_table(table[["Category", "Revenue", "Orders", "AOV"]])


def page_delivery() -> None:
    section("Delivery health", "Identify geographic delivery pressure and operational risk")

    if not (HAS_LATE and HAS_DAYS):
        st.info("Delivery columns (is_late, delivery_days) are not available in this dataset.")
        return

    delivery = (
        orders_df.groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            late_rate=("is_late", "mean"),
            avg_delivery_days=("delivery_days", "mean"),
        )
        .reset_index()
    )
    delivery = delivery[delivery["orders"] >= MIN_STATE_ORDERS].copy()
    delivery["late_rate"] *= 100
    delivery = delivery.sort_values("late_rate", ascending=False)

    if delivery.empty:
        st.info(f"No state has at least {MIN_STATE_ORDERS} orders under the current filters.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            fig = hbar(delivery.head(10), "late_rate", "customer_state", SCALE_RED,
                       height=440, title="Highest late-delivery rates")
            fig.update_xaxes(title="Late delivery rate (%)")
            show_chart(fig)

        with c2:
            fig = px.scatter(
                delivery,
                x="avg_delivery_days",
                y="late_rate",
                size="orders",
                color="late_rate",
                hover_name="customer_state",
                color_continuous_scale=["#DCFCE7", "#F59E0B", "#EF4444"],
            )
            style_fig(fig, 440, "Delivery time vs late rate")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(title="Average delivery days")
            fig.update_yaxes(title="Late delivery rate (%)")
            show_chart(fig)

    section("Delivery-time distribution")
    days = orders_df.dropna(subset=["delivery_days"])
    if days.empty:
        st.info("No delivery-time data for the selected filters.")
    else:
        fig = px.histogram(days, x="delivery_days", nbins=35, color_discrete_sequence=[CYAN])
        style_fig(fig, 350)
        fig.update_xaxes(title="Delivery days")
        fig.update_yaxes(title="Orders")
        show_chart(fig)

    if not delivery.empty:
        table = delivery.rename(
            columns={
                "customer_state": "State",
                "orders": "Orders",
                "late_rate": "Late rate",
                "avg_delivery_days": "Avg delivery days",
            }
        )
        table["Orders"] = table["Orders"].map(lambda x: f"{x:,}")
        table["Late rate"] = table["Late rate"].map(lambda x: f"{x:.1f}%")
        table["Avg delivery days"] = table["Avg delivery days"].map(lambda x: f"{x:.1f}")
        show_table(table[["State", "Orders", "Late rate", "Avg delivery days"]])


def page_business_insights() -> None:
    category = f.groupby("category")["revenue"].sum().sort_values(ascending=False)
    state = f.groupby("customer_state")["revenue"].sum().sort_values(ascending=False)
    monthly = f.groupby("month")["revenue"].sum()

    peak_month = monthly.idxmax()

    decision_card(
        "Executive decision center",
        "What should the business pay attention to?",
        "The dashboard connects revenue concentration, customer geography and "
        "delivery performance to help prioritize commercial and operational actions.",
    )

    section("Key findings")
    i1, i2, i3 = st.columns(3)

    with i1:
        insight_card(
            "🏆", "Category leader",
            text=f"<b>{category.index[0]}</b> is the highest-revenue category in the "
                 f"selected dataset.<br><br>Revenue: <b>{brl(category.iloc[0])}</b>",
        )
    with i2:
        insight_card(
            "🌎", "Geographic leader",
            text=f"<b>{state.index[0]}</b> contributes the largest revenue amount "
                 f"among customer states.<br><br>Revenue: <b>{brl(state.iloc[0])}</b>",
        )
    with i3:
        insight_card(
            "📅", "Peak period",
            text=f"The strongest monthly revenue occurred in <b>{peak_month:%B %Y}</b>."
                 f"<br><br>Revenue: <b>{brl(monthly.max())}</b>",
        )

    section("Recommended actions")
    actions = [
        ("🎯", "Protect revenue leaders",
         "Prioritize high-performing categories with inventory availability, "
         "merchandising and targeted promotional planning."),
        ("🚚", "Investigate delivery risk",
         "Focus operational reviews on states with elevated late-delivery rates "
         "and longer delivery times."),
        ("📊", "Monitor revenue concentration",
         "Track category and geographic concentration to identify dependency risk "
         "and potential opportunities for diversification."),
    ]
    for col, (icon, title, text) in zip(st.columns(3), actions):
        with col:
            insight_card(icon, title, text=text)


# =========================================================
# ROUTER
# =========================================================

ROUTES = {
    "Overview": page_overview,
    "Revenue Intelligence": page_revenue_intelligence,
    "Sales & Categories": page_sales_categories,
    "Delivery Operations": page_delivery,
    "Business Insights": page_business_insights,
}

ROUTES[page]()

# =========================================================
# FOOTER
# =========================================================

html(
    """
    <div class="footer">
        Olist Analytics • Revenue Intelligence Dashboard<br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """
)
