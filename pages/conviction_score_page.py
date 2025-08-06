import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Conviction Score",
    page_icon="💡",
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
    index=2  # Conviction Score is the 3rd option (index 2)
)

# Navigate to selected page
if selected_page != "💡 Conviction Score":
    st.switch_page(page_options[selected_page])

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