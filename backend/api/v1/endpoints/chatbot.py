from fastapi import APIRouter, HTTPException
from services.chat_service import get_chat_model, get_answer
from schemas.chat import ChatRequest
import logging

chatbot_router = APIRouter()


@chatbot_router.post("/chat")
async def chat(request: ChatRequest) -> dict:
    """
    챗봇에게 유저 메시지를 전달하고 챗봇의 응답을 반환

    Args:
        request (ChatRequest): 유저 메시지가 담긴 요청

    Returns:
        dict: 챗봇의 응답

    Raises:
        HTTPException: 챗봇 응답 중 오류가 발생한 경우 500 에러 반환
    """
    try:
        answer = get_answer(user_query=request.message)
        return {"message": answer}
    except Exception as e:
        logging.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
