import streamlit as st
import pandas as pd
import json
from src.classification import classify_reviews
from src.intelligence import generate_all_intelligence


st.set_page_config(
    page_title="AI Operations Intelligence",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Operations Intelligence")

st.write(
    "Transform AppFolio customer feedback into operational intelligence."
)

st.sidebar.header("Navigation")

uploaded_file = st.file_uploader(
    "Upload AppFolio review CSV",
    type=["csv"]
)


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully!")

    classified_df = classify_reviews(df)
    
    # ---------- KPI ----------
    st.subheader("Executive Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Reviews", len(classified_df))
    col2.metric("Issue Categories",
                classified_df["issue_category"].nunique())
    col3.metric("Negative Reviews",
                len(classified_df[classified_df["score"] <= 2]))
    
    # ---------- Issue Distribution ----------
    issue_summary = (
        classified_df["issue_category"]
        .value_counts()
        .reset_index()
    )
    
    issue_summary.columns = ["Issue Category", "Reviews"]
    
    st.bar_chart(issue_summary.set_index("Issue Category"))
    
    # ---------- AI Intelligence ----------
    raw_intelligence = generate_all_intelligence(classified_df)
    intelligence = [json.loads(item) for item in raw_intelligence]
    
    st.subheader("AI Operational Intelligence")
    
    for item in intelligence:

        with st.container():
    
            highest_priority = item["themes"][0]["priority"]
    
            if highest_priority == "High":
                st.error(f"🔴 {item['issue_category']}")
            elif highest_priority == "Medium":
                st.warning(f"🟠 {item['issue_category']}")
            else:
                st.success(f"🟢 {item['issue_category']}")
    
            for theme in item["themes"]:
    
                st.write(f"### {theme['theme']}")
                st.write(f"**Frequency:** {theme['frequency']}")
                st.write(f"**Root Cause:** {theme['root_cause']}")
                st.write(f"**Business Impact:** {theme['business_impact']}")
                st.write(f"**Recommendation:** {theme['recommendation']}")
                st.write(f"**Priority:** {theme['priority']}")
    
                st.divider()