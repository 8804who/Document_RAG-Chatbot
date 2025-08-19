from core import config
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr
from util.document import vector_store
import logging
from typing import Dict

OPENAI_API_KEY = config.OPENAI_API_KEY
OPENAI_MODEL = config.OPENAI_MODEL

_CHAT_HISTORIES: Dict[str, ChatMessageHistory] = {}


def _get_history(session_id: str) -> ChatMessageHistory:
    """
    세션 아이디에 대한 채팅 기록 반환

    Args:
        session_id (str): 세션 아이디

    Returns:
        ChatMessageHistory: 채팅 기록
    """
    history = _CHAT_HISTORIES.get(session_id)
    if history is None:
        history = ChatMessageHistory()
        _CHAT_HISTORIES[session_id] = history
    return history


def get_chat_model() -> ChatOpenAI:
    """
    OpenAI Chat 모델 반환

    Returns:
        ChatOpenAI: OpenAI Chat 모델
    """
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set.")
    return ChatOpenAI(api_key=SecretStr(OPENAI_API_KEY), model=OPENAI_MODEL)


async def get_answer(user_query: str, session_id: str) -> str:
    """
    유저의 질문에 응답을 반환

    Args:
        user_query (str): 유저의 질문
        session_id (str): 세션 아이디
    Returns:
        str: 응답
    """
    try:
        model = get_chat_model()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant."),
                ("placeholder", "{chat_history}"),
                (
                    "user",
                    "Answer the question based on the following context: {context}",
                ),
                ("user", "Question: {question}"),
            ]
        )

        contexts = retrieve_context(user_query)
        context = "\n".join([doc.page_content for doc in contexts["context"]])

        chain = prompt | model

        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda sid: _get_history(sid),
            input_messages_key="question",
            history_messages_key="chat_history",
        )

        result = chain_with_history.invoke(
            {"context": context, "question": user_query},
            config={"configurable": {"session_id": session_id}},
        )
        return result.content
    except Exception as e:
        logging.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
