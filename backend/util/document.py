import os
from core import config
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    """
    파일 저장

    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID
        document_content (str): 문서 내용
    """
    file_path = f"documents/{user_id}/{document_id}.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(document_content)


def get_user_document(user_id: str, document_id: str) -> str:
    """
    파일 읽어오기

    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID

    Returns:
        str: 파일의 content
    """
    file_path = f"documents/{user_id}/{document_id}.txt"
    with open(file_path, "r") as f:
        return f.read()


def insert_document(user_id: str, document_id: str) -> None:
    """
    Document content를 vector store에 저장

    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID
    """
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


def chunk_document(document_content: str) -> list[str]:
    """
    Document content를 청킹하여 반환

    Args:
        document_content (str): document의 content

    Returns:
        list[str]: 청킹된 문서 리스트
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_text(document_content)
