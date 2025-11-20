from pydantic import BaseModel

class DetectionResult(BaseModel):
    message : str
    image : str

