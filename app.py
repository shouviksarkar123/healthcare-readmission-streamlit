import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide"
)

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Predicting 30-day hospital readmission risk using AI")

DATA_DIR = Path(".")

# ---------------- DASHBOARD MAP ----------------
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

# ---------------- SIDEBAR ----------------
selected_dashboard = st.sidebar.selectbox(
    "📊 Select Dashboard",
    list(DASHBOARDS.keys())
)

file_path = DATA_DIR / DASHBOARDS[selected_dashboard]

# ---------------- LOAD CSV ----------------
df = pd.read_csv(file_path)
st.success("CSV loaded successfully")

with st.expander("🔍 Show Columns"):
    st.write(df.columns.tolist())
    st.dataframe(df.head())

st.divider()
st.subheader(selected_dashboard)

# ---------------- TABLE VIEW ----------------
st.dataframe(df, use_container_width=True)

# ---------------- COLOR PALETTE ----------------
COLOR_SEQ = px.colors.qualitative.Set2

# ---------------- CHART LOGIC ----------------

# ✅ ACTUAL vs AI (SPECIAL)
if selected_dashboard == "Actual vs AI Risk":

    risk_col = df.columns[0]

    actual_col = None
    ai_col = None

    for c in df.columns:
        cl = c.lower()
        if "actual" in cl:
            actual_col = c
        if "ai" in cl or "pred" in cl:
            ai_col = c

    if actual_col and ai_col:
        fig = px.bar(
            df,
            x=risk_col,
            y=[actual_col, ai_col],
            barmode="group",
            color_discrete_sequence=COLOR_SEQ,
            title="Actual vs AI Predicted Readmission"
        )

        fig.update_layout(
            xaxis_title="Risk Category",
            yaxis_title="Patient Count",
            legend_title="Metric",
            plot_bgcolor="rgba(0,0,0,0)",
            bargap=0.25
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Expected Actual & AI columns not found")

# ---------------- ALL OTHER DASHBOARDS ----------------
else:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        x_col = df.columns[0]
        y_col = numeric_cols[-1]

        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=x_col,
            color_discrete_sequence=COLOR_SEQ,
            title=f"{selected_dashboard}"
        )

        fig.update_layout(
            xaxis_title=x_col.replace("_", " ").title(),
            yaxis_title=y_col.replace("_", " ").title(),
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )

        fig.update_traces(
            texttemplate="%{y}",
            textposition="outside"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No numeric column available for chart")

st.success("Dashboard rendered successfully")
