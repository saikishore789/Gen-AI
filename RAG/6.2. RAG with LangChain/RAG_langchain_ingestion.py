from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import nltk


# configuration
docs_dir_path = "/mnt/c/Practice/Gen-AI/RAG/6.2. RAG with LangChain/docs_dir"
vector_db_path = "/mnt/c/Practice/Gen-AI/RAG/6.2. RAG with LangChain/vector_db"
collection_name  = "document_collection"

# loading the embedding model
embedding = HuggingFaceEmbeddings()

# directory loader
loader = DirectoryLoader(
    path=docs_dir_path,
    glob="./*.pdf",
    loader_cls=UnstructuredFileLoader
)

# single file can also be loaded with UnstructuredFileLoader

# load the documents
documents = loader.load()

print(type(documents))

len(documents)

# initializing the text splitter
text_splitter = CharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=500
)

# splitting the text into smaller chunks
text_chunks = text_splitter.split_documents(documents)

len(text_chunks)

# creating the vector store
vector_store = Chroma.from_documents(
    documents=text_chunks,
    embedding=embedding,
    persist_directory=vector_db_path,
    collection_name=collection_name
)