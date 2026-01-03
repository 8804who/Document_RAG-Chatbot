import logging
from operator import itemgetter

import yaml
from fastapi import HTTPException
from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.util.chat_history import get_chat_history
from app.util.document import vector_store
from app.util.tokenizer import OpenAiTokenizer

OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_MODEL = settings.OPENAI_MODEL

trimmer = trim_messages(
    strategy="last",
    max_tokens=2000,
    token_counter=OpenAiTokenizer().count_tokens,
)


class ChatService:
    def __init__(self, model_type: str = "openai"):
        self.chat_model = self.get_chat_model(model_type)

    def get_chat_model(self, model_type: str) -> ChatOpenAI:
        if model_type == "openai":
            if not OPENAI_API_KEY.get_secret_value():
                raise ValueError("OPENAI_API_KEY is not set.")
            return ChatOpenAI(
                api_key=OPENAI_API_KEY.get_secret_value(), model=OPENAI_MODEL
            )
        # elif model_type == "anthropic":
        #     return Anthropic(api_key=SecretStr(ANTHROPIC_API_KEY), model=ANTHROPIC_MODEL)
        # elif model_type == "google":
        #     return Google(api_key=SecretStr(GOOGLE_API_KEY), model=GOOGLE_MODEL)
        else:
            raise ValueError(f"Invalid model type: {model_type}")

    
    def get_chat_prompt(self) -> ChatPromptTemplate:

        messages = []

        with open("app/prompts/chat_prompt.yaml", "r") as f:    
            cfg = yaml.safe_load(f)

        for message in cfg["messages"]:
            if message["type"] == "system":
                messages.append(("system", message["content"]))
            elif message["type"] == "user":
                messages.append(("user", message["content"]))
            elif message["type"] == "placeholder":
                messages.append(MessagesPlaceholder(variable_name=message["name"]))
        return ChatPromptTemplate.from_messages(messages)

    async def get_answer(
        self, user_query: str, session_id: str
    ) -> BaseMessage:
        """
        유저의 질문에 응답을 반환

        Args:
            user_query (str): 유저의 질문
            session_id (str): 세션 아이디
        Returns:
            BaseMessage: 응답
        """
        try:
            prompt = self.get_chat_prompt()

            contexts = self.retrieve_context(user_query)
            context = "\n".join(
                [doc.page_content for doc in contexts["context"]]
            )

            chain = prompt | self.chat_model

            chain_with_trimmer = (
                RunnablePassthrough.assign(
                    chat_history=itemgetter("chat_history") | trimmer
                )
                | chain
            )

            chain_with_history = RunnableWithMessageHistory(
                chain_with_trimmer,
                get_chat_history,
                input_messages_key="user_query",
                history_messages_key="chat_history",
            )

            result = await chain_with_history.ainvoke(
                {"context": context, "user_query": user_query},
                config={"configurable": {"session_id": session_id}},
            )

            return result
        except Exception as e:
            logging.error(f"Error in chat_service: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def retrieve_context(self, user_query: str) -> dict:
        """
        유저의 질문에 대해 유사도 높은 문서 반환

        Args:
            user_query (str): 유저의 질문

        Returns:
            dict
        """
        try:
            retrieved_docs = vector_store.similarity_search(user_query)
            return {"context": retrieved_docs}
        except Exception as e:
            logging.error(f"Error in retrieve_context: {e}")
            raise HTTPException(status_code=500, detail=str(e))
