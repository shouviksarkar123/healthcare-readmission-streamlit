import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Readmission", layout="wide")

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Predicting 30-day hospital readmission risk using AI")

# Load data
df = pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")

# ✅ Sidebar filter (REAL column)
status = st.sidebar.selectbox(
    "Select Readmission Status",
    sorted(df["readmit_status"].unique())
)

filtered_df = df[df["readmit_status"] == status]

# KPI
st.metric(
    "Total Patients",
    int(filtered_df["count(*)"].sum())
)

# Chart (SAFE – no duplicate id)
chart = st.empty()

fig = px.bar(
    filtered_df,
    x="readmit_status",
    y="count(*)",
    title="Readmission Status Count"
)

chart.plotly_chart(fig, use_container_width=True)

st.success("✅ Dashboard loaded successfully")
