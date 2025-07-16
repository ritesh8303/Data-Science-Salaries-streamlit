import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pycountry

# === Page Setup ===
st.set_page_config(page_title="2025 AI/ML Job Salaries", layout="wide")
sns.set_style("whitegrid")

# === Load Data ===
df = pd.read_csv("cleaned_salaries.csv")

# Map country codes to full names
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

df["company_country"] = df["company_location"].apply(get_country_name)
df["employee_country"] = df["employee_residence"].apply(get_country_name)

# === Sidebar Filters ===
with st.sidebar:
    st.title("🔎 Filters")
    job = st.selectbox("Job Title", ["All"] + sorted(df["job_title"].unique()))
    country = st.selectbox("Company Country", ["All"] + sorted(df["company_country"].unique()))
    experience = st.selectbox("Experience Level", ["All"] + sorted(df["experience_level"].unique()))
    remote = st.slider("Remote Work %", 0, 100, (0, 100), step=25)

# === Apply Filters ===
filtered = df.copy()
if job != "All":
    filtered = filtered[filtered["job_title"] == job]
if country != "All":
    filtered = filtered[filtered["company_country"] == country]
if experience != "All":
    filtered = filtered[filtered["experience_level"] == experience]
filtered = filtered[(filtered["remote_ratio"] >= remote[0]) & (filtered["remote_ratio"] <= remote[1])]

# === Layout ===
st.title("📊 AI & ML Job Salaries – 2025 Overview")
col1, col2, col3 = st.columns(3)

# KPI 1: Average Salary
with col1:
    avg_salary = filtered["salary_in_usd"].mean()
    st.metric("💰 Avg Salary (USD)", f"${avg_salary:,.0f}")

# KPI 2: Most Common Job Title
with col2:
    common_job = filtered["job_title"].mode()[0] if not filtered.empty else "N/A"
    st.metric("👩‍💻 Top Job Title", common_job)

# KPI 3: Most Hiring Country
with col3:
    top_country = filtered["company_country"].value_counts().idxmax() if not filtered.empty else "N/A"
    st.metric("🌍 Top Hiring Country", top_country)

st.markdown("---")

# === Two Charts Side by Side ===
chart1, chart2 = st.columns(2)

# Chart 1: Avg Salary by Job Title
with chart1:
    st.subheader("💼 Avg Salary by Job Title (Top 6)")
    top_jobs = (
        filtered.groupby("job_title")["salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
        .head(6)
    )
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(x=top_jobs.values, y=top_jobs.index, palette="Spectral", ax=ax)
    ax.set_xlabel("USD Salary")
    ax.set_ylabel("")
    st.pyplot(fig)

# Chart 2: Job Count by Country
with chart2:
    st.subheader("📍 Job Count by Country (Top 6)")
    top_countries = filtered["company_country"].value_counts().head(6)
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="coolwarm", ax=ax2)
    ax2.set_xlabel("No. of Jobs")
    ax2.set_ylabel("")
    st.pyplot(fig2)

st.markdown("---")

# === Final Row: Experience & Remote Correlation ===
col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Salary vs Experience Level")
    fig3, ax3 = plt.subplots(figsize=(4.5, 3))
    sns.boxplot(x="experience_level", y="salary_in_usd", data=filtered, palette="Set2", ax=ax3)
    ax3.set_xlabel("Experience Level")
    ax3.set_ylabel("Salary (USD)")
    st.pyplot(fig3)

with col5:
    st.subheader("🏡 Salary vs Remote Ratio")
    fig4, ax4 = plt.subplots(figsize=(4.5, 3))
    sns.scatterplot(x="remote_ratio", y="salary_in_usd", data=filtered, hue="company_country", ax=ax4, s=40)
    ax4.set_xlabel("Remote Work (%)")
    ax4.set_ylabel("Salary (USD)")
    st.pyplot(fig4)
