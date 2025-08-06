import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Faye - Home",
    page_icon="🤓",
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
    index=0
)

# Navigate to selected page
if selected_page != "🏠 Home":
    st.switch_page(page_options[selected_page])

# Home page content
st.title("Hi! Welcome to Faye 🤓")
st.write(
    "Your all-in-one internal market research tool, powered by Buntin Group"
    "\n\nPlease put your Gemini API key below. Don't know the key? Find out how to get it [here](https://ai.google.dev/gemini-api/docs/api-key). "
)

# Add in main section for password protection
# st.write(
# ":closed_loack_with_key: Please enter in the password to access Faye."
# "\nPlease contact your administrator if you are having trouble with access.")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
print(openai_api_key)

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Who are the main competitors of CFP?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
