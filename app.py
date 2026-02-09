import streamlit as st
import requests

# Page Title
st.title("AI Data Analyst Copilot")

# User Input
user_input = st.text_area(
    "Describe what you want (SQL query / Excel formula / Data insight):"
)

# Button
if st.button("Generate"):

    if user_input.strip() == "":
        st.warning("Please enter a request.")
    else:

        # 🔥 Replace with your real Grok API key later
        api_key = "YOUR_GROK_API_KEY"

        # Prompt Engineering (IMPORTANT)
        prompt = f"""
        You are a senior data analyst.

        Convert the following request into:

        1. SQL query if applicable
        2. Excel formula if applicable
        3. Clear data analysis explanation

        Request:
        {user_input}
        """

        # 🔥 Replace endpoint according to Grok API docs
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

            st.subheader("AI Output:")
            st.write(result)

        except Exception as e:
            st.error(f"Error: {e}")
