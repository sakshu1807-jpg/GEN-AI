from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Dict
from dotenv import load_dotenv
load_dotenv()

model = ChatMistralAI(
    model_name= "mistral-medium-latest",
    temperature= 0.3
)

"""Reducer function to prevent overwriting of the nodes output"""

def reducer_func(existing: dict, updated: dict) -> Dict:
    if existing:
        return {**existing, **updated}
    return updated

class Parallel_State(TypedDict):
    raw_tweet : str
    overall_score : Annotated[Dict[str, int], reducer_func]

llm = ChatMistralAI(
    model_name= 'mistral-medium-latest',
    temperature= 0.3
)

def error_node(state: Parallel_State):

    prompt = f"""
    Act as an expert grammar coach and editor. Analyze the paragraph below for spelling, punctuation, tense consistency, and grammatical errors. 

    Provide your response in this exact structure:
    Grammar Rating: [Score out of 5, where 5 is completely error-free] only.

    Paragraph to analyze:
    {state['raw_tweet']}
        """
    response = model.invoke(prompt)
    score = response.content
    return {
        'overall_score': {'Error_Analyzer': score}
    }

def creative_node(state: Parallel_State):

    prompt = f"""
    Act as an expert creative writing coach and literary critic. Analyze the paragraph below specifically for creativity, use of literary devices, flow, and original style.

    Provide your response in this exact structure:
        Creativity Rating: [Score out of 5, where 5 is highly inventive, evocative, and original] only.

    Paragraph to analyze:
    {state["raw_tweet"]}
        """
    response = model.invoke(prompt)
    score = response.content
    return {
            'overall_score': {'Creativity_Analyzer': score}
        }

def factual_node(state: Parallel_State):

    prompt = f"""
    Act as an expert fact-checker and researcher. Analyze the paragraph below for factual accuracy, misrepresentations, myths, or unsupported claims based on verified, consensus-backed information as of 2026.

    Provide your response in this exact structure:
    Factuality Rating: [Score out of 5, where 5 is completely accurate, truthful, and verified] only.

    Paragraph to analyze:
    {state["raw_tweet"]}
        """
    response = model.invoke(prompt)
    score = response.content
    return {
            'overall_score': {'Factuality_Analyzer': score}
        }

graph = StateGraph(Parallel_State)

graph.add_node("error_checker", error_node)
graph.add_node("creativity_checker", creative_node)
graph.add_node("factuality_checker", factual_node)

graph.add_edge(START, "error_checker")
graph.add_edge(START, "creativity_checker")
graph.add_edge(START, "factuality_checker")

graph.add_edge("error_checker", END)
graph.add_edge("creativity_checker", END)
graph.add_edge("factuality_checker", END)

app = graph.compile()

para = "The heavy, sapphire-blue blanket of night whispered secrets to the sleeping desert, " \
"and the stars danced like scattered diamonds on black velvet. " \
"Venus, which is the closest planet to Earth, shined bright in the sky while a lone wolf howls at the moon. " \
"The quietness of the dunes was beautiful, but the desert can be dangerous because cobras, " \
"which are native only to South America, hunts silently in the dark sand."

result = app.invoke({
    "raw_tweet": para
})

print(result["overall_score"])