import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_FILES_TO_CLEAR = [
    PROCESSED_DIR / "pdf_chunks.json",
    PROCESSED_DIR / "note_chunks.json",
    PROCESSED_DIR / "video_chunks.json",
    PROCESSED_DIR / "knowledge_base.json",
    PROCESSED_DIR / "chunk_metadata.json",
    PROCESSED_DIR / "chunk_embeddings.npy",
    PROCESSED_DIR / "knowledge_index.faiss",
]


def clear_processed_artifacts() -> list[str]:
    messages = []
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in PROCESSED_FILES_TO_CLEAR:
        if file_path.exists():
            file_path.unlink()
            messages.append(f"Deleted: {file_path}")
        else:
            messages.append(f"Not found: {file_path}")

    return messages


def run_script(script_path: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )

        output = (result.stdout or "") + ("\n" if result.stdout and result.stderr else "") + (result.stderr or "")
        output = output.strip()

        harmless_messages = [
            "No PDF files found. Skipping PDF ingestion.",
            "No note files found. Skipping note ingestion.",
            "No video transcript files found. Skipping video transcript ingestion.",
        ]

        if any(msg in output for msg in harmless_messages):
            return True, output or f"{script_path} skipped because no matching files were found."

        return result.returncode == 0, output or f"{script_path} completed."

    except Exception as e:
        return False, str(e)


def rebuild_knowledge_pipeline() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []

    cleanup_messages = clear_processed_artifacts()
    results.append(("Clear Processed Artifacts", True, "\n".join(cleanup_messages)))

    steps = [
        ("Ingest PDFs", "ingestion/ingest_pdfs.py"),
        ("Ingest Notes", "ingestion/ingest_notes.py"),
        ("Ingest Video Transcripts", "ingestion/ingest_videos.py"),
        ("Build Knowledge Base", "ingestion/build_knowledge_base.py"),
        ("Build Embeddings", "retrieval/build_embeddings.py"),
        ("Build FAISS Index", "retrieval/build_faiss_index.py"),
    ]

    stop_pipeline = False

    for step_name, script_path in steps:
        if stop_pipeline:
            results.append((step_name, False, "Skipped because a previous required step failed."))
            continue

        success, output = run_script(script_path)
        results.append((step_name, success, output))

        if not success:
            stop_pipeline = True

    return results
