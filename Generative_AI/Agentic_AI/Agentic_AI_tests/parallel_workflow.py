from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Dict
from dotenv import load_dotenv
load_dotenv()

model = ChatMistralAI(
    model_name= "mistral-medium-latest",
    temperature= 0.3
)

def reducer_task():
    
class Parallel_State(TypedDict):
    raw_tweet : str
    total_score : Annotated[Dict[str, int], reducer_task]