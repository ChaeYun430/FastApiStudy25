from kafka import KafkaConsumer
from dotenv import load_dotenv
import json
import os
from model import predict_risk

load_dotenv()
consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC"),
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    group_id = os.getenv("KAFKA_GROUP_ID"),
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    print(f"Received payment event: {event['paymentId']}")

    risk_score = predict_risk(event)
    if risk_score > 0.8:
        print(f"High risk transaction detected: {event['paymentId']}")
        # 후처리: 알림/환불/리뷰 처리