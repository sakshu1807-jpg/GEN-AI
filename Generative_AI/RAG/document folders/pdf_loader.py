from langchain_core.documents import Document
from pypdf import PdfReader

file_path = 'Generative_AI\RAG\document folders\sample_pdf.pdf'

pdf_file = PdfReader(stream = file_path)
pages = []

for i, page in enumerate(pdf_file.pages):
    content = page.extract_text()
    if content:
        pages.append(
            Document(
                page_content = content,
                metadata = {"source" : file_path, "page" : i + 1}
            )
        )

print(pages[0].page_content)
