import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Reader File",
    page_icon="📖",
    layout="wide"
)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/password_page.py")


# Custom persona dropdown
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
    index=3  # Reader File is the 4th option (index 3)
)

# Navigate to selected page only if a valid option is selected and it's different from current page
if selected_page != "None" and selected_page != "Reader File" and persona_options[selected_page] is not None:
    st.switch_page(persona_options[selected_page])

# Home button
if st.button("🏠 Back to Home", key="reader_home"):
    st.switch_page("streamlit_app.py")

st.title("Reader File 📖")
st.write("This is the Reader File page. You can add your file reading functionality here.")

# Example reader file functionality
st.header("Document Reader")
st.write("Upload and read documents with enhanced analysis capabilities.")

uploaded_file = st.file_uploader(
    "Upload documents to read (.txt or .md)", 
    type=("txt", "md"),
    key="reader_uploader"
)

if uploaded_file:
    st.success("Document uploaded successfully!")
    st.write("Add your document reading analysis here.")