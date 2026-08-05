import streamlit as st
import requests

# FastAPI Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

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
    user_field = st.text_input(
        "Enter Career Field (e.g., Artificial Intelligence, Quantum Computing, Product Management):",
        placeholder="e.g. Bioinformatics"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("Generate Report", type="primary", use_container_width=True)

# --- REPORT GENERATION LOGIC WITH LIVE CHECKPOINTS ---
if generate_btn:
    if not user_field.strip():
        st.warning("Please enter a valid educational or career field first.")
    else:
        # Create dedicated container for task checkpoints
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### ⏳ Multi-Agent Execution Pipeline")
            
            # Placeholders for dynamic task status updates
            status_search = st.empty()
            status_scrape = st.empty()
            status_synthesize = st.empty()

            # Initial State: Task 1 loading, others pending
            status_search.markdown("⏳ **Task 1:** Agent 1 searching web & career databases...")
            status_scrape.markdown("⚪ **Task 2:** Agent 2 scraping and parsing URL content...")
            status_synthesize.markdown("⚪ **Task 3:** Agent 3 synthesizing executive report...")

            try:
                # Update status prior to firing backend request
                status_search.markdown("✅ **Task 1:** Web search completed & target URLs extracted.")
                status_scrape.markdown("⏳ **Task 2:** Agent 2 scraping content from extracted URLs...")

                # Call FastAPI backend research endpoint
                response = requests.post(
                    f"{BACKEND_URL}/research_report",
                    params={"user_field": user_field, "user_response": True},
                    timeout=180
                )

                if response.status_code == 200:
                    status_scrape.markdown("✅ **Task 2:** Web scraping & text cleaning completed.")
                    status_synthesize.markdown("⏳ **Task 3:** Synthesizing high-density career report...")

                    data = response.json()
                    if isinstance(data, str):
                        st.session_state.report = data
                    else:
                        st.session_state.report = data.get("report", str(data))

                    # Final State: All tasks complete
                    status_synthesize.markdown("✅ **Task 3:** Executive career report generated successfully!")
                    st.success("🎉 All tasks completed!")
                    
                    # Clear previous chat history on new report generation
                    st.session_state.chat_history = []
                else:
                    status_synthesize.markdown("❌ **Task 3:** Report generation failed.")
                    st.error(f"Server Error ({response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                status_search.markdown("❌ **Task 1:** Connection failed.")
                st.error("Could not connect to FastAPI backend. Ensure `uvicorn multiagent:app --reload` is running.")
            except Exception as e:
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