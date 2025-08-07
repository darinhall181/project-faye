import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Market Research",
    page_icon="🔍",
    layout="wide"
)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/password_page.py")

# === Sidebar ===

# Persona dropdown
st.sidebar.title("Persona 🤖")

# Create persona dropdown
persona_options = {
    "None": None,
    "Market Research": "pages/market_research_page.py", 
    "Conviction Score": "pages/conviction_score_page.py",
    "Reader File": "pages/reader_file_page.py"
}

selected_page = st.sidebar.selectbox(
    "Choose a persona:",
    options=list(persona_options.keys()),
    index=1  # Market Research is the 2nd option (index 1)
)

# Navigate to selected page only if a valid option is selected and it's different from current page
if selected_page != "None" and selected_page != "Market Research" and persona_options[selected_page] is not None:
    st.switch_page(persona_options[selected_page])

# === Main Content ===

# Home button
if st.button("🏠 Back to Home", key="market_home"):
    st.switch_page("streamlit_app.py")

st.title("Market Research 🔍")

# === Gemini Chatbot Integration ===

# Gemini API Key from secrets.toml
Gemini_Key = st.secrets["GEMINI_APIKEY"]

# Check if API key is stored in session state
if "Key" not in st.session_state:
    st.session_state["Key"]  = st.secrets["GEMINI_APIKEY"]

# Configure Gemini API
genai.configure(api_key=Gemini_Key)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm an expert market researcher who's here to help :)"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input(placeholder="What are the latest trends in the electric vehicle market?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not Gemini_Key:
        st.info("The current API key is not working. Please contact your administrator for help.")
        st.stop()

    model =genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    with st.chat_message("assistant"):
        with st.spinner("Thinking with conviction..."):
            response = chat.send_message(prompt,stream=True)
            response.resolve()
            st.session_state.messages.append({"role": "assistant", "content": response.text}) 
            for chunk in response:
                st.markdown(chunk.text)


# === Document Uploader ===
uploaded_file = st.file_uploader(
    "Upload relevant documents as needed", 
    type=("pdf", "docx"),
    key="document_uploader"
)

if uploaded_file:
    st.success("Document uploaded successfully!")