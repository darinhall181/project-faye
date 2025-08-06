import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Market Research",
    page_icon="🔍",
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
    index=1  # Market Research is the 2nd option (index 1)
)

# Navigate to selected page
if selected_page != "🔍 Market Research":
    st.switch_page(page_options[selected_page])

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
