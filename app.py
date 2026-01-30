import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Healthcare Readmission", layout="wide")

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.markdown("Predicting 30-day hospital readmission risk using AI")

# Load data
df = pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")
st.write("Columns:", df.columns.tolist())

# Sidebar filter
st.sidebar.header("Filter")
options = df["readmit_status"].unique()
risk = st.sidebar.selectbox(
    "Select Readmission Status",
    options
)

filtered_df = df[df["readmit_status"] == risk]
# KPI
st.metric("Total Patients", len(filtered_df))

# Chart
fig = px.histogram(
    filtered_df,
    x="readmit_probability",
    nbins=20,
    title="Readmission Probability Distribution"
)
st.plotly_chart(fig, use_container_width=True)

st.success("Live AI Risk Dashboard Running Successfully 🚀")


