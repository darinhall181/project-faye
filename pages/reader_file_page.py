import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Reader File",
    page_icon="📖",
    layout="wide"
)

# Navigation dropdown
st.sidebar.title("Navigation & History")

# Create navigation dropdown
page_options = {
    "🏠 Home": "streamlit_app.py",
    "🔍 Market Research": "pages/market_research_page.py", 
    "💡 Conviction Score": "pages/conviction_score_page.py",
    "📖 Reader File": "pages/reader_file_page.py"
}

selected_page = st.sidebar.selectbox(
    "Choose a page:",
    options=list(page_options.keys()),
    index=3  # Reader File is the 4th option (index 3)
)

# Navigate to selected page
if selected_page != "📖 Reader File":
    st.switch_page(page_options[selected_page])

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