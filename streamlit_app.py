import streamlit as st
from openai import OpenAI
import google.generativeai as genai
from utils.auth import ensure_authentication

# ==== Page Configuration ====
st.set_page_config(
    page_title="Home",
    page_icon="🤓",
    layout="wide"
)

# Removes automatic side bar

# ==== Sidebar ====
# Persona buttons
st.sidebar.title("Persona 🎭")

persona_options = {
    "Market Research": "pages/market_research_page.py", 
    "Conviction Score": "pages/conviction_score_page.py",
    "Reader File": "pages/reader_file_page.py"
}

st.sidebar.write("Choose a persona:")
for persona_label, persona_path in persona_options.items():
    if st.sidebar.button(persona_label, key=f"persona_btn_home_{persona_label.replace(' ', '_').lower()}"):
        st.switch_page(persona_path)

# ==== Main ====
# Check authentication first
ensure_authentication()

# Navigation only occurs on button click above



# Home page content (centered)
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.title("Hi! Welcome to Faye")
    st.write(
        "Your all-in-one internal market research tool, powered by Buntin Group"
        "\n\nThis is a work in progress. Find out how to get the GeminiAPI key [here](https://ai.google.dev/gemini-api/docs/api-key). "
        "\n\nNew to Faye? Find out how to use it below."
    )
    here = st.button("I'm new here!", key="here", use_container_width=True)
    if here:
        st.switch_page("pages/how_to.py")

    if st.button("🚪 Sign Out", key="logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.pop("username", None)
        st.session_state.pop("user_store", None)
        st.switch_page("pages/password_page.py")