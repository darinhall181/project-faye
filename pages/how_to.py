import streamlit as st
from utils.auth import ensure_authentication

st.set_page_config(
    page_title="How to Use Faye",
    page_icon="🤨",
    layout="wide"
)

# Enforce auth
ensure_authentication()

# Navigation Button
if st.button("🏠 Back to Home", key="how_to_home"):
    st.switch_page("streamlit_app.py")

# Main Title
st.title("How to Use Faye")
st.markdown("---")

# General Overview
st.header("📌 What is Faye?")
st.write("""
Faye is Buntin's in-house AI research assistant, designed to help you move faster and smarter on strategy and creative planning. 
Powered by Google's Gemini and trained with decades of Buntin insights, Faye blends real-time web search with our proprietary intelligence.
Use it to upload documents, research new categories, or get a quick pulse check through our Conviction Score tool.
""")

# Key Features
st.header("🧰 What Can Faye Do?")
st.subheader("📄 Upload Documents")
st.write("""
Have a pitch deck, brief, or research file? Upload it! Faye will read the content and use it to guide its responses to your prompts.
This means smarter, more specific answers based on what you've already got. All files stay within your session — nothing is uploaded online.
""")

st.subheader("🔍 Deep Web Search")
st.write("""
Need a quick download on a new brand or topic? Faye can search trusted online sources and summarize what's relevant.
It's built to behave like a Buntin strategist — sourcing the right sites and asking the right follow-up questions.
""")

st.subheader("💡 Conviction Score")
st.write("""
This is our unique way of measuring a brand's strength. Based on the Four Buntin Pillars — Practical, Emotional, Personal, and Causal —
Faye will analyze your input and return a score with reasoning, helping you make fast, insightful brand assessments.
""")

st.subheader("📊 Market Research Reports")
st.write("""
Kick off your next pitch or project with a custom research report. Faye can generate overviews of industries, products, or brands,
including key competitors and category trends. Export the output as a Word doc, PDF, or LaTeX file for further editing.
""")

# Helpful Reminders
st.header("ℹ️ Tips for Getting the Most Out of Faye")
st.markdown("""
- Be specific! The more detail you give Faye in your prompt, the better it performs.
- Upload documents early. If you're working from a deck or brief, upload it first before asking questions.
- Use it as a conversation. Faye can follow up, ask questions back, and evolve its answers based on your inputs.
""")

# Contact Info
st.markdown("---")
st.markdown("If you run into any issues or have questions, please reach out to your administrator.")

