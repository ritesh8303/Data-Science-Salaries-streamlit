# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pycountry

# Page config
st.set_page_config(page_title="Salaries 2025 Dashboard", layout="wide")
st.title("📊 Data Science, AI & ML Job Salaries - 2025")

# Read the cleaned data
df = pd.read_csv("cleaned_salaries.csv")

# Convert country codes to full names
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code  # fallback if not found

df["company_location_full"] = df["company_location"].apply(get_country_name)

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filters")
    job_filter = st.multiselect("Select Job Title(s):", df["job_title"].unique())
    location_filter = st.multiselect("Select Company Location(s):", df["company_location_full"].unique())

# Apply filters
filtered_df = df.copy()
if job_filter:
    filtered_df = filtered_df[filtered_df["job_title"].isin(job_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["company_location_full"].isin(location_filter)]

# Show dataset preview
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head())

# Summary Stats
st.subheader("📈 Summary Statistics")
st.write(filtered_df.describe())

# Plot 1: Average Salary by Job Title
st.subheader("💼 Average Salary by Job Title")
avg_salary = filtered_df.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=True)
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=avg_salary.values, y=avg_salary.index, palette="viridis", ax=ax1)
ax1.set_xlabel("Average Salary (USD)")
ax1.set_ylabel("Job Title")
st.pyplot(fig1)

# Plot 2: Job Counts by Country
st.subheader("🌍 Number of Jobs per Country")
location_counts = filtered_df["company_location_full"].value_counts()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=location_counts.values, y=location_counts.index, palette="coolwarm", ax=ax2)
ax2.set_xlabel("Number of Jobs")
ax2.set_ylabel("Country")
st.pyplot(fig2)

# Plot 3: Salary Distribution
st.subheader("📊 Salary Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(filtered_df["salary_in_usd"], kde=True, ax=ax3, color="skyblue")
ax3.set_xlabel("Salary in USD")
st.pyplot(fig3)
