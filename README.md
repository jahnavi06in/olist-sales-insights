# 📊 Olist Sales Insights

An interactive analytics dashboard that turns **96,203 delivered e-commerce orders** into clear commercial and operational decisions: what sells, where it sells, and where deliveries are failing.

**🔗 Live demo:** [https://olist-sales-insights-wk64yswh3kzjfehtns229w.streamlit.app/](https://olist-sales-insights-wk64yswh3kzjfehtns229w.streamlit.app/)

![Dashboard overview](assets/dashboard.png)

---

## ❗ Business Problem

### Context
Olist is a Brazilian marketplace that connects thousands of small sellers with customers across the country. Every order creates data: what was bought, who bought it, where it was delivered and whether it arrived on time. That data is spread across several raw tables, so it is hard for non-technical managers to use.

### The Problem
Leadership needs fast, reliable answers, but the raw data makes that slow. This leads to four specific problems:

| # | Problem | Why it matters |
|---|---|---|
| 1 | **No clear view of what drives revenue** | Teams cannot tell which categories and states earn the most, so stock, marketing and promotion decisions rely on guesswork. |
| 2 | **Hidden revenue concentration** | If a few categories or states generate most of the income, the business is exposed when demand drops in any of them. |
| 3 | **Delivery problems are not visible by region** | Late deliveries hurt customer trust and repeat purchases, but without a state-by-state view nobody knows where to act first. |
| 4 | **Slow, manual reporting** | Analysts spend hours in spreadsheets answering the same questions, and managers wait for answers. |

### Who Is Affected
- **Category and merchandising managers:** need to know what to stock and promote
- **Operations and logistics teams:** need to know where deliveries are failing
- **Executives:** need a quick, trustworthy view of overall performance

## ✅ Solution

### Approach
I turned the raw order data into a single interactive dashboard in four steps:

1. **Prepare the data:** combine order, item, customer, product and delivery information into one clean, analysis-ready table, and fix missing or inconsistent values.
2. **Define the metrics:** revenue, orders, average order value, late delivery rate and delivery time, each with a clear definition (see Metric Definitions below).
3. **Build the dashboard:** a multi-page Streamlit app with filters for period, state and category, so users can explore without writing any code.
4. **Add decision support:** auto-generated insights and a recommended action, so the dashboard says what to do next as well as what happened.

### How the Dashboard Solves Each Problem

| Problem | Dashboard feature | What it reveals |
|---|---|---|
| No clear view of revenue drivers | Top 10 categories, revenue mix, revenue by state map | **Health & Beauty** leads the categories and **São Paulo contributes 38.4%** of revenue |
| Hidden concentration | Concentration card and category ranking | **Top 5 categories generate 39.9%** of revenue, and **SP + RJ + MG are about 63%** |
| Delivery issues not visible by region | Late rate by state, delivery time vs late rate | **8.1%** of orders are late overall, but **14 states exceed 10%**, with **Alagoas worst at 24.0%** |
| Slow, manual reporting | KPI cards, month-over-month change, instant filters | Key numbers and trends in seconds, with no spreadsheet work |

### Outcome
A decision-maker can open one page and answer, in under a minute:
- What is our revenue and is it growing or shrinking?
- Which categories and states should we protect?
- Where are deliveries failing, and which state should we fix first?

Based on the findings, the project recommends protecting the top categories, reducing dependence on three states, and investigating carrier and estimate accuracy in the high-risk states, starting with Alagoas.

## 🎯 Business Questions

1. Which product categories and customer states drive revenue?
2. How concentrated is revenue, and is that a risk?
3. Where are deliveries running late, and how bad is it?
4. How is revenue moving month over month?

## 🔍 Key Findings

> Figures below are for the full period (2017–2018), delivered orders only.

| Metric | Result |
|---|---|
| Total revenue | **R$ 13.18M** across **96,203** orders |
| Average order value | **R$ 137** |
| Revenue concentration | Top 5 categories generate **39.9%** of revenue |
| #1 category | **Health & Beauty**, R$ 1.23M (9.3% of revenue) |
| Geographic concentration | **São Paulo = 38.4%** of revenue; SP + RJ + MG ≈ **63%** |
| Peak month | **Nov 2017**, R$ 987,648 (likely Black Friday season) |
| Late delivery rate | **8.1%** overall, but **14 states exceed 10%** |
| Worst late rate | **Alagoas (AL), 24.0%** |
| Average delivery time | **12.1 days** |

## 💡 Recommendations

- **Protect the leaders:** prioritise stock and promotions for Health & Beauty, Watches & Gifts and Bed Bath Table.
- **Reduce geographic dependency:** nearly two-thirds of revenue comes from three states; test growth in under-served regions.
- **Fix delivery in high-risk states:** review carrier and estimate accuracy in the 14 states above a 10% late rate, starting with AL.

## ✨ Dashboard Pages

| Page | What it shows |
|---|---|
| **Overview** | KPI cards with trends, revenue trend, category mix, state map, top 10 categories, delivery performance, key insights |
| **Revenue Intelligence** | Peak month, month-over-month movement, concentration, category ranking |
| **Sales & Categories** | Revenue vs order volume vs AOV, full category table |
| **Delivery Operations** | Late rate by state, delivery time vs lateness, delivery-time distribution |
| **Business Insights** | Auto-generated findings and recommended actions |

Filters: analysis period, customer states, product categories.

## 📐 Metric Definitions

- **Revenue:** sum of order revenue for delivered orders
- **Orders:** unique `order_id`
- **AOV:** revenue ÷ orders
- **Late delivery rate:** share of delivered orders that arrived after the estimated date
- **State delivery stats:** only states with at least 100 orders, to avoid misleading small samples
- **Change vs previous month:** latest month in the selected period compared with the month before it

## 🛠️ Tech Stack

Python · Pandas · Plotly · Streamlit · HTML/CSS (custom UI)

## 🧱 Project Structure

```
olist-sales-insights/
├── app.py              # Streamlit dashboard (UI, charts, pages)
├── data.py             # Data loading and preparation
├── data/               # Source data files
├── requirements.txt    # Dependencies
├── assets/             # Screenshots
└── .streamlit/         # Theme config
```

## 🚀 Run Locally

```bash
git clone https://github.com/jahnavi06in/olist-sales-insights.git
cd olist-sales-insights
pip install -r requirements.txt
streamlit run app.py
```

## 📦 Data

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle). Real, anonymised orders from a Brazilian marketplace.

## 🔮 Next Steps

- Add customer segmentation (RFM) and repeat-purchase analysis
- Add review-score analysis and its link to late deliveries
- Forecast monthly revenue

## 👩‍💻 Author

**Jahnavi** · BCA student aiming for data analyst roles
[LinkedIn](https://www.linkedin.com/in/jahnavi-j-508b97327) · [GitHub](https://github.com/jahnavi06in)
