import inspect
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data import load_data


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Olist Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# THEME
# =========================================================

PURPLE = "#6D5CE7"
INDIGO = "#4F46E5"
BLUE = "#2563EB"
CYAN = "#0891B2"
GREEN = "#059669"
ORANGE = "#D97706"
RED = "#DC2626"
PINK = "#DB2777"
DARK = "#111827"
GREY = "#64748B"
LIGHT = "#F5F7FB"
BORDER = "#E5E7EB"

PAGES = [
    "Overview",
    "Revenue Intelligence",
    "Sales & Categories",
    "Delivery Operations",
    "Business Insights",
]

PAGE_ICONS = {
    "Overview": "🏠",
    "Revenue Intelligence": "📈",
    "Sales & Categories": "🏷️",
    "Delivery Operations": "🚚",
    "Business Insights": "💡",
}


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(109,92,231,0.08),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(37,99,235,0.05),
                transparent 25%
            ),
            {LIGHT};
    }}

    .block-container {{
        max-width: 1550px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    h1,h2,h3,h4 {{
        color: {DARK} !important;
    }}

    /* SIDEBAR */

    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #0B1026 0%,
            #151B38 100%
        );
    }}

    section[data-testid="stSidebar"] * {{
        color: #E5E7EB;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: white !important;
    }}

    .brand {{
        display:flex;
        align-items:center;
        gap:12px;
        padding:8px 4px 20px 4px;
    }}

    .brand-logo {{
        width:45px;
        height:45px;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:linear-gradient(
            135deg,
            #6D5CE7,
            #8B5CF6
        );
        color:white;
        font-size:22px;
        font-weight:900;
        box-shadow:0 10px 25px rgba(109,92,231,.35);
    }}

    .brand-name {{
        color:white;
        font-size:18px;
        font-weight:800;
    }}

    .brand-sub {{
        color:#94A3B8;
        font-size:11px;
        margin-top:3px;
    }}

    /* HEADER */

    .eyebrow {{
        color:{PURPLE};
        font-size:11px;
        font-weight:900;
        letter-spacing:2px;
        text-transform:uppercase;
        margin-bottom:5px;
    }}

    .main-title {{
        font-size:38px;
        font-weight:850;
        color:{DARK};
        letter-spacing:-1.5px;
        line-height:1.1;
    }}

    .subtitle {{
        color:{GREY};
        font-size:14px;
        margin-top:7px;
        margin-bottom:20px;
    }}

    /* KPI */

    .kpi {{
        border-radius:20px;
        padding:20px;
        min-height:145px;
        color:white;
        box-shadow:0 12px 30px rgba(15,23,42,.12);
        overflow:hidden;
    }}

    .kpi-label {{
        font-size:12px;
        font-weight:700;
        opacity:.9;
    }}

    .kpi-value {{
        font-size:28px;
        font-weight:850;
        margin-top:12px;
        letter-spacing:-1px;
    }}

    .kpi-note {{
        font-size:11px;
        margin-top:7px;
        opacity:.82;
    }}

    /* CARDS */

    .card {{
        background:white;
        border:1px solid {BORDER};
        border-radius:20px;
        padding:20px;
        box-shadow:0 7px 25px rgba(15,23,42,.045);
        margin-bottom:16px;
    }}

    .card-title {{
        color:{DARK};
        font-size:16px;
        font-weight:800;
        margin-bottom:3px;
    }}

    .card-sub {{
        color:#94A3B8;
        font-size:11px;
        margin-bottom:10px;
    }}

    /* DECISION */

    .decision {{
        background:linear-gradient(
            135deg,
            #111827,
            #272052,
            #4338CA
        );
        border-radius:20px;
        padding:25px;
        color:white;
        box-shadow:0 15px 40px rgba(67,56,202,.18);
        margin:15px 0;
    }}

    .decision-label {{
        color:#C4B5FD;
        font-size:10px;
        font-weight:900;
        letter-spacing:1.5px;
        text-transform:uppercase;
    }}

    .decision-title {{
        color:white;
        font-size:23px;
        font-weight:850;
        margin-top:7px;
    }}

    .decision-text {{
        color:#D1D5DB;
        font-size:13px;
        line-height:1.7;
        margin-top:8px;
    }}

    /* INSIGHT */

    .insight {{
        background:white;
        border:1px solid {BORDER};
        border-radius:17px;
        padding:19px;
        height:100%;
    }}

    .insight-icon {{
        font-size:22px;
        margin-bottom:8px;
    }}

    .insight-title {{
        font-weight:800;
        font-size:14px;
        color:{DARK};
    }}

    .insight-text {{
        color:{GREY};
        font-size:12px;
        line-height:1.6;
        margin-top:6px;
    }}

    /* TABLE */

    .metric-big {{
        font-size:30px;
        font-weight:850;
        color:{DARK};
    }}

    .metric-small {{
        font-size:11px;
        color:#94A3B8;
    }}

    .footer {{
        text-align:center;
        color:#94A3B8;
        font-size:11px;
        border-top:1px solid {BORDER};
        padding-top:20px;
        margin-top:40px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def brl(value):
    if pd.isna(value):
        return "R$ 0"
    return f"R$ {float(value):,.0f}"


def pct(value):
    if pd.isna(value):
        return "0.0%"
    return f"{float(value):.1f}%"


def show_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Arial, sans-serif",
            color=DARK,
            size=11,
        ),
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
        ),
    )

    if "width" in inspect.signature(st.plotly_chart).parameters:
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )
    else:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )


def card(title, subtitle=""):
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def close_card():
    st.markdown("</div>", unsafe_allow_html=True)


def kpi(label, value, note, gradient):
    st.markdown(
        f"""
        <div class="kpi"
             style="background:{gradient};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def decision(title, text):
    st.markdown(
        f"""
        <div class="decision">
            <div class="decision-label">
                BUSINESS DECISION
            </div>
            <div class="decision-title">
                {title}
            </div>
            <div class="decision-text">
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title, subtitle=""):
    st.markdown(
        f"""
        <div style="margin-top:24px;margin-bottom:12px;">
            <div style="
                font-size:19px;
                font-weight:850;
                color:{DARK};
            ">
                {title}
            </div>
            <div style="
                font-size:12px;
                color:#94A3B8;
                margin-top:3px;
            ">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# LOAD DATA
# =========================================================

try:
    df = load_data().copy()
except Exception as e:
    st.error("Unable to load the Olist dataset.")
    st.exception(e)
    st.stop()


# =========================================================
# DATA CLEANING
# =========================================================

df["month"] = pd.to_datetime(df["month"])

df["revenue"] = pd.to_numeric(
    df["revenue"],
    errors="coerce",
).fillna(0)

df["category"] = (
    df["category"]
    .fillna("unknown")
    .astype(str)
    .str.replace("_", " ")
    .str.title()
)

df["customer_state"] = (
    df["customer_state"]
    .fillna("Unknown")
    .astype(str)
)

df["order_id"] = df["order_id"].astype(str)

if "delivery_days" in df.columns:
    df["delivery_days"] = pd.to_numeric(
        df["delivery_days"],
        errors="coerce",
    )

if "is_late" in df.columns:
    df["is_late"] = pd.to_numeric(
        df["is_late"],
        errors="coerce",
    ).fillna(0)

if "review_score" in df.columns:
    df["review_score"] = pd.to_numeric(
        df["review_score"],
        errors="coerce",
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-logo">OI</div>
            <div>
                <div class="brand-name">
                    Olist Intelligence
                </div>
                <div class="brand-sub">
                    Revenue & Sales Analytics
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        PAGES,
        format_func=lambda x:
            f"{PAGE_ICONS[x]}  {x}",
    )

    st.markdown("---")

    st.markdown("### Filters")

    min_date = df["month"].min().date()
    max_date = df["month"].max().date()

    selected_dates = st.date_input(
        "Analysis period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    states = sorted(
        df["customer_state"]
        .dropna()
        .unique()
    )

    selected_states = st.multiselect(
        "Customer states",
        states,
        default=[],
    )

    categories = sorted(
        df["category"]
        .dropna()
        .unique()
    )

    selected_categories = st.multiselect(
        "Product categories",
        categories,
        default=[],
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            font-size:11px;
            color:#94A3B8;
            line-height:1.6;
        ">
        <b style="color:#E5E7EB;">
        Dataset
        </b><br>
        Brazilian Olist E-Commerce<br><br>

        <b style="color:#E5E7EB;">
        Analytics focus
        </b><br>
        Revenue • Sales • Categories<br>
        Delivery • Business Decisions
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = df.copy()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = (
        pd.Timestamp(selected_dates[1])
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )

    filtered = filtered[
        (filtered["month"] >= start_date)
        & (filtered["month"] <= end_date)
    ]

if selected_states:
    filtered = filtered[
        filtered["customer_state"].isin(
            selected_states
        )
    ]

if selected_categories:
    filtered = filtered[
        filtered["category"].isin(
            selected_categories
        )
    ]


# =========================================================
# COMMON METRICS
# =========================================================

total_revenue = filtered["revenue"].sum()

orders = filtered["order_id"].nunique()

customers = (
    filtered["customer_id"].nunique()
    if "customer_id" in filtered.columns
    else orders
)

aov = (
    total_revenue / orders
    if orders
    else 0
)

late_rate = (
    filtered["is_late"].mean() * 100
    if "is_late" in filtered.columns
    and len(filtered)
    else 0
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="eyebrow">OLIST REVENUE INTELLIGENCE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="main-title">{page}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        A decision-focused sales intelligence platform
        for revenue, category and operational performance.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAGE 1 — OVERVIEW
# =========================================================

def page_overview():

    # -----------------------------------------------------
    # KPI ROW
    # -----------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi(
            "Total Revenue",
            brl(total_revenue),
            "Item revenue within selected period",
            "linear-gradient(135deg,#5B5CE2,#7C3AED)",
        )

    with k2:
        kpi(
            "Orders",
            f"{orders:,}",
            "Unique delivered orders",
            "linear-gradient(135deg,#2563EB,#0891B2)",
        )

    with k3:
        kpi(
            "Average Order Value",
            brl(aov),
            "Revenue per order",
            "linear-gradient(135deg,#059669,#0D9488)",
        )

    with k4:
        kpi(
            "Late Delivery Rate",
            pct(late_rate),
            "Orders delivered after estimate",
            "linear-gradient(135deg,#D97706,#EA580C)",
        )

    # -----------------------------------------------------
    # REVENUE TREND
    # -----------------------------------------------------

    section(
        "Revenue Performance",
        "Monthly revenue trend across the selected period.",
    )

    monthly = (
        filtered.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("month")
    )

    monthly["aov"] = (
        monthly["revenue"]
        / monthly["orders"].replace(0, pd.NA)
    )

    if not monthly.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=monthly["month"],
                y=monthly["revenue"],
                mode="lines+markers",
                name="Revenue",
                line=dict(
                    color=PURPLE,
                    width=3,
                ),
                fill="tozeroy",
                fillcolor="rgba(109,92,231,0.10)",
                hovertemplate=(
                    "%{x|%b %Y}<br>"
                    "Revenue: R$ %{y:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="Revenue",
        )

        show_chart(fig)

    # -----------------------------------------------------
    # CATEGORY + STATES
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        card(
            "Top Categories",
            "Revenue contribution by product category.",
        )

        cat = (
            filtered.groupby("category")
            .agg(
                revenue=("revenue", "sum"),
                orders=("order_id", "nunique"),
            )
            .reset_index()
            .sort_values(
                "revenue",
                ascending=False,
            )
            .head(10)
        )

        fig = px.bar(
            cat.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
        )

        fig.update_traces(
            marker_color=PURPLE,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: R$ %{x:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=430,
            xaxis_title="Revenue",
            yaxis_title="",
        )

        show_chart(fig)
        close_card()

    with c2:

        card(
            "State Performance",
            "Revenue generated across customer states.",
        )

        state = (
            filtered.groupby("customer_state")
            .agg(
                revenue=("revenue", "sum"),
                orders=("order_id", "nunique"),
            )
            .reset_index()
            .sort_values(
                "revenue",
                ascending=False,
            )
            .head(10)
        )

        fig = px.bar(
            state.sort_values("revenue"),
            x="revenue",
            y="customer_state",
            orientation="h",
        )

        fig.update_traces(
            marker_color=BLUE,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: R$ %{x:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=430,
            xaxis_title="Revenue",
            yaxis_title="",
        )

        show_chart(fig)
        close_card()

    # -----------------------------------------------------
    # EXECUTIVE SUMMARY
    # -----------------------------------------------------

    if not monthly.empty:

        best_month = monthly.loc[
            monthly["revenue"].idxmax()
        ]

        best_category = (
            cat.iloc[0]["category"]
            if not cat.empty
            else "N/A"
        )

        decision(
            "Executive Sales Readout",
            f"""
            The selected business period generated
            <b>{brl(total_revenue)}</b> across
            <b>{orders:,}</b> orders, with an average order value
            of <b>{brl(aov)}</b>.
            <br><br>
            The strongest revenue month was
            <b>{best_month["month"].strftime("%B %Y")}</b>,
            while <b>{best_category}</b> was the leading
            product category by revenue.
            <br><br>
            The next commercial priority should be to protect
            high-performing categories while improving order value
            in high-volume categories.
            """,
        )


# =========================================================
# PAGE 2 — REVENUE INTELLIGENCE
# =========================================================

def page_revenue():

    monthly = (
        filtered.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("month")
    )

    monthly["aov"] = (
        monthly["revenue"]
        / monthly["orders"].replace(0, pd.NA)
    )

    monthly["mom_growth"] = (
        monthly["revenue"]
        .pct_change()
        * 100
    )

    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    peak_month = (
        monthly.loc[
            monthly["revenue"].idxmax()
        ]
        if not monthly.empty
        else None
    )

    latest_growth = (
        monthly.iloc[-1]["mom_growth"]
        if len(monthly) > 1
        else 0
    )

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        kpi(
            "Peak Revenue Month",
            (
                peak_month["month"].strftime("%b %Y")
                if peak_month is not None
                else "N/A"
            ),
            (
                brl(peak_month["revenue"])
                if peak_month is not None
                else "No data"
            ),
            "linear-gradient(135deg,#6D5CE7,#4F46E5)",
        )

    with r2:
        kpi(
            "Latest MoM Growth",
            pct(latest_growth),
            "Revenue change vs previous month",
            "linear-gradient(135deg,#059669,#0D9488)",
        )

    with r3:
        kpi(
            "Peak Monthly Revenue",
            (
                brl(peak_month["revenue"])
                if peak_month is not None
                else "R$ 0"
            ),
            "Highest observed month",
            "linear-gradient(135deg,#2563EB,#0891B2)",
        )

    with r4:
        kpi(
            "Revenue per Order",
            brl(aov),
            "Current selected period",
            "linear-gradient(135deg,#D97706,#EA580C)",
        )

    # -----------------------------------------------------
    # TREND + GROWTH
    # -----------------------------------------------------

    section(
        "Revenue Trend & Growth",
        "Identify acceleration, contraction and inflection points.",
    )

    c1, c2 = st.columns(2)

    with c1:

        card(
            "Monthly Revenue",
            "Absolute revenue performance.",
        )

        fig = px.area(
            monthly,
            x="month",
            y="revenue",
        )

        fig.update_traces(
            line_color=PURPLE,
            fillcolor="rgba(109,92,231,.15)",
        )

        fig.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="Revenue",
        )

        show_chart(fig)
        close_card()

    with c2:

        card(
            "Month-over-Month Growth",
            "Percentage change in monthly revenue.",
        )

        growth_df = monthly.dropna(
            subset=["mom_growth"]
        )

        fig = px.bar(
            growth_df,
            x="month",
            y="mom_growth",
        )

        fig.update_traces(
            marker_color=[
                GREEN if x >= 0 else RED
                for x in growth_df["mom_growth"]
            ],
            hovertemplate=(
                "%{x|%b %Y}<br>"
                "Growth: %{y:.1f}%"
                "<extra></extra>"
            ),
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="#CBD5E1",
        )

        fig.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="Growth %",
        )

        show_chart(fig)
        close_card()

    # -----------------------------------------------------
    # CATEGORY CONCENTRATION
    # -----------------------------------------------------

    section(
        "Revenue Concentration",
        "Measure dependency on leading product categories.",
    )

    category = (
        filtered.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False,
        )
    )

    category["share"] = (
        category["revenue"]
        / category["revenue"].sum()
        * 100
    )

    category["cumulative_share"] = (
        category["share"].cumsum()
    )

    c1, c2 = st.columns(2)

    with c1:

        card(
            "Pareto Revenue Curve",
            "How quickly categories accumulate total revenue.",
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=category["category"],
                y=category["share"],
                name="Revenue Share",
                marker_color=PURPLE,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=category["category"],
                y=category["cumulative_share"],
                name="Cumulative Share",
                mode="lines+markers",
                yaxis="y2",
                line=dict(
                    color=ORANGE,
                    width=3,
                ),
            )
        )

        fig.update_layout(
            height=470,
            yaxis=dict(
                title="Category Revenue Share %",
            ),
            yaxis2=dict(
                title="Cumulative %",
                overlaying="y",
                side="right",
                range=[0, 105],
            ),
            xaxis=dict(
                tickangle=-45,
            ),
        )

        show_chart(fig)
        close_card()

    with c2:

        top5 = (
            category.head(5)["revenue"].sum()
            / category["revenue"].sum()
            * 100
            if not category.empty
            else 0
        )

        top10 = (
            category.head(10)["revenue"].sum()
            / category["revenue"].sum()
            * 100
            if not category.empty
            else 0
        )

        card(
            "Concentration Signals",
            "Revenue dependency indicators.",
        )

        st.markdown(
            f"""
            <div style="padding:20px 5px;">

                <div style="margin-bottom:25px;">
                    <div class="metric-small">
                        TOP 5 CATEGORY SHARE
                    </div>
                    <div class="metric-big">
                        {top5:.1f}%
                    </div>
                </div>

                <div style="margin-bottom:25px;">
                    <div class="metric-small">
                        TOP 10 CATEGORY SHARE
                    </div>
                    <div class="metric-big">
                        {top10:.1f}%
                    </div>
                </div>

                <div>
                    <div class="metric-small">
                        NUMBER OF CATEGORIES
                    </div>
                    <div class="metric-big">
                        {len(category)}
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        close_card()

    if top5 >= 60:

        decision(
            "Concentration Risk",
            f"""
            The top five categories account for
            <b>{top5:.1f}%</b> of revenue.
            <br><br>
            Protect inventory, pricing and customer experience
            for these categories because a disruption could
            materially affect overall revenue.
            """,
        )

    else:

        decision(
            "Healthy Revenue Diversification",
            f"""
            The top five categories contribute
            <b>{top5:.1f}%</b> of revenue.
            <br><br>
            The portfolio is relatively diversified, giving
            management room to invest in growth categories
            without excessive dependence on a small number
            of product groups.
            """,
        )


# =========================================================
# PAGE 3 — SALES & CATEGORIES
# =========================================================

def page_sales_categories():

    category = (
        filtered.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    category["aov"] = (
        category["revenue"]
        / category["orders"].replace(0, pd.NA)
    )

    category = category.sort_values(
        "revenue",
        ascending=False,
    )

    avg_orders = category["orders"].mean()
    avg_aov = category["aov"].mean()

    category["revenue_share"] = (
        category["revenue"]
        / category["revenue"].sum()
        * 100
    )

    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    top = category.iloc[0] if not category.empty else None

    high_volume_high_value = category[
        (category["orders"] >= avg_orders)
        & (category["aov"] >= avg_aov)
    ]

    high_volume_low_value = category[
        (category["orders"] >= avg_orders)
        & (category["aov"] < avg_aov)
    ]

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        kpi(
            "Top Category",
            (
                str(top["category"])
                if top is not None
                else "N/A"
            ),
            (
                brl(top["revenue"])
                if top is not None
                else ""
            ),
            "Highest revenue contribution",
            "linear-gradient(135deg,#6D5CE7,#7C3AED)",
        )

    with s2:
        kpi(
            "Category AOV",
            brl(avg_aov),
            "Average across categories",
            "linear-gradient(135deg,#2563EB,#0891B2)",
        )

    with s3:
        kpi(
            "High-Value Categories",
            f"{len(high_volume_high_value)}",
            "High volume + high AOV",
            "linear-gradient(135deg,#059669,#0D9488)",
        )

    with s4:
        kpi(
            "Growth Opportunities",
            f"{len(high_volume_low_value)}",
            "High volume + lower AOV",
            "linear-gradient(135deg,#D97706,#EA580C)",
        )

    # -----------------------------------------------------
    # TOP CATEGORIES + SCATTER
    # -----------------------------------------------------

    section(
        "Category Performance",
        "Compare revenue scale, demand volume and order value.",
    )

    c1, c2 = st.columns([1, 1.25])

    with c1:

        card(
            "Revenue Ranking",
            "Top categories by total revenue.",
        )

        top_categories = category.head(12).copy()

        fig = px.bar(
            top_categories.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
        )

        fig.update_traces(
            marker_color=PURPLE,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: R$ %{x:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=520,
            xaxis_title="Revenue",
            yaxis_title="",
        )

        show_chart(fig)
        close_card()

    with c2:

        card(
            "Volume vs Value Matrix",
            "Identify high-volume and high-value categories.",
        )

        matrix = category.copy()

        matrix["segment"] = "Low Volume / Low Value"

        matrix.loc[
            (matrix["orders"] >= avg_orders)
            & (matrix["aov"] >= avg_aov),
            "segment",
        ] = "High Volume / High Value"

        matrix.loc[
            (matrix["orders"] >= avg_orders)
            & (matrix["aov"] < avg_aov),
            "segment",
        ] = "High Volume / Low Value"

        matrix.loc[
            (matrix["orders"] < avg_orders)
            & (matrix["aov"] >= avg_aov),
            "segment",
        ] = "Low Volume / High Value"

        fig = px.scatter(
            matrix,
            x="orders",
            y="aov",
            size="revenue",
            color="segment",
            text="category",
            color_discrete_map={
                "High Volume / High Value": GREEN,
                "High Volume / Low Value": BLUE,
                "Low Volume / High Value": ORANGE,
                "Low Volume / Low Value": RED,
            },
            hover_data=[
                "revenue",
                "revenue_share",
            ],
        )

        fig.update_traces(
            textposition="top center",
        )

        fig.add_hline(
            y=avg_aov,
            line_dash="dash",
            line_color="#CBD5E1",
        )

        fig.add_vline(
            x=avg_orders,
            line_dash="dash",
            line_color="#CBD5E1",
        )

        fig.update_layout(
            height=520,
            xaxis_title="Orders",
            yaxis_title="Average Order Value",
        )

        show_chart(fig)
        close_card()

    # -----------------------------------------------------
    # OPPORTUNITY
    # -----------------------------------------------------

    if not high_volume_low_value.empty:

        opportunity = high_volume_low_value.sort_values(
            ["orders", "revenue"],
            ascending=False,
        ).iloc[0]

        decision(
            "Revenue Expansion Opportunity",
            f"""
            <b>{opportunity["category"]}</b> generates
            <b>{opportunity["orders"]:,.0f}</b> orders but its
            AOV is only <b>{brl(opportunity["aov"])}</b>.
            <br><br>
            This is a strong candidate for bundles,
            cross-selling, premium alternatives and
            minimum-order promotions.
            """,
        )

    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------

    section(
        "Category Performance Table",
        "Detailed commercial ranking.",
    )

    table = category.copy()

    table["Revenue"] = table["revenue"].map(brl)
    table["Revenue Share"] = table["revenue_share"].map(
        lambda x: f"{x:.1f}%"
    )
    table["Orders"] = table["orders"].map(
        lambda x: f"{x:,.0f}"
    )
    table["AOV"] = table["aov"].map(brl)

    table = table[
        [
            "category",
            "Revenue",
            "Revenue Share",
            "Orders",
            "AOV",
        ]
    ].rename(
        columns={
            "category": "Category",
        }
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=500,
    )


# =========================================================
# PAGE 4 — DELIVERY OPERATIONS
# =========================================================

def page_delivery():

    if "delivery_days" not in filtered.columns:

        st.warning(
            "Delivery information is unavailable."
        )
        return

    delivery = filtered.copy()

    avg_delivery = delivery[
        "delivery_days"
    ].mean()

    median_delivery = delivery[
        "delivery_days"
    ].median()

    late = (
        delivery["is_late"].mean() * 100
        if "is_late" in delivery.columns
        else 0
    )

    late_revenue = (
        delivery.loc[
            delivery["is_late"] == 1,
            "revenue",
        ].sum()
        if "is_late" in delivery.columns
        else 0
    )

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        kpi(
            "Average Delivery",
            f"{avg_delivery:.1f} days",
            "Purchase to delivery",
            "linear-gradient(135deg,#2563EB,#0891B2)",
        )

    with d2:
        kpi(
            "Median Delivery",
            f"{median_delivery:.0f} days",
            "Typical customer experience",
            "linear-gradient(135deg,#6D5CE7,#7C3AED)",
        )

    with d3:
        kpi(
            "Late Delivery Rate",
            pct(late),
            "Orders delivered late",
            "linear-gradient(135deg,#D97706,#EA580C)",
        )

    with d4:
        kpi(
            "Late-Order Revenue",
            brl(late_revenue),
            "Revenue exposed to late delivery",
            "linear-gradient(135deg,#DC2626,#B91C1C)",
        )

    # -----------------------------------------------------
    # DELIVERY DISTRIBUTION
    # -----------------------------------------------------

    section(
        "Delivery Performance",
        "Understand operational speed and its relationship with sales.",
    )

    c1, c2 = st.columns(2)

    with c1:

        card(
            "Delivery Time Distribution",
            "Number of delivered orders by delivery duration.",
        )

        delivery_plot = delivery[
            delivery["delivery_days"].between(
                0,
                delivery["delivery_days"].quantile(.99),
            )
        ]

        fig = px.histogram(
            delivery_plot,
            x="delivery_days",
            nbins=30,
        )

        fig.update_traces(
            marker_color=BLUE,
        )

        fig.update_layout(
            height=420,
            xaxis_title="Delivery Days",
            yaxis_title="Orders",
        )

        show_chart(fig)
        close_card()

    with c2:

        card(
            "Late vs On-Time Revenue",
            "Revenue exposure by delivery performance.",
        )

        if "is_late" in delivery.columns:

            status = (
                delivery.groupby("is_late")
                .agg(
                    revenue=("revenue", "sum"),
                    orders=("order_id", "nunique"),
                )
                .reset_index()
            )

            status["status"] = status["is_late"].map(
                {
                    0: "On Time",
                    1: "Late",
                }
            )

            fig = px.bar(
                status,
                x="status",
                y="revenue",
            )

            fig.update_traces(
                marker_color=[
                    GREEN if x == "On Time"
                    else RED
                    for x in status["status"]
                ],
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Revenue: R$ %{y:,.0f}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=420,
                xaxis_title="",
                yaxis_title="Revenue",
            )

            show_chart(fig)

        close_card()

    # -----------------------------------------------------
    # STATE RISK
    # -----------------------------------------------------

    section(
        "Delivery Risk by State",
        "Find locations where service performance may threaten revenue.",
    )

    if "is_late" in delivery.columns:

        state_delivery = (
            delivery.groupby("customer_state")
            .agg(
                orders=("order_id", "nunique"),
                revenue=("revenue", "sum"),
                late_rate=("is_late", "mean"),
                avg_delivery=("delivery_days", "mean"),
            )
            .reset_index()
        )

        state_delivery["late_rate"] *= 100

        state_delivery = state_delivery[
            state_delivery["orders"] >= 100
        ]

        state_delivery = state_delivery.sort_values(
            "late_rate",
            ascending=False,
        )

        if not state_delivery.empty:

            fig = px.scatter(
                state_delivery,
                x="late_rate",
                y="revenue",
                size="orders",
                color="late_rate",
                text="customer_state",
                color_continuous_scale=[
                    "#DBEAFE",
                    "#F59E0B",
                    "#DC2626",
                ],
            )

            fig.update_traces(
                textposition="top center",
            )

            fig.update_layout(
                height=500,
                xaxis_title="Late Delivery Rate %",
                yaxis_title="Revenue",
                coloraxis_colorbar_title="Late %",
            )

            show_chart(fig)

            risk = state_delivery.iloc[0]

            decision(
                "Operational Risk Signal",
                f"""
                <b>{risk["customer_state"]}</b> has the highest
                late-delivery rate among states with at least
                100 orders: <b>{risk["late_rate"]:.1f}%</b>.
                <br><br>
                Average delivery time is
                <b>{risk["avg_delivery"]:.1f} days</b>, while the
                state represents <b>{brl(risk["revenue"])}</b>
                in revenue.
                <br><br>
                Prioritize carrier performance and fulfilment
                investigation in this market.
                """,
            )

    # -----------------------------------------------------
    # REVIEW IMPACT
    # -----------------------------------------------------

    if "review_score" in delivery.columns:

        section(
            "Delivery & Customer Experience",
            "Explore whether delivery performance aligns with review outcomes.",
        )

        review_df = delivery.dropna(
            subset=[
                "review_score",
                "delivery_days",
            ]
        )

        if not review_df.empty:

            review_summary = (
                review_df.groupby("review_score")
                .agg(
                    avg_delivery=(
                        "delivery_days",
                        "mean",
                    ),
                    orders=(
                        "order_id",
                        "nunique",
                    ),
                )
                .reset_index()
            )

            fig = px.bar(
                review_summary,
                x="review_score",
                y="avg_delivery",
            )

            fig.update_traces(
                marker_color=PURPLE,
            )

            fig.update_layout(
                height=400,
                xaxis_title="Review Score",
                yaxis_title="Average Delivery Days",
            )

            show_chart(fig)


# =========================================================
# PAGE 5 — BUSINESS INSIGHTS
# =========================================================

def page_business():

    # -----------------------------------------------------
    # BUILD BUSINESS METRICS
    # -----------------------------------------------------

    category = (
        filtered.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    category["aov"] = (
        category["revenue"]
        / category["orders"].replace(0, pd.NA)
    )

    state = (
        filtered.groupby("customer_state")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    state["aov"] = (
        state["revenue"]
        / state["orders"].replace(0, pd.NA)
    )

    top_category = (
        category.sort_values(
            "revenue",
            ascending=False,
        ).iloc[0]
        if not category.empty
        else None
    )

    top_state = (
        state.sort_values(
            "revenue",
            ascending=False,
        ).iloc[0]
        if not state.empty
        else None
    )

    avg_category_aov = (
        category["aov"].mean()
        if not category.empty
        else 0
    )

    opportunity_categories = category[
        (category["orders"] >= category["orders"].mean())
        & (category["aov"] < avg_category_aov)
    ]

    # -----------------------------------------------------
    # EXECUTIVE SCORECARD
    # -----------------------------------------------------

    section(
        "Executive Decision Center",
        "Translate analytics into commercial actions.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            f"""
            <div class="insight">
                <div class="insight-icon">🏆</div>
                <div class="insight-title">
                    Revenue Leader
                </div>
                <div class="insight-text">
                    <b>
                    {top_category["category"]
                    if top_category is not None else "N/A"}
                    </b>
                    is the strongest category by revenue,
                    generating
                    <b>
                    {brl(top_category["revenue"])
                    if top_category is not None else "R$ 0"}
                    </b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            f"""
            <div class="insight">
                <div class="insight-icon">📍</div>
                <div class="insight-title">
                    Strongest Market
                </div>
                <div class="insight-text">
                    <b>
                    {top_state["customer_state"]
                    if top_state is not None else "N/A"}
                    </b>
                    leads state-level revenue with
                    <b>
                    {brl(top_state["revenue"])
                    if top_state is not None else "R$ 0"}
                    </b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            f"""
            <div class="insight">
                <div class="insight-icon">🚀</div>
                <div class="insight-title">
                    Growth Pipeline
                </div>
                <div class="insight-text">
                    <b>
                    {len(opportunity_categories)}
                    </b>
                    categories have high order volume but
                    below-average AOV, creating potential
                    upsell opportunities.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # BUSINESS PRIORITIES
    # -----------------------------------------------------

    section(
        "Priority Actions",
        "What management should do with the evidence.",
    )

    if top_category is not None:

        decision(
            "1 — Protect Revenue Leaders",
            f"""
            <b>{top_category["category"]}</b> is the largest
            revenue contributor.
            <br><br>
            Maintain availability, monitor pricing and protect
            the customer experience around this category.
            """,
        )

    if not opportunity_categories.empty:

        opp = opportunity_categories.sort_values(
            "orders",
            ascending=False,
        ).iloc[0]

        decision(
            "2 — Increase Revenue per Order",
            f"""
            <b>{opp["category"]}</b> has strong order volume
            but an AOV of only <b>{brl(opp["aov"])}</b>.
            <br><br>
            Test bundles, complementary products,
            premium alternatives and threshold-based offers.
            """,
        )

    if late_rate >= 10:

        decision(
            "3 — Reduce Delivery Risk",
            f"""
            The current late-delivery rate is
            <b>{late_rate:.1f}%</b>.
            <br><br>
            Delivery reliability should be treated as a
            commercial issue because delayed orders expose
            both revenue and customer satisfaction.
            """,
        )

    else:

        decision(
            "3 — Maintain Delivery Discipline",
            f"""
            Late delivery is currently at
            <b>{late_rate:.1f}%</b>.
            <br><br>
            Continue monitoring fulfilment performance while
            protecting the operational standards that support
            customer experience.
            """,
        )

    # -----------------------------------------------------
    # TOP STATE REVENUE
    # -----------------------------------------------------

    section(
        "Market Opportunity",
        "Revenue distribution across customer states.",
    )

    if not state.empty:

        state_chart = state.sort_values(
            "revenue",
            ascending=False,
        ).head(12)

        fig = px.bar(
            state_chart.sort_values("revenue"),
            x="revenue",
            y="customer_state",
            orientation="h",
        )

        fig.update_traces(
            marker_color=BLUE,
        )

        fig.update_layout(
            height=470,
            xaxis_title="Revenue",
            yaxis_title="State",
        )

        show_chart(fig)

    # -----------------------------------------------------
    # FINAL EXECUTIVE MESSAGE
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="decision">

            <div class="decision-label">
                MANAGEMENT SUMMARY
            </div>

            <div class="decision-title">
                From dashboard to decision
            </div>

            <div class="decision-text">

                The selected business period represents
                <b>{brl(total_revenue)}</b> in revenue across
                <b>{orders:,}</b> orders.

                The strongest opportunity is not simply to
                increase order volume, but to improve the
                economics of existing demand through category
                mix, average order value and operational
                reliability.

                <br><br>

                The dashboard therefore prioritizes three levers:
                <b>protect revenue leaders</b>,
                <b>increase value per transaction</b>, and
                <b>reduce delivery risk</b>.

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# ROUTER
# =========================================================

if page == "Overview":
    page_overview()

elif page == "Revenue Intelligence":
    page_revenue()

elif page == "Sales & Categories":
    page_sales_categories()

elif page == "Delivery Operations":
    page_delivery()

elif page == "Business Insights":
    page_business()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Olist Sales Intelligence • Revenue Analytics Dashboard
        <br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
