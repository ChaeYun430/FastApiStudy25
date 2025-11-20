import cv2
from ultralytics import YOLO


from fastapi import APIRouter

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def read_video():
    return None


# 1. YOLOv8 모델 로딩
model = YOLO("yolov8n.pt")  # n = nano (가볍고 빠름)

# 2. 비디오 파일 열기
video_path = "your_video.mp4"
cap = cv2.VideoCapture(video_path)

# 3. 클래스 이름 가져오기
class_names = model.model.names  # COCO 클래스 이름 (0: person, 1: bicycle, ...)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 4. YOLOv8으로 추론
    results = model(frame, verbose=False)[0]  # 첫 번째 프레임 결과

    # 5. 탐지 결과 처리
    for box in results.boxes:
        cls_id = int(box.cls[0])  # 클래스 ID
        conf = float(box.conf[0])  # 신뢰도
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding Box 좌표

        # 클래스 이름
        class_name = class_names[cls_id]

        # 콘솔 출력
        print(f"[{class_name}] {conf:.2f} @ ({x1}, {y1}) → ({x2}, {y2})")

        # 6. 화면에 박스 + 라벨 그리기
        label = f"{class_name} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 7. 결과 출력
    cv2.imshow("YOLOv8 Object Detection", frame)

    # 종료 키: ESC
    if cv2.waitKey(1) == 27:
        break

# 종료
cap.release()
cv2.destroyAllWindows()