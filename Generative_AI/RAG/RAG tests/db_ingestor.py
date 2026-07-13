from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain_chroma import Chroma

load_dotenv()

def db_ingestion():
    file_path = r"Generative_AI\RAG\document folders\sample_pdf.pdf"
    pdf = PdfReader(stream = file_path)
    pdf_file = []

    for i, page in enumerate(pdf.pages):
        content = page.extract_text()
        if content:
            pdf_file.append(
                Document(
                    page_content= content,
                    metadata = {"source": file_path, "page_no.": i+1}
                )
            )

    embeddings_model = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents = pdf_file,
        embedding= embeddings_model,
        persist_directory= r"./Generative_AI\RAG\document folders\chroma_db"
    )

    return vector_store

if __name__ == '__main__':
    db_ingestion()