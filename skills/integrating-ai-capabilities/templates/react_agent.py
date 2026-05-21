"""
ReAct Agent — Full Production Template
Autonomous agent with tool calling, memory, and observability.
Works with: OpenAI function calling API (native tool use).
"""

import os
import json
import time
import logging
from openai import OpenAI
from typing import Callable, Any
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ─── Tool Registry ────────────────────────────────────────────────────────────
@dataclass
class Tool:
    """A tool definition for the agent."""
    name: str
    description: str
    parameters: dict        # JSON Schema for parameters
    function: Callable      # The actual Python function to call
    
    def to_openai_schema(self) -> dict:
        """Convert to OpenAI tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

class ToolRegistry:
    """Registry of available tools for the agent."""
    
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def register(self, name: str, description: str, parameters: dict) -> Callable:
        """Decorator to register a function as a tool."""
        def decorator(func: Callable) -> Callable:
            self._tools[name] = Tool(
                name=name,
                description=description,
                parameters=parameters,
                function=func
            )
            logger.debug(f"Registered tool: {name}")
            return func
        return decorator
    
    def get_schemas(self) -> list[dict]:
        """Get all tool schemas for the LLM."""
        return [tool.to_openai_schema() for tool in self._tools.values()]
    
    def execute(self, name: str, args: dict) -> Any:
        """Execute a tool by name with given args."""
        if name not in self._tools:
            raise ValueError(f"Unknown tool: '{name}'. Available: {list(self._tools.keys())}")
        tool = self._tools[name]
        logger.info(f"Executing tool: {name}({args})")
        return tool.function(**args)

# ─── Create your tool registry ───────────────────────────────────────────────
registry = ToolRegistry()

# Example tools — replace/add your own
@registry.register(
    name="search_web",
    description="Search the web for current information on a topic",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "num_results": {"type": "integer", "description": "Number of results (1-10)", "default": 5}
        },
        "required": ["query"]
    }
)
def search_web(query: str, num_results: int = 5) -> str:
    """Your web search implementation here."""
    # Replace with: Serper API, Tavily, SerpAPI, or Bing Search
    return f"[Search results for '{query}' - implement with Serper/Tavily/SerpAPI]"

@registry.register(
    name="read_file",
    description="Read the contents of a file from the filesystem",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path to read"}
        },
        "required": ["path"]
    }
)
def read_file(path: str) -> str:
    """Read a file safely."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@registry.register(
    name="write_file",
    description="Write content to a file",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path to write"},
            "content": {"type": "string", "description": "Content to write"},
            "mode": {"type": "string", "enum": ["write", "append"], "default": "write"}
        },
        "required": ["path", "content"]
    }
)
def write_file(path: str, content: str, mode: str = "write") -> str:
    """Write to a file safely."""
    try:
        file_mode = "w" if mode == "write" else "a"
        with open(path, file_mode) as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# ─── Agent Implementation ─────────────────────────────────────────────────────
@dataclass
class AgentRun:
    """Result of an agent execution."""
    goal: str
    final_answer: str
    steps: list[dict] = field(default_factory=list)
    total_tokens: int = 0
    duration_seconds: float = 0
    success: bool = True
    error: str = ""

AGENT_SYSTEM = """You are an autonomous AI agent. You have access to tools to help you accomplish goals.

When working on a task:
1. Think through what information or actions you need
2. Use your available tools to gather information or take actions
3. Analyze the results and decide on next steps
4. Once you have everything needed, provide a comprehensive final answer

Be thorough but efficient. Only call tools when necessary.
Always verify your work before declaring completion."""

def run_agent(goal: str,
              model: str = "gpt-4o",
              max_steps: int = 15,
              verbose: bool = True) -> AgentRun:
    """
    Run the ReAct agent to accomplish a goal.
    
    Args:
        goal: What the agent should accomplish
        model: LLM model (gpt-4o or claude-sonnet-4-5 recommended)
        max_steps: Maximum tool calls before stopping
        verbose: Whether to print step-by-step progress
    
    Returns:
        AgentRun with final answer and execution trace
    """
    start_time = time.time()
    messages = [
        {"role": "system", "content": AGENT_SYSTEM},
        {"role": "user", "content": f"Goal: {goal}"}
    ]
    
    run = AgentRun(goal=goal, final_answer="")
    tools = registry.get_schemas()
    
    if verbose:
        print(f"\n🚀 Agent starting: {goal}\n{'─'*60}")
    
    for step in range(max_steps):
        try:
            # Call LLM
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=2000,
            )
            
            msg = resp.choices[0].message
            run.total_tokens += resp.usage.total_tokens
            messages.append(msg)
            
            # No tool calls = final answer
            if not msg.tool_calls:
                run.final_answer = msg.content
                run.duration_seconds = time.time() - start_time
                if verbose:
                    print(f"\n✅ Final Answer: {msg.content}")
                    print(f"Steps: {step+1} | Tokens: {run.total_tokens} | Time: {run.duration_seconds:.1f}s")
                return run
            
            # Execute tool calls
            step_info = {"step": step + 1, "tool_calls": []}
            
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                if verbose:
                    print(f"\n[Step {step+1}] 🔧 {tool_name}({json.dumps(tool_args)[:100]})")
                
                # Execute tool
                try:
                    result = registry.execute(tool_name, tool_args)
                except Exception as e:
                    result = f"Tool execution error: {str(e)}"
                
                result_str = str(result)
                if verbose:
                    print(f"           ← {result_str[:150]}{'...' if len(result_str) > 150 else ''}")
                
                step_info["tool_calls"].append({
                    "tool": tool_name, "args": tool_args, "result": result_str
                })
                
                # Feed result back to LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_str
                })
            
            run.steps.append(step_info)
            
        except Exception as e:
            run.success = False
            run.error = str(e)
            run.duration_seconds = time.time() - start_time
            logger.error(f"Agent error at step {step}: {e}")
            return run
    
    # Max steps reached
    run.final_answer = "Maximum steps reached without completing the goal."
    run.duration_seconds = time.time() - start_time
    return run

# ─── Usage Example ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run_agent(
        goal="Search for the latest developments in AI agents (2025) and write a 200-word summary to summary.txt",
        verbose=True
    )
    
    if result.success:
        print(f"\n📊 Execution Summary:")
        print(f"  Steps taken: {len(result.steps)}")
        print(f"  Total tokens: {result.total_tokens}")
        print(f"  Duration: {result.duration_seconds:.1f}s")
    else:
        print(f"❌ Agent failed: {result.error}")
