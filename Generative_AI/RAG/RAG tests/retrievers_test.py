from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
load_dotenv()

docs = [
    Document(page_content= "Machine learning is a subset of Artificial Intelligence", metadata = {'source': 'ML'}),
    Document(page_content= "Deep Learning is a subset of Machine Learning", metadata = {'source': 'DL'}),
    Document(page_content= "Deep Learning involves neural networks", metadata = {'source': 'NN'}),
    Document(page_content= "Machine learning is a subset of Artificial Intelligence and has various types of learning algorithms"),
    Document(page_content= "Machine Learning has various types of learning algorithms", metadata = {'source': 'LA'}),
]

embedding_model = HuggingFaceEmbeddings(
    model = 'sentence-transformers/all-MiniLM-L6-v2'
)
vector_store = Chroma.from_documents(
    documents= docs,
    embedding= embedding_model
)
# 1) First Method :- Similarity Search for retrieving the response

# similarity_ret = vector_store.as_retriever(
#     search_type = 'similarity',
#     search_kwargs = {"k": 3} # The number of similar results to return/ retrieve
# )

# print("="*60)
# print("Similarity Search Result")
# print("="*60)
# print()

# similarity_res = similarity_ret.invoke("Tell me about Machine Learning")

# for r in similarity_res:
#     print(r.page_content)

# # 2) Second Method :- MMR (Maximal Marginal Result) Search for retrieving the response

# mmr_ret = vector_store.as_retriever(
#     search_type = 'mmr',
#     search_kwargs = {"k": 3} # The number of similar results to return/ retrieve
# )

# print("="*60)
# print("Maximal Marginal Result")
# print("="*60)
# print()

# mmr_res = mmr_ret.invoke('Tell me about Machine Learning')

# for r in mmr_res:
#     print(r.page_content)

# 3) Third Method (Most Practical): Multiquery -> Generates multiple query using llm (by itself), to create multiple query so
# that it creates better context for the output

retriever = vector_store.as_retriever()

llm = ChatMistralAI(
    model = 'mistral-medium-latest'
)

multi_query_ret = MultiQueryRetriever.from_llm(
    retriever= retriever,
    llm = llm
)

query = "What is Deep Learning"
result = multi_query_ret.invoke(query)

for r in result:
    print(r.page_content)