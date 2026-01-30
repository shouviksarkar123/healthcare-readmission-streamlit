import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Healthcare Readmission Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.markdown("Predicting **30-day hospital readmission risk** using AI")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("30Day Patient Readmission Status-2026-01-30.csv")

df = load_data()

# ---------------- SIDEBAR FILTER ----------------
st.sidebar.header("Filters")

risk_options = ["All"] + sorted(df["risk_bucket"].dropna().unique().tolist())
selected_risk = st.sidebar.selectbox(
    "Select Risk Bucket",
    risk_options
)

status_options = ["All"] + sorted(df["readmit_status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox(
    "Select Readmission Status",
    status_options
)

filtered_df = df.copy()

if selected_risk != "All":
    filtered_df = filtered_df[filtered_df["risk_bucket"] == selected_risk]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["readmit_status"] == selected_status]

# ---------------- KPI SECTION ----------------
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Total Patients", int(filtered_df["count(*)"].sum()))

with kpi2:
    st.metric(
        "Avg Readmit Probability",
        round(filtered_df["readmit_probability"].mean(), 2)
    )

with kpi3:
    st.metric(
        "High Risk %",
        round(
            (filtered_df[filtered_df["risk_bucket"] == "High"]["count(*)"].sum()
             / filtered_df["count(*)"].sum()) * 100
            if len(filtered_df) > 0 else 0,
            2
        )
    )

st.divider()

# ---------------- CHART 1: Risk Bucket Distribution ----------------
fig1 = px.bar(
    filtered_df,
    x="risk_bucket",
    y="count(*)",
    color="risk_bucket",
    title="Risk Bucket Distribution",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True, key="chart_risk_bucket")

# ---------------- CHART 2: Readmission Status ----------------
fig2 = px.bar(
    filtered_df,
    x="readmit_status",
    y="count(*)",
    color="readmit_status",
    title="Readmission Status Distribution",
    text_auto=True
)

st.plotly_chart(fig2, use_container_width=True, key="chart_readmit_status")

# ---------------- CHART 3: Probability Distribution ----------------
fig3 = px.histogram(
    filtered_df,
    x="readmit_probability",
    nbins=20,
    title="Readmission Probability Distribution"
)

st.plotly_chart(fig3, use_container_width=True, key="chart_probability")

# ---------------- CHART 4: Age Group vs Risk ----------------
fig4 = px.bar(
    filtered_df,
    x="age_group",
    y="count(*)",
    color="risk_bucket",
    title="Age Group vs Risk Level",
    text_auto=True
)

st.plotly_chart(fig4, use_container_width=True, key="chart_age_risk")

# ---------------- DATA TABLE ----------------
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.success("✅ Live AI Readmission Dashboard Running Successfully")
