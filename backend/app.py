from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api.v1.router import api_router
import uvicorn

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
    secret_key="12312dadl3l1k3k",  # 반드시 랜덤하고 안전한 값으로 설정 (배포 시 중요!)
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"message": "서버가 정상 실행중입니다."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10004)
