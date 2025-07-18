"use client";
import React, { useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import "pdfjs-dist/build/pdf.worker.entry";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  // Converte PDF em array de blobs PNG
  const pdfToImages = async (pdfFile: File): Promise<Blob[]> => {
    const arrayBuffer = await pdfFile.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    const images: Blob[] = [];
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const viewport = page.getViewport({ scale: 2.0 });
      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d")!;
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      await page.render({ canvasContext: context, viewport }).promise;
      const blob: Blob = await new Promise((resolve) =>
        canvas.toBlob((b) => resolve(b!), "image/png")
      );
      images.push(blob);
    }
    return images;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);

    // 1. Converte PDF em imagens
    const images = await pdfToImages(file);

    // 2. Envia as imagens para o backend
    const formData = new FormData();
    images.forEach((img, idx) => {
      formData.append("files", img, `page${idx + 1}.png`);
    });

    const res = await fetch("/api/ocr", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary to-secondary flex flex-col items-center justify-center p-4">
      <div className="card w-full max-w-xl bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title text-3xl mb-4">Super OCR do Campo Visual</h2>
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <input
              type="file"
              accept="application/pdf"
              className="file-input file-input-bordered w-full"
              onChange={handleFileChange}
            />
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !file}
            >
              {loading ? "Processando..." : "Extrair Texto"}
            </button>
          </form>
          {result && (
            <div className="mt-6">
              <h3 className="text-xl font-bold mb-2">Resultado (JSON):</h3>
              <pre className="bg-gray-100 p-2 rounded overflow-x-auto text-xs max-h-96">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
      <footer className="mt-8 text-center text-gray-500">
        <p>Lab prof Mario</p>
      </footer>
    </div>
  );
}
