import os
import requests
from httpx import HTTPStatusError
from langchain.tools import tool
from tavily import AsyncTavilyClient
from langchain_core.messages import ToolMessage
from typing import List, Dict, Any
from pydantic import AnyHttpUrl
from bs4 import BeautifulSoup

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

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
                    and competitive exam boards, analyze the field of {field} and provide the career roadmap.
                    Extract the definitive career paths, specific entrance or standardized exams required,
                    and the future significance/job growth outlook for this field."""
    
    raw_data = await client.search(
        query= final_query,
        search_depth= "advanced",
        max_results= 6,
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
    i = 1
    for url in urls:
        try:
            response = requests.get(url= url, timeout= 7, headers= {"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, features= "html.parser")
            for tag in soup(["script", "nav", "style", "footer"]):
                tag.decompose()

            url_text = soup.get_text(separator= ' ', strip= True)[:2000]
            scrapped_text[url] = url_text
            print(f"URL : {i} successfully scraped.")
            i += 1

        except Exception as error:
            return f"An error occurred as {error}"

    return scrapped_text

def web_search_tool_error(exc: Exception, request) -> str | None:

    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed: {type(exc).__name__}. Fix the input and retry."

    return None

def web_scrape_tool_error(exc: Exception, request) -> str | None:

    if isinstance(exc, ConnectionError):
        return f"Tool `{request.tool_call['name']}` encountered a connection error."
    elif isinstance(exc, HTTPStatusError) and HTTPStatusError:
        return f"Tool `{request.tool_call['name']}` encountered a"
    return None