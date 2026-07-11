from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document
from pypdf import PdfReader

load_dotenv()

file_path = r'sample_pdf.pdf'
file = PdfReader(stream = file_path).pages
pdf_file = []

for i, page in enumerate(file):
    content = page.extract_text()
    if content:
        pdf_file.append(
            Document(
                page_content = content,
                metadata = {"source": file_path, "page_num": i + 1}
            )
        )

embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

vector = Chroma.from_documents(
    documents = pdf_file, 
    embedding = embedding_model,
    persist_directory = './vector_database'
)