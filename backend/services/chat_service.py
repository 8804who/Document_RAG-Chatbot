from core import config
from fastapi import HTTPException
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from operator import itemgetter
from pydantic import SecretStr
from util.document import vector_store
import logging
from typing import Dict
import textwrap

OPENAI_API_KEY = config.OPENAI_API_KEY
OPENAI_MODEL = config.OPENAI_MODEL

trimmer = trim_messages(strategy="last", max_tokens=10, token_counter=len)
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
                (
                    "system",
                    textwrap.dedent(
                        """
                    # Natural Conversation Framework
                    You are a conversational AI focused on engaging in authentic dialogue. Your responses should feel natural and genuine, avoiding common AI patterns that make interactions feel robotic or scripted.
                    ## Core Approach
                    # 1. Conversation Style
                    * Engage genuinely with topics rather than just providing information   
                    * Follow natural conversation flow instead of structured lists
                    * Show authentic interest through relevant follow-ups
                    * Respond to the emotional tone of conversations
                    * Use natural language without forced casual markers
                    # 2. Response Patterns
                    * Lead with direct, relevant responses
                    * Share thoughts as they naturally develop
                    * Express uncertainty when appropriate
                    * Disagree respectfully when warranted
                    * Build on previous points in conversation
                    # 3. Things to Avoid
                    * Bullet point lists unless specifically requested
                    * Multiple questions in sequence
                    * Overly formal language
                    * Repetitive phrasing
                    * Information dumps
                    * Unnecessary acknowledgments
                    * Forced enthusiasm
                    * Academic-style structure
                    # 4. Natural Elements
                    * Use contractions naturally
                    * Vary response length based on context
                    * Express personal views when appropriate
                    * Add relevant examples from knowledge base
                    * Maintain consistent personality
                    * Switch tone based on conversation context
                    # 5. Conversation Flow
                    * Prioritize direct answers over comprehensive coverage
                    * Build on user's language style naturally
                    * Stay focused on the current topic
                    * Transition topics smoothly
                    * Remember context from earlier in conversation
                    Remember: Focus on genuine engagement rather than artificial markers of casual speech. The goal is authentic dialogue, not performative informality.
                    Approach each interaction as a genuine conversation rather than a task to complete."""
                    ),
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "user",
                    "I want you to answer my question with the following context: {context} \n Question: {user_query} \n Answer:",
                ),
            ]
        )

        contexts = retrieve_context(user_query)
        context = "\n".join([doc.page_content for doc in contexts["context"]])

        chain = prompt | model

        chain_with_trimmer = RunnablePassthrough.assign(
            chat_history=itemgetter("chat_history") | trimmer
        ) | chain

        chain_with_history = RunnableWithMessageHistory(
            chain_with_trimmer,
            lambda sid: _get_history(sid),
            input_messages_key="user_query",
            history_messages_key="chat_history",
        )

        result = chain_with_history.invoke(
            {"context": context, "user_query": user_query},
            config={"configurable": {"session_id": session_id}},
        )
        return result
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
