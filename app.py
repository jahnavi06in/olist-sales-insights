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

    .stApp {
        background: #F6F7FB;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #0F172A;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    .hero {
        background: linear-gradient(135deg, #111827, #312E81);
        border-radius: 22px;
        padding: 30px;
        margin-bottom: 24px;
    }

    .hero-eyebrow {
        color: #A5B4FC;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .hero-title {
        color: white;
        font-size: 38px;
        font-weight: 800;
        margin: 5px 0;
    }

    .hero-text {
        color: #D1D5DB;
        font-size: 15px;
    }

    .section-title {
        color: #111827;
        font-size: 23px;
        font-weight: 800;
        margin-top: 28px;
        margin-bottom: 14px;
    }

    .kpi-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 19px;
        min-height: 125px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .kpi-label {
        color: #6B7280;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }

    .kpi-value {
        color: #111827;
        font-size: 26px;
        font-weight: 800;
        margin-top: 9px;
    }

    .kpi-note {
        color: #6B7280;
        font-size: 12px;
        margin-top: 5px;
    }

    .decision-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-left: 5px solid #6366F1;
        border-radius: 15px;
        padding: 18px 20px;
        margin: 15px 0;
    }

    .decision-label {
        color: #6366F1;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }

    .decision-title {
        color: #111827;
        font-size: 17px;
        font-weight: 800;
        margin: 4px 0 7px;
    }

    .decision-text {
        color: #4B5563;
        font-size: 14px;
        line-height: 1.6;
    }

    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def money(value):
    return f"R$ {value:,.0f}"


def percentage(value):
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
            <div class="decision-label">BUSINESS DECISION</div>
            <div class="decision-title">{title}</div>
            <div class="decision-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=420):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#374151"),
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        gridcolor="#EEF0F5",
        zeroline=False,
    )

    return fig


def clean_category(value):
    value = str(value).strip()

    if value.lower() in {
        "",
        "nan",
        "none",
        "unknown",
    }:
        return "Unknown"

    return value.replace("_", " ").title()


# =========================================================
# LOAD DATA
# =========================================================

try:
    df = load_data().copy()

except Exception as error:
    st.error("The dashboard could not load the Olist data.")
    st.exception(error)
    st.stop()


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = {
    "order_id",
    "month",
    "customer_state",
    "category",
    "revenue",
    "delivery_days",
    "is_late",
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(
        "The following required columns are missing: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()


# =========================================================
# DATA CLEANING
# =========================================================

df["order_id"] = df["order_id"].astype(str)

df["month"] = pd.to_datetime(
    df["month"],
    errors="coerce",
)

df["customer_state"] = (
    df["customer_state"]
    .astype(str)
    .str.upper()
    .str.strip()
)

df["category"] = df["category"].apply(clean_category)

df["revenue"] = pd.to_numeric(
    df["revenue"],
    errors="coerce",
).fillna(0)

df["delivery_days"] = pd.to_numeric(
    df["delivery_days"],
    errors="coerce",
)

df["is_late"] = (
    pd.to_numeric(
        df["is_late"],
        errors="coerce",
    )
    .fillna(0)
    .astype(int)
)

df = df.dropna(
    subset=[
        "month",
        "order_id",
    ]
)

df = df[df["revenue"] >= 0]

if df.empty:
    st.error("No usable records were found.")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📊 Olist Sales Insights")

    st.caption(
        "Revenue & Sales Analytics Dashboard"
    )

    st.divider()

    page = st.radio(
        "Dashboard",
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

    minimum_date = df["month"].min().date()
    maximum_date = df["month"].max().date()

    selected_dates = st.date_input(
        "Business period",
        value=(
            minimum_date,
            maximum_date,
        ),
        min_value=minimum_date,
        max_value=maximum_date,
    )

    all_states = sorted(
        df["customer_state"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_states = st.multiselect(
        "Customer states",
        all_states,
        default=all_states,
    )

    all_categories = sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        "Product categories",
        all_categories,
        default=all_categories,
    )

    st.divider()

    st.caption(
        "Olist Brazilian E-Commerce Dataset"
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = df.copy()

if (
    isinstance(selected_dates, (tuple, list))
    and len(selected_dates) == 2
):

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = (
        pd.Timestamp(selected_dates[1])
        + pd.Timedelta(days=1)
    )

    filtered = filtered[
        (filtered["month"] >= start_date)
        & (filtered["month"] < end_date)
    ]


if selected_states:

    filtered = filtered[
        filtered["customer_state"].isin(
            selected_states
        )
    ]

else:

    filtered = filtered.iloc[0:0]


if selected_categories:

    filtered = filtered[
        filtered["category"].isin(
            selected_categories
        )
    ]

else:

    filtered = filtered.iloc[0:0]


if filtered.empty:

    st.warning(
        "No data matches the selected filters."
    )

    st.stop()


# =========================================================
# COMMON METRICS
# =========================================================

total_revenue = filtered["revenue"].sum()

total_orders = filtered["order_id"].nunique()

average_order_value = safe_divide(
    total_revenue,
    total_orders,
)

order_level = (
    filtered
    .groupby("order_id", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        is_late=("is_late", "max"),
        delivery_days=("delivery_days", "max"),
    )
)

late_delivery_rate = (
    safe_divide(
        order_level["is_late"].sum(),
        len(order_level),
    )
    * 100
)


# =========================================================
# HERO
# =========================================================

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
            revenue, sales and operational insights.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAGE 1 — OVERVIEW
# =========================================================

def page_overview():

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_kpi(
            "TOTAL REVENUE",
            money(total_revenue),
            "Selected business period",
        )

    with col2:
        show_kpi(
            "ORDERS",
            f"{total_orders:,}",
            "Unique orders",
        )

    with col3:
        show_kpi(
            "AVERAGE ORDER VALUE",
            money(average_order_value),
            "Revenue per order",
        )

    with col4:
        show_kpi(
            "LATE DELIVERY RATE",
            percentage(late_delivery_rate),
            "Order level",
        )

    monthly = (
        filtered
        .groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("month")
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly Revenue",
        )

        fig.update_yaxes(
            tickprefix="R$ "
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

    with col2:

        category = (
            filtered
            .groupby("category", as_index=False)
            .agg(
                revenue=("revenue", "sum")
            )
            .sort_values(
                "revenue",
                ascending=False,
            )
            .head(10)
        )

        fig = px.bar(
            category.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            title="Top Categories by Revenue",
        )

        fig.update_xaxes(
            tickprefix="R$ "
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

    state = (
        filtered
        .groupby("customer_state", as_index=False)
        .agg(
            revenue=("revenue", "sum")
        )
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
        title="Top Customer States by Revenue",
    )

    fig.update_xaxes(
        tickprefix="R$ "
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True,
    )

    if not category.empty:

        top_category = category.iloc[0]

        show_decision(
            "Protect the revenue leader",
            f"<b>{top_category['category']}</b> is the leading "
            f"category by revenue, contributing "
            f"<b>{money(top_category['revenue'])}</b>. "
            "Maintain availability, monitor pricing and "
            "protect the customer experience around this category.",
        )


# =========================================================
# PAGE 2 — REVENUE INSIGHTS
# =========================================================

def page_revenue():

    st.markdown(
        '<div class="section-title">Revenue Insights</div>',
        unsafe_allow_html=True,
    )

    monthly = (
        filtered
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

    monthly["mom"] = (
        monthly["revenue"]
        .pct_change()
        * 100
    )

    peak = monthly.loc[
        monthly["revenue"].idxmax()
    ]

    latest_growth = (
        monthly["mom"].iloc[-1]
        if len(monthly) > 1
        else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        show_kpi(
            "PEAK REVENUE MONTH",
            peak["month"].strftime("%B %Y"),
            money(peak["revenue"]),
        )

    with col2:
        show_kpi(
            "LATEST MOM GROWTH",
            percentage(latest_growth),
            "vs previous month",
        )

    with col3:
        show_kpi(
            "REVENUE PER ORDER",
            money(average_order_value),
            "Selected period",
        )

    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Revenue Trend",
    )

    fig.update_yaxes(
        tickprefix="R$ "
    )

    st.plotly_chart(
        style_chart(fig, 430),
        use_container_width=True,
    )

    growth = monthly.dropna(
        subset=["mom"]
    )

    if not growth.empty:

        fig = px.bar(
            growth,
            x="month",
            y="mom",
            title="Month-over-Month Revenue Growth",
        )

        fig.update_yaxes(
            ticksuffix="%"
        )

        st.plotly_chart(
            style_chart(fig, 380),
            use_container_width=True,
        )

    category = (
        filtered
        .groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum")
        )
        .sort_values(
            "revenue",
            ascending=False,
        )
    )

    top5_share = (
        safe_divide(
            category.head(5)["revenue"].sum(),
            total_revenue,
        )
        * 100
    )

    top10_share = (
        safe_divide(
            category.head(10)["revenue"].sum(),
            total_revenue,
        )
        * 100
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        show_kpi(
            "TOP 5 CATEGORY SHARE",
            percentage(top5_share),
            "Revenue share",
        )

    with col2:
        show_kpi(
            "TOP 10 CATEGORY SHARE",
            percentage(top10_share),
            "Revenue share",
        )

    with col3:
        show_kpi(
            "NUMBER OF CATEGORIES",
            f"{len(category):,}",
            "Selected period",
        )

    show_decision(
        "Healthy Revenue Diversification",
        f"The top five categories contribute "
        f"<b>{percentage(top5_share)}</b> of revenue. "
        "The portfolio is relatively diversified, giving "
        "management room to invest in growth categories "
        "without excessive dependence on a small number "
        "of product groups.",
    )


# =========================================================
# PAGE 3 — SALES & CATEGORIES
# =========================================================

def page_sales_categories():

    st.markdown(
        '<div class="section-title">Sales & Category Insights</div>',
        unsafe_allow_html=True,
    )

    category = (
        filtered
        .groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
    )

    category["aov"] = (
        category["revenue"]
        / category["orders"]
    )

    category["revenue_share"] = (
        category["revenue"]
        / total_revenue
        * 100
    )

    category = category.sort_values(
        "revenue",
        ascending=False,
    )

    top = category.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_kpi(
            "TOP CATEGORY",
            top["category"],
            "Highest revenue",
        )

    with col2:
        show_kpi(
            "TOP CATEGORY REVENUE",
            money(top["revenue"]),
            percentage(top["revenue_share"])
            + " of revenue",
        )

    with col3:
        show_kpi(
            "TOP CATEGORY ORDERS",
            f"{int(top['orders']):,}",
            "Unique orders",
        )

    with col4:
        show_kpi(
            "TOP CATEGORY AOV",
            money(top["aov"]),
            "Revenue per order",
        )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            category.head(10).sort_values(
                "revenue"
            ),
            x="revenue",
            y="category",
            orientation="h",
            title="Top Categories by Revenue",
        )

        fig.update_xaxes(
            tickprefix="R$ "
        )

        st.plotly_chart(
            style_chart(fig, 430),
            use_container_width=True,
        )

    with col2:

        fig = px.scatter(
            category,
            x="orders",
            y="aov",
            size="revenue",
            hover_name="category",
            title="Order Volume vs Average Order Value",
        )

        fig.update_yaxes(
            tickprefix="R$ "
        )

        st.plotly_chart(
            style_chart(fig, 430),
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Category Performance Matrix</div>',
        unsafe_allow_html=True,
    )

    median_orders = category["orders"].median()
    median_aov = category["aov"].median()

    matrix = category.copy()

    matrix["segment"] = matrix.apply(
        lambda row:
        "High Volume + High Value"
        if row["orders"] >= median_orders
        and row["aov"] >= median_aov
        else
        "High Volume + Low Value"
        if row["orders"] >= median_orders
        else
        "Low Volume + High Value"
        if row["aov"] >= median_aov
        else
        "Low Volume + Low Value",
        axis=1,
    )

    fig = px.scatter(
        matrix,
        x="orders",
        y="aov",
        size="revenue",
        color="segment",
        hover_name="category",
        title="Category Volume vs Value",
    )

    fig.add_vline(
        x=median_orders,
        line_dash="dash",
    )

    fig.add_hline(
        y=median_aov,
        line_dash="dash",
    )

    fig.update_yaxes(
        tickprefix="R$ "
    )

    st.plotly_chart(
        style_chart(fig, 470),
        use_container_width=True,
    )

    opportunity = category[
        (category["orders"] >= median_orders)
        & (category["aov"] < median_aov)
    ].sort_values(
        "orders",
        ascending=False,
    )

    if not opportunity.empty:

        opportunity_row = opportunity.iloc[0]

        show_decision(
            "Increase Revenue per Order",
            f"<b>{opportunity_row['category']}</b> has strong "
            f"order volume but an AOV of only "
            f"<b>{money(opportunity_row['aov'])}</b>. "
            "Test bundles, complementary products, premium "
            "alternatives and threshold-based offers.",
        )

    table = category.copy()

    table["Revenue"] = table["revenue"].map(
        money
    )

    table["Orders"] = table["orders"].map(
        lambda value: f"{int(value):,}"
    )

    table["AOV"] = table["aov"].map(
        money
    )

    table["Revenue Share"] = table[
        "revenue_share"
    ].map(
        percentage
    )

    st.dataframe(
        table[
            [
                "category",
                "Revenue",
                "Orders",
                "AOV",
                "Revenue Share",
            ]
        ].rename(
            columns={
                "category": "Category"
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# PAGE 4 — DELIVERY
# =========================================================

def page_delivery():

    st.markdown(
        '<div class="section-title">Delivery Operations</div>',
        unsafe_allow_html=True,
    )

    average_delivery = (
        order_level["delivery_days"].mean()
    )

    late_revenue = order_level.loc[
        order_level["is_late"] == 1,
        "revenue",
    ].sum()

    on_time_revenue = order_level.loc[
        order_level["is_late"] == 0,
        "revenue",
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_kpi(
            "LATE DELIVERY RATE",
            percentage(late_delivery_rate),
            "Order level",
        )

    with col2:
        show_kpi(
            "AVERAGE DELIVERY",
            f"{average_delivery:.1f} days",
            "Purchase to delivery",
        )

    with col3:
        show_kpi(
            "LATE-ORDER REVENUE",
            money(late_revenue),
            "Revenue in late orders",
        )

    with col4:
        show_kpi(
            "ON-TIME REVENUE",
            money(on_time_revenue),
            "Revenue in on-time orders",
        )

    state = (
        filtered
        .groupby("customer_state", as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            late_rate=("is_late", "mean"),
            avg_delivery=("delivery_days", "mean"),
            revenue=("revenue", "sum"),
        )
    )

    state["late_rate"] *= 100

    state = state[
        state["orders"] >= 100
    ].sort_values(
        "late_rate",
        ascending=False,
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            state.head(10).sort_values(
                "late_rate"
            ),
            x="late_rate",
            y="customer_state",
            orientation="h",
            title="Highest Late-Delivery Rates",
        )

        fig.update_xaxes(
            ticksuffix="%"
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True,
        )

    with col2:

        fig = px.scatter(
            state,
            x="revenue",
            y="late_rate",
            size="orders",
            hover_name="customer_state",
            title="Revenue vs Delivery Risk",
        )

        fig.update_xaxes(
            tickprefix="R$ "
        )

        fig.update_yaxes(
            ticksuffix="%"
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True,
        )

    if not state.empty:

        risk = state.iloc[0]

        show_decision(
            "Maintain Delivery Discipline",
            f"<b>{risk['customer_state']}</b> has the highest "
            f"late-delivery rate among states with at least "
            f"100 orders: <b>{risk['late_rate']:.1f}%</b>. "
            f"Average delivery time is "
            f"<b>{risk['avg_delivery']:.1f} days</b>, while "
            f"the state represents "
            f"<b>{money(risk['revenue'])}</b> in revenue. "
            "Prioritize carrier performance and fulfilment "
            "investigation in this market.",
        )


# =========================================================
# PAGE 5 — BUSINESS INSIGHTS
# =========================================================

def page_business_insights():

    st.markdown(
        '<div class="section-title">Business Insights</div>',
        unsafe_allow_html=True,
    )

    category = (
        filtered
        .groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
    )

    category["aov"] = (
        category["revenue"]
        / category["orders"]
    )

    category = category.sort_values(
        "revenue",
        ascending=False,
    )

    top = category.iloc[0]

    median_orders = category["orders"].median()
    median_aov = category["aov"].median()

    opportunity = category[
        (category["orders"] >= median_orders)
        & (category["aov"] < median_aov)
    ].sort_values(
        "orders",
        ascending=False,
    )

    show_decision(
        "1 — Protect the Revenue Leader",
        f"<b>{top['category']}</b> is the largest "
        f"revenue contributor with "
        f"<b>{money(top['revenue'])}</b>. "
        "Maintain availability, monitor pricing and "
        "protect the customer experience around this category.",
    )

    if not opportunity.empty:

        row = opportunity.iloc[0]

        show_decision(
            "2 — Increase Revenue per Order",
            f"<b>{row['category']}</b> has strong order volume "
            f"but an AOV of only <b>{money(row['aov'])}</b>. "
            "Test bundles, complementary products, premium "
            "alternatives and threshold-based offers.",
        )

    else:

        show_decision(
            "2 — Improve Order Economics",
            "Review high-volume categories for bundling, "
            "cross-selling and premium product opportunities.",
        )

    show_decision(
        "3 — Maintain Delivery Discipline",
        f"Late delivery is currently at "
        f"<b>{percentage(late_delivery_rate)}</b>. "
        "Continue monitoring fulfilment performance while "
        "protecting the operational standards that support "
        "customer experience.",
    )

    state = (
        filtered
        .groupby("customer_state", as_index=False)
        .agg(
            revenue=("revenue", "sum")
        )
        .sort_values(
            "revenue",
            ascending=False,
        )
        .head(12)
    )

    fig = px.bar(
        state.sort_values("revenue"),
        x="revenue",
        y="customer_state",
        orientation="h",
        title="Revenue Distribution Across Customer States",
    )

    fig.update_xaxes(
        tickprefix="R$ "
    )

    st.plotly_chart(
        style_chart(fig, 430),
        use_container_width=True,
    )

    st.markdown(
        f"""
        <div class="decision-card">

            <div class="decision-label">
                MANAGEMENT SUMMARY
            </div>

            <div class="decision-title">
                From Dashboard to Decision
            </div>

            <div class="decision-text">

                The selected business period represents
                <b>{money(total_revenue)}</b>
                in revenue across
                <b>{total_orders:,}</b>
                orders.

                The strongest opportunity is not simply to
                increase order volume, but to improve the
                economics of existing demand through category
                mix, average order value and operational reliability.

                <br><br>

                The dashboard therefore prioritizes three levers:

                <b>protect revenue leaders</b>,

                <b>increase value per transaction</b>,

                and

                <b>reduce delivery risk</b>.

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PAGE ROUTER
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
        Olist Sales Insights • Revenue & Sales Analytics Dashboard
        • Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
