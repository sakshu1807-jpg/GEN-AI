from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import List, Dict, TypedDict
from pdf_extractor import pdf_embedding_creator
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
load_dotenv()

class ConditionalState(TypedDict):
    query: str
    result: str

def model_initializer() -> ChatGroq:
    model = ChatGroq(
            model= "openai/gpt-oss-120b",
            temperature= 0.45
        )
    return model

def best_context_retriever(filename: str, state: ConditionalState) -> str:
    model = model_initializer()
    file_name = filename

    vector_store = pdf_embedding_creator(filename= file_name)
    retriever = vector_store.as_retriever()

    multi_queries = MultiQueryRetriever.from_llm(
        llm= model,
        retriever= retriever
    )

    retrieved_docs = multi_queries.invoke(state['query'])
    context = [doc.page_content for doc in retrieved_docs]
    return ' '.join(context)

def router(state: ConditionalState) -> str:
    prompt = "You are a helpful AI assisstant who helps the further agents to know which task to proceed with."\
    "# Input :- "\
    "You will recieve a query from the user, your task is to classify whether the query relates to `egypt_node' or `quantum_node` or `none`"\
    "You will give the output out of the three choices."\
    f"The user query is :- {state['query']}"

    model = model_initializer()

    response = model.invoke(prompt)
    return response.content

# creating the nodes 
def quantum_node(state: ConditionalState) -> str:
    filename = "quantum_computing_guide.pdf"
    context = best_context_retriever(filename= filename)

    prompt = f"{context}"
    model = model_initializer()

    response = model.invoke(prompt)
    return response.content

def egypt_node(state: ConditionalState) -> str:
    filename = "ancient_egyptian_mythology.pdf"
    context = best_context_retriever(filename= filename)

    prompt = f"{context}"
    model = model_initializer()

    response = model.invoke(prompt)
    return response.content

def llm_node(state: ConditionalState):

    model = model_initializer()
    prompt = ""
    response = model.invoke(prompt)
    return response.content

graph = StateGraph(ConditionalState)

graph.add_node("quantum_node", quantum_node)
graph.add_node("egypt_node", egypt_node)
graph.add_node("none", llm_node)

graph.add_conditional_edges(START, router)
graph.add_edge(router, END)

app = graph.compile()
question = ""
result = app.invoke({
    "query": question
})
print(result["result"])