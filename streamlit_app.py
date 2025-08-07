import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Home",
    page_icon="🤓",
    layout="wide"
)

# ==== Sidebar ====
# Persona dropdown
st.sidebar.title("Persona 🤖")

# Create persona dropdown 
persona_options = {
    "None": None,
    "Market Research": "pages/market_research_page.py", 
    "Conviction Score": "pages/conviction_score_page.py",
    "Reader File": "pages/reader_file_page.py"
}

selected_page = st.sidebar.selectbox(
    "Choose a persona:",
    options=list(persona_options.keys()),
    index=0
)

# ==== Main ====
# Check authentication first
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/password_page.py")

# Navigate to selected page only if a valid option is selected
if selected_page != "None" and persona_options[selected_page] is not None:
    st.switch_page(persona_options[selected_page])


# Home page content
st.title("Hi! Welcome to Faye 🤓")
st.write(
    "Your all-in-one internal market research tool, powered by Buntin Group"
    "\n\nThis is a work in progress. Find out how to get the GeminiAPI key [here](https://ai.google.dev/gemini-api/docs/api-key). "
    "\n\nNew to Faye? Find out how to use it below."
)
here = st.button("HERE", key="here")
if here:
    st.switch_page("pages/how_to.py")

if st.button("🚪 Sign Out", key="logout"):
    st.session_state.authenticated = False
    st.switch_page("pages/password_page.py")