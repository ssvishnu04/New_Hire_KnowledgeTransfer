import json
from pathlib import Path

from chunker import chunk_text


BASE_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = BASE_DIR / "data" / "raw" / "notes"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "note_chunks.json"


def extract_note_chunks() -> list[dict]:
    all_chunks: list[dict] = []

    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    note_files = []
    note_files.extend(NOTES_DIR.glob("*.txt"))
    note_files.extend(NOTES_DIR.glob("*.md"))

    note_files = list(note_files)

    if not note_files:
        print("No note files found. Skipping note ingestion.")
        return []

    for note_file in note_files:
        print(f"Processing Note: {note_file.name}")

        try:
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
                    "timestamp_markers": [],
                    "chunk_id": f"{note_file.stem}_c{idx}",
                    "text": chunk,
                })

        except Exception as e:
            print(f"Failed to process note {note_file.name}: {str(e)}")

    return all_chunks


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    chunks = extract_note_chunks()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(chunks)} note chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
