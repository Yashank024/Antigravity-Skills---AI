# Vector Database Integration Guide

## Overview

Vector databases store high-dimensional embeddings (float arrays) and enable 
semantic similarity search — the backbone of RAG systems, recommendation engines, 
and semantic search.

---

## Quick Start by Use Case

| You Need | Use | Why |
|---------|-----|-----|
| Just prototyping | **Chroma** | Zero setup, runs in-process |
| Already using Postgres | **pgvector** | No new infrastructure |
| Production RAG | **Pinecone** | Managed, auto-scales, zero ops |
| Hybrid search (keyword + vector) | **Weaviate** | BM25 + vector out of the box |
| High performance + filtering | **Qdrant** | Rust-based, fast payload filtering |
| Enterprise scale | **Milvus** | Billions of vectors, GPU acceleration |

---

## 1. Chroma — Local Development (Zero Setup)

```bash
pip install chromadb
```

```python
import chromadb
from chromadb.utils import embedding_functions

# Use OpenAI embeddings (or any)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-3-small"
)

# Persistent local store
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"}  # cosine similarity
)

# Add documents (embeddings generated automatically)
collection.add(
    documents=["Python is a programming language", "FastAPI is a web framework"],
    metadatas=[{"source": "docs.txt", "page": 1}, {"source": "docs.txt", "page": 2}],
    ids=["doc_1", "doc_2"]
)

# Query
results = collection.query(
    query_texts=["What language should I learn for web development?"],
    n_results=3,
    where={"source": "docs.txt"},       # Optional metadata filter
    include=["documents", "metadatas", "distances"]
)

for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"Score: {1-dist:.3f} | Source: {meta['source']} | {doc[:80]}")
```

---

## 2. Pinecone — Production Cloud

```bash
pip install pinecone
```

```python
from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Create index (one-time)
if "knowledge-base" not in pc.list_indexes().names():
    pc.create_index(
        name="knowledge-base",
        dimension=3072,              # Must match your embedding model
        metric="cosine",             # cosine, euclidean, or dotproduct
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index("knowledge-base")

# Upsert vectors
def upsert_documents(chunks: list[str], embeddings: list[list], source: str):
    vectors = [
        {
            "id": f"{source}_{i}",
            "values": embedding,
            "metadata": {
                "text": chunk,
                "source": source,
                "timestamp": datetime.now().isoformat()
            }
        }
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]
    # Batch upsert (max 100 per call)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i+batch_size], namespace="v1")

# Query with metadata filtering
def semantic_search(query_embedding: list, k: int = 10,
                    source_filter: list | None = None) -> list:
    filter_dict = {}
    if source_filter:
        filter_dict["source"] = {"$in": source_filter}
    
    results = index.query(
        vector=query_embedding,
        top_k=k,
        include_metadata=True,
        namespace="v1",
        filter=filter_dict if filter_dict else None
    )
    return [
        {"text": m.metadata["text"], "source": m.metadata["source"], "score": m.score}
        for m in results.matches
    ]

# Stats
print(index.describe_index_stats())  # Total vector count, namespaces
```

---

## 3. pgvector — PostgreSQL Extension

Best for: teams already using PostgreSQL who want semantic search without new infrastructure.

```sql
-- Enable extension (one time, requires postgres 13+)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id          SERIAL PRIMARY KEY,
    content     TEXT NOT NULL,
    embedding   VECTOR(1536),          -- Match your embedding model dimensions
    source      TEXT,
    section     TEXT,
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Create HNSW index for fast approximate nearest neighbor search
-- (Much faster than exact search for large datasets)
CREATE INDEX ON documents 
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Insert with embedding
INSERT INTO documents (content, embedding, source)
VALUES ($1, $2::vector, $3);

-- Semantic search: find top-10 most similar
SELECT 
    content,
    source,
    1 - (embedding <=> $1::vector) AS similarity
FROM documents
ORDER BY embedding <=> $1::vector   -- <=> is cosine distance operator
LIMIT 10;

-- Hybrid search: combine semantic + full-text (BM25-like)
SELECT 
    content,
    source,
    ts_rank(to_tsvector('english', content), plainto_tsquery('english', $2)) AS keyword_score,
    1 - (embedding <=> $1::vector) AS semantic_score,
    -- Combine both scores (adjust weights as needed)
    0.5 * ts_rank(to_tsvector('english', content), plainto_tsquery('english', $2)) +
    0.5 * (1 - (embedding <=> $1::vector)) AS combined_score
FROM documents
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', $2)  -- Keyword pre-filter
ORDER BY combined_score DESC
LIMIT 10;
```

```python
# Python with psycopg2
import psycopg2
import json

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

def insert_document(content: str, embedding: list, source: str):
    cur.execute(
        "INSERT INTO documents (content, embedding, source) VALUES (%s, %s, %s)",
        (content, embedding, source)
    )
    conn.commit()

def search_documents(query_embedding: list, k: int = 10, source: str = None) -> list:
    if source:
        cur.execute(
            """SELECT content, source, 1-(embedding <=> %s::vector) AS sim
               FROM documents WHERE source = %s
               ORDER BY embedding <=> %s::vector LIMIT %s""",
            (query_embedding, source, query_embedding, k)
        )
    else:
        cur.execute(
            """SELECT content, source, 1-(embedding <=> %s::vector) AS sim
               FROM documents ORDER BY embedding <=> %s::vector LIMIT %s""",
            (query_embedding, query_embedding, k)
        )
    return [{"content": r[0], "source": r[1], "similarity": r[2]} for r in cur.fetchall()]
```

---

## 4. Qdrant — High Performance + Advanced Filtering

```bash
pip install qdrant-client
# Or run: docker run -p 6333:6333 qdrant/qdrant
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)

client = QdrantClient(url="http://localhost:6333")

# Create collection
client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
)

# Upsert points
client.upsert(
    collection_name="knowledge_base",
    points=[
        PointStruct(
            id=i,
            vector=embedding,
            payload={"text": chunk, "source": source, "page": page}
        )
        for i, (chunk, embedding, source, page) in enumerate(data)
    ]
)

# Search with filtering
results = client.search(
    collection_name="knowledge_base",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="source", match=MatchValue(value="manual.pdf")),
        ]
    ),
    limit=10,
    with_payload=True,
)

for r in results:
    print(f"Score: {r.score:.3f} | {r.payload['text'][:100]}")
```

---

## 5. Weaviate — Hybrid Search (BM25 + Vector)

```bash
pip install weaviate-client
```

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_local()

# Create schema
collection = client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-small"
    ),
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
    ]
)

# Insert (auto-vectorizes)
collection.data.insert({"content": "Python is great", "source": "docs.txt"})

# Hybrid search (BM25 + vector combined)
results = collection.query.hybrid(
    query="programming language web development",
    alpha=0.5,    # 0=pure BM25, 1=pure vector, 0.5=balanced
    limit=10,
)

for item in results.objects:
    print(item.properties)
```

---

## Production Best Practices

### Namespace / Tenant Isolation
```python
# Pinecone: use namespaces per customer
index.upsert(vectors=vectors, namespace=f"tenant_{org_id}")
results = index.query(vector=q, namespace=f"tenant_{org_id}")

# Qdrant: use separate collections or payload filtering
# Chroma: use separate collections
# pgvector: add org_id column and filter in WHERE clause
```

### Embedding Model Consistency
```python
# CRITICAL: Use the SAME embedding model for indexing AND querying
# Mixing models = garbage results
EMBEDDING_MODEL = "text-embedding-3-large"  # Lock this in and never change

def embed_for_index(text: str) -> list:
    return client.embeddings.create(model=EMBEDDING_MODEL, input=text).data[0].embedding

def embed_for_query(text: str) -> list:
    return embed_for_index(text)  # Same function = same model guaranteed
```

### Indexing Pipeline with Error Handling
```python
def index_documents_safely(documents: list[Document], batch_size: int = 50) -> dict:
    """Index documents with retry and error tracking."""
    success = 0
    failed = []
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        try:
            texts = [d.content for d in batch]
            embeddings = embed(texts)
            # ... upsert to your DB
            success += len(batch)
        except Exception as e:
            failed.extend([d.source for d in batch])
            logger.error(f"Batch {i//batch_size} failed: {e}")
    
    return {"success": success, "failed": failed}
```
