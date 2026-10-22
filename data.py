import os

import pandas as pd
import streamlit as st

DATA_DIR = "data"


@st.cache_data
def load_data():
    orders = pd.read_csv(
        f"{DATA_DIR}/olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )
    items = pd.read_csv(f"{DATA_DIR}/olist_order_items_dataset.csv")
    customers = pd.read_csv(f"{DATA_DIR}/olist_customers_dataset.csv")
    products = pd.read_csv(f"{DATA_DIR}/olist_products_dataset.csv")
    cats = pd.read_csv(f"{DATA_DIR}/product_category_name_translation.csv")

    # Keep only completed orders with a delivery date
    orders = orders[orders["order_status"] == "delivered"]
    orders = orders.dropna(subset=["order_delivered_customer_date"])

    df = (
        orders.merge(items, on="order_id")
        .merge(customers, on="customer_id")
        .merge(products, on="product_id", how="left")
        .merge(cats, on="product_category_name", how="left")
    )

    # Optional: customer review scores (one averaged score per order)
    reviews_path = f"{DATA_DIR}/olist_order_reviews_dataset.csv"
    has_reviews = os.path.exists(reviews_path)
    if has_reviews:
        reviews = pd.read_csv(reviews_path, usecols=["order_id", "review_score"])
        reviews = reviews.groupby("order_id", as_index=False)["review_score"].mean()
        df = df.merge(reviews, on="order_id", how="left")

    df["category"] = df["product_category_name_english"].fillna("unknown")
    df["revenue"] = df["price"]  # item price only, freight is kept separately
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    df["is_late"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    ).astype(int)

    # 2016 and late 2018 are incomplete months, so exclude them
    df = df[(df["month"] >= "2017-01-01") & (df["month"] <= "2018-08-01")]

    columns = [
        "order_id", "month", "customer_state", "category",
        "revenue", "freight_value", "delivery_days", "is_late",
    ]
    if has_reviews:
        columns.append("review_score")

    return df[columns].copy()
