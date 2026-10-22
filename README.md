# Olist Sales Insights

### Sales Analytics & Revenue Intelligence Dashboard

An interactive **sales analytics dashboard** built with Python and Streamlit to transform transactional e-commerce data into actionable insights around **revenue, orders, product categories, regional performance, and delivery operations**.

The project focuses on answering a practical business question:

> **Where is revenue coming from, what is driving sales performance, and where should the business take action?**

🔗 **Live Dashboard:** https://olist-sales-insights-wk64yswh3kzjfehtns229w.streamlit.app/

---

## 📌 Business Problem

E-commerce businesses generate large volumes of transactional data, but raw order data does not directly explain business performance.

A sales team or business manager needs to quickly understand:

- How much revenue is being generated?
- Is revenue growing or declining over time?
- Which product categories contribute the most revenue?
- Which regions are performing strongly?
- What happens to sales when deliveries are delayed?
- Which areas require management attention?

Without a centralized analytical view, these questions require manually combining and analyzing multiple datasets.

### The objective of this project

Build a **decision-oriented sales analytics dashboard** that converts raw Olist transaction data into clear business insights that can support revenue monitoring, category planning, regional analysis, and operational decisions.

---

# 🎯 Project Objectives

The dashboard was designed to:

- Monitor overall sales performance
- Track revenue and order trends
- Analyze Average Order Value (AOV)
- Identify high-performing and underperforming categories
- Compare regional sales performance
- Analyze category revenue concentration
- Monitor delivery performance
- Understand the relationship between delivery delays and sales
- Generate actionable business recommendations

---

# 📊 Dashboard Features

## 1. Executive Sales Overview

Provides a high-level view of business performance.

### Key KPIs

- Total Revenue
- Total Orders
- Average Order Value
- Monthly Revenue
- Revenue Growth
- Sales Trends

The overview helps decision-makers understand the current state of the business before moving into deeper analysis.

---

## 2. Revenue Insights

Analyzes how revenue changes over time and across business dimensions.

### Key Analysis

- Monthly revenue trends
- Month-over-month revenue growth
- Revenue concentration
- Category contribution
- Regional revenue performance
- Growing and declining categories

This section helps identify where revenue is increasing and where performance may require attention.

---

## 3. Sales & Category Performance

Examines product-category performance from a sales perspective.

### Key Analysis

- Top-performing categories
- Lowest-performing categories
- Revenue by category
- Orders by category
- Average Order Value
- Category growth
- Revenue concentration / Pareto analysis

This helps identify the categories that contribute most significantly to overall sales.

---

## 4. Delivery Operations

Connects operational performance with sales outcomes.

### Key Analysis

- Average delivery time
- On-time vs delayed deliveries
- Revenue associated with delayed orders
- AOV comparison
- Regional delivery performance
- Delivery performance by state
- Review performance where review data is available

The goal is not simply to monitor logistics, but to understand how operational issues can affect the customer experience and commercial performance.

---

## 5. Business Insights

The final section converts analysis into decision-oriented recommendations.

Instead of only displaying charts, the dashboard highlights areas such as:

- Revenue opportunities
- Category performance issues
- Regional opportunities
- Delivery risk
- Areas requiring management attention

This makes the dashboard more useful as a **business decision-support tool** rather than simply a visualization project.

---

# 🧠 Key Business Questions

The dashboard is designed to answer questions such as:

### Revenue
- Is revenue increasing or declining?
- Which periods generated the strongest sales?
- How concentrated is revenue across categories?

### Sales
- Which categories drive the most revenue?
- Which categories have weaker performance?
- How does Average Order Value change over time?

### Regional Performance
- Which states generate the most sales?
- Are there regions with strong order volume but weaker revenue?

### Operations
- How frequently are orders delivered late?
- Which regions have higher delivery risk?
- How much revenue is associated with delayed orders?

### Decision Making
- Where should management focus attention?
- Which categories deserve further investigation?
- Which operational areas may represent a business risk?

---

# 📁 Dataset

The project uses the **Brazilian Olist e-commerce dataset**, containing transactional information related to orders, products, customers, categories, delivery, and reviews.

The analysis combines multiple datasets to create a unified analytical layer.

### Main data sources

- Orders
- Order items
- Customers
- Products
- Product category translation
- Order reviews

---

# 🔄 Data Preparation

The data pipeline performs several preparation steps before analysis:

1. Loads multiple Olist datasets
2. Filters for delivered orders
3. Removes records without delivery dates where required
4. Joins order, item, customer, and product information
5. Translates product categories into English
6. Creates monthly time periods
7. Calculates revenue
8. Calculates delivery duration
9. Identifies late deliveries
10. Integrates review scores when available
11. Creates an analysis-ready dataset

This creates a consistent data layer for the dashboard.

---

# 🛠️ Tech Stack

### Programming & Analysis

- Python
- Pandas
- NumPy

### Visualization

- Plotly

### Dashboard

- Streamlit

### Development

- Jupyter Notebook
- Git
- GitHub

---

# 📐 Key Metrics

### Revenue

Revenue is calculated from product price at the transaction level.

### Orders

Orders are calculated using unique order IDs to avoid double-counting orders containing multiple products.

### Average Order Value

```text
AOV = Total Revenue / Total Orders
```

### Month-over-Month Growth

```text
MoM Growth =
(Current Month Revenue - Previous Month Revenue)
/
Previous Month Revenue × 100
```

### Delivery Days

```text
Delivery Days =
Delivered Date - Purchase Date
```

### Late Delivery

An order is classified as late when the actual delivery date exceeds the estimated delivery date.

---

# 🏗️ Project Structure

```text
olist-sales-insights/
│
├── app.py
├── data.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   └── product_category_name_translation.csv
│
└── assets/
    └── dashboard screenshots
```

---

# 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/jahnavi06in/olist-sales-insights.git
```

### 2. Move into the project folder

```bash
cd olist-sales-insights
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

# 🌐 Live Application

Try the interactive dashboard:

**https://olist-sales-insights-wk64yswh3kzjfehtns229w.streamlit.app/**

---

# 💼 Business Value

This project demonstrates how transactional data can be transformed into a practical business intelligence workflow:

```text
Raw Transaction Data
        ↓
Data Cleaning & Integration
        ↓
Metric Engineering
        ↓
Exploratory Analysis
        ↓
Interactive Dashboard
        ↓
Business Insights
        ↓
Decision Support
```

The focus is on moving beyond simply creating charts and instead building an analytical product that helps users understand **what happened, where it happened, and where action may be required**.

---

# 🎓 Skills Demonstrated

### Data Analytics

- Data cleaning
- Data transformation
- Exploratory Data Analysis
- KPI development
- Trend analysis
- Revenue analysis
- Category analysis
- Regional analysis
- Operational analysis

### Business Intelligence

- Dashboard development
- Interactive filtering
- KPI monitoring
- Business storytelling
- Decision-oriented reporting

### Technical

- Python
- Pandas
- Plotly
- Streamlit
- Git
- GitHub

---

# 🔮 Future Improvements

Potential future enhancements include:

- Automated sales forecasting
- Customer-level revenue analysis
- Advanced anomaly detection
- More granular product analysis
- Automated dashboard alerts
- Scheduled data refresh
- Additional payment and customer behavior analysis

These improvements would extend the dashboard from descriptive analytics toward more advanced predictive and prescriptive capabilities.

---

# 👩‍💻 Author

**Jahnavi J**

BCA Student | Aspiring Data Analyst / Business Analyst

Focused on building practical analytics projects using **Python, SQL, Power BI, Tableau, Excel, and Streamlit**.

---

## ⭐ Project Highlights

**Olist Sales Insights** demonstrates an end-to-end analytics workflow:

**Data → Analysis → Visualization → Business Insight → Decision Support**

If you find the project useful, consider giving the repository a ⭐ on GitHub.
