import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def run_script(script_path: str) -> tuple[bool, str]:
    """
    Runs a Python script and returns:
    (success, output_message)
    """
    try:
        result = subprocess.run(
            ["python", script_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout.strip() or f"{script_path} completed successfully."
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() or e.stdout.strip() or str(e)
        return False, error_message


def rebuild_knowledge_pipeline() -> list[tuple[str, bool, str]]:
    steps = [
        ("Ingest PDFs", "ingestion/ingest_pdfs.py"),
        ("Ingest Notes", "ingestion/ingest_notes.py"),
        ("Ingest Video Transcripts", "ingestion/ingest_videos.py"),
        ("Build Knowledge Base", "ingestion/build_knowledge_base.py"),
        ("Build Embeddings", "retrieval/build_embeddings.py"),
        ("Build FAISS Index", "retrieval/build_faiss_index.py"),
    ]

    results = []

    for step_name, script_path in steps:
        success, output = run_script(script_path)
        results.append((step_name, success, output))
        if not success:
            break

    return results