import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data import load_data


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# COLOR SYSTEM
# =========================================================

INDIGO = "#5B5CE2"
PURPLE = "#7C3AED"
BLUE = "#2563EB"
CYAN = "#06B6D4"
GREEN = "#10B981"
ORANGE = "#F59E0B"
RED = "#EF4444"
PINK = "#EC4899"
SLATE = "#64748B"
DARK = "#111827"

CHART_COLORS = [
    "#5B5CE2",
    "#7C3AED",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#EC4899",
    "#3B82F6",
    "#14B8A6",
    "#8B5CF6"
]


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(91,92,226,0.08), transparent 25%),
            radial-gradient(circle at 90% 10%, rgba(124,58,237,0.06), transparent 25%),
            #F7F8FC;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3, h4 {
        color: #111827 !important;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1F2937;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    .sidebar-brand {
        padding: 10px 4px 25px 4px;
    }

    .brand-logo {
        width: 42px;
        height: 42px;
        border-radius: 13px;
        background: linear-gradient(
            135deg,
            #5B5CE2,
            #8B5CF6
        );
        display: flex;
        align-items: center;
        justify-content: center;
        color: white !important;
        font-size: 20px;
        font-weight: 800;
        box-shadow: 0 8px 25px rgba(91,92,226,0.35);
    }

    .brand-name {
        font-size: 18px;
        font-weight: 800;
        color: white !important;
        margin-top: 10px;
    }

    .brand-sub {
        font-size: 11px;
        color: #9CA3AF !important;
        margin-top: 2px;
    }

    /* ---------- TOP HEADER ---------- */

    .eyebrow {
        color: #5B5CE2 !important;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .main-title {
        font-size: 38px;
        line-height: 1.1;
        font-weight: 850;
        color: #111827 !important;
        letter-spacing: -1.5px;
    }

    .subtitle {
        color: #6B7280 !important;
        font-size: 15px;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 8px 13px;
        border-radius: 999px;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #047857 !important;
        font-size: 12px;
        font-weight: 800;
    }

    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 0 4px rgba(16,185,129,0.12);
    }

    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #E7EAF0;
        border-radius: 20px;
        padding: 22px;
        min-height: 155px;
        box-shadow: 0 8px 30px rgba(15,23,42,0.055);
        position: relative;
        overflow: hidden;
    }

    .kpi-card:after {
        content: "";
        position: absolute;
        width: 90px;
        height: 90px;
        right: -25px;
        top: -25px;
        border-radius: 50%;
        background: rgba(91,92,226,0.07);
    }

    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .kpi-label {
        color: #6B7280 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .kpi-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: white !important;
    }

    .kpi-value {
        color: #111827 !important;
        font-size: 29px;
        font-weight: 850;
        margin-top: 18px;
        letter-spacing: -1px;
    }

    .kpi-description {
        color: #9CA3AF !important;
        font-size: 12px;
        margin-top: 7px;
    }

    /* ---------- SECTION HEADERS ---------- */

    .section-title {
        color: #111827 !important;
        font-size: 18px;
        font-weight: 800;
        margin-top: 24px;
        margin-bottom: 2px;
    }

    .section-subtitle {
        color: #94A3B8 !important;
        font-size: 12px;
        margin-bottom: 12px;
    }

    /* ---------- INSIGHT CARDS ---------- */

    .insight-card {
        background: white;
        border: 1px solid #E7EAF0;
        border-radius: 18px;
        padding: 20px;
        height: 100%;
        box-shadow: 0 7px 25px rgba(15,23,42,0.045);
    }

    .insight-icon {
        font-size: 23px;
        margin-bottom: 10px;
    }

    .insight-title {
        color: #111827 !important;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .insight-text {
        color: #64748B !important;
        font-size: 12px;
        line-height: 1.6;
    }

    /* ---------- DECISION CARD ---------- */

    .decision-card {
        background:
            linear-gradient(
                135deg,
                #111827 0%,
                #25204D 55%,
                #4338CA 100%
            );
        border-radius: 22px;
        padding: 28px;
        color: white !important;
        box-shadow: 0 15px 45px rgba(67,56,202,0.2);
    }

    .decision-label {
        color: #C4B5FD !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .decision-title {
        color: white !important;
        font-size: 25px;
        font-weight: 850;
        margin-top: 7px;
    }

    .decision-text {
        color: #D1D5DB !important;
        font-size: 13px;
        line-height: 1.7;
        margin-top: 10px;
    }

    /* ---------- STATUS ---------- */

    .status-good {
        display: inline-block;
        background: #ECFDF5;
        color: #047857 !important;
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 800;
    }

    .status-warning {
        display: inline-block;
        background: #FFF7ED;
        color: #C2410C !important;
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 800;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94A3B8 !important;
        font-size: 11px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #E5E7EB;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .main-title {
            font-size: 30px;
        }

        .subtitle {
            font-size: 13px;
        }

        .kpi-card {
            min-height: 135px;
            padding: 18px;
        }

        .kpi-value {
            font-size: 25px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()


# =========================================================
# DATA CLEANING
# =========================================================

df["month"] = pd.to_datetime(df["month"], errors="coerce")

if "delivery_days" in df.columns:
    df["delivery_days"] = pd.to_numeric(
        df["delivery_days"],
        errors="coerce"
    )

if "revenue" in df.columns:
    df["revenue"] = pd.to_numeric(
        df["revenue"],
        errors="coerce"
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-logo">OI</div>
            <div class="brand-name">Olist Analytics</div>
            <div class="brand-sub">Revenue Intelligence Platform</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "Overview",
            "Revenue Intelligence",
            "Sales & Categories",
            "Delivery Operations",
            "Business Insights"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### Filters")

    min_date = df["month"].min()
    max_date = df["month"].max()

    period = st.slider(
        "Analysis period",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(
            min_date.to_pydatetime(),
            max_date.to_pydatetime()
        ),
        format="MMM YYYY"
    )

    states = sorted(
        df["customer_state"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_states = st.multiselect(
        "Customer states",
        states,
        default=states
    )

    categories = sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        "Product categories",
        categories,
        default=categories
    )

    st.markdown("---")

    st.caption("Olist Brazilian E-Commerce Dataset")
    st.caption("Delivered orders • Revenue intelligence")


# =========================================================
# FILTER DATA
# =========================================================

mask = (
    (df["month"] >= pd.Timestamp(period[0])) &
    (df["month"] <= pd.Timestamp(period[1])) &
    (df["customer_state"].isin(selected_states)) &
    (df["category"].isin(selected_categories))
)

f = df.loc[mask].copy()

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# =========================================================
# CORE METRICS
# =========================================================

orders_df = f.drop_duplicates("order_id")

total_revenue = f["revenue"].sum()

total_orders = orders_df["order_id"].nunique()

aov = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

late_rate = (
    orders_df["is_late"].mean() * 100
    if "is_late" in orders_df.columns and len(orders_df) > 0
    else 0
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="eyebrow">OLIST ANALYTICS</div>',
    unsafe_allow_html=True
)

header_left, header_right = st.columns([5, 1])

with header_left:

    st.markdown(
        f"""
        <div class="main-title">{page}</div>
        <div class="subtitle">
            Turn transaction data into commercially useful decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        """
        <div style="text-align:right;">
            <div class="live-badge">
                <span class="live-dot"></span>
                LIVE DATA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-icon"
                     style="background:linear-gradient(135deg,#5B5CE2,#7C3AED);">
                    ₹
                </div>
            </div>

            <div class="kpi-value">
                R$ {total_revenue:,.0f}
            </div>

            <div class="kpi-description">
                Delivered order revenue
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">Orders</div>
                <div class="kpi-icon"
                     style="background:linear-gradient(135deg,#2563EB,#06B6D4);">
                    ↗
                </div>
            </div>

            <div class="kpi-value">
                {total_orders:,.0f}
            </div>

            <div class="kpi-description">
                Unique delivered orders
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">Average Order Value</div>
                <div class="kpi-icon"
                     style="background:linear-gradient(135deg,#10B981,#14B8A6);">
                    $
                </div>
            </div>

            <div class="kpi-value">
                R$ {aov:,.0f}
            </div>

            <div class="kpi-description">
                Revenue per order
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    late_color = "#EF4444" if late_rate > 10 else "#F59E0B"

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">Late Delivery Rate</div>
                <div class="kpi-icon"
                     style="background:linear-gradient(135deg,{late_color},#F97316);">
                    !
                </div>
            </div>

            <div class="kpi-value">
                {late_rate:.1f}%
            </div>

            <div class="kpi-description">
                Orders delivered after estimate
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">Revenue performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Monthly commercial performance across the selected period</div>',
        unsafe_allow_html=True
    )

    monthly = (
        f.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["revenue"],
            mode="lines+markers",
            name="Revenue",
            line=dict(
                color=INDIGO,
                width=3
            ),
            marker=dict(
                size=7,
                color=PURPLE
            ),
            fill="tozeroy",
            fillcolor="rgba(91,92,226,0.10)"
        )
    )

    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(
            title="",
            showgrid=False
        ),
        yaxis=dict(
            title="Revenue",
            gridcolor="#EEF0F5"
        ),
        font=dict(
            color=DARK
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2 = st.columns(2)


    # ---------- CATEGORY ----------

    with c1:

        st.markdown(
            '<div class="section-title">Revenue by category</div>',
            unsafe_allow_html=True
        )

        cat = (
            f.groupby("category", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
            .head(8)
        )

        fig_cat = px.bar(
            cat.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            color="revenue",
            color_continuous_scale=[
                "#DDD6FE",
                "#8B5CF6",
                "#5B5CE2"
            ]
        )

        fig_cat.update_layout(
            height=390,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#EEF0F5"),
            yaxis=dict(title="")
        )

        st.plotly_chart(
            fig_cat,
            use_container_width=True
        )


    # ---------- REVENUE MIX ----------

    with c2:

        st.markdown(
            '<div class="section-title">Revenue mix</div>',
            unsafe_allow_html=True
        )

        mix = (
            f.groupby("category", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
            .head(6)
        )

        fig_pie = px.pie(
            mix,
            names="category",
            values="revenue",
            hole=0.62,
            color_discrete_sequence=CHART_COLORS
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        fig_pie.update_layout(
            height=390,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            legend=dict(
                orientation="h",
                y=-0.05
            )
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# =========================================================
# REVENUE INTELLIGENCE
# =========================================================

elif page == "Revenue Intelligence":

    monthly = (
        f.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )

    peak_row = monthly.loc[
        monthly["revenue"].idxmax()
    ]

    latest_growth = 0

    if len(monthly) >= 2:

        previous = monthly.iloc[-2]["revenue"]
        latest = monthly.iloc[-1]["revenue"]

        if previous != 0:
            latest_growth = (
                (latest - previous) / previous
            ) * 100


    a, b, c = st.columns(3)

    with a:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">🚀</div>
                <div class="insight-title">Peak Revenue Month</div>
                <div class="kpi-value">
                    R$ {peak_row["revenue"]:,.0f}
                </div>
                <div class="kpi-description">
                    {peak_row["month"].strftime("%b %Y")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">📈</div>
                <div class="insight-title">Latest Monthly Movement</div>
                <div class="kpi-value">
                    {latest_growth:+.1f}%
                </div>
                <div class="kpi-description">
                    Compared with previous month
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">💰</div>
                <div class="insight-title">Revenue per Order</div>
                <div class="kpi-value">
                    R$ {aov:,.0f}
                </div>
                <div class="kpi-description">
                    Average basket value
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section-title">Revenue trend</div>',
        unsafe_allow_html=True
    )

    fig = px.area(
        monthly,
        x="month",
        y="revenue",
        markers=True
    )

    fig.update_traces(
        line_color=INDIGO,
        fillcolor="rgba(91,92,226,0.13)"
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title="Revenue",
            gridcolor="#EEF0F5"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # TOP CATEGORIES

    cat_rev = (
        f.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    top5 = cat_rev.head(5)

    top5_share = (
        top5["revenue"].sum() / total_revenue * 100
        if total_revenue > 0
        else 0
    )


    st.markdown(
        f"""
        <div class="decision-card">
            <div class="decision-label">Revenue concentration</div>
            <div class="decision-title">
                Top 5 categories generate {top5_share:.1f}% of selected revenue
            </div>
            <div class="decision-text">
                Use this concentration signal to prioritize merchandising,
                inventory planning, promotional activity and category-level
                performance reviews.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">Category revenue ranking</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        cat_rev.head(10).sort_values("revenue"),
        x="revenue",
        y="category",
        orientation="h",
        color="revenue",
        color_continuous_scale=[
            "#DBEAFE",
            "#3B82F6",
            "#1D4ED8"
        ]
    )

    fig.update_layout(
        height=450,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#EEF0F5"),
        yaxis=dict(title="")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SALES & CATEGORIES
# =========================================================

elif page == "Sales & Categories":

    category = (
        f.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique")
        )
        .reset_index()
    )

    category["aov"] = (
        category["revenue"] /
        category["orders"]
    )

    category = category.sort_values(
        "revenue",
        ascending=False
    )


    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            category.head(10).sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            color="revenue",
            color_continuous_scale=[
                "#FDE68A",
                "#F59E0B",
                "#EA580C"
            ]
        )

        fig.update_layout(
            title="Top categories by revenue",
            height=450,
            coloraxis_showscale=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with c2:

        fig = px.scatter(
            category,
            x="orders",
            y="aov",
            size="revenue",
            color="revenue",
            hover_name="category",
            color_continuous_scale=[
                "#DDD6FE",
                "#8B5CF6",
                "#5B5CE2"
            ]
        )

        fig.update_layout(
            title="Order volume vs average order value",
            height=450,
            coloraxis_showscale=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(
                title="Orders",
                gridcolor="#EEF0F5"
            ),
            yaxis=dict(
                title="Average order value",
                gridcolor="#EEF0F5"
            ),
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown(
        '<div class="section-title">Category performance table</div>',
        unsafe_allow_html=True
    )

    display_category = category.copy()

    display_category["revenue"] = display_category["revenue"].map(
        lambda x: f"R$ {x:,.0f}"
    )

    display_category["aov"] = display_category["aov"].map(
        lambda x: f"R$ {x:,.0f}"
    )

    display_category["orders"] = display_category["orders"].map(
        lambda x: f"{x:,}"
    )

    display_category.columns = [
        "Category",
        "Revenue",
        "Orders",
        "AOV"
    ]

    st.dataframe(
        display_category,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DELIVERY OPERATIONS
# =========================================================

elif page == "Delivery Operations":

    st.markdown(
        '<div class="section-title">Delivery health</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Identify geographic delivery pressure and operational risk</div>',
        unsafe_allow_html=True
    )


    delivery = (
        orders_df
        .groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            late_rate=("is_late", "mean"),
            avg_delivery_days=("delivery_days", "mean")
        )
        .reset_index()
    )

    delivery = delivery[
        delivery["orders"] >= 100
    ].copy()

    delivery["late_rate"] *= 100

    delivery = delivery.sort_values(
        "late_rate",
        ascending=False
    )


    c1, c2 = st.columns(2)


    # WORST STATES

    with c1:

        worst = delivery.head(10)

        fig = px.bar(
            worst.sort_values("late_rate"),
            x="late_rate",
            y="customer_state",
            orientation="h",
            color="late_rate",
            color_continuous_scale=[
                "#FEE2E2",
                "#F87171",
                "#DC2626"
            ]
        )

        fig.update_layout(
            title="Highest late-delivery rates",
            height=440,
            coloraxis_showscale=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=10, r=10, t=50, b=10),
            xaxis=dict(
                title="Late delivery rate (%)",
                gridcolor="#EEF0F5"
            ),
            yaxis=dict(title="")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # DELIVERY RELATIONSHIP

    with c2:

        fig = px.scatter(
            delivery,
            x="avg_delivery_days",
            y="late_rate",
            size="orders",
            color="late_rate",
            hover_name="customer_state",
            color_continuous_scale=[
                "#DCFCE7",
                "#F59E0B",
                "#EF4444"
            ]
        )

        fig.update_layout(
            title="Delivery time vs late rate",
            height=440,
            coloraxis_showscale=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=10, r=10, t=50, b=10),
            xaxis=dict(
                title="Average delivery days",
                gridcolor="#EEF0F5"
            ),
            yaxis=dict(
                title="Late delivery rate (%)",
                gridcolor="#EEF0F5"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # HISTOGRAM

    st.markdown(
        '<div class="section-title">Delivery-time distribution</div>',
        unsafe_allow_html=True
    )

    fig = px.histogram(
        orders_df,
        x="delivery_days",
        nbins=35,
        color_discrete_sequence=[CYAN]
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(
            title="Delivery days",
            gridcolor="#EEF0F5"
        ),
        yaxis=dict(
            title="Orders",
            gridcolor="#EEF0F5"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # OPERATIONAL TABLE

    operational = delivery.copy()

    operational["late_rate"] = operational[
        "late_rate"
    ].map(lambda x: f"{x:.1f}%")

    operational["avg_delivery_days"] = operational[
        "avg_delivery_days"
    ].map(lambda x: f"{x:.1f}")

    operational["orders"] = operational[
        "orders"
    ].map(lambda x: f"{x:,}")

    operational.columns = [
        "State",
        "Orders",
        "Late rate",
        "Avg delivery days"
    ]

    st.dataframe(
        operational,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "Business Insights":

    category = (
        f.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    state = (
        f.groupby("customer_state")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    monthly = (
        f.groupby("month")["revenue"]
        .sum()
        .sort_values()
    )


    top_category = category.index[0]
    top_category_value = category.iloc[0]

    top_state = state.index[0]
    top_state_value = state.iloc[0]

    peak_month = monthly.idxmax()
    peak_month_value = monthly.max()


    st.markdown(
        """
        <div class="decision-card">
            <div class="decision-label">
                Executive decision center
            </div>

            <div class="decision-title">
                What should the business pay attention to?
            </div>

            <div class="decision-text">
                The dashboard connects revenue concentration,
                customer geography and delivery performance to help
                prioritize commercial and operational actions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">Key findings</div>',
        unsafe_allow_html=True
    )


    i1, i2, i3 = st.columns(3)


    with i1:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">🏆</div>

                <div class="insight-title">
                    Category leader
                </div>

                <div class="insight-text">
                    <b>{top_category}</b> is the highest-revenue
                    category in the selected dataset.

                    <br><br>

                    Revenue:
                    <b>R$ {top_category_value:,.0f}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with i2:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">🌎</div>

                <div class="insight-title">
                    Geographic leader
                </div>

                <div class="insight-text">
                    <b>{top_state}</b> contributes the largest
                    revenue amount among customer states.

                    <br><br>

                    Revenue:
                    <b>R$ {top_state_value:,.0f}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with i3:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">📅</div>

                <div class="insight-title">
                    Peak period
                </div>

                <div class="insight-text">
                    The strongest monthly revenue occurred in
                    <b>{peak_month.strftime("%B %Y")}</b>.

                    <br><br>

                    Revenue:
                    <b>R$ {peak_month_value:,.0f}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section-title">Recommended actions</div>',
        unsafe_allow_html=True
    )


    r1, r2, r3 = st.columns(3)


    with r1:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-icon">🎯</div>

                <div class="insight-title">
                    Protect revenue leaders
                </div>

                <div class="insight-text">
                    Prioritize high-performing categories with
                    inventory availability, merchandising and
                    targeted promotional planning.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with r2:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-icon">🚚</div>

                <div class="insight-title">
                    Investigate delivery risk
                </div>

                <div class="insight-text">
                    Focus operational reviews on states with
                    elevated late-delivery rates and longer
                    delivery times.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with r3:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-icon">📊</div>

                <div class="insight-title">
                    Monitor revenue concentration
                </div>

                <div class="insight-text">
                    Track category and geographic concentration
                    to identify dependency risk and potential
                    opportunities for diversification.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Olist Analytics • Revenue Intelligence Dashboard
        <br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
