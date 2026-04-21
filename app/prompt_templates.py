def build_rag_prompt(user_question: str, retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        source_type = chunk.get("source_type", "unknown")
        file_name = chunk.get("file_name", "unknown_file")
        page_number = chunk.get("page_number")
        timestamps = chunk.get("timestamp_markers", [])

        source_label = f"{source_type.upper()} | {file_name}"
        if page_number:
            source_label += f" | Page {page_number}"
        if timestamps:
            source_label += f" | Timestamps: {', '.join(timestamps)}"

        context_blocks.append(
            f"[Source {i}] {source_label}\n{chunk['text']}"
        )

    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are an AI onboarding and knowledge transfer assistant for a company.

Your job is to help new hires by answering questions only from the provided company knowledge context.

Rules:
1. Answer only from the provided context.
2. If the answer is not clearly in the context, say: "I could not find that in the knowledge base."
3. Be concise, helpful, and professional.
4. At the end, include:
   - "Recommended Source"
   - "Why this source is useful"
5. Mention the source number(s) you used, such as [Source 1], [Source 2].

User Question:
{user_question}

Company Knowledge Context:
{context_text}

Now provide:
1. Answer
2. Recommended Source
3. Why this source is useful
""".strip()

    return prompt
