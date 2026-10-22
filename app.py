import pandas as pd
import plotly.express as px
import streamlit as st

from data import load_data


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Olist Sales Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f6f7fb;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8eaf0;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    /* ---------- SIDEBAR ---------- */

    .sidebar-brand {
        padding: 0.4rem 0.2rem 1.4rem 0.2rem;
    }

    .sidebar-brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.02em;
    }

    .sidebar-brand-subtitle {
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }

    .sidebar-section {
        font-size: 0.72rem;
        font-weight: 800;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 55%,
            #312e81 100%
        );
        border-radius: 20px;
        padding: 2.1rem 2.3rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.12);
    }

    .hero-eyebrow {
        color: #a5b4fc;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        margin-bottom: 0.55rem;
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.25rem;
        line-height: 1.1;
        font-weight: 850;
        letter-spacing: -0.04em;
    }

    .hero-text {
        color: #d1d5db;
        font-size: 0.98rem;
        margin-top: 0.7rem;
        max-width: 720px;
        line-height: 1.55;
    }

    /* ---------- SECTION HEADERS ---------- */

    .section-title {
        font-size: 1.28rem;
        font-weight: 800;
        color: #111827;
        margin-top: 1.4rem;
        margin-bottom: 0.1rem;
        letter-spacing: -0.025em;
    }

    .section-subtitle {
        font-size: 0.82rem;
        color: #6b7280;
        margin-bottom: 0.85rem;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 16px;
        padding: 1.05rem 1.15rem;
        min-height: 122px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
    }

    .kpi-label {
        color: #6b7280;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.045em;
    }

    .kpi-value {
        color: #111827;
        font-size: 1.65rem;
        font-weight: 850;
        margin-top: 0.4rem;
        letter-spacing: -0.035em;
    }

    .kpi-note {
        color: #9ca3af;
        font-size: 0.73rem;
        margin-top: 0.3rem;
    }

    /* ---------- INSIGHT CARDS ---------- */

    .insight-card {
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        min-height: 155px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.035);
    }

    .insight-label {
        color: #6366f1;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.45rem;
    }

    .insight-title {
        color: #111827;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }

    .insight-text {
        color: #4b5563;
        font-size: 0.82rem;
        line-height: 1.55;
    }

    /* ---------- DECISION CARDS ---------- */

    .decision-card {
        background: #ffffff;
        border-left: 4px solid #6366f1;
        border-top: 1px solid #e8eaf0;
        border-right: 1px solid #e8eaf0;
        border-bottom: 1px solid #e8eaf0;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }

    .decision-title {
        color: #111827;
        font-size: 0.9rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .decision-text {
        color: #4b5563;
        font-size: 0.8rem;
        line-height: 1.5;
    }

    /* ---------- FILTER BOX ---------- */

    .filter-note {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.7rem 0.8rem;
        color: #6b7280;
        font-size: 0.74rem;
        line-height: 1.45;
        margin-top: 0.5rem;
    }

    /* ---------- TABLE ---------- */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.72rem;
        padding-top: 2.5rem;
        padding-bottom: 0.5rem;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .hero {
            padding: 1.5rem;
        }

        .hero-title {
            font-size: 1.7rem;
        }

        .hero-text {
            font-size: 0.88rem;
        }

        .kpi-value {
            font-size: 1.35rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def money(value):
    if pd.isna(value):
        return "R$0"
    return f"R${value:,.0f}"


def money_decimal(value):
    if pd.isna(value):
        return "R$0.00"
    return f"R${value:,.2f}"


def number(value):
    if pd.isna(value):
        return "0"
    return f"{int(value):,}"


def percentage(value):
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"


def safe_divide(a, b):
    if b == 0:
        return 0
    return a / b


def show_kpi(label, value, note=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_decision(title, text):
    st.markdown(
        f"""
        <div class="decision-card">
            <div class="decision-title">{title}</div>
            <div class="decision-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_insight(label, title, text):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">{label}</div>
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial, sans-serif",
            color="#374151",
        ),
        title_font=dict(
            size=15,
            color="#111827",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#e5e7eb",
    )

    fig.update_yaxes(
        gridcolor="#eef0f4",
        zeroline=False,
    )

    return fig


# =========================================================
# LOAD DATA
# =========================================================

try:
    df = load_data()
except Exception as e:
    st.error("The dashboard could not load the data.")
    st.exception(e)
    st.stop()


# =========================================================
# VALIDATE DATA
# =========================================================

required_columns = [
    "order_id",
    "month",
    "customer_state",
    "category",
    "revenue",
    "freight_value",
    "delivery_days",
    "is_late",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# =========================================================
# CLEAN DATA
# =========================================================

df = df.copy()

df["month"] = pd.to_datetime(df["month"], errors="coerce")

df["revenue"] = pd.to_numeric(
    df["revenue"],
    errors="coerce",
).fillna(0)

df["freight_value"] = pd.to_numeric(
    df["freight_value"],
    errors="coerce",
).fillna(0)

df["delivery_days"] = pd.to_numeric(
    df["delivery_days"],
    errors="coerce",
)

df["is_late"] = pd.to_numeric(
    df["is_late"],
    errors="coerce",
).fillna(0)

df["customer_state"] = (
    df["customer_state"]
    .fillna("Unknown")
    .astype(str)
)

df["category"] = (
    df["category"]
    .fillna("Unknown")
    .astype(str)
)

df = df.dropna(subset=["month"])


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">
                📊 Olist Sales Insights
            </div>
            <div class="sidebar-brand-subtitle">
                Revenue & Sales Analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Dashboard</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Revenue Insights",
            "Sales & Categories",
            "Delivery Operations",
            "Business Insights",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-section">Filters</div>',
        unsafe_allow_html=True,
    )

    min_month = df["month"].min().date()
    max_month = df["month"].max().date()

    selected_dates = st.date_input(
        "Business period",
        value=(min_month, max_month),
        min_value=min_month,
        max_value=max_month,
    )

    states = sorted(
        df["customer_state"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_states = st.multiselect(
        "Customer states",
        options=states,
        default=[],
    )

    categories = sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        "Product categories",
        options=categories,
        default=[],
    )

    st.markdown(
        """
        <div class="filter-note">
            Filters apply across the dashboard.
            Leave a filter empty to include all values.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = (
        pd.Timestamp(selected_dates[1])
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )

    filtered_df = filtered_df[
        (filtered_df["month"] >= start_date)
        & (filtered_df["month"] <= end_date)
    ]

if selected_states:
    filtered_df = filtered_df[
        filtered_df["customer_state"].isin(selected_states)
    ]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]


if filtered_df.empty:
    st.warning(
        "No data is available for the selected filters. "
        "Please widen the filters."
    )
    st.stop()


# =========================================================
# COMMON METRICS
# =========================================================

total_revenue = filtered_df["revenue"].sum()

total_orders = filtered_df["order_id"].nunique()

aov = safe_divide(
    total_revenue,
    total_orders,
)

late_rate = (
    filtered_df["is_late"].mean() * 100
)

avg_delivery = (
    filtered_df["delivery_days"]
    .dropna()
    .mean()
)

late_orders = filtered_df.loc[
    filtered_df["is_late"] == 1,
    "order_id",
].nunique()

late_revenue = filtered_df.loc[
    filtered_df["is_late"] == 1,
    "revenue",
].sum()


# =========================================================
# HERO
# =========================================================

st.markdown(
    "### SALES ANALYTICS DASHBOARD"
)

st.title("Olist Sales Insights")

st.caption(
    "Turning transactional e-commerce data into actionable "
    "revenue, sales and operational insights."
)

st.divider()
# =========================================================
# PAGE 1 — OVERVIEW
# =========================================================

def page_overview():

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'A high-level view of revenue, order activity and delivery performance.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- KPI ROW ----------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_kpi(
            "Total Revenue",
            money(total_revenue),
            "Selected business period",
        )

    with c2:
        show_kpi(
            "Orders",
            number(total_orders),
            "Unique delivered orders",
        )

    with c3:
        show_kpi(
            "Average Order Value",
            money_decimal(aov),
            "Revenue per order",
        )

    with c4:
        show_kpi(
            "Late Delivery Rate",
            percentage(late_rate),
            "Orders delivered after estimate",
        )

    # ---------- REVENUE TREND ----------

    st.markdown(
        '<div class="section-title">Revenue Performance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Monthly revenue trend across the selected period.'
        '</div>',
        unsafe_allow_html=True,
    )

    monthly = (
        filtered_df
        .groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("month")
    )

    monthly["aov"] = (
        monthly["revenue"]
        / monthly["orders"]
    )

    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue",
    )

    fig.update_traces(
        line_width=3,
        hovertemplate=(
            "%{x|%b %Y}<br>"
            "Revenue: R$%{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig = chart_layout(fig, 410)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ---------- ORDERS + AOV ----------

    c1, c2 = st.columns(2)

    with c1:

        fig_orders = px.bar(
            monthly,
            x="month",
            y="orders",
            title="Monthly Order Volume",
        )

        fig_orders.update_traces(
            hovertemplate=(
                "%{x|%b %Y}<br>"
                "Orders: %{y:,}"
                "<extra></extra>"
            ),
        )

        fig_orders = chart_layout(
            fig_orders,
            360,
        )

        st.plotly_chart(
            fig_orders,
            use_container_width=True,
        )

    with c2:

        fig_aov = px.line(
            monthly,
            x="month",
            y="aov",
            markers=True,
            title="Average Order Value",
        )

        fig_aov.update_traces(
            line_width=3,
            hovertemplate=(
                "%{x|%b %Y}<br>"
                "AOV: R$%{y:,.2f}"
                "<extra></extra>"
            ),
        )

        fig_aov = chart_layout(
            fig_aov,
            360,
        )

        st.plotly_chart(
            fig_aov,
            use_container_width=True,
        )

    # ---------- QUICK BUSINESS READ ----------

    st.markdown(
        '<div class="section-title">Quick Business Read</div>',
        unsafe_allow_html=True,
    )

    strongest_month = (
        monthly.loc[
            monthly["revenue"].idxmax(),
            "month",
        ]
        if not monthly.empty
        else None
    )

    strongest_month_revenue = (
        monthly["revenue"].max()
        if not monthly.empty
        else 0
    )

    strongest_month_name = (
        strongest_month.strftime("%B %Y")
        if pd.notna(strongest_month)
        else "N/A"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        show_insight(
            "Revenue",
            "Strongest month",
            f"{strongest_month_name} generated "
            f"{money(strongest_month_revenue)} in revenue.",
        )

    with c2:
        show_insight(
            "Operations",
            "Delivery exposure",
            f"{percentage(late_rate)} of delivered orders "
            f"were completed after the estimated delivery date.",
        )

    with c3:
        show_insight(
            "Commercial",
            "Order economics",
            f"The average order generated "
            f"{money_decimal(aov)} in item revenue.",
        )


# =========================================================
# PAGE 2 — REVENUE INSIGHTS
# =========================================================

def page_revenue():

    st.markdown(
        '<div class="section-title">Revenue Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Understand revenue momentum, market concentration and geographic performance.'
        '</div>',
        unsafe_allow_html=True,
    )

    monthly = (
        filtered_df
        .groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("month")
    )

    monthly["mom_growth"] = (
        monthly["revenue"]
        .pct_change()
        * 100
    )

    # ---------- MONTHLY REVENUE ----------

    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Revenue Trend",
    )

    fig.update_traces(
        line_width=3,
        hovertemplate=(
            "%{x|%b %Y}<br>"
            "Revenue: R$%{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig = chart_layout(fig, 390)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ---------- MOM TABLE ----------

    st.markdown(
        '<div class="section-title">Monthly Growth</div>',
        unsafe_allow_html=True,
    )

    growth_display = monthly.copy()

    growth_display["month"] = (
        growth_display["month"]
        .dt.strftime("%b %Y")
    )

    growth_display["Revenue"] = (
        growth_display["revenue"]
        .map(money)
    )

    growth_display["Orders"] = (
        growth_display["orders"]
        .map(number)
    )

    growth_display["MoM Growth"] = (
        growth_display["mom_growth"]
        .map(percentage)
    )

    growth_display = growth_display[
        [
            "month",
            "Revenue",
            "Orders",
            "MoM Growth",
        ]
    ].rename(
        columns={
            "month": "Month",
        }
    )

    st.dataframe(
        growth_display,
        use_container_width=True,
        hide_index=True,
    )

    # ---------- STATES ----------

    st.markdown(
        '<div class="section-title">Geographic Revenue Performance</div>',
        unsafe_allow_html=True,
    )

    state_perf = (
        filtered_df
        .groupby("customer_state", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values(
            "revenue",
            ascending=False,
        )
    )

    state_perf["aov"] = (
        state_perf["revenue"]
        / state_perf["orders"]
    )

    c1, c2 = st.columns(2)

    with c1:

        top_states = state_perf.head(10)

        fig_states = px.bar(
            top_states.sort_values("revenue"),
            x="revenue",
            y="customer_state",
            orientation="h",
            title="Top States by Revenue",
        )

        fig_states.update_traces(
            hovertemplate=(
                "%{y}<br>"
                "Revenue: R$%{x:,.0f}"
                "<extra></extra>"
            ),
        )

        fig_states = chart_layout(
            fig_states,
            420,
        )

        st.plotly_chart(
            fig_states,
            use_container_width=True,
        )

    with c2:

        state_table = state_perf.head(10).copy()

        state_table["Revenue"] = (
            state_table["revenue"]
            .map(money)
        )

        state_table["Orders"] = (
            state_table["orders"]
            .map(number)
        )

        state_table["AOV"] = (
            state_table["aov"]
            .map(money_decimal)
        )

        state_table = state_table[
            [
                "customer_state",
                "Revenue",
                "Orders",
                "AOV",
            ]
        ].rename(
            columns={
                "customer_state": "State",
            }
        )

        st.dataframe(
            state_table,
            use_container_width=True,
            hide_index=True,
        )

    # ---------- CONCENTRATION ----------

    st.markdown(
        '<div class="section-title">Revenue Concentration</div>',
        unsafe_allow_html=True,
    )

    category_revenue = (
        filtered_df
        .groupby("category")["revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    category_total = category_revenue.sum()

    top5_share = safe_divide(
        category_revenue.head(5).sum(),
        category_total,
    ) * 100

    top10_share = safe_divide(
        category_revenue.head(10).sum(),
        category_total,
    ) * 100

    active_categories = (
        category_revenue
        .index
        .nunique()
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        show_kpi(
            "Top 5 Category Share",
            percentage(top5_share),
            "Share of total revenue",
        )

    with c2:
        show_kpi(
            "Top 10 Category Share",
            percentage(top10_share),
            "Share of total revenue",
        )

    with c3:
        show_kpi(
            "Active Categories",
            number(active_categories),
            "Categories generating revenue",
        )


# =========================================================
# PAGE 3 — SALES & CATEGORIES
# =========================================================

def page_sales_categories():

    st.markdown(
        '<div class="section-title">Sales & Category Performance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Identify high-value categories, volume leaders and revenue opportunities.'
        '</div>',
        unsafe_allow_html=True,
    )

    category_perf = (
        filtered_df
        .groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
    )

    category_perf["aov"] = (
        category_perf["revenue"]
        / category_perf["orders"]
    )

    category_perf = category_perf.sort_values(
        "revenue",
        ascending=False,
    )

    # ---------- TOP CATEGORIES ----------

    c1, c2 = st.columns(2)

    with c1:

        top_revenue = category_perf.head(10)

        fig = px.bar(
            top_revenue.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            title="Top Categories by Revenue",
        )

        fig.update_traces(
            hovertemplate=(
                "%{y}<br>"
                "Revenue: R$%{x:,.0f}"
                "<extra></extra>"
            ),
        )

        fig = chart_layout(fig, 440)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with c2:

        top_orders = (
            category_perf
            .sort_values(
                "orders",
                ascending=False,
            )
            .head(10)
        )

        fig = px.bar(
            top_orders.sort_values("orders"),
            x="orders",
            y="category",
            orientation="h",
            title="Top Categories by Order Volume",
        )

        fig.update_traces(
            hovertemplate=(
                "%{y}<br>"
                "Orders: %{x:,}"
                "<extra></extra>"
            ),
        )

        fig = chart_layout(fig, 440)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # ---------- REVENUE VS VOLUME ----------

    st.markdown(
        '<div class="section-title">Revenue vs Order Volume</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Categories above the trend are relatively stronger revenue contributors.'
        '</div>',
        unsafe_allow_html=True,
    )

    scatter = px.scatter(
        category_perf,
        x="orders",
        y="revenue",
        size="aov",
        hover_name="category",
        title="Category Revenue vs Order Volume",
    )

    scatter.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Orders: %{x:,}<br>"
            "Revenue: R$%{y:,.0f}"
            "<extra></extra>"
        ),
    )

    scatter = chart_layout(
        scatter,
        470,
    )

    st.plotly_chart(
        scatter,
        use_container_width=True,
    )

    # ---------- CATEGORY TABLE ----------

    st.markdown(
        '<div class="section-title">Category Performance Matrix</div>',
        unsafe_allow_html=True,
    )

    table = category_perf.copy()

    table["Revenue"] = table["revenue"].map(money)
    table["Orders"] = table["orders"].map(number)
    table["AOV"] = table["aov"].map(money_decimal)

    table = table[
        [
            "category",
            "Revenue",
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
    )

    # ---------- CATEGORY INSIGHTS ----------

    if not category_perf.empty:

        leading_category = category_perf.iloc[0]

        volume_category = (
            category_perf
            .sort_values(
                "orders",
                ascending=False,
            )
            .iloc[0]
        )

        high_aov_category = (
            category_perf
            .sort_values(
                "aov",
                ascending=False,
            )
            .iloc[0]
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            show_insight(
                "Revenue Leader",
                leading_category["category"],
                f"Generated {money(leading_category['revenue'])} "
                f"in revenue.",
            )

        with c2:
            show_insight(
                "Volume Leader",
                volume_category["category"],
                f"Generated {number(volume_category['orders'])} "
                f"unique orders.",
            )

        with c3:
            show_insight(
                "AOV Leader",
                high_aov_category["category"],
                f"Average order value of "
                f"{money_decimal(high_aov_category['aov'])}.",
            )


# =========================================================
# PAGE 4 — DELIVERY OPERATIONS
# =========================================================

def page_delivery():

    st.markdown(
        '<div class="section-title">Delivery Operations</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Measure delivery reliability and understand where operational risk affects sales.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- KPI ROW ----------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_kpi(
            "Late Delivery Rate",
            percentage(late_rate),
            "Share of delivered orders",
        )

    with c2:
        show_kpi(
            "Late Orders",
            number(late_orders),
            "Unique orders delivered late",
        )

    with c3:
        show_kpi(
            "Revenue in Late Orders",
            money(late_revenue),
            "Item revenue associated with late orders",
        )

    with c4:
        show_kpi(
            "Average Delivery",
            f"{avg_delivery:.1f} days",
            "Purchase to delivery",
        )

    # ---------- ON TIME VS LATE ----------

    status_df = pd.DataFrame(
        {
            "Delivery Status": [
                "On Time",
                "Late",
            ],
            "Orders": [
                filtered_df.loc[
                    filtered_df["is_late"] == 0,
                    "order_id",
                ].nunique(),
                late_orders,
            ],
        }
    )

    fig = px.bar(
        status_df,
        x="Delivery Status",
        y="Orders",
        title="On-Time vs Late Orders",
    )

    fig.update_traces(
        hovertemplate=(
            "%{x}<br>"
            "Orders: %{y:,}"
            "<extra></extra>"
        ),
    )

    fig = chart_layout(
        fig,
        360,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ---------- DELIVERY DISTRIBUTION ----------

    st.markdown(
        '<div class="section-title">Delivery Time Distribution</div>',
        unsafe_allow_html=True,
    )

    delivery_data = filtered_df[
        filtered_df["delivery_days"].notna()
        & (filtered_df["delivery_days"] >= 0)
    ].copy()

    fig = px.histogram(
        delivery_data,
        x="delivery_days",
        nbins=40,
        title="Days from Purchase to Delivery",
    )

    fig.update_traces(
        hovertemplate=(
            "Delivery Days: %{x}<br>"
            "Orders: %{y:,}"
            "<extra></extra>"
        ),
    )

    fig = chart_layout(
        fig,
        380,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ---------- STATE RISK ----------

    st.markdown(
        '<div class="section-title">Geographic Delivery Risk</div>',
        unsafe_allow_html=True,
    )

    state_delivery = (
        filtered_df
        .groupby("customer_state", as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            late_rate=("is_late", "mean"),
            avg_delivery=("delivery_days", "mean"),
            revenue=("revenue", "sum"),
        )
    )

    state_delivery["late_rate"] *= 100

    state_delivery = state_delivery[
        state_delivery["orders"] >= 100
    ].sort_values(
        "late_rate",
        ascending=False,
    )

    if not state_delivery.empty:

        fig = px.bar(
            state_delivery.head(10).sort_values("late_rate"),
            x="late_rate",
            y="customer_state",
            orientation="h",
            title="States with Highest Late-Delivery Rate",
        )

        fig.update_traces(
            hovertemplate=(
                "%{y}<br>"
                "Late Rate: %{x:.1f}%"
                "<extra></extra>"
            ),
        )

        fig = chart_layout(
            fig,
            420,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        risk_table = state_delivery.head(10).copy()

        risk_table["Late Rate"] = (
            risk_table["late_rate"]
            .map(percentage)
        )

        risk_table["Orders"] = (
            risk_table["orders"]
            .map(number)
        )

        risk_table["Avg Delivery"] = (
            risk_table["avg_delivery"]
            .map(lambda x: f"{x:.1f} days")
        )

        risk_table["Revenue"] = (
            risk_table["revenue"]
            .map(money)
        )

        risk_table = risk_table[
            [
                "customer_state",
                "Late Rate",
                "Orders",
                "Avg Delivery",
                "Revenue",
            ]
        ].rename(
            columns={
                "customer_state": "State",
            }
        )

        st.dataframe(
            risk_table,
            use_container_width=True,
            hide_index=True,
        )

    # ---------- REVIEWS ----------

    if "review_score" in filtered_df.columns:

        review_df = filtered_df.copy()

        review_df["Delivery Status"] = (
            review_df["is_late"]
            .map(
                {
                    0: "On Time",
                    1: "Late",
                }
            )
        )

        review_summary = (
            review_df
            .dropna(subset=["review_score"])
            .groupby("Delivery Status", as_index=False)
            ["review_score"]
            .mean()
        )

        if not review_summary.empty:

            st.markdown(
                '<div class="section-title">'
                'Delivery Performance & Customer Reviews'
                '</div>',
                unsafe_allow_html=True,
            )

            fig = px.bar(
                review_summary,
                x="Delivery Status",
                y="review_score",
                title="Average Review Score by Delivery Status",
            )

            fig.update_yaxes(
                range=[0, 5],
            )

            fig.update_traces(
                hovertemplate=(
                    "%{x}<br>"
                    "Average Review: %{y:.2f}"
                    "<extra></extra>"
                ),
            )

            fig = chart_layout(
                fig,
                350,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


# =========================================================
# PAGE 5 — BUSINESS INSIGHTS
# =========================================================

def page_business_insights():

    st.markdown(
        '<div class="section-title">Business Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Translate dashboard findings into commercial and operational actions.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- CORE ANALYSIS ----------

    monthly = (
        filtered_df
        .groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("month")
    )

    category_perf = (
        filtered_df
        .groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
    )

    category_perf["aov"] = (
        category_perf["revenue"]
        / category_perf["orders"]
    )

    category_perf = category_perf.sort_values(
        "revenue",
        ascending=False,
    )

    strongest_month_name = "N/A"
    strongest_month_revenue = 0

    if not monthly.empty:

        strongest_month = monthly.loc[
            monthly["revenue"].idxmax()
        ]

        strongest_month_name = (
            strongest_month["month"]
            .strftime("%B %Y")
        )

        strongest_month_revenue = (
            strongest_month["revenue"]
        )

    leading_category = "N/A"
    leading_category_revenue = 0

    if not category_perf.empty:

        leading_category = (
            category_perf.iloc[0]["category"]
        )

        leading_category_revenue = (
            category_perf.iloc[0]["revenue"]
        )

    category_revenue = (
        filtered_df
        .groupby("category")["revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top5_share = safe_divide(
        category_revenue.head(5).sum(),
        category_revenue.sum(),
    ) * 100

    # ---------- EXECUTIVE READOUT ----------

    st.markdown(
        '<div class="section-title">Executive Readout</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">EXECUTIVE SUMMARY</div>
            <div class="insight-title">
                Revenue performance is being driven by a focused group of categories and markets.
            </div>
            <div class="insight-text">
                The selected business period generated
                <b>{money(total_revenue)}</b> across
                <b>{number(total_orders)}</b> delivered orders,
                with an average order value of
                <b>{money_decimal(aov)}</b>.
                {strongest_month_name} recorded the strongest monthly
                revenue performance, while
                <b>{leading_category}</b> emerged as the leading
                category by revenue.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    # ---------- THREE MAIN INSIGHTS ----------

    c1, c2, c3 = st.columns(3)

    with c1:
        show_insight(
            "Revenue Momentum",
            strongest_month_name,
            f"The strongest month generated "
            f"{money(strongest_month_revenue)}. "
            f"This period can be used as a benchmark "
            f"for future commercial planning.",
        )

    with c2:
        show_insight(
            "Category Leadership",
            leading_category,
            f"The leading category contributed "
            f"{money(leading_category_revenue)} "
            f"in item revenue.",
        )

    with c3:
        show_insight(
            "Revenue Concentration",
            f"{top5_share:.1f}% in Top 5",
            "A concentrated revenue base means "
            "high-performing categories should be "
            "protected while emerging categories are developed.",
        )

    # ---------- DECISION CENTER ----------

    st.markdown(
        '<div class="section-title">Decision Center</div>',
        unsafe_allow_html=True,
    )

    show_decision(
        "1. Protect high-performing categories",
        f"{leading_category} is currently the leading revenue category. "
        "Maintain availability, pricing discipline and promotional visibility "
        "for high-contribution categories.",
    )

    show_decision(
        "2. Increase revenue per order",
        f"The current average order value is {money_decimal(aov)}. "
        "Cross-selling, bundles and stronger product combinations can "
        "increase revenue without relying only on additional order volume.",
    )

    show_decision(
        "3. Monitor delivery risk",
        f"{percentage(late_rate)} of delivered orders were late. "
        "States with persistently high late-delivery rates should be "
        "prioritized for logistics and fulfillment review.",
    )

    show_decision(
        "4. Reduce revenue concentration risk",
        f"The top five categories account for approximately "
        f"{top5_share:.1f}% of revenue. "
        "The business should protect these categories while building "
        "growth in promising lower-contribution categories.",
    )

    show_decision(
        "5. Use peak periods as planning benchmarks",
        f"{strongest_month_name} delivered the strongest monthly revenue. "
        "Understanding the category and order mix behind this period "
        "can improve future inventory and promotional planning.",
    )

    # ---------- MANAGEMENT PRIORITIES ----------

    st.markdown(
        '<div class="section-title">Management Priorities</div>',
        unsafe_allow_html=True,
    )

    priorities = pd.DataFrame(
        {
            "Priority": [
                "Revenue Growth",
                "Order Economics",
                "Delivery Reliability",
                "Category Strategy",
            ],
            "What to Monitor": [
                "Monthly revenue and growth",
                "AOV and high-value orders",
                "Late-delivery rate by state",
                "Revenue contribution by category",
            ],
            "Recommended Action": [
                "Replicate patterns from strongest periods",
                "Use bundles and cross-selling",
                "Investigate high-risk states",
                "Protect leaders and develop emerging categories",
            ],
        }
    )

    st.dataframe(
        priorities,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# PAGE ROUTING
# =========================================================

if page == "Overview":
    page_overview()

elif page == "Revenue Insights":
    page_revenue()

elif page == "Sales & Categories":
    page_sales_categories()

elif page == "Delivery Operations":
    page_delivery()

elif page == "Business Insights":
    page_business_insights()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Olist Sales Insights · Revenue & Sales Analytics
        <br>
        Built with Python · Pandas · Plotly · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
