import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

def detect_object(image: Image.Image):
    img = np.array(image)
    class_names = model.names

    results = model(img)

    # 결과를 바운딩 박스, 클래스 이름, 정확도로 이미지에 표시
    for result in results:
        boxes = result.boxes.xyxy  # 바운딩 박스
        confidences = result.boxes.conf  # 신뢰도
        class_ids = result.boxes.cls  # 클래스 이름

        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)  # 좌표를 점수로 반환
            label = class_names[int(class_ids)]  # 클래스 이름
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(img, f'{label}{confidences:.2f}',
                        (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 0), 2)

    return Image.fromarray(img)
