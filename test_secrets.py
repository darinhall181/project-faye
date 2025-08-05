import streamlit as st
import os

st.write("Working directory:", os.getcwd())
st.write("Loaded secrets:", st.secrets)

try:
    st.write("API Key:", st.secrets["openai"]["privateKey"])
except Exception as e:
    st.error(f"Couldn't load API key: {e}")
