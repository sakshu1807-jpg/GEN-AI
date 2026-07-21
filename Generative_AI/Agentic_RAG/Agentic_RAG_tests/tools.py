from langchain_tavily import TavilySearch
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatMistralAI(
    model_name= 'mistral-medium-latest'
)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template(
    """You're a helpful AI Assisstant, who provides the summary of news in clean, clear bullet points.
    The news is {news}"""
)

# Agent = Tool + LLM

topic = input("Enter the topic to get news on :- ")

tool = TavilySearch(
    max_results = 6,
    topic = 'news' # Category of the search
)

news_reults = tool.run(topic)

chain = prompt | model | parser

final_result = chain.invoke({'news': news_reults})
print(final_result)