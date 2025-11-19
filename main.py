from fastapi import FastAPI

app = FastAPI(
    title = 'Fast Api Study',
    version = 'v0.0.1',
    docs_url = None,
    redoc_url = None
)


# 이 데코레이터는 FastAPI에게 아래 함수가 경로 /의 get 작동에 해당한다고 알려줌
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 타입 선언을 하면 FastAPI는 자동으로 요청을 파싱(데이터 검증)함
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}