import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="BSS Retail Dashboard", layout="wide")

# ✅ Load and clean the malformed CSV (this is the key fix!)
with open("BSS Retail Data.csv", "r") as f:
    lines = f.readlines()

# Split the first row into column names
columns = lines[0].strip().split(",")

# Read the rest of the rows and split them properly
data = [line.strip().split(",") for line in lines[1:]]
df = pd.DataFrame(data, columns=columns)

# ✅ Convert numeric columns
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

# ✅ Strip extra spaces from column names
df.columns = df.columns.str.strip()

# ✅ Drop columns with too many missing values (except important ones)
important_cols = ['sku', 'salesdate']
threshold = len(df) * 0.4
cols_to_keep = [col for col in df.columns if df[col].notna().sum() > threshold or col in important_cols]
df_clean = df[cols_to_keep].copy()
df_clean.fillna(df_clean.mean(numeric_only=True), inplace=True)

# ✅ Sidebar filter
st.sidebar.title("Filter Options")
if 'sku' in df_clean.columns:
    sku_filter = st.sidebar.selectbox("Select SKU:", df_clean['sku'].unique())
    filtered_df = df_clean[df_clean['sku'] == sku_filter]
else:
    st.warning("'sku' column is not available.")
    filtered_df = df_clean.copy()

# ✅ Check required columns
if 'sales' in filtered_df.columns and 'adspend' in filtered_df.columns:
    st.title("📊 BSS Retail Interactive Dashboard")

    # 1. Sales Distribution
    st.subheader("📈 Sales Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered_df['sales'], bins=30, kde=True, ax=ax1)
    st.pyplot(fig1)

    # 2. Ad Spend vs Sales
    st.subheader("💸 Ad Spend vs Sales")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='adspend', y='sales', data=filtered_df, ax=ax2)
    st.pyplot(fig2)

    # 3. Correlation Heatmap
    st.subheader("🔍 Correlation Heatmap")
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax3)
    st.pyplot(fig3)

else:
    st.error("Required columns like 'sales' or 'adspend' are missing.")
