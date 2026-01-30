import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Healthcare Readmission", layout="wide")

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.markdown("Predicting 30-day hospital readmission risk using AI")

# ---- Load Data ----
df = pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")

# ---- Sidebar ----
st.sidebar.header("Filters")

risk = st.sidebar.selectbox(
    "Select Risk Bucket",
    sorted(df["risk_bucket"].unique()),
    key="risk_select"
)

# ---- Filtered Data ----
filtered_df = df[df["risk_bucket"] == risk]

# ---- KPI ----
st.metric(
    label="Total Patients",
    value=int(filtered_df["count(*)"].sum()),
)

# ---- Chart Container (IMPORTANT) ----
chart_container = st.container()

with chart_container:
    fig = px.bar(
        filtered_df,
        x="risk_bucket",
        y="count(*)",
        color="risk_bucket",
        title="Patient Distribution by Risk Bucket"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="risk_bucket_chart"
    )

st.success("✅ Dashboard loaded without errors")
