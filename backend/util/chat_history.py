from core import config
import psycopg
from langchain_postgres import PostgresChatMessageHistory

db_connection_string = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

table_name = "chat_history"
_async_connection: psycopg.AsyncConnection | None = None


def get_chat_history(session_id: str) -> PostgresChatMessageHistory:
    if _async_connection is None:
        raise RuntimeError("Chat history not initialized. Call init_chat_history() during app startup.")
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        async_connection=_async_connection
    )


async def init_chat_history() -> None:
    global _async_connection
    if _async_connection is None:
        _async_connection = await psycopg.AsyncConnection.connect(db_connection_string)
        await PostgresChatMessageHistory.acreate_tables(_async_connection, table_name)


async def close_chat_history() -> None:
    global _async_connection
    if _async_connection is not None:
        await _async_connection.close()
        _async_connection = None