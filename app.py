import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide"
)

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Databricks Healthcare Analytics → Streamlit")

DATA_DIR = Path(".")

DASHBOARDS = {
    "AI Risk Distribution":
        "AIBased Patient Risk Distribution-2026-01-30.csv",

    "Risk by Age Group":
        "Readmission Risk by Age Group-2026-01-30.csv",

    "Hospital Utilization by Risk":
        "Hospital Utilization by AI Risk Level-2026-01-30.csv",

    "Diabetes Impact on Readmission":
        "Impact of Diabetes on Readmission Risk-2026-01-30.csv",

    "Actual vs AI Risk":
        "AI Risk vs Actual Readmission-2026-01-30.csv",

    "Overall Readmission Risk Level":
        "Overall Readmission Risk Level-2026-01-30.csv",

    "30-Day Readmission Status":
        "30Day Patient Readmission Status-2026-01-30.csv"
}

# Sidebar
selected_dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    list(DASHBOARDS.keys())
)

file_path = DATA_DIR / DASHBOARDS[selected_dashboard]

st.success("CSV loaded successfully")

df = pd.read_csv(file_path)

# Show columns (debug / transparency)
with st.expander("🔍 Show Columns"):
    st.write(df.columns.tolist())
    st.dataframe(df.head())

st.divider()

# ---------- TABLE VIEW ----------
st.subheader(selected_dashboard)
st.dataframe(df, use_container_width=True)

# ---------- AUTO BAR CHART ----------
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if len(numeric_cols) >= 1:
    x_col = df.columns[0]
    y_col = numeric_cols[-1]

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{selected_dashboard} (Databricks Style)"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No numeric column found for chart")

st.success("Dashboard rendered successfully")
