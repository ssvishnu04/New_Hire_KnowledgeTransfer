from search_index import KnowledgeRetriever


def print_results(query: str, results: list[dict]) -> None:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Score       : {result['score']:.4f}")
        print(f"Source Type : {result['source_type']}")
        print(f"File Name   : {result['file_name']}")
        print(f"Title       : {result['title']}")
        print(f"Page Number : {result.get('page_number')}")
        print(f"Chunk ID    : {result['chunk_id']}")
        if result.get("timestamp_markers"):
            print(f"Timestamps  : {result['timestamp_markers']}")
        print("Text:")
        print(result["text"])
        print("-" * 80)


def main() -> None:
    retriever = KnowledgeRetriever()

    sample_queries = [
        "How do I request JIRA access?",
        "How do I submit reimbursable expenses?",
        "What should I focus on during my first week?",
        "How do I prepare for deployment?",
        "Who should I contact if I am blocked during onboarding?",
    ]

    for query in sample_queries:
        results = retriever.search(query, top_k=3)
        print_results(query, results)


if __name__ == "__main__":
    main()