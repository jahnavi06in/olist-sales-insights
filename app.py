import inspect

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

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
GREY = "#A5B4CF"

CHART_COLORS = [PURPLE, BLUE, GREEN, ORANGE, PINK, CYAN, INDIGO, RED, "#14B8A6", "#8B5CF6"]

SCALE_INDIGO = ["#DDD6FE", "#8B5CF6", "#4F46E5"]
SCALE_BLUE = ["#DBEAFE", "#3B82F6", "#1D4ED8"]
SCALE_AMBER = ["#FDE68A", "#F59E0B", "#EA580C"]
SCALE_RED = ["#FEE2E2", "#F87171", "#DC2626"]

REQUIRED_COLUMNS = ["order_id", "month", "revenue", "customer_state", "category"]
MIN_STATE_ORDERS = 100
LATE_ALERT = 10  # % late rate that triggers the recommendation

PAGES = ["Overview", "Revenue Intelligence", "Sales & Categories", "Delivery Operations", "Business Insights"]
PAGE_ICONS = {
    "Overview": "🏠",
    "Revenue Intelligence": "📈",
    "Sales & Categories": "🏷️",
    "Delivery Operations": "🚚",
    "Business Insights": "💡",
}

# Approximate state centroids (lat, lon) for the bubble map
STATE_COORDS = {
    "AC": (-9.0, -70.8), "AL": (-9.6, -36.8), "AP": (1.4, -51.8), "AM": (-3.4, -65.0),
    "BA": (-12.9, -41.7), "CE": (-5.2, -39.3), "DF": (-15.8, -47.9), "ES": (-19.6, -40.6),
    "GO": (-15.9, -49.8), "MA": (-5.0, -45.3), "MT": (-12.9, -55.9), "MS": (-20.5, -54.5),
    "MG": (-18.5, -44.6), "PA": (-3.8, -52.5), "PB": (-7.1, -36.8), "PR": (-24.6, -51.6),
    "PE": (-8.4, -37.9), "PI": (-7.7, -42.7), "RJ": (-22.2, -42.7), "RN": (-5.8, -36.6),
    "RS": (-29.7, -53.7), "RO": (-10.9, -62.8), "RR": (2.1, -61.4), "SC": (-27.3, -50.5),
    "SP": (-22.2, -48.8), "SE": (-10.6, -37.4), "TO": (-10.2, -48.3),
}

# =========================================================
# GLOBAL CSS
# =========================================================

CSS = """
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(91,92,226,0.08), transparent 25%),
        radial-gradient(circle at 90% 10%, rgba(124,58,237,0.06), transparent 25%),
        #F5F6FB;
}
.block-container { max-width: 1600px; padding-top: 1.4rem; padding-bottom: 3rem; }
h1, h2, h3, h4 { color: #111827 !important; }

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1026 0%, #111936 100%);
    border-right: 1px solid #1F2A4A;
}
section[data-testid="stSidebar"] * { color: #E5E7EB; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #F9FAFB !important; font-size: 16px !important; }
section[data-testid="stSidebar"] hr { border-color: #1F2A4A; }

.sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 6px 2px 14px 2px; }
.brand-logo {
    width: 44px; height: 44px; border-radius: 50%; flex: none;
    background: linear-gradient(135deg, #5B5CE2, #8B5CF6);
    display: flex; align-items: center; justify-content: center;
    color: white !important; font-size: 20px; font-weight: 800;
    box-shadow: 0 6px 20px rgba(91,92,226,0.45);
}
.brand-name { font-size: 18px; font-weight: 800; color: white !important; line-height: 1.1; }
.brand-sub { font-size: 11px; color: #9CA3AF !important; margin-top: 3px; }

/* nav radio -> menu buttons */
section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 6px; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    padding: 11px 14px; border-radius: 12px; width: 100%; cursor: pointer; transition: all .15s;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: rgba(255,255,255,0.06); }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(135deg, #5B5CE2, #7C3AED);
    box-shadow: 0 8px 22px rgba(91,92,226,0.35);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) * {
    color: white !important; font-weight: 700;
}

/* sidebar inputs */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #1A2244 !important; border: 1px solid #2B3558 !important; border-radius: 10px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] { background: #4F46E5 !important; }
section[data-testid="stSidebar"] [data-baseweb="tag"] * { color: white !important; }
section[data-testid="stSidebar"] div[role="slider"] { background: #7C3AED !important; }
.side-note { font-size: 11px; color: #9CA3AF !important; line-height: 1.5; margin-top: 4px; }
.side-note b { color: #E5E7EB !important; font-size: 12px; }

/* ---------- HEADER ---------- */
.eyebrow {
    color: #5B5CE2 !important; font-size: 12px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;
}
.main-title { font-size: 40px; line-height: 1.1; font-weight: 800; color: #111827 !important; letter-spacing: -1.5px; }
.subtitle { color: #6B7280 !important; font-size: 15px; margin-top: 8px; margin-bottom: 18px; }
.header-right { display: flex; justify-content: flex-end; align-items: center; gap: 14px; flex-wrap: wrap; }
.live-badge {
    display: inline-flex; align-items: center; gap: 7px; padding: 8px 14px;
    border-radius: 999px; background: #ECFDF5; border: 1px solid #A7F3D0;
    color: #047857 !important; font-size: 12px; font-weight: 800; white-space: nowrap;
}
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #10B981; }
.profile { display: flex; align-items: center; gap: 9px; }
.avatar {
    width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #5B5CE2, #8B5CF6);
    color: white !important; font-weight: 800; font-size: 13px; display: flex; align-items: center; justify-content: center;
}
.profile-name { font-size: 13px; font-weight: 800; color: #111827 !important; line-height: 1.1; }
.profile-role { font-size: 11px; color: #9CA3AF !important; }

/* ---------- KPI CARDS ---------- */
.kpi {
    position: relative; overflow: hidden; border-radius: 20px; padding: 20px 22px;
    min-height: 158px; color: white; box-shadow: 0 14px 34px rgba(15,23,42,0.16);
}
.kpi-top { display: flex; align-items: center; gap: 12px; }
.kpi-icon {
    width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.22);
    display: flex; align-items: center; justify-content: center; font-size: 18px; flex: none;
}
.kpi-label { color: white !important; font-size: 15px; font-weight: 600; }
.kpi-value { color: white !important; font-size: 33px; font-weight: 800; margin-top: 14px; letter-spacing: -1px; }
.kpi .delta { color: rgba(255,255,255,0.92) !important; font-size: 12px; font-weight: 600; }
.spark { position: absolute; right: 16px; bottom: 16px; opacity: 0.9; }

/* ---------- CARDS ---------- */
[class*="st-key-card-"] {
    background: white; border: 1px solid #E7EAF0; border-radius: 20px;
    padding: 18px 20px 12px 20px; box-shadow: 0 8px 30px rgba(15,23,42,0.05);
}
.card-head { display: flex; align-items: center; gap: 11px; margin-bottom: 8px; }
.card-ico {
    width: 34px; height: 34px; border-radius: 10px; background: #EEF2FF;
    display: flex; align-items: center; justify-content: center; font-size: 16px; flex: none;
}
.card-title { font-size: 16px; font-weight: 800; color: #111827 !important; line-height: 1.2; }
.card-sub { font-size: 12px; color: #94A3B8 !important; }

/* legend */
.legend { display: flex; flex-direction: column; gap: 9px; padding-top: 6px; }
.leg-row { display: flex; align-items: center; gap: 9px; font-size: 12.5px; }
.leg-dot { width: 11px; height: 11px; border-radius: 50%; flex: none; }
.leg-name { color: #374151 !important; flex: 1; }
.leg-pct { color: #111827 !important; font-weight: 700; }

/* top table */
.top-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.top-table th {
    text-align: left; color: #9CA3AF !important; font-weight: 600; font-size: 11px;
    padding: 6px 6px; border-bottom: 1px solid #EEF0F5;
}
.top-table td { padding: 8px 6px; color: #374151 !important; border-bottom: 1px solid #F5F6FA; }
.top-table .rk { color: #9CA3AF !important; width: 22px; }
.top-table .cat { font-weight: 600; color: #111827 !important; }
.bar-wrap { background: #F1F2F8; border-radius: 6px; height: 8px; min-width: 50px; }
.bar { height: 8px; border-radius: 6px; }

/* mini stats */
.mini-row { display: flex; gap: 12px; margin-top: 6px; flex-wrap: wrap; }
.mini {
    flex: 1; min-width: 150px; display: flex; gap: 12px; align-items: center;
    border: 1px solid #E7EAF0; border-radius: 14px; padding: 12px 14px;
}
.mini-ico { font-size: 24px; }
.mini-label { font-size: 11px; color: #6B7280 !important; }
.mini-val { font-size: 22px; font-weight: 800; color: #111827 !important; line-height: 1.15; }
.mini-delta { font-size: 11px; font-weight: 700; }
.good { color: #059669 !important; }
.bad { color: #DC2626 !important; }

/* insight rows */
.insight-row {
    display: flex; gap: 12px; align-items: center; background: #F8F9FD;
    border-radius: 14px; padding: 12px 14px; margin-bottom: 10px;
}
.insight-tile {
    width: 38px; height: 38px; border-radius: 11px; flex: none; color: white !important;
    display: flex; align-items: center; justify-content: center; font-size: 17px;
}
.insight-row-title { font-size: 13px; font-weight: 800; color: #111827 !important; }
.insight-row-text { font-size: 12px; color: #6B7280 !important; line-height: 1.5; }
.action-card {
    background: linear-gradient(135deg, #111827 0%, #25204D 55%, #4338CA 100%);
    border-radius: 14px; padding: 16px 18px; margin-top: 4px;
}
.action-label { color: #C4B5FD !important; font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; }
.action-text { color: white !important; font-size: 13px; line-height: 1.5; margin-top: 4px; font-weight: 600; }

/* section / insight cards for the other pages */
.section-title { color: #111827 !important; font-size: 18px; font-weight: 800; margin-top: 22px; margin-bottom: 2px; }
.section-subtitle { color: #94A3B8 !important; font-size: 12px; margin-bottom: 12px; }
.insight-card {
    background: white; border: 1px solid #E7EAF0; border-radius: 18px; padding: 20px;
    height: 100%; box-shadow: 0 7px 25px rgba(15,23,42,0.045);
}
.insight-icon { font-size: 23px; margin-bottom: 10px; }
.insight-title { color: #111827 !important; font-size: 14px; font-weight: 800; margin-bottom: 7px; }
.insight-text { color: #64748B !important; font-size: 12px; line-height: 1.6; }
.big-value { color: #111827 !important; font-size: 29px; font-weight: 800; letter-spacing: -1px; }
.big-desc { color: #9CA3AF !important; font-size: 12px; margin-top: 4px; }
.decision-card {
    background: linear-gradient(135deg, #111827 0%, #25204D 55%, #4338CA 100%);
    border-radius: 22px; padding: 28px; margin: 18px 0; box-shadow: 0 15px 45px rgba(67,56,202,0.2);
}
.decision-label { color: #C4B5FD !important; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; }
.decision-title { color: white !important; font-size: 25px; font-weight: 800; margin-top: 7px; }
.decision-text { color: #D1D5DB !important; font-size: 13px; line-height: 1.7; margin-top: 10px; }

.footer {
    text-align: center; color: #94A3B8 !important; font-size: 11px;
    margin-top: 40px; padding-top: 20px; border-top: 1px solid #E5E7EB;
}

@media (max-width: 768px) {
    .block-container { padding: 1rem; }
    .main-title { font-size: 30px; }
    .kpi { min-height: 140px; padding: 18px; margin-bottom: 12px; }
    .kpi-value { font-size: 27px; }
    .header-right { justify-content: flex-start; margin-bottom: 8px; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

_PLOTLY_HAS_WIDTH = "width" in inspect.signature(st.plotly_chart).parameters
PLOT_CONFIG = {"displayModeBar": False}


def html(markup: str) -> None:
    """Render HTML safely (Markdown treats indented / blank-line-split HTML as code)."""
    cleaned = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def show_chart(fig: go.Figure) -> None:
    if _PLOTLY_HAS_WIDTH:
        st.plotly_chart(fig, width="stretch", config=PLOT_CONFIG)
    else:
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)


def show_table(data: pd.DataFrame) -> None:
    try:
        st.dataframe(data, width="stretch", hide_index=True)
    except Exception:
        st.dataframe(data, use_container_width=True, hide_index=True)


def brl(value: float) -> str:
    return f"R$ {value:,.0f}"


def card(name: str):
    """White rounded card. Needs Streamlit >= 1.39 for the styling hook; falls back to a bordered box."""
    try:
        return st.container(key=f"card-{name}")
    except TypeError:
        return st.container(border=True)


def card_head(icon: str, title: str, subtitle: str = "") -> None:
    sub = f'<div class="card-sub">{subtitle}</div>' if subtitle else ""
    html(
        f"""
        <div class="card-head">
            <div class="card-ico">{icon}</div>
            <div><div class="card-title">{title}</div>{sub}</div>
        </div>
        """
    )


def section(title: str, subtitle: str = "") -> None:
    html(f'<div class="section-title">{title}</div>')
    if subtitle:
        html(f'<div class="section-subtitle">{subtitle}</div>')


def sparkline(values, width: int = 120, height: int = 44) -> str:
    vals = [float(v) for v in values if pd.notna(v)]
    if len(vals) < 2:
        return ""
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    pts = " ".join(
        f"{i / (len(vals) - 1) * width:.1f},{height - 4 - (v - lo) / span * (height - 8):.1f}"
        for i, v in enumerate(vals)
    )
    return (
        f'<svg class="spark" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
        f'<polyline points="{pts}" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" '
        f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


def change(series: pd.Series, pct: bool = True):
    """Latest value vs previous value (month over month)."""
    s = series.dropna()
    if len(s) < 2:
        return None
    last, prev = s.iloc[-1], s.iloc[-2]
    if pct:
        return None if prev == 0 else (last - prev) / prev * 100
    return last - prev


def delta_html(value, unit: str = "%") -> str:
    if value is None:
        return '<span class="delta">No previous month</span>'
    arrow = "▲" if value >= 0 else "▼"
    return f'<span class="delta">{arrow} {value:+.1f}{unit} vs. previous month</span>'


def kpi_card(label: str, value: str, delta: str, icon: str, gradient: str, spark_values) -> None:
    html(
        f"""
        <div class="kpi" style="background:{gradient};">
            <div class="kpi-top"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div></div>
            <div class="kpi-value">{value}</div>
            {delta}
            {sparkline(spark_values)}
        </div>
        """
    )


def insight_card(icon: str, title: str, text: str = "", value: str = "", description: str = "") -> None:
    value_html = f'<div class="big-value">{value}</div>' if value else ""
    desc_html = f'<div class="big-desc">{description}</div>' if description else ""
    text_html = f'<div class="insight-text">{text}</div>' if text else ""
    html(
        f"""
        <div class="insight-card">
            <div class="insight-icon">{icon}</div>
            <div class="insight-title">{title}</div>
            {value_html}{desc_html}{text_html}
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


def legend(items) -> None:
    rows = "".join(
        f'<div class="leg-row"><span class="leg-dot" style="background:{c}"></span>'
        f'<span class="leg-name">{label}</span><span class="leg-pct">{pct:.1f}%</span></div>'
        for label, pct, c in items
    )
    html(f'<div class="legend">{rows}</div>')


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
        data.sort_values(x), x=x, y=y, orientation="h", color=x, color_continuous_scale=scale
    )
    style_fig(fig, height, title)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(title="")
    return fig


def category_revenue(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )


def monthly_metrics(frame: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    m = pd.DataFrame(
        {
            "revenue": frame.groupby("month")["revenue"].sum(),
            "orders": orders.groupby("month")["order_id"].nunique(),
        }
    ).sort_index()
    m["aov"] = m["revenue"] / m["orders"]
    if HAS_LATE:
        m["late"] = orders.groupby("month")["is_late"].mean() * 100
    if HAS_DAYS:
        m["days"] = orders.groupby("month")["delivery_days"].mean()
    return m


def state_delivery(orders: pd.DataFrame) -> pd.DataFrame:
    d = (
        orders.groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            late_rate=("is_late", "mean"),
            avg_delivery_days=("delivery_days", "mean"),
        )
        .reset_index()
    )
    d = d[d["orders"] >= MIN_STATE_ORDERS].copy()
    d["late_rate"] *= 100
    return d


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
df["category"] = (
    df["category"].fillna("Uncategorized").astype(str).str.replace("_", " ").str.title()
)

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
            <div class="brand-logo">📊</div>
            <div><div class="brand-name">Olist Analytics</div>
            <div class="brand-sub">Revenue Intelligence Platform</div></div>
        </div>
        """
    )

    page = st.radio(
        "Navigation",
        PAGES,
        format_func=lambda p: f"{PAGE_ICONS[p]}   {p}",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🔻 Filters")

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
    else:
        period = (min_date, max_date)
        st.caption(f"Data covers {min_date:%b %Y} only.")

    all_states = sorted(df["customer_state"].unique().tolist())
    selected_states = (
        st.multiselect("Customer states", all_states, placeholder="All states") or all_states
    )

    all_categories = sorted(df["category"].unique().tolist())
    selected_categories = (
        st.multiselect("Product categories", all_categories, placeholder="All categories")
        or all_categories
    )

    st.markdown("---")
    html(
        """
        <div class="side-note"><b>Data source</b><br>Brazilian E-Commerce<br>Public Dataset by Olist</div>
        """
    )
    html(
        """
        <div class="side-note" style="margin-top:14px"><b>Analysis</b><br>Delivered orders • Revenue excludes freight</div>
        """
    )

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
monthly = monthly_metrics(f, orders_df)

total_revenue = float(f["revenue"].sum())
total_orders = int(orders_df["order_id"].nunique())
aov = total_revenue / total_orders if total_orders else 0.0

late_rate = float(orders_df["is_late"].mean() * 100) if HAS_LATE else 0.0
if pd.isna(late_rate):
    late_rate = 0.0

avg_days = float(orders_df["delivery_days"].mean()) if HAS_DAYS else 0.0
if pd.isna(avg_days):
    avg_days = 0.0

# =========================================================
# HEADER
# =========================================================

html('<div class="eyebrow">OLIST ANALYTICS</div>')

header_left, header_right = st.columns([3, 2])

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
        <div class="header-right">
            <div class="live-badge"><span class="live-dot"></span>LIVE DATASET</div>
            <div class="profile">
                <div class="avatar">JN</div>
                <div><div class="profile-name">Jahnavi</div><div class="profile-role">Analyst</div></div>
            </div>
        </div>
        """
    )

# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Total Revenue", brl(total_revenue), delta_html(change(monthly["revenue"])), "💰",
             "linear-gradient(135deg,#7C5CFA,#4F46E5)", monthly["revenue"])
with k2:
    kpi_card("Orders", f"{total_orders:,}", delta_html(change(monthly["orders"])), "📦",
             "linear-gradient(135deg,#3B82F6,#0EA5E9)", monthly["orders"])
with k3:
    kpi_card("Average Order Value", brl(aov), delta_html(change(monthly["aov"])), "🛒",
             "linear-gradient(135deg,#10B981,#0D9488)", monthly["aov"])
with k4:
    kpi_card(
        "Late Delivery Rate",
        f"{late_rate:.1f}%" if HAS_LATE else "N/A",
        delta_html(change(monthly["late"], pct=False), " pp") if HAS_LATE else "",
        "⏱️",
        "linear-gradient(135deg,#F43F5E,#F97316)",
        monthly["late"] if HAS_LATE else [],
    )

st.write("")

# =========================================================
# OVERVIEW COMPONENTS
# =========================================================


def trend_chart() -> go.Figure:
    fig = go.Figure(
        go.Scatter(
            x=monthly.index,
            y=monthly["revenue"],
            mode="lines+markers",
            line=dict(color=PURPLE, width=3),
            marker=dict(size=6, color=PURPLE),
            fill="tozeroy",
            fillcolor="rgba(124,58,237,0.10)",
            hovertemplate="%{x|%b %Y}<br>R$ %{y:,.0f}<extra></extra>",
        )
    )
    last_x, last_y = monthly.index[-1], monthly["revenue"].iloc[-1]
    fig.add_annotation(
        x=last_x, y=last_y, text=f"{last_x:%b %Y}<br><b>{brl(last_y)}</b>",
        showarrow=True, arrowhead=0, ax=-40, ay=-45,
        bgcolor="white", bordercolor="#E5E7EB", borderwidth=1, font=dict(size=11),
    )
    style_fig(fig, 300)
    fig.update_xaxes(title="", showgrid=False)
    fig.update_yaxes(title="", tickprefix="R$ ", tickformat="~s")
    return fig


def donut_block(cats: pd.DataFrame) -> None:
    top = cats.head(5)
    others = total_revenue - float(top["revenue"].sum())
    labels = top["category"].tolist()
    values = top["revenue"].tolist()
    colors = CHART_COLORS[: len(labels)]
    if others > 0:
        labels.append("Others")
        values.append(others)
        colors.append(GREY)

    fig = go.Figure(
        go.Pie(
            labels=labels, values=values, hole=0.7, sort=False,
            marker=dict(colors=colors, line=dict(color="white", width=2)),
            textinfo="none", hovertemplate="%{label}<br>R$ %{value:,.0f} (%{percent})<extra></extra>",
        )
    )
    style_fig(fig, 270)
    fig.update_layout(
        showlegend=False,
        annotations=[dict(text=f"<b>R$ {total_revenue / 1e6:.2f}M</b><br>Total Revenue",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=13))],
    )
    left, right = st.columns([1.1, 1])
    with left:
        show_chart(fig)
    with right:
        total = sum(values) or 1
        legend([(l, v / total * 100, c) for l, v, c in zip(labels, values, colors)])


def geo_chart(frame: pd.DataFrame):
    states = frame.groupby("customer_state", as_index=False)["revenue"].sum()
    states["lat"] = states["customer_state"].map(lambda s: STATE_COORDS.get(s, (None, None))[0])
    states["lon"] = states["customer_state"].map(lambda s: STATE_COORDS.get(s, (None, None))[1])
    states = states.dropna(subset=["lat", "lon"])
    if states.empty:
        return None
    fig = px.scatter_geo(
        states, lat="lat", lon="lon", size="revenue", color="revenue",
        hover_name="customer_state", hover_data={"lat": False, "lon": False, "revenue": ":,.0f"},
        color_continuous_scale=SCALE_INDIGO, size_max=32,
    )
    fig.update_geos(
        scope="south america", lonaxis_range=[-75, -33], lataxis_range=[-35, 6],
        showcountries=True, countrycolor="#CBD5E1", landcolor="#F1F0FF",
        showocean=False, showframe=False, bgcolor="white",
    )
    style_fig(fig, 270)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
    return fig


def top_categories_table(frame: pd.DataFrame) -> None:
    g = (
        frame.groupby("category")
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
        .reset_index()
    )
    g["aov"] = g["revenue"] / g["orders"]
    g = g.sort_values("revenue", ascending=False).head(10)
    max_orders = g["orders"].max() or 1

    rows = ""
    for i, r in enumerate(g.itertuples(), 1):
        color = CHART_COLORS[(i - 1) % len(CHART_COLORS)]
        width = r.orders / max_orders * 100
        rows += (
            f'<tr><td class="rk">{i}</td><td class="cat">{r.category}</td>'
            f"<td>{brl(r.revenue)}</td>"
            f'<td><div class="bar-wrap"><div class="bar" style="width:{width:.0f}%;background:{color}"></div></div></td>'
            f"<td>{r.orders:,}</td><td>{brl(r.aov)}</td></tr>"
        )
    html(
        f"""
        <table class="top-table">
        <thead><tr><th>#</th><th>Category</th><th>Revenue</th><th colspan="2">Orders</th><th>AOV</th></tr></thead>
        <tbody>{rows}</tbody>
        </table>
        """
    )


def mini_stat(icon: str, label: str, value: str, delta_text: str, good: bool) -> str:
    cls = "good" if good else "bad"
    return (
        f'<div class="mini"><div class="mini-ico">{icon}</div><div>'
        f'<div class="mini-label">{label}</div><div class="mini-val">{value}</div>'
        f'<div class="mini-delta {cls}">{delta_text}</div></div></div>'
    )


def delivery_block() -> None:
    d = state_delivery(orders_df).sort_values("orders", ascending=False).head(10)
    if d.empty:
        st.info(f"No state has at least {MIN_STATE_ORDERS} orders under the current filters.")
    else:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(x=d["customer_state"], y=d["avg_delivery_days"], name="Avg Delivery Days",
                    marker_color=INDIGO, secondary_y=False)
        fig.add_trace(
            go.Scatter(x=d["customer_state"], y=d["late_rate"], name="Late Rate", mode="lines+markers",
                       line=dict(color=ORANGE, width=2.5), marker=dict(size=6)),
            secondary_y=True,
        )
        style_fig(fig, 260)
        fig.update_layout(bargap=0.45, legend=dict(orientation="h", y=1.15, x=1, xanchor="right"))
        fig.update_yaxes(title="", secondary_y=False)
        fig.update_yaxes(title="", ticksuffix="%", showgrid=False, secondary_y=True)
        show_chart(fig)

    days_change = change(monthly["days"], pct=False) if HAS_DAYS else None
    late_change = change(monthly["late"], pct=False) if HAS_LATE else None
    days_txt = "No previous month" if days_change is None else f"{'▲' if days_change >= 0 else '▼'} {days_change:+.1f} days vs. previous month"
    late_txt = "No previous month" if late_change is None else f"{'▲' if late_change >= 0 else '▼'} {late_change:+.1f} pp vs. previous month"
    html(
        '<div class="mini-row">'
        + mini_stat("🚚", "Avg Delivery Days", f"{avg_days:.1f}", days_txt, days_change is None or days_change <= 0)
        + mini_stat("⚠️", "Late Delivery Rate", f"{late_rate:.1f}%", late_txt, late_change is None or late_change <= 0)
        + "</div>"
    )


def insights_block(cats: pd.DataFrame) -> None:
    growth = change(monthly["revenue"])
    if growth is None:
        momentum = "Not enough months selected to measure momentum."
    else:
        verb = "grew" if growth >= 0 else "declined"
        momentum = f"Revenue {verb} {abs(growth):.1f}% in {monthly.index[-1]:%b %Y} versus the previous month."

    states = f.groupby("customer_state")["revenue"].sum().sort_values(ascending=False)
    top_state = states.index[0]
    state_share = states.iloc[0] / total_revenue * 100 if total_revenue else 0
    top_cat = cats.iloc[0]
    cat_share = top_cat["revenue"] / total_revenue * 100 if total_revenue else 0

    if HAS_LATE and HAS_DAYS:
        risky = state_delivery(orders_df)
        risky = risky[risky["late_rate"] > LATE_ALERT].sort_values("late_rate", ascending=False)
        if risky.empty:
            action = f"No state exceeds a {LATE_ALERT}% late rate. Keep monitoring delivery performance."
        else:
            action = (f"Focus on improving delivery performance in {len(risky)} state(s) with a "
                      f">{LATE_ALERT}% late rate. Worst: {risky.iloc[0]['customer_state']} "
                      f"({risky.iloc[0]['late_rate']:.1f}%).")
    else:
        action = "Add delivery data to unlock delivery recommendations."

    items = [
        ("📈", PURPLE, "Revenue Momentum", momentum),
        ("📍", GREEN, "Top Performing State", f"{top_state} contributes {state_share:.1f}% of total revenue."),
        ("🏷️", ORANGE, "Key Category", f"{top_cat['category']} is the top revenue generator with {brl(top_cat['revenue'])} ({cat_share:.1f}% share)."),
    ]
    for icon, color, title, text in items:
        html(
            f"""
            <div class="insight-row">
                <div class="insight-tile" style="background:{color}">{icon}</div>
                <div><div class="insight-row-title">{title}</div><div class="insight-row-text">{text}</div></div>
            </div>
            """
        )
    html(
        f"""
        <div class="action-card">
            <div class="action-label">Recommended Action</div>
            <div class="action-text">{action}</div>
        </div>
        """
    )


# =========================================================
# PAGES
# =========================================================


def page_overview() -> None:
    cats = category_revenue(f)

    c1, c2, c3 = st.columns([1.35, 1.2, 1.15])
    with c1:
        with card("trend"):
            card_head("📈", "Revenue Trend", "Monthly revenue performance")
            show_chart(trend_chart())
    with c2:
        with card("category"):
            card_head("🍩", "Revenue by Category", "Top product categories by revenue")
            donut_block(cats)
    with c3:
        with card("geo"):
            card_head("🗺️", "Geographic Performance", "Revenue by customer state")
            geo = geo_chart(f)
            if geo is not None:
                show_chart(geo)
            top_states = f.groupby("customer_state")["revenue"].sum().sort_values(ascending=False)
            share = top_states / (top_states.sum() or 1) * 100
            items = [(s, share[s], CHART_COLORS[i]) for i, s in enumerate(share.index[:5])]
            if len(share) > 5:
                items.append(("Others", share.iloc[5:].sum(), GREY))
            legend(items)

    st.write("")
    d1, d2, d3 = st.columns([1.3, 1.1, 1])
    with d1:
        with card("top10"):
            card_head("🏆", "Top 10 Categories", "Revenue and order volume")
            top_categories_table(f)
    with d2:
        with card("delivery"):
            card_head("🚚", "Delivery Performance", "Average delivery time and late rate by state")
            if HAS_LATE and HAS_DAYS:
                delivery_block()
            else:
                st.info("Delivery columns are not available in this dataset.")
    with d3:
        with card("insights"):
            card_head("💡", "Key Insights")
            insights_block(cats)


def page_revenue_intelligence() -> None:
    peak_month = monthly["revenue"].idxmax()
    growth = change(monthly["revenue"])

    a, b, c = st.columns(3)
    with a:
        insight_card("🚀", "Peak Revenue Month", value=brl(monthly["revenue"].max()),
                     description=f"{peak_month:%b %Y}")
    with b:
        insight_card("📈", "Latest Monthly Movement",
                     value="N/A" if growth is None else f"{growth:+.1f}%",
                     description="Compared with previous month")
    with c:
        insight_card("💰", "Revenue per Order", value=brl(aov), description="Average basket value")

    with card("rev-trend"):
        card_head("📈", "Revenue trend", "Monthly revenue over the selected period")
        fig = px.area(monthly.reset_index(), x="month", y="revenue", markers=True)
        fig.update_traces(line_color=PURPLE, fillcolor="rgba(124,58,237,0.12)")
        style_fig(fig, 380)
        fig.update_xaxes(title="", showgrid=False)
        fig.update_yaxes(title="", tickprefix="R$ ", tickformat="~s")
        show_chart(fig)

    cats = category_revenue(f)
    top5_share = cats.head(5)["revenue"].sum() / total_revenue * 100 if total_revenue > 0 else 0.0
    decision_card(
        "Revenue concentration",
        f"Top 5 categories generate {top5_share:.1f}% of selected revenue",
        "Use this concentration signal to prioritize merchandising, inventory planning, "
        "promotional activity and category-level performance reviews.",
    )

    with card("rev-rank"):
        card_head("🏷️", "Category revenue ranking", "Top 10 categories")
        show_chart(hbar(cats.head(10), "revenue", "category", SCALE_BLUE, height=430))


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
        with card("sales-bar"):
            card_head("🏷️", "Top categories by revenue")
            show_chart(hbar(category.head(10), "revenue", "category", SCALE_AMBER, height=430))
    with c2:
        with card("sales-scatter"):
            card_head("🔵", "Order volume vs average order value")
            fig = px.scatter(
                category, x="orders", y="aov", size="revenue", color="revenue",
                hover_name="category", color_continuous_scale=SCALE_INDIGO,
            )
            style_fig(fig, 430)
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
    if not (HAS_LATE and HAS_DAYS):
        st.info("Delivery columns (is_late, delivery_days) are not available in this dataset.")
        return

    delivery = state_delivery(orders_df).sort_values("late_rate", ascending=False)

    if delivery.empty:
        st.info(f"No state has at least {MIN_STATE_ORDERS} orders under the current filters.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            with card("del-worst"):
                card_head("🚨", "Highest late-delivery rates")
                fig = hbar(delivery.head(10), "late_rate", "customer_state", SCALE_RED, height=400)
                fig.update_xaxes(title="Late delivery rate (%)")
                show_chart(fig)
        with c2:
            with card("del-scatter"):
                card_head("⏱️", "Delivery time vs late rate")
                fig = px.scatter(
                    delivery, x="avg_delivery_days", y="late_rate", size="orders", color="late_rate",
                    hover_name="customer_state", color_continuous_scale=["#DCFCE7", "#F59E0B", "#EF4444"],
                )
                style_fig(fig, 400)
                fig.update_layout(coloraxis_showscale=False)
                fig.update_xaxes(title="Average delivery days")
                fig.update_yaxes(title="Late delivery rate (%)")
                show_chart(fig)

    days = orders_df.dropna(subset=["delivery_days"])
    if not days.empty:
        with card("del-hist"):
            card_head("📊", "Delivery-time distribution")
            fig = px.histogram(days, x="delivery_days", nbins=35, color_discrete_sequence=[CYAN])
            style_fig(fig, 320)
            fig.update_xaxes(title="Delivery days")
            fig.update_yaxes(title="Orders")
            show_chart(fig)

    if not delivery.empty:
        table = delivery.rename(
            columns={
                "customer_state": "State", "orders": "Orders",
                "late_rate": "Late rate", "avg_delivery_days": "Avg delivery days",
            }
        )
        table["Orders"] = table["Orders"].map(lambda x: f"{x:,}")
        table["Late rate"] = table["Late rate"].map(lambda x: f"{x:.1f}%")
        table["Avg delivery days"] = table["Avg delivery days"].map(lambda x: f"{x:.1f}")
        show_table(table[["State", "Orders", "Late rate", "Avg delivery days"]])


def page_business_insights() -> None:
    category = f.groupby("category")["revenue"].sum().sort_values(ascending=False)
    state = f.groupby("customer_state")["revenue"].sum().sort_values(ascending=False)
    peak_month = monthly["revenue"].idxmax()

    decision_card(
        "Executive decision center",
        "What should the business pay attention to?",
        "The dashboard connects revenue concentration, customer geography and delivery "
        "performance to help prioritize commercial and operational actions.",
    )

    section("Key findings")
    i1, i2, i3 = st.columns(3)
    with i1:
        insight_card("🏆", "Category leader",
                     text=f"<b>{category.index[0]}</b> is the highest-revenue category.<br><br>"
                          f"Revenue: <b>{brl(category.iloc[0])}</b>")
    with i2:
        insight_card("🌎", "Geographic leader",
                     text=f"<b>{state.index[0]}</b> contributes the largest revenue among customer states."
                          f"<br><br>Revenue: <b>{brl(state.iloc[0])}</b>")
    with i3:
        insight_card("📅", "Peak period",
                     text=f"The strongest monthly revenue occurred in <b>{peak_month:%B %Y}</b>."
                          f"<br><br>Revenue: <b>{brl(monthly['revenue'].max())}</b>")

    section("Recommended actions")
    actions = [
        ("🎯", "Protect revenue leaders",
         "Prioritize high-performing categories with inventory availability, merchandising and targeted promotions."),
        ("🚚", "Investigate delivery risk",
         "Focus operational reviews on states with elevated late-delivery rates and longer delivery times."),
        ("📊", "Monitor revenue concentration",
         "Track category and geographic concentration to spot dependency risk and diversification opportunities."),
    ]
    for col, (icon, title, text) in zip(st.columns(3), actions):
        with col:
            insight_card(icon, title, text=text)


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
        Olist Sales Insights • Business Analytics Portfolio Project • Built with Python, Pandas, Plotly &amp; Streamlit
    </div>
    """
)
