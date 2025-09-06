from core import config
import psycopg
from langchain_postgres import PostgresChatMessageHistory

db_connection_string = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

sync_connection = psycopg.connect(db_connection_string)
async_connection = psycopg.AsyncConnection.connect(db_connection_string)

table_name = "chat_history"
PostgresChatMessageHistory.create_tables(sync_connection, table_name)


def get_chat_history(session_id: str) -> PostgresChatMessageHistory:
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        async_connection=async_connection
    )