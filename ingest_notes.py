import json
from pathlib import Path

from chunker import chunk_text


BASE_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = BASE_DIR / "data" / "raw" / "notes"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "note_chunks.json"


def extract_note_chunks():
    all_chunks = []

    note_files = list(NOTES_DIR.glob("*.*"))
    for note_file in note_files:
        text = note_file.read_text(encoding="utf-8").strip()
        if not text:
            continue

        chunks = chunk_text(text, chunk_size=500, overlap=100)

        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "source_type": "note",
                "file_name": note_file.name,
                "title": note_file.stem,
                "page_number": None,
                "chunk_id": f"{note_file.stem}_c{idx}",
                "text": chunk,
            })

    return all_chunks


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    chunks = extract_note_chunks()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(chunks)} note chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()