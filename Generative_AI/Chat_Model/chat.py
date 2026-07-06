from dotenv import load_dotenv

load_dotenv()

# GOOGLE CHATBOT TESTING

# from langchain.chat_models import init_chat_model

# model_gemini = init_chat_model(model = "google_genai:gemini-2.5-flash")

# response_gemini = model_gemini.invoke("Hello, My name is saksham. Tell me about yourself")
# print(response_gemini.content)

# GROQ CHATBOT TESTING
# Importing the particular model class

# from langchain_groq import ChatGroq

# model_groq = ChatGroq(model = "openai/gpt-oss-120b")

# response_groq = model_groq.invoke("Hello Groq, tell me about yourself.")
# print(response_groq.content)

# MISTRAL AI CHATBOT TESTING

from langchain_mistralai import ChatMistralAI

model_mistral = ChatMistralAI(model = "mistral-medium-latest")

response_mistral = model_mistral.invoke("Hello, Mistral AI. Tell me about yourself.")
print(response_mistral.content)
