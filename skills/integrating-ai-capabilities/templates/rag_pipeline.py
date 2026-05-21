"""
RAG Pipeline — Production Template
Complete Retrieval-Augmented Generation implementation.
Supports: OpenAI embeddings + in-memory store (replace with Pinecone/pgvector for prod).
"""

import os
import json
import numpy as np
from openai import OpenAI
from dataclasses import dataclass, field
from typing import Optional
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ─── Data Types ───────────────────────────────────────────────────────────────
@dataclass
class Document:
    """A document chunk with metadata."""
    content: str
    source: str
    page: Optional[int] = None
    section: Optional[str] = None
    metadata: dict = field(default_factory=dict)

@dataclass
class RAGResult:
    """Result from a RAG query."""
    answer: str
    sources: list[Document]
    confidence: str  # "high", "medium", "low"
    tokens_used: int

# ─── Chunking ─────────────────────────────────────────────────────────────────
def chunk_text(text: str,
               chunk_size: int = 400,
               overlap: int = 50,
               source: str = "unknown") -> list[Document]:
    """
    Split text into overlapping chunks for RAG indexing.
    Tries to split at sentence boundaries for better coherence.
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        
        # Try to split at sentence boundary
        last_period = chunk_text.rfind(". ")
        if last_period > chunk_size * 0.5:
            end = start + last_period + 1
            chunk_text = text[start:end]
        
        if chunk_text.strip():
            chunks.append(Document(content=chunk_text.strip(), source=source))
        
        start = end - overlap
    
    logger.info(f"Chunked '{source}' into {len(chunks)} chunks")
    return chunks

# ─── Embeddings ───────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "text-embedding-3-large"  # 3072 dims, highest quality
# Cheaper alternative: "text-embedding-3-small" (1536 dims, $0.02/M)

def embed(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts. Batches automatically."""
    # OpenAI supports up to 2048 texts per call
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        resp = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        all_embeddings.extend([r.embedding for r in resp.data])
    
    return all_embeddings

# ─── Vector Store ─────────────────────────────────────────────────────────────
class VectorStore:
    """
    In-memory vector store for development/small-scale use.
    For production, replace with: Pinecone, pgvector, Qdrant, or Chroma.
    """
    
    def __init__(self):
        self.documents: list[Document] = []
        self.vectors: list[list[float]] = []
    
    def add_documents(self, documents: list[Document]) -> None:
        """Embed and store documents."""
        logger.info(f"Indexing {len(documents)} documents...")
        texts = [doc.content for doc in documents]
        embeddings = embed(texts)
        self.documents.extend(documents)
        self.vectors.extend(embeddings)
        logger.info(f"Total documents indexed: {len(self.documents)}")
    
    def add_text(self, text: str, source: str = "unknown",
                 chunk_size: int = 400, overlap: int = 50) -> None:
        """Chunk text and add to store."""
        chunks = chunk_text(text, chunk_size, overlap, source)
        self.add_documents(chunks)
    
    def search(self, query: str, k: int = 5) -> list[tuple[Document, float]]:
        """Semantic search — returns (document, similarity_score) pairs."""
        if not self.vectors:
            return []
        
        q_vec = np.array(embed([query])[0])
        scores = []
        
        for i, vec in enumerate(self.vectors):
            v = np.array(vec)
            sim = np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v))
            scores.append((i, sim))
        
        top_k = sorted(scores, key=lambda x: -x[1])[:k]
        return [(self.documents[i], score) for i, score in top_k]
    
    def save(self, path: str) -> None:
        """Persist store to disk."""
        data = {
            "documents": [
                {"content": d.content, "source": d.source,
                 "page": d.page, "section": d.section, "metadata": d.metadata}
                for d in self.documents
            ],
            "vectors": self.vectors
        }
        with open(path, "w") as f:
            json.dump(data, f)
        logger.info(f"Store saved to {path}")
    
    def load(self, path: str) -> None:
        """Load store from disk."""
        with open(path) as f:
            data = json.load(f)
        self.documents = [Document(**d) for d in data["documents"]]
        self.vectors = data["vectors"]
        logger.info(f"Loaded {len(self.documents)} documents from {path}")

# ─── RAG Query ────────────────────────────────────────────────────────────────
RAG_SYSTEM = """You are a precise Q&A assistant with access to a specific knowledge base.

STRICT RULES:
- Answer ONLY from the provided context documents
- If the answer is NOT in the context, say: "I don't have that information in the provided documents."
- Always cite which source you used (by source name)
- Never speculate, guess, or use outside knowledge
- If context is partially relevant, answer what you can and note the gaps"""

def rag_query(question: str,
              store: VectorStore,
              k: int = 5,
              model: str = "gpt-4o") -> RAGResult:
    """
    Query the RAG system.
    
    Args:
        question: User's question
        store: Populated VectorStore
        k: Number of context chunks to retrieve
        model: LLM model for generation
    
    Returns:
        RAGResult with answer, sources, and metadata
    """
    # Retrieve relevant chunks
    results = store.search(question, k=k)
    
    if not results:
        return RAGResult(
            answer="No relevant documents found in the knowledge base.",
            sources=[],
            confidence="low",
            tokens_used=0
        )
    
    # Build context from top chunks
    context_parts = []
    sources = []
    for doc, score in results:
        context_parts.append(f"[Source: {doc.source}]\n{doc.content}")
        sources.append(doc)
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Determine confidence based on top similarity score
    top_score = results[0][1]
    confidence = "high" if top_score > 0.85 else ("medium" if top_score > 0.70 else "low")
    
    # Generate answer
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": RAG_SYSTEM},
            {"role": "user", "content":
             f"Context documents:\n\n{context}\n\n---\n\nQuestion: {question}"}
        ],
        max_tokens=1000,
        temperature=0.1  # Low temp for factual accuracy
    )
    
    return RAGResult(
        answer=response.choices[0].message.content,
        sources=sources,
        confidence=confidence,
        tokens_used=response.usage.total_tokens
    )

# ─── Usage Example ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Build knowledge base
    store = VectorStore()
    
    # Add your documents
    store.add_text(
        """Python is a high-level, interpreted programming language known for its 
        clear syntax and readability. Created by Guido van Rossum in 1991, Python 
        supports multiple programming paradigms including procedural, object-oriented, 
        and functional programming.""",
        source="python_overview.txt"
    )
    
    store.add_text(
        """FastAPI is a modern, high-performance web framework for building APIs with 
        Python based on standard Python type hints. It's one of the fastest Python 
        frameworks available and automatically generates OpenAPI documentation.""",
        source="fastapi_docs.txt"
    )
    
    # Query
    result = rag_query("What is FastAPI used for?", store)
    print(f"Answer: {result.answer}")
    print(f"Confidence: {result.confidence}")
    print(f"Sources: {[s.source for s in result.sources]}")
    print(f"Tokens used: {result.tokens_used}")
