import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Healthcare Dashboard", layout="wide")

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("End-to-end analytics powered by Databricks + AI")

# ===============================
# Sidebar Navigation
# ===============================
dashboard = st.sidebar.selectbox(
    "📊 Select Dashboard",
    [
        "30-Day Readmission Status",
        "AI Risk Distribution",
        "AI Risk vs Actual Readmission",
        "Hospital Utilization by Risk",
        "Impact of Diabetes",
        "Overall Risk Level",
        "Risk by Age Group",
        "Risk by Hospital Utilization"
    ]
)

# ===============================
# Helper function
# ===============================
def load_csv(name):
    return pd.read_csv(name)

# ===============================
# DASHBOARDS
# ===============================

if dashboard == "30-Day Readmission Status":
    df = load_csv("30Day Patient Readmission Status-2026-01-30.csv")

    st.metric("Total Patients", int(df["count(*)"].sum()))

    fig = px.bar(
        df,
        x="readmit_status",
        y="count(*)",
        title="Readmission Status Count",
        text="count(*)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)

# --------------------------------------------------

elif dashboard == "AI Risk Distribution":
    df = load_csv("AI Based Patient Risk Distribution-2026-01-30.csv")

    fig = px.pie(
        df,
        names="risk_bucket",
        values="count(*)",
        title="AI Risk Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------

elif dashboard == "AI Risk vs Actual Readmission":
    df = load_csv("AI Risk vs Actual Readmission-2026-01-30.csv")

    fig = px.bar(
        df,
        x="risk_bucket",
        y="count(*)",
        color="readmit_status",
        barmode="group",
        title="AI Risk vs Actual Readmission"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------

elif dashboard == "Hospital Utilization by Risk":
    df = load_csv("Hospital Utilization by AI Risk Level-2026-01-30.csv")

    fig = px.bar(
        df,
        x="risk_bucket",
        y="count(*)",
        color="hospital_utilization",
        title="Hospital Utilization by AI Risk Level"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------

elif dashboard == "Impact of Diabetes":
    df = load_csv("Impact of Diabetes on Readmission Risk-2026-01-30.csv")

    fig = px.bar(
        df,
        x="diabetes",
        y="count(*)",
        color="risk_bucket",
        title="Impact of Diabetes on Readmission Risk"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------

elif dashboard == "Overall Risk Level":
    df = load_csv("Overall Readmission Risk Level-2026-01-30.csv")

    fig = px.bar(
        df,
        x="risk_bucket",
        y="count(*)",
        title="Overall Readmission Risk Level"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------

elif dashboard == "Risk by Age Group":
    df = load_csv("Readmission Risk by Age Group-2026-01-30.csv")

    fig = px.bar(
        df,
        x="age_group",
        y="count(*)",
        color="risk_bucket",
        title="Readmission Risk by Age Group"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------

elif dashboard == "Risk by Hospital Utilization":
    df = load_csv("Readmission Risk by Hospital Utilization-2026-01-30.csv")

    fig = px.bar(
        df,
        x="hospital_utilization",
        y="count(*)",
        color="risk_bucket",
        title="Readmission Risk by Hospital Utilization"
    )
    st.plotly_chart(fig, use_container_width=True)

# ===============================
st.success("✅ All dashboards loaded successfully")
