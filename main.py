from nudenet import NudeDetector
from dataclasses import dataclass
from enum import Enum
from fastapi import FastAPI, Request
from base64 import b64decode
from PIL import Image
import io
import numpy as np
import cv2


class Detection(Enum):
    EXPOSED_ANUS = "EXPOSED_ANUS"
    EXPOSED_ARMPITS = "EXPOSED_ARMPITS"
    COVERED_BELLY = "COVERED_BELLY"
    EXPOSED_BELLY = "EXPOSED_BELLY"
    COVERED_BUTTOCKS = "COVERED_BUTTOCKS"
    EXPOSED_BUTTOCKS = "EXPOSED_BUTTOCKS"
    FACE_F = "FACE_F"
    FACE_M = "FACE_M"
    COVERED_FEET = "COVERED_FEET"
    EXPOSED_FEET = "EXPOSED_FEET"
    COVERED_BREAST_F = "COVERED_BREAST_F"
    EXPOSED_BREAST_F = "EXPOSED_BREAST_F"
    COVERED_GENITALIA_F = "COVERED_GENITALIA_F"
    EXPOSED_GENITALIA_F = "EXPOSED_GENITALIA_F"
    EXPOSED_BREAST_M = "EXPOSED_BREAST_M"
    EXPOSED_GENITALIA_M = "EXPOSED_GENITALIA_M"


@dataclass
class Result:
    detection: list[Detection]

    @classmethod
    def from_dict(cls, data: list[dict[str, list | int | float]]):
        return cls(
            detection=[Detection(detection.get("label")) for detection in data],
        )


app = FastAPI()


@app.post("/detect", response_model=Result)
async def detect(request: Request):
    return Result.from_dict(
        NudeDetector().detect(
            np.array(Image.open(io.BytesIO(b64decode(await request.body()))))
        )
    )