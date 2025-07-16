import streamlit as st
import pandas as pd
import plotly.express as px

# === Page Setup ===
st.set_page_config(page_title="2025 AI/ML Salary Dashboard", layout="wide")

# === Load Data ===
df = pd.read_csv("cleaned_salaries.csv")

# === Location Mapping ===
import pycountry
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code
df["Location"] = df["company_location"].apply(get_country_name)

# === Sidebar Filters ===
with st.sidebar:
    st.title("🔍 Filters")
    job_titles = ["All"] + sorted(df["job_title"].unique())
    locations = ["All"] + sorted(df["Location"].unique())

    selected_job = st.selectbox("🎯 Job Title", job_titles)
    selected_location = st.selectbox("🌍 Location", locations)

# === Filter Logic ===
filtered_df = df.copy()
if selected_job != "All":
    filtered_df = filtered_df[filtered_df["job_title"] == selected_job]
if selected_location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == selected_location]

# === Metrics ===
avg_salary = filtered_df["salary_in_usd"].mean()
max_salary = filtered_df["salary_in_usd"].max()
min_salary = filtered_df["salary_in_usd"].min()

st.title("💼 2025 AI/ML Job Salaries Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("📊 Average Salary", f"${avg_salary:,.0f}")
col2.metric("🔥 Max Salary", f"${max_salary:,.0f}")
col3.metric("💤 Min Salary", f"${min_salary:,.0f}")

st.markdown("---")

# === Row 1: Bar Chart + Stacked Column ===
c1, c2 = st.columns(2)

# Bar Chart: Average Salary by Job Title
with c1:
    st.subheader("💼 Average Salary by Job Title")
    bar_data = (
        filtered_df.groupby("job_title")["salary_in_usd"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )
    fig1 = px.bar(
        bar_data,
        x="salary_in_usd",
        y="job_title",
        orientation="h",
        color="salary_in_usd",
        color_continuous_scale="Viridis",
        labels={"salary_in_usd": "Avg Salary (USD)", "job_title": "Job Title"},
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)

# Stacked Column Chart: Salary by Job Title and Experience
with c2:
    st.subheader("📚 Salary by Experience Level & Job Title")
    grouped = filtered_df.groupby(["job_title", "experience_level"])["salary_in_usd"].mean().reset_index()
    fig2 = px.bar(
        grouped,
        x="job_title",
        y="salary_in_usd",
        color="experience_level",
        barmode="stack",
        labels={"salary_in_usd": "Avg Salary", "job_title": "Job Title", "experience_level": "Experience"},
        height=400,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig2, use_container_width=True)

# === Row 2: Map ===
st.subheader("🗺️ Average Salary by Country")
map_data = filtered_df.groupby("Location")["salary_in_usd"].mean().reset_index()
fig3 = px.choropleth(
    map_data,
    locations="Location",
    locationmode="country names",
    color="salary_in_usd",
    color_continuous_scale="Plasma",
    title="Average Salary by Country",
    labels={"salary_in_usd": "Avg Salary"},
    height=500
)
st.plotly_chart(fig3, use_container_width=True)
