import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
# langchain library has been restructured recently. Use langchain_classic for older imports as mentioned below.
from langchain_classic.chains import RetrievalQA

os.environ["GROQ_API_KEY"] = ""

# configuration
vector_db_path = "/Volumes/MyDrive/3_udemy/1_gen_ai_bonus/fix_code/6.2. RAG with LangChain/vector_db"
collection_name  = "document_collection"

# loading the embedding model - default model
embedding = HuggingFaceEmbeddings()

# initialize groq llm
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0
)

vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embedding,
    persist_directory=vector_db_path
)

retriever = vector_store.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

query = "What does the document say about Adaptive Radiation?"
response = qa_chain.invoke({"query":query})
print(response["result"])
print("-"*80)
for source in response["source_documents"]:
    print(source.metadata)