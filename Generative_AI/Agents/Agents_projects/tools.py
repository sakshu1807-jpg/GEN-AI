import os
import requests
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from tavily import TavilyClient
from langchain_core.messages import ToolMessage

# LLm for grounding the user query
from langchain_mistralai import ChatMistralAI

# Tool - 1 : Extracts the current data along with the URLs

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

@tool
def get_source_data(user_field: str):
    """This tool is used to extract all the data from different sources as per the field of study given by the user
    ans returns all the content along with the urls of the source it visited or searched."""

    llm = ChatMistralAI(
        model_name= 'mistral-small-latest',
        api_key= MISTRAL_API_KEY
    )
    
    career_websites = [
        "onetonline.org",
        "careeronestop.org",
        "mindler.com",
        "sarvgyan.com",
        "edumilestones.com",
        "collegeboard.org",
        "mba.com",
        "ets.org",
        "glassdoor.com",
        "linkedin.com"
    ]

    client = TavilyClient(
        api_key= TAVILY_API_KEY,
    )

    final_query = f"""Inside the included professional career databases, educational planning portals,
                    and competitive exam boards, analyze the field of {user_field}.
                    Extract the definitive career paths, specific entrance or standardized exams required,
                    and the future significance/job growth outlook for this field."""
    
    raw_data = client.search(
        query= final_query,
        search_depth= "advanced",
        max_results= 10,
        include_domains= career_websites
    )

    return raw_data

@wrap_tool_call
def user_approval(request, handler):
    """This custom middleware seeks the approval from the user to whether geenrate the final report or not."""

    print(" ✅ Data from Different Sources Collected.\n")

    user_input = input("Enter YES to generate the final report")

    if user_input.strip().lower() != 'yes':
        return ToolMessage(
            content= "User denied to generate the final report."
        )
    
    return handler(request)



    