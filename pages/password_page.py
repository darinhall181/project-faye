import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Sign In",
    page_icon="🔐",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Define the correct password (you can change this)
CORRECT_PASSWORD = "faye2024"

# Main authentication logic
if not st.session_state.authenticated:
    st.title("Please sign in 🔐")
    
    # Create a centered container for the password form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        # Password input
        password = st.text_input(
            "Enter your password:",
            type="password",
            placeholder="Enter password here..."
        )
        
        # Submit button
        if st.button("Sign In", type="primary", use_container_width=True):
            if password == CORRECT_PASSWORD:
                st.session_state.authenticated = True
                st.success("Authentication successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
        
        st.markdown("---")
        
        # Add some helpful text
        st.info("💡 Contact your administrator if you need access credentials.")
        
else:
    # User is authenticated, redirect to main app
    st.switch_page("streamlit_app.py") 