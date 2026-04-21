import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "data" / "processed" / "knowledge_index.faiss"
METADATA_FILE = BASE_DIR / "data" / "processed" / "chunk_metadata.json"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"


class KnowledgeRetriever:
    def __init__(self) -> None:
        print("Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        print("Loading FAISS index...")
        self.index = faiss.read_index(str(INDEX_FILE))

        print("Loading metadata...")
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            item = self.metadata[idx].copy()
            item["score"] = float(score)
            results.append(item)

        return results