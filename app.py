import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== HEADER ==================
st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Production-grade analytics for 30-day hospital readmission risk")

# ================== STEP 1 : FILE LOADER ==================
with st.status("🔄 Step 1: Loading Dataset", expanded=True) as status:

    st.sidebar.header("📂 Dataset Control")
    csv_files = [f for f in os.listdir() if f.endswith(".csv")]

    if not csv_files:
        st.error("❌ No CSV files found")
        st.stop()

    selected_file = st.sidebar.selectbox("Select CSV Dataset", csv_files)

    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)

    df = load_data(selected_file)

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress.progress(i + 1)

    st.toast("Dataset loaded successfully 🎉")
    status.update(label="✅ Dataset Loaded", state="complete")

# ================== STEP 2 : COLUMN DISCOVERY ==================
with st.status("🔍 Step 2: Understanding Dataset", expanded=False):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    with st.expander("📌 Click to view dataset columns"):
        st.write(df.columns.tolist())

    st.info(f"Detected {len(numeric_cols)} numeric and {len(cat_cols)} categorical features")

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

# ================== STEP 3 : DASHBOARD NAVIGATION ==================
with st.status("📊 Step 3: Choose Dashboard View", expanded=True):

    dashboard = st.sidebar.radio(
        "Dashboard Sections",
        [
            "🧑‍💼 Executive Overview",
            "🤖 AI Risk Distribution",
            "👵 Risk by Age Group",
            "🏨 Hospital Utilization",
            "🩺 Diabetes Impact",
            "📋 Data Table"
        ]
    )

# ================== STEP 4 : DASHBOARDS ==================

# ---------- EXECUTIVE OVERVIEW ----------
if dashboard == "🧑‍💼 Executive Overview":

    st.subheader("📌 Executive Summary")

    with st.spinner("Loading KPIs..."):
        time.sleep(0.5)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", len(df))
    c2.metric("Numeric Metrics", len(numeric_cols))
    c3.metric("Categorical Features", len(cat_cols))
    c4.metric("Primary Avg", round(df[numeric_cols[0]].mean(), 2) if numeric_cols else "N/A")

    with st.expander("📈 Click to explore distribution"):
        metric = st.selectbox("Select Metric", numeric_cols)
        fig = px.histogram(
            df,
            x=metric,
            nbins=40,
            title=f"Distribution of {metric}",
            color_discrete_sequence=["#4CC9F0"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info("💡 Leadership-level snapshot for quick decision making")

# ---------- AI RISK DISTRIBUTION ----------
elif dashboard == "🤖 AI Risk Distribution":

    st.subheader("🤖 AI Risk Exploration")

    tab1, tab2, tab3 = st.tabs(["📊 Bar", "📈 Histogram", "📦 Box"])

    y = st.selectbox("Risk Metric", numeric_cols)
    x = st.selectbox("Segment By", cat_cols)

    with tab1:
        fig = px.bar(df, x=x, y=y, color=x,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = px.histogram(df, x=y, color=x,
                           color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = px.box(df, x=x, y=y, color=x,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

# ---------- RISK BY AGE ----------
elif dashboard == "👵 Risk by Age Group":

    st.subheader("👵 Age-based Risk Analysis")

    age = st.selectbox("Age Group Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)

    fig = px.bar(
        df, x=age, y=risk, color=age,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- HOSPITAL UTILIZATION ----------
elif dashboard == "🏨 Hospital Utilization":

    st.subheader("🏨 Utilization vs Risk")

    x = st.selectbox("Risk Category", cat_cols)
    y = st.selectbox("Utilization Metric", numeric_cols)
    agg = st.radio("Aggregation", ["mean", "sum", "count"], horizontal=True)

    df_agg = df.groupby(x)[y].agg(agg).reset_index()

    fig = px.bar(
        df_agg, x=x, y=y, color=x,
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- DIABETES IMPACT ----------
elif dashboard == "🩺 Diabetes Impact":

    st.subheader("🩺 Chronic Condition Impact")

    diab = st.selectbox("Diabetes Column", cat_cols)
    risk = st.selectbox("Readmission Metric", numeric_cols)

    fig = px.bar(
        df, x=diab, y=risk, color=diab,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- DATA TABLE ----------
elif dashboard == "📋 Data Table":

    st.subheader("📋 Raw Dataset Viewer")
    rows = st.slider("Rows to show", 10, 300, 50)
    st.dataframe(df.head(rows), use_container_width=True)

# ================== FOOTER ==================
st.success("✅ Interactive dashboard loaded successfully")
st.caption("Databricks → Streamlit | Healthcare AI | Product-style Analytics")
