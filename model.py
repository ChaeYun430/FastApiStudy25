import numpy as np

# 가상 모델 로드
# 실제: AutoEncoder load_weights, scaler load
def predict_risk(features):
    # 단순 예시 계산
    risk_score = 0.4*features['high_amount_flag'] + \
                 0.3*features['location_change_flag'] + \
                 0.3*features['device_change_flag']
    recon_error_norm = np.random.rand() * 0.6  # AutoEncoder error placeholder
    final_score = 0.6*recon_error_norm + 0.4*risk_score
    is_suspicious = int(final_score > 0.5)
    return {"risk_score": final_score, "is_suspicious": is_suspicious}