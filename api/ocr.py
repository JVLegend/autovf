import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import io

app = FastAPI()
ocr = PaddleOCR(lang='en', use_angle_cls=True)

@app.post("/api/ocr")
async def extract_images(files: list[UploadFile] = File(...)):
    results = []
    for idx, file in enumerate(files):
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_np = np.array(img)
        ocr_result = ocr.ocr(img_np)
        page_text = []
        for res in ocr_result[0]:
            text = res[1][0]
            conf = res[1][1]
            bbox = res[0]
            page_text.append({
                "text": text,
                "confidence": conf,
                "bbox": bbox
            })
        results.append({
            "page": idx + 1,
            "content": page_text
        })
    return JSONResponse(content={"pages": results}) 