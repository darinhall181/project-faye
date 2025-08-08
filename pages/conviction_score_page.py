import streamlit as st
import google.generativeai as genai
import hashlib
from datetime import datetime
from utils.auth import ensure_authentication, current_username
from utils.user_store import save_user_store

# Page configuration
st.set_page_config(
    page_title="Conviction Score",
    page_icon="💡",
    layout="wide"
)

# Check authentication
ensure_authentication()

# === Initialize Session State (Conviction-specific) ===
if "conviction_chat_history" not in st.session_state:
    user_store = st.session_state.get("user_store") or {}
    st.session_state.conviction_chat_history = (user_store.get("conviction", {}).get("chat_history") or {})

if "conviction_current_chat_id" not in st.session_state:
    user_store = st.session_state.get("user_store") or {}
    st.session_state.conviction_current_chat_id = user_store.get("conviction", {}).get("current_chat_id")

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
    if persona_label != "Conviction Score":
        if st.sidebar.button(persona_label, key=f"persona_btn_conviction_{persona_label.replace(' ', '_').lower()}"):
            st.switch_page(persona_path)

# === Chat History Management ===
st.sidebar.markdown("---")
st.sidebar.title("Chat History 💬")
st.sidebar.subheader("Conversations")

# Create new chat button
if st.sidebar.button("New Chat", key="conviction_new_chat_btn"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_chat_id = f"conv_chat_{timestamp}"
    default_title = f"Chat on {datetime.now().strftime('%b %d, %Y')}"

    st.session_state.conviction_chat_history[new_chat_id] = {
        "messages": [
            {"role": "assistant", "content": "Hi! I'm your conviction scoring assistant. Upload an investment document or ask a question to get started."}
        ],
        "uploaded_files": [],
        "created_at": timestamp,
        "title": default_title,
    }

    st.session_state.conviction_current_chat_id = new_chat_id
    # Persist
    user_store = st.session_state.get("user_store", {})
    user_store.setdefault("conviction", {})["chat_history"] = st.session_state.conviction_chat_history
    user_store["conviction"]["current_chat_id"] = st.session_state.conviction_current_chat_id
    st.session_state.user_store = user_store
    save_user_store(current_username() or "anonymous", user_store)
    st.rerun()

# Display existing chats (newest first)
if st.session_state.conviction_chat_history:
    sorted_chats = sorted(
        st.session_state.conviction_chat_history.items(),
        key=lambda item: item[1].get("created_at", item[0]),
        reverse=True,
    )
    for chat_id, chat_data in sorted_chats:
        chat_title = chat_data.get("title", f"Chat {chat_id}")

        with st.sidebar.expander(f"{chat_title}", expanded=False):
            # Uploaded files info
            if chat_data.get("uploaded_files"):
                st.write("📎 Files:", ", ".join([f["name"] for f in chat_data["uploaded_files"]]))

            # Open chat
            if st.button("Open Chat", key=f"open_{chat_id}"):
                st.session_state.conviction_current_chat_id = chat_id
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("conviction", {})["current_chat_id"] = chat_id
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.rerun()

            # Delete chat
            if st.button("🗑️ Delete", key=f"delete_{chat_id}"):
                del st.session_state.conviction_chat_history[chat_id]
                if st.session_state.conviction_current_chat_id == chat_id:
                    st.session_state.conviction_current_chat_id = None
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("conviction", {})["chat_history"] = st.session_state.conviction_chat_history
                user_store["conviction"]["current_chat_id"] = st.session_state.conviction_current_chat_id
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.rerun()

# Home button
if st.button("🏠 Back to Home", key="conviction_home"):
    st.switch_page("streamlit_app.py")

# === Main Content ===
st.title("Conviction Score 💡")

# === Chat Interface ===
st.markdown("---")
st.subheader("💬 Chat with Conviction Assistant")

# Do not auto-select a chat; require clicking "Open Chat"

# Display current chat
if st.session_state.conviction_current_chat_id and st.session_state.conviction_current_chat_id in st.session_state.conviction_chat_history:
    current_chat = st.session_state.conviction_chat_history[st.session_state.conviction_current_chat_id]

    # === Document Uploader (only with active chat) ===
    st.markdown("---")
    st.subheader("📎 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload relevant investment documents (PDF, DOCX)", 
        type=("pdf", "docx"),
        key="conviction_uploader"
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
            user_store = st.session_state.get("user_store", {})
            user_store.setdefault("conviction", {})["chat_history"] = st.session_state.conviction_chat_history
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
    if prompt := st.chat_input("Ask about conviction and risk...", key="conviction_chat_input"):
        current_chat["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # Persist
        user_store = st.session_state.get("user_store", {})
        user_store.setdefault("conviction", {})["chat_history"] = st.session_state.conviction_chat_history
        save_user_store(current_username() or "anonymous", user_store)

        # Build context summary
        context_summary = {
            "uploaded_files": [f["name"] for f in current_chat.get("uploaded_files", [])],
            "num_messages": len(current_chat["messages"])
        }

        enhanced_prompt = f"""
        User Query: {prompt}

        Context Information:
        - Uploaded files: {context_summary['uploaded_files']}
        - Conversation length: {context_summary['num_messages']} messages

        You are an advertising analyst. Provide a conviction score rationale based on the uploaded documents. Use any uploaded documents as grounding context.
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
                    with st.spinner("💡 Evaluating conviction..."):
                        response = chat.send_message(enhanced_prompt, stream=True)
                        response.resolve()
                        current_chat["messages"].append({"role": "assistant", "content": response.text})
                        user_store = st.session_state.get("user_store", {})
                        user_store.setdefault("conviction", {})["chat_history"] = st.session_state.conviction_chat_history
                        save_user_store(current_username() or "anonymous", user_store)
                        for chunk in response:
                            st.markdown(chunk.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please check your API key and try again.")
else:
    st.info("💡 Start a new chat or open an existing one from the sidebar to begin conviction scoring!")
    st.markdown("""
    **How to use:**
    1. Click "New Chat" in the sidebar (if no chats exist)
    2. Or click "Open Chat" on a conversation (if chats exist)
    3. Upload relevant documents that you would like to be included in the calculation
    """)

# === Delete All Chats (with confirmation) ===
confirm_flag_key = "confirm_delete_all_conviction"
if st.session_state.conviction_chat_history:
    st.sidebar.markdown("---")
    if not st.session_state.get(confirm_flag_key):
        if st.sidebar.button("Delete all chats", key="conviction_delete_all"):
            st.session_state[confirm_flag_key] = True
            st.rerun()
    else:
        st.sidebar.warning("Are you sure you want to delete all chats? This action cannot be undone and all information from the chats will be lost.")
        col_a, col_b = st.sidebar.columns(2)
        with col_a:
            if st.button("Confirm", key="conviction_confirm_delete_all"):
                st.session_state.conviction_chat_history = {}
                st.session_state.conviction_current_chat_id = None
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("conviction", {})["chat_history"] = {}
                user_store["conviction"]["current_chat_id"] = None
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.session_state[confirm_flag_key] = False
                st.rerun()
        with col_b:
            if st.button("Cancel", key="conviction_cancel_delete_all"):
                st.session_state[confirm_flag_key] = False
                st.rerun()
else:
    # Reset any stale confirmation state
    if st.session_state.get(confirm_flag_key):
        st.session_state[confirm_flag_key] = False