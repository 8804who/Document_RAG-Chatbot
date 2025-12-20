import logging
import textwrap
from operator import itemgetter

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
