import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 E-commerce EDA Dashboard")

@st.cache_data
def load_data():
    df = pd.read_excel("ecommerce_dataset...xlsx", sheet_name="ecommerce_dataset")
    df["revenue"] = df["quantity"] * df["price"] * (1 - df["discount"])
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M")
    return df

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Sales by Month
# Create month column as datetime (1st of each month)
# Ensure order_date is datetime
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Create month column as datetime (first day of each month)
df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

# Create a continuous 12-month range
all_months = pd.date_range(
    start=df["month"].min(), 
    end=df["month"].max(), 
    freq="MS"  # Month start
)

# Group by month and sum revenue
sales_over_time = df.groupby("month")["revenue"].sum().reindex(all_months, fill_value=0).reset_index()

# Rename for plotting
sales_over_time.columns = ["month", "revenue"]

# Plot in correct time order with 12 dots
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(x="month", y="revenue", data=sales_over_time, ax=ax, marker="o")
ax.set_title("Monthly Revenue Trend")
plt.xticks(rotation=45)
st.pyplot(fig)


# Category revenue
st.subheader("Revenue by Category")
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="category", y="revenue", data=df, estimator=sum, ax=ax)
st.pyplot(fig)

# Region revenue
st.subheader("Revenue by Region")
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="region", y="revenue", data=df, estimator=sum, ax=ax)
st.pyplot(fig)

# Payment method
st.subheader("Payment Method Distribution")
fig, ax = plt.subplots()
df["payment_method"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
st.pyplot(fig)
