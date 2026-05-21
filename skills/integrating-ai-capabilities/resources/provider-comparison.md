# Provider Comparison — Complete Guide

## Model Comparison Matrix (2025/2026)

| Model | Context | Best For | Input Cost/1M | Output Cost/1M | Strengths |
|-------|---------|----------|--------------|----------------|-----------|
| GPT-4o | 128K | General, vision, audio | $2.50 | $10.00 | Fastest frontier, multi-modal, function calling |
| GPT-4o mini | 128K | High-volume, simple | $0.15 | $0.60 | 80% quality at 6% cost of GPT-4o |
| o1 / o3 | 200K | Complex reasoning, math | $15.00 / $2.00 | $60.00 | Extended thinking, STEM |
| Claude Sonnet 4 | 200K | Code, analysis, long docs | $3.00 | $15.00 | #1 SWE-bench, instruction following |
| Claude Haiku 4 | 200K | Fast, cheap tasks | $0.80 | $4.00 | Ultra-low latency, high throughput |
| Claude Opus 4 | 200K | Complex, nuanced tasks | $15.00 | $75.00 | Deepest reasoning, best writing |
| Gemini 2.5 Pro | 1M | Long context, grounding | $3.50 | $10.50 | 1M token window, Google Search |
| Gemini 2.5 Flash | 1M | Cost-efficient, fast | $0.15 | $0.60 | Best price/performance 2025 |
| Mistral Large | 128K | EU compliance | $2.00 | $6.00 | European data residency |
| Ollama (local) | Varies | Privacy, no cost | $0 | $0 | Zero API cost, air-gapped |

---

## Model Selection Decision Tree

```
What is your primary need?
│
├─ Simple: classify / summarize / extract short text
│   └─> GPT-4o mini ($0.15/M) or Gemini 2.5 Flash ($0.15/M)
│
├─ Code generation & review
│   └─> Claude Sonnet 4 (top SWE-bench scores consistently)
│
├─ Complex multi-step reasoning / math / logic
│   └─> o1/o3 or Claude Opus 4 (extended thinking)
│
├─ Long document processing (>50K tokens)
│   └─> Gemini 2.5 Pro (1M token context window)
│
├─ Real-time web data needed
│   └─> Gemini 2.5 Pro/Flash with Search grounding
│
├─ EU data residency required
│   └─> Mistral Large (EU servers) or Azure OpenAI (EU regions)
│
├─ Privacy / no data leaving your infrastructure
│   └─> Ollama with Llama 3.3 70B or Qwen 2.5 Coder
│
├─ Vision / image understanding
│   └─> GPT-4o or Gemini 2.5 Pro (both handle complex images)
│
├─ Voice / audio input
│   └─> OpenAI Whisper + GPT-4o audio preview
│
└─ Structured JSON output (most reliable)
    └─> Any provider with json_schema mode — Claude most reliable
```

---

## Provider SDK Comparison

| Feature | OpenAI | Anthropic | Google Gemini | LiteLLM |
|---------|--------|-----------|---------------|---------|
| Python SDK | `openai` | `anthropic` | `google-genai` | `litellm` |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| Function Calling | ✅ | ✅ Tool Use | ✅ | ✅ |
| Vision | ✅ | ✅ | ✅ | ✅ |
| JSON Mode | ✅ json_schema | ✅ tool use | ✅ | ✅ |
| Prompt Caching | ✅ (auto) | ✅ (manual, 90% off) | ✅ | ✅ |
| Batch API | ✅ 50% off | ✅ | ✅ | ✅ |
| Embeddings | ✅ | ❌ | ✅ | ✅ |
| Local Models | ❌ | ❌ | ❌ | ✅ (Ollama) |
| Fallback Routing | ❌ | ❌ | ❌ | ✅ |

---

## Agent Framework Comparison (2025)

| Framework | Language | Best For | Key Strength | Maturity |
|-----------|----------|---------|--------------|----------|
| LangChain | Python/JS | RAG, chains, agents | Largest ecosystem, 600+ integrations | Production |
| LlamaIndex | Python | RAG, document Q&A | Best-in-class RAG, data connectors | Production |
| LangGraph | Python | Stateful agent workflows | Graph-based control flow, checkpointing | Production |
| CrewAI | Python | Multi-agent teams | Role-based agents, simple crew syntax | Growing |
| AutoGen | Python | Multi-agent conversation | Microsoft-backed, research-grade | Growing |
| Pydantic AI | Python | Type-safe agents | Structured outputs, validation | New 2025 |
| Vercel AI SDK | TypeScript | Next.js/React AI apps | Frontend streaming, RSC support | Production |
| Mastra | TypeScript | Full-stack TS agents | TypeScript-native, built-in tools | New 2025 |

---

## Vector Database Comparison

| Database | Type | Best For | Scale | Key Feature | Setup |
|----------|------|---------|-------|-------------|-------|
| Pinecone | Managed cloud | Production RAG, serverless | Billions | Zero-ops, auto-scaling, metadata filtering | `pip install pinecone` |
| Weaviate | OSS + cloud | Multi-modal, hybrid search | 100M+ | BM25 + vector hybrid out of the box | Docker or cloud |
| Qdrant | OSS + cloud | High performance, Rust | 100M+ | Payload filtering, quantization | `pip install qdrant-client` |
| pgvector | PostgreSQL ext | Existing Postgres users | 10M | No new infra, SQL joins | `CREATE EXTENSION vector` |
| Chroma | OSS embedded | Prototyping, local dev | <1M | Zero setup, Python-native | `pip install chromadb` |
| Milvus | OSS + cloud | Enterprise, high throughput | Billions | GPU acceleration, distributed | Docker |
| Redis VSS | Redis module | Low-latency + search | 100M | Sub-millisecond, existing Redis | Redis Stack |

---

## Embedding Model Comparison

| Model | Provider | Dimensions | Best For | Cost/1M tokens |
|-------|----------|-----------|---------|----------------|
| text-embedding-3-large | OpenAI | 3072 | Production RAG, highest quality | $0.13 |
| text-embedding-3-small | OpenAI | 1536 | Good quality, lower cost | $0.02 |
| embed-english-v3.0 | Cohere | 1024 | English-only retrieval | $0.10 |
| embed-multilingual-v3.0 | Cohere | 1024 | Multilingual content | $0.10 |
| text-embedding-004 | Google | 768 | Gemini-native RAG pipelines | $0.00 |
| nomic-embed-text | Ollama/local | 768 | Air-gapped, fully local | $0 |
| all-MiniLM-L6-v2 | HuggingFace | 384 | Lightweight, CPU-friendly | $0 |

---

## Chunking Strategy Guide

| Strategy | Chunk Size | Overlap | Best For | Library |
|----------|-----------|---------|---------|---------|
| Fixed Size | 200-400 tokens | 10-20% | General purpose, simple docs | LangChain TextSplitter |
| Recursive Character | 400-600 tokens | 50-100 tokens | Long documents, articles | LangChain RecursiveCharacterTextSplitter |
| Semantic (sentence) | Full sentences | ±1 sentence | Q&A over structured content | LlamaIndex SentenceSplitter |
| Semantic (embedding) | Dynamic by meaning shift | N/A | Research papers, tech docs | LangChain SemanticChunker |
| Markdown/HTML aware | By heading level | Inherit parent | Documentation, wikis | LangChain MarkdownHeaderSplitter |
| Parent-Child | Small child (100t), large parent (400t) | N/A | High precision with context | LlamaIndex ParentDocumentRetriever |
