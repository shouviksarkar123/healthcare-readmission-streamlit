import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Readmission", layout="wide")

st.title("AI-Powered Patient Readmission Dashboard")

df = pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")

risk = st.sidebar.selectbox(
    "Select Risk Bucket",
    df["risk_bucket"].unique()
)

filtered_df = df[df["risk_bucket"] == risk]

st.metric("Total Patients", int(filtered_df["count(*)"].sum()))

fig = px.bar(
    filtered_df,
    x="risk_bucket",
    y="count(*)",
    title="Risk Bucket Distribution"
)

st.plotly_chart(fig, use_container_width=True, key="unique_chart_001")

st.success("Dashboard loaded successfully")
