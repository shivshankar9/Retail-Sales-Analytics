# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Config
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("🛒 Retail Sales Analytics Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_sales_data.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)  # FIXED
    df["Year"] = df["Order Date"].dt.year
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect("Select Region:", df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category:", df["Product Category"].unique(), default=df["Product Category"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [df["Order Date"].min(), df["Order Date"].max()])

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Product Category"].isin(category)) &
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1]))
]

# KPIs
total_sales = filtered_df["Sales"].sum()
avg_order = filtered_df["Sales"].mean()
top_customer = filtered_df.groupby("Customer Name")["Sales"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📦 Avg Order Value", f"${avg_order:,.2f}")
col3.metric("🏅 Top Customer", top_customer)

# Charts Section
st.markdown("## 📊 Sales Trends")

# Monthly Sales Trend
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()
monthly_sales = monthly_sales.sort_values("Month")

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_sales, x="Month", y="Sales", marker="o", ax=ax1, color="green")
ax1.set_title("Monthly Sales Trend")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Sales by Region
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(data=region_sales, x="Region", y="Sales", ax=ax2, palette="Blues_d")
ax2.set_title("Sales by Region")
st.pyplot(fig2)

# Profit vs Sales
fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=filtered_df, x="Sales", y="Profit", hue="Region", ax=ax3)
ax3.set_title("Profit vs Sales")
st.pyplot(fig3)

# Top Customers
st.markdown("## 🏆 Top 5 Customers")
top_customers = filtered_df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5)

st.bar_chart(top_customers)
