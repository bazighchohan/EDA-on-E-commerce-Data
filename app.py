import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 E-commerce Exploratory Data Analysis (EDA) Dashboard")

@st.cache_data
def load_data():
    df = pd.read_excel("ecommerce_dataset...xlsx", sheet_name="ecommerce_dataset")
    df["revenue"] = df["quantity"] * df["price"] * (1 - df["discount"])
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df

df = load_data()

# =========================
# 1. DATA OVERVIEW
# =========================
st.header("📌 Data Overview")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Dataset Shape")
st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

st.subheader("Data Types")
st.write(df.dtypes)

st.subheader("Missing Values")
st.write(df.isnull().sum())

st.subheader("Summary Statistics")
st.write(df.describe())

# =========================
# 2. UNIVARIATE ANALYSIS
# =========================
st.header("📌 Univariate Analysis")

st.subheader("Numerical Feature Distributions")
num_cols = ["quantity", "price", "discount", "revenue"]
for col in num_cols:
    fig, ax = plt.subplots()
    sns.histplot(df[col], kde=True, ax=ax)
    ax.set_title(f"Distribution of {col}")
    st.pyplot(fig)

st.subheader("Categorical Feature Counts")
cat_cols = ["region", "category", "payment_method"]
for col in cat_cols:
    fig, ax = plt.subplots()
    sns.countplot(x=col, data=df, ax=ax)
    ax.set_title(f"Count of {col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =========================
# 3. BIVARIATE ANALYSIS
# =========================
st.header("📌 Bivariate Analysis")

st.subheader("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.subheader("Revenue by Category")
fig, ax = plt.subplots()
sns.barplot(x="category", y="revenue", data=df, estimator=sum, ax=ax)
st.pyplot(fig)

st.subheader("Revenue by Region")
fig, ax = plt.subplots()
sns.barplot(x="region", y="revenue", data=df, estimator=sum, ax=ax)
st.pyplot(fig)

st.subheader("Payment Method Distribution")
fig, ax = plt.subplots()
df["payment_method"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# =========================
# 4. MULTIVARIATE / BUSINESS INSIGHTS
# =========================
st.header("📌 Multivariate Analysis & Business Insights")

st.subheader("Revenue by Category across Regions")
category_region = df.groupby(["region", "category"])["revenue"].sum().reset_index()
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x="region", y="revenue", hue="category", data=category_region, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Monthly Revenue Trend")
monthly_revenue = df.groupby("month")["revenue"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(x="month", y="revenue", data=monthly_revenue, marker="o", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("🏆 Top 10 Products by Revenue")
top_products = df.groupby("product_id")["revenue"].sum().nlargest(10).reset_index()

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x="product_id", y="revenue", data=top_products, ax=ax, palette="viridis")

ax.set_title("Top 10 Products by Revenue")
ax.set_xlabel("Product ID")
ax.set_ylabel("Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)


st.subheader("Discount vs Revenue Impact")
fig, ax = plt.subplots()
sns.scatterplot(x="discount", y="revenue", data=df, alpha=0.6, ax=ax)
st.pyplot(fig)

st.subheader("Customer Contribution (Pareto 80/20 Rule)")
customer_revenue = df.groupby("customer_id")["revenue"].sum().sort_values(ascending=False).reset_index()
customer_revenue["cum_perc"] = 100 * customer_revenue["revenue"].cumsum() / customer_revenue["revenue"].sum()
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(x=range(len(customer_revenue)), y="cum_perc", data=customer_revenue, ax=ax)
ax.axhline(80, color="red", linestyle="--")
ax.set_xlabel("Customers (sorted by revenue)")
ax.set_ylabel("Cumulative % of Revenue")
st.pyplot(fig)
