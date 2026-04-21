import sys
from pathlib import Path

# Allow importing from retrieval/
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "retrieval"))

from search_index import KnowledgeRetriever  # noqa: E402
from prompt_templates import build_rag_prompt  # noqa: E402
from llm_client import call_groq_llm  # noqa: E402


class KnowledgeTransferRAG:
    def __init__(self) -> None:
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