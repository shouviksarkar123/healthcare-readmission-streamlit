import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide"
)

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Predicting 30-day hospital readmission risk using AI")

# -----------------------
# Load CSV (auto)
# -----------------------
csv_files = [f for f in st.session_state.get("uploaded_files", [])]

try:
    # fallback: load first CSV in repo
    df = pd.read_csv(next(iter(st.session_state.get("csv_path", [])), None))
except:
    # manual fallback (repo file)
    import os
    files = [f for f in os.listdir() if f.endswith(".csv")]
    if not files:
        st.error("❌ No CSV file found in repository")
        st.stop()
    df = pd.read_csv(files[0])

st.success("CSV loaded successfully")

# -----------------------
# Show columns
# -----------------------
with st.expander("🔍 Show Columns"):
    st.write(list(df.columns))

# -----------------------
# Helper: numeric columns only
# -----------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    st.error("❌ No numeric columns found. Cannot build charts.")
    st.stop()

# -----------------------
# Sidebar: Dashboard selector
# -----------------------
st.sidebar.header("📊 Select Dashboard")

dashboard = st.sidebar.selectbox(
    "Dashboard View",
    [
        "Overall Metric",
        "Bar Chart",
        "Histogram",
        "Table View"
    ]
)

# -----------------------
# Dashboard: Overall Metric
# -----------------------
if dashboard == "Overall Metric":
    col = numeric_cols[0]
    st.metric(
        label=f"Metric: {col}",
        value=round(df[col].sum(), 2)
    )

# -----------------------
# Dashboard: Bar Chart
# -----------------------
elif dashboard == "Bar Chart":
    x_col = st.sidebar.selectbox("X Axis", df.columns)
    y_col = st.sidebar.selectbox("Y Axis", numeric_cols)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} by {x_col}"
    )

    st.plotly_chart(fig, use_container_width=True, key="bar_chart")

# -----------------------
# Dashboard: Histogram
# -----------------------
elif dashboard == "Histogram":
    col = st.sidebar.selectbox("Numeric Column", numeric_cols)

    fig = px.histogram(
        df,
        x=col,
        title=f"Distribution of {col}"
    )

    st.plotly_chart(fig, use_container_width=True, key="hist_chart")

# -----------------------
# Dashboard: Table
# -----------------------
elif dashboard == "Table View":
    st.dataframe(df)

st.success("✅ Dashboard rendered successfully")
