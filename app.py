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
