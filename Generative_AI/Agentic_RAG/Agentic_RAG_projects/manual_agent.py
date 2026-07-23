import os
import requests
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from tavily import TavilyClient
from rich import print
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """This tool returns the weathher details of a city"""

    weather_api = os.getenv('OPENWEATHER_API_KEY')
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weather_api}"

    geo_response = requests.get(url = geo_url)
    geo_data = geo_response.json()

    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']
    
    weather_url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        "units": "metric",
        "lang": "en",
        "appid": weather_api
    }
    weather_response = requests.get(url = weather_url, params= params)
    weather_data = weather_response.json()

    if weather_data.get('cod') != 200:
        return "Couldn't fetch the live weather data"
    
    return weather_data

@tool
def get_latest_news(city: str) -> str:
    """This tool returns the latest news of the city"""
    query = f'Latest news of {city}'
    tavily_api = os.getenv('TAVILY_API_KEY')
    client = TavilyClient(api_key = tavily_api)

    news_data = client.search(
        query= query,
        max_results= 4,
        search_depth= 'basic'
    )

    return news_data

model = ChatMistralAI(
    model_name = 'mistral-medium-latest'
)
parser = StrOutputParser()

messages = []

tools = {
    'get_latest_news': get_latest_news,
    'get_weather': get_weather
}

model_with_tools = model.bind_tools([get_weather, get_latest_news])

print("-"*50)
print("Tool Filled AI")
print("-"*50)
print("\nEnter 'exit' to end the conversation")

while True:
    user_input = input('You :- ')
    if user_input.lower().strip() == 'exit':
        print("\nConversation Ended")
        break

    messages.append(HumanMessage(user_input)) # Human Message

    result = model_with_tools.invoke(messages)
    messages.append(result) # AI Message

    if not result.tool_calls:
        answer = parser.parse(result.content)
        print("Bot :- ", answer)

    else:
        for tool_call in result.tool_calls:
            tool_name = tool_call['name']
            tool_selected = tools[tool_name]

            tool_result = tool_selected.invoke(tool_call)
            messages.append(tool_result) # Tool Message

        final_result = model_with_tools.invoke(messages) # AI Message
        answer = parser.parse(final_result.content)
        print(answer)