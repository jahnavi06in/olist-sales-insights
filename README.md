# Olist Sales Insights

### Revenue & Sales Analytics Dashboard | Python • Pandas • Plotly • Streamlit

> **Turning transactional e-commerce data into clear sales insights and actionable business decisions.**

---

## 📌 Business Problem

E-commerce businesses generate thousands of transactions, but raw transaction data does not immediately explain **what is driving sales, where revenue is growing, which categories need attention, or where operational problems may affect revenue.**

A business team needs answers to questions such as:

- Which categories generate the most revenue?
- Which categories are growing or declining?
- Which categories have high order volume but low average order value?
- Which customer states contribute the most revenue?
- How concentrated is overall revenue?
- How do late deliveries affect revenue?
- Which regions have strong sales but operational risk?
- Where are the biggest revenue opportunities?
- What actions should management prioritize?

### Core Business Challenge

**How can raw e-commerce transaction data be transformed into meaningful sales insights that support revenue growth, category strategy, and operational decision-making?**

---

# 💡 Solution

**Olist Sales Insights** is an interactive sales analytics dashboard built to transform raw Olist e-commerce data into meaningful business insights.

The project integrates and analyzes transactional, customer, product, category, delivery, and review information to provide a consolidated view of:

- Revenue performance
- Order performance
- Category performance
- Customer geography
- Average order value
- Revenue growth
- Delivery performance
- Revenue concentration
- Business opportunities
- Business risks

Instead of simply displaying charts, the dashboard focuses on answering:

> **What happened? Why does it matter? What should the business look at next?**

---

# 🏗️ Solution Architecture

```text
OLIST E-COMMERCE DATA
        ↓
DATA INTEGRATION
        ↓
DATA CLEANING & PREPARATION
        ↓
BUSINESS METRIC DEVELOPMENT
        ↓
┌─────────────────────────────┐
│ Revenue Insights            │
│ Sales & Category Insights   │
│ Geographic Insights         │
│ Delivery Insights           │
│ Business Insights           │
└─────────────────────────────┘
        ↓
ACTIONABLE BUSINESS INSIGHTS
        ↓
DECISION SUPPORT
```

---

# 📊 Dashboard Modules

## 1. Executive Overview

Provides a high-level view of overall sales performance.

### Key KPIs

- Total Revenue
- Total Orders
- Average Order Value
- Late Delivery Rate

### Analysis

- Monthly revenue trend
- Revenue by category
- Geographic sales performance
- Top-performing categories
- Delivery performance
- Executive-level observations

### Business Use

Helps management quickly understand the current sales position without going through raw transactional data.

---

# 2. Revenue Insights

Focuses on understanding revenue movement and concentration.

### Analysis Includes

- Monthly revenue trend
- Month-over-month revenue growth
- Peak revenue period
- Revenue per order
- Category revenue contribution
- Top category concentration
- Revenue growth opportunities

### Business Questions

- When was revenue strongest?
- Is revenue increasing or declining?
- Which categories contribute most to revenue?
- Is revenue heavily dependent on a small number of categories?

---

# 3. Sales & Category Insights

Analyzes product-category performance from both **volume and value perspectives**.

### Metrics

- Category Revenue
- Number of Orders
- Average Order Value
- Revenue Share
- Category Growth

### Category Performance Matrix

Categories are evaluated using order volume and average order value.

| Category Type | Business Interpretation |
|---|---|
| High Volume + High Value | Protect and scale |
| High Volume + Low Value | Improve basket value |
| Low Volume + High Value | Investigate demand generation |
| Low Volume + Low Value | Review pricing, positioning or inventory |

This helps move beyond simply identifying the "top category."

---

# 4. Delivery Operations

Analyzes the relationship between delivery performance and sales.

### Metrics

- Late Delivery Rate
- Average Delivery Time
- Revenue from Late Orders
- On-Time vs Late Orders
- State-level delivery performance

### Business Insight

A region with strong revenue but poor delivery performance can represent a **commercial risk**, because operational problems may eventually affect customer experience and future sales.

The dashboard therefore connects operational performance with revenue rather than treating delivery as an isolated metric.

---

# 5. Business Insights

The final layer converts analysis into business-oriented observations.

### Example Insight Areas

**Revenue Protection**

Identify categories and regions that contribute significantly to overall revenue.

**Revenue Expansion**

Identify categories with strong order volume but relatively low average order value.

**Operational Improvement**

Identify high-revenue regions experiencing elevated late-delivery rates.

**Revenue Risk**

Identify situations where a large percentage of revenue depends on a limited number of categories or regions.

---

# 📈 Analytical Approach

The project follows a structured analytics workflow:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Data Integration
   ↓
KPI Development
   ↓
Descriptive Analysis
   ↓
Diagnostic Analysis
   ↓
Opportunity & Risk Identification
   ↓
Business Recommendations
```

The goal is not just to create visualizations.

The goal is to **translate transaction-level data into business understanding.**

---

# 📐 Key Business Metrics

### Total Revenue

```text
Total Revenue = Sum of Order Revenue
```

### Average Order Value

```text
AOV = Total Revenue / Total Orders
```

### Revenue Share

```text
Revenue Share = Category Revenue / Total Revenue × 100
```

### Month-over-Month Growth

```text
MoM Growth =
(Current Month Revenue - Previous Month Revenue)
/
Previous Month Revenue × 100
```

### Late Delivery Rate

```text
Late Delivery Rate =
Late Orders / Total Orders × 100
```

---

# 🛠️ Technology Stack

### Programming & Analysis

- Python
- Pandas
- NumPy

### Visualization

- Plotly
- Interactive charts
- KPI dashboards

### Application

- Streamlit

### Data Sources

- Olist Brazilian E-Commerce Dataset
- Orders
- Order Items
- Customers
- Products
- Product Categories
- Reviews
- Delivery information

### Development

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

# 📁 Project Structure

```text
olist-sales-insights/
│
├── app.py
├── data.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── orders.csv
│   ├── order_items.csv
│   ├── customers.csv
│   ├── products.csv
│   └── ...
│
└── assets/
    └── dashboard screenshots
```

---

# 🎯 Business Impact

| Analysis | Business Value |
|---|---|
| Revenue Trends | Understand sales movement |
| Category Analysis | Identify strong and weak categories |
| AOV Analysis | Identify basket-value opportunities |
| Geographic Analysis | Compare regional performance |
| Revenue Concentration | Identify dependency risks |
| Delivery Analysis | Detect operational risks |
| Business Insights | Support prioritization |

---

# 🚀 What This Project Demonstrates

This project demonstrates practical skills across the **Data Analytics lifecycle**:

- Data cleaning
- Data integration
- Exploratory data analysis
- KPI development
- Revenue analysis
- Sales analysis
- Category analysis
- Geographic analysis
- Operational analysis
- Data visualization
- Business interpretation
- Dashboard development
- Decision-oriented reporting

More importantly, it demonstrates the ability to move from:

**Data → Analysis → Insight → Business Action**

---

# 🔮 Future Enhancements

Potential extensions include:

- SQL-based analytical layer
- Automated KPI alerts
- Revenue forecasting
- Customer lifetime value analysis
- Cohort analysis
- Customer segmentation
- Automated reporting
- Cloud data warehouse integration
- Scheduled dashboard refresh

---

# 👩‍💻 Author

**Jahnavi J**

BCA | Data Analytics & Business Intelligence

Interested in **Data Analytics, Business Analytics, SQL, Python, and Business Intelligence.**

---

# ⭐ Project Philosophy

> **A basic dashboard tells you what happened.  
> A strong analytics project explains why it matters.  
> A business-focused dashboard helps identify what should be looked at next.**

**Olist Sales Insights** is built around this approach.
