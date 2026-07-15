This script is a **Document Ingestion Pipeline** for a **RAG (Retrieval-Augmented Generation)** application.

The purpose of this script is:

> **PDF Documents → Extract Text → Split into Chunks → Convert into Embeddings → Store in Vector Database (ChromaDB)**

Think of it as preparing books so that an AI can search them later.

---

# Overall Flow

```text
        PDF Files
            │
            ▼
  DirectoryLoader
            │
            ▼
  Extract Text from PDFs
            │
            ▼
 CharacterTextSplitter
            │
            ▼
  Small Text Chunks
            │
            ▼
 HuggingFace Embeddings
            │
            ▼
 Numerical Vectors
            │
            ▼
     Chroma Vector DB
```

Let's go through every line.

---

# Import Statements

```python
from langchain.document_loaders import DirectoryLoader
```

## What does this do?

Imports **DirectoryLoader** from LangChain.

DirectoryLoader is responsible for

* Opening a folder
* Finding files
* Passing each file to another loader

Imagine this folder

```
docs_dir/

invoice.pdf
book.pdf
resume.pdf
notes.pdf
```

Instead of loading every file manually,

```python
loader.load("invoice.pdf")
loader.load("book.pdf")
loader.load("resume.pdf")
```

DirectoryLoader automatically loads all files.

Think of it as

> "Open this folder and load every PDF."

---

```python
from langchain.document_loaders.unstructured import UnstructuredFileLoader
```

This imports a loader capable of reading many document types.

Examples

* PDF
* DOCX
* PPT
* TXT
* HTML

For PDFs,

it extracts text like

```
This is Chapter 1...
```

instead of binary PDF data.

Without this loader,

LangChain cannot understand PDF content.

---

```python
from langchain.text_splitters import CharacterTextSplitter
```

LLMs cannot process extremely large documents.

Example

Imagine a PDF containing

```
100 pages
```

You cannot send all 100 pages to GPT.

Instead

Split into

```
Page 1-3

Page 3-5

Page 5-7
```

This class performs that splitting.

---

```python
from langchain.embeddings import HuggingFaceEmbeddings
```

This imports an embedding model.

Embedding converts

```
"The capital of France is Paris."
```

into

```
[-0.124,
0.345,
0.832,
...768 numbers...]
```

AI understands numbers—not text.

Embeddings are those numbers.

---

```python
from langchain.vectorstores import Chroma
```

Imports Chroma Vector Database.

Instead of storing

```
Text
```

it stores

```
Embedding Vector
+
Original Text
+
Metadata
```

Example

| Text             | Vector          |
| ---------------- | --------------- |
| Kubernetes is... | [0.23,0.88,...] |

Later,

user asks

> Explain Kubernetes

Chroma finds similar vectors.

---

```python
import nltk
```

Imports the Natural Language Toolkit.

Although not used directly in this script, some loaders (like `UnstructuredFileLoader`) may rely on NLTK for sentence detection or tokenization.

---

# Configuration

```python
docs_dir_path = "/mnt/c/Practice/Gen-AI/RAG/6.2. RAG with LangChain/docs_dir"
```

This is the folder containing PDFs.

Example

```
docs_dir/

AWS.pdf

Docker.pdf

Kubernetes.pdf
```

---

```python
vector_db_path = "/mnt/c/Practice/Gen-AI/RAG/6.2. RAG with LangChain/vector_db"
```

This is where Chroma stores its database.

Think of it as

```
vector_db/

index files

embeddings

metadata
```

Instead of MySQL tables,

Chroma creates vector index files.

---

```python
collection_name = "document_collection"
```

A Chroma database can contain multiple collections.

Like SQL

```
Database

Customers

Orders

Employees
```

Chroma

```
Database

collection1

collection2

document_collection
```

---

# Loading Embedding Model

```python
embedding = HuggingFaceEmbeddings()
```

Loads the embedding model.

Internally it downloads a sentence transformer model (by default, depending on the LangChain version).

Later,

```
Text

↓

Embedding Model

↓

768-dimensional vector
```

Example

Input

```
Python is a programming language.
```

Output

```
[0.234,
-0.553,
0.782,
...
]
```

This vector represents the meaning of the sentence.

---

# Directory Loader

```python
loader = DirectoryLoader(
```

Creates a loader object.

---

```python
path=docs_dir_path,
```

Which folder?

```
docs_dir/
```

---

```python
glob="./*.pdf",
```

Only load PDFs.

Suppose folder contains

```
resume.pdf

book.pdf

notes.txt

image.png
```

Only these are loaded

```
resume.pdf

book.pdf
```

---

```python
loader_cls=UnstructuredFileLoader
```

For each PDF,

use

```
UnstructuredFileLoader
```

to extract text.

Think of it as

```
DirectoryLoader

↓

Find PDF

↓

Send PDF

↓

Unstructured Loader

↓

Extract text
```

---

# Load Documents

```python
documents = loader.load()
```

Now every PDF becomes a LangChain `Document` object.

Example

```
AWS.pdf
```

becomes

```python
Document(
page_content="Amazon Web Services is...",
metadata={
"source":"AWS.pdf"
}
)
```

If folder contains

```
AWS.pdf

Docker.pdf
```

Output

```python
[
Document(...),

Document(...)
]
```

---

```python
print(type(documents))
```

Output

```python
<class 'list'>
```

Because multiple documents are returned.

---

```python
len(documents)
```

Suppose

Folder contains

```
5 PDFs
```

Output

```
5
```

---

# Text Splitter

```python
text_splitter = CharacterTextSplitter(
```

Creates the splitter.

---

```python
chunk_size=2000,
```

Maximum chunk length

```
2000 characters
```

Example

Original

```
10000 characters
```

Becomes

```
Chunk1

2000 chars

Chunk2

2000 chars

Chunk3

2000 chars
...
```

---

```python
chunk_overlap=500
```

This is one of the most important settings.

Suppose

Chunk 1

```
Kubernetes manages containers.
Pods are scheduled...
```

Chunk 2

Starts 500 characters before the end of Chunk 1.

Visualization:

```text
Chunk 1

-----------------------------

ABCDEFGHIJKLMNOQRSTUVWXYZ

          overlap

          KLMNOQRSTUVWXYZ

-----------------------------

Chunk2

KLMNOQRSTUVWXYZ123456789
```

Why?

Because important context may span chunk boundaries.

Without overlap

```
Chunk1

The capital of France

Chunk2

is Paris
```

The answer gets split.

With overlap

```
Chunk1

The capital of France

is

Chunk2

France is Paris
```

Better retrieval.

---

# Split Documents

```python
text_chunks = text_splitter.split_documents(documents)
```

Suppose one PDF contains

```
100 pages
```

After splitting

```
150 chunks
```

Output

```
[
Document(chunk1),

Document(chunk2),

Document(chunk3)
]
```

Each chunk is still a `Document` object with its own text and metadata.

---

```python
len(text_chunks)
```

Suppose

```
3 PDFs
```

Each creates

```
50 chunks
```

Total

```
150
```

---

# Create Vector Store

```python
vector_store = Chroma.from_documents(
```

This is the most important step.

Pipeline:

```
Text Chunk

↓

Embedding Model

↓

Vector

↓

Store in Chroma
```

---

```python
documents=text_chunks,
```

Input

```
All chunks
```

Example

```
Chunk1

Chunk2

Chunk3

...
```

---

```python
embedding=embedding,
```

For every chunk,

call

```
Embedding Model
```

Example

```
"Kubernetes"

↓

[0.45,0.22,...]
```

---

```python
persist_directory=vector_db_path,
```

Save the database to disk.

Without this,

everything stays only in memory and is lost when the program exits.

---

```python
collection_name=collection_name
```

Store vectors inside

```
document_collection
```

---

# What happens internally?

Imagine you have two PDFs:

```
AWS.pdf

Kubernetes.pdf
```

### Step 1 – Load

```text
AWS.pdf
↓

Document
```

```text
Kubernetes.pdf
↓

Document
```

---

### Step 2 – Split

```text
AWS Chunk 1

AWS Chunk 2

AWS Chunk 3

Kubernetes Chunk 1

Kubernetes Chunk 2
```

---

### Step 3 – Embedding

```text
Chunk

↓

Embedding Model

↓

[0.23,0.67,...]
```

Each chunk becomes a high-dimensional vector.

---

### Step 4 – Save

Chroma stores something conceptually like this:

| Chunk                          | Embedding         | Metadata              |
| ------------------------------ | ----------------- | --------------------- |
| AWS EC2 is a virtual server... | [0.12, 0.55, ...] | source=AWS.pdf        |
| Kubernetes Pods are...         | [0.78, 0.31, ...] | source=Kubernetes.pdf |

When a user later asks:

> "What is EC2?"

the query is also converted into an embedding vector. Chroma performs a similarity search (often using cosine similarity or another distance metric) to find the stored vectors closest to the query vector, retrieves the corresponding chunks, and passes them to the LLM as context. This is the core of a RAG application.

## Summary of each component

| Component                | Purpose                                                              | Example                                                    |
| ------------------------ | -------------------------------------------------------------------- | ---------------------------------------------------------- |
| `DirectoryLoader`        | Finds files in a folder                                              | Loads all PDFs from `docs_dir`                             |
| `UnstructuredFileLoader` | Extracts text from each file                                         | Reads text from a PDF                                      |
| `CharacterTextSplitter`  | Splits long documents into manageable chunks                         | 10,000-character document → several 2,000-character chunks |
| `HuggingFaceEmbeddings`  | Converts each chunk into a numerical vector representing its meaning | `"Kubernetes manages containers"` → `[0.23, -0.41, ...]`   |
| `Chroma`                 | Stores vectors and associated metadata for fast semantic search      | Saves embeddings to `vector_db/document_collection`        |

**second half of the RAG (Retrieval-Augmented Generation) pipeline**.

In the previous script, you performed **Document Ingestion**:

```text
PDF Files
      ↓
Load Documents
      ↓
Split into Chunks
      ↓
Create Embeddings
      ↓
Store in Chroma Vector DB
```

This script performs **Question Answering**:

```text
User Question
      ↓
Convert Question to Embedding
      ↓
Search Chroma Vector DB
      ↓
Retrieve Relevant Chunks
      ↓
Send Chunks + Question to Llama 3.1
      ↓
Generate Final Answer
```

---

# Complete Architecture

```text
                    DOCUMENT INGESTION (Previous Script)

PDF Files
      │
      ▼
Directory Loader
      │
      ▼
Extract Text
      │
      ▼
Split into Chunks
      │
      ▼
HuggingFace Embeddings
      │
      ▼
Chroma Vector Database
══════════════════════════════════════════════════════════════════════

                    QUESTION ANSWERING (Current Script)

User Question
      │
      ▼
Embedding Model
      │
      ▼
Search Chroma DB
      │
      ▼
Top Similar Chunks
      │
      ▼
Llama 3.1 (Groq)
      │
      ▼
Final Answer
```

Now let's go line by line.

---

# Import Libraries

```python
import os
```

## Purpose

Imports Python's built-in Operating System module.

It is mainly used here to store the API key.

Example

```python
os.environ["GROQ_API_KEY"] = "abc123"
```

This creates an environment variable.

Instead of writing

```python
api_key="abc123"
```

inside the code, environment variables keep secrets separate from your application logic.

---

```python
from langchain_chroma import Chroma
```

Imports the **Chroma Vector Database**.

Remember from the previous script:

```
PDF

↓

Embedding

↓

Chroma Database
```

Now we want to **read** from that database.

Think of Chroma like a library:

```
Books

↓

Stored on shelves

↓

Later searched
```

---

```python
from langchain_huggingface import HuggingFaceEmbeddings
```

Imports the same embedding model used during ingestion.

### Why must we use the same embedding model?

Suppose during ingestion we stored vectors like

```
Sentence

↓

Model A

↓

[0.21 0.44 0.98]
```

Later the user asks

```
Question

↓

Model B

↓

[7.88 1.44 9.55]
```

The vector spaces are different, so similarity search will fail.

**Rule:** Use the same embedding model for both indexing and querying.

---

```python
from langchain_groq import ChatGroq
```

Imports the Groq LLM wrapper.

Groq provides extremely fast inference for open-weight models like:

* Llama 3.1
* Gemma
* Mixtral

Without Groq, you could instead use:

```python
ChatOpenAI()
```

or

```python
Ollama()
```

The rest of the RAG flow remains largely the same.

---

```python
from langchain_classic.chains import RetrievalQA
```

Imports a prebuilt RAG chain.

Instead of manually writing:

1. Retrieve documents
2. Build prompt
3. Call LLM
4. Parse answer

`RetrievalQA` handles all these steps for you.

Think of it as a workflow manager.

---

# API Key

```python
os.environ["GROQ_API_KEY"] = ""
```

Groq requires authentication.

Normally you would write:

```python
os.environ["GROQ_API_KEY"]="gsk_xxxxxxxxx"
```

The library automatically reads this environment variable when making API requests.

---

# Configuration

```python
vector_db_path = "/Volumes/.../vector_db"
```

This points to the Chroma database created by the ingestion script.

Think of it as opening an existing database.

```
vector_db/

chroma.sqlite3

index/

embeddings/
```

---

```python
collection_name="document_collection"
```

This must match the collection name used during ingestion.

If ingestion stored data in:

```
document_collection
```

but retrieval looks for:

```
books_collection
```

nothing will be found.

---

# Load Embedding Model

```python
embedding = HuggingFaceEmbeddings()
```

Loads the embedding model again.

This model converts the user's question into a vector.

Example:

Question:

```
What is Adaptive Radiation?
```

↓

Embedding

↓

```
[0.234,
-0.543,
...
]
```

This vector is used to search the database.

---

# Initialize LLM

```python
llm = ChatGroq(
```

Creates the LLM object.

---

```python
model="llama-3.1-8b-instant",
```

Uses Meta's Llama 3.1 8B Instant model hosted on Groq.

This model generates the final answer.

It does **not** search documents.

It only answers using the retrieved context.

---

```python
temperature=0.0
```

Controls randomness.

### Temperature = 0

Always gives the most deterministic answer.

Example:

Question:

```
Capital of France?
```

Output every time:

```
Paris
```

---

Temperature = 1

Might produce:

```
Paris

The capital city of France is Paris.

France's beautiful capital is Paris.
```

Higher values increase creativity but reduce consistency.

For RAG, `0.0` is a common choice because factual accuracy is preferred.

---

# Connect to Chroma

```python
vector_store = Chroma(
```

This opens the existing vector database.

---

```python
collection_name=collection_name,
```

Which collection?

```
document_collection
```

---

```python
embedding_function=embedding,
```

Used to embed user queries.

Important: It does **not** re-embed all stored documents. The document embeddings already exist. This embedding function is primarily used to convert incoming search queries into vectors in the same embedding space.

---

```python
persist_directory=vector_db_path
```

Location of the stored vectors.

---

Internally, it opens something like:

```
vector_db/

index files

vectors

metadata
```

---

# Create Retriever

```python
retriever = vector_store.as_retriever()
```

This is one of the most important lines.

Without a retriever:

```
Question

↓

LLM
```

The LLM only knows its training data.

With a retriever:

```
Question

↓

Vector Search

↓

Relevant Chunks

↓

LLM
```

The retriever's job is:

1. Embed the question.
2. Search Chroma for similar vectors.
3. Return the most relevant document chunks.

You can also configure it, for example:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)
```

This returns the top 3 matching chunks instead of the default.

---

# Create Retrieval QA Chain

```python
qa_chain = RetrievalQA.from_chain_type(
```

Builds the complete RAG pipeline.

---

```python
llm=llm,
```

Use Groq Llama.

---

```python
chain_type="stuff",
```

One of LangChain's document-combining strategies.

### What does "stuff" mean?

Suppose retrieval returns:

```
Chunk 1

Chunk 2

Chunk 3
```

The "stuff" chain simply concatenates all retrieved chunks into one prompt:

```
Context:

Chunk 1

Chunk 2

Chunk 3

Question:
What is Adaptive Radiation?
```

Then it sends that single prompt to the LLM.

This works well when the total context fits within the model's context window.

Other chain types include:

| Chain Type   | Purpose                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------- |
| `stuff`      | Put all retrieved chunks into one prompt (simple and common).                            |
| `map_reduce` | Answer each chunk separately, then combine the answers. Useful for very large documents. |
| `refine`     | Build the answer incrementally, refining it with each additional chunk.                  |
| `map_rerank` | Answer each chunk and score the answers, then choose the best one.                       |

---

```python
retriever=retriever,
```

Connects the retriever.

Flow:

```
Question

↓

Retriever

↓

Relevant Chunks

↓

LLM
```

---

```python
return_source_documents=True
```

This tells LangChain to return:

* the generated answer, **and**
* the retrieved source documents.

Without it:

```python
{
   "result":"..."
}
```

With it:

```python
{
   "result":"...",
   "source_documents":[...]
}
```

This is useful for transparency and debugging.

---

# User Query

```python
query = "What does the document say about Adaptive Radiation?"
```

User asks a question.

---

# Invoke the Chain

```python
response = qa_chain.invoke({"query":query})
```

This single line performs multiple operations internally.

## Internal Workflow

### Step 1

Convert the question into an embedding.

```
Question

↓

Embedding Model

↓

Vector
```

---

### Step 2

Search Chroma.

```
Question Vector

↓

Similarity Search

↓

Top Matching Chunks
```

---

### Step 3

Construct the prompt.

```
Context:

Chunk 1

Chunk 2

Chunk 3

Question:

What does the document say about Adaptive Radiation?
```

---

### Step 4

Send the prompt to Llama.

---

### Step 5

Receive the generated answer.

---

# Print the Answer

```python
print(response["result"])
```

Possible output:

```
Adaptive radiation is the evolutionary process where one ancestral species diversifies into multiple species, each adapted to different ecological niches.
```

---

```python
print("-"*80)
```

Prints a separator line:

```
--------------------------------------------------------------------------------
```

This improves readability.

---

# Print Source Metadata

```python
for source in response["source_documents"]:
```

Loops through all retrieved chunks.

Each `source` is a LangChain `Document` object.

---

```python
print(source.metadata)
```

Example output:

```python
{
 "source":"biology.pdf",
 "page":12
}
```

If multiple chunks are retrieved:

```python
{
 "source":"biology.pdf",
 "page":12
}

{
 "source":"biology.pdf",
 "page":13
}
```

This helps you verify where the answer came from and is useful for citations or debugging retrieval quality.

## End-to-end execution flow

```text
                         USER
                           │
                           ▼
"What does the document say about Adaptive Radiation?"
                           │
                           ▼
              HuggingFace Embeddings
                           │
                           ▼
                  Question Vector
                           │
                           ▼
                    Chroma Vector DB
                           │
             Similarity Search (e.g., cosine similarity)
                           │
                           ▼
            Top Matching Document Chunks
                           │
                           ▼
 RetrievalQA ("stuff" chain builds the prompt)
                           │
                           ▼
                    ChatGroq (Llama 3.1)
                           │
                           ▼
                 Generated Answer + Sources
                           │
                           ▼
                     Printed to Console
```

### Summary of each component

| Component                           | Role                                                 | Input                                  | Output                                  |
| ----------------------------------- | ---------------------------------------------------- | -------------------------------------- | --------------------------------------- |
| `HuggingFaceEmbeddings`             | Converts the user's question into a vector           | Question text                          | Query embedding                         |
| `Chroma`                            | Stores and searches document embeddings              | Query embedding                        | Most similar document chunks            |
| `Retriever`                         | Provides a retrieval interface over the vector store | Question                               | Relevant chunks                         |
| `RetrievalQA`                       | Orchestrates retrieval and LLM prompting             | Question + retrieved chunks            | Final answer                            |
| `ChatGroq` (`llama-3.1-8b-instant`) | Generates the natural-language response              | Prompt containing context and question | Answer                                  |
| `return_source_documents=True`      | Returns the retrieved evidence along with the answer | Retrieved chunks                       | Source `Document` objects with metadata |


