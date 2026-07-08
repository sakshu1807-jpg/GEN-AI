from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={"trust_remote_code": True} 
)
content = [
    "Hello, My name is Saksham.",
    "It's raining heavily today.",
    "All the streets are filled with water."
]

embed_vector = embedding.embed_documents(content)

print("Embeddings created successfully")
print(f"\nLength of the embedding is: {len(embed_vector)}")
print(f"\n{embed_vector[:5]}")