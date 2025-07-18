import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import io

app = FastAPI()
ocr = PaddleOCR(lang='en', use_angle_cls=True)

@app.post("/api/ocr")
async def extract_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    results = []
    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
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
            "page": page_num + 1,
            "content": page_text
        })
    return JSONResponse(content={"pages": results}) 