# 📊 Olist Sales Insights

### Sales Analytics & Revenue Intelligence Dashboard

An interactive sales analytics and business intelligence dashboard built with **Python, Pandas, Plotly, and Streamlit** to transform real-world e-commerce transaction data into clear, actionable business insights.

The dashboard helps analyze **revenue performance, order activity, category performance, regional sales, delivery operations, and business opportunities** through an interactive analytical interface.

🔗 **Live Dashboard:** https://olist-sales-insights-wk64yswh3kzjfehtns229w.streamlit.app/

---

## 📸 Dashboard Preview

<p align="center">
  <img src="./dashboard%20olist.png.png" alt="Olist Sales Insights Dashboard" width="100%">
</p>

### Executive Sales Overview

The dashboard brings key sales and operational metrics together in one place, allowing users to monitor revenue, orders, Average Order Value, delivery performance, revenue trends, category performance, and business insights.

---

# 🎯 Business Problem

E-commerce businesses generate large volumes of transactional data across products, categories, customers, regions, orders, and delivery operations.

However, raw transaction data does not directly answer the questions that business teams need to make decisions:

- Which categories are driving revenue?
- Is sales performance improving or declining?
- Which regions contribute the most sales?
- Where are potential revenue opportunities?
- Are delivery delays creating operational risk?
- Which areas require management attention?

When these questions require manually combining multiple datasets and reports, it becomes difficult to identify important trends quickly.

### The Core Problem

> How can raw e-commerce transaction data be transformed into a centralized, interactive analytical system that helps business teams understand sales performance and make faster, data-driven decisions?

---

# 💡 Solution

**Olist Sales Insights** addresses this problem by combining multiple Olist datasets into a structured analytical layer and presenting the results through an interactive Streamlit dashboard.

The solution provides a centralized view of:

### 📈 Revenue Performance

- Total Revenue
- Monthly Revenue
- Revenue Trends
- Month-over-Month Growth
- Average Order Value
- Revenue Contribution

### 🛍️ Category Performance

- Top-performing categories
- Underperforming categories
- Category revenue
- Order volume
- Category growth
- Revenue concentration
- Pareto analysis

### 🌎 Regional Sales Performance

Compare customer states to identify:

- High-revenue regions
- High-order regions
- Regional performance differences
- Areas requiring further investigation

### 🚚 Delivery & Operational Performance

- Delivery duration
- On-time vs late deliveries
- Late-delivery rate
- Revenue associated with delayed orders
- Regional delivery performance
- Review performance where available

### 🎯 Business Decision Support

The dashboard goes beyond displaying charts by providing a **Quick Business Read** that highlights important findings and areas requiring attention.

**Data → Analysis → Insight → Decision**

---

# 📊 Dashboard Features

## 1. Executive Sales Overview

A management-level summary of overall business performance.

**Key Metrics**

- Total Revenue
- Total Orders
- Average Order Value
- Late Delivery Rate
- Revenue Trends
- Order Activity

**Business value:** Provides a fast overview of the overall sales and operational picture.

---

## 2. Revenue Insights

Analyzes how revenue changes across time and business dimensions.

**Analysis Includes**

- Monthly revenue trends
- Month-over-month growth
- Revenue contribution
- Category performance
- Regional revenue performance
- Strong and weak revenue periods

**Business value:** Helps identify revenue growth patterns and periods requiring attention.

---

## 3. Sales & Category Performance

Examines sales performance across product categories.

**Analysis Includes**

- Top-performing categories
- Lower-performing categories
- Category revenue
- Order volume
- Average Order Value
- Category growth
- Revenue concentration
- Pareto analysis

**Business value:** Helps identify which categories are driving sales and where performance may be weaker.

---

## 4. Delivery Operations

Connects delivery performance with sales and customer outcomes.

**Analysis Includes**

- Average delivery time
- On-time vs delayed orders
- Late-delivery rate
- Revenue associated with delayed orders
- Regional delivery performance
- Delivery performance by state
- Review performance where available

**Business value:** Helps identify operational areas that may affect customer experience and business performance.

---

## 5. Business Insights

The dashboard converts analytical findings into decision-oriented observations.

### Quick Business Read

Highlights:

- Strong revenue periods
- Delivery exposure
- Order economics
- Sales opportunities
- Areas requiring further investigation

**Business value:** Bridges the gap between visualization and business decision-making.

---

# 🧠 Key Business Questions

| Business Question | Analytical Solution |
|---|---|
| How are sales performing? | Revenue, order, AOV and KPI monitoring |
| Is revenue growing or declining? | Monthly revenue and growth analysis |
| Which categories drive sales? | Category revenue and order analysis |
| Where does revenue come from? | Regional and category analysis |
| Which categories need attention? | Category performance and growth comparisons |
| Are delivery delays a risk? | Delivery-time and late-order analysis |
| What should management investigate? | Business insights and recommendations |

---

# 🔄 Data-to-Decision Workflow

```text
Raw Olist Transaction Data
            ↓
Data Cleaning & Integration
            ↓
Metric Engineering
            ↓
Sales & Revenue Analysis
            ↓
Interactive Visualization
            ↓
Business Insights
            ↓
Decision Support
```

---

# 📁 Dataset

The project uses the **Brazilian Olist E-commerce Dataset**, a real-world transactional dataset containing information about orders, products, customers, categories, deliveries, and reviews.

### Main Data Sources

- Orders
- Order Items
- Customers
- Products
- Product Category Translation
- Order Reviews

Multiple datasets are joined and transformed into an analysis-ready structure before being used by the dashboard.

---

# 🧹 Data Preparation

The data pipeline performs the following steps:

1. Loads multiple Olist datasets
2. Filters for delivered orders
3. Removes records without required delivery dates
4. Joins order, item, customer, and product information
5. Translates product categories into English
6. Creates monthly time periods
7. Calculates transaction-level revenue
8. Calculates delivery duration
9. Identifies late deliveries
10. Integrates review scores when available
11. Produces a structured dataset for analysis

---

# 📐 Key Metrics

### Total Revenue

Calculated from product transaction prices within the selected analysis period.

### Orders

Unique order IDs are used for order-level KPIs to avoid double-counting orders containing multiple items.

### Average Order Value

```text
AOV = Total Revenue / Total Orders
```

### Month-over-Month Revenue Growth

```text
MoM Growth =
(Current Month Revenue - Previous Month Revenue)
/
Previous Month Revenue × 100
```

### Delivery Days

```text
Delivery Days =
Actual Delivery Date - Purchase Date
```

### Late Delivery

An order is classified as late when:

```text
Actual Delivery Date > Estimated Delivery Date
```

---

# 🛠️ Technology Stack

### Programming & Data Analysis

- Python
- Pandas
- NumPy

### Visualization

- Plotly

### Dashboard

- Streamlit

### Development & Version Control

- Jupyter Notebook
- Git
- GitHub

---

# 🏗️ Project Structure

```text
olist-sales-insights/
│
├── app.py
├── data.py
├── README.md
├── requirements.txt
├── config.toml
├── satisfaction_page.py
│
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   └── product_category_name_translation.csv
│
└── dashboard olist.png.png
```

---

# 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jahnavi06in/olist-sales-insights.git
```

### 2. Open the project directory

```bash
cd olist-sales-insights
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
streamlit run app.py
```

---

# 🌐 Live Application

Experience the interactive dashboard:

https://olist-sales-insights-wk64yswh3kzjfehtns229w.streamlit.app/

---

# 💼 Business Value

This project demonstrates an end-to-end **Data Analytics and Business Intelligence workflow**.

It shows how raw transactional data can be transformed into a decision-support solution:

```text
Raw Data
   ↓
Cleaning
   ↓
Transformation
   ↓
KPI Development
   ↓
Exploratory Analysis
   ↓
Interactive Dashboard
   ↓
Business Insights
   ↓
Decision Support
```

The project focuses on answering three practical questions:

### What happened?

Understand revenue, orders, categories, regions, and delivery performance.

### Where did it happen?

Identify categories, regions, and operational areas contributing to performance changes.

### Where should attention go?

Use analytical findings to identify opportunities, risks, and areas requiring further investigation.

---

# 🎓 Skills Demonstrated

### Data Analytics

- Data cleaning
- Data transformation
- Exploratory Data Analysis
- KPI development
- Revenue analysis
- Trend analysis
- Category analysis
- Regional analysis
- Operational analysis

### Business Intelligence

- Interactive dashboard development
- KPI monitoring
- Data visualization
- Business storytelling
- Decision-oriented reporting
- Insight generation

### Technical

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Git
- GitHub

---

# 🔮 Future Enhancements

Potential future improvements include:

- Sales forecasting
- Automated anomaly detection
- Customer-level revenue analysis
- Product-level performance analysis
- Automated alerts for revenue declines
- Scheduled data refresh
- Additional payment and customer behavior analysis

These enhancements could extend the project from descriptive analytics toward more advanced predictive and prescriptive analytics.

---

# 👩‍💻 Author

## Jahnavi J

**BCA Student | Aspiring Data Analyst / Business Analyst**

Interested in building practical analytics solutions using:

**Python • SQL • Power BI • Tableau • Excel • Pandas • Streamlit**

---

# ⭐ Project Summary

**Olist Sales Insights** transforms real-world e-commerce transactions into an interactive sales analytics platform for monitoring:

**Revenue → Sales → Categories → Regions → Delivery → Business Insights**

The project demonstrates how raw business data can be transformed into a clear, interactive, and decision-oriented analytics solution.
