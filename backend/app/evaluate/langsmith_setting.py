from langsmith import Client

from app.core.config import settings


LANGSMITH_API_KEY = settings.LANGSMITH_API_KEY.get_secret_value()
LANGSMITH_ENDPOINT = settings.LANGSMITH_ENDPOINT
LANGSMITH_PROJECT = settings.LANGSMITH_PROJECT
LANGSMITH_TRACING = settings.LANGSMITH_TRACING

client = Client(api_key=LANGSMITH_API_KEY)
