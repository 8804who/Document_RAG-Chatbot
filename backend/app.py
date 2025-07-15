from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
    return {"message": "서버가 정상 실행중입니다."}
