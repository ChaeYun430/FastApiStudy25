from fastapi import FastAPI, Depends
from routers import video
app = FastAPI(
    title = 'object_detection Study',
    version = 'v0.0.1',
    # docs_url = None,
    redoc_url = None
)

app.include_router(video.router)


@app.get("")
async def root():
    return {"message": "Hello World"}

@app.post("")
async def root():
    return {"message": "Hello World"}

