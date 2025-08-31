from core import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api.v1.router import api_router
import uvicorn
from contextlib import asynccontextmanager
from services.chat_service import _save_history_to_db
import asyncio

app = FastAPI()

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    서버 생명주기 관리

    Args:
        app (FastAPI): FastAPI 애플리케이션
    """
    asyncio.create_task(_save_history_to_db())
    yield

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10004)
