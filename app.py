import streamlit as st
import requests

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(page_title="AI Data Analyst Copilot", layout="wide")

st.title("AI Data Analyst Copilot")

# ===================================
# SESSION STATE (Retention System)
# ===================================

if "history" not in st.session_state:
    st.session_state.history = []

if "example" not in st.session_state:
    st.session_state.example = ""

# ===================================
# SIDEBAR (Recent Results)
# ===================================

st.sidebar.title("Recent Results")

for item in reversed(st.session_state.history[-5:]):
    st.sidebar.code(item)

# ===================================
# MODE SELECTOR (Professional UX)
# ===================================

mode = st.selectbox(
    "Choose Mode:",
    ["SQL Generator", "Excel Formula", "Data Insight"]
)

# ===================================
# DISCOVERY MAGNET (Example Templates)
# ===================================

st.markdown("### Try Example Tasks")

example1 = "Create SQL query to find top 10 customers by revenue"
example2 = "Excel formula to calculate percentage growth"
example3 = "Explain sales dataset trends for last quarter"

col1, col2, col3 = st.columns(3)

if col1.button("SQL Example"):
    st.session_state.example = example1

if col2.button("Excel Example"):
    st.session_state.example = example2

if col3.button("Insight Example"):
    st.session_state.example = example3

# ===================================
# USER INPUT
# ===================================

user_input = st.text_area(
    "Describe your task:",
    value=st.session_state.example
)

# ===================================
# GENERATE BUTTON
# ===================================

if st.button("Generate"):

    if user_input.strip() == "":
        st.warning("Please enter a request.")

    else:

        # 🔥 Replace with your real Grok API key
        api_key = "YOUR_GROK_API_KEY"

        # Prompt engineering based on mode
        if mode == "SQL Generator":
            prompt = f"You are expert SQL developer. Convert this into optimized SQL query:\n{user_input}"

        elif mode == "Excel Formula":
            prompt = f"You are Excel expert. Generate correct Excel formula with explanation:\n{user_input}"

        else:
            prompt = f"You are senior data analyst. Provide clear data insights and explanation:\n{user_input}"

        # 🔥 Replace with real Grok API endpoint
        url = "GROK_API_ENDPOINT"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "prompt": prompt
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            # Convert result safely to string
            output_text = str(result)

            # ===================================
            # DISPLAY RESULT (Growth Feature)
            # ===================================

            st.subheader("AI Output")

            st.code(output_text)

            # Save history (Retention feature)
            st.session_state.history.append(output_text)

            # ===================================
            # COPY & SHARE (Viral Growth Feature)
            # ===================================

            st.markdown("### Copy & Share")

            st.text_area(
                "Quick Copy Box:",
                value=output_text,
                height=150
            )

            share_text = f"""
I just generated this using AI Data Analyst Copilot:

{output_text}

Try it here: YOUR_APP_LINK
"""

            st.text_area(
                "Share this on LinkedIn / X / Reddit:",
                value=share_text,
                height=200
            )

        except Exception as e:
            st.error(f"Error: {e}")
