import os
import requests
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from tavily import TavilyClient

# Tool - 1 : Extracts the current data along with the URLs

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@tool
def get_source_data(query: str):
    """This tool is used to extract all the data from different sources as per the query given by the user
    ans returns all the urls of the source it visited or searched."""

    client = TavilyClient(
        api_key= TAVILY_API_KEY,
    )

    raw_data = client.search(
        query= query,
        search_depth= "advanced",
        max_results= 10
    )

    urls = []

    for result in raw_data['results']:
        url = result['url']

        urls.append(url)

    return urls



    