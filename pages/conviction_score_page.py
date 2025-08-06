import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Conviction Score",
    page_icon="💡",
    layout="wide"
)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/password_page.py")

# Persona dropdown
st.sidebar.title("Persona")

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
    index=2  # Conviction Score is the 3rd option (index 2)
)

# Navigate to selected page only if a valid option is selected and it's different from current page
if selected_page != "None" and selected_page != "Conviction Score" and persona_options[selected_page] is not None:
    st.switch_page(persona_options[selected_page])

# Home button
if st.button("🏠 Back to Home", key="conviction_home"):
    st.switch_page("streamlit_app.py")

st.title("Conviction Score 💡")
st.write("This is the Conviction Score page. You can add your conviction scoring functionality here.")

# Example conviction score functionality
st.header("Investment Conviction Analysis")
st.write("Upload documents to analyze investment conviction and risk factors.")

uploaded_file = st.file_uploader(
    "Upload investment documents (.txt or .md)", 
    type=("txt", "md"),
    key="conviction_uploader"
)

if uploaded_file:
    st.success("Document uploaded successfully!")
    st.write("Add your conviction score analysis here.")