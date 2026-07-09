from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print(""*30, "Welcome to Jarvis Chatbot")
print("="*60)

print("\nEnter 'exit' to terminate the conversation!!\n")

# -----------------------------------------------------------
# Unprofessional way of handling the memory with just a list
# -----------------------------------------------------------

# messages = []
# while True:
#     model = ChatMistralAI(
#         model = "mistral-medium-latest",
#         temperature= 0.35, 
#         max_tokens= 300
#     )
#     prompt = input("You : ")
#     messages.append(prompt)
#     if prompt == "0":
#         print("\nChat Ended. Thank you for this engaging conversation.")
#         break

#     response = model.invoke(messages) # Sending the entire history to the model to develop the context of the past conversation
#     print("Jarvis : ", response.content)

# ----------------------------------------------------------------------------------------------------------------
# Professional way of handling the memory with langchain.core library which has three different types of messages
# ----------------------------------------------------------------------------------------------------------------

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class chatbot():
    def __init__(self, api_key : str):
        self.model = ChatMistralAI(
                model = "mistral-medium-latest",
                temperature= 0.6,
                api_key = api_key
        )
        
    def set_tone(self, tone : str):
        self.prompts_history = [SystemMessage(tone)]
        return self.prompts_history

    def moody_chatbot(self, prompt: str):
        hm = HumanMessage(content = prompt)
        self.prompts_history.append(hm)

        if prompt.strip().lower() == "exit":
            return "Chat Ended. Thank you for the engaging conversation."

        response = self.model.invoke(self.prompts_history).content
        am = AIMessage(content = response)
        self.prompts_history.append(am)
        return response, self.prompts_history

    