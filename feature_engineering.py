from typing import Dict
from schemas import Transaction

def get_high_amount_flag(tx: Transaction):
    avg_amount = tx.get('avg_transaction_amount', 1)  # 0 방지
    amount = tx.get('amount', 0)
    features['amount_ratio'] = amount / avg_amount
    features['high_amount_flag'] = int(amount > avg_amount * 4)  # 4배 이상이면 High


def get_location_change_flag(tx: Transaction):
    # 2. 위치 관련
    # last_location 정보가 필요하면 User/Transaction history에서 전달
    last_location = tx.get('last_location', tx.get('location'))
    current_location = tx.get('location', 'KR')
    features['location_change_flag'] = int(current_location != last_location)
    # 해외 거래 위험 점수 (간단 예시)

    country_risk_map = {'KR': 0, 'US': 0.3, 'JP': 0.2, 'CN': 0.5}
    features['country_risk_score'] = country_risk_map.get(current_location, 0.1)





def compute_features(tx: Dict) -> Dict:
    """
    Transaction dict를 받아서 ML 모델 입력용 Feature 계산
    """
    features = {}


    # 3. 디바이스 관련
    last_device = tx.get('last_device_type', tx.get('device_type'))
    current_device = tx.get('device_type', 'mobile')
    features['device_change_flag'] = int(current_device != last_device)

    # 4. 시간 관련
    # timestamp에서 시간 추출 가능
    timestamp = tx.get('timestamp')
    if timestamp:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp)
        features['hour'] = dt.hour
        features['is_weekend'] = int(dt.weekday() >= 5)
    else:
        features['hour'] = 0
        features['is_weekend'] = 0

    # 5. 상점(Merchant) 관련
    mcc = tx.get('mcc', '0000')
    # 단순 예시: 위험 상점이면 1
    high_risk_mcc = {'5912', '5814'}  # 예: 온라인 구독, 술/주류
    features['merchant_risk_level'] = int(mcc in high_risk_mcc)

    return features


# 사용 예시
tx_example = {
    'amount': 1200,
    'avg_transaction_amount': 300,
    'location': 'US',
    'last_location': 'KR',
    'device_type': 'pc',
    'last_device_type': 'mobile',
    'timestamp': '2025-11-29T15:00:00',
    'mcc': '5912'
}

features = compute_features(tx_example)
print(features)
