from core import config
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr
from util.document import vector_store
import logging

OPENAI_API_KEY = config.OPENAI_API_KEY
OPENAI_MODEL = config.OPENAI_MODEL


def get_chat_model():
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set.")
    return ChatOpenAI(api_key=SecretStr(OPENAI_API_KEY), model=OPENAI_MODEL)


def get_answer(user_query: str) -> str:
    """
    유저의 질문에 응답을 반환

    Args:
        user_query (str): 유저의 질문

    Returns:
        str: 응답
    """
    # try:
    model = get_chat_model()
    prompt = PromptTemplate.from_template(
        """
        You are a helpful assistant. Answer the question based on the following context: {context}

        Question: {question}
        """
    )

    contexts = retrieve_context(user_query)
    context = "\n".join([doc.page_content for doc in contexts["context"]])

    chain = prompt | model | StrOutputParser()
    answer = chain.invoke({"context": context, "question": user_query})
    return answer
    # except Exception as e:
    #     logging.error(f"Error in chat: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))


def retrieve_context(user_query: str) -> str:
    """
    유저의 질문에 대해 유사도 높은 문서 반환

    Args:
        user_query (str): 유저의 질문

    Returns:
        str:
    """
    try:
        retrived_docs = vector_store.similarity_search(user_query)
        return {"context": retrived_docs}
    except Exception as e:
        logging.error(f"Error in retrieve_context: {e}")
        raise HTTPException(status_code=500, detail=str(e))
