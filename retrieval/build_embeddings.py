import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_FILE = BASE_DIR / "data" / "processed" / "knowledge_base.json"
EMBEDDINGS_FILE = BASE_DIR / "data" / "processed" / "chunk_embeddings.npy"
METADATA_FILE = BASE_DIR / "data" / "processed" / "chunk_metadata.json"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def load_knowledge_base(file_path: Path) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    print("Loading knowledge base...")
    chunks = load_knowledge_base(KNOWLEDGE_BASE_FILE)

    if not chunks:
        raise ValueError("Knowledge base is empty. Please build the knowledge base first.")

    print(f"Loaded {len(chunks)} chunks.")

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    print(f"Embeddings shape: {embeddings.shape}")

    print(f"Saving embeddings to {EMBEDDINGS_FILE}")
    np.save(EMBEDDINGS_FILE, embeddings)

    print(f"Saving metadata to {METADATA_FILE}")
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print("Embedding generation complete.")


if __name__ == "__main__":
    main()
