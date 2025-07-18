# Super OCR do Campo Visual

Este projeto permite o upload de PDFs, extração de texto via PaddleOCR (Python) e exibição do resultado em uma interface bonita feita com Next.js, TypeScript e DaisyUI, pronto para deploy no Vercel.

## Como funciona
- **Frontend (Next.js + DaisyUI):**
  - O usuário faz upload de um PDF.
  - Cada página do PDF é convertida em imagem (PNG) no navegador usando JavaScript (`pdfjs-dist`).
  - As imagens são enviadas para o backend Python.
  - O resultado do OCR é exibido em JSON organizado na tela.
- **Backend (Python, FastAPI, PaddleOCR):**
  - Recebe múltiplas imagens (uma para cada página do PDF).
  - Processa cada imagem com PaddleOCR.
  - Retorna o resultado do OCR em JSON.

## Como rodar localmente

### 1. Backend Python (API OCR)
```bash
pip install -r requirements.txt
uvicorn api.ocr:app --reload
```
Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para testar o upload de imagens pela interface Swagger.

### 2. Frontend Next.js
```bash
cd frontend
npm install
npm install pdfjs-dist
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

## Observações importantes
- O backend **não aceita mais PDF diretamente**. O frontend converte o PDF em imagens antes do envio.
- Não há mais dependência de bibliotecas nativas problemáticas como PyMuPDF.
- O fluxo é 100% compatível com o ambiente serverless do Vercel.

Pronto! Seu sistema estará disponível online e funcionando de ponta a ponta.
