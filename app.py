import streamlit as st
from data import load_data

st.set_page_config(page_title="Olist Sales Insights", layout="wide")
st.title("Olist Sales Insights")

df = load_data()
st.write(f"{len(df):,} rows, {df['order_id'].nunique():,} orders")
st.dataframe(df.head(10))
