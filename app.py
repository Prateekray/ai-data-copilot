import streamlit as st
import requests

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
# GLOBAL SETTINGS
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

    url = "https://api.groq.com/openai/v1/chat/completions"

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    if "choices" not in result:
        return f"API ERROR:\n{result}"

    return result["choices"][0]["message"]["content"]

# ===================================
# SMART RESPONSE RENDERER
# ===================================

def render_response(response):

    # Remove markdown code fences
    response = response.replace("```sql", "").replace("```", "")

    lines = response.split("\n")

    sql_lines = []
    other_lines = []

    sql_started = False

    stop_words = ("Explanation", "Optimization", "Tips", "Example")

    for line in lines:

        # Detect start of SQL
        if line.strip().upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "WITH")):
            sql_started = True

        # Detect end of SQL
        if any(word in line for word in stop_words):
            sql_started = False

        if sql_started:
            sql_lines.append(line)
        else:
            other_lines.append(line)

    sql_text = "\n".join(sql_lines).strip()
    rest_text = "\n".join(other_lines).strip()

    # Clean AI headings automatically
    rest_text = (
        rest_text
        .replace("SQL Query:", "")
        .replace("Explanation:", "")
        .replace("## SQL Query", "")
        .replace("### SQL Query", "")
        .strip()
    )

    if sql_text:
        st.subheader("🧠 SQL Query")
        st.code(sql_text, language="sql")

        st.subheader("📘 Explanation & Optimization")
        st.markdown(rest_text)
    else:
        st.markdown(response)

# ===================================
# SQL TAB
# ===================================

with tab_sql:

    st.subheader("SQL Generator")

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
        render_response(result)

# ===================================
# EXCEL TAB
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
        render_response(result)

# ===================================
# INSIGHT TAB
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
        render_response(result)
