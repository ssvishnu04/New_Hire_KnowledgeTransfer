import json
import re
from pathlib import Path

from chunker import chunk_text


BASE_DIR = Path(__file__).resolve().parent.parent
VIDEOS_DIR = BASE_DIR / "data" / "raw" / "videos"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "video_chunks.json"

TIMESTAMP_PATTERN = re.compile(r"\[(\d{2}:\d{2})\]")


def extract_video_chunks() -> list[dict]:
    all_chunks: list[dict] = []

    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    transcript_files = list(VIDEOS_DIR.glob("*.txt"))

    if not transcript_files:
        print("No video transcript files found. Skipping video transcript ingestion.")
        return []

    for transcript_file in transcript_files:
        print(f"Processing Video Transcript: {transcript_file.name}")

        try:
            text = transcript_file.read_text(encoding="utf-8").strip()

            if not text:
                continue

            chunks = chunk_text(text, chunk_size=500, overlap=100)

            for idx, chunk in enumerate(chunks):
                timestamps = TIMESTAMP_PATTERN.findall(chunk)

                all_chunks.append({
                    "source_type": "video_transcript",
                    "file_name": transcript_file.name,
                    "title": transcript_file.stem,
                    "page_number": None,
                    "timestamp_markers": timestamps,
                    "chunk_id": f"{transcript_file.stem}_c{idx}",
                    "text": chunk,
                })

        except Exception as e:
            print(f"Failed to process video transcript {transcript_file.name}: {str(e)}")

    return all_chunks


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    chunks = extract_video_chunks()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(chunks)} video transcript chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
