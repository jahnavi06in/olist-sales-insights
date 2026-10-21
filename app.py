hereimport streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data import load_data


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Olist Sales Insights",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COLORS
# =========================================================

NAVY = "#172554"
NAVY_2 = "#1E3A8A"
INDIGO = "#4F46E5"
BLUE = "#2563EB"
LIGHT_BLUE = "#EEF2FF"

WHITE = "#FFFFFF"
PAGE_BG = "#F5F7FB"
CARD_BG = "#FFFFFF"

TEXT = "#111827"
MUTED = "#64748B"
BORDER = "#E2E8F0"

GREEN = "#059669"
RED = "#DC2626"
ORANGE = "#D97706"


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* ---------------- PAGE ---------------- */

    .stApp {{
        background: {PAGE_BG};
        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stMainBlockContainer"] {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }}


    /* ---------------- SIDEBAR ---------------- */

    [data-testid="stSidebar"] {{
        background: {NAVY};
        min-width: 245px;
        max-width: 245px;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding: 1.3rem 1rem;
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    .sidebar-brand {{
        padding: 12px 10px 22px 10px;
    }}

    .brand-mark {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: white;
        color: {NAVY};
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 18px;
        margin-bottom: 12px;
    }}

    .brand-name {{
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}

    .brand-name span {{
        color: #A5B4FC;
    }}

    .brand-sub {{
        font-size: 11px;
        color: #CBD5E1 !important;
        margin-top: 4px;
        line-height: 1.4;
    }}

    .sidebar-section {{
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8 !important;
        font-weight: 700;
        margin: 18px 10px 8px 10px;
    }}

    .sidebar-footer {{
        position: fixed;
        bottom: 20px;
        width: 205px;
        padding: 12px;
        border-top: 1px solid rgba(255,255,255,0.12);
        color: #94A3B8 !important;
        font-size: 10px;
    }}


    /* ---------------- HEADER ---------------- */

    .top-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }}

    .page-title {{
        font-size: 29px;
        font-weight: 800;
        color: {TEXT};
        letter-spacing: -1px;
        margin: 0;
    }}

    .page-subtitle {{
        color: {MUTED};
        font-size: 13px;
        margin-top: 5px;
    }}

    .status-pill {{
        background: #ECFDF5;
        color: {GREEN};
        border: 1px solid #A7F3D0;
        border-radius: 20px;
        padding: 7px 13px;
        font-size: 11px;
        font-weight: 700;
    }}


    /* ---------------- FILTER BAR ---------------- */

    .filter-box {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 12px 16px 3px 16px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(15,23,42,0.025);
    }}


    /* ---------------- KPI CARDS ---------------- */

    .kpi-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 17px 18px;
        min-height: 110px;
        box-shadow: 0 3px 12px rgba(15,23,42,0.035);
    }}

    .kpi-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 11px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .4px;
    }}

    .kpi-icon {{
        width: 30px;
        height: 30px;
        border-radius: 9px;
        background: {LIGHT_BLUE};
        color: {INDIGO};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 800;
    }}

    .kpi-value {{
        color: {TEXT};
        font-size: 24px;
        font-weight: 800;
        margin-top: 10px;
        letter-spacing: -0.7px;
    }}

    .kpi-note {{
        color: {MUTED};
        font-size: 10px;
        margin-top: 4px;
    }}


    /* ---------------- SECTION CARDS ---------------- */

    .section-card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 3px 12px rgba(15,23,42,0.03);
    }}

    .card-title {{
        font-size: 14px;
        font-weight: 750;
        color: {TEXT};
    }}

    .card-subtitle {{
        font-size: 10px;
        color: {MUTED};
        margin-top: 3px;
    }}


    /* ---------------- INSIGHT CARDS ---------------- */

    .insight {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-left: 4px solid {INDIGO};
        border-radius: 10px;
        padding: 13px 15px;
        margin-bottom: 9px;
    }}

    .insight-title {{
        color: {TEXT};
        font-weight: 750;
        font-size: 12px;
        margin-bottom: 4px;
    }}

    .insight-text {{
        color: {MUTED};
        font-size: 11px;
        line-height: 1.5;
    }}


    /* ---------------- FOOTER ---------------- */

    .footer {{
        text-align: center;
        color: #94A3B8;
        font-size: 10px;
        padding: 30px 0 5px 0;
    }}


    /* ---------------- STREAMLIT INPUTS ---------------- */

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stSlider"] label {{
        font-size: 11px !important;
        font-weight: 650 !important;
        color: {TEXT} !important;
    }}

    .stButton button {{
        border-radius: 9px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

df = load_data()

if df.empty:
    st.error("No data found. Please check the files inside the data folder.")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="brand-mark">
                ◈
            </div>

            <div class="brand-name">
                Olist <span>Insights</span>
            </div>

            <div class="brand-sub">
                E-commerce Revenue &<br>
                Operations Analytics
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Sales Performance",
            "Delivery Analytics",
            "Business Insights",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-section">Dataset</div>',
        unsafe_allow_html=True,
    )

    st.caption("Olist Brazilian E-Commerce")
    st.caption("Delivered orders only")
    st.caption("Jan 2017 – Aug 2018")

    st.markdown(
        """
        <div class="sidebar-footer">
            Data Analyst Portfolio Project<br>
            Built with Python · Pandas · Plotly · Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FILTERS
# =========================================================

months = sorted(df["month"].dt.date.unique())

with st.container():

    st.markdown(
        '<div class="filter-box">',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns([1.2, 1, 1])

    with f1:

        start, end = st.select_slider(
            "Analysis Period",
            options=months,
            value=(months[0], months[-1]),
            format_func=lambda d: d.strftime("%b %Y"),
        )

    with f2:

        states = st.multiselect(
            "Customer State",
            sorted(df["customer_state"].dropna().unique()),
            placeholder="All states",
        )

    with f3:

        categories = st.multiselect(
            "Product Category",
            sorted(df["category"].dropna().unique()),
            placeholder="All categories",
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# FILTER DATA
# =========================================================

mask = (
    (df["month"].dt.date >= start)
    & (df["month"].dt.date <= end)
)

if states:
    mask &= df["customer_state"].isin(states)

if categories:
    mask &= df["category"].isin(categories)

f = df.loc[mask].copy()

if f.empty:
    st.warning(
        "No records match the selected filters. Please widen your filters."
    )
    st.stop()


# =========================================================
# PREPARED DATA
# =========================================================

orders_df = f.drop_duplicates("order_id")

monthly = (
    f.groupby("month", as_index=False)
    .agg(revenue=("revenue", "sum"))
)

monthly_orders = (
    orders_df.groupby("month", as_index=False)
    .agg(orders=("order_id", "nunique"))
)

cat_rev = (
    f.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

state_rev = (
    f.groupby("customer_state")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

by_state = (
    orders_df.groupby("customer_state")
    .agg(
        orders=("order_id", "count"),
        late_pct=("is_late", "mean"),
        avg_days=("delivery_days", "mean"),
    )
    .reset_index()
)

by_state["late_pct"] *= 100

by_state = by_state[
    by_state["orders"] >= 100
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

revenue = f["revenue"].sum()

orders = orders_df["order_id"].nunique()

aov = revenue / orders if orders else 0

late_pct = (
    orders_df["is_late"].mean() * 100
    if orders
    else 0
)

avg_delivery = (
    orders_df["delivery_days"].mean()
    if orders
    else 0
)

growth = None

if len(monthly) >= 2:

    previous = monthly.iloc[-2]["revenue"]
    current = monthly.iloc[-1]["revenue"]

    if previous != 0:
        growth = (current / previous - 1) * 100


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="top-header">

        <div>
            <div class="page-title">
                {page}
            </div>

            <div class="page-subtitle">
                Olist e-commerce performance at a glance
            </div>
        </div>

        <div class="status-pill">
            ● LIVE ANALYSIS
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# KPI CARD FUNCTION
# =========================================================

def kpi(column, label, value, note, icon):

    with column:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-top">

                    <div class="kpi-label">
                        {label}
                    </div>

                    <div class="kpi-icon">
                        {icon}
                    </div>

                </div>

                <div class="kpi-value">
                    {value}
                </div>

                <div class="kpi-note">
                    {note}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# KPI ROW
# =========================================================

k1, k2, k3, k4, k5 = st.columns(5)

kpi(
    k1,
    "Revenue",
    f"R$ {revenue:,.0f}",
    "Filtered item revenue",
    "R",
)

kpi(
    k2,
    "Orders",
    f"{orders:,}",
    "Unique delivered orders",
    "O",
)

kpi(
    k3,
    "Avg Order Value",
    f"R$ {aov:,.0f}",
    "Revenue per order",
    "A",
)

kpi(
    k4,
    "MoM Growth",
    f"{growth:+.1f}%" if growth is not None else "N/A",
    "Latest vs previous month",
    "%",
)

kpi(
    k5,
    "Late Delivery",
    f"{late_pct:.1f}%",
    f"Avg. delivery {avg_delivery:.1f} days",
    "D",
)


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# CHART THEME
# =========================================================

def chart_style(fig, height=330):

    fig.update_layout(
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT,
        ),
        margin=dict(
            l=10,
            r=10,
            t=45,
            b=10,
        ),
        title=dict(
            font=dict(
                size=14,
                color=TEXT,
            ),
            x=0,
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(
            size=10,
            color=MUTED,
        ),
    )

    fig.update_yaxes(
        gridcolor="#F1F5F9",
        zeroline=False,
        tickfont=dict(
            size=10,
            color=MUTED,
        ),
    )

    return fig


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    # -----------------------------------------------------
    # ROW 1
    # -----------------------------------------------------

    left, right = st.columns([1.75, 1])

    with left:

        fig = px.area(
            monthly,
            x="month",
            y="revenue",
        )

        fig.update_traces(
            line=dict(
                color=INDIGO,
                width=3,
            ),
            fillcolor="rgba(79,70,229,0.10)",
            hovertemplate="R$ %{y:,.0f}<extra></extra>",
        )

        fig.update_layout(
            title="Revenue Trend",
            xaxis_title=None,
            yaxis_title=None,
        )

        st.markdown(
            """
            <div class="section-card">
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            chart_style(fig, 345),
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        top_cat = (
            cat_rev.head(7)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            top_cat,
            x="revenue",
            y="category",
            orientation="h",
        )

        fig.update_traces(
            marker_color=BLUE,
            hovertemplate="R$ %{x:,.0f}<extra></extra>",
        )

        fig.update_layout(
            title="Top Categories",
            xaxis_title=None,
            yaxis_title=None,
        )

        st.plotly_chart(
            chart_style(fig, 345),
            use_container_width=True,
            config={"displayModeBar": False},
        )


    # -----------------------------------------------------
    # ROW 2
    # -----------------------------------------------------

    left, right = st.columns(2)

    with left:

        top_state = (
            state_rev.head(10)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            top_state,
            x="revenue",
            y="customer_state",
            orientation="h",
        )

        fig.update_traces(
            marker_color=INDIGO,
            hovertemplate="R$ %{x:,.0f}<extra></extra>",
        )

        fig.update_layout(
            title="Revenue by State",
            xaxis_title="Revenue (R$)",
            yaxis_title=None,
        )

        st.plotly_chart(
            chart_style(fig, 330),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:

        fig = px.line(
            monthly_orders,
            x="month",
            y="orders",
            markers=True,
        )

        fig.update_traces(
            line=dict(
                color=NAVY_2,
                width=3,
            ),
            marker=dict(size=6),
            hovertemplate="%{y:,} orders<extra></extra>",
        )

        fig.update_layout(
            title="Order Volume",
            xaxis_title=None,
            yaxis_title="Orders",
        )

        st.plotly_chart(
            chart_style(fig, 330),
            use_container_width=True,
            config={"displayModeBar": False},
        )


# =========================================================
# SALES PERFORMANCE
# =========================================================

elif page == "Sales Performance":

    st.markdown(
        """
        <div class="section-card">
        """,
        unsafe_allow_html=True,
    )

    category_data = (
        f.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    category_data["aov"] = (
        category_data["revenue"]
        / category_data["orders"]
    )

    fig = px.bar(
        category_data.head(15).sort_values("revenue"),
        x="revenue",
        y="category",
        orientation="h",
    )

    fig.update_traces(
        marker_color=INDIGO,
        hovertemplate="R$ %{x:,.0f}<extra></extra>",
    )

    fig.update_layout(
        title="Category Revenue Performance",
        xaxis_title="Revenue (R$)",
        yaxis_title=None,
    )

    st.plotly_chart(
        chart_style(fig, 500),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
        """,
        unsafe_allow_html=True,
    )

    display = category_data.copy()

    display["revenue"] = display["revenue"].map(
        lambda x: f"R$ {x:,.0f}"
    )

    display["aov"] = display["aov"].map(
        lambda x: f"R$ {x:,.0f}"
    )

    display.columns = [
        "Category",
        "Revenue",
        "Orders",
        "Avg Order Value",
    ]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# DELIVERY ANALYTICS
# =========================================================

elif page == "Delivery Analytics":

    left, right = st.columns(2)

    with left:

        if by_state.empty:

            st.info(
                "Not enough orders per state for delivery comparison."
            )

        else:

            worst = (
                by_state
                .sort_values("late_pct", ascending=False)
                .head(10)
            )

            fig = px.bar(
                worst,
                x="customer_state",
                y="late_pct",
            )

            fig.update_traces(
                marker_color=RED,
                hovertemplate="%{y:.1f}%<extra></extra>",
            )

            fig.update_layout(
                title="Highest Late-Delivery Rates",
                xaxis_title=None,
                yaxis_title="Late Orders (%)",
            )

            st.plotly_chart(
                chart_style(fig, 360),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    with right:

        if not by_state.empty:

            fig = px.scatter(
                by_state,
                x="avg_days",
                y="late_pct",
                size="orders",
                hover_name="customer_state",
            )

            fig.update_traces(
                marker=dict(
                    color=INDIGO,
                    opacity=0.78,
                ),
            )

            fig.update_layout(
                title="Delivery Time vs Late Rate",
                xaxis_title="Average Delivery Days",
                yaxis_title="Late Orders (%)",
            )

            st.plotly_chart(
                chart_style(fig, 360),
                use_container_width=True,
                config={"displayModeBar": False},
            )


    st.markdown("<br>", unsafe_allow_html=True)

    delivery = orders_df[
        orders_df["delivery_days"] <= 60
    ]

    fig = px.histogram(
        delivery,
        x="delivery_days",
        nbins=40,
    )

    fig.update_traces(
        marker_color=BLUE,
    )

    fig.update_layout(
        title="Delivery Time Distribution",
        xaxis_title="Delivery Days",
        yaxis_title="Orders",
    )

    st.plotly_chart(
        chart_style(fig, 350),
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "Business Insights":

    peak_month = monthly.loc[
        monthly["revenue"].idxmax(),
        "month",
    ]

    peak_revenue = monthly["revenue"].max()

    top_category = cat_rev.index[0]
    top_category_revenue = cat_rev.iloc[0]

    top_state = state_rev.index[0]
    top_state_revenue = state_rev.iloc[0]

    top5_share = (
        cat_rev.head(5).sum() / revenue * 100
        if revenue
        else 0
    )

    # -----------------------------------------------------
    # SUMMARY CARD
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="section-card">

            <div class="card-title">
                Executive Summary
            </div>

            <div class="card-subtitle">
                Key observations generated from the selected data.
            </div>

            <br>

            <div class="insight">

                <div class="insight-title">
                    Revenue leader
                </div>

                <div class="insight-text">
                    {top_category.title()} is the strongest revenue
                    category, contributing R$ {top_category_revenue:,.0f}
                    ({top_category_revenue / revenue:.1%}) of filtered revenue.
                </div>

            </div>

            <div class="insight">

                <div class="insight-title">
                    Geographic concentration
                </div>

                <div class="insight-text">
                    {top_state} generates the highest revenue contribution
                    at R$ {top_state_revenue:,.0f}
                    ({top_state_revenue / revenue:.1%}).
                </div>

            </div>

            <div class="insight">

                <div class="insight-title">
                    Category concentration
                </div>

                <div class="insight-text">
                    The top five categories contribute
                    {top5_share:.1f}% of filtered revenue.
                </div>

            </div>

            <div class="insight">

                <div class="insight-title">
                    Peak revenue period
                </div>

                <div class="insight-text">
                    {peak_month:%B %Y} recorded the highest monthly revenue
                    at R$ {peak_revenue:,.0f}.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # DELIVERY INSIGHT
    # -----------------------------------------------------

    if not by_state.empty:

        worst = by_state.sort_values(
            "late_pct",
            ascending=False,
        ).iloc[0]

        best = by_state.sort_values(
            "late_pct",
            ascending=True,
        ).iloc[0]

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="section-card">

                <div class="card-title">
                    Delivery Risk Signals
                </div>

                <div class="card-subtitle">
                    Geographic comparison using states with at least
                    100 orders.
                </div>

                <br>

                <div class="insight">

                    <div class="insight-title">
                        Highest delivery risk
                    </div>

                    <div class="insight-text">
                        {worst["customer_state"]} has the highest observed
                        late-delivery rate at {worst["late_pct"]:.1f}%,
                        with an average delivery time of
                        {worst["avg_days"]:.1f} days.
                    </div>

                </div>

                <div class="insight">

                    <div class="insight-title">
                        Strongest delivery benchmark
                    </div>

                    <div class="insight-text">
                        {best["customer_state"]} has the lowest observed
                        late-delivery rate at {best["late_pct"]:.1f}%.
                    </div>

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
        Olist Brazilian E-Commerce Public Dataset ·
        Delivered orders · Jan 2017 – Aug 2018 ·
        Revenue = item price, excluding freight
    </div>
    """,
    unsafe_allow_html=True,
    )
