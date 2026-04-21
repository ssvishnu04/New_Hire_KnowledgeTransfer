from rag_pipeline import KnowledgeTransferRAG


def print_sources(sources: list[dict]) -> None:
    print("\nRetrieved Sources:")
    print("-" * 80)

    for i, source in enumerate(sources, start=1):
        print(f"\nSource {i}")
        print(f"Type       : {source.get('source_type')}")
        print(f"File       : {source.get('file_name')}")
        print(f"Title      : {source.get('title')}")
        print(f"Page       : {source.get('page_number')}")
        print(f"Timestamps : {source.get('timestamp_markers', [])}")
        print(f"Score      : {source.get('score', 0):.4f}")
        print("Text:")
        print(source.get("text", ""))
        print("-" * 80)


def main() -> None:
    rag = KnowledgeTransferRAG()

    sample_questions = [
        "How do I request JIRA access?",
        "How do I submit employee expenses?",
        "What should I complete during the first week?",
        "How do I prepare for deployment?",
        "What should I do if I am blocked during onboarding?",
    ]

    for question in sample_questions:
        print("\n" + "=" * 100)
        print(f"QUESTION: {question}")
        print("=" * 100)

        result = rag.answer_question(question, top_k=3)

        print("\nAnswer:")
        print(result["answer"])

        print_sources(result["sources"])


if __name__ == "__main__":
    main()