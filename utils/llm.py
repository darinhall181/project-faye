import streamlit as st
from openai import OpenAI

'''
File Information:

Handles API calls, client setups, and error handling
'''

api_key = st.secrets["OpenAI"]["privateKey"]

