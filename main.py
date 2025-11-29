from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_risk

app = FastAPI()

# 요청 모델 정의
class Transaction(BaseModel):
    amount_ratio: float
    high_amount_flag: int
    location_change_flag: int
    device_change_flag: int


@app.post("/predict")
def predict(tx: Transaction):
    features = tx.dict()
    return predict_risk(features)
