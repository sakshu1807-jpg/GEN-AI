import os
import streamlit as st
import requests
from dotenv import load_dotenv

st.set_page_config(page_title="Question Generator AI Bot", page_icon="📝", layout="centered")

load_dotenv()

st.title("📝 Question Generator AI Bot")
st.markdown("Analyze paragraphs and generate highly structured educational question schemas.")

BACKEND_URL = "http://127.0.0.1:8000"

st.sidebar.header("⚙️ API Configuration")
st.sidebar.markdown(
    "This app runs on a free developer key by default. If the system experiences high traffic "
    "and encounters a rate limit, please paste your personal free Mistral API key below to continue testing."
)
user_mistral_key = st.sidebar.text_input("Your Mistral API Key (Fallback)", type="password")

num_questions = st.slider("Number of questions to generate:", min_value=1, max_value=10, value=3)
user_paragraph = st.text_area(
    "Enter your paragraph here:", 
    height=200, 
    placeholder="Paste your source text or article snippet here..."
)

if st.button("Generate Questions", type="primary"):
    if not user_paragraph.strip():
        st.warning("Please enter a text paragraph first!")
    else:

        st.warning(
            "⚠️ **Attention:** This application uses Render's FREE hosting tier. "
            "If the app hasn't been visited recently, the server goes to sleep and can take "
            "**30 to 40 seconds** to wake up. Please remain on the page!"
        )

        with st.spinner("Generating questions from AI model..."):
            
            active_key = user_mistral_key if user_mistral_key else os.getenv("MISTRAL_API_KEY")

            payload = {
                "paragraph": user_paragraph,
                "num_questions": num_questions,
                "api_key": active_key
            }

            try:
                response = requests.post(BACKEND_URL, json = payload, timeout = 140)

                if response.status_code == 400:
                        st.warning("⚠️ **Input too long:** Please limit your input paragraph to under 3,000 words.")
                        
                elif response.status_code == 429:
                    st.error("⚠️ **Demo Request Limit Reached!**")
                    st.markdown("The shared free developer quota for this app has temporarily run out of tokens.")
                    st.info("💡 **How to resolve:** Paste your personal free Mistral API key into the sidebar panel!")
                    
                elif response.status_code != 200:
                    st.error("The backend server encountered an error processing your request.")
                    st.code(response.text)
                    
                else:
                    # SUCCESS: Parse response data dictionary directly
                    json_data = response.json()
                    st.success("🎉 Structured Data Generated Successfully!")
                    
                    st.subheader(f"Topic: {json_data.get('topic', 'General Analysis')}")
                    st.info(json_data.get('introduction', ''))
                    
                    st.markdown("### Generated Questions:")
                    for idx, question in enumerate(json_data.get('questions', []), 1):
                        st.markdown(f"**{idx}.** {question}")
                        
            except requests.exceptions.RequestException as e:
                st.error("Could not connect to the backend server. Make sure it is running and accessible.")
                st.code(e)