from tools import get_source_data, user_approval

# Langchain Components
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

# Agents Components
from langchain.agents import create_agent
from langchain.agents.middleware import(
    LLMToolSelectorMiddleware,
    SummarizationMiddleware
)
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, AnyHttpUrl
from typing import List

# Environmental Variables
from dotenv import load_dotenv

load_dotenv()

class Response(BaseModel):

    summary_content: str
    urls: List[AnyHttpUrl]

small_model = ChatMistralAI(
    model_name= 'mistral-small-latest'
)

medium_model = ChatMistralAI(

    model_name= 'mistral-medium-latest'
)

system_msg_1 = SystemMessage(
    content= """
    A helpful AI Assisstant, who recieves a raw data of the sources from the tool. Your goal is to fetch all 
    the urls present in the output of the tool and create a batch of those urls.
    Generate your response as :- 
    1. A summary of all the content given to you.
    2. A batch of all the urls.
    """
)


agent_1 = create_agent(
    model= medium_model,
    tools= [get_source_data],
    system_prompt= system_msg_1,
    checkpointer= InMemorySaver(),
    middleware= [user_approval]
)

you = input("You :- ")
urls = agent_1.invoke(you)
