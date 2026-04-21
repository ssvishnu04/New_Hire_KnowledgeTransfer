import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "app"))

from rag_pipeline import KnowledgeTransferRAG  # noqa: E402
from source_formatter import format_recommended_source  # noqa: E402
from admin_utils import rebuild_knowledge_pipeline  # noqa: E402
from file_upload_utils import save_uploaded_file, list_raw_files, delete_raw_file  # noqa: E402


st.set_page_config(
    page_title="New Hire Onboarding Assistant",
    page_icon="",
    layout="wide"
)

if "question_history" not in st.session_state:
    st.session_state.question_history = []


@st.cache_resource
def load_rag_pipeline():
    return KnowledgeTransferRAG()


def refresh_rag_pipeline():
    load_rag_pipeline.clear()


def choose_best_source(sources: list[dict]) -> dict | None:
    if not sources:
        return None

    for source in sources:
        if source.get("source_type") == "pdf":
            return source

    return sources[0]


def render_source_card(source: dict, index: int):
    with st.container():
        st.markdown(f"### Source {index}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.write(f"**Type:** {source.get('source_type', 'N/A')}")
            st.write(f"**File:** {source.get('file_name', 'N/A')}")
            st.write(f"**Title:** {source.get('title', 'N/A')}")
            st.write(f"**Score:** {source.get('score', 0):.4f}")

            if source.get("page_number"):
                st.write(f"**Page:** {source['page_number']}")

            if source.get("timestamp_markers"):
                timestamps = ", ".join(source["timestamp_markers"])
                st.write(f"**Timestamps:** {timestamps}")

        with col2:
            st.write("**Matched Text:**")
            st.info(source.get("text", ""))

        st.markdown("---")


def main():
    st.title("Knowledge Transfer AI Assistant")
    st.caption(
        "Help new hires learn faster by retrieving answers from company PDFs, notes, and video transcripts."
    )

    with st.sidebar:
        st.header("Search Settings")
        top_k = st.slider("Number of sources to retrieve", min_value=1, max_value=8, value=3)
        show_debug = st.checkbox("Show debug information", value=False)

        st.markdown("---")
        st.markdown("### Example Questions")
        st.markdown("- How do I request JIRA access?")
        st.markdown("- How do I submit employee expenses?")
        st.markdown("- What should I complete in my first week?")
        st.markdown("- How do I prepare for deployment?")
        st.markdown("- What do I do if I am blocked during onboarding?")

        st.markdown("---")
        st.markdown("### Recent Questions")
        if st.session_state.question_history:
            for q in st.session_state.question_history:
                st.markdown(f"- {q}")
        else:
            st.caption("No questions asked yet.")

    tab1, tab2 = st.tabs(["Knowledge Assistant", "Knowledge Management"])

    with tab1:
        rag = load_rag_pipeline()

        user_question = st.text_input(
            "Ask a question",
            placeholder="Example: How do I request JIRA access?"
        )

        ask_clicked = st.button("Get Answer")

        if ask_clicked:
            if not user_question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Searching company knowledge base and generating answer..."):
                    result = rag.answer_question(user_question=user_question, top_k=top_k)

                st.session_state.question_history.insert(0, user_question)
                st.session_state.question_history = st.session_state.question_history[:10]

                answer = result["answer"]
                sources = result["sources"]

                st.subheader("Answer")
                st.success(answer)

                best_source = choose_best_source(sources)

                st.subheader("Recommended Learning Asset")
                if best_source:
                    st.info(format_recommended_source(best_source))
                    st.write(
                        "**Why this source is useful:** "
                        "This source is the best available match for the question based on semantic retrieval."
                    )
                else:
                    st.warning("No relevant source was found.")

                st.subheader("Supporting Sources")
                if sources:
                    for i, source in enumerate(sources, start=1):
                        render_source_card(source, i)
                else:
                    st.warning("No supporting sources found.")

                if show_debug:
                    st.subheader("Debug Details")
                    st.write("**Question:**", result["question"])
                    st.write("**Retrieved Source Count:**", len(sources))

                    with st.expander("Prompt Sent to LLM"):
                        st.code(result["prompt"], language="text")

    with tab2:
        st.subheader("Upload New Company Knowledge")

        knowledge_type = st.selectbox(
            "Choose content type",
            ["PDF", "Note", "Video Transcript"]
        )

        uploaded_file = st.file_uploader(
            "Upload a file",
            type=["pdf", "txt", "md"],
            key="admin_upload"
        )

        if st.button("Save Uploaded File"):
            if uploaded_file is None:
                st.warning("Please upload a file first.")
            else:
                try:
                    if knowledge_type == "PDF":
                        category = "pdf"
                    elif knowledge_type == "Note":
                        category = "note"
                    else:
                        category = "video_transcript"

                    saved_path = save_uploaded_file(uploaded_file, category)
                    st.success(f"File saved successfully: {saved_path}")
                except Exception as e:
                    st.error(f"Failed to save file: {str(e)}")

        st.markdown("---")
        st.subheader("Manage Existing Knowledge Files")

        existing_files = list_raw_files()

        file_category_label = st.selectbox(
            "Choose category to manage",
            ["PDF", "Note", "Video Transcript"],
            key="manage_category"
        )

        if file_category_label == "PDF":
            manage_category = "pdf"
        elif file_category_label == "Note":
            manage_category = "note"
        else:
            manage_category = "video_transcript"

        current_files = existing_files.get(manage_category, [])

        if current_files:
            selected_file_to_delete = st.selectbox(
                "Select a file to delete",
                current_files,
                key="file_to_delete"
            )

            if st.button("Delete Selected File"):
                message = delete_raw_file(manage_category, selected_file_to_delete)
                st.success(message)
                st.info("Now click 'Rebuild Knowledge Pipeline' to remove it from search results.")
                st.rerun()
        else:
            st.caption("No files found in this category.")

        st.markdown("---")
        st.subheader("Rebuild Knowledge Base")

        st.write(
            "After uploading or deleting files, click the button below to rebuild the processed knowledge base, "
            "embeddings, and vector index."
        )

        if st.button("Rebuild Knowledge Pipeline"):
            with st.spinner("Rebuilding knowledge pipeline..."):
                results = rebuild_knowledge_pipeline()

            all_success = True
            for step_name, success, output in results:
                if success:
                    st.success(f"{step_name} completed.")
                else:
                    all_success = False
                    st.error(f"{step_name} failed.")

                with st.expander(f"Output: {step_name}"):
                    st.code(output if output else "No output", language="text")

            if all_success:
                refresh_rag_pipeline()
                st.success("Knowledge pipeline rebuilt successfully. New content is now searchable.")
            else:
                st.warning("Pipeline rebuild stopped because one of the steps failed.")


if __name__ == "__main__":
    main()
