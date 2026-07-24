from langchain.agents import create_agent
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain.agents.middleware import wrap_tool_call, LLMToolSelectorMiddleware
from dotenv import load_dotenv
from rich import print

load_dotenv()

model = ChatMistralAI(
    model_name= 'mistral-medium-latest'
)

@tool
def get_eligibility(age: int) -> str:
    """This function checks the eligibility if the candidate is eligible to vote according to it's age."""

    if age < 18:
        return "You are not eligible."
    
    return "You are eligible"

@tool
def get_weather(location: str) -> str:
    """This function returns the weather status of the entered location."""

    return f"It's raining in {location}"

agent = create_agent(
    model= model,
    tools= [get_eligibility, get_weather],
    system_prompt= 'You are a helpful AI assisstant.',
    middleware= LLMToolSelectorMiddleware(
        model= model,
        system_prompt= "An AI assisstent, which selects the relevent tool before sending to the main model.",
        max_tools= 1
    )
)

prompt = input("Enter the prompt :- ")
inputs = {"messages": [{"role": "user", "content": prompt}]}

result = agent.invoke(inputs)
answer = result['messages'][-1].content
print(answer)