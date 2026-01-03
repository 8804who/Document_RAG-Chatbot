from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from app.schemas.chat import ChatRequest, ChatResponse
from app.util.chatbot import save_chat_log
from app.util.dependencies import get_current_user
from app.util.logger import logger
from app.util.session_id import session_id_management

chatbot_router = APIRouter()


@chatbot_router.post("/chat")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    """
    챗봇에게 유저 메시지를 전달하고 챗봇의 응답을 반환

    Args:
        request (ChatRequest): 유저 메시지가 담긴 요청
        current_user (dict): 인증된 사용자 정보

    Returns:
        ChatResponse: 챗봇의 응답

    Raises:
        HTTPException: 챗봇 응답 중 오류가 발생한 경우 500 에러 반환
    """
    try:
        logger.info(
            f"Chat request from user: {current_user.get('email', 'unknown')}"
        )

        session_id = await session_id_management(
            current_user.get("email", "unknown")
        )
        response = await request.app.state.chat_service.get_answer(
            user_query=chat_request.message, session_id=session_id
        )
        answer = response.content
        logger.info(f"Chat answer: {answer}")

        # 개별 채팅 로그 저장
        background_tasks.add_task(
            save_chat_log,
            email=current_user.get("email", "unknown"),
            query=chat_request.message,
            answer=answer,
        )

        return ChatResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
