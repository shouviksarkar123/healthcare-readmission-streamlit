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

# ================== GLOBAL THEME + AUTO COLOR ANIMATION ==================
st.markdown("""
<style>
@keyframes bgShift {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}
.stApp {
  background: linear-gradient(-45deg,#0f172a,#020617,#1e293b,#020617);
  background-size: 400% 400%;
  animation: bgShift 18s ease infinite;
  color: #f9fafb;
}
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#020617,#020617);
}
.dashboard-card {
  background: linear-gradient(135deg,#020617,#020617);
  padding: 18px;
  border-radius: 18px;
  border: 1px solid #1f2937;
  box-shadow: 0 18px 45px rgba(0,0,0,0.6);
  transition: all 0.35s ease;
  margin-bottom: 18px;
}
.dashboard-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 30px 70px rgba(0,0,0,0.9);
}
.card-title {
  font-size: 20px;
  font-weight: 700;
}
.card-desc {
  color: #cbd5f5;
  font-size: 14px;
}
.slide-in {
  animation: slideIn 0.7s ease-in-out;
}
@keyframes slideIn {
  from {opacity:0; transform: translateX(50px);}
  to {opacity:1; transform: translateX(0);}
}
</style>
""", unsafe_allow_html=True)

# ================== TOP BANNER ==================
st.markdown(f"""
<div class="dashboard-card">
  <h2>🏥 AI-Powered Patient Readmission Dashboard</h2>
  <p><b>Built by:</b> Shouvik Sarkar (Self Project)</p>
  <p><b>Challenge:</b> IDC Resume Project Challenge |
     <b>Organisers:</b> Indian Data Club & Codebasics |
     <b>Sponsor:</b> Databricks</p>
  <p>🕒 Last Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>
</div>
""", unsafe_allow_html=True)

# ================== DATASET LOADER ==================
st.sidebar.header("📂 Dataset Control")
csv_files = [f for f in os.listdir() if f.endswith(".csv")]

if not csv_files:
    st.error("❌ No CSV files found")
    st.stop()

selected_file = st.sidebar.selectbox("Select CSV Dataset", csv_files)

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

with st.spinner("Loading dataset..."):
    df = load_data(selected_file)
    time.sleep(0.4)

numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ================== DATE FILTER ==================
st.sidebar.header("📅 Date Filter")
date_col = next((c for c in df.columns if "date" in c.lower()), None)
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    start, end = st.sidebar.date_input(
        "Select Date Range",
        [df[date_col].min(), df[date_col].max()]
    )
    df = df[(df[date_col] >= pd.to_datetime(start)) &
            (df[date_col] <= pd.to_datetime(end))]

# ================== DEPARTMENT FILTER ==================
dept_col = next((c for c in df.columns if "department" in c.lower() or "specialty" in c.lower()), None)
if dept_col:
    depts = st.sidebar.multiselect(
        "Select Department",
        df[dept_col].dropna().unique(),
        default=df[dept_col].dropna().unique()
    )
    df = df[df[dept_col].isin(depts)]

# ================== DASHBOARD MENU ==================
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
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Records", len(df))
    k2.metric("Departments", df[dept_col].nunique() if dept_col else "N/A")
    k3.metric("Numeric Metrics", len(numeric_cols))
    k4.metric("Avg Risk", round(df[numeric_cols[0]].mean(),2) if numeric_cols else "N/A")

    metric = st.selectbox("Select Metric", numeric_cols)
    fig = px.histogram(
        df, x=metric, nbins=40,
        color_discrete_sequence=["#38bdf8"]
    )
    fig.update_layout(transition_duration=700)
    st.plotly_chart(fig, use_container_width=True)

    # Department Load
    if dept_col:
        pid = next((c for c in df.columns if "patient" in c.lower()), None)
        if pid:
            dept_load = df.groupby(dept_col)[pid].count().reset_index(name="Patients")
            fig = px.bar(
                dept_load, x=dept_col, y="Patients",
                color=dept_col,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_layout(transition_duration=700)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== AI RISK DISTRIBUTION ==================
elif dashboard == "🤖 AI Risk Distribution":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    y = st.selectbox("Risk Metric", numeric_cols)
    x = st.selectbox("Segment By", cat_cols)

    tabs = st.tabs(["📊 Bar","📈 Histogram","📦 Box"])
    with tabs[0]:
        st.plotly_chart(px.bar(df,x=x,y=y,color=x,
            color_discrete_sequence=px.colors.qualitative.Set2),
            use_container_width=True)
    with tabs[1]:
        st.plotly_chart(px.histogram(df,x=y,color=x,
            color_discrete_sequence=px.colors.qualitative.Set2),
            use_container_width=True)
    with tabs[2]:
        st.plotly_chart(px.box(df,x=x,y=y,color=x,
            color_discrete_sequence=px.colors.qualitative.Set2),
            use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== RISK BY AGE ==================
elif dashboard == "👵 Risk by Age Group":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    age = st.selectbox("Age Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)
    st.plotly_chart(px.bar(df,x=age,y=risk,color=age,
        color_discrete_sequence=px.colors.qualitative.Pastel),
        use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== HOSPITAL UTILIZATION ==================
elif dashboard == "🏨 Hospital Utilization":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    x = st.selectbox("Risk Category", cat_cols)
    y = st.selectbox("Utilization Metric", numeric_cols)
    agg = st.radio("Aggregation",["mean","sum","count"],horizontal=True)
    df_agg = df.groupby(x)[y].agg(agg).reset_index()

    st.plotly_chart(px.bar(df_agg,x=x,y=y,color=x,
        color_discrete_sequence=px.colors.qualitative.Dark24),
        use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== DIABETES IMPACT ==================
elif dashboard == "🩺 Diabetes Impact":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    diab = st.selectbox("Disease Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)
    st.plotly_chart(px.bar(df,x=diab,y=risk,color=diab,
        color_discrete_sequence=px.colors.qualitative.Safe),
        use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== DATA TABLE ==================
elif dashboard == "📋 Data Table":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    rows = st.slider("Rows",10,300,50)
    st.dataframe(df.head(rows), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================== FOOTER ==================
st.divider()
st.markdown("""
<div class="dashboard-card">
<b>Project:</b> AI-Powered Patient Readmission Prediction<br>
<b>Built by:</b> Shouvik Sarkar<br>
<b>Context:</b> IDC Resume Project Challenge – Codebasics<br>
<b>Sponsor:</b> Databricks<br><br>
Databricks • Delta Lake • PySpark • MLflow • SQL • Streamlit
</div>
""", unsafe_allow_html=True)

st.caption("© 2026 Shouvik Sarkar | Healthcare AI | Databricks Ecosystem")
