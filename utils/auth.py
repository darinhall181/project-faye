"""
Authentication utilities for Faye.

Overview
--------
- Credentials are read at runtime from Streamlit secrets (st.secrets)
  which are stored locally in .streamlit/secrets.toml (git-ignored) or
  configured in the hosting environment (e.g., Streamlit Cloud Secrets UI).
- Upon successful login, pages set st.session_state["authenticated"] = True
  and st.session_state["username"] to the logged-in user. These values
  live for the duration of the user’s session in the browser.
- Pages should call ensure_authentication() at the top to redirect
  unauthenticated users back to the login page.
"""

import streamlit as st
from typing import Optional


def authenticate(username: str, password: str) -> bool:
    """Return True if provided credentials match the configured secrets.

    This compares the submitted username and password against
    st.secrets["CORRECT_USERNAME"] and st.secrets["CORRECT_PASSWORD"].
    Secrets are never stored in Git; they are loaded from the environment
    where the app runs.
    """
    USERNAME = st.secrets["CORRECT_USERNAME"]
    try:
        correct_password = st.secrets["CORRECT_PASSWORD"]
    except Exception:
        correct_password = None
    return username == USERNAME and password == correct_password


def ensure_authentication() -> None:
    """Redirect to the login page if the user is not authenticated.

    Use this at the top of any page that requires login. It checks the
    session flag set by the login page and prevents unauthenticated access.
    """
    if not st.session_state.get("authenticated"):
        st.switch_page("pages/password_page.py")


def current_username() -> Optional[str]:
    """Get the username associated with the current session, if any."""
    return st.session_state.get("username")


