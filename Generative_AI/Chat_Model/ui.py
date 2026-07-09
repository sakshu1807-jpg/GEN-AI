import os
import json
import streamlit as st
from dotenv import load_dotenv

from mini_project_1 import question_generator

st.set_page_config(page_title="Question Generator AI Bot", page_icon="📝", layout="centered")

load_dotenv()

st.title("📝 Question Generator AI Bot")
st.markdown("Analyze paragraphs and generate highly structured educational question schemas.")

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
        with st.spinner("Generating questions from AI model..."):
            
            active_key = user_mistral_key if user_mistral_key else os.getenv("MISTRAL_API_KEY")

            result = question_generator(user_paragraph, num_questions, active_key)
            error_check = result.lower()
            
            if "input too long" in error_check:
                st.warning("⚠️ **Input too long:** Please limit your input paragraph to under 3,000 words.")
            
            # Check for structural 429 errors, structural limits, or timeouts passed back by the error block
            elif "429" in error_check or "rate limit" in error_check or "quota" in error_check or "timeout" in error_check:
                st.error("⚠️ **Demo Request Limit Reached!**")
                st.markdown(
                    "The shared free developer quota for this app has temporarily run out of tokens "
                    "due to high traffic spikes from LinkedIn visitors."
                )
                st.info(
                    "💡 **How to resolve:** Please generate your own free API key from the Mistral Console, "
                    "paste it into the left sidebar settings panel, and try again!"
                )
                
            elif result.startswith("The model cannot load"):
                st.error("An unexpected error occurred while communicating with the AI model server.")
                st.code(result)
                
            else:
                st.success("🎉 Questions Generated Successfully!")
                
                try:
                    json_data = json.loads(result)
                    
                    st.subheader(f"Topic : {json_data.get('topic', 'General Analysis')}")
                    st.info(json_data.get('introduction', 'No introduction generated.'))
                    for idx, question in enumerate(json_data.get('questions', []), 1):
                        st.markdown(f"**{idx}.** {question}")
                        
                except Exception as parse_error:
                    st.markdown("### Raw Output:")
                    st.code(result, language="json")