import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Market Research",
    page_icon="🔍",
    layout="wide"
)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/password_page.py")

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
    index=1  # Market Research is the 2nd option (index 1)
)

# Navigate to selected page only if a valid option is selected and it's different from current page
if selected_page != "None" and selected_page != "Market Research" and persona_options[selected_page] is not None:
    st.switch_page(persona_options[selected_page])

# Home button
if st.button("🏠 Back to Home", key="market_home"):
    st.switch_page("streamlit_app.py")

st.title("Market Research 🔍")
st.write("This is the Market Research page. You can add your market research functionality here.")

# Example market research functionality
st.header("Competitor Analysis")
st.write("Upload documents to analyze competitors and market trends.")

uploaded_file = st.file_uploader(
    "Upload market research documents (.txt or .md)", 
    type=("txt", "md"),
    key="market_research_uploader"
)

if uploaded_file:
    st.success("Document uploaded successfully!")
    st.write("Add your market research analysis here.")
