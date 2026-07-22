import os
import shutil
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

load_dotenv()

working_dir = os.path.dirname(os.path.abspath(__file__))

embedding = HuggingFaceEmbeddings()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

VECTOR_DB = os.path.join(working_dir, "doc_vectorstore")


def process_documents_to_chroma_db(file_paths):
    """
    file_paths = list of PDF paths
    """

    all_documents = []

    for file in file_paths:
        loader = UnstructuredPDFLoader(file)
        docs = loader.load()

        # Add filename in metadata
        for doc in docs:
            doc.metadata["source"] = os.path.basename(file)

        all_documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
    )

    texts = splitter.split_documents(all_documents)

    vectordb = Chroma(
        persist_directory=VECTOR_DB,
        embedding_function=embedding,
    )

    vectordb.add_documents(texts)


def answer_question(question):

    vectordb = Chroma(
        persist_directory=VECTOR_DB,
        embedding_function=embedding,
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 4}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )

    response = qa_chain.invoke({"query": question})

    answer = response["result"]

    sources = list(
        {
            doc.metadata.get("source", "Unknown")
            for doc in response["source_documents"]
        }
    )

    return answer, sources