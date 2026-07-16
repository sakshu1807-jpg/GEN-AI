import os
import chromadb
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_chroma import Chroma
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from utils import file_input
from dotenv import load_dotenv
load_dotenv()

session = {}

@asynccontextmanager
async def data_lifespan(app: FastAPI):
    yield
    session.clear()
    
app = FastAPI(lifespan= data_lifespan)

def get_chat_model():
    if 'chat_model' not in session:
        session['chat_model'] = ChatMistralAI(
            model_name="mistral-medium-latest", 
            temperature=0.45, 
            api_key=os.getenv("MISTRAL_API_KEY")
        )
    return session['chat_model']

def get_embedding_model():
    if 'embedding_model' not in session:
        session['embedding_model'] = GoogleGenerativeAIEmbeddings(
            model='gemini-embedding-001',
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    return session['embedding_model']

def get_chroma_client():
    if 'chroma_client' not in session:
        session['chroma_client'] = chromadb.EphemeralClient()
    return session['chroma_client']

@app.get("/keep-alive")
async def keep_alive():
    return {"status": "alive", "message": "Keeping the gears turning!"}

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):

    file_name = file.filename.lower().strip()
    ext = file_name.split('.')[-1]
    documents = await file_input(file)
    if documents:
        try:
            vector_store = await Chroma.afrom_documents(
                documents= documents,
                embedding= session.get('embedding_model'),
                client= session.get('chroma_client')
            )

            session['vector_store'] = vector_store
            session['chat_history'] = []

            return {
                'Result': "Success",
                'Message': f"{ext.upper()} file successfully analyzed. Ask your questions/doubts now."
            }
        
        except Exception as error:
            raise HTTPException(status_code= 500, detail= str(error))
        
class Request(BaseModel):
    question: str

class Response(BaseModel):
    response: str

@app.post('/chat', response_model= Response)
async def chatbot(request: Request):

    try:
        model: ChatMistralAI = session['chat_model']
        vector_store: Chroma = session['vector_store']
        chat_history = session['chat_history']
        base_retriever = vector_store.as_retriever()

        query_retriever = MultiQueryRetriever.from_llm(
            retriever= base_retriever,
            llm= model
        )

        retrieved_docs = await query_retriever.ainvoke(request.question)
        context = '\n'.join([doc.page_content for doc in retrieved_docs])

        system_message = SystemMessage(f"""You are a helpful and knowledgeable AI assistant. 
        Your task is to answer user queries based strictly on the provided context retrieved from the documents.
        Answer the user's query using ONLY the pieces of context provided in the `<context>` blocks below.
        If the answer cannot be found in the provided context, state clearly: "I cannot find the answer to that in the provided documents." 
        Do not try to make up an answer, just give a jist of the question asked by the user and remind the user to ask from the document only.
        Keep your answers conversational, accurate, and directly relevant to the user's question.
        The context is {context}""")

        session['chat_history'].append(HumanMessage(request.question))
        final_prompt = [system_message] + chat_history
    
        answer = await model.ainvoke(final_prompt)
        session['chat_history'].append(AIMessage(answer.content))
        return Response(response = answer.content)
    
    except Exception as error:
        raise HTTPException(status_code= 404, detail= str(error))
    
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)