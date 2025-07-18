import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("cleaned_salaries_full_forms.csv")

# Streamlit page config
st.set_page_config(layout="wide", page_title="DS/ML/AI Salaries 2025 Dashboard")

# Title
st.markdown("## 📊 Data Science, AI & ML Job Salaries - 2025 Dashboard")

# ---- SIDEBAR FILTERS ----
with st.sidebar:
    st.header("🔎 Filter Options")
    
    # Job Titles (only first 8 selected by default)
    job_titles = sorted(df["job_title"].unique().tolist())
    default_jobs = job_titles[:8]
    selected_jobs = st.multiselect("Job Title", options=job_titles, default=default_jobs)

    # Locations
    locations = sorted(df["employee_residence"].unique().tolist())
    selected_locations = st.multiselect("Location", options=locations, default=locations)

    # Companies
    companies = sorted(df["company_name"].dropna().unique().tolist())
    selected_companies = st.multiselect("Company", options=companies, default=companies)

    # Work Year
    years = sorted(df["work_year"].unique().tolist())
    selected_years = st.multiselect("Year", options=years, default=years)

# ---- DATA FILTERING ----
filtered_df = df[
    (df["job_title"].isin(selected_jobs)) &
    (df["employee_residence"].isin(selected_locations)) &
    (df["company_name"].isin(selected_companies)) &
    (df["work_year"].isin(selected_years))
]

# ---- METRICS CARDS ----
avg_salary = int(filtered_df["salary_in_usd"].mean())
max_salary = int(filtered_df["salary_in_usd"].max())
min_salary = int(filtered_df["salary_in_usd"].min())
total_jobs = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Avg Salary (USD)", f"${avg_salary:,.0f}")
col2.metric("📈 Max Salary (USD)", f"${max_salary:,.0f}")
col3.metric("📉 Min Salary (USD)", f"${min_salary:,.0f}")
col4.metric("🧑‍💼 Total Jobs", total_jobs)

# ---- VISUALS ----

# 1. Bar Chart: Average Salary by Job Title
fig1 = px.bar(
    filtered_df.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=False).reset_index(),
    x="salary_in_usd",
    y="job_title",
    orientation='h',
    color="salary_in_usd",
    color_continuous_scale="viridis",
    title="Average Salary by Job Title"
)

# 2. Map: Average Salary by Location
fig2 = px.scatter_geo(
    filtered_df.groupby("employee_residence")["salary_in_usd"].mean().reset_index(),
    locations="employee_residence",
    locationmode="country names",
    size="salary_in_usd",
    color="salary_in_usd",
    title="Salaries by Location (Map)",
    color_continuous_scale="plasma"
)

# 3. Stacked Column Chart: Salaries by Company and Job Title
fig3 = px.bar(
    filtered_df,
    x="company_name",
    y="salary_in_usd",
    color="job_title",
    title="Salaries by Company and Job Title"
)

# 4. Line Chart: Salary Trend Over Years
fig4 = px.line(
    filtered_df.groupby("work_year")["salary_in_usd"].mean().reset_index(),
    x="work_year",
    y="salary_in_usd",
    markers=True,
    title="Salary Trends Over Years"
)

# ---- LAYOUT (All on screen without scroll) ----
left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

with right_col:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
