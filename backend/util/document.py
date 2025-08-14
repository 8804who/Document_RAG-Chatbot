import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from core import config
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings

OPENAI_EMBEDDING_MODEL = config.OPENAI_EMBEDDING_MODEL
CHUNK_SIZE = config.CHUNK_SIZE
CHUNK_OVERLAP = config.CHUNK_OVERLAP
CHROMA_DB_PATH = config.CHROMA_DB_PATH
COLLECTION_NAME = config.COLLECTION_NAME

embedding_model = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embedding_model,
    persist_directory=CHROMA_DB_PATH,
)


def save_user_document(user_id: str, document_id: str, document_content: str) -> None:
    file_path = f"documents/{user_id}/{document_id}.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(document_content)


def get_user_document(user_id: str, document_id: str) -> str:
    file_path = f"documents/{user_id}/{document_id}.txt"
    with open(file_path, "r") as f:
        return f.read()


def insert_document(user_id: str, document_id: str) -> None:
    documents = []
    document_content = get_user_document(user_id, document_id)
    for chunk in chunk_document(document_content):
        documents.append(
            Document(
                page_content=chunk,
                metadata={"user_id": user_id, "document_id": document_id},
            )
        )
    vector_store.add_documents(documents)
    vector_store.persist()


def chunk_document(document_content: str) -> None:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_text(document_content)
    return chunks
