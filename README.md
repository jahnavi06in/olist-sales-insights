# Olist Sales Intelligence

### Revenue & Sales Analytics Platform | Python • Pandas • Plotly • Streamlit

> **Turning transactional e-commerce data into revenue intelligence and actionable business decisions.**

---

## 🚨 Business Problem

E-commerce companies generate thousands of transactions across products, customers, locations, payments, and deliveries. However, raw transactional data does not immediately explain **where revenue is coming from, where performance is weakening, or what the business should do next.**

For the Olist e-commerce business, management needs answers to questions such as:

- Which product categories are driving the majority of revenue?
- Is revenue growing consistently or experiencing periods of decline?
- Which categories generate high order volume but relatively low revenue per order?
- Which customer states contribute the most commercial value?
- Is revenue overly dependent on a small number of categories?
- How much revenue is associated with delayed deliveries?
- Which regions have a combination of high revenue and operational risk?
- Where are the strongest opportunities to increase revenue?
- Which problems should management prioritize?

The challenge is therefore not simply **reporting sales numbers**.

The real challenge is:

> **How can raw e-commerce transactions be converted into insights that support revenue growth, category strategy, and operational decisions?**

---

# 💡 Business Solution

I built **Olist Sales Intelligence**, an interactive revenue and sales analytics platform that transforms multiple Olist transactional datasets into a decision-focused business dashboard.

The solution integrates and analyzes:

- Orders
- Order items
- Customers
- Products
- Product categories
- Delivery performance
- Customer reviews

The platform then converts this data into business metrics and analytical views covering:

### Revenue Performance
Identifies revenue trends, growth patterns, peak periods, and revenue concentration.

### Sales & Category Performance
Determines which categories drive revenue, which generate high order volume, and where average order value can be improved.

### Geographic Performance
Identifies high-value customer states and regional revenue concentration.

### Delivery Impact
Connects delivery performance with commercial exposure by measuring late orders and the revenue associated with them.

### Business Decision Support
Converts analytical findings into recommended actions such as:

- Protecting high-performing categories
- Increasing average order value
- Cross-selling complementary products
- Investigating high-risk regions
- Improving delivery performance
- Reducing revenue concentration risk

---

# 🎯 Solution Architecture

```text
                    OLIST DATASETS
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
      Orders           Products         Customers
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                   Data Integration
                          │
                   Data Preparation
                          │
                 Business Metrics
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
     Revenue          Categories        Operations
     Analysis          Analysis          Analysis
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                   Business Insights
                          │
                  Decision Support
```

---

# 📊 Dashboard

## 1. Executive Overview

Provides management with a high-level view of business performance.

### Key Metrics

- Total Revenue
- Total Orders
- Average Order Value
- Late Delivery Rate

### Questions Answered

> How much revenue did the business generate?

> How many orders were processed?

> What is the average revenue generated per order?

> Is delivery performance creating operational risk?

---

# 📈 2. Revenue Intelligence

The Revenue Intelligence module focuses on **revenue growth and concentration**.

### Analysis Includes

- Monthly revenue
- Month-over-month growth
- Peak revenue period
- Revenue per order
- Category revenue contribution
- Cumulative revenue contribution

### Business Use

Management can identify:

- Growth periods
- Declining periods
- Revenue concentration
- Revenue dependency on leading categories

### Decision Example

If a small number of categories generate a large percentage of total revenue, the business should prioritize:

**inventory availability + pricing + customer experience**

for those categories.

---

# 🏷️ 3. Sales & Category Intelligence

The Sales & Categories module evaluates the commercial strength of each product category.

Each category is analyzed using:

- Revenue
- Orders
- Average Order Value
- Revenue Share
- Volume
- Commercial position

### Category Performance Matrix

Categories are classified using order volume and AOV:

```text
                         HIGH AOV
                            ↑
                            │
       LOW VOLUME           │        HIGH VOLUME
       HIGH VALUE           │        HIGH VALUE
                            │
                            │
────────────────────────────┼────────────────────────→
                            │                  ORDERS
       LOW VOLUME           │        HIGH VOLUME
       LOW VALUE            │        LOW VALUE
                            │
                            ↓
                         LOW AOV
```

This helps identify four types of commercial situations:

### 🟢 High Volume + High Value

Strong commercial performers.

**Action:** Protect and scale.

### 🔵 High Volume + Low Value

Strong demand but weaker value per transaction.

**Action:** Explore bundles, cross-selling and premium alternatives.

### 🟠 Low Volume + High Value

Potentially valuable but under-penetrated categories.

**Action:** Investigate demand generation opportunities.

### 🔴 Low Volume + Low Value

Weak commercial performers.

**Action:** Review pricing, positioning, inventory or product relevance.

---

# 🚚 4. Delivery Operations

Delivery performance can directly affect customer experience and future revenue.

The Delivery Operations module measures:

- Average delivery time
- Median delivery time
- Late delivery rate
- Revenue from late orders
- Delivery distribution
- State-level delivery risk
- Delivery and review relationships where available

### Business Question

> **Where can operational performance become a commercial problem?**

For example:

```text
HIGH REVENUE
      +
HIGH LATE DELIVERY
      ↓
COMMERCIAL RISK
      ↓
INVESTIGATE LOGISTICS
```

This moves the analysis beyond operational reporting and connects logistics with business impact.

---

# 💡 5. Business Insights & Decision Center

The final module converts analytical results into **business actions**.

Instead of simply showing:

> "Category X has high revenue."

the dashboard asks:

> **"What should management do about it?"**

Examples include:

### Revenue Protection

Protect high-performing categories through inventory and pricing monitoring.

### Revenue Expansion

Identify high-volume categories with below-average AOV and test:

- Product bundles
- Cross-selling
- Premium alternatives
- Minimum-order incentives

### Operational Improvement

Identify regions with elevated late-delivery rates and investigate fulfilment or logistics performance.

### Revenue Risk Management

Monitor concentration when a large percentage of revenue depends on a small number of categories.

---

# 🧠 Analytical Framework

The project follows a business-first analytics workflow:

```text
RAW DATA
   ↓
DATA CLEANING
   ↓
DATA INTEGRATION
   ↓
KPI DEVELOPMENT
   ↓
DESCRIPTIVE ANALYSIS
   ↓
DIAGNOSTIC ANALYSIS
   ↓
OPPORTUNITY / RISK DETECTION
   ↓
BUSINESS RECOMMENDATIONS
```

The goal is not simply to create visualizations.

The goal is to move from:

**What happened?**

→ **Why does it matter?**

→ **Where is the opportunity or risk?**

→ **What should the business do?**

---

# 📌 Key Business Metrics

### Total Revenue

```text
Total Revenue = Sum of Order Revenue
```

### Average Order Value

```text
AOV = Total Revenue / Unique Orders
```

### Revenue Share

```text
Revenue Share =
Category Revenue / Total Revenue × 100
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

| Technology | Purpose |
|---|---|
| Python | Data analysis and application logic |
| Pandas | Data cleaning and transformation |
| Plotly | Interactive visual analytics |
| Streamlit | Business intelligence dashboard |
| GitHub | Version control |
| CSV | Source data |

---

# 📂 Project Structure

```text
olist-sales-insights/
│
├── app.py
├── data.py
├── requirements.txt
├── README.md
│
└── data/
    ├── olist_orders_dataset.csv
    ├── olist_order_items_dataset.csv
    ├── olist_customers_dataset.csv
    ├── olist_products_dataset.csv
    ├── product_category_name_translation.csv
    └── olist_order_reviews_dataset.csv
```

---

# 📊 Business Impact

The dashboard is designed to help a business answer four major questions:

| Business Area | Decision Supported |
|---|---|
| Revenue | Where is revenue growing or declining? |
| Categories | Which products should be protected or expanded? |
| Customers & Regions | Which markets generate the most value? |
| Operations | Where could delivery problems affect revenue? |

The result is a single analytical layer that connects:

```text
SALES
  +
REVENUE
  +
CATEGORY PERFORMANCE
  +
GEOGRAPHY
  +
DELIVERY
  ↓
BUSINESS DECISIONS
```

---

# 🎯 What This Project Demonstrates

This project demonstrates the ability to work through the complete Data Analytics lifecycle:

### Data

Clean and integrate multiple transactional datasets.

### Analytics

Build KPIs, trends, comparisons and performance metrics.

### Business Intelligence

Create an interactive dashboard for decision makers.

### Diagnosis

Identify revenue drivers, opportunities and operational risks.

### Decision Making

Translate analytical findings into practical business recommendations.

---

# 🚀 Future Enhancements

Potential extensions include:

- SQL analytical layer
- Automated KPI alerts
- Revenue forecasting
- Customer lifetime value
- Cohort analysis
- Customer segmentation
- Automated reporting
- Cloud data warehouse integration
- Scheduled data refresh

---

# 👩‍💻 Author

## Jahnavi J

**BCA | Data Analytics & Business Intelligence**

Interested in:

- Data Analytics
- Business Intelligence
- Product Analytics
- Revenue Analytics
- SQL
- Python
- Power BI

---

# ⭐ Project Philosophy

> **A good dashboard tells you what happened.**
>
> **A strong analytics solution explains why it matters.**
>
> **A business intelligence solution tells you what to do next.**

**Olist Sales Intelligence is designed around the third principle.**
