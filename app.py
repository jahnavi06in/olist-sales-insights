import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Olist Sales Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f7f8fc;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, p, span, div {
        font-family: Inter, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8eaf0;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 55%,
            #312e81 100%
        );

        border-radius: 24px;
        padding: 38px 42px;
        margin-bottom: 28px;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.12);
    }

    .hero-eyebrow {
        color: #a5b4fc;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: white;
        font-size: 38px;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 10px;
    }

    .hero-text {
        color: #d1d5db;
        font-size: 16px;
        line-height: 1.6;
        max-width: 720px;
    }

    /* ---------- SECTION HEADER ---------- */

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #111827;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* ---------- KPI ---------- */

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 18px;
        padding: 22px;
        min-height: 130px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.045);
    }

    .kpi-label {
        color: #6b7280;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.2;
    }

    .kpi-note {
        color: #9ca3af;
        font-size: 12px;
        margin-top: 7px;
    }

    /* ---------- INSIGHT CARDS ---------- */

    .insight-card {
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
    }

    .insight-title {
        color: #111827;
        font-size: 16px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .insight-text {
        color: #4b5563;
        font-size: 14px;
        line-height: 1.65;
    }

    /* ---------- DECISION CARDS ---------- */

    .decision-card {
        background: #ffffff;
        border-left: 4px solid #4f46e5;
        border-top: 1px solid #e8eaf0;
        border-right: 1px solid #e8eaf0;
        border-bottom: 1px solid #e8eaf0;
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 14px;
    }

    .decision-title {
        color: #111827;
        font-size: 16px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .decision-text {
        color: #4b5563;
        font-size: 14px;
        line-height: 1.65;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        padding-top: 35px;
        padding-bottom: 10px;
    }

    /* ---------- DATAFRAME ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .hero {
            padding: 28px 24px;
        }

        .hero-title {
            font-size: 30px;
        }

        .hero-text {
            font-size: 14px;
        }

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

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
    if b == 0 or pd.isna(b):
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


def chart_layout(fig, height=420):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#374151",
        ),
        title_font=dict(
            size=17,
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
            font_size=13,
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


# ============================================================
# LOAD DATA
# ============================================================

try:
    from data import load_data

    df = load_data().copy()

except Exception as e:
    st.error("Unable to load the Olist dataset.")
    st.code(str(e))
    st.stop()


# ============================================================
# VALIDATE DATA
# ============================================================

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
    st.error("Required columns are missing from the dataset.")
    st.write(missing_columns)
    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

df["month"] = pd.to_datetime(df["month"], errors="coerce")

df["revenue"] = pd.to_numeric(
    df["revenue"],
    errors="coerce"
).fillna(0)

df["freight_value"] = pd.to_numeric(
    df["freight_value"],
    errors="coerce"
).fillna(0)

df["delivery_days"] = pd.to_numeric(
    df["delivery_days"],
    errors="coerce"
)

df["is_late"] = pd.to_numeric(
    df["is_late"],
    errors="coerce"
).fillna(0)

df["category"] = (
    df["category"]
    .fillna("Unknown")
    .astype(str)
    .str.replace("_", " ", regex=False)
    .str.title()
)

df["customer_state"] = (
    df["customer_state"]
    .fillna("Unknown")
    .astype(str)
    .str.upper()
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:800;
            color:#111827;
            margin-bottom:4px;
        ">
            📊 Olist Sales Insights
        </div>

        <div style="
            color:#6b7280;
            font-size:13px;
            margin-bottom:25px;
        ">
            Revenue & Sales Analytics
        </div>
        """,
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
    )

    st.divider()

    st.markdown("### Filters")

    min_date = df["month"].min()
    max_date = df["month"].max()

    selected_dates = st.date_input(
        "Business period",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

        start_date = pd.Timestamp(selected_dates[0])
        end_date = pd.Timestamp(selected_dates[1])

    else:

        start_date = min_date
        end_date = max_date

    states = sorted(df["customer_state"].dropna().unique())

    selected_states = st.multiselect(
        "Customer states",
        states,
        default=states,
    )

    categories = sorted(df["category"].dropna().unique())

    selected_categories = st.multiselect(
        "Product categories",
        categories,
        default=categories,
    )

    st.divider()

    st.caption(
        "Olist Brazilian E-Commerce Dataset"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["month"] >= start_date)
    & (df["month"] <= end_date)
    & (df["customer_state"].isin(selected_states))
    & (df["category"].isin(selected_categories))
].copy()


# ============================================================
# EMPTY STATE
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data matches the selected filters. "
        "Please widen the business period or select more categories/states."
    )

    st.stop()


# ============================================================
# COMMON METRICS
# ============================================================

total_revenue = filtered_df["revenue"].sum()

total_orders = filtered_df["order_id"].nunique()

total_customers = filtered_df["customer_state"].shape[0]

aov = safe_divide(
    total_revenue,
    total_orders,
)

late_rate = filtered_df["is_late"].mean() * 100

avg_delivery = filtered_df["delivery_days"].mean()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            SALES ANALYTICS DASHBOARD
        </div>

        <div class="hero-title">
            Olist Sales Insights
        </div>

        <div class="hero-text">
            Turning transactional e-commerce data into
            actionable revenue, sales and operational insights.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PAGE: OVERVIEW
# ============================================================

def page_overview():

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'A high-level view of revenue performance, order activity and operational health.'
        '</div>',
        unsafe_allow_html=True,
    )

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

    st.markdown("")

    # Monthly revenue

    monthly = (
        filtered_df
        .groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("month")
    )

    monthly["aov"] = monthly.apply(
        lambda row: safe_divide(
            row["revenue"],
            row["orders"],
        ),
        axis=1,
    )

    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
        labels={
            "month": "",
            "revenue": "Revenue",
        },
    )

    fig.update_traces(
        hovertemplate="Revenue: R$%{y:,.0f}<extra></extra>"
    )

    st.plotly_chart(
        chart_layout(fig, 430),
        use_container_width=True,
    )

    c1, c2 = st.columns(2)

    # Orders trend

    with c1:

        fig_orders = px.bar(
            monthly,
            x="month",
            y="orders",
            title="Monthly Order Volume",
            labels={
                "month": "",
                "orders": "Orders",
            },
        )

        st.plotly_chart(
            chart_layout(fig_orders, 380),
            use_container_width=True,
        )

    # AOV trend

    with c2:

        fig_aov = px.line(
            monthly,
            x="month",
            y="aov",
            markers=True,
            title="Average Order Value Trend",
            labels={
                "month": "",
                "aov": "AOV",
            },
        )

        fig_aov.update_traces(
            hovertemplate="AOV: R$%{y:,.2f}<extra></extra>"
        )

        st.plotly_chart(
            chart_layout(fig_aov, 380),
            use_container_width=True,
        )


# ============================================================
# PAGE: REVENUE
# ============================================================

def page_revenue():

    st.markdown(
        '<div class="section-title">Revenue Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Understand where revenue comes from, how it changes over time and where concentration exists.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Monthly revenue

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
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
        * 100
    )

    fig = px.bar(
        monthly,
        x="month",
        y="revenue",
        title="Monthly Revenue",
        labels={
            "month": "",
            "revenue": "Revenue",
        },
    )

    fig.update_traces(
        hovertemplate="Revenue: R$%{y:,.0f}<extra></extra>"
    )

    st.plotly_chart(
        chart_layout(fig, 430),
        use_container_width=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        fig_growth = px.line(
            monthly,
            x="month",
            y="mom_growth",
            markers=True,
            title="Month-over-Month Revenue Growth",
            labels={
                "month": "",
                "mom_growth": "Growth %",
            },
        )

        fig_growth.add_hline(
            y=0,
            line_width=1,
        )

        fig_growth.update_traces(
            hovertemplate="Growth: %{y:.1f}%<extra></extra>"
        )

        st.plotly_chart(
            chart_layout(fig_growth, 380),
            use_container_width=True,
        )

    with c2:

        # State revenue

        state_revenue = (
            filtered_df
            .groupby("customer_state", as_index=False)
            ["revenue"]
            .sum()
            .sort_values(
                "revenue",
                ascending=False,
            )
            .head(10)
        )

        fig_state = px.bar(
            state_revenue,
            x="revenue",
            y="customer_state",
            orientation="h",
            title="Top States by Revenue",
            labels={
                "revenue": "Revenue",
                "customer_state": "",
            },
        )

        fig_state.update_layout(
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            chart_layout(fig_state, 380),
            use_container_width=True,
        )

    # Revenue concentration

    st.markdown(
        '<div class="section-title">Revenue Concentration</div>',
        unsafe_allow_html=True,
    )

    category_revenue = (
        filtered_df
        .groupby("category", as_index=False)
        ["revenue"]
        .sum()
        .sort_values(
            "revenue",
            ascending=False,
        )
    )

    total_category_revenue = category_revenue["revenue"].sum()

    top5_share = safe_divide(
        category_revenue.head(5)["revenue"].sum(),
        total_category_revenue,
    ) * 100

    top10_share = safe_divide(
        category_revenue.head(10)["revenue"].sum(),
        total_category_revenue,
    ) * 100

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
            number(category_revenue.shape[0]),
            "Categories in selection",
        )


# ============================================================
# PAGE: SALES & CATEGORIES
# ============================================================

def page_sales_categories():

    st.markdown(
        '<div class="section-title">Sales & Category Performance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Identify revenue leaders, high-volume categories and opportunities to improve order value.'
        '</div>',
        unsafe_allow_html=True,
    )

    category = (
        filtered_df
        .groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    category["aov"] = category.apply(
        lambda row: safe_divide(
            row["revenue"],
            row["orders"],
        ),
        axis=1,
    )

    category = category.sort_values(
        "revenue",
        ascending=False,
    )

    c1, c2 = st.columns(2)

    with c1:

        top_categories = category.head(12).sort_values(
            "revenue"
        )

        fig = px.bar(
            top_categories,
            x="revenue",
            y="category",
            orientation="h",
            title="Top Categories by Revenue",
            labels={
                "revenue": "Revenue",
                "category": "",
            },
        )

        st.plotly_chart(
            chart_layout(fig, 500),
            use_container_width=True,
        )

    with c2:

        volume_categories = (
            category
            .sort_values("orders", ascending=False)
            .head(12)
            .sort_values("orders")
        )

        fig = px.bar(
            volume_categories,
            x="orders",
            y="category",
            orientation="h",
            title="Top Categories by Order Volume",
            labels={
                "orders": "Orders",
                "category": "",
            },
        )

        st.plotly_chart(
            chart_layout(fig, 500),
            use_container_width=True,
        )

    # Category matrix

    st.markdown(
        '<div class="section-title">Category Performance Matrix</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Revenue versus order volume helps separate category leaders from value-growth opportunities.'
        '</div>',
        unsafe_allow_html=True,
    )

    fig_matrix = px.scatter(
        category,
        x="orders",
        y="revenue",
        size="aov",
        hover_name="category",
        title="Revenue vs Order Volume",
        labels={
            "orders": "Orders",
            "revenue": "Revenue",
            "aov": "AOV",
        },
    )

    st.plotly_chart(
        chart_layout(fig_matrix, 500),
        use_container_width=True,
    )

    # Opportunity table

    category_display = category.copy()

    category_display["Revenue"] = category_display["revenue"].map(
        money
    )

    category_display["Orders"] = category_display["orders"].map(
        number
    )

    category_display["AOV"] = category_display["aov"].map(
        money_decimal
    )

    category_display = category_display[
        [
            "category",
            "Revenue",
            "Orders",
            "AOV",
        ]
    ]

    category_display = category_display.rename(
        columns={
            "category": "Category"
        }
    )

    st.dataframe(
        category_display,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE: DELIVERY
# ============================================================

def page_delivery():

    st.markdown(
        '<div class="section-title">Delivery Operations</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Measure delivery performance and identify where operational risk can affect sales experience.'
        '</div>',
        unsafe_allow_html=True,
    )

    on_time = filtered_df[
        filtered_df["is_late"] == 0
    ]

    late = filtered_df[
        filtered_df["is_late"] == 1
    ]

    late_revenue = late["revenue"].sum()

    late_orders = late["order_id"].nunique()

    ontime_orders = on_time["order_id"].nunique()

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
            "Orders delivered after estimate",
        )

    with c3:
        show_kpi(
            "Revenue in Late Orders",
            money(late_revenue),
            "Revenue associated with late orders",
        )

    with c4:
        show_kpi(
            "Average Delivery",
            f"{avg_delivery:.1f} days",
            "Purchase to delivery",
        )

    c1, c2 = st.columns(2)

    with c1:

        delivery_status = pd.DataFrame(
            {
                "Status": [
                    "On Time",
                    "Late",
                ],
                "Orders": [
                    ontime_orders,
                    late_orders,
                ],
            }
        )

        fig = px.bar(
            delivery_status,
            x="Status",
            y="Orders",
            title="On-Time vs Late Orders",
        )

        st.plotly_chart(
            chart_layout(fig, 390),
            use_container_width=True,
        )

    with c2:

        fig = px.histogram(
            filtered_df,
            x="delivery_days",
            nbins=30,
            title="Delivery Time Distribution",
            labels={
                "delivery_days": "Delivery Days"
            },
        )

        st.plotly_chart(
            chart_layout(fig, 390),
            use_container_width=True,
        )

    # State operational risk

    state_delivery = (
        filtered_df
        .groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            late_rate=("is_late", "mean"),
            avg_delivery=("delivery_days", "mean"),
            revenue=("revenue", "sum"),
        )
        .reset_index()
    )

    state_delivery["late_rate"] *= 100

    state_delivery = state_delivery.sort_values(
        "late_rate",
        ascending=False,
    ).head(12)

    fig = px.bar(
        state_delivery.sort_values("late_rate"),
        x="late_rate",
        y="customer_state",
        orientation="h",
        title="States with Highest Late-Delivery Rate",
        labels={
            "late_rate": "Late Delivery %",
            "customer_state": "",
        },
    )

    st.plotly_chart(
        chart_layout(fig, 450),
        use_container_width=True,
    )

    # Review relationship

    if "review_score" in filtered_df.columns:

        review_df = filtered_df.dropna(
            subset=["review_score"]
        ).copy()

        if not review_df.empty:

            review_summary = (
                review_df
                .groupby("is_late", as_index=False)
                ["review_score"]
                .mean()
            )

            review_summary["Delivery Status"] = (
                review_summary["is_late"]
                .map(
                    {
                        0: "On Time",
                        1: "Late",
                    }
                )
            )

            fig = px.bar(
                review_summary,
                x="Delivery Status",
                y="review_score",
                title="Average Review Score by Delivery Status",
                labels={
                    "review_score": "Average Review Score"
                },
            )

            st.plotly_chart(
                chart_layout(fig, 390),
                use_container_width=True,
            )


# ============================================================
# PAGE: BUSINESS INSIGHTS
# ============================================================

def page_business_insights():

    st.markdown(
        '<div class="section-title">Business Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'A management-oriented readout translating the analysis into commercial priorities.'
        '</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Core business metrics
    # --------------------------------------------------------

    monthly = (
        filtered_df
        .groupby("month", as_index=False)
        ["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    category = (
        filtered_df
        .groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    category["aov"] = category.apply(
        lambda row: safe_divide(
            row["revenue"],
            row["orders"],
        ),
        axis=1,
    )

    strongest_month = (
        monthly.iloc[0]["month"]
        if not monthly.empty
        else None
    )

    strongest_month_revenue = (
        monthly.iloc[0]["revenue"]
        if not monthly.empty
        else 0
    )

    leading_category = (
        category.sort_values(
            "revenue",
            ascending=False,
        ).iloc[0]["category"]
        if not category.empty
        else "Unknown"
    )

    leading_category_revenue = (
        category.sort_values(
            "revenue",
            ascending=False,
        ).iloc[0]["revenue"]
        if not category.empty
        else 0
    )

    # --------------------------------------------------------
    # Executive readout
    # --------------------------------------------------------

    show_decision(
        "Executive Readout",
        (
            f"The selected business period generated "
            f"{money(total_revenue)} in revenue across "
            f"{number(total_orders)} orders, with an average "
            f"order value of {money_decimal(aov)}. "
            f"{strongest_month.strftime('%B %Y') if strongest_month is not None else 'The selected period'} "
            f"recorded the strongest monthly revenue performance, "
            f"while {leading_category} emerged as the leading "
            f"product category by revenue."
        ),
    )

    # --------------------------------------------------------
    # Revenue concentration
    # --------------------------------------------------------

    category_sorted = category.sort_values(
        "revenue",
        ascending=False,
    )

    total_cat_revenue = category_sorted["revenue"].sum()

    top5_share = safe_divide(
        category_sorted.head(5)["revenue"].sum(),
        total_cat_revenue,
    ) * 100

    top10_share = safe_divide(
        category_sorted.head(10)["revenue"].sum(),
        total_cat_revenue,
    ) * 100

    show_decision(
        "Revenue Concentration",
        (
            f"The top five categories contribute "
            f"{top5_share:.1f}% of selected revenue, while "
            f"the top ten contribute {top10_share:.1f}%. "
            f"This indicates the revenue base is distributed "
            f"across multiple categories rather than relying "
            f"on a single product segment."
        ),
    )

    # --------------------------------------------------------
    # Category opportunity
    # --------------------------------------------------------

    high_volume = category.sort_values(
        "orders",
        ascending=False,
    ).head(10)

    high_volume_low_aov = high_volume.sort_values(
        "aov"
    ).iloc[0]

    show_decision(
        "Increase Revenue per Order",
        (
            f"{high_volume_low_aov['category']} combines strong "
            f"order volume with an average order value of "
            f"{money_decimal(high_volume_low_aov['aov'])}. "
            f"This creates an opportunity to test bundles, "
            f"cross-selling, complementary products and "
            f"threshold-based offers to increase basket value."
        ),
    )

    # --------------------------------------------------------
    # Delivery
    # --------------------------------------------------------

    show_decision(
        "Maintain Delivery Discipline",
        (
            f"{late_rate:.1f}% of selected orders were delivered "
            f"after the estimated date, representing approximately "
            f"{money(late_revenue)} in associated revenue. "
            f"Continued monitoring of high-risk states and "
            f"delivery-time variation can help protect the "
            f"customer experience."
        ),
    )

    # --------------------------------------------------------
    # Market opportunity
    # --------------------------------------------------------

    state_revenue = (
        filtered_df
        .groupby("customer_state")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_state = (
        state_revenue.index[0]
        if not state_revenue.empty
        else "Unknown"
    )

    top_state_revenue = (
        state_revenue.iloc[0]
        if not state_revenue.empty
        else 0
    )

    show_decision(
        "Market Opportunity",
        (
            f"{top_state} is the strongest customer-state market "
            f"within the current selection, generating "
            f"{money(top_state_revenue)} in revenue. "
            f"Regional performance should be considered when "
            f"prioritising category availability, fulfilment "
            f"capacity and commercial campaigns."
        ),
    )

    # --------------------------------------------------------
    # Management priorities
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Management Priorities</div>',
        unsafe_allow_html=True,
    )

    priorities = [
        (
            "Protect revenue leaders",
            f"Maintain availability and commercial focus on {leading_category}, "
            "the strongest category by selected revenue.",
        ),
        (
            "Increase transaction value",
            "Use bundles, cross-selling and product-mix strategies "
            "to improve AOV in high-volume categories.",
        ),
        (
            "Reduce operational risk",
            "Monitor late-delivery hotspots and investigate states "
            "with consistently higher delivery delays.",
        ),
    ]

    for title, text in priorities:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    {title}
                </div>

                <div class="insight-text">
                    {text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ROUTING
# ============================================================

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


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Olist Sales Insights
        &nbsp;•&nbsp;
        Revenue & Sales Analytics Dashboard
        &nbsp;•&nbsp;
        Python
        &nbsp;•&nbsp;
        Pandas
        &nbsp;•&nbsp;
        Plotly
        &nbsp;•&nbsp;
        Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
