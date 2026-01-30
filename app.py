import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Powered Patient Readmission Dashboard",
    layout="wide"
)

st.title("🏥 AI-Powered Patient Readmission Dashboard")
st.caption("Predicting 30-day hospital readmission risk using AI")

# ---------------- DATA FOLDER ----------------
DATA_DIR = Path(".")

csv_files = sorted([f.name for f in DATA_DIR.glob("*.csv")])

if not csv_files:
    st.error("❌ No CSV files found in project directory")
    st.stop()

# ---------------- SIDEBAR ----------------
selected_file = st.sidebar.selectbox(
    "📁 Select Dataset",
    csv_files
)

file_path = DATA_DIR / selected_file

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv(file_path)
    st.success(f"Loaded: {selected_file}")
except Exception as e:
    st.error("CSV load failed")
    st.stop()

with st.expander("🔍 Show Columns"):
    st.write(df.columns.tolist())
    st.dataframe(df.head())

st.divider()

# ---------------- COLOR PALETTE ----------------
COLORS = px.colors.qualitative.Set2

# ---------------- ACTUAL vs AI RISK ----------------
if "actual" in selected_file.lower() and "ai" in selected_file.lower():

    actual_col = None
    ai_col = None
    x_col = df.columns[0]

    for col in df.columns:
        c = col.lower()
        if "actual" in c:
            actual_col = col
        if "ai" in c or "pred" in c:
            ai_col = col

    if actual_col and ai_col:
        fig = px.bar(
            df,
            x=x_col,
            y=[actual_col, ai_col],
            barmode="group",
            color_discrete_sequence=COLORS,
            title="Actual vs AI Predicted Readmission Risk"
        )

        fig.update_layout(
            xaxis_title="Risk Category",
            yaxis_title="Patient Count",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title="Metric"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("❌ Could not detect Actual / AI columns automatically")

# ---------------- GENERIC DASHBOARD ----------------
else:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        x = df.columns[0]
        y = numeric_cols[-1]

        fig = px.bar(
            df,
            x=x,
            y=y,
            color=x,
            color_discrete_sequence=COLORS,
            title=selected_file.replace(".csv", "")
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )

        fig.update_traces(
            texttemplate="%{y}",
            textposition="outside"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric columns available")

st.success("✅ Dashboard rendered successfully")
