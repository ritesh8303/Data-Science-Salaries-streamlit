import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO

# Set page config
st.set_page_config(page_title="AI/ML Job Salaries 2025", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_salaries.csv")
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

job_filter = st.sidebar.multiselect("Job Titles", df["job_title"].unique())
location_filter = st.sidebar.multiselect("Company Locations", df["company_location"].unique())
experience_filter = st.sidebar.multiselect("Experience Levels", df["experience_level"].unique())

salary_min, salary_max = int(df.salary_in_usd.min()), int(df.salary_in_usd.max())
salary_range = st.sidebar.slider("Salary Range (USD)", salary_min, salary_max, (salary_min, salary_max))

filtered_df = df[
    (df.salary_in_usd >= salary_range[0]) & (df.salary_in_usd <= salary_range[1])
]

if job_filter:
    filtered_df = filtered_df[filtered_df["job_title"].isin(job_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["company_location"].isin(location_filter)]
if experience_filter:
    filtered_df = filtered_df[filtered_df["experience_level"].isin(experience_filter)]

# Title
st.title("💼 Data Science, AI & ML Salaries - 2025 Interactive Dashboard")

# Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Avg Salary (USD)", f"${filtered_df['salary_in_usd'].mean():,.0f}")
col3.metric("Unique Job Titles", filtered_df['job_title'].nunique())

# Download buttons
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Data')
    writer.close()
    return output.getvalue()

st.download_button("📥 Download CSV", data=filtered_df.to_csv(index=False), file_name="filtered_data.csv", mime="text/csv")
st.download_button("📊 Download Excel", data=to_excel(filtered_df), file_name="filtered_data.xlsx", mime="application/vnd.ms-excel")

# Bar Chart - Average Salary by Job Title (Plotly)
st.subheader("💸 Average Salary by Job Title")
salary_by_title = filtered_df.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=False).reset_index()
fig1 = px.bar(salary_by_title, x="salary_in_usd", y="job_title", orientation='h', color="salary_in_usd",
              color_continuous_scale="Viridis", labels={"salary_in_usd": "Average Salary (USD)", "job_title": "Job Title"})
st.plotly_chart(fig1, use_container_width=True)

# Box Plot - Salary Distribution for Top 5 Companies (Plotly)
st.subheader("📦 Salary Distribution - Top 5 Company Locations")
top_companies = filtered_df.groupby("company_location")["salary_in_usd"].mean().nlargest(5).index
top_df = filtered_df[filtered_df["company_location"].isin(top_companies)]
fig2 = px.box(top_df, x="company_location", y="salary_in_usd", color="company_location",
              labels={"salary_in_usd": "Salary (USD)", "company_location": "Location"})
st.plotly_chart(fig2, use_container_width=True)

# Count Plot - Number of Jobs per Location
st.subheader("📍 Number of Jobs per Location")
location_count = filtered_df["company_location"].value_counts().reset_index()
fig3 = px.bar(location_count, x="index", y="company_location",
              labels={"index": "Location", "company_location": "Number of Jobs"},
              color="company_location", color_continuous_scale="Blues")
st.plotly_chart(fig3, use_container_width=True)

# Line Chart - Salary Trends by Work Year (if >1 year)
if df["work_year"].nunique() > 1:
    st.subheader("📈 Salary Trend by Year")
    trend = filtered_df.groupby("work_year")["salary_in_usd"].mean().reset_index()
    fig4 = px.line(trend, x="work_year", y="salary_in_usd", markers=True,
                   labels={"salary_in_usd": "Avg Salary (USD)", "work_year": "Year"})
    st.plotly_chart(fig4, use_container_width=True)

# Pie Chart - Company Size Distribution
st.subheader("🏢 Company Size Distribution")
if "company_size" in filtered_df.columns:
    size_counts = filtered_df["company_size"].value_counts().reset_index()
    fig5 = px.pie(size_counts, names="index", values="company_size", title="Distribution by Company Size",
                  labels={"index": "Company Size", "company_size": "Count"})
    st.plotly_chart(fig5)

# Correlation Heatmap - Seaborn
st.subheader("🧠 Feature Correlation")
num_cols = filtered_df.select_dtypes(include=["int64", "float64"])
if len(num_cols.columns) > 1:
    fig6, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(num_cols.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig6)

# Show Data
with st.expander("🗃 Show Filtered Data"):
    st.dataframe(filtered_df)

# Export to PDF (Text-based workaround using dataframe.to_string)
with st.expander("📄 Export Summary Report (PDF Workaround)"):
    st.code(filtered_df.head(20).to_string(index=False))
    st.caption("📌 Copy the above output and paste it into a PDF manually using any editor.")
