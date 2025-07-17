from fastapi import APIRouter
from endpoints.chatbot import chatbot_router

api_router = APIRouter()

api_router.include_router(chatbot_router, prefix="/v1/chatbot", tags=["chatbot"])
