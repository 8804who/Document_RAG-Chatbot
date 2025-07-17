from dotenv import load_dotenv
import os

load_dotenv()

# API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DB
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
