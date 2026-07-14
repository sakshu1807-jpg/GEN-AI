import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DocuChat AI", page_icon="📄", layout="wide")

# Initialize local session states
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "file_analyzed" not in st.session_state:
    st.session_state["file_analyzed"] = False
if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = ""

st.title("📄 DocuChat AI RAG Pipeline")
st.markdown("---")

# --- STEP 1: Main Page Upload Zone (Shows only if no file is analyzed yet) ---
if not st.session_state["file_analyzed"]:
    st.subheader("Upload your document to get started")
    uploaded_file = st.file_uploader(
        "Supports PDF, DOCX, or TXT documents", 
        type=["pdf", "docx", "txt"]
    )
    
    if uploaded_file is not None:
        if st.button("🚀 Analyze & Start Chatting", use_container_width=True):
            with st.spinner("Analyzing document structure and extracting text..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                try:
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.session_state["file_analyzed"] = True
                        st.session_state["uploaded_filename"] = uploaded_file.name
                        st.session_state["messages"] = []  # Reset chat history
                        st.rerun()  # Refresh layout instantly
                    else:
                        st.error(f"Server Error ({response.status_code}): {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend server. Make sure FastAPI is running.")

# --- STEP 2: Dashboard Layout (Triggers after successful analysis) ---
else:
    # Create two columns: Left for document management, Right for the actual Chat UI
    col1, col2 = st.columns([1, 2], gap="large")
    
    # Left Column: Document Overview
    with col1:
        st.subheader("📁 Active Document")
        st.info(f"**Filename:** {st.session_state['uploaded_filename']}")
        
        st.markdown("---")
        # Let the user reset and upload a different document if they want
        if st.button("🔄 Upload Different Document", use_container_width=True):
            st.session_state["file_analyzed"] = False
            st.session_state["uploaded_filename"] = ""
            st.session_state["messages"] = []
            st.rerun()

    # Right Column: The Main Chat Application
    with col2:
        st.subheader("💬 Chat Context")
        
        # Container to hold messages for scrollable area feel
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat Input Box fixed at the bottom
        if user_query := st.chat_input("Ask a question about your document..."):
            # Display user message instantly
            st.session_state["messages"].append({"role": "user", "content": user_query})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_query)
                    
            # Call backend API
            with chat_container:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    with st.spinner("Analyzing context..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/chat", 
                                json={"question": user_query}
                            )
                            
                            if response.status_code == 200:
                                answer = response.json().get("response", "")
                                message_placeholder.markdown(answer)
                                st.session_state["messages"].append({"role": "assistant", "content": answer})
                            else:
                                st.error(f"Chat Error ({response.status_code}): {response.text}")
                        except requests.exceptions.ConnectionError:
                            st.error("Lost connection to the backend server.")