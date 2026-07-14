from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from pypdf import PdfReader

file_path = r'Generative_AI\RAG\RAG project\LLM2024.pdf'

pdf = PdfReader(file_path)
pdf_file = []

for i, page in enumerate(pdf.pages):
    content = page.extract_text()
    if content:
        pdf_file.append(
            Document(
                page_content= content,
                metadata = {
                    "source" : "Transformers pdf from Stanford",
                    "page_no." : i+1
                }
            )
        )

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 900,
    chunk_overlap = 300
)
# Creation of chunks
chunks = splitter.split_documents(pdf_file)

embedding_model = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)

vector_store = Chroma.from_documents(
    documents= chunks,
    embedding= embedding_model,
    persist_directory= r'Generative_AI\RAG\RAG project\chroma_db'
)