import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- TITLE ----------------
st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Predicting 30-day hospital readmission risk using AI")

# ---------------- FILE SELECTION ----------------
st.sidebar.header("📂 Dataset Selection")

csv_files = [f for f in os.listdir() if f.endswith(".csv")]

if not csv_files:
    st.error("❌ No CSV files found in project folder")
    st.stop()

selected_file = st.sidebar.selectbox("Select CSV file", csv_files)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(selected_file)

st.success(f"Loaded dataset: **{selected_file}**")

with st.expander("🔍 Show Available Columns"):
    st.write(list(df.columns))

numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ---------------- GLOBAL FILTER ----------------
st.sidebar.header("🎛 Global Filter")

if cat_cols:
    filter_col = st.sidebar.selectbox("Filter by category", cat_cols)
    filter_values = st.sidebar.multiselect(
        "Select values",
        df[filter_col].dropna().unique(),
        default=df[filter_col].dropna().unique()
    )
    df = df[df[filter_col].isin(filter_values)]

# ---------------- DASHBOARD TYPE ----------------
dashboard_type = st.sidebar.selectbox(
    "📊 Select Dashboard View",
    [
        "Overview",
        "AI Risk Distribution",
        "Risk by Age Group",
        "Hospital Utilization by Risk",
        "Diabetes Impact on Readmission",
        "Table View"
    ]
)

# ---------------- OVERVIEW ----------------
if dashboard_type == "Overview":

    st.subheader("📌 Key Metrics")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Records", len(df))
    c2.metric("Numeric Columns", len(numeric_cols))
    c3.metric("Categorical Columns", len(cat_cols))

    if numeric_cols:
        chart_col = st.selectbox("Select metric for distribution", numeric_cols)

        fig = px.histogram(
            df,
            x=chart_col,
            nbins=40,
            title=f"Distribution of {chart_col}",
            color_discrete_sequence=["#4CC9F0"]
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- AI RISK DISTRIBUTION ----------------
elif dashboard_type == "AI Risk Distribution":

    st.subheader("🤖 AI Risk Distribution")

    y_col = st.selectbox("Select AI Risk Metric", numeric_cols)
    x_col = st.selectbox("Select Category", cat_cols)

    chart_type = st.radio("Chart Type", ["Bar", "Histogram"], horizontal=True)

    if chart_type == "Bar":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=x_col,
            title="AI Risk Distribution",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    else:
        fig = px.histogram(
            df,
            x=y_col,
            color=x_col,
            title="AI Risk Histogram",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- RISK BY AGE ----------------
elif dashboard_type == "Risk by Age Group":

    st.subheader("👵 Readmission Risk by Age Group")

    age_col = st.selectbox("Select Age Group Column", cat_cols)
    risk_col = st.selectbox("Select Risk Metric", numeric_cols)

    fig = px.bar(
        df,
        x=age_col,
        y=risk_col,
        color=age_col,
        title="Risk by Age Group",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- HOSPITAL UTILIZATION ----------------
elif dashboard_type == "Hospital Utilization by Risk":

    st.subheader("🏨 Hospital Utilization vs AI Risk")

    x_col = st.selectbox("Select Risk Category", cat_cols)
    y_col = st.selectbox("Select Utilization Metric", numeric_cols)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        title="Hospital Utilization by Risk Level",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- DIABETES IMPACT ----------------
elif dashboard_type == "Diabetes Impact on Readmission":

    st.subheader("🩺 Diabetes Impact Analysis")

    x_col = st.selectbox("Select Diabetes Indicator", cat_cols)
    y_col = st.selectbox("Select Readmission Metric", numeric_cols)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        title="Impact of Diabetes on Readmission Risk",
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TABLE VIEW ----------------
elif dashboard_type == "Table View":

    st.subheader("📋 Dataset Preview")

    rows = st.slider("Number of rows to display", 5, 100, 20)
    st.dataframe(df.head(rows), use_container_width=True)

# ---------------- FOOTER ----------------
st.success("✅ Dashboard loaded successfully")
st.caption("Built with Streamlit • Databricks-style Analytics • Interview-Ready Project")
