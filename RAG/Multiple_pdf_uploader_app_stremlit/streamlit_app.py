import os
import streamlit as st

from Multi_RAG_utility import (
    process_documents_to_chroma_db,
    answer_question,
)

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Multi PDF RAG",
    page_icon="📄",
)

st.title("🦙 Llama-3.3-70B Document RAG")

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:

    file_paths = []

    for uploaded_file in uploaded_files:

        save_path = os.path.join(
            working_dir,
            uploaded_file.name,
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_paths.append(save_path)

    with st.spinner("Processing documents..."):
        process_documents_to_chroma_db(file_paths)

    st.success(f"{len(uploaded_files)} document(s) processed successfully!")

st.divider()

user_question = st.text_area(
    "Ask a question about the uploaded documents"
)

if st.button("Answer"):

    if not user_question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Generating answer..."):

            answer, sources = answer_question(user_question)

        st.markdown("## Answer")
        st.write(answer)

        st.markdown("### Source Documents")

        for source in sources:
            st.write(f"📄 {source}")