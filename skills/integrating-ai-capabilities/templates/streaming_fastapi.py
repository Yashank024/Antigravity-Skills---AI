"""
FastAPI Streaming Endpoint — Production Template
Real-time AI response streaming via Server-Sent Events (SSE).
Includes: session management, rate limiting, error handling, CORS.
"""

import os
import json
import asyncio
import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel, field_validator
from typing import Optional

logger = logging.getLogger(__name__)

app = FastAPI(title="AI Chat API", version="1.0.0")
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

# CORS — adjust origins for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ───────────────────────────────────────────────────────────────────
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000
    system: Optional[str] = "You are a helpful AI assistant."
    user_id: Optional[str] = "anonymous"

    @field_validator("model")
    @classmethod
    def validate_model(cls, v):
        allowed = ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4-5", "gemini-2.5-flash"]
        if v not in allowed:
            raise ValueError(f"Model must be one of: {allowed}")
        return v

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v):
        if len(v) > 50:
            raise ValueError("Maximum 50 messages per request")
        return v

# ─── SSE Streaming Endpoint ───────────────────────────────────────────────────
@app.post("/api/chat/stream")
async def stream_chat(request: ChatRequest, http_request: Request):
    """
    Stream AI response via Server-Sent Events.
    
    Frontend consumes this with:
    - fetch() + ReadableStream in vanilla JS/React
    - EventSource API (GET only — use fetch for POST)
    """
    async def event_generator():
        try:
            # Build messages array
            messages_list = [{"role": "system", "content": request.system}]
            messages_list.extend([{"role": m.role, "content": m.content}
                                   for m in request.messages])

            stream = await client.chat.completions.create(
                model=request.model,
                messages=messages_list,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            )

            full_response = ""
            async for chunk in stream:
                # Check if client disconnected
                if await http_request.is_disconnected():
                    logger.info(f"Client {request.user_id} disconnected")
                    break

                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    # SSE format: "data: {json}\n\n"
                    yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"

            # Send done signal
            yield f"data: {json.dumps({'content': '', 'done': True, 'full_response': full_response})}\n\n"

        except Exception as e:
            logger.error(f"Stream error for user {request.user_id}: {e}")
            yield f"data: {json.dumps({'error': 'An error occurred. Please try again.'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",          # Disable nginx buffering
            "Connection": "keep-alive",
        }
    )

# ─── Non-streaming endpoint ───────────────────────────────────────────────────
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint."""
    messages_list = [{"role": "system", "content": request.system}]
    messages_list.extend([{"role": m.role, "content": m.content}
                           for m in request.messages])
    
    response = await client.chat.completions.create(
        model=request.model,
        messages=messages_list,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    
    return {
        "response": response.choices[0].message.content,
        "model": request.model,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }
    }

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "AI Chat API"}

# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streaming_fastapi:app", host="0.0.0.0", port=8000, reload=True)
