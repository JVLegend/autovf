# Certifique-se de instalar as bibliotecas necessárias
#pip install gradio tensorflow requests opencv-python-headless pandas huggingface_hub easyocr datasets paddlepaddle-gpu==2.5.2 paddleocr==2.6.1.3

import os
import cv2
import easyocr
import numpy as np
import pandas as pd
import gradio as gr
import tensorflow as tf
from datetime import datetime
from PIL import Image as PILImage
from paddleocr import PaddleOCR
import paddle
paddle.utils.run_check()

# Save_data import funcionalidade simulada
def flag(method, text_output, img):
    print(f"Flagging: Method: {method}, Text Output: {text_output}")

# Paddle OCR
paddle_ocr = PaddleOCR(lang='en', use_angle_cls=True)

def ocr_with_paddle(img):
    # Se for PIL, converte para np array
    if isinstance(img, PILImage.Image):
        img = np.array(img)
    finaltext = ''
    result = paddle_ocr.ocr(img)
    for res in result[0]:
        text = res[1][0]
        finaltext += ' ' + text
    return finaltext

# Easy OCR
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(src):
    return cv2.threshold(src, 127, 255, cv2.THRESH_TOZERO)[1]

def ocr_with_easy(img):
    gray_scale_image = get_grayscale(img)
    thresholded = thresholding(gray_scale_image)
    cv2.imwrite('image.png', thresholded)
    reader = easyocr.Reader(['th', 'en'])
    bounds = reader.readtext('image.png', paragraph=False, detail=0)
    bounds = ''.join(bounds)
    return bounds

# Generate OCR
def generate_ocr(Method, img):
    text_output = ''
    if img.any():
        if Method == 'EasyOCR':
            text_output = ocr_with_easy(img)
        elif Method == 'PaddleOCR':
            text_output = ocr_with_paddle(img)

        try:
            flag(Method, text_output, img)
        except Exception as e:
            print(e)
        return text_output
    else:
        raise gr.Error("Please upload an image!")

# Criação da interface do usuário para demonstração OCR
image = gr.Image()
method = gr.Radio(["PaddleOCR", "EasyOCR"], value="PaddleOCR")
output = gr.Textbox(label="Output")

demo = gr.Interface(
    generate_ocr,
    [method, image],
    output,
    title="Super OCR do Campo Visual",
    css=".gradio-container {background-color: lightgray} #radio_div {background-color: #FFD8B4; font-size: 40px;}",
    article="""<p style='text-align: center;'>Lab prof Mario""",
)

demo.launch(debug=True) #para remover o log basta usar demo.launch()
