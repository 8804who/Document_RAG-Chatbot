from fastapi import APIRouter
from api.v1.endpoints.auth import auth_router
from api.v1.endpoints.chatbot import chatbot_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/v1/auth", tags=["authentication"])
api_router.include_router(chatbot_router, prefix="/v1/chatbot", tags=["chatbot"])
