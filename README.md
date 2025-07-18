# Super OCR do Campo Visual

Este projeto permite o upload de PDFs, extração de texto via PaddleOCR (Python) e exibição do resultado em uma interface bonita feita com Next.js, TypeScript e DaisyUI, pronto para deploy no Vercel.

## Como funciona
- Frontend: Next.js + DaisyUI (upload de PDF, exibição do JSON extraído)
- Backend: Python (FastAPI, PaddleOCR, PyMuPDF) como função serverless em `/api/ocr.py`

## Como rodar localmente

### 1. Backend Python (API OCR)
```bash
pip install -r requirements.txt
uvicorn api.ocr:app --reload
```
Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para testar o upload do PDF pela interface Swagger.

### 2. Frontend Next.js
```bash
cd frontend
npm install
npm run dev
```
Acesse [http://localhost:3000](http://localhost:3000)

#### Para integração local:
- Altere o endpoint do fetch no frontend para `http://localhost:8000/api/ocr` durante o desenvolvimento local.
- Exemplo:
```ts
const res = await fetch("http://localhost:8000/api/ocr", { ... })
```

## Deploy no Vercel
1. Suba todo o projeto (com as pastas `api/` e `frontend/`) para o GitHub.
2. No Vercel, conecte o repositório.
3. O Vercel detecta automaticamente:
   - Funções Python em `/api` (serverless)
   - Frontend Next.js em `/frontend`
4. O endpoint `/api/ocr` ficará disponível para o frontend consumir.

Pronto! Seu sistema estará disponível online.
