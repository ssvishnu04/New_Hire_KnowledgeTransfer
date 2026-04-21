from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "raw" / "pdfs"
NOTES_DIR = BASE_DIR / "data" / "raw" / "notes"
VIDEOS_DIR = BASE_DIR / "data" / "raw" / "videos"


def save_uploaded_file(uploaded_file, category: str) -> str:
    if category == "pdf":
        target_dir = PDF_DIR
    elif category == "note":
        target_dir = NOTES_DIR
    elif category == "video_transcript":
        target_dir = VIDEOS_DIR
    else:
        raise ValueError(f"Unsupported category: {category}")

    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)


def list_raw_files() -> dict:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    return {
        "pdf": sorted([p.name for p in PDF_DIR.glob("*") if p.is_file()]),
        "note": sorted([p.name for p in NOTES_DIR.glob("*") if p.is_file()]),
        "video_transcript": sorted([p.name for p in VIDEOS_DIR.glob("*") if p.is_file()]),
    }


def delete_raw_file(category: str, filename: str) -> str:
    if category == "pdf":
        target_dir = PDF_DIR
    elif category == "note":
        target_dir = NOTES_DIR
    elif category == "video_transcript":
        target_dir = VIDEOS_DIR
    else:
        raise ValueError(f"Unsupported category: {category}")

    file_path = target_dir / filename

    if not file_path.exists():
        return f"File not found: {file_path}"

    file_path.unlink()
    return f"Deleted: {file_path}"
