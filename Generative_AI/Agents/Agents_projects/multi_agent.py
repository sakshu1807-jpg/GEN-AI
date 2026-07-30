from tools import web_search, web_scrape, user_approval

# Langchain Components
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

# Agents Components
from langchain.agents import create_agent
from langchain.agents.middleware import(
    SummarizationMiddleware
)
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, AnyHttpUrl
from typing import List
from rich import print

# Environmental Variables
from dotenv import load_dotenv

load_dotenv()

small_model = ChatMistralAI(
    model_name= 'mistral-small-latest'
)

medium_model = ChatMistralAI(

    model_name= 'mistral-medium-latest'
)

checkpointer = InMemorySaver()

while True:
        system_msg_1 = SystemMessage(
            content= """
            A helpful AI Assisstant, who retrieves information by web scraping by using the tool only when a user enters a valid educatinal 
            field. If the user enters an invalid educational field. Ask them to enter a valid one. 
            After using the tool, your goal is to fetch all the urls present in the output of the tool and create a batch of those urls.
            Generate your response as :- 
            1. A summary of all the content given to you.
            2. A batch of all the urls (in the form of List[AnyHttpUrl]).
            """
        )

        agent_1 = create_agent(
            model= medium_model,
            tools= [web_search],
            system_prompt= system_msg_1,
        )

        prompt = input("Enter Field :- ")
        if prompt.lower().strip() == 'exit':
                print("------------ Conversation Ended ------------")
                break
        
        config = {"configurable": {"thread_id": "thread-1"}}
        inputs_1 = {"messages": [{"role": "user", "content": prompt}]}

        result_1 = agent_1.invoke(inputs_1, config= config)
        first_ai_msg: AIMessage = result_1['messages'][1]

        if not first_ai_msg.tool_calls:
                print("No valid field detected. Please enter a valid career field.")

        else:
                content_1 = result_1['messages'][-1].content
                print("\n✅ Raw Data Collected from Sources")
                break

system_msg_2 = SystemMessage(
        content= """
        A helpful AI Assisstant which performs the following tasks :-
        Core Task: Read the provided summary content and the list of URLs. 
        Extract all URLs and pass them together as an array/list in a single tool call to the web scraping tool.
        Loop Management: The tool returns the scraped data dictionary, the dictionary consists of url as key and the 
        scrapped text as values.
        Use the provided summary and the scrapped texts to create a well formatted and clean text document.
        """
)
agent_2 = create_agent(
    model= medium_model,
    tools= [web_scrape],
    system_prompt= system_msg_2,
)

config_2 = {"configurable": {"thread_id": "thread-2"}}
inputs_2 = {"messages": [{"role": "user", "content": content_1}]}

result_2 = agent_2.invoke(inputs_2)
content_2 = result_2['messages'][-1].content
print("\n⏳ Loading clean scrapped text ...\n\n")
print(content_2)
