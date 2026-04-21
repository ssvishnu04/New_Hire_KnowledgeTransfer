import sys
import subprocess
from pathlib import Path

# Base directory of project
BASE_DIR = Path(__file__).resolve().parent.parent

# Allow importing from retrieval/ and app/
sys.path.append(str(BASE_DIR / "retrieval"))
sys.path.append(str(BASE_DIR / "app"))

from search_index import KnowledgeRetriever  # noqa: E402
from prompt_templates import build_rag_prompt  # noqa: E402
from llm_client import call_groq_llm  # noqa: E402

INDEX_FILE = BASE_DIR / "data" / "processed" / "knowledge_index.faiss"
KNOWLEDGE_BASE_FILE = BASE_DIR / "data" / "processed" / "knowledge_base.json"
EMBEDDINGS_FILE = BASE_DIR / "data" / "processed" / "chunk_embeddings.npy"
METADATA_FILE = BASE_DIR / "data" / "processed" / "chunk_metadata.json"


def run_script(script_path: str) -> None:
    """
    Run a Python script from the project root.
    Raises an exception if the script fails.
    """
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Failed while running {script_path}\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )


def ensure_pipeline_ready() -> None:
    """
    Ensures the processed knowledge base artifacts exist.
    If missing, rebuilds the full ingestion + embedding + FAISS pipeline.
    """
    required_files = [
        KNOWLEDGE_BASE_FILE,
        EMBEDDINGS_FILE,
        METADATA_FILE,
        INDEX_FILE,
    ]

    all_exist = all(file_path.exists() for file_path in required_files)

    if all_exist:
        return

    print("Required processed files not found. Building pipeline...")

    steps = [
        "ingestion/ingest_pdfs.py",
        "ingestion/ingest_notes.py",
        "ingestion/ingest_videos.py",
        "ingestion/build_knowledge_base.py",
        "retrieval/build_embeddings.py",
        "retrieval/build_faiss_index.py",
    ]

    for step in steps:
        print(f"Running: {step}")
        run_script(step)

    print("Pipeline built successfully.")


class KnowledgeTransferRAG:
    def __init__(self) -> None:
        ensure_pipeline_ready()
        self.retriever = KnowledgeRetriever()

    def answer_question(self, user_question: str, top_k: int = 3) -> dict:
        retrieved_chunks = self.retriever.search(user_question, top_k=top_k)

        if not retrieved_chunks:
            return {
                "question": user_question,
                "answer": "I could not find that in the knowledge base.",
                "sources": [],
                "prompt": "",
            }

        prompt = build_rag_prompt(user_question, retrieved_chunks)
        answer = call_groq_llm(prompt)

        return {
            "question": user_question,
            "answer": answer,
            "sources": retrieved_chunks,
            "prompt": prompt,
        }
