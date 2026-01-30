import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Readmission", layout="wide")

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Predicting 30-day hospital readmission risk using AI")

# Load data
df = pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")

# Sidebar filter
risk = st.sidebar.selectbox(
    "Select Risk Bucket",
    sorted(df["risk_bucket"].unique())
)

filtered_df = df[df["risk_bucket"] == risk]

# KPI
st.metric(
    "Total Patients",
    int(filtered_df["count(*)"].sum())
)

# 🔑 CRITICAL FIX: use container
chart_container = st.empty()

fig = px.bar(
    filtered_df,
    x="risk_bucket",
    y="count(*)",
    title="Patient Distribution by Risk Bucket"
)

chart_container.plotly_chart(
    fig,
    use_container_width=True
)

st.success("✅ Dashboard loaded successfully (no duplicate ID)")
