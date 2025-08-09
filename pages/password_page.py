"""
Login page for Faye.

How it works
------------
- This page renders the login form and verifies credentials by calling
  utils.auth.authenticate(), which checks values in st.secrets.
- On success, it sets st.session_state["authenticated"] = True and
  st.session_state["username"], then loads the user’s persisted store
  into st.session_state["user_store"].
- Other pages protect access by calling utils.auth.ensure_authentication()
  so unauthenticated users are redirected here.
"""

import streamlit as st
from streamlit.runtime.secrets import StreamlitSecretNotFoundError
from utils.auth import authenticate
from utils.user_store import load_user_store

# Page configuration
st.set_page_config(
    page_title="Sign In",
    page_icon="🔐",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Main authentication logic
if not st.session_state.authenticated:
    
    # Create a centered container for the password form
    col1, col2, col3 = st.columns([1, 2, 1])
   
    with col2:
        st.title("Please sign in below") 


    with col2:
        st.markdown("---")
        
        # Username input
        username = st.text_input(
            "Username:",
            placeholder="Enter username",
            value="",
            key="login_username"
        )

        # Password input
        password = st.text_input(
            "Enter your password:",
            type="password",
            placeholder="Enter password here..."
        )
        
        # Submit button
        if st.button("Sign In", type="secondary", use_container_width=True):
            try:
                if authenticate(username.strip(), password):
                    st.session_state.authenticated = True
                    st.session_state.username = username.strip()
                    # Load user store into session
                    st.session_state.user_store = load_user_store(st.session_state.username)
                    st.success("Authentication successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Incorrect credentials. Please try again.")
            except StreamlitSecretNotFoundError:
                st.error("No secrets configured. Add a .streamlit/secrets.toml or set secrets in your deploy environment.")
                st.info("Required keys: CORRECT_USERNAME, CORRECT_PASSWORD, GEMINI_APIKEY")
        
        st.markdown("---")
        
        # Add some helpful text
        st.info("💡 Contact your administrator if you need access credentials.")
        
else:
    # User is authenticated, redirect to main app
    st.switch_page("streamlit_app.py") 