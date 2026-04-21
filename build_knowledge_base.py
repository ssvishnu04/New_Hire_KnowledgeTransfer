import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "knowledge_base.json"


INPUT_FILES = [
    PROCESSED_DIR / "pdf_chunks.json",
    PROCESSED_DIR / "note_chunks.json",
    PROCESSED_DIR / "video_chunks.json",
]


def load_json(file_path: Path):
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    all_chunks = []

    for file_path in INPUT_FILES:
        all_chunks.extend(load_json(file_path))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Knowledge base built successfully with {len(all_chunks)} chunks.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()