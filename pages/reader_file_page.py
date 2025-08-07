import streamlit as st
import google.generativeai as genai
import hashlib
from datetime import datetime
from utils.auth import ensure_authentication, current_username
from utils.user_store import save_user_store

# Page configuration
st.set_page_config(
    page_title="Reader File",
    page_icon="📖",
    layout="wide"
)

# Check authentication
ensure_authentication()

# === Initialize Session State (Reader-specific keys) ===
if "reader_chat_history" not in st.session_state:
    user_store = st.session_state.get("user_store") or {}
    st.session_state.reader_chat_history = (user_store.get("reader", {}).get("chat_history") or {})

if "reader_current_chat_id" not in st.session_state:
    user_store = st.session_state.get("user_store") or {}
    st.session_state.reader_current_chat_id = user_store.get("reader", {}).get("current_chat_id")

# === Sidebar ===
# Persona buttons on top
st.sidebar.title("Persona 🎭")

persona_options = {
    "Market Research": "pages/market_research_page.py", 
    "Conviction Score": "pages/conviction_score_page.py",
    "Reader File": "pages/reader_file_page.py"
}

st.sidebar.write("Choose a persona:")
for persona_label, persona_path in persona_options.items():
    if persona_label != "Reader File":
        if st.sidebar.button(persona_label, key=f"persona_btn_reader_{persona_label.replace(' ', '_').lower()}"):
            st.switch_page(persona_path)

# === Chat History Management ===
st.sidebar.markdown("---")
st.sidebar.title("Chat History 💬")
st.sidebar.subheader("Conversations")

# Create new chat button
if st.sidebar.button("New Chat", key="reader_new_chat_btn"):
    # Generate new chat ID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_chat_id = f"reader_chat_{timestamp}"
    default_title = f"Chat on {datetime.now().strftime('%b %d, %Y')}"

    # Initialize new chat
    st.session_state.reader_chat_history[new_chat_id] = {
        "messages": [
            {"role": "assistant", "content": "Hi! Upload a document and ask me anything about it."}
        ],
        "uploaded_files": [],
        "created_at": timestamp,
        "title": default_title,
    }

    st.session_state.reader_current_chat_id = new_chat_id
    # Persist
    user_store = st.session_state.get("user_store", {})
    user_store.setdefault("reader", {})["chat_history"] = st.session_state.reader_chat_history
    user_store["reader"]["current_chat_id"] = st.session_state.reader_current_chat_id
    st.session_state.user_store = user_store
    save_user_store(current_username() or "anonymous", user_store)
    st.rerun()

# Display existing chats (newest first)
if st.session_state.reader_chat_history:
    sorted_chats = sorted(
        st.session_state.reader_chat_history.items(),
        key=lambda item: item[1].get("created_at", item[0]),
        reverse=True,
    )
    for chat_id, chat_data in sorted_chats:
        chat_title = chat_data.get("title", f"Chat {chat_id}")
        created_time = chat_data.get("created_at", "")

        with st.sidebar.expander(f"{chat_title}", expanded=False):
            # Uploaded files info
            if chat_data.get("uploaded_files"):
                st.write("📎 Files:", ", ".join([f["name"] for f in chat_data["uploaded_files"]]))

            if st.button("Open Chat", key=f"open_{chat_id}"):
                st.session_state.reader_current_chat_id = chat_id
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("reader", {})["current_chat_id"] = chat_id
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.rerun()

            if st.button("🗑️ Delete", key=f"delete_{chat_id}"):
                del st.session_state.reader_chat_history[chat_id]
                if st.session_state.reader_current_chat_id == chat_id:
                    st.session_state.reader_current_chat_id = None
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("reader", {})["chat_history"] = st.session_state.reader_chat_history
                user_store["reader"]["current_chat_id"] = st.session_state.reader_current_chat_id
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.rerun()

# Home button
if st.button("🏠 Back to Home", key="reader_home"):
    st.switch_page("streamlit_app.py")

# === Main Content ===
st.title("Reader File 📖")

# === Chat Interface ===
st.markdown("---")
st.subheader("💬 Chat about your document")

# Do not auto-select a chat; require clicking "Open Chat"

if st.session_state.reader_current_chat_id and st.session_state.reader_current_chat_id in st.session_state.reader_chat_history:
    current_chat = st.session_state.reader_chat_history[st.session_state.reader_current_chat_id]

    # === Document Uploader (only with active chat) ===
    st.markdown("---")
    st.subheader("📎 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload documents to read (TXT or MD)", 
        type=("txt", "md"),
        key="reader_uploader"
    )

    if uploaded_file:
        file_content = uploaded_file.read()
        file_hash = hashlib.md5(file_content).hexdigest()

        file_info = {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "size": len(file_content),
            "hash": file_hash,
            "uploaded_at": datetime.now().isoformat()
        }

        existing_files = current_chat.setdefault("uploaded_files", [])
        if not any(f["hash"] == file_hash for f in existing_files):
            existing_files.append(file_info)
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            # Persist after upload
            user_store = st.session_state.get("user_store", {})
            user_store.setdefault("reader", {})["chat_history"] = st.session_state.reader_chat_history
            save_user_store(current_username() or "anonymous", user_store)
        else:
            st.info(f"📄 {uploaded_file.name} already uploaded in this conversation.")

    # Show uploaded files
    if current_chat.get("uploaded_files"):
        st.write("📎 **Uploaded Files:**")
        for file_info in current_chat["uploaded_files"]:
            st.write(f"  • {file_info['name']} ({file_info['type']})")

    # Render chat messages
    for msg in current_chat["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask anything about the uploaded document...", key="reader_chat_input"):
        current_chat["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # Persist after user message
        user_store = st.session_state.get("user_store", {})
        user_store.setdefault("reader", {})["chat_history"] = st.session_state.reader_chat_history
        save_user_store(current_username() or "anonymous", user_store)

        # Compose context from files and messages
        context_summary = {
            "uploaded_files": [f["name"] for f in current_chat.get("uploaded_files", [])],
            "num_messages": len(current_chat["messages"])
        }

        enhanced_prompt = f"""
        User Query: {prompt}

        Context:
        - Uploaded files: {context_summary['uploaded_files']}
        - Conversation length: {context_summary['num_messages']} messages

        Please read the uploaded documents if provided and answer the question.
        """

        Gemini_Key = st.secrets["GEMINI_APIKEY"]
        if not Gemini_Key:
            st.error("❌ API key not configured. Please contact your administrator.")
        else:
            try:
                genai.configure(api_key=Gemini_Key)
                model = genai.GenerativeModel("gemini-pro")
                chat = model.start_chat(history=[])

                with st.chat_message("assistant"):
                    with st.spinner("📖 Reading and analyzing the document..."):
                        response = chat.send_message(enhanced_prompt, stream=True)
                        response.resolve()
                        current_chat["messages"].append({"role": "assistant", "content": response.text})
                        # Persist after assistant message
                        user_store = st.session_state.get("user_store", {})
                        user_store.setdefault("reader", {})["chat_history"] = st.session_state.reader_chat_history
                        save_user_store(current_username() or "anonymous", user_store)
                        for chunk in response:
                            st.markdown(chunk.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please check your API key and try again.")
else:
    st.info("💡 Start a new chat or open an existing one from the sidebar to begin reading your document!")
    st.markdown("""
    **How to use:**
    1. Click "New Chat" in the sidebar (if no chats exist)
    2. Or click "Open Chat" on a conversation (if chats exist)
    3. Upload a document (appears once a chat is active)
    4. Ask questions about the content
    5. Your conversations will be saved in the sidebar
    """)

# === Delete All Chats (with confirmation) ===
confirm_flag_key = "confirm_delete_all_reader"
if st.session_state.reader_chat_history:
    st.sidebar.markdown("---")
    if not st.session_state.get(confirm_flag_key):
        if st.sidebar.button("Delete all chats", key="reader_delete_all"):
            st.session_state[confirm_flag_key] = True
            st.rerun()
    else:
        st.sidebar.warning("Are you sure you want to delete all chats? This action cannot be undone and all information from the chats will be lost.")
        col_a, col_b = st.sidebar.columns(2)
        with col_a:
            if st.button("Confirm", key="reader_confirm_delete_all"):
                st.session_state.reader_chat_history = {}
                st.session_state.reader_current_chat_id = None
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("reader", {})["chat_history"] = {}
                user_store["reader"]["current_chat_id"] = None
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.session_state[confirm_flag_key] = False
                st.rerun()
        with col_b:
            if st.button("Cancel", key="reader_cancel_delete_all"):
                st.session_state[confirm_flag_key] = False
                st.rerun()
else:
    # Reset any stale confirmation state
    if st.session_state.get(confirm_flag_key):
        st.session_state[confirm_flag_key] = False