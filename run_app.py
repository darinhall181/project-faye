#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        import streamlit.web.cli as stcli
        import streamlit as st
        
        # Set up the command line arguments for streamlit
        sys.argv = ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
        
        # Run the streamlit app
        stcli.main()
        
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        print("This might be due to Python 3.13.1 compatibility issues.")
        print("Try using Python 3.11 or 3.12 instead.")

if __name__ == "__main__":
    main() 