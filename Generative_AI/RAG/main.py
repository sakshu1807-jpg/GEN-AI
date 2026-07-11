from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from pypdf import PdfReader
load_dotenv()

# For text file handling

# prompt_template_1 = ChatPromptTemplate([
#         ("system","""
#     You are an AI Agent which generates a summary of the text file data given to you.
#     Include the introductory part as well, and do not ask further questions. Just give the summary.
#     """),
#         ("human","""
#     Here is the data:
#     {data}
#     """)
#     ])
# try:
#     model = ChatMistralAI(
#         model = "mistral-medium-latest",
#         temperature = 0.4
#     )

#     file_path = "Generative_AI/RAG/document folders/test_text.txt"
#     with open(file_path, 'r') as f:
#         content = f.read()

#     docs = Document(
#         page_content= content,
#         metadata = {"source": file_path}
#     )
#     prompt = prompt_template_1.invoke({"data" : docs})

#     response = model.invoke(prompt).content
#     print(response)

# except Exception as error:
#     print(f"An error occurred as {error}")

# For pdf file handling

prompt_template_2 = ChatPromptTemplate([
        ("system","""
    You are an AI Agent which generates a summary of the content of the pdf file along with the page number in the metadata given to you.
    Include the introductory part as well, and do not ask further questions. Just give the summary.
    """),
        ("human","""
    Here is the content:
    {file_data}
    """)
    ])

try:
    model = ChatMistralAI(
        model = "mistral-medium-latest",
        temperature = 0.4
    )

    file_path = r"Generative_AI\RAG\document folders\sample_pdf.pdf"
    pdf_file = PdfReader(stream = file_path)
    pages = []

    for i, page in enumerate(pdf_file.pages):
        content = page.extract_text()
        if content:
            pages.append(
                Document(
                    page_content = content,
                    metadata = {"source" : file_path, "page_number" : i + 1}
                )
            )
    
    prompt = prompt_template_2.invoke({'file_data' : pages})
    response = model.invoke(prompt).content
    print(response)

except Exception as error:
    print(f"An error occurred as {error}") 