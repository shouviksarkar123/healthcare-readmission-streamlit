import streamlit as st
import pandas as pd
import plotly.express as px
import os, time
from datetime import datetime

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== GLOBAL THEME + DESIGN ==================
st.markdown("""
<style>
@keyframes bgShift {
  0% {background-position:0% 50%;}
  50% {background-position:100% 50%;}
  100% {background-position:0% 50%;}
}
.stApp {
  background: linear-gradient(-45deg,#020617,#0f172a,#020617,#1e293b);
  background-size: 400% 400%;
  animation: bgShift 20s ease infinite;
  color: #f8fafc;
}
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#020617,#020617);
}

/* CARD */
.card {
  background: rgba(15,23,42,0.75);
  backdrop-filter: blur(14px);
  border-radius: 18px;
  padding: 18px;
  border: 1px solid rgba(148,163,184,0.15);
  box-shadow: 0 18px 45px rgba(0,0,0,0.55);
  transition: all .35s ease;
  margin-bottom: 18px;
}
.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 28px 65px rgba(0,0,0,0.85);
}

/* KPI */
.kpi {
  text-align: center;
  padding: 20px;
  border-radius: 16px;
  background: linear-gradient(135deg,#1e293b,#020617);
  border: 1px solid rgba(148,163,184,0.18);
}
.kpi h3 {
  margin: 0;
  color: #38bdf8;
}
.kpi p {
  margin: 0;
  font-size: 14px;
  color: #cbd5f5;
}

/* SECTION ANIMATION */
.slide {
  animation: slideIn .7s ease-in-out;
}
@keyframes slideIn {
  from {opacity:0; transform:translateX(40px);}
  to {opacity:1; transform:translateX(0);}
}
</style>
""", unsafe_allow_html=True)

# ================== TOP HEADER ==================
st.markdown(f"""
<div class="card">
  <h2>🏥 AI-Powered Patient Readmission Dashboard</h2>
  <p><b>Built by:</b> Shouvik Sarkar (Self Project)</p>
  <p><b>Challenge:</b> IDC Resume Project Challenge |
     <b>Organisers:</b> Indian Data Club & Codebasics |
     <b>Sponsor:</b> Databricks</p>
  <p>🕒 Last Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>
</div>
""", unsafe_allow_html=True)

# ================== DATASET ==================
st.sidebar.header("📂 Dataset Control")
csv_files = [f for f in os.listdir() if f.endswith(".csv")]
selected_file = st.sidebar.selectbox("Select CSV Dataset", csv_files)

@st.cache_data
def load_data(f): return pd.read_csv(f)

with st.spinner("Loading dataset..."):
    df = load_data(selected_file)
    time.sleep(.3)

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ================== FILTERS ==================
date_col = next((c for c in df.columns if "date" in c.lower()), None)
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    s,e = st.sidebar.date_input("📅 Date Range",[df[date_col].min(),df[date_col].max()])
    df = df[(df[date_col]>=pd.to_datetime(s))&(df[date_col]<=pd.to_datetime(e))]

dept_col = next((c for c in df.columns if "department" in c.lower() or "specialty" in c.lower()), None)
if dept_col:
    depts = st.sidebar.multiselect("🏥 Department", df[dept_col].unique(), default=df[dept_col].unique())
    df = df[df[dept_col].isin(depts)]

# ================== MENU ==================
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
    st.markdown('<div class="slide">', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f"<div class='kpi'><h3>{len(df)}</h3><p>Total Records</p></div>",unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'><h3>{df[dept_col].nunique() if dept_col else 'N/A'}</h3><p>Departments</p></div>",unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'><h3>{len(num_cols)}</h3><p>Numeric Metrics</p></div>",unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi'><h3>{round(df[num_cols[0]].mean(),2) if num_cols else 'N/A'}</h3><p>Avg Risk</p></div>",unsafe_allow_html=True)

    metric = st.selectbox("Select Metric", num_cols)
    fig = px.histogram(df, x=metric, nbins=40, template="plotly_dark")
    fig.update_layout(transition_duration=700)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== AI RISK ==================
elif dashboard == "🤖 AI Risk Distribution":
    st.markdown('<div class="slide">', unsafe_allow_html=True)

    y = st.selectbox("Risk Metric", num_cols)
    x = st.selectbox("Segment By", cat_cols)

    tabs = st.tabs(["📊 Bar","📈 Histogram","📦 Box"])
    for t,chart in zip(tabs,["bar","hist","box"]):
        with t:
            fig = getattr(px,chart)(df,x=x if chart!="hist" else None,y=y if chart!="hist" else y,
                                    color=x,template="plotly_dark")
            fig.update_layout(transition_duration=700)
            st.markdown("<div class='card'>",unsafe_allow_html=True)
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== AGE ==================
elif dashboard == "👵 Risk by Age Group":
    fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0], template="plotly_dark")
    st.markdown("<div class='card slide'>",unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ================== UTILIZATION ==================
elif dashboard == "🏨 Hospital Utilization":
    x = st.selectbox("Risk Category", cat_cols)
    y = st.selectbox("Metric", num_cols)
    df_agg = df.groupby(x)[y].mean().reset_index()
    fig = px.bar(df_agg,x=x,y=y,color=x,template="plotly_dark")
    st.markdown("<div class='card slide'>",unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ================== DIABETES ==================
elif dashboard == "🩺 Diabetes Impact":
    fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0], template="plotly_dark")
    st.markdown("<div class='card slide'>",unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ================== TABLE ==================
elif dashboard == "📋 Data Table":
    st.markdown("<div class='card slide'>",unsafe_allow_html=True)
    st.dataframe(df,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ================== FOOTER ==================
st.markdown("""
<div class="card">
<b>Project:</b> AI-Powered Patient Readmission Prediction<br>
<b>Built by:</b> Shouvik Sarkar<br>
<b>Context:</b> IDC Resume Project Challenge – Codebasics<br>
<b>Sponsor:</b> Databricks<br><br>
Databricks • Delta Lake • PySpark • MLflow • SQL • Streamlit
</div>
""", unsafe_allow_html=True)

st.caption("© 2026 Shouvik Sarkar | Healthcare AI | Databricks Ecosystem")
