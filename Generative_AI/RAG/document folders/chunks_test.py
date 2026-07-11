from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from langchain_core.documents import Document

file_path = r'Generative_AI\RAG\document folders\sample_pdf.pdf'
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

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 80,
    chunk_overlap = 10
)

chunks = splitter.split_documents(pdf_file)

print(len(chunks))
print()
for i in range(20):
    print(chunks[i].page_content)
    print()
