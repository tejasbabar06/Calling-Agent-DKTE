from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embedding_function = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(
    collection_name="college",
    persist_directory="./chromadb",
    embedding_function=embedding_function
)

query = "Fee Of AIML Department"

documents = db.similarity_search(query=query,k=3)

for document in documents:
    print(f"Document : {document}")
    print("-"*80)
