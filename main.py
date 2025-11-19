from fastapi import FastAPI

app = FastAPI(
    title = 'Fast Api Study',
    version = 'v0.0.1',
    # docs_url = None,
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


# 경로 작동은 순차적으로 실행/ “라우트 등록 순서”가 곧 우선순위
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# 경로 매개변수로 가능한 값들을 미리 정의하고 싶다면
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# path를 포함하는 경로 매개변수를 선언
# Starlette(FastAPI)의 path 컨버터
# /를 포함하는 경로 문자열 전체를 하나의 파라미터로 해석하게 하는 기능
# 슬래시 포함 문자열 전체를 하나의 값으로 수집
# 남은 경로를 더 이상 분리하지 않고 끝까지 파싱
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}