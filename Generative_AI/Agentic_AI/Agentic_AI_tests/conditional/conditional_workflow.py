from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import Literal, Dict, TypedDict
from pdf_extractor import pdf_embedding_creator
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
load_dotenv()

class ConditionalState(TypedDict):
    query: str
    selected_domain: str
    result: str

def model_initializer() -> ChatGroq:
    model = ChatGroq(
            model= "openai/gpt-oss-120b",
            temperature= 0.45
        )
    return model

def best_context_retriever(filename: str) -> str:
    model = model_initializer()
    file_name = filename

    vector_store = pdf_embedding_creator(filename= file_name)
    retriever = vector_store.as_retriever()

    multi_queries = MultiQueryRetriever.from_llm(
        llm= model,
        retriever= retriever
    )

    retrieved_docs = multi_queries.invoke(ConditionalState['query'])
    context = [doc.page_content for doc in retrieved_docs]
    return ' '.join(context)

def classifier_node(state: ConditionalState) -> Dict:

    prompt = "You are a helpful AI assisstant who helps the further agents to know which task to proceed with."\
        "# Input :- "\
        "You will recieve a query from the user, your task is to classify whether the query relates to `egypt_node' or `quantum_node` or `none`"\
        "You will give the output out of the three choices only."\
        f"The user query is :- {state['query']}"
    
    model = model_initializer()

    response = model.invoke(prompt).content
    category = 'none'

    if 'quantum' in response:
        category = 'quantum_node'
    elif 'egypt' in response:
        category = 'egypt_node'
    else:
        category = 'none'
    return {
        "selected_domain": category
    }

def router(state: ConditionalState) -> Literal['quantum', 'egypt', 'none']:

    domain = state['selected_domain']
    if domain == 'quantum_node':
        return 'quantum'
    elif domain == 'egypt_node':
        return 'egypt'
    
    return 'none'

# creating the nodes 
def quantum_node(state: ConditionalState) -> Dict:
    filename = "quantum_computing_guide.pdf"
    context = best_context_retriever(filename= filename)

    prompt = f"""Answer the user's query using only the retrieved context. Be concise, accurate, and direct. 
    Do not invent information. If the context is insufficient or conflicting, state this clearly.
    The retrieved context is :-
    {context}
    The user query is :- {state['query']}
"""
    model = model_initializer()

    response = model.invoke(prompt)
    return {
        'result': response.content
    }

def egypt_node(state: ConditionalState) -> Dict:
    filename = "ancient_egyptian_mythology.pdf"
    context = best_context_retriever(filename= filename)

    prompt = f"""Answer the user's query using only the retrieved context. Be concise, accurate, and direct. 
    Do not invent information. If the context is insufficient or conflicting, state this clearly.
    The retrieved context is :-
    {context}
    The user query is :- {state['query']}
"""
    model = model_initializer()

    response = model.invoke(prompt)
    return {
            'result': response.content
        }

def llm_node(state: ConditionalState) -> Dict:

    model = model_initializer()
    prompt = f"""
You are a helpful, friendly, and reliable AI chatbot. Understand the user's intent and provide clear, accurate, and relevant responses. 
Answer directly in a natural, conversational tone, adding explanation when useful. 
If unsure, be honest, ask clarifying questions when needed, and prioritize helpfulness, accuracy, and safety.

The user query is :- {state['query']}
"""
    response = model.invoke(prompt)
    return {
            'result': response.content
        }

graph = StateGraph(ConditionalState)

graph.add_node("classifier", classifier_node)
graph.add_node("quantum", quantum_node)
graph.add_node("egypt", egypt_node)
graph.add_node("none", llm_node)

graph.add_edge(START, "classifier")
graph.add_conditional_edges("classifier", router)
graph.add_edge("quantum", END)
graph.add_edge("egypt", END)
graph.add_edge("none", END)

app = graph.compile()

print("Note :- Type `end` to conclude the conversation.")
while True:

    question = input("You :- ")
    if question.lower().strip() == 'end':
        break
    result = app.invoke({
        "query": question
    })
    print("Bot :- ", result["result"])