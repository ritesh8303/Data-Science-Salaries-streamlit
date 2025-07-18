import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("cleaned_salaries_full_forms.csv")

# Convert codes to full country names for readability
from iso3166 import countries
def get_country_name(code):
    try:
        return countries.get(code).name
    except:
        return code

df['company_location_full'] = df['company_location'].apply(get_country_name)

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_year = st.sidebar.multiselect("Select Year", sorted(df['work_year'].unique()), default=df['work_year'].unique())
selected_job = st.sidebar.multiselect("Select Job Title", sorted(df['job_title'].unique()), default=df['job_title'].unique())
selected_location = st.sidebar.multiselect("Select Location", sorted(df['company_location_full'].unique()), default=df['company_location_full'].unique())
selected_company = st.sidebar.multiselect("Select Company", sorted(df['company_name'].dropna().unique()), default=df['company_name'].dropna().unique())

# Filtered data
filtered_df = df[
    (df['work_year'].isin(selected_year)) &
    (df['job_title'].isin(selected_job)) &
    (df['company_location_full'].isin(selected_location)) &
    (df['company_name'].isin(selected_company))
]

# Main layout
st.set_page_config(layout="wide")
st.title("📊 Data Science, AI & ML Job Salaries - 2025 Dashboard")

# Cards - KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Average Salary (USD)", f"${filtered_df['salary_in_usd'].mean():,.0f}")
col2.metric("🏆 Max Salary (USD)", f"${filtered_df['salary_in_usd'].max():,.0f}")
col3.metric("📉 Min Salary (USD)", f"${filtered_df['salary_in_usd'].min():,.0f}")
col4.metric("👥 Total Jobs", f"{filtered_df.shape[0]}")

# Charts layout
chart1, chart2 = st.columns(2)

# Bar Chart: Average Salary by Job Title
avg_salary_job = filtered_df.groupby('job_title')['salary_in_usd'].mean().sort_values().reset_index()
fig_bar = px.bar(avg_salary_job, x='salary_in_usd', y='job_title', orientation='h',
                 color='salary_in_usd', color_continuous_scale='viridis',
                 title="💼 Average Salary by Job Title")
chart1.plotly_chart(fig_bar, use_container_width=True)

# Map: Salaries by Location
location_salary = filtered_df.groupby('company_location_full')['salary_in_usd'].mean().reset_index()
fig_map = px.choropleth(location_salary,
                        locations='company_location_full',
                        locationmode='country names',
                        color='salary_in_usd',
                        color_continuous_scale='plasma',
                        title="🌍 Average Salaries by Country")
chart2.plotly_chart(fig_map, use_container_width=True)

# Stacked Column: Salary by Company and Job Title
pivot = filtered_df.groupby(['company_name', 'job_title'])['salary_in_usd'].mean().reset_index()
fig_stack = px.bar(pivot, x='company_name', y='salary_in_usd',
                   color='job_title', title='🏢 Salary by Company & Job Title')
st.plotly_chart(fig_stack, use_container_width=True)

# Line Chart: Salary Trends Over Years
trend = filtered_df.groupby('work_year')['salary_in_usd'].mean().reset_index()
fig_line = px.line(trend, x='work_year', y='salary_in_usd', markers=True,
                   title='📈 Salary Trend Over Years')
st.plotly_chart(fig_line, use_container_width=True)
