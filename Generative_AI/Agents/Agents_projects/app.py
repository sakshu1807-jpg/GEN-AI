import streamlit as st
import requests

# FastAPI Backend URL
BACKEND_URL = " https://multi-agent-research-report-system.onrender.com"

st.set_page_config(
    page_title="Multi-Agent Career Research System",
    page_icon="🚀",
    layout="wide"
)

# Initialize Streamlit Session State
if "report" not in st.session_state:
    st.session_state.report = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🚀 Multi-Agent Career Research & Intelligence System")
st.markdown("Enter an educational or professional career field to generate a comprehensive, data-dense research report, then chat with an AI grounded directly in the results.")

# --- SIDEBAR / INPUT SECTION ---
with st.container():
    st.subheader("Target Field Configuration")

    st.info(
    "ℹ️ **Note:** The backend is hosted on Render's free tier, which spins down after 15 minutes of inactivity. "
    "If the server is sleeping, the initial request may take **30–40 seconds** to wake up. Thank you for your patience!"
    )
    
    user_field = st.text_input(
        "Enter Career Field (e.g., Artificial Intelligence, Quantum Computing, Product Management):",
        placeholder="e.g. Bioinformatics"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("Generate Report", type="primary", use_container_width=True)

# --- REPORT GENERATION LOGIC WITH NATIVE STREAMLIT STATUS CONTAINER ---
if generate_btn:
    if not user_field.strip():
        st.warning("Please enter a valid educational or career field first.")
    else:
        # st.status creates a container with a spinning loading indicator while running
        with st.status("Executing Multi-Agent Workflow...", expanded=True) as status:
            st.write("🔍 **Task 1:** Agent 1 searching web & career databases...")
            st.write("🌐 **Task 2:** Agent 2 scraping and parsing URL content...")
            st.write("🧠 **Task 3:** Agent 3 synthesizing executive report...")

            try:
                # Send HTTP POST request to FastAPI backend
                response = requests.post(
                    f"{BACKEND_URL}/research_report",
                    params={"user_field": user_field, "user_response": True},
                    timeout=180
                )

                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, str):
                        st.session_state.report = data
                    else:
                        st.session_state.report = data.get("report", str(data))

                    # Update status container label and flip the spinner into a complete checkmark
                    status.update(
                        label="✅ All agent tasks completed! Intelligence report generated.",
                        state="complete",
                        expanded=False
                    )
                    
                    # Clear previous chat history on new report generation
                    st.session_state.chat_history = []
                else:
                    status.update(
                        label="❌ Report generation failed.",
                        state="error",
                        expanded=True
                    )
                    st.error(f"Server Error ({response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                status.update(
                    label="❌ Connection failed.",
                    state="error",
                    expanded=True
                )
                st.error("Could not connect to FastAPI backend. Ensure `uvicorn multi_agent_2:app --reload` is running.")
            except Exception as e:
                status.update(
                    label="❌ Error occurred.",
                    state="error",
                    expanded=True
                )
                st.error(f"An unexpected error occurred: {e}")

# --- DISPLAY REPORT & CHAT INTERFACE ---
if st.session_state.report:
    st.divider()
    st.subheader("📄 Generated Intelligence Report")
    
    with st.container():
        st.markdown(st.session_state.report)
        
    st.divider()
    st.subheader("💬 Ask Questions About This Report")
    st.markdown("Chat with the Llama-3 model, strictly grounded in the research context above.")

    for message in st.session_state.chat_history:
        role = message.get("role")
        content = message.get("content")
        with st.chat_message(role):
            st.markdown(content)

    if user_query := st.chat_input("Ask something about the career paths, exams, or future outlook..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing report context..."):
                try:
                    chat_response = requests.post(
                        f"{BACKEND_URL}/chat_model",
                        params={"user": user_query},
                        timeout=60
                    )
                    
                    if chat_response.status_code == 200:
                        res_json = chat_response.json()
                        ai_answer = res_json.get("content", str(res_json)) if isinstance(res_json, dict) else str(res_json)
                        
                        st.markdown(ai_answer)
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_answer})
                    else:
                        st.error(f"Chat error: {chat_response.text}")
                except Exception as e:
                    st.error(f"Failed to communicate with chat service: {e}")