import streamlit as st
import google.generativeai as genai
import hashlib
from datetime import datetime
from utils.auth import ensure_authentication, current_username
from utils.user_store import save_user_store

# Page configuration
st.set_page_config(
    page_title="Market Research",
    page_icon="🔍",
    layout="wide"
)

# Check authentication
ensure_authentication()

# === Initialize Session State ===
if "chat_history" not in st.session_state:
    # Initialize from user store if available
    user = current_username()
    user_store = st.session_state.get("user_store") or {}
    st.session_state.chat_history = (user_store.get("market", {}).get("chat_history") or {})

if "current_chat_id" not in st.session_state:
    user_store = st.session_state.get("user_store") or {}
    st.session_state.current_chat_id = user_store.get("market", {}).get("current_chat_id")

if "uploaded_files_info" not in st.session_state:
    st.session_state.uploaded_files_info = {}

# === Sidebar ===
# Persona buttons - Moved to top for better accessibility
st.sidebar.title("Persona 🎭")

persona_options = {
    "Market Research": "pages/market_research_page.py", 
    "Conviction Score": "pages/conviction_score_page.py",
    "Reader File": "pages/reader_file_page.py"
}

st.sidebar.write("Choose a persona:")
for persona_label, persona_path in persona_options.items():
    if persona_label != "Market Research":
        if st.sidebar.button(persona_label, key=f"persona_btn_market_{persona_label.replace(' ', '_').lower()}"):
            st.switch_page(persona_path)

# === Chat History Management ===
st.sidebar.markdown("---")
st.sidebar.title("Chat History 💬")
st.sidebar.subheader("Conversations")

# Create new chat button
if st.sidebar.button("New Chat", key="new_chat_btn"):
    # Generate new chat ID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_chat_id = f"chat_{timestamp}"
    default_title = f"Chat on {datetime.now().strftime('%b %d, %Y')}"
    
    # Initialize new chat
    st.session_state.chat_history[new_chat_id] = {
        "messages": [
            {"role": "assistant", "content": "Hi, I'm an expert market researcher who's here to help! What would you like to research today?"}
        ],
        "uploaded_files": [],
        "created_at": timestamp,
        "title": default_title,
    }
    
    st.session_state.current_chat_id = new_chat_id
    # Persist to user store
    user_store = st.session_state.get("user_store", {})
    user_store.setdefault("market", {})["chat_history"] = st.session_state.chat_history
    user_store["market"]["current_chat_id"] = st.session_state.current_chat_id
    st.session_state.user_store = user_store
    save_user_store(current_username() or "anonymous", user_store)
    st.rerun()

# Display existing chats (newest first)
if st.session_state.chat_history:
    sorted_chats = sorted(
        st.session_state.chat_history.items(),
        key=lambda item: item[1].get("created_at", item[0]),
        reverse=True,
    )
    for chat_id, chat_data in sorted_chats:
        # Show chat title and timestamp
        chat_title = chat_data.get("title", f"Chat {chat_id}")
        created_time = chat_data.get("created_at", "")
        
        # Create expandable section for each chat
        with st.sidebar.expander(f"{chat_title}", expanded=False):
            
            # Show uploaded files info
            if chat_data.get("uploaded_files"):
                st.write("📎 Files:", ", ".join([f["name"] for f in chat_data["uploaded_files"]]))
            
            # Button to switch to this chat
            if st.button("Open Chat", key=f"open_{chat_id}"):
                st.session_state.current_chat_id = chat_id
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("market", {})["current_chat_id"] = chat_id
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.rerun()
            
            # Button to delete chat
            if st.button("🗑️ Delete", key=f"delete_{chat_id}"):
                del st.session_state.chat_history[chat_id]
                if st.session_state.current_chat_id == chat_id:
                    st.session_state.current_chat_id = None
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("market", {})["chat_history"] = st.session_state.chat_history
                user_store["market"]["current_chat_id"] = st.session_state.current_chat_id
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.rerun()

# Home button
if st.button("🏠 Back to Home", key="market_home"):
    st.switch_page("streamlit_app.py")

# === Main Content ===
st.title("Market Research 🔍")

# === Chat Interface ===
st.markdown("---")
st.subheader("💬 Chat with Market Research Assistant")

# Do not auto-select a chat; require user to click "Open Chat"

# Display current chat
if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.chat_history:
    current_chat = st.session_state.chat_history[st.session_state.current_chat_id]
    
    # === Document Uploader (only visible when a chat is active) ===
    st.markdown("---")
    st.subheader("📎 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload relevant documents (PDF, DOCX)", 
        type=("pdf", "docx"),
        key="document_uploader"
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
        current_chat.setdefault("uploaded_files", [])
        existing_files = current_chat["uploaded_files"]
        if not any(f["hash"] == file_hash for f in existing_files):
            current_chat["uploaded_files"].append(file_info)
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            user_store = st.session_state.get("user_store", {})
            user_store.setdefault("market", {})["chat_history"] = st.session_state.chat_history
            save_user_store(current_username() or "anonymous", user_store)
        else:
            st.info(f"📄 {uploaded_file.name} already uploaded in this conversation.")
    
    # Show uploaded files for current chat
    if current_chat.get("uploaded_files"):
        st.write("📎 **Uploaded Files:**")
        for file_info in current_chat["uploaded_files"]:
            st.write(f"  • {file_info['name']} ({file_info['type']})")
    
    # Display chat messages
    for msg in current_chat["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about market research...", key="chat_input"):
        # Add user message
        current_chat["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # Persist after user message
        user_store = st.session_state.get("user_store", {})
        user_store.setdefault("market", {})["chat_history"] = st.session_state.chat_history
        save_user_store(current_username() or "anonymous", user_store)
        
        # Prepare context information
        context_info = {
            "user_prompt": prompt,
            "uploaded_files": current_chat.get("uploaded_files", []),
            "chat_history": len(current_chat["messages"])
        }
        
        # Create enhanced prompt with context
        enhanced_prompt = f"""
        User Query: {prompt}
        
        Context Information:
        - Number of uploaded files: {len(context_info['uploaded_files'])}
        - Files: {[f['name'] for f in context_info['uploaded_files']]}
        - Conversation length: {context_info['chat_history']} messages
        
        Please provide a comprehensive market research response considering any uploaded documents and previous conversation context. 
        Please be as robust as possible, including any relevant information that you can find including links to the sources.
        """
        
        # Gemini API integration
        Gemini_Key = st.secrets["GEMINI_APIKEY"]
        
        if not Gemini_Key:
            st.error("❌ API key not configured. Please contact your administrator.")
        else:
            try:
                genai.configure(api_key=Gemini_Key)
                model = genai.GenerativeModel("gemini-pro")
                chat = model.start_chat(history=[])
                
                with st.chat_message("assistant"):
                    with st.spinner("🔍 Analyzing market research..."):
                        response = chat.send_message(enhanced_prompt, stream=True)
                        response.resolve()
                        
                        # Add assistant response
                        current_chat["messages"].append({"role": "assistant", "content": response.text})
                        # Persist after assistant response
                        user_store = st.session_state.get("user_store", {})
                        user_store.setdefault("market", {})["chat_history"] = st.session_state.chat_history
                        save_user_store(current_username() or "anonymous", user_store)
                        
                        # Stream the response
                        for chunk in response:
                            st.markdown(chunk.text)
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please check your API key and try again.")

else:
    # No active chat
    st.info("💡 Start a new chat or open an existing one from the sidebar to begin your market research!")
    st.markdown("""
    **How to use:**
    1. Click "New Chat" in the sidebar (if no chats exist)
    2. Or click "Open Chat" on a conversation (if chats exist)
    3. Upload relevant documents that you would like to be included in the market research report
    4. Ask questions about market research
    """)

# === Delete All Chats (with confirmation) ===
confirm_flag_key = "confirm_delete_all_market"
if st.session_state.chat_history:
    st.sidebar.markdown("---")
    if not st.session_state.get(confirm_flag_key):
        if st.sidebar.button("Delete all chats", key="market_delete_all"):
            st.session_state[confirm_flag_key] = True
            st.rerun()
    else:
        st.sidebar.warning("Are you sure you want to delete all chats? This action cannot be undone and all information from the chats will be lost.")
        col_a, col_b = st.sidebar.columns(2)
        with col_a:
            if st.button("Confirm", key="market_confirm_delete_all"):
                st.session_state.chat_history = {}
                st.session_state.current_chat_id = None
                user_store = st.session_state.get("user_store", {})
                user_store.setdefault("market", {})["chat_history"] = {}
                user_store["market"]["current_chat_id"] = None
                st.session_state.user_store = user_store
                save_user_store(current_username() or "anonymous", user_store)
                st.session_state[confirm_flag_key] = False
                st.rerun()
        with col_b:
            if st.button("Cancel", key="market_cancel_delete_all"):
                st.session_state[confirm_flag_key] = False
                st.rerun()
else:
    # Reset any stale confirmation state
    if st.session_state.get(confirm_flag_key):
        st.session_state[confirm_flag_key] = False
