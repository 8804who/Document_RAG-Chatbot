from langsmith import Client

from app.core.config import Settings


LANGSMITH_API_KEY = Settings.LANGSMITH_API_KEY
LANGSMITH_ENDPOINT = Settings.LANGSMITH_ENDPOINT
LANGSMITH_PROJECT = Settings.LANGSMITH_PROJECT
LANGSMITH_TRACING = Settings.LANGSMITH_TRACING

client = Client(api_key=LANGSMITH_API_KEY)
