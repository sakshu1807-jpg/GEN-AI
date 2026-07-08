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

model = ChatMistralAI(
    model = "mistral-medium-latest",
    temperature= 0.6,
)

print("Enter your choice for the tone of response by the model :- ")
print("1. Funny Jarvis\n2. Angry Jarvis\n3. Depressed Jarvis\n4. Straight to the point")

choice = int(input("Enter the option :- "))

if choice == 1:
    mode = "You are a funny large language model, replying with jokes and humour"
elif choice == 2:
    mode = "You are an angry AI, and responds with aggression"
elif choice == 3:
    mode = "You are a depressed and sad AI, replying every answer with sadness and grief"
else:
    mode = "You are a large language model who answers straight to the point"

prompts = [
    SystemMessage(mode)
]
while True:
    prompt = input("You : ")
    hm = HumanMessage(content = prompt)
    prompts.append(hm)

    if prompt.strip().lower() == "exit":
        print("\nChat Ended. Thank you for the engaging conversation.")
        break

    response = model.invoke(prompts)
    am = AIMessage(content = response.content)
    prompts.append(am)
    print("Jarvis : ", response.content)

    