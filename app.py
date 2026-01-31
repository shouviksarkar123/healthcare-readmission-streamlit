import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Healthcare Readmission Dashboard Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== GLOBAL THEME & ANIMATION ==================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0b132b, #1c2541);
    color: #f9fafb;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1f2933);
}
.dashboard-card {
    background: linear-gradient(135deg, #1f2933, #111827);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #374151;
    box-shadow: 0 12px 28px rgba(0,0,0,0.45);
    transition: all 0.3s ease;
    margin-bottom: 18px;
}
.dashboard-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 45px rgba(0,0,0,0.65);
}
.card-title {
    font-size: 20px;
    font-weight: 700;
    color: #f9fafb;
}
.card-desc {
    color: #d1d5db;
    font-size: 14px;
}
.slide-in {
    animation: slideIn 0.6s ease-in-out;
}
@keyframes slideIn {
    from {opacity:0; transform: translateX(40px);}
    to {opacity:1; transform: translateX(0);}
}
</style>
""", unsafe_allow_html=True)

# ================== TOP PROJECT BANNER ==================
st.markdown(f"""
<div class="dashboard-card">
    <h2>🏥 Healthcare Readmission Dashboard Analysis</h2>
    <p><b>Built by:</b> Shouvik Sarkar (Self Project)</p>
    <p>
    <b>Challenge:</b> IDC Resume Project Challenge |
    <b>Organisers:</b> Indian Data Club & Codebasics |
    <b>Sponsor:</b> Databricks
    </p>
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

st.success(f"Dataset loaded: {selected_file}")

numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

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

# ================== SECTION PREVIEW CARDS ==================
st.subheader("📌 Analytics Modules")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">🧑‍💼 Executive Overview</div>
        <div class="card-desc">Leadership KPIs & summary insights</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">🤖 AI Risk Distribution</div>
        <div class="card-desc">Readmission risk by patient segment</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">🏨 Hospital Utilization</div>
        <div class="card-desc">Operational & capacity analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ================== EXECUTIVE OVERVIEW ==================
if dashboard == "🧑‍💼 Executive Overview":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    st.subheader("📌 Executive Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Records", len(df))
    k2.metric("Numeric Metrics", len(numeric_cols))
    k3.metric("Categorical Features", len(cat_cols))
    k4.metric("Primary Avg", round(df[numeric_cols[0]].mean(), 2) if numeric_cols else "N/A")

    metric = st.selectbox("Select Metric", numeric_cols)
    fig = px.histogram(
        df, x=metric, nbins=40,
        color_discrete_sequence=["#4CC9F0"]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 High-level snapshot for hospital leadership & decision makers")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== AI RISK DISTRIBUTION ==================
elif dashboard == "🤖 AI Risk Distribution":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    y = st.selectbox("Risk Metric", numeric_cols)
    x = st.selectbox("Segment By", cat_cols)

    tab1, tab2, tab3 = st.tabs(["📊 Bar", "📈 Histogram", "📦 Box"])

    with tab1:
        st.plotly_chart(px.bar(df, x=x, y=y, color=x,
                               color_discrete_sequence=px.colors.qualitative.Set2),
                        use_container_width=True)
    with tab2:
        st.plotly_chart(px.histogram(df, x=y, color=x,
                                     color_discrete_sequence=px.colors.qualitative.Set2),
                        use_container_width=True)
    with tab3:
        st.plotly_chart(px.box(df, x=x, y=y, color=x,
                               color_discrete_sequence=px.colors.qualitative.Set2),
                        use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== RISK BY AGE ==================
elif dashboard == "👵 Risk by Age Group":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    age = st.selectbox("Age Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)

    st.plotly_chart(px.bar(df, x=age, y=risk, color=age,
                           color_discrete_sequence=px.colors.qualitative.Pastel),
                    use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================== HOSPITAL UTILIZATION ==================
elif dashboard == "🏨 Hospital Utilization":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    x = st.selectbox("Risk Category", cat_cols)
    y = st.selectbox("Utilization Metric", numeric_cols)
    agg = st.radio("Aggregation", ["mean", "sum", "count"], horizontal=True)

    df_agg = df.groupby(x)[y].agg(agg).reset_index()

    st.plotly_chart(px.bar(df_agg, x=x, y=y, color=x,
                           color_discrete_sequence=px.colors.qualitative.Dark24),
                    use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================== DIABETES IMPACT ==================
elif dashboard == "🩺 Diabetes Impact":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)

    diab = st.selectbox("Disease / Diabetes Column", cat_cols)
    risk = st.selectbox("Risk Metric", numeric_cols)

    st.plotly_chart(px.bar(df, x=diab, y=risk, color=diab,
                           color_discrete_sequence=px.colors.qualitative.Safe),
                    use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================== DATA TABLE ==================
elif dashboard == "📋 Data Table":
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    rows = st.slider("Rows to display", 10, 300, 50)
    st.dataframe(df.head(rows), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================== FOOTER ==================
st.divider()
st.markdown("""
<div class="dashboard-card">
<b>Project:</b> Healthcare Readmission Dashboard Analysis<br>
<b>Built by:</b> Shouvik Sarkar (Self Project)<br>
<b>Context:</b> IDC Resume Project Challenge – Codebasics<br>
<b>Sponsor:</b> Databricks<br><br>
Databricks • Delta Lake • PySpark • MLflow • SQL • Streamlit
</div>
""", unsafe_allow_html=True)

st.caption("© 2026 Shouvik Sarkar | Healthcare AI | Databricks Ecosystem")
