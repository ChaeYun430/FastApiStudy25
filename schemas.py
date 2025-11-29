from pydantic import BaseModel
from typing import Optional

# Transaction
class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    merchant_id: str
    amount: float
    currency: str
    transaction_type: str  # 카드, 계좌이체, PG 등
    status: str  # 승인, 거절 등
    timestamp: str
    mcc: str
    device_type: str
    location: str

# User
class User(BaseModel):
    user_id: str

    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    account_created_at: Optional[str]
    avg_transaction_amount: Optional[float]
    device_history: Optional[str]

# Merchant
class Merchant(BaseModel):
    merchant_id: str

    name: Optional[str]
    business_no: Optional[str]
    category: Optional[str]
    bank_account: Optional[str]
    location: Optional[str]

# FraudScore
class FraudScore(BaseModel):
    transaction_id: str
    score: float
    threshold: float
    decision: str  # 승인, 추가 인증, 거절
    created_at: str
