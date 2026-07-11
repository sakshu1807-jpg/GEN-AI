from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

file_path = "Generative_AI/RAG/document folders/test_text.txt"
with open(file_path, 'r') as f:
    content = f.read()


docs = Document(
    page_content= content,
    metadata = {"source": file_path}
)

print(docs.page_content)
