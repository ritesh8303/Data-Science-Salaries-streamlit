import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pycountry

# Set page config
st.set_page_config(page_title="Salaries 2025 Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("cleaned_salaries.csv")

# Convert country code to full name
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

df["company_location_full"] = df["company_location"].apply(get_country_name)

# Sidebar filters
with st.sidebar:
    st.header("🔎 Filters")
    job_filter = st.selectbox("Job Title", ["All"] + sorted(df["job_title"].unique().tolist()))
    location_filter = st.selectbox("Company Location", ["All"] + sorted(df["company_location_full"].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if job_filter != "All":
    filtered_df = filtered_df[filtered_df["job_title"] == job_filter]
if location_filter != "All":
    filtered_df = filtered_df[filtered_df["company_location_full"] == location_filter]

# ---- LAYOUT ----
col1, col2 = st.columns(2)

# Chart 1: Average Salary by Job Title (Top 5)
with col1:
    st.subheader("💼 Avg Salary by Job Title (Top 5)")
    top_jobs = (
        filtered_df.groupby("job_title")["salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )
    fig, ax = plt.subplots(figsize=(4, 2.5))
    sns.barplot(x=top_jobs.values, y=top_jobs.index, palette="viridis", ax=ax)
    ax.set_xlabel("Avg Salary (USD)")
    ax.set_ylabel("")
    st.pyplot(fig)

# Chart 2: Jobs per Country (Top 5)
with col2:
    st.subheader("🌍 Job Count by Country (Top 5)")
    top_locations = (
        filtered_df["company_location_full"]
        .value_counts()
        .head(5)
    )
    fig2, ax2 = plt.subplots(figsize=(4, 2.5))
    sns.barplot(x=top_locations.values, y=top_locations.index, palette="coolwarm", ax=ax2)
    ax2.set_xlabel("Number of Jobs")
    ax2.set_ylabel("")
    st.pyplot(fig2)
