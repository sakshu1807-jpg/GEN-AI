import os
import json
import requests
from langchain_mistralai import ChatMistralAI
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

result = get_weather.invoke({'city': 'Delhi'})

print(result)