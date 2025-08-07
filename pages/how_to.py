import streamlit as st

st.set_page_config(
    page_title="How to Use Faye",
    page_icon="🤨",
    layout="wide"
)

# Home page button
if st.button("🏠 Back to Home", key="how_to_home"):
    st.switch_page("streamlit_app.py")

st.title("How to Use Faye")

st.write("This is the how to use this website!")
st.write("What is Faye?")
st.write("Personas")
st.write("Market Research 🔍")
st.write("Conviction Score 💡")
st.write("Reader File 📖")
