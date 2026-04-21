import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def run_script(script_path: str) -> tuple[bool, str]:
    """
    Runs a Python script from the project root and returns:
    (success, combined_output)

    Rules:
    - Missing source files (for example, no PDFs) are treated as a valid non-failure state
    - Any real execution failure returns success=False
    """
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
    """
    Rebuilds the full knowledge pipeline.

    Important behavior:
    - If one ingestion source has no files, pipeline continues
    - Only true script failures are treated as failures
    - Pipeline does NOT stop for harmless "no files found" conditions
    """
    steps = [
        ("Ingest PDFs", "ingestion/ingest_pdfs.py"),
        ("Ingest Notes", "ingestion/ingest_notes.py"),
        ("Ingest Video Transcripts", "ingestion/ingest_videos.py"),
        ("Build Knowledge Base", "ingestion/build_knowledge_base.py"),
        ("Build Embeddings", "retrieval/build_embeddings.py"),
        ("Build FAISS Index", "retrieval/build_faiss_index.py"),
    ]

    results: list[tuple[str, bool, str]] = []
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
