import os
from pypdf import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from typing import List



pdf_file = []
def pdf_embedding_creator(filename: str) -> Chroma:

    file_path = r"Generative_AI\Agentic_AI\Agentic_AI_tests\conditional"
    embedding_model = GoogleGenerativeAIEmbeddings(
            model= "gemini-embedding-001"
        )

    file_name = os.path.join(file_path, filename)
    pdf = PdfReader(file_name)

    for i, page in enumerate(pdf.pages):
        content = page.extract_text()
        if content:
            pdf_file.append(Document(
                page_content= content, 
                metadata = {"page_number": i+1}
            ))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size= 90,
        chunk_overlap= 30
    )

    chunks: List[Document] = splitter.split_documents(pdf_file)
    vector_store = Chroma.from_documents(
        documents= chunks,
        embedding = embedding_model
    )

    return vector_store