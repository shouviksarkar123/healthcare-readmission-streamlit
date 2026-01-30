import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== TOP PROJECT BANNER ==================
st.markdown(
    """
    <div style="padding:15px; border-radius:10px; background-color:#f5f7fa;">
        <h2>🏥 AI-Powered Patient Readmission Dashboard</h2>
        <p><b>Built by:</b> Shouvik Sarkar (Self Project)</p>
        <p>
        <b>Challenge:</b> IDC Resume Project Challenge |
        <b>Organisers:</b> Indian Data Club & Codebasics |
        <b>Sponsor:</b> Databricks
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Production-grade analytics for 30-day hospital readmission risk")

# ================== DATE & TIME ==================
st.markdown(
    f"🕒 **Last Updated:** {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
)

st.divider()

# ================== STEP 1 : FILE LOADER ==================
with st.status("🔄 Step 1: Loading Dataset", expanded=True) as status:

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

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.004)
        progress.progress(i + 1)

    status.update(label="✅ Dataset Loaded Successfully", state="complete")

# ================== STEP 2 : COLUMN DISCOVERY ==================
with st.status("🔍 Step 2: Understanding Dataset", expanded=False):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    with st.expander("📌 View Dataset Columns"):
        st.write(df.columns.tolist())

    st.info(f"Detected {len(numeric_cols)} numeric and {len(cat_cols)} categorical columns")

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

# ================== OPTIONAL PATIENT INFO ==================
with st.expander("🧑‍⚕️ Sample Patient / Disease Info (if available)"):

    for col in ["patient_id", "patient_nbr", "disease", "diagnosis", "medical_specialty"]:
        if col in df.columns:
            st.write(f"**{col}** sample values:", df[col].dropna().unique()[:5])

# ================== STEP 3 : DASHBOARD NAVIGATION ==================
dashboard = st.sidebar.radio(
    "📊 Dashboard Sections",
    [
        "🧑‍💼 Executive Overview",
        "🤖 AI Risk Distribution",
        "👵 Risk by Age Group",
        "🏨 Hospital Utilization",
        "🩺 Diabetes Impact",
        "📋 Data Table"
    ]
)

# ================== EXECUTIVE OVERVIEW ==================
if dashboard == "🧑‍💼 Executive Overview":

    st.subheader("📌 Executive Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", len(df))
    c2.metric("Numeric Metrics", len(numeric_cols))
    c3.metric("Categorical Features", len(cat_cols))
    c4.metric(
        "Primary Avg",
        round(df[numeric_cols[0]].mean(), 2) if numeric_cols else "N/A"
    )

    with st.expander("📈 Metric Distribution"):
        metric = st.selectbox("Select Metric", numeric_cols)
        fig = px.histogram(
            df,
            x=metric,
            nbins=40,
            color_discrete_sequence=["#4CC9F0"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info("💡 High-level snapshot for hospital leadership & management")

# ================== AI RISK DISTRIBUTION ==================
elif dashboard == "🤖 AI Risk Distribution":

    st.subheader("🤖 AI Risk Analysis")

    y = st.selectbox("Risk Metric", numeric_cols)
    x = st.selectbox("Segment By", cat_cols)

    tabs = st.tabs(["📊 Bar", "📈 Histogram", "📦 Box"])

    with tabs[0]:
        st.plotly_chart(
            px.bar(df, x=x, y=y, color=x,
                   color_discrete_sequence=px.colors.qualitative.Set2),
            use_container_width=True
        )

    with tabs[1]:
        st.plotly_chart(
            px.histogram(df, x=y, color=x,
                         color_discrete_sequence=px.colors.qualitative.Set2),
            use_container_width=True
        )

    with tabs[2]:
        st.plotly_chart(
            px.box(df, x=x, y=y, color=x,
                   color_discrete_sequence=px.colors.qualitative.Set2),
            use_container_width=True
        )

# ================== RISK BY AGE ==================
elif dashboard == "👵 Risk by Age Group":

    st.subheader("👵 Risk by Age")

    age = st.selectbox("Age Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)

    st.plotly_chart(
        px.bar(df, x=age, y=risk, color=age,
               color_discrete_sequence=px.colors.qualitative.Pastel),
        use_container_width=True
    )

# ================== HOSPITAL UTILIZATION ==================
elif dashboard == "🏨 Hospital Utilization":

    st.subheader("🏨 Hospital Utilization vs Risk")

    x = st.selectbox("Risk Category", cat_cols)
    y = st.selectbox("Utilization Metric", numeric_cols)
    agg = st.radio("Aggregation", ["mean", "sum", "count"], horizontal=True)

    df_agg = df.groupby(x)[y].agg(agg).reset_index()

    st.plotly_chart(
        px.bar(df_agg, x=x, y=y, color=x,
               color_discrete_sequence=px.colors.qualitative.Dark24),
        use_container_width=True
    )

# ================== DIABETES IMPACT ==================
elif dashboard == "🩺 Diabetes Impact":

    st.subheader("🩺 Diabetes / Disease Impact")

    diab = st.selectbox("Disease / Diabetes Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)

    st.plotly_chart(
        px.bar(df, x=diab, y=risk, color=diab,
               color_discrete_sequence=px.colors.qualitative.Safe),
        use_container_width=True
    )

# ================== DATA TABLE ==================
elif dashboard == "📋 Data Table":

    st.subheader("📋 Dataset Explorer")
    rows = st.slider("Rows to display", 10, 300, 50)
    st.dataframe(df.head(rows), use_container_width=True)

# ================== FINAL FOOTER ==================
st.divider()

st.markdown(
    """
    ### 👤 Project Ownership & Credits

    **Project Name:** AI-Powered Patient Readmission Prediction  
    **Built by:** **Shouvik Sarkar** (Self-Directed End-to-End Project)

    **Challenge Context:**  
    IDC Resume Project Challenge  
    Organised by **Indian Data Club (IDC)** & **Codebasics**  
    Sponsored by **Databricks**

    **Tech Stack:**  
    Databricks • Delta Lake • PySpark • MLflow • Databricks SQL • Streamlit
    """
)

st.caption("© 2026 Shouvik Sarkar | Healthcare AI • Databricks Ecosystem")
