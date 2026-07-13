from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi import FastAPI, UploadFile
from typing import List, Dict
load_dotenv()

"""
Workflow of RAG Application :-
Phase 1: (in the db_loader.py)
Document -> Docs Loader -> Creation of Chunks -> Embeddings -> Vector Storage
Phase 2:
User Query (Prompt_by_user) -> Embedding of query -> Searching in the Vector Store -> Retrieved Docs + Query
(for multi query and context development) -> Prompt(by_machine) -> LLM -> response
"""
# Fetching the chroma_db embeddings
embedding_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    embedding_function= embedding_model,
    persist_directory= r'Generative_AI\RAG\RAG project\chroma_db'
)

# Creating the retriver class to slect top 5 relevent docs

retriever = vector_store.as_retriever()

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            'system',"""
You are a helpful and knowledgeable AI assistant. 
Your task is to answer user queries based strictly on the provided context retrieved from the documents.
Answer the user's query using ONLY the pieces of context provided in the `<context>` blocks below.
If the answer cannot be found in the provided context, state clearly: "I cannot find the answer to that in the provided documents." 
Do not try to make up an answer or use outside knowledge.
Keep your answers conversational, accurate, and directly relevant to the user's question.
"""
        ),
        (
            'human',"""
Context : {context}
User Query : {question}
"""
        )
    ]
)

print("="*60)
print("Local RAG Application")
print("="*60)
print("\nType 0 to end the conversation.")

chat_model = ChatMistralAI(model = 'mistral-medium-latest', temperature=0.1)
queries = MultiQueryRetriever.from_llm(
    retriever= retriever,
    llm = chat_model
)

while True:
    question = input("User :- ")
    if question == '0':
        print("Thank you for visiting!!")
        break
    retrieved_docs = queries.invoke(question)
    context = [doc.page_content for doc in retrieved_docs]

    final_prompt = prompt_template.invoke({
        "context": context,
        "question": question
    })

    response = chat_model.invoke(final_prompt).content

    print(f"Bot :- {response}")