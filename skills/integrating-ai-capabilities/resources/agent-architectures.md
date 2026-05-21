# Agent Architectures — Complete Guide

## Overview

AI agents are systems where an LLM decides what actions to take, executes them, observes the results,
and continues until a goal is achieved. Agents go beyond static Q&A — they can browse the web,
write and execute code, query databases, send emails, and orchestrate complex multi-step workflows.

---

## Architecture Comparison

| Architecture | Description | Best For | Complexity |
|-------------|-------------|---------|-----------|
| **ReAct** | Reason + Act loop. Think → Call tool → Observe → Repeat until done | General purpose agents with tools | Low |
| **Plan-and-Execute** | Planner creates full plan upfront. Executor runs each step. | Structured tasks, parallel execution | Medium |
| **Reflexion** | Agent reflects on failures and retries with self-critique. | Tasks requiring precision, complex reasoning | Medium |
| **LATS (Tree Search)** | Explore multiple action paths, backtrack on failure. | Complex multi-step with wrong-path recovery | High |
| **Multi-Agent** | Specialist agents collaborate. Orchestrator delegates. | Complex, large-scale, specialized work | High |
| **Mixture of Agents (MoA)** | Multiple LLMs run in parallel, aggregator synthesizes. | Highest quality output requirements | Very High |

---

## ReAct Agent — Full Production Implementation

```python
from anthropic import Anthropic
import json, re

client = Anthropic()

SYSTEM = """You are an autonomous agent. To solve tasks, use this exact format:

Thought: [Your reasoning about what to do next]
Action: tool_name
Action Input: {"param": "value"}

After receiving an observation, continue thinking and acting.
When you have the final answer, say:
Final Answer: [your complete answer]
"""

def react_agent(goal: str, tools: dict, max_steps: int = 10) -> str:
    """
    ReAct agent that loops until goal is achieved or max_steps reached.
    
    Args:
        goal: The task for the agent to complete
        tools: Dict of {tool_name: callable} - your actual function implementations
        max_steps: Safety limit on number of tool calls
    
    Returns:
        Final answer string
    """
    messages = [{"role": "user", "content": f"Goal: {goal}"}]

    for step in range(max_steps):
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            system=SYSTEM,
            messages=messages
        )
        output = resp.content[0].text
        messages.append({"role": "assistant", "content": output})

        # Check for final answer
        if "Final Answer:" in output:
            return output.split("Final Answer:")[-1].strip()

        # Parse and execute action
        if "Action:" in output and "Action Input:" in output:
            action = re.search(r"Action: (.+)", output).group(1).strip()
            action_input = re.search(r"Action Input: (.+)", output, re.DOTALL).group(1).strip()

            try:
                args = json.loads(action_input)
                if action in tools:
                    observation = tools[action](**args)
                    print(f"[Step {step+1}] Action: {action} → {str(observation)[:100]}")
                else:
                    observation = f"Error: Unknown tool '{action}'. Available: {list(tools.keys())}"
            except json.JSONDecodeError:
                observation = "Error: Action Input must be valid JSON"
            except Exception as e:
                observation = f"Tool error: {str(e)}"

            messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "Max steps reached without final answer"

# Example usage
def search_web(query: str) -> str:
    # Your implementation
    return f"Search results for: {query}"

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def write_file(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return f"File written: {path}"

tools = {
    "search_web": search_web,
    "read_file": read_file,
    "write_file": write_file,
}

result = react_agent("Research the top 3 Python web frameworks and write a comparison to comparison.md", tools)
print(result)
```

---

## Plan-and-Execute Agent

```python
from openai import OpenAI
import json

client = OpenAI()

PLANNER_SYSTEM = """You are a planning agent. Given a goal, create a step-by-step execution plan.
Output ONLY a JSON array of steps:
[
  {"step": 1, "action": "tool_name", "args": {"param": "value"}, "description": "what this does"},
  ...
]"""

EXECUTOR_SYSTEM = """You are an execution agent. Execute the given step and return the result."""

def plan_and_execute(goal: str, tools: dict) -> str:
    # Phase 1: Plan
    plan_resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM},
            {"role": "user", "content": f"Goal: {goal}"}
        ],
        response_format={"type": "json_object"}
    )
    plan = json.loads(plan_resp.choices[0].message.content)
    steps = plan.get("steps", plan) if isinstance(plan, dict) else plan

    # Phase 2: Execute each step
    results = []
    for step in steps:
        tool_name = step["action"]
        args = step.get("args", {})
        if tool_name in tools:
            result = tools[tool_name](**args)
        else:
            result = f"Unknown tool: {tool_name}"
        results.append({"step": step["step"], "result": result})
        print(f"✓ Step {step['step']}: {step['description']} → {str(result)[:100]}")

    # Phase 3: Synthesize
    synthesis = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":
             f"Goal: {goal}\n\nExecution results:\n{json.dumps(results, indent=2)}\n\nSummarize the final outcome."}
        ]
    )
    return synthesis.choices[0].message.content
```

---

## Multi-Agent System with CrewAI

```python
# pip install crewai crewai-tools
from crewai import Agent, Task, Crew, Process

# Define specialist agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and technology",
    backstory="Expert at finding and synthesizing information from multiple sources.",
    verbose=True,
    allow_delegation=False,
    # tools=[search_tool]  # Add your tools
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content that clearly explains technical topics",
    backstory="Experienced writer who can translate complex topics for any audience.",
    verbose=True,
    allow_delegation=True,
)

# Define tasks
research_task = Task(
    description="Research the latest developments in {topic}. Find key trends and important news.",
    expected_output="A bullet-point summary of the 5 most important developments.",
    agent=researcher,
)

writing_task = Task(
    description="Write a blog post based on the research. 500 words, engaging intro, clear sections.",
    expected_output="A complete 500-word blog post in markdown format.",
    agent=writer,
)

# Assemble and run
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # or Process.hierarchical
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "AI agents in 2025"})
print(result)
```

---

## Agent Memory Systems

### Memory Type Reference

| Memory Type | Storage | Persistence | Purpose |
|-------------|---------|-------------|---------|
| **Conversational (Short-term)** | Messages array | Session only | Current conversation history |
| **Episodic (Long-term)** | Vector DB | Permanent | Past interactions by similarity |
| **Semantic (Knowledge)** | Vector DB | Permanent | Domain facts, RAG knowledge base |
| **Procedural (Skills)** | System prompt | Per-task | How to do specific tasks |
| **Working Memory (Scratchpad)** | Redis / KV | Task duration | Temporary multi-step state |

### Sliding Window Memory (Short-term)

```python
MAX_MESSAGES = 20  # Keep last 10 exchanges
CONTEXT_TOKENS = 4000

def manage_conversation_memory(messages: list[dict]) -> list[dict]:
    """Keep conversation within context limits using sliding window."""
    if len(messages) <= MAX_MESSAGES:
        return messages

    # Always keep system message
    system_msgs = [m for m in messages if m["role"] == "system"]
    recent_msgs = messages[-MAX_MESSAGES:]  # Keep recent exchanges

    # Optionally: summarize older messages
    if len(messages) > MAX_MESSAGES * 2:
        older_msgs = messages[len(system_msgs):-MAX_MESSAGES]
        summary = summarize_conversation(older_msgs)
        summary_msg = {"role": "system",
                       "content": f"[Earlier conversation summary]: {summary}"}
        return system_msgs + [summary_msg] + recent_msgs

    return system_msgs + recent_msgs

def summarize_conversation(messages: list[dict]) -> str:
    """Compress old messages into a summary."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheap model for summaries
        messages=[
            {"role": "system", "content": "Summarize this conversation in 2-3 sentences."},
            {"role": "user", "content": json.dumps(messages)}
        ],
        max_tokens=200
    )
    return resp.choices[0].message.content
```

### Redis-Backed Episodic Memory (Long-term)

```python
import redis, json
from openai import OpenAI
import numpy as np

r = redis.Redis(host="localhost", port=6379)
client = OpenAI()

def embed_text(text: str) -> list[float]:
    return client.embeddings.create(
        model="text-embedding-3-small", input=text).data[0].embedding

def remember(user_id: str, content: str, memory_type: str = "episodic"):
    """Store a memory with embedding for semantic retrieval."""
    emb = embed_text(content)
    key = f"mem:{memory_type}:{user_id}:{hash(content)}"
    r.hset(key, mapping={
        "text": content,
        "embedding": json.dumps(emb),
        "type": memory_type,
        "timestamp": str(datetime.now().isoformat())
    })
    r.expire(key, 86400 * 90)  # 90-day TTL

def recall(user_id: str, query: str, k: int = 5, memory_type: str = "episodic") -> list[str]:
    """Find k most semantically relevant memories."""
    q_emb = np.array(embed_text(query))
    keys = r.keys(f"mem:{memory_type}:{user_id}:*")
    scored = []
    for key in keys:
        data = r.hgetall(key)
        if data:
            mem_emb = np.array(json.loads(data[b"embedding"]))
            similarity = np.dot(q_emb, mem_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(mem_emb))
            scored.append((similarity, data[b"text"].decode()))
    scored.sort(key=lambda x: -x[0])
    return [text for _, text in scored[:k]]

# Usage in agent loop
def agent_with_memory(user_id: str, message: str) -> str:
    # Recall relevant memories
    memories = recall(user_id, message, k=3)
    memory_context = "\n".join([f"- {m}" for m in memories]) if memories else "No relevant memories."

    messages = [
        {"role": "system", "content": f"You are a helpful assistant.\n\nRelevant past context:\n{memory_context}"},
        {"role": "user", "content": message}
    ]
    resp = client.chat.completions.create(model="gpt-4o", messages=messages)
    answer = resp.choices[0].message.content

    # Store this interaction in memory
    remember(user_id, f"User asked: {message}. Assistant answered: {answer[:200]}")
    return answer
```

---

## LangGraph — Stateful Agent Workflows

```python
# pip install langgraph
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_action: str
    result: str

def should_continue(state: AgentState) -> str:
    """Decide whether to continue or end."""
    if state["next_action"] == "end":
        return END
    return "execute_tool"

def llm_node(state: AgentState) -> AgentState:
    """Call the LLM to decide next action."""
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=state["messages"],
        tools=tools
    )
    msg = resp.choices[0].message
    if msg.tool_calls:
        return {"messages": [msg], "next_action": "tool_call"}
    return {"messages": [msg], "next_action": "end", "result": msg.content}

def tool_node(state: AgentState) -> AgentState:
    """Execute the tool call."""
    last_msg = state["messages"][-1]
    results = []
    for call in last_msg.tool_calls:
        result = dispatch_tool(call.function.name, json.loads(call.function.arguments))
        results.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
    return {"messages": results, "next_action": "continue"}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("llm", llm_node)
workflow.add_node("execute_tool", tool_node)
workflow.add_edge("execute_tool", "llm")  # Always go back to LLM after tool
workflow.add_conditional_edges("llm", should_continue)
workflow.set_entry_point("llm")

app = workflow.compile()

# Run
result = app.invoke({
    "messages": [{"role": "user", "content": "What's the weather in London?"}],
    "next_action": "continue"
})
print(result["result"])
```
