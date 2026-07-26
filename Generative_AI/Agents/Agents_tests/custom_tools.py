from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

@tool
def news(topic: str, max_results: int) -> str:
    """This callable is used to return a news on a particular topic."""
    
    news_results = TavilySearch(
        max_results = max_results,
        topic = 'news'
    )

    return news_results.run(topic)

model = ChatMistralAI(
    model_name= 'mistral-medium-latest'
)

prompt = ChatPromptTemplate.from_template(
    """You're a helpful AI Assisstant, who provides the summary of news in clean, clear bullet points.
    The news is {news}"""
)

parser = StrOutputParser()
topic = input("Enter the topic for the news :- ")
max_points = int(input("Enter the number of related news to get :- "))

latest_news = news.invoke({'topic': topic, 'max_results': max_points})

chain = prompt | model | parser
result = chain.invoke({'news': latest_news})

print(result)
