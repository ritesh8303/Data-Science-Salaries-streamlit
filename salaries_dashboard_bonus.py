import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pycountry

st.set_page_config(page_title="Salaries 2025 Dashboard", layout="wide")
st.title("📊 Data Science, AI & ML Job Salaries - 2025")

# Load data
df = pd.read_csv("cleaned_salaries.csv")

# Convert country codes to full names
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

df["company_location_full"] = df["company_location"].apply(get_country_name)

# Sidebar filters with search-enabled dropdown (multiselect)
with st.sidebar:
    st.header("🔍 Filters")
    job_filter = st.multiselect("Select Job Title(s):", df["job_title"].unique(), max_selections=5)
    location_filter = st.multiselect("Select Company Location(s):", df["company_location_full"].unique(), max_selections=5)

# Filter data
filtered_df = df.copy()
if job_filter:
    filtered_df = filtered_df[filtered_df["job_title"].isin(job_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["company_location_full"].isin(location_filter)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("💼 Avg Salary by Job Title (Top 10)")
    avg_salary = filtered_df.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    sns.barplot(x=avg_salary.values, y=avg_salary.index, palette="viridis", ax=ax1)
    ax1.set_xlabel("Average Salary (USD)")
    ax1.set_ylabel("Job Title")
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.subheader("🌍 Jobs per Country (Top 10)")
    location_counts = filtered_df["company_location_full"].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    sns.barplot(x=location_counts.values, y=location_counts.index, palette="coolwarm", ax=ax2)
    ax2.set_xlabel("Number of Jobs")
    ax2.set_ylabel("Country")
    plt.tight_layout()
    st.pyplot(fig2)

with col1:
    st.subheader("📊 Salary Distribution")
    fig3, ax3 = plt.subplots(figsize=(5, 3))
    sns.histplot(filtered_df["salary_in_usd"], kde=True, ax=ax3, color="skyblue", bins=20)
    ax3.set_xlabel("Salary in USD")
    plt.tight_layout()
    st.pyplot(fig3)
