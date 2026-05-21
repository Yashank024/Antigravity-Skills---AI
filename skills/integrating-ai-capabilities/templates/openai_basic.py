"""
OpenAI Basic Setup — Production Template
Copy this file into your project as a starting point.
Replace the model, system prompt, and add your own logic.
"""

import os
import time
import random
import logging
from openai import OpenAI, RateLimitError, APIError
from typing import Generator

logger = logging.getLogger(__name__)

# ─── Client Setup ──────────────────────────────────────────────────────────────
def get_client() -> OpenAI:
    """Get OpenAI client. Raises if API key not set."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)

client = get_client()

# ─── Retry Logic ──────────────────────────────────────────────────────────────
def with_retry(func, max_retries: int = 5, base_delay: float = 1.0):
    """Exponential backoff with jitter for all LLM providers."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Rate limited. Retry {attempt+1}/{max_retries} in {delay:.1f}s")
            time.sleep(delay)
        except APIError as e:
            if e.status_code in [500, 502, 503, 529]:  # Server errors
                if attempt == max_retries - 1:
                    raise
                time.sleep(base_delay * (2 ** attempt))
            else:
                raise  # 4xx client errors — don't retry

# ─── Basic Chat Completion ────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful, accurate, and professional AI assistant.
Always respond clearly and concisely. If you don't know something, say so."""

def chat(user_message: str,
         model: str = "gpt-4o",
         system: str = SYSTEM_PROMPT,
         temperature: float = 0.7,
         max_tokens: int = 1000,
         conversation_history: list[dict] | None = None) -> str:
    """
    Single-turn or multi-turn chat completion.
    
    Args:
        user_message: The user's input message
        model: OpenAI model to use
        system: System prompt
        temperature: 0=deterministic, 2=very creative
        max_tokens: Maximum response length
        conversation_history: Previous messages for multi-turn
    
    Returns:
        Assistant's response text
    """
    messages = [{"role": "system", "content": system}]
    
    if conversation_history:
        messages.extend(conversation_history)
    
    messages.append({"role": "user", "content": user_message})
    
    response = with_retry(lambda: client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    ))
    
    # Log token usage
    usage = response.usage
    logger.info(f"Tokens: input={usage.prompt_tokens}, output={usage.completion_tokens}, "
                f"total={usage.total_tokens}")
    
    return response.choices[0].message.content

# ─── Streaming Chat ───────────────────────────────────────────────────────────
def chat_stream(user_message: str,
                model: str = "gpt-4o",
                system: str = SYSTEM_PROMPT) -> Generator[str, None, None]:
    """
    Streaming chat — yields tokens as they arrive.
    Use for user-facing applications to avoid blank screen waits.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content

# ─── Usage Example ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Basic chat
    print("=== Basic Chat ===")
    response = chat("What is the capital of France?")
    print(response)
    
    # Multi-turn conversation
    print("\n=== Multi-turn ===")
    history = []
    for question in ["My name is Alice.", "What's my name?"]:
        response = chat(question, conversation_history=history)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})
        print(f"Q: {question}\nA: {response}\n")
    
    # Streaming
    print("=== Streaming ===")
    for token in chat_stream("Write a haiku about coding"):
        print(token, end="", flush=True)
    print()
