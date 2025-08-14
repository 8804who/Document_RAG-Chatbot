from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# OPENAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

# DB
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Chroma
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# OAuth2
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# SessionMiddleware
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

# Chunking
CHUNK_SIZE = os.getenv("CHUNK_SIZE")
CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP")
