import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Readmission", layout="wide")

st.title("🏥 AI-Powered Patient Readmission Dashboard")

# Load data
df = pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")

# Sidebar
risk = st.sidebar.selectbox(
    "Select Risk Bucket",
    df["risk_bucket"].unique(),
    key="risk_select_unique"
)

filtered_df = df[df["risk_bucket"] == risk]

# KPI
st.metric("Total Patients", int(filtered_df["count(*)"].sum()))

# Chart (ONLY ONE chart)
fig = px.bar(
    filtered_df,
    x="risk_bucket",
    y="count(*)",
    title="Patient Distribution by Risk Bucket"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="ONLY_ONE_CHART_KEY"
)

st.success("✅ App running without duplicate ID errors")
