import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Afficionado Coffee Roasters Dashboard",
    layout="wide"
)

# ---------------- TITLE ---------------- #

st.title("☕ Afficionado Coffee Roasters Dashboard")
st.markdown("### Coffee Demand & Sales Analysis")

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("Afficionado Coffee Roasters.xlsx - Transactions.csv")

# ---------------- DATA PREPROCESSING ---------------- #

# Convert transaction time
df['transaction_time'] = pd.to_datetime(
    df['transaction_time'],
    format='%H:%M:%S'
)

# Create Hour column
df['Hour'] = df['transaction_time'].dt.hour

# Create Revenue column
df['Revenue'] = df['transaction_qty'] * df['unit_price']

# ---------------- SIDEBAR FILTER ---------------- #

st.sidebar.header("Filter Data")

selected_store = st.sidebar.multiselect(
    "Select Store Location",
    options=df['store_location'].unique(),
    default=df['store_location'].unique()
)

filtered_df = df[df['store_location'].isin(selected_store)]

# ---------------- KPI SECTION ---------------- #

total_revenue = filtered_df['Revenue'].sum()
total_transactions = filtered_df['transaction_id'].count()
top_store = filtered_df.groupby('store_location')['Revenue'].sum().idxmax()
top_category = filtered_df.groupby('product_category')['Revenue'].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🧾 Total Transactions", total_transactions)
col3.metric("🏪 Top Store", top_store)
col4.metric("☕ Top Category", top_category)

st.markdown("---")

# ---------------- PEAK HOUR ANALYSIS ---------------- #

st.subheader("⏰ Revenue by Hour")

hourly_revenue = filtered_df.groupby('Hour')['Revenue'].sum()

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(hourly_revenue.index, hourly_revenue.values, marker='o')
ax1.set_xlabel("Hour")
ax1.set_ylabel("Revenue")
ax1.set_title("Peak Hour Revenue")

st.pyplot(fig1)

# ---------------- STORE PERFORMANCE ---------------- #

st.subheader("🏪 Store Revenue Comparison")

store_sales = filtered_df.groupby('store_location')['Revenue'].sum()

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(store_sales.index, store_sales.values)
ax2.set_xlabel("Store Location")
ax2.set_ylabel("Revenue")
ax2.set_title("Revenue by Store")

st.pyplot(fig2)

# ---------------- PRODUCT CATEGORY ANALYSIS ---------------- #

st.subheader("☕ Product Category Revenue")

category_sales = filtered_df.groupby('product_category')['Revenue'].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(category_sales.index, category_sales.values)
ax3.set_xlabel("Product Category")
ax3.set_ylabel("Revenue")
ax3.set_title("Revenue by Product Category")
plt.xticks(rotation=45)

st.pyplot(fig3)

# ---------------- PRODUCT TYPE ANALYSIS ---------------- #

st.subheader("🔥 Top Product Types")

product_type_sales = filtered_df.groupby('product_type')['Revenue'].sum().sort_values(ascending=False).head(10)

fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.barh(product_type_sales.index, product_type_sales.values)
ax4.set_xlabel("Revenue")
ax4.set_ylabel("Product Type")
ax4.set_title("Top 10 Product Types")

st.pyplot(fig4)

# ---------------- DATA PREVIEW ---------------- #

st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head(20))


