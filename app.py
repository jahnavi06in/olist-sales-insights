import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
# GLOBAL STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- APP ---------- */

    .stApp {
        background: #f7f8fc;
        color: #111827;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    .brand {
        font-size: 23px;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.7px;
        margin-bottom: 2px;
    }

    .brand span {
        color: #4f46e5;
    }

    .brand-sub {
        color: #6b7280;
        font-size: 12px;
        margin-bottom: 28px;
    }

    .side-section {
        font-size: 10px;
        font-weight: 700;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    /* ---------- HEADER ---------- */

    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }

    .page-eyebrow {
        font-size: 12px;
        font-weight: 700;
        color: #6366f1;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin-bottom: 6px;
    }

    .page-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #111827;
        margin: 0;
    }

    .page-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-top: 7px;
    }

    .live-pill {
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        white-space: nowrap;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px;
        min-height: 132px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
    }

    .kpi-label {
        color: #6b7280;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .kpi-value {
        color: #111827;
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }

    .kpi-note {
        color: #9ca3af;
        font-size: 11px;
        margin-top: 8px;
    }

    .kpi-accent {
        width: 32px;
        height: 4px;
        background: #4f46e5;
        border-radius: 10px;
        margin-bottom: 14px;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 18px;
        font-weight: 750;
        color: #111827;
        letter-spacing: -0.3px;
        margin-top: 28px;
        margin-bottom: 4px;
    }

    .section-description {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 15px;
    }

    /* ---------- INSIGHT CARDS ---------- */

    .insight-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
        min-height: 145px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.03);
    }

    .insight-label {
        font-size: 11px;
        color: #6366f1;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }

    .insight-value {
        font-size: 18px;
        font-weight: 750;
        color: #111827;
        margin-bottom: 7px;
    }

    .insight-text {
        font-size: 12px;
        color: #6b7280;
        line-height: 1.55;
    }

    /* ---------- DECISION CARD ---------- */

    .decision-card {
        background: #111827;
        border-radius: 18px;
        padding: 25px;
        color: white;
        margin-top: 20px;
    }

    .decision-label {
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .decision-title {
        font-size: 24px;
        font-weight: 800;
        margin-top: 7px;
        margin-bottom: 8px;
    }

    .decision-text {
        color: #d1d5db;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        border-top: 1px solid #e5e7eb;
        margin-top: 45px;
        padding-top: 18px;
        color: #9ca3af;
        font-size: 11px;
        text-align: center;
    }

    /* ---------- STREAMLIT CLEANUP ---------- */

    div[data-testid="stMetric"] {
        background: transparent;
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
    }

    div[data-testid="stMetricValue"] {
        color: #111827;
    }

    button[kind="secondary"] {
        border-radius: 9px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def get_data():
    return load_data()


df = get_data().copy()


# =========================================================
# DATA PREPARATION
# =========================================================

df["month"] = pd.to_datetime(df["month"], errors="coerce")

if "revenue" in df.columns:
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0)

if "delivery_days" in df.columns:
    df["delivery_days"] = pd.to_numeric(
        df["delivery_days"], errors="coerce"
    )

if "late" in df.columns:
    df["late"] = pd.to_numeric(df["late"], errors="coerce").fillna(0)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">Olist <span>Insights</span></div>
        <div class="brand-sub">E-commerce intelligence dashboard</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-section">Workspace</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Revenue Intelligence",
            "Sales & Categories",
            "Delivery Operations",
            "Business Insights",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<div class="side-section">Filters</div>', unsafe_allow_html=True)

    # Date filter
    valid_months = df["month"].dropna()

    if len(valid_months) > 0:
        min_month = valid_months.min().date()
        max_month = valid_months.max().date()

        date_range = st.slider(
            "Analysis period",
            min_value=min_month,
            max_value=max_month,
            value=(min_month, max_month),
        )

        start_date = pd.Timestamp(date_range[0])
        end_date = pd.Timestamp(date_range[1])

        df_filtered = df[
            (df["month"] >= start_date)
            & (df["month"] <= end_date)
        ].copy()
    else:
        df_filtered = df.copy()

    # State filter
    if "customer_state" in df.columns:
        states = sorted(
            df["customer_state"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_states = st.multiselect(
            "Customer state",
            states,
            default=[],
        )

        if selected_states:
            df_filtered = df_filtered[
                df_filtered["customer_state"].astype(str).isin(
                    selected_states
                )
            ]

    # Category filter
    if "category" in df.columns:
        categories = sorted(
            df["category"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_categories = st.multiselect(
            "Product category",
            categories,
            default=[],
        )

        if selected_categories:
            df_filtered = df_filtered[
                df_filtered["category"].astype(str).isin(
                    selected_categories
                )
            ]

    st.markdown("---")

    st.caption("DATA SOURCE")
    st.caption("Brazilian E-Commerce Public Dataset by Olist")

    st.caption("ANALYSIS")
    st.caption("Delivered orders • Revenue excludes freight")


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(value):
    if pd.isna(value):
        return "R$ 0"
    return f"R$ {value:,.0f}"


def number(value):
    if pd.isna(value):
        return "0"
    return f"{int(value):,}"


def percent(value):
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"


def style_chart(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=35, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#374151",
            size=12,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_color="#111827",
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=11),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#e5e7eb",
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#f0f1f5",
        zeroline=False,
    )

    return fig


def section(title, description=""):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CORE METRICS
# =========================================================

f = df_filtered.copy()

if len(f) == 0:
    st.warning("No data matches the selected filters.")
    st.stop()


orders_df = f.drop_duplicates("order_id")

total_revenue = f["revenue"].sum()

total_orders = orders_df["order_id"].nunique()

aov = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

if "late" in orders_df.columns:
    late_rate = orders_df["late"].mean() * 100
else:
    late_rate = 0

if "delivery_days" in orders_df.columns:
    avg_delivery = orders_df["delivery_days"].mean()
else:
    avg_delivery = 0


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="top-header">
        <div>
            <div class="page-eyebrow">Olist Analytics</div>
            <div class="page-title">{page}</div>
            <div class="page-subtitle">
                Turn transaction data into commercially useful decisions.
            </div>
        </div>

        <div class="live-pill">
            ● LIVE DATASET
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    # KPI ROW
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-accent"></div>
                <div class="kpi-label">TOTAL REVENUE</div>
                <div class="kpi-value">{money(total_revenue)}</div>
                <div class="kpi-note">Delivered order revenue</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-accent"></div>
                <div class="kpi-label">ORDERS</div>
                <div class="kpi-value">{number(total_orders)}</div>
                <div class="kpi-note">Unique delivered orders</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-accent"></div>
                <div class="kpi-label">AVERAGE ORDER VALUE</div>
                <div class="kpi-value">{money(aov)}</div>
                <div class="kpi-note">Revenue per order</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-accent"></div>
                <div class="kpi-label">LATE DELIVERY RATE</div>
                <div class="kpi-value">{percent(late_rate)}</div>
                <div class="kpi-note">Orders delivered late</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # REVENUE + CATEGORY
    section(
        "Commercial performance",
        "A high-level view of revenue momentum and product mix."
    )

    col1, col2 = st.columns([1.7, 1])

    with col1:

        monthly = (
            f.groupby("month", as_index=False)["revenue"]
            .sum()
            .sort_values("month")
        )

        fig = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="Revenue: R$ %{y:,.0f}<extra></extra>",
        )

        fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)

        fig = style_chart(fig, 390)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:

        cat = (
            f.groupby("category", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
            .head(8)
        )

        cat = cat.sort_values("revenue")

        fig = px.bar(
            cat,
            x="revenue",
            y="category",
            orientation="h",
            text_auto=".2s",
        )

        fig.update_traces(
            marker_line_width=0,
            hovertemplate="R$ %{x:,.0f}<extra></extra>",
        )

        fig.update_xaxes(
            title=None,
            tickprefix="R$ ",
            tickformat=",.0f",
        )

        fig.update_yaxes(title=None)

        fig = style_chart(fig, 390)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # GEOGRAPHIC PERFORMANCE
    section(
        "Geographic performance",
        "Revenue concentration across Brazilian customer states."
    )

    state_rev = (
        f.groupby("customer_state", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    fig = px.bar(
        state_rev,
        x="customer_state",
        y="revenue",
        text_auto=".2s",
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="%{x}: R$ %{y:,.0f}<extra></extra>",
    )

    fig.update_yaxes(
        title=None,
        tickprefix="R$ ",
        tickformat=",.0f",
    )

    fig.update_xaxes(title=None)

    fig = style_chart(fig, 350)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# REVENUE INTELLIGENCE
# =========================================================

elif page == "Revenue Intelligence":

    section(
        "Revenue intelligence",
        "Understand when revenue is generated and how performance changes over time."
    )

    monthly = (
        f.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )

    if len(monthly) >= 2:
        monthly["growth"] = monthly["revenue"].pct_change() * 100
    else:
        monthly["growth"] = 0

    latest_revenue = monthly.iloc[-1]["revenue"]

    if len(monthly) >= 2:
        previous_revenue = monthly.iloc[-2]["revenue"]
        growth = (
            (latest_revenue - previous_revenue)
            / previous_revenue
            * 100
            if previous_revenue != 0
            else 0
        )
    else:
        growth = 0

    peak_row = monthly.loc[monthly["revenue"].idxmax()]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Peak revenue month",
            peak_row["month"].strftime("%b %Y"),
        )

    with c2:
        st.metric(
            "Peak monthly revenue",
            money(peak_row["revenue"]),
        )

    with c3:
        st.metric(
            "Latest month change",
            f"{growth:+.1f}%",
        )

    st.markdown("")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["revenue"],
            mode="lines+markers",
            fill="tozeroy",
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="R$ %{y:,.0f}<extra></extra>",
        )
    )

    fig.update_yaxes(
        title=None,
        tickprefix="R$ ",
        tickformat=",.0f",
    )

    fig.update_xaxes(title=None)

    fig = style_chart(fig, 440)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    section(
        "Revenue concentration",
        "How much of total revenue comes from the leading categories?"
    )

    category_rev = (
        f.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    total_cat_revenue = category_rev.sum()

    top5_share = (
        category_rev.head(5).sum() / total_cat_revenue * 100
        if total_cat_revenue > 0
        else 0
    )

    st.metric(
        "Top 5 categories' revenue share",
        f"{top5_share:.1f}%",
    )

    top_categories = (
        category_rev
        .head(10)
        .reset_index()
        .rename(columns={"revenue": "Revenue"})
    )

    top_categories["Share"] = (
        top_categories["Revenue"]
        / total_cat_revenue
        * 100
    )

    st.dataframe(
        top_categories.style.format(
            {
                "Revenue": "R$ {:,.0f}",
                "Share": "{:.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# SALES & CATEGORIES
# =========================================================

elif page == "Sales & Categories":

    section(
        "Sales & category intelligence",
        "Identify the products and markets contributing most to commercial performance."
    )

    category = (
        f.groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )

    category["aov"] = (
        category["revenue"] / category["orders"]
    )

    left, right = st.columns([1.4, 1])

    with left:

        top = category.head(12).sort_values("revenue")

        fig = px.bar(
            top,
            x="revenue",
            y="category",
            orientation="h",
            text_auto=".2s",
        )

        fig.update_traces(
            marker_line_width=0,
            hovertemplate=(
                "%{y}<br>"
                "Revenue: R$ %{x:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.update_xaxes(
            title=None,
            tickprefix="R$ ",
            tickformat=",.0f",
        )

        fig.update_yaxes(title=None)

        fig = style_chart(fig, 500)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:

        fig = px.scatter(
            category,
            x="orders",
            y="aov",
            size="revenue",
            hover_name="category",
        )

        fig.update_traces(
            marker=dict(
                opacity=0.75,
                line=dict(width=1),
            ),
            hovertemplate=(
                "%{hovertext}<br>"
                "Orders: %{x:,}<br>"
                "AOV: R$ %{y:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.update_xaxes(
            title="Orders",
            tickformat=",",
        )

        fig.update_yaxes(
            title="Average order value",
            tickprefix="R$ ",
            tickformat=",.0f",
        )

        fig = style_chart(fig, 500)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    section(
        "Category performance table",
        "A recruiter-friendly view of the commercial metrics behind the chart."
    )

    table = category.copy()

    table["revenue"] = table["revenue"].round(0)
    table["aov"] = table["aov"].round(0)

    table = table.rename(
        columns={
            "category": "Category",
            "revenue": "Revenue",
            "orders": "Orders",
            "aov": "AOV",
        }
    )

    st.dataframe(
        table.style.format(
            {
                "Revenue": "R$ {:,.0f}",
                "Orders": "{:,.0f}",
                "AOV": "R$ {:,.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# DELIVERY OPERATIONS
# =========================================================

elif page == "Delivery Operations":

    section(
        "Delivery operations",
        "Find geographic areas where customer delivery experience requires attention."
    )

    delivery = (
        orders_df.groupby("customer_state", as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            avg_delivery=("delivery_days", "mean"),
            late_rate=("late", "mean"),
        )
    )

    delivery["late_rate"] = delivery["late_rate"] * 100

    delivery = delivery[
        delivery["orders"] >= 100
    ].copy()

    if len(delivery) > 0:

        worst = delivery.sort_values(
            "late_rate",
            ascending=False,
        ).head(10)

        c1, c2 = st.columns(2)

        with c1:

            fig = px.bar(
                worst.sort_values("late_rate"),
                x="late_rate",
                y="customer_state",
                orientation="h",
                text_auto=".1f",
            )

            fig.update_traces(
                marker_line_width=0,
                hovertemplate=(
                    "%{y}: %{x:.1f}% late"
                    "<extra></extra>"
                ),
            )

            fig.update_xaxes(
                title=None,
                ticksuffix="%",
            )

            fig.update_yaxes(title=None)

            fig = style_chart(fig, 430)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with c2:

            fig = px.scatter(
                delivery,
                x="avg_delivery",
                y="late_rate",
                size="orders",
                hover_name="customer_state",
            )

            fig.update_traces(
                marker=dict(
                    opacity=0.75,
                    line=dict(width=1),
                ),
                hovertemplate=(
                    "%{hovertext}<br>"
                    "Avg delivery: %{x:.1f} days<br>"
                    "Late rate: %{y:.1f}%"
                    "<extra></extra>"
                ),
            )

            fig.update_xaxes(
                title="Average delivery time",
                ticksuffix=" days",
            )

            fig.update_yaxes(
                title="Late delivery rate",
                ticksuffix="%",
            )

            fig = style_chart(fig, 430)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

        section(
            "Operational benchmark",
            "States with at least 100 delivered orders are included to avoid unstable small-sample comparisons."
        )

        operational_table = delivery.sort_values(
            "late_rate",
            ascending=False,
        ).copy()

        operational_table = operational_table.rename(
            columns={
                "customer_state": "State",
                "orders": "Orders",
                "avg_delivery": "Avg Delivery Days",
                "late_rate": "Late Rate",
            }
        )

        st.dataframe(
            operational_table.style.format(
                {
                    "Orders": "{:,.0f}",
                    "Avg Delivery Days": "{:.1f}",
                    "Late Rate": "{:.1f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info(
            "Not enough orders in the selected filters to calculate the delivery benchmark."
        )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "Business Insights":

    section(
        "Business insights",
        "Translate the analysis into practical commercial and operational actions."
    )

    category_rev = (
        f.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    state_rev = (
        f.groupby("customer_state")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    monthly = (
        f.groupby("month")["revenue"]
        .sum()
        .sort_values()
    )

    top_category = (
        category_rev.index[0]
        if len(category_rev) > 0
        else "N/A"
    )

    top_category_revenue = (
        category_rev.iloc[0]
        if len(category_rev) > 0
        else 0
    )

    top_state = (
        state_rev.index[0]
        if len(state_rev) > 0
        else "N/A"
    )

    top_state_revenue = (
        state_rev.iloc[0]
        if len(state_rev) > 0
        else 0
    )

    peak_month = (
        monthly.idxmax()
        if len(monthly) > 0
        else None
    )

    peak_month_revenue = (
        monthly.max()
        if len(monthly) > 0
        else 0
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">CATEGORY LEADER</div>
                <div class="insight-value">{top_category}</div>
                <div class="insight-text">
                    Leading category by revenue with
                    <b>{money(top_category_revenue)}</b>
                    generated in the selected period.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">GEOGRAPHIC LEADER</div>
                <div class="insight-value">{top_state}</div>
                <div class="insight-text">
                    Highest-revenue customer state with
                    <b>{money(top_state_revenue)}</b>
                    in selected revenue.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        peak_label = (
            peak_month.strftime("%b %Y")
            if peak_month is not None
            else "N/A"
        )

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">PEAK PERIOD</div>
                <div class="insight-value">{peak_label}</div>
                <div class="insight-text">
                    Highest monthly revenue reached
                    <b>{money(peak_month_revenue)}</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # DECISION FRAMEWORK
    st.markdown(
        """
        <div class="decision-card">
            <div class="decision-label">Decision framework</div>
            <div class="decision-title">
                From reporting to action
            </div>
            <div class="decision-text">
                Use the dashboard to identify where revenue is concentrated,
                which categories deserve commercial attention, and which
                geographic markets require delivery-performance improvement.
                The goal is not simply to report what happened, but to give
                decision-makers a clear starting point for what to investigate next.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # THREE BUSINESS ACTIONS
    section(
        "Recommended actions",
        "Evidence-based actions generated directly from the dashboard analysis."
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-label">01 · GROWTH</div>
                <div class="insight-value">Protect category leaders</div>
                <div class="insight-text">
                    Monitor the strongest revenue categories closely and
                    investigate whether inventory, pricing or promotion
                    changes could affect their contribution.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with a2:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-label">02 · OPERATIONS</div>
                <div class="insight-value">Prioritize delivery hotspots</div>
                <div class="insight-text">
                    Investigate states with elevated late-delivery rates
                    and meaningful order volumes before making network-wide
                    operational changes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with a3:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-label">03 · PLANNING</div>
                <div class="insight-value">Use peak periods strategically</div>
                <div class="insight-text">
                    Compare high-revenue months with category and geographic
                    performance to improve future demand planning and
                    commercial prioritization.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Olist Sales Insights · Business Analytics Portfolio Project
        · Built with Python, Pandas, Plotly & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
    )
