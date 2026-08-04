# Tools Management
from tools import web_search, web_scrape,    web_search_tool_error, web_scrape_tool_error

# FastAPI Components
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel, AnyHttpUrl, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from rich import print

# Langchain Components
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import Runnable

# Agents Components
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware, ToolErrorMiddleware

# Environmental Variables
from dotenv import load_dotenv

load_dotenv()

class Response_2(BaseModel):
    overview_summary: str = Field(description= "The overview summary of the total content")
    web_scraped_dictionary: Dict[AnyHttpUrl, str] = Field(description= "The dictionary where urls are keys and the text scraped are the values.")

initial_loadings = {}
messages = []

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

    groq_model = ChatGroq(
        model= 'llama-3.1-8b-instant',
        temperature= 0.3
    )

    parser = StrOutputParser()

    initial_loadings['small_model'] = small_model
    initial_loadings['medium_model'] = medium_model
    initial_loadings['groq_model'] = groq_model
    initial_loadings['parser'] = parser

    yield
    messages = []
    initial_loadings.clear()

app = FastAPI(title="MULTI-AGENT RESEARCH SYSTEM", lifespan= lifespan)

report_to_groq: str = ''

@app.post('/research_report')
async def research_report(user_field: str, user_response: bool = True):

    # -------------- AGENT 1 --------------

    small_model: ChatMistralAI = initial_loadings['small_model']
    medium_model: ChatMistralAI = initial_loadings['medium_model']
    parser: StrOutputParser = initial_loadings['parser']

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

    result_1 = await web_search_agent.ainvoke(inputs_1, config= config)
    first_ai_msg: AIMessage = result_1['messages'][1]

    if not first_ai_msg.tool_calls:
        return AIMessage(
            content= "Ready to generate your deep-dive topic report! " \
            "But please enter a valid eductional field below. " 
        )
    last_ai_msg: AIMessage = result_1['messages'][-1]
    content_1 = last_ai_msg.content

    print("\n✅ Data Collected From Different Sources")

    # -------------- AGENT 2 --------------

    web_scrape_system_msg = SystemMessage(
            content= """
            You are a web extraction assistant.
            Extract all URLs from the provided text and pass them to the web_scrape tool.
    
            CRITICAL: 
            - Output ONLY the raw JSON object of the tool output where urls are the keys and the scaped text as values.
            - Do NOT include any intro text, conversational filler, or trailing explanations.
            - Do NOT wrap the JSON in markdown code blocks.
            """
    )

    web_scrape_agent = create_agent(
        model= medium_model,
        tools= [web_scrape],
        system_prompt= web_scrape_system_msg,
        middleware= [
                    ToolRetryMiddleware(max_retries= 3, on_failure= "error",),
                    ToolErrorMiddleware(on_error= web_scrape_tool_error, tools= [web_scrape])
                    ]
    )

    config_2 = {"configurable": {"thread_id": "thread-2"}}
    inputs_2 = {"messages": [{"role": "user", "content": content_1}]}

    output_2 = await web_scrape_agent.ainvoke(inputs_2, config_2)
    result_2: AIMessage = output_2['messages'][-1]

    print("\n✅ Clean Scrapped Text Loaded...")

    prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", """
                You are an expert career research analyst and executive data synthesizer. 
                You recieve a JSON Object having a dictionary where url is the key and scarapped text is the value.
                Your task is to generate a highly detailed, compact, and comprehensive career field report 
                based on the provided research context.
                Extract, synthesize, and merge the information from all sources into a dense, high-utility intelligence report.
                Introduce with a concise introduction.
                Avoid fluff or generic career advice. Every sentence must deliver concrete, actionable data.

                ### EXECUTION CONSTRAINTS
                - **Information Density:** Maximize facts, data points, statistics, and tool names per paragraph. 
                - **Compactness:** Use bullet points, nested lists, and bold text for extreme scannability. Do not write long narrative paragraphs.
                - **Formatting:** Output only the markdown report. Do not include conversational greetings, opening remarks, or closing summaries. Start directly with the report title.

                Conclude with the bullet points having all the urls used as a source in this report.
                """),
                ("human", """
                Your research context is {json_object}.
                """)
            ]
    )

    if user_response:
        final_chain: Runnable = prompt_template | medium_model | parser

        report = await final_chain.ainvoke(
            {
                'json_object': result_2.content
            }
        )
        print("\n⏳ Generating Report...\n")
        report_to_groq = report_to_groq + report
        return report

    else:
        return "❌ Cannot Genertae the Final Report.\nUser denied the permission to generate the final report."

groq_sys_msg = SystemMessage(
        content= f"""You're a helpful AI Assisstant. You answers the user's questions strictly
        under the provided context. You will be given a report regarding a particular field of study.
        The report context is {report_to_groq}"""
    )

@app.post('/chat_model')
async def chat_for_report(user: str) -> str:

    question = HumanMessage(
            content= user
        )
    messages.append(question)
    chat_history = messages

    groq_model: ChatGroq = initial_loadings['groq_model']
    final_prompt = [groq_sys_msg] + chat_history

    try:
        response = await groq_model.ainvoke(final_prompt)
        ai_response = AIMessage(content= response.content)
        messages.append(ai_response)

        return ai_response
    
    except Exception as error:
        return f"An error occurred as {error}"

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)