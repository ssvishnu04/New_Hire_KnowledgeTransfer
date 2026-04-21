def format_recommended_source(source: dict) -> str:
    source_type = source.get("source_type", "unknown")
    file_name = source.get("file_name", "unknown_file")
    page_number = source.get("page_number")
    timestamps = source.get("timestamp_markers", [])

    if source_type == "pdf":
        return f"PDF: {file_name} (Page {page_number})"

    if source_type == "video_transcript":
        if timestamps:
            return f"Video Transcript: {file_name} (Relevant timestamps: {', '.join(timestamps)})"
        return f"Video Transcript: {file_name}"

    if source_type == "note":
        return f"Note: {file_name}"

    return f"{source_type}: {file_name}"
