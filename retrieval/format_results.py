def format_source_label(result: dict) -> str:
    source_type = result.get("source_type", "unknown")
    file_name = result.get("file_name", "unknown_file")

    if source_type == "pdf":
        page = result.get("page_number")
        return f"PDF: {file_name} (Page {page})"

    if source_type == "video_transcript":
        timestamps = result.get("timestamp_markers", [])
        if timestamps:
            return f"Video Transcript: {file_name} (Timestamps: {', '.join(timestamps)})"
        return f"Video Transcript: {file_name}"

    if source_type == "note":
        return f"Note: {file_name}"

    return f"{source_type}: {file_name}"
