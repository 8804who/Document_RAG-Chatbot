from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from api.v1.router import api_router
from core import config
from util.chat_history import init_chat_history, close_chat_history
from util.logger import setup_logger, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    서버 생명주기 관리

    Args:
        app (FastAPI): FastAPI 애플리케이션
    """
    try:
        setup_logger()
        logger.info("Server is starting...")
        await init_chat_history()
        yield
    finally:
        logger.info("Server is stopping...")
        await close_chat_history()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:10002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=config.SESSION_SECRET_KEY,
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"message": "서버가 정상 실행중입니다."}


@app.middleware("http")
async def log_processing_time(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time

    log_endpoint_list = ["/api/v1/chatbot/chat"]

    if request.url.path in log_endpoint_list:
        logger.info(f"{request.method} {request.url.path} -> {process_time:.4f}s")

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10004)
