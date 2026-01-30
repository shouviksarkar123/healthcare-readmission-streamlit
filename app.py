import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide"
)

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.markdown("Predicting 30-day hospital readmission risk using AI")

# ---------------- FILE SELECTION ----------------
st.sidebar.header("📂 Select Dashboard")

csv_files = [f for f in os.listdir() if f.endswith(".csv")]

if not csv_files:
    st.error("❌ No CSV files found in project folder")
    st.stop()

selected_file = st.sidebar.selectbox("Select CSV file", csv_files)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(selected_file)

st.success(f"Loaded: {selected_file}")
st.expander("🔍 Show Columns").write(list(df.columns))

numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ---------------- DASHBOARD TYPE ----------------
dashboard_type = st.sidebar.selectbox(
    "Select View",
    [
        "Overview",
        "AI Risk Distribution",
        "Risk by Age Group",
        "Hospital Utilization by Risk",
        "Diabetes Impact on Readmission",
        "Actual vs AI Readmission",
        "Table View"
    ]
)

# ---------------- OVERVIEW ----------------
if dashboard_type == "Overview":

    st.subheader("📊 Overall Metrics")

    if numeric_cols:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Rows", len(df))

        with col2:
            st.metric("Numeric Columns", len(numeric_cols))

        with col3:
            st.metric("Avg Value", round(df[numeric_cols[0]].mean(), 2))

    if numeric_cols:
        fig = px.histogram(
            df,
            x=numeric_cols[0],
            nbins=30,
            title="Overall Distribution",
            color_discrete_sequence=["#00B4D8"]
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- AI RISK DISTRIBUTION ----------------
elif dashboard_type == "AI Risk Distribution":

    st.subheader("🤖 AI Risk Distribution")

    y_col = st.selectbox("Select AI Risk Column", numeric_cols)
    x_col = st.selectbox("Select Category", cat_cols)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title="AI Risk Distribution",
        color=x_col,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- RISK BY AGE ----------------
elif dashboard_type == "Risk by Age Group":

    st.subheader("👵 Risk by Age Group")

    age_col = st.selectbox("Select Age Column", cat_cols)
    risk_col = st.selectbox("Select Risk Column", numeric_cols)

    fig = px.bar(
        df,
        x=age_col,
        y=risk_col,
        title="Readmission Risk by Age Group",
        color=age_col,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- HOSPITAL UTILIZATION ----------------
elif dashboard_type == "Hospital Utilization by Risk":

    st.subheader("🏨 Hospital Utilization by Risk")

    x_col = st.selectbox("Select Risk Bucket", cat_cols)
    y_col = st.selectbox("Select Utilization Metric", numeric_cols)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title="Hospital Utilization by AI Risk",
        color=x_col,
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- DIABETES IMPACT ----------------
elif dashboard_type == "Diabetes Impact on Readmission":

    st.subheader("🩺 Diabetes Impact on Readmission")

    x_col = st.selectbox("Select Diabetes Column", cat_cols)
    y_col = st.selectbox("Select Readmission Metric", numeric_cols)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title="Impact of Diabetes on Readmission",
        color=x_col,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ACTUAL vs AI (FINAL FIX) ----------------
elif dashboard_type == "Actual vs AI Readmission":

    st.subheader("📊 Actual vs AI Readmission Comparison")

    if len(numeric_cols) < 2:
        st.error("❌ Need at least two numeric columns")
    else:
        col1, col2 = st.columns(2)

        with col1:
            actual_col = st.selectbox("Select ACTUAL column", numeric_cols)

        with col2:
            ai_col = st.selectbox(
                "Select AI column",
                [c for c in numeric_cols if c != actual_col]
            )

        x_col = st.selectbox("Select Category", cat_cols)

        fig = px.bar(
            df,
            x=x_col,
            y=[actual_col, ai_col],
            barmode="group",
            title="Actual vs AI Readmission",
            color_discrete_sequence=["#EF476F", "#06D6A0"]
        )

        fig.update_traces(texttemplate="%{y}", textposition="outside")
        fig.update_layout(
            yaxis_title="Patient Count",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- TABLE VIEW ----------------
elif dashboard_type == "Table View":

    st.subheader("📋 Data Table")
    st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.success("✅ Dashboard rendered successfully")
