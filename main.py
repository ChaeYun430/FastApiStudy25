from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from core.dependencies import get_query_token, get_token_header
from routers import item, user

app = FastAPI(
    title = 'Fast Api Study',
    version = 'v0.0.1',
    # docs_url = None,
    redoc_url = None,
    dependencies=[Depends(get_query_token)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(
    item.router,
    prefix="/item",
    tags=["item"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a item"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


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



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

from typing import Union

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

ㄴ