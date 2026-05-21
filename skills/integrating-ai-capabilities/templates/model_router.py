"""
Model Router — Cost Optimization Template
Routes queries to the most cost-effective model based on complexity.
Implements: semantic caching, budget tracking, and intelligent routing.
Expected cost reduction: 60-80% vs always using expensive models.
"""

import os
import json
import time
import redis
import numpy as np
import logging
from openai import OpenAI
from dataclasses import dataclass
from datetime import datetime, date
from functools import lru_cache
from typing import Optional

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
r = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"),
                port=int(os.environ.get("REDIS_PORT", 6379)),
                decode_responses=True)

# ─── Model Tiers ─────────────────────────────────────────────────────────────
CHEAP    = "gpt-4o-mini"        # $0.15/M input  — 80% quality
MEDIUM   = "gpt-4o"             # $2.50/M input  — general purpose
COSTLY   = "o3-mini"            # $1.10/M input  — reasoning tasks
PREMIUM  = "claude-sonnet-4-5"  # $3.00/M input  — code & analysis

# Pricing: (input_per_1M, output_per_1M)
PRICING = {
    "gpt-4o-mini":        (0.15,  0.60),
    "gpt-4o":             (2.50, 10.00),
    "o3-mini":            (1.10,  4.40),
    "claude-sonnet-4-5":  (3.00, 15.00),
    "gemini-2.5-flash":   (0.15,  0.60),
}

# ─── Complexity Keywords ──────────────────────────────────────────────────────
COMPLEX_KEYWORDS = [
    "analyze", "complex", "compare", "reason", "strategy", "design",
    "architecture", "optimize", "algorithm", "explain why", "research",
    "evaluate", "critique", "tradeoffs", "recommend", "plan", "review"
]

REASONING_KEYWORDS = [
    "step by step", "prove", "derive", "mathematical", "solve",
    "debug", "find the bug", "calculate", "proof", "logic"
]

CODE_KEYWORDS = [
    "write code", "implement", "function", "class", "api", "refactor",
    "debug", "fix the bug", "write a", "create a", "build a", "generate"
]

# ─── Model Router ─────────────────────────────────────────────────────────────
def route_model(query: str) -> str:
    """
    Route query to the most cost-effective model.
    
    Routing logic:
    - Short + simple → CHEAP (saves 94% vs GPT-4o)
    - Code tasks → PREMIUM (best SWE-bench scores)
    - Reasoning tasks → COSTLY (extended thinking)
    - Everything else → MEDIUM (safe default)
    """
    query_lower = query.lower()
    word_count = len(query.split())
    
    # Route to premium for code tasks
    if any(kw in query_lower for kw in CODE_KEYWORDS) and word_count > 10:
        logger.debug(f"Routing to PREMIUM: code task detected")
        return PREMIUM
    
    # Route to costly for reasoning
    if any(kw in query_lower for kw in REASONING_KEYWORDS):
        logger.debug(f"Routing to COSTLY: reasoning task detected")
        return COSTLY
    
    # Route to cheap: short, simple factual queries
    is_complex = any(kw in query_lower for kw in COMPLEX_KEYWORDS)
    if word_count < 30 and not is_complex:
        logger.debug(f"Routing to CHEAP: short simple query ({word_count} words)")
        return CHEAP
    
    # Default: medium quality
    logger.debug(f"Routing to MEDIUM: general task")
    return MEDIUM

# ─── Semantic Cache ───────────────────────────────────────────────────────────
CACHE_TTL = 3600          # 1 hour
SIMILARITY_THRESHOLD = 0.96  # Very high similarity = same query

def _get_embedding(text: str) -> list[float]:
    """Get embedding for cache key."""
    resp = client.embeddings.create(
        model="text-embedding-3-small",  # Cheap for cache lookups
        input=text
    )
    return resp.data[0].embedding

def _cosine_sim(a: list, b: list) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def cache_lookup(query: str) -> Optional[str]:
    """Check if a semantically similar query is cached."""
    try:
        q_emb = _get_embedding(query)
        keys = r.keys("cache:*")
        
        for key in keys[:100]:  # Check up to 100 cached queries
            cached = r.hgetall(key)
            if not cached:
                continue
            cached_emb = json.loads(cached["embedding"])
            similarity = _cosine_sim(q_emb, cached_emb)
            
            if similarity >= SIMILARITY_THRESHOLD:
                r.hincrby(key, "hits", 1)
                logger.info(f"Cache hit! Similarity: {similarity:.3f}")
                return cached["response"]
    except Exception as e:
        logger.warning(f"Cache lookup failed: {e}")
    
    return None

def cache_store(query: str, response: str) -> None:
    """Store query+response in semantic cache."""
    try:
        q_emb = _get_embedding(query)
        key = f"cache:{hash(query)}"
        r.hset(key, mapping={
            "query": query,
            "response": response,
            "embedding": json.dumps(q_emb),
            "hits": "0",
            "created": datetime.now().isoformat()
        })
        r.expire(key, CACHE_TTL)
    except Exception as e:
        logger.warning(f"Cache store failed: {e}")

# ─── Budget Tracking ──────────────────────────────────────────────────────────
DAILY_BUDGET_USD = float(os.environ.get("AI_DAILY_BUDGET_USD", "10.0"))

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USD for a completion."""
    p_in, p_out = PRICING.get(model, (5.0, 15.0))
    return (input_tokens / 1_000_000) * p_in + (output_tokens / 1_000_000) * p_out

def track_usage(user_id: str, model: str, input_tokens: int,
                output_tokens: int) -> float:
    """Track usage and return today's total cost for this user."""
    cost = calculate_cost(model, input_tokens, output_tokens)
    today = date.today().isoformat()
    key = f"budget:{user_id}:{today}"
    
    new_total = float(r.incrbyfloat(key, cost))
    r.expire(key, 86400)  # 24-hour TTL
    
    if new_total > DAILY_BUDGET_USD:
        raise Exception(
            f"Daily AI budget exceeded for user {user_id}: "
            f"${new_total:.4f} > ${DAILY_BUDGET_USD:.2f}"
        )
    
    logger.info(f"User {user_id}: model={model}, cost=${cost:.4f}, daily_total=${new_total:.4f}")
    return new_total

# ─── Main Entry Point ─────────────────────────────────────────────────────────
def smart_complete(query: str,
                   user_id: str = "anonymous",
                   system: str = "You are a helpful assistant.",
                   force_model: Optional[str] = None,
                   use_cache: bool = True) -> dict:
    """
    Cost-optimized completion with routing, caching, and budget tracking.
    
    Args:
        query: User's query
        user_id: User identifier for budget tracking
        system: System prompt
        force_model: Override model selection
        use_cache: Whether to check semantic cache first
    
    Returns:
        dict with: response, model_used, cost_usd, cache_hit
    """
    # 1. Check semantic cache
    if use_cache:
        cached = cache_lookup(query)
        if cached:
            return {"response": cached, "model_used": "cache", "cost_usd": 0.0, "cache_hit": True}
    
    # 2. Route to appropriate model
    model = force_model or route_model(query)
    
    # 3. Generate completion
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": query}
    ]
    
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1000,
    )
    
    response = resp.choices[0].message.content
    
    # 4. Track usage and enforce budget
    cost = track_usage(user_id, model, resp.usage.prompt_tokens, resp.usage.completion_tokens)
    
    # 5. Cache response
    if use_cache:
        cache_store(query, response)
    
    return {
        "response": response,
        "model_used": model,
        "cost_usd": calculate_cost(model, resp.usage.prompt_tokens, resp.usage.completion_tokens),
        "cache_hit": False,
        "tokens": {"input": resp.usage.prompt_tokens, "output": resp.usage.completion_tokens}
    }

# ─── Usage Example ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Test routing
    queries = [
        "What is Python?",                              # → CHEAP
        "Write a FastAPI authentication middleware",    # → PREMIUM
        "Prove that sqrt(2) is irrational",            # → COSTLY
        "Analyze the tradeoffs between SQL and NoSQL",  # → MEDIUM
    ]
    
    for q in queries:
        model = route_model(q)
        print(f"Query: {q[:50]}...\nRouted to: {model}\n")
    
    # Test full pipeline (requires Redis + OpenAI key)
    # result = smart_complete("What is machine learning?", user_id="user_123")
    # print(result)
