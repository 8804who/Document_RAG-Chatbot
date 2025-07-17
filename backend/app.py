from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/health")
def health_check():
    return {"message": "서버가 정상 실행중입니다."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
