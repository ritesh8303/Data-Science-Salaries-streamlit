# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Salaries 2025 Dashboard", layout="wide")

st.title("📊 Data Science, AI & ML Job Salaries - 2025")

# Upload CSV
uploaded_file = st.file_uploader("Upload your cleaned salaries CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File successfully uploaded!")

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")
        job_filter = st.multiselect("Select Job Title(s):", df["job_title"].unique())
        location_filter = st.multiselect("Select Company Location(s):", df["company_location"].unique())

    # Apply filters
    if job_filter:
        df = df[df["job_title"].isin(job_filter)]
    if location_filter:
        df = df[df["company_location"].isin(location_filter)]

    # Show dataset
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head(10))

    # Summary Stats
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # Visualization 1 - Avg Salary by Job Title
    st.subheader("💼 Average Salary by Job Title")
    avg_salary_job = df.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=avg_salary_job.values, y=avg_salary_job.index, ax=ax1)
    ax1.set_xlabel("Average Salary (USD)")
    ax1.set_ylabel("Job Title")
    st.pyplot(fig1)

    # Visualization 2 - Count by Location
    st.subheader("🌍 Number of Jobs per Company Location")
    loc_counts = df["company_location"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=loc_counts.values, y=loc_counts.index, ax=ax2)
    ax2.set_xlabel("Number of Jobs")
    ax2.set_ylabel("Company Location")
    st.pyplot(fig2)

    # Visualization 3 - Salary Distribution
    st.subheader("📊 Salary Distribution")
    fig3, ax3 = plt.subplots()
    sns.histplot(df["salary_in_usd"], kde=True, ax=ax3)
    ax3.set_xlabel("Salary in USD")
    st.pyplot(fig3)
else:
    st.warning("Please upload the cleaned_salaries.csv file.")
