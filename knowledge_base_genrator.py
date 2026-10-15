from pathlib import Path
import json
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

DATA_SOURCE = Path("./DataSet_College")
CHROMA_PATH = "./chromadb"

embedding_function = OllamaEmbeddings(model="nomic-embed-text")

db = Chroma(
    collection_name="college",
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function
)


def create_college_documents(data, filename):
    documents = []
    for index, item in enumerate(data, start=1):
        if isinstance(item, dict):
            page_content = (
                item.get("content")
                or item.get("text")
                or item.get("page_content")
                or json.dumps(item, ensure_ascii=False)
            )
            page_number = item.get("page_number",item.get("page", index))
        else:
            page_content = str(item)
            page_number = index
        metadata = {
            "filename": filename,
            "page_number": int(page_number)
        }
        college_document = Document(
            page_content=page_content,
            metadata=metadata
        )
        documents.append(college_document)
    return documents
all_documents = []
for document_path in DATA_SOURCE.glob("*.json"):
    print(f"Reading: {document_path.name}")
    with open(document_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if isinstance(data, dict):
        data = [data]
    info_documents = create_college_documents(data,document_path.name)
    all_documents.extend(info_documents)

if all_documents:
    db.add_documents(all_documents)
    print(f"Added {len(all_documents)} documents.")

print("Knowledge base ready!")
