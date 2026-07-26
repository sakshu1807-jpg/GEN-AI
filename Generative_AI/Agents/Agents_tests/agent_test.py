from langchain.agents import create_agent
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.middleware import (
    LLMToolSelectorMiddleware, 
    SummarizationMiddleware,
    HumanInTheLoopMiddleware)
from dotenv import load_dotenv
from rich import print

load_dotenv()

model_medium = ChatMistralAI(
    model_name= 'mistral-medium-latest'
)
summary_model = ChatMistralAI(
    model_name= 'mistral-small-latest',

)

@tool
def get_eligibility(age: int) -> str:
    """This tool checks the eligibility if the candidate is eligible to vote according to it's age."""

    if age < 18:
        return "You are not eligible."
    
    return "You are eligible"

@tool
def get_weather(location: str) -> str:
    """This tool returns the weather status of the entered location."""

    return f"It's raining in {location}"

@tool
def get_greeting(name: str) -> str:
    "This tool returns a greeting message to the user."

    return f"Hello and Welcome {name}"

@tool
def email_send(recipient_name: str, sender_name: str, context: str) -> str:
    """This tool uses a llm to generate an email message including to, from and the body of the email."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', """
            An AI assisstant who generates the email body based on the context provided
            along with the 'to' and 'from' elements."""),
            ('human', """
            To: {recipient_name}, From: {sender_name}, context: {context}""")
        ]
    )
    chain = prompt | model_medium
    result = chain.invoke({
        'recipient_name': recipient_name,
        'sender_name': sender_name,
        'context': context
    })

    return result

agent = create_agent(
    model= model_medium,
    tools= [get_eligibility, get_weather, get_greeting, email_send],
    system_prompt= 'You are a helpful AI assisstant.',
    middleware= [
        LLMToolSelectorMiddleware(
        model= model_medium,
        system_prompt= "An AI assisstent, which selects the relevent tool before sending to the main model.",
        max_tools= 2,
        always_include= [get_greeting]
        ),
        SummarizationMiddleware(
            model= summary_model,
            trigger= [
                ("tokens", 2000),
                ("messages", 6)
            ],
            keep= ("messages", 15)
        ),
        HumanInTheLoopMiddleware(
            
        )
    ]
)

prompt = input("Enter the prompt :- ")
inputs = {"messages": [{"role": "user", "content": prompt}]}

result = agent.invoke(inputs)
answer = result['messages'][-1].content
print(answer)