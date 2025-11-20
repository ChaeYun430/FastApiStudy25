# pip install fastapi uvicorn pydantic Pillow numpy requests
# pip install ultralytics opencv-python python-multipart

# fastapi : 비동기 웹 프레임워크, 자동 OpenAPI 문서 생성
# uvicorn : 고성능 비동기 서버, ASGI 표준 지원
# pydantic : 데이터 검증, 직렬화, 타입 힌팅, 설정관리
# Pillow : 이미지 열기, 저장, 변환, 다양한 이미지 처리용
# numpy : 수치계산, 배열 및 행렬 연산, 다양한 수학함수
# requests : 간단한 http 요청 및 응답 처리
# ultralytics : YOLO8 객체 탐지 모델 제공
# opencv-python : 이미지 및 비디오 처리, 컴퓨터 비전 기능(roboflow 대체)
# python-multipart : 멀티파트 폼 데이터를 파싱하기 위함


from fastapi import UploadFile,File,Form
import io, base64
from fastapi import APIRouter
from PIL import Image
from ..pipeline.detect_object import detect_object
from ..schemas.detection import DetectionResult

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}}
)

@router.post("/detect",response_model=DetectionResult)
async def detect_service(message : str = Form(...), file:UploadFile = File(...)):

    image = Image.open(io.BytesIO(await file.read()))

    # 알파 채널 제거하고 RGB로 변환
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode !='RGB':
        image = image.convert('RGB')

    # 객체 탐지 수행 -> 이미지가 들어가서 모델에서 처리 후 결과를 받음
    result_image = detect_object(image)

    # 이미지 결과를 base64로 인코딩
    buffered = io.BytesIO()
    result_image.save(buffered,format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return DetectionResult(message=message,image=img_str)



