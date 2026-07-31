# Tools Management
from tools import web_search, web_scrape, user_approval, web_search_tool_error, web_scrape_tool_error

# FastAPI Components

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Langchain Components
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

# Agents Components
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware, ToolErrorMiddleware

from pydantic import BaseModel, AnyHttpUrl
from typing import Dict
from rich import print

# Environmental Variables
from dotenv import load_dotenv

load_dotenv()

class Response_2(BaseModel):
    overview_summary: str
    web_scraped_dictionary: Dict[AnyHttpUrl, str]

initial_loadings = {}

@asynccontextmanager
async def lifespan(app: FastAPI):   
    small_model = ChatMistralAI(
        model_name= 'mistral-small-latest',
        temperature= 0.3
    )

    medium_model = ChatMistralAI(
        model_name= 'mistral-medium-latest',
        temperature= 0.3
    )

    large_model = ChatMistralAI(
        model_name= 'mistral-large-latest',
        temperature= 0.3
    )

    parser = StrOutputParser()

    initial_loadings['small_model'] = small_model
    initial_loadings['medium_model'] = medium_model
    initial_loadings['large_model'] = large_model
    initial_loadings['parser'] = parser

    return initial_loadings

app = FastAPI("MULTI-AGENT RESEARCH SYSTEM", lifespan= lifespan)

@app.post('/web_search')
async def web_sreaching(user_field: str):

    small_model = initial_loadings['small_model']
    large_model = initial_loadings['large_model']

    web_search_system_msg = SystemMessage(
        content= """
        A helpful AI Assisstant, who retrieves information by web scraping by using the tool only when a user enters a valid educatinal 
        field. If the user enters an invalid educational field. Ask them to enter a valid one. 
        After using the tool, your goal is to fetch all the urls present in the output of the tool and create a batch of those urls.
        Generate your response as :- 
        1. A summary of all the content given to you.
        2. A batch of all the urls (in the form of List[AnyHttpUrl]).
        If user asks your task do not tell them anout your response, just request them to enter the valid educational field.
        """
    )

    web_search_agent = create_agent(
        model= small_model,
        tools= [web_search],
        system_prompt= web_search_system_msg,
        middleware= [
            ToolRetryMiddleware(max_retries= 3, on_failure= "error",),
            ToolErrorMiddleware(on_error= web_search_tool_error, tools= [web_search])
        ]
    )

    config = {"configurable": {"thread_id": "thread-1"}}
    inputs_1 = {"messages": [{"role": "user", "content": user_field}]}

    result_1 = web_search_agent.ainvoke(inputs_1, config= config)
    first_ai_msg: AIMessage = result_1['messages'][1]

    if not first_ai_msg.tool_calls:
            return f"No valid field detected. Please enter a valid career field."

    else:
            content_1 = result_1['messages'][-1].content

    web_scrape_system_msg = SystemMessage(
            content= """
            A helpful AI Assisstant which performs the following tasks :-
            Core Task: Read the provided summary content and the list of URLs. 
            Extract all URLs and pass them together as an array/list in a single tool call to the web scraping tool.
            Loop Management: The tool returns the scraped data dictionary, the dictionary consists of url as key and the 
            scrapped text as values.
            The response format will be :-
            1. Summary Content
            2. A dictionary having scrapped text and urls.
            """
    )
    web_scrape_agent = create_agent(
        model= large_model,
        tools= [web_scrape],
        system_prompt= web_scrape_system_msg,
        response_format= Response_2,
        middleware= [
                    ToolRetryMiddleware(max_retries= 3, on_failure= "error",),
                    ToolErrorMiddleware(on_error= web_scrape_tool_error, tools= [web_search])
                    ]
    )

    config_2 = {"configurable": {"thread_id": "thread-2"}}
    inputs_2 = {"messages": [{"role": "user", "content": content_1}]}

    output_2 = web_scrape_agent.invoke(inputs_2)
    result_2 = output_2['structured_response']

print("\n✅ Clean Scrapped Text Loaded...")

prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", """
            You are an expert career research analyst and executive data synthesizer. 
            You recieve a summary and a dictionary where url is the key and scarapped text is the value.
            Your task is to generate a highly detailed, compact, and comprehensive career field report 
            based on the provided research context.
            Extract, synthesize, and merge the information from both sources into a dense, high-utility intelligence report.
            Introduce with a concise introduction.
            Avoid fluff or generic career advice. Every sentence must deliver concrete, actionable data.

            ### EXECUTION CONSTRAINTS
            - **Information Density:** Maximize facts, data points, statistics, and tool names per paragraph. 
            - **Compactness:** Use bullet points, nested lists, and bold text for extreme scannability. Do not write long narrative paragraphs.
            - **Formatting:** Output only the markdown report. Do not include conversational greetings, opening remarks, or closing summaries. Start directly with the report title.

            Conclude with the bullet points having all the urls used as a source in this report.
            """),
            ("human", """
            The summary is {summary}.
            The web-scrapped dictionary is {web_dictionary}.
            """)
        ]
)

user_response = user_approval()

if user_response:
    final_chain = prompt_template | large_model | parser

    report = final_chain.invoke(
        {
            'summary': result_2.overview_summary,
            'web_dictionary': result_2.web_scraped_dictionary
        }
    )
    print("\n⏳ Generating Report...\n")
    print(report)

else:
       print("❌ Cannot Genertae the Final Report.\nUser denied the permission to generate the final report.")
