# Cost Optimization Guide — Slash Your AI Bill by 60-90%

## Overview

AI API costs can spiral fast. A well-optimized system typically achieves **60-90% cost reduction** 
vs a naive implementation without impacting quality.

**Apply these strategies in order of impact.** Each layer compounds the savings.

---

## Strategy 1: Model Routing (Highest Impact — saves 60-70%)

**Concept:** Not all queries need your most expensive model. Route simple queries to cheap models,
complex ones to expensive models.

**A 70/30 routing split (cheap/expensive) typically cuts costs 60-70% with <5% quality drop.**

| Query Type | Route To | Cost/1M Input | Quality |
|-----------|---------|--------------|---------|
| Simple: classify/summarize/extract | GPT-4o mini / Gemini Flash | $0.15 | 80% of expensive |
| General: chat/Q&A/explain | GPT-4o | $2.50 | Full quality |
| Code generation | Claude Sonnet 4 | $3.00 | Best code quality |
| Complex reasoning | o3-mini | $1.10 | Extended thinking |

```python
# See templates/model_router.py for full implementation
def route_model(query: str) -> str:
    """Route to most cost-effective model."""
    token_estimate = len(query.split()) * 1.3
    CHEAP  = "gpt-4o-mini"  # $0.15/M
    MEDIUM = "gpt-4o"       # $2.50/M
    COSTLY = "o3-mini"      # $1.10/M

    # Short + simple = cheap
    if token_estimate < 200 and not any(w in query.lower() for w in
        ["analyze", "complex", "compare", "reason", "strategy"]):
        return CHEAP

    # Reasoning = costly (but still much cheaper than GPT-4o for this)
    if any(w in query.lower() for w in ["step by step", "prove", "derive"]):
        return COSTLY

    return MEDIUM
```

---

## Strategy 2: Prompt Caching (saves 50-90% on cached tokens)

Prompt caching stores large system prompts or documents server-side.
**Cached tokens cost 10% of normal price** and serve at 0 latency.

### Anthropic (manual caching — most powerful)
```python
# Mark blocks for caching — minimum 1,024 tokens per block
response = client.messages.create(
    model="claude-sonnet-4-5",
    system=[{
        "type": "text",
        "text": VERY_LONG_SYSTEM_PROMPT,       # 2,000+ tokens
        "cache_control": {"type": "ephemeral"} # 90% off on cache hits
    }],
    messages=[{"role": "user", "content": user_question}]
)
# First call: builds cache (cache_creation_input_tokens)
# Subsequent calls: 10% price (cache_read_input_tokens)
```

### OpenAI (automatic caching)
```python
# OpenAI automatically caches prompts > 1,024 tokens
# No code changes needed — happens transparently
# Cached prefix discount: 50% off cached tokens
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},  # Cached automatically
        {"role": "user", "content": user_question}
    ]
)
```

**Best practices for caching:**
- Put stable content (system prompt, documents) FIRST in the prompt
- Put dynamic content (user question) LAST
- Ensure cacheable blocks are >= 1,024 tokens (Anthropic) or 1,024 tokens (OpenAI)
- Cache: system prompts, knowledge base docs, few-shot examples, codebases

---

## Strategy 3: Response Caching (saves 20-40%)

Cache complete responses for repeated or semantically similar queries.

### Exact Match Cache (Redis)
```python
import redis, json, hashlib

r = redis.Redis()

def cached_response(query: str, generate_fn, ttl: int = 3600) -> str:
    """Cache by exact query hash."""
    cache_key = f"resp:{hashlib.md5(query.encode()).hexdigest()}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)    # Cache hit!
    
    response = generate_fn(query)   # Cache miss — generate
    r.setex(cache_key, ttl, json.dumps(response))
    return response
```

### Semantic Cache (similarity-based)
```python
# Cache by embedding similarity — catches paraphrased queries
SIMILARITY_THRESHOLD = 0.96  # Adjust: higher = more precise matching

def semantic_cache_lookup(query: str, threshold: float = 0.96) -> str | None:
    """Find cached response for semantically similar query."""
    q_emb = embed(query)
    for key in r.scan_iter("scache:*"):
        data = json.loads(r.get(key))
        if cosine_similarity(q_emb, data["embedding"]) >= threshold:
            return data["response"]  # Cache hit!
    return None
```

**What to cache:**
- ✅ FAQ responses, documentation Q&A, product descriptions
- ✅ Classification results for similar inputs
- ❌ NEVER cache PII-containing responses
- ❌ NEVER cache personalized or time-sensitive answers

---

## Strategy 4: Token Optimization (saves 10-30%)

### Prompt Optimization
```python
# BEFORE: Verbose (120 tokens)
bad_system = """You are a helpful assistant that helps users with their questions.
When a user asks you something, please make sure to provide a thorough and comprehensive
response that addresses all aspects of their question in a detailed manner."""

# AFTER: Tight (25 tokens) — same quality
good_system = """You are a helpful assistant. Be concise and accurate."""

# Use structured formats for extraction (saves 40-60% over prose)
# BEFORE: "Please extract the name, age, and city from the following text and present..."
# AFTER: "Extract JSON: name, age, city from: [text]"
```

### Token Counting Before Sending
```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(prompt: str, model: str = "gpt-4o") -> float:
    tokens = count_tokens(prompt, model)
    price_per_million = {"gpt-4o": 2.50, "gpt-4o-mini": 0.15}.get(model, 2.50)
    return (tokens / 1_000_000) * price_per_million

# Always set explicit max_tokens
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=500,  # NEVER leave at default (4096) — pay for what you need
)
```

---

## Strategy 5: Batch Processing (50% off non-real-time)

```python
# OpenAI Batch API — 50% off, 24h turnaround
# Use for: bulk classification, data extraction, async summarization

import json
from openai import OpenAI

client = OpenAI()

# 1. Prepare batch requests
requests = [
    {
        "custom_id": f"task_{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": f"Classify: {text}"}],
            "max_tokens": 10,
        }
    }
    for i, text in enumerate(texts_to_classify)
]

# 2. Upload and submit batch
with open("batch_requests.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")

batch_file = client.files.create(
    file=open("batch_requests.jsonl", "rb"),
    purpose="batch"
)
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"  # 50% discount
)

# 3. Poll for completion (async)
import time
while batch.status not in ["completed", "failed"]:
    batch = client.batches.retrieve(batch.id)
    print(f"Status: {batch.status}")
    time.sleep(60)

# 4. Download results
output_file = client.files.content(batch.output_file_id)
results = [json.loads(line) for line in output_file.text.splitlines() if line]
```

---

## Strategy 6: Local Models for High-Volume / Private Work

```python
# Ollama — zero per-request cost, fully local
# Llama 3.3 70B rivals GPT-4o on many tasks at $0 API cost
# 
# Installation: https://ollama.ai
# Pull: ollama pull llama3.3
# 
# Use for: internal tools, PII data, bulk processing, dev/staging

import ollama

# Direct Python API
response = ollama.chat(
    model='llama3.3',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}]
)
print(response['message']['content'])

# Or use LiteLLM for seamless switching
from litellm import completion
resp = completion(model="ollama/llama3.3", messages=msgs)  # Same interface!
```

---

## Cost Monitoring & Budget Alerts

```python
import dataclasses
from datetime import datetime, date

PRICING = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "claude-sonnet-4-5": (3.00, 15.00),
    "gemini-2.5-flash": (0.15, 0.60),
}

ALERT_THRESHOLDS = [0.5, 0.8, 1.0]  # Alert at 50%, 80%, 100% of budget
MONTHLY_BUDGET = float(os.environ.get("AI_MONTHLY_BUDGET", "100.0"))

def log_and_alert(model: str, usage, user_id: str) -> None:
    """Log usage and send alerts if approaching budget."""
    p_in, p_out = PRICING.get(model, (5.0, 15.0))
    cost = (usage.input_tokens / 1e6) * p_in + (usage.output_tokens / 1e6) * p_out
    
    # Store to your DB
    db.save({
        "model": model, "cost_usd": cost, "user_id": user_id,
        "input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens,
        "timestamp": datetime.now().isoformat()
    })
    
    # Check monthly total
    monthly_total = db.get_monthly_cost(user_id)
    usage_ratio = monthly_total / MONTHLY_BUDGET
    
    for threshold in ALERT_THRESHOLDS:
        if usage_ratio >= threshold:
            send_alert(f"AI budget alert: {threshold*100}% used (${monthly_total:.2f} / ${MONTHLY_BUDGET:.2f})")
```

---

## Expected Savings by Tier

| Optimization Applied | Expected Monthly Savings |
|---------------------|------------------------|
| Model routing only | 60-70% |
| + Prompt caching | 75-80% |
| + Response caching | 80-85% |
| + Token optimization | 83-88% |
| + Batch API | 87-92% |
| + Local models for volume | 90%+ |

**Example:** $1,000/month AI bill → $100-$200 with all optimizations applied.
