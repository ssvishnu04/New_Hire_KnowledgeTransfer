import json
from pathlib import Path
import fitz  # PyMuPDF

from chunker import chunk_text


BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "raw" / "pdfs"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "pdf_chunks.json"


def extract_pdf_chunks():
    all_chunks = []

    pdf_files = list(PDF_DIR.glob("*.pdf"))
    for pdf_file in pdf_files:
        doc = fitz.open(pdf_file)

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if not text:
                continue

            chunks = chunk_text(text, chunk_size=500, overlap=100)

            for idx, chunk in enumerate(chunks):
                all_chunks.append({
                    "source_type": "pdf",
                    "file_name": pdf_file.name,
                    "title": pdf_file.stem,
                    "page_number": page_num,
                    "chunk_id": f"{pdf_file.stem}_p{page_num}_c{idx}",
                    "text": chunk,
                })

    return all_chunks


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    chunks = extract_pdf_chunks()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(chunks)} PDF chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()