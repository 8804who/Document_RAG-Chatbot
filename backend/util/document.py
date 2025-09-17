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


def save_user_document_to_file(
    user_id: str, document_id: str, document_content: str
) -> None:
    """
    파일 저장

    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID
        document_content (str): 문서 내용
    """
    file_path = f"documents/{user_id}/{document_id}.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(document_content)


def read_user_document_from_file(user_id: str, document_id: str) -> str:
    """
    파일 읽어오기

    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID

    Returns:
        str: 파일의 content
    """
    file_path = f"documents/{user_id}/{document_id}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_user_documents_from_vector_store(user_id: str) -> list[str]:
    """
    사용자의 문서 목록 조회

    Args:
        user_id (str): 사용자 ID

    Returns:
        list[dict]: 문서 메타데이터 리스트
    """
    documents = vector_store._collection.get(
        where={"user_id": user_id}, include=["metadatas", "documents"]
    )
    parsed_document_metadatas = parse_document_metadata(documents)
    return parsed_document_metadatas


def parse_document_metadata(document_metadatas: list[dict]) -> list[dict]:
    """
    문서 메타데이터 파싱

    Args:
        document_metadatas (list[dict]): 문서 메타데이터 리스트

    Returns:
        list[dict]: 파싱된 문서 메타데이터 리스트
    """
    document_dict = {}
    for metadata, document in zip(
        document_metadatas["metadatas"], document_metadatas["documents"]
    ):
        if metadata["document_name"] not in document_dict:
            document_dict[metadata["document_name"]] = []
        document_dict[metadata["document_name"]].append([document])
    print(document_dict)
    parsed_document_metadatas = [
        {
            "document_name": document_name,
            "document_contents": document_contents,
        }
        for document_name, document_contents in zip(
            document_dict.keys(), document_dict.values()
        )
    ]
    return parsed_document_metadatas


def insert_document_to_vector_store(
    user_id: str, document_id: str, document_name: str
) -> None:
    """
    Document content를 vector store에 저장

    Args:
        user_id (str): 사용자 ID
        document_id (str): 문서 ID
        document_name (str): 문서 이름
    """
    documents = []
    document_content = read_user_document_from_file(user_id, document_id)
    for chunk in chunk_document(document_content):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "user_id": user_id,
                    "document_id": document_id,
                    "document_name": document_name,
                },
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
