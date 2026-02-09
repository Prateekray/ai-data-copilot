import streamlit as st
import requests
import time

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(
    page_title="AI Data Analyst Workspace",
    layout="wide"
)

# ===================================
# SESSION STATE DEFAULTS
# ===================================

if "skill_level" not in st.session_state:
    st.session_state.skill_level = "Beginner"

if "database_type" not in st.session_state:
    st.session_state.database_type = "PostgreSQL"

# ===================================
# HEADER
# ===================================

st.title("💎 AI Data Analyst Workspace")

st.success("SQL • Excel • Data Insights | Live AI Tool")

# ===================================
# GLOBAL SETTINGS (Skill level only)
# ===================================

st.session_state.skill_level = st.selectbox(
    "Skill Level",
    ["Beginner","Intermediate","Advanced"],
    index=["Beginner","Intermediate","Advanced"].index(
        st.session_state.skill_level
    )
)

# ===================================
# API CALL FUNCTION
# ===================================

def call_ai(prompt):

    api_key = st.secrets["GROK_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    url = "GROK_API_ENDPOINT"

    response = requests.post(url, headers=headers, json={"prompt": prompt})

    return str(response.json())

# ===================================
# STREAM OUTPUT
# ===================================

def stream_output(text):

    placeholder = st.empty()
    streamed = ""

    for char in text:
        streamed += char
        placeholder.markdown(streamed)
        time.sleep(0.001)

# ===================================
# TABS
# ===================================

tab_sql, tab_excel, tab_insight = st.tabs([
    "🧠 SQL Generator",
    "📊 Excel Formula Builder",
    "📈 Data Insight Explainer"
])

# ===================================
# SQL GENERATOR TAB
# ===================================

with tab_sql:

    st.subheader("SQL Generator")

    # Database selector ONLY here
    st.session_state.database_type = st.selectbox(
        "Database Type",
        ["PostgreSQL","MySQL","SQL Server","SQLite"],
        index=["PostgreSQL","MySQL","SQL Server","SQLite"].index(
            st.session_state.database_type
        )
    )

    table = st.text_input("Table Name")
    columns = st.text_input("Columns")
    goal = st.text_area("Goal")
    filters = st.text_input("Filters")

    if st.button("🚀 Generate SQL"):

        prompt = f"""
SQL Expert AI.

Skill level: {st.session_state.skill_level}
Database: {st.session_state.database_type}

Table: {table}
Columns: {columns}
Goal: {goal}
Filters: {filters}

Provide:
SQL Query
Explanation
Optimization Tips
"""

        result = call_ai(prompt)
        stream_output(result)

# ===================================
# EXCEL FORMULA TAB
# ===================================

with tab_excel:

    st.subheader("Excel Formula Builder")

    excel_task = st.text_area("Describe Excel task")

    if st.button("🚀 Generate Excel Formula"):

        prompt = f"""
Excel Expert AI.

Skill level: {st.session_state.skill_level}

Task:
{excel_task}

Provide:
Formula
Explanation
Tips
"""

        result = call_ai(prompt)
        stream_output(result)

# ===================================
# DATA INSIGHT TAB
# ===================================

with tab_insight:

    st.subheader("Data Insight Explainer")

    insight_task = st.text_area("Describe data scenario")

    if st.button("🚀 Generate Insights"):

        prompt = f"""
Data Analyst AI.

Skill level: {st.session_state.skill_level}

Scenario:
{insight_task}

Provide:
Insights
Analysis
Recommendations
"""

        result = call_ai(prompt)
        stream_output(result)
