import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== HEADER ==================
st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Production-grade analytics for 30-day hospital readmission risk")

# ================== FILE LOADER ==================
st.sidebar.header("📂 Dataset Control")

csv_files = [f for f in os.listdir() if f.endswith(".csv")]

if not csv_files:
    st.error("❌ No CSV files found in project directory")
    st.stop()

selected_file = st.sidebar.selectbox("Select CSV Dataset", csv_files)

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

df = load_data(selected_file)
st.success(f"Dataset loaded: **{selected_file}**")

# ================== COLUMN DISCOVERY ==================
numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

with st.expander("🔍 Dataset Columns"):
    st.write(df.columns.tolist())

# ================== GLOBAL FILTER ==================
st.sidebar.header("🎛 Global Filters")

if cat_cols:
    filter_col = st.sidebar.selectbox("Filter Column", cat_cols)
    filter_vals = st.sidebar.multiselect(
        "Filter Values",
        df[filter_col].dropna().unique(),
        default=df[filter_col].dropna().unique()
    )
    df = df[df[filter_col].isin(filter_vals)]

# ================== DASHBOARD SELECTION ==================
dashboard = st.sidebar.radio(
    "📊 Dashboard Views",
    [
        "Executive Overview",
        "AI Risk Distribution",
        "Risk by Age Group",
        "Hospital Utilization Analysis",
        "Diabetes Impact Analysis",
        "Data Table"
    ]
)

# ================== EXECUTIVE OVERVIEW ==================
if dashboard == "Executive Overview":

    st.subheader("📌 Executive KPIs")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Records", len(df))
    k2.metric("Numeric Metrics", len(numeric_cols))
    k3.metric("Categorical Features", len(cat_cols))

    if numeric_cols:
        k4.metric("Avg of Primary Metric", round(df[numeric_cols[0]].mean(), 2))
    else:
        k4.metric("Avg Metric", "N/A")

    if numeric_cols:
        metric = st.selectbox("Select Metric for Distribution", numeric_cols)
        fig = px.histogram(
            df,
            x=metric,
            nbins=40,
            title=f"Distribution of {metric}",
            color_discrete_sequence=["#4CC9F0"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "📘 **Business Insight:** This view gives leadership a high-level understanding "
        "of data volume, feature richness, and overall risk distribution."
    )

# ================== AI RISK DISTRIBUTION ==================
elif dashboard == "AI Risk Distribution":

    st.subheader("🤖 AI Risk Distribution Analysis")

    y = st.selectbox("Select AI Risk Metric", numeric_cols)
    x = st.selectbox("Group By Category", cat_cols)

    chart_type = st.radio("Chart Type", ["Bar", "Histogram", "Box"], horizontal=True)

    if chart_type == "Bar":
        fig = px.bar(df, x=x, y=y, color=x,
                     title="AI Risk by Category",
                     color_discrete_sequence=px.colors.qualitative.Set2)
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=y, color=x,
                           title="AI Risk Distribution",
                           color_discrete_sequence=px.colors.qualitative.Set2)
    else:
        fig = px.box(df, x=x, y=y, color=x,
                     title="AI Risk Spread",
                     color_discrete_sequence=px.colors.qualitative.Set2)

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "📘 **Business Insight:** Shows how AI-predicted risk varies across segments. "
        "Useful for identifying high-risk cohorts."
    )

# ================== RISK BY AGE ==================
elif dashboard == "Risk by Age Group":

    st.subheader("👵 Risk Stratification by Age")

    age = st.selectbox("Age Group Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)

    fig = px.bar(
        df, x=age, y=risk, color=age,
        title="Readmission Risk by Age Group",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "📘 **Business Insight:** Identifies age segments with elevated readmission risk, "
        "supporting targeted preventive care."
    )

# ================== HOSPITAL UTILIZATION ==================
elif dashboard == "Hospital Utilization Analysis":

    st.subheader("🏨 Hospital Utilization vs Risk")

    x = st.selectbox("Risk Category", cat_cols)
    y = st.selectbox("Utilization Metric", numeric_cols)

    agg = st.selectbox("Aggregation Method", ["mean", "sum", "count"])

    df_agg = df.groupby(x)[y].agg(agg).reset_index()

    fig = px.bar(
        df_agg, x=x, y=y, color=x,
        title=f"Hospital Utilization ({agg}) by Risk",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "📘 **Business Insight:** Helps operations teams optimize bed usage "
        "and resource allocation based on risk tiers."
    )

# ================== DIABETES IMPACT ==================
elif dashboard == "Diabetes Impact Analysis":

    st.subheader("🩺 Impact of Diabetes on Readmission")

    diab = st.selectbox("Diabetes Indicator", cat_cols)
    risk = st.selectbox("Readmission Metric", numeric_cols)

    fig = px.bar(
        df, x=diab, y=risk, color=diab,
        title="Diabetes vs Readmission Risk",
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "📘 **Business Insight:** Quantifies how chronic conditions like diabetes "
        "increase readmission probability."
    )

# ================== TABLE VIEW ==================
elif dashboard == "Data Table":

    st.subheader("📋 Raw Dataset Explorer")

    rows = st.slider("Rows to display", 10, 200, 50)
    st.dataframe(df.head(rows), use_container_width=True)

# ================== FOOTER ==================
st.success("✅ Production-grade dashboard rendered successfully")
st.caption("Databricks → Streamlit | Healthcare Analytics | Interview-Ready Project")
