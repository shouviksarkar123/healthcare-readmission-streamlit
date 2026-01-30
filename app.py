import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Healthcare Readmission Dashboard",
    layout="wide"
)

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.markdown("Predicting 30-day hospital readmission risk using AI")

# -------------------------------------------------
# UTILITY FUNCTIONS (VERY IMPORTANT)
# -------------------------------------------------
@st.cache_data
def load_csv(file_name):
    if not os.path.exists(file_name):
        st.error(f"❌ File not found: {file_name}")
        return None
    return pd.read_csv(file_name)


def safe_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def show_columns(df):
    with st.expander("🔍 Show Columns"):
        st.write(df.columns.tolist())


# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
st.sidebar.header("📊 Dashboards")

dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "AI Risk Distribution",
        "Risk by Age Group",
        "Hospital Utilization by Risk",
        "Diabetes Impact on Readmission",
        "Overall Readmission Risk Level",
        "Actual vs AI Risk"
    ]
)

# -------------------------------------------------
# DASHBOARD 1: AI RISK DISTRIBUTION
# -------------------------------------------------
if dashboard == "AI Risk Distribution":
    df = load_csv("AI Based Patient Risk Distribution-2026-01-30.csv")
    if df is not None:
        show_columns(df)

        risk_col = safe_col(df, ["risk_bucket", "risk_level"])
        count_col = safe_col(df, ["count(*)", "count", "total"])

        if risk_col and count_col:
            fig = px.pie(
                df,
                names=risk_col,
                values=count_col,
                title="AI Risk Distribution"
            )
            st.plotly_chart(fig, use_container_width=True, key="risk_dist")
        else:
            st.error("Required columns missing in this CSV")

# -------------------------------------------------
# DASHBOARD 2: RISK BY AGE GROUP
# -------------------------------------------------
elif dashboard == "Risk by Age Group":
    df = load_csv("Readmission Risk by Age Group-2026-01-30.csv")
    if df is not None:
        show_columns(df)

        age_col = safe_col(df, ["age_group", "age"])
        risk_col = safe_col(df, ["risk_bucket", "risk_level"])
        count_col = safe_col(df, ["count(*)", "count"])

        if age_col and risk_col and count_col:
            fig = px.bar(
                df,
                x=age_col,
                y=count_col,
                color=risk_col,
                barmode="group",
                title="Readmission Risk by Age Group"
            )
            st.plotly_chart(fig, use_container_width=True, key="age_risk")
        else:
            st.error("Required columns missing in this CSV")

# -------------------------------------------------
# DASHBOARD 3: HOSPITAL UTILIZATION
# -------------------------------------------------
elif dashboard == "Hospital Utilization by Risk":
    df = load_csv("Hospital Utilization by AI Risk Level-2026-01-30.csv")
    if df is not None:
        show_columns(df)

        util_col = safe_col(df, ["hospital_utilization", "utilization"])
        risk_col = safe_col(df, ["risk_bucket"])
        count_col = safe_col(df, ["count(*)", "count"])

        if util_col and risk_col and count_col:
            fig = px.bar(
                df,
                x=util_col,
                y=count_col,
                color=risk_col,
                title="Hospital Utilization by AI Risk Level"
            )
            st.plotly_chart(fig, use_container_width=True, key="util_risk")
        else:
            st.error("Required columns missing in this CSV")

# -------------------------------------------------
# DASHBOARD 4: DIABETES IMPACT
# -------------------------------------------------
elif dashboard == "Diabetes Impact on Readmission":
    df = load_csv("Impact of Diabetes on Readmission Risk-2026-01-30.csv")
    if df is not None:
        show_columns(df)

        diabetes_col = safe_col(df, ["diabetes_status", "diabetes"])
        risk_col = safe_col(df, ["risk_bucket"])
        count_col = safe_col(df, ["count(*)", "count"])

        if diabetes_col and risk_col and count_col:
            fig = px.bar(
                df,
                x=diabetes_col,
                y=count_col,
                color=risk_col,
                title="Impact of Diabetes on Readmission Risk"
            )
            st.plotly_chart(fig, use_container_width=True, key="diabetes_risk")
        else:
            st.error("Required columns missing in this CSV")

# -------------------------------------------------
# DASHBOARD 5: OVERALL READMISSION RISK
# -------------------------------------------------
elif dashboard == "Overall Readmission Risk Level":
    df = load_csv("Overall Readmission Risk Level-2026-01-30.csv")
    if df is not None:
        show_columns(df)

        risk_col = safe_col(df, ["risk_bucket"])
        count_col = safe_col
