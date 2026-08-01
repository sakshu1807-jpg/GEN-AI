import os
import requests
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from tavily import AsyncTavilyClient
from langchain_core.messages import ToolMessage
from typing import List, Dict, Any
from pydantic import AnyHttpUrl
from bs4 import BeautifulSoup

# Tool - 1 : Extracts the current data along with the URLs

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

async def get_source_data(field: str) -> List:
    """This function gets the source data from different domains regarding the career field user has entered"""
    
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

    client = AsyncTavilyClient(
        api_key= TAVILY_API_KEY,
    )

    final_query = f"""Inside the included professional career databases, educational planning portals,
                    and competitive exam boards, analyze the field of {field}.
                    Extract the definitive career paths, specific entrance or standardized exams required,
                    and the future significance/job growth outlook for this field."""
    
    raw_data = await client.search(
        query= final_query,
        search_depth= "basic",
        max_results= 3,
        include_domains= career_websites
    )

    return raw_data

@tool
async def web_search(user_field: str) -> Dict[str, Any]:
    """This tool is used to extract all the data from different sources as per the field of study given by the user
        and returns the raw dictionary of all the sources visited."""
    
    return await get_source_data(user_field)

@tool
async def web_scrape(urls: List[AnyHttpUrl]) -> Dict[AnyHttpUrl, str]:
    """This tool web scrapes the given urls to generate clean, formatted text.
        It assissts the LLM to gather textual information."""
    
    scrapped_text = {}

    for url in urls:
        try:
            response = await requests.get(url= url, timeout= 7, headers= {"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, features= "html.parser")
            for tag in soup(["script", "nav", "style", "footer"]):
                tag.decompose()

            url_text = soup.get_text(separator= ' ', strip= True)[:4000]
            scrapped_text[url] = url_text

        except Exception as error:
            return f"An error occurred as {error}"

    return scrapped_text


def user_approval() -> bool:
    """This custom middleware seeks the approval from the user to whether generate the final report or not."""

    print("\n✅ Data from Different Sources Collected.\n⏳ Waiting for confirmation to generate the report.\n")

    user_input = input("Enter YES to generate the final report :- ")

    if user_input.strip().lower() != 'yes':
        return False
    
    return True

def web_search_tool_error(exc: Exception, request) -> str | None:

    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed: {type(exc).__name__}. Fix the input and retry."

    return None

def web_scrape_tool_error(exc: Exception, request) -> str | None:

    if isinstance(exc, ConnectionError):
        return f"Tool `{request.tool_call['name']}` encountered a connection error."

    return None