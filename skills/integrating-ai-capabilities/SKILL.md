---
name: integrating-ai-capabilities
description: >
  Integrates LLM APIs and production-grade AI capabilities into any project in any
  language or framework. Use when asked to: add AI to a project, integrate OpenAI or
  GPT-4o, use the Claude API, add Gemini, build a chatbot, implement RAG or document
  Q&A, add vector search, reduce AI API costs, build AI agents, add streaming responses,
  implement function calling or tool use, add prompt caching, build semantic search,
  implement multi-agent systems, add AI to an existing API, build LLM pipelines,
  switch between AI providers, add memory to an AI, implement embeddings, connect to a
  vector database, optimize LLM token usage, integrate LangChain or LlamaIndex,
  build autonomous agents, add real-time AI, implement ReAct pattern, or analyze a
  project to determine the best AI integration strategy. Returns: production-ready code
  with streaming, error handling, retry logic, cost tracking, PII protection, and tests.
---

# AntiGravity AI Integration Skill

> **Version:** 2.0.0 | **Edition:** 2025/2026 | **Providers:** OpenAI · Anthropic · Gemini · Mistral · Ollama
> **Patterns:** 20+ Integration Patterns | **Languages:** Python · JavaScript/TypeScript · Go · Java

---

## When to Use This Skill

- User wants to **add any LLM API** (OpenAI, Anthropic, Gemini, Cohere, Mistral, local)
- User needs a **chatbot**, conversational AI, or Q&A system
- User wants **RAG** — document question answering over their own data
- User asks about **vector databases** (Pinecone, pgvector, Chroma, Qdrant, Weaviate)
- User wants **AI agents**, autonomous workflows, or tool-calling systems
- User needs **streaming AI responses** in their frontend
- User wants to **reduce LLM API costs** or optimize token usage
- User needs **structured JSON output** from an LLM
- User asks about **prompt engineering**, system prompts, or few-shot examples
- User wants to **add memory, context, or personalization** to an AI feature
- Any mention of: embeddings, semantic search, LangChain, LlamaIndex, agents, RAG
- User says "**analyze my project**" to determine what AI should be integrated

---

## Phase 0 — Project Analysis (MANDATORY FIRST STEP)

Before writing any code, analyze the existing project to determine the optimal AI integration strategy.

- [ ] **Scan Project Structure**: Read directory tree, identify languages, frameworks, existing APIs
- [ ] **Identify Integration Points**: Where should AI be added? (endpoint, service, UI, CLI)
- [ ] **Assess Data Sources**: What data will the AI reason over? (DB, files, APIs, user input)
- [ ] **Determine Connection Method**: REST endpoint, SDK import, message queue, WebSocket
- [ ] **Check Existing Infrastructure**: Does the project already use Redis, Postgres, a job queue?
- [ ] **Select AI Pattern**: Use the Decision Framework below to pick the right pattern
- [ ] **Choose Provider & Model**: Use the Model Selection Guide below
- [ ] **Generate Integration Plan**: Output a structured plan before touching any code

### Project Analysis Checklist

```
PROJECT SNAPSHOT (fill before coding)
─────────────────────────────────────────────
Language/Runtime   : _______________
Framework          : _______________
Database           : _______________
Auth System        : _______________
Frontend           : _______________
Existing APIs      : _______________
Data Sources       : _______________
Deployment Target  : _______________
─────────────────────────────────────────────
AI INTEGRATION DECISION
Pattern Selected   : _______________
Provider Selected  : _______________
Model Selected     : _______________
Streaming Needed   : YES / NO
Vector DB Needed   : YES / NO / EXISTING
Agent Needed       : YES / NO
Cost Budget/Month  : _______________
─────────────────────────────────────────────
```

---

## AI Integration Decision Framework

| User Need | Recommended Stack | Key Template |
|-----------|------------------|--------------|
| Simple chatbot | OpenAI GPT-4o + streaming + memory | `templates/streaming_fastapi.py` |
| Document Q&A / RAG | OpenAI embeddings + pgvector + GPT-4o | `templates/rag_pipeline.py` |
| Autonomous task agent | Claude Sonnet 4 + tool calling + ReAct | `templates/react_agent.py` |
| High-volume classification | GPT-4o mini + batch API + caching | `templates/model_router.py` |
| Private / air-gapped | Ollama + LlamaIndex + Chroma | `templates/local_stack.py` |
| Real-time + web data | Gemini 2.5 Flash + Search grounding | `templates/gemini_grounding.py` |
| Multi-modal (vision+text) | GPT-4o or Gemini 2.5 Pro | `templates/vision_input.py` |
| Cost-optimized production | LiteLLM Router + model cascade + cache | `templates/litellm_router.py` |
| EU data residency | Mistral Large or Azure OpenAI EU | `templates/openai_basic.py` |
| Structured JSON extraction | Any provider with json_schema mode | `templates/structured_output.py` |

---

## Model Selection Guide

| Task | Best Model | Cost/1M Input | Why |
|------|-----------|--------------|-----|
| General chatbot | GPT-4o or Claude Sonnet 4 | $2.50 / $3.00 | Best quality/cost balance |
| High-volume simple tasks | GPT-4o mini | $0.15 | 80% quality at 6% cost |
| Code generation & review | Claude Sonnet 4 | $3.00 | Top SWE-bench scores |
| Complex reasoning / math | o1/o3 or Claude Opus 4 | $15 | Extended thinking |
| Long documents (>50K tok) | Gemini 2.5 Pro (1M ctx) | $3.50 | Best long-context handling |
| Real-time web data | Gemini 2.5 + Search grounding | $3.50 | Live Google Search access |
| Privacy / local | Ollama + Llama 3.3 70B | $0 (compute) | Zero API cost, air-gapped |
| Structured JSON | Any with json_schema mode | varies | Claude most reliable |
| EU data residency | Mistral Large | $2.00 | European servers |
| Fast + cheap | Gemini 2.5 Flash | $0.15 | Best price/performance 2025 |

---

## Integration Workflow

### Step 1 — Install & Configure Provider

```bash
# OpenAI
pip install openai
# Set: OPENAI_API_KEY=sk-...

# Anthropic Claude
pip install anthropic
# Set: ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
pip install google-genai
# Set: GEMINI_API_KEY=AIza...

# LiteLLM (universal proxy — same interface for ALL providers)
pip install litellm

# Agent Frameworks
pip install langchain langchain-openai llama-index langgraph crewai pydantic-ai

# Vector DBs
pip install pinecone          # Pinecone cloud
pip install chromadb          # Local dev
pip install qdrant-client     # Qdrant
# pgvector: CREATE EXTENSION vector; in PostgreSQL

# RAG utilities
pip install tiktoken sentence-transformers presidio-analyzer presidio-anonymizer

# Observability
pip install langsmith          # Tracing & evals

# Local models
# 1. Install Ollama: https://ollama.ai
# 2. ollama pull llama3.3       # General purpose
# 3. ollama pull qwen2.5-coder  # Best local code model
```

### Step 2 — Secure API Keys (CRITICAL)

- **NEVER** hardcode keys in source code — they are exposed forever on commit
- **NEVER** put keys in client-side JS/frontend — they WILL be extracted
- **NEVER** share keys across environments — use separate keys per env
- **NEVER** use keys without spending limits — set hard budget caps
- **DO**: Store in `.env` files (gitignored), OS secrets manager, or Vault/AWS SSM
- **DO**: Rotate keys quarterly and immediately on any suspected exposure
- **DO**: Use a proxy layer (LiteLLM, PortKey) so keys never leave your backend

```bash
# .env file (add to .gitignore FIRST)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
```

### Step 3 — Choose Integration Pattern

See `resources/integration-patterns.md` for all 20+ patterns with full code. Quick reference:

1. **Basic Chat Completion** → `templates/openai_basic.py`
2. **Streaming (user-facing apps)** → `templates/streaming_fastapi.py`
3. **Structured JSON Output** → `templates/structured_output.py`
4. **Function Calling / Tool Use** → `templates/tool_calling_loop.py`
5. **RAG Pipeline** → `templates/rag_pipeline.py`
6. **ReAct Agent** → `templates/react_agent.py`
7. **Multi-Agent System** → `templates/multi_agent.py`
8. **Local/Private AI** → `templates/local_stack.py`
9. **Universal Proxy** → `templates/litellm_router.py`
10. **Cost-Optimized Router** → `templates/model_router.py`

### Step 4 — Apply Production Hardening

- [ ] API keys in environment variables — NEVER hardcoded
- [ ] Retry logic with exponential backoff on rate limits
- [ ] Streaming implemented for ALL user-facing responses
- [ ] Token usage logged per request per user
- [ ] Budget alerts configured in provider dashboard
- [ ] PII scrubbed before sending to external APIs (Presidio)
- [ ] Model routing: cheap model for simple tasks, expensive for complex
- [ ] Response caching for repeated queries (Redis)
- [ ] Prompt caching for large repeated system prompts (Anthropic)
- [ ] Error messages don't expose API keys, model names, or system prompts
- [ ] Rate limiting per user (prevent abuse)
- [ ] Observability enabled (LangSmith, Arize, or Helicone)
- [ ] Fallback model configured (primary provider outage scenario)
- [ ] Max token limits set on ALL completions

---

## Cost Optimization (60–90% savings achievable)

Apply in this order — each step compounds the savings:

1. **Model Routing** — route 70% to cheap model → saves 60–70%
2. **Prompt Caching** — cache large system prompts (Anthropic 90% off) → saves 50–90%
3. **Response Caching** — Redis cache for repeated queries → saves 20–40%
4. **Token Optimization** — tighter prompts, capped max_tokens → saves 10–30%
5. **Batch API** — 50% off for non-real-time jobs (OpenAI Batch API)
6. **Local Models** — Ollama for high-volume or privacy-sensitive work → $0/request

Full implementation: `templates/model_router.py` and `resources/cost-optimization.md`

---

## Security Rules

* Always sanitize user input with `safe_prompt()` before sending to LLM
* Defend against prompt injection (see `resources/security.md`)
* Use Presidio to scrub PII before any external API call
* Never return raw LLM errors to end users
* Implement per-user rate limiting on all AI endpoints
* Never log raw request/response bodies that contain API keys

---

## Resources

- [Integration Patterns Reference](resources/integration-patterns.md) — All 20+ patterns
- [Provider Comparison](resources/provider-comparison.md) — Full provider analysis
- [Cost Optimization Guide](resources/cost-optimization.md) — Step-by-step savings
- [Security & PII Guide](resources/security.md) — Prompt injection, PII, GDPR
- [Agent Architecture Guide](resources/agent-architectures.md) — ReAct, LATS, MoA
- [Vector DB Guide](resources/vector-db-guide.md) — Pinecone, pgvector, Qdrant, Chroma
- [Prompt Engineering](resources/prompt-engineering.md) — System prompts, CoT, few-shot
- [Model Pricing Data](resources/model-pricing.json) — Current pricing all providers
- [Templates Directory](templates/) — Ready-to-use production code
- [Examples Directory](examples/) — Full working applications

---

## Quick Implementation Reference

### Pattern 1: Basic Chat
```python
from openai import OpenAI
client = OpenAI()  # reads OPENAI_API_KEY
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"system","content":"You are a helpful assistant."},
              {"role":"user","content":user_message}],
    temperature=0.7, max_tokens=1000)
return response.choices[0].message.content
```

### Pattern 2: Streaming (Always for user-facing)
```python
stream = client.chat.completions.create(model="gpt-4o",
    messages=messages, stream=True)
for chunk in stream:
    if chunk.choices[0].delta.content:
        yield chunk.choices[0].delta.content
```

### Pattern 3: Minimal RAG
```python
context = vector_db.search(embed(question), top_k=5)
response = client.chat.completions.create(model="gpt-4o", messages=[
    {"role":"system","content":"Answer ONLY from the provided context."},
    {"role":"user","content":f"Context:\n{context}\n\nQuestion: {question}"}])
```

### Pattern 4: Tool Calling Loop
```python
while True:
    resp = client.chat.completions.create(model="gpt-4o",
        messages=messages, tools=tools)
    msg = resp.choices[0].message
    messages.append(msg)
    if not msg.tool_calls: return msg.content
    for call in msg.tool_calls:
        result = dispatch(call.function.name, json.loads(call.function.arguments))
        messages.append({"role":"tool","tool_call_id":call.id,"content":str(result)})
```
