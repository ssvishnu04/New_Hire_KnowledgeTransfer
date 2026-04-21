from pathlib import Path

import faiss
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDINGS_FILE = BASE_DIR / "data" / "processed" / "chunk_embeddings.npy"
INDEX_FILE = BASE_DIR / "data" / "processed" / "knowledge_index.faiss"


def main() -> None:
    print("Loading embeddings...")
    embeddings = np.load(EMBEDDINGS_FILE)

    if embeddings.size == 0:
        raise ValueError("Embeddings file is empty.")

    print(f"Embeddings loaded with shape: {embeddings.shape}")

    dimension = embeddings.shape[1]

    print("Creating FAISS index...")
    index = faiss.IndexFlatIP(dimension)

    print("Adding embeddings to index...")
    index.add(embeddings)

    print(f"Saving FAISS index to {INDEX_FILE}")
    faiss.write_index(index, str(INDEX_FILE))

    print("FAISS index built successfully.")


if __name__ == "__main__":
    main()