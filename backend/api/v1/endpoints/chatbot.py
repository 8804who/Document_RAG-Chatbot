from fastapi import APIRouter, HTTPException, Depends
from schemas.chat import ChatRequest
from services.chat_service import get_answer
from util.chatbot import save_chat_log
from util.dependencies import get_current_user
import logging

chatbot_router = APIRouter()


@chatbot_router.get("/health")
async def health_check(current_user: dict = Depends(get_current_user)) -> dict:
    """
    인증이 필요한 상태 확인 엔드포인트

    Args:
        current_user (dict): 인증된 사용자 정보

    Returns:
        dict: 상태 확인 결과와 인증된 사용자 정보
    """
    return {
        "status": "healthy",
        "authenticated_user": current_user.get("email", "unknown"),
        "message": "Chatbot service is running",
    }


@chatbot_router.post("/chat")
async def chat(
    request: ChatRequest, current_user: dict = Depends(get_current_user)
) -> dict:
    """
    챗봇에게 유저 메시지를 전달하고 챗봇의 응답을 반환

    Args:
        request (ChatRequest): 유저 메시지가 담긴 요청
        current_user (dict): 인증된 사용자 정보

    Returns:
        dict: 챗봇의 응답

    Raises:
        HTTPException: 챗봇 응답 중 오류가 발생한 경우 500 에러 반환
    """
    # try:
    logging.info(f"Chat request from user: {current_user.get('email', 'unknown')}")

    answer = get_answer(user_query=request.message)
    save_chat_log(
        email=current_user.get("email", "unknown"),
        query=request.message,
        response=answer.content,
    )
    return {"message": answer.content}
    # except Exception as e:
    #     logging.error(f"Error in chat: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))
