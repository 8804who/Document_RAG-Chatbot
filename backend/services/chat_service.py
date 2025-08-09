from core import config
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
import logging

OPENAI_API_KEY = config.OPENAI_API_KEY
OPENAI_MODEL = config.OPENAI_MODEL


def get_chat_model():
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set.")
    return ChatOpenAI(api_key=SecretStr(OPENAI_API_KEY), model=OPENAI_MODEL)


def get_answer(user_query: str):
    try:
        model = get_chat_model()
        answer = model.invoke(user_query)
        return answer
    except Exception as e:
        logging.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
