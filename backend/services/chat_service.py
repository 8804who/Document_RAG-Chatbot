from langchain_openai import ChatOpenAI
from core import config
from pydantic import SecretStr

OPENAI_API_KEY = config.OPENAI_API_KEY


def get_chat_model():
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set.")
    return ChatOpenAI(api_key=SecretStr(OPENAI_API_KEY), model="gpt-4o-mini")
