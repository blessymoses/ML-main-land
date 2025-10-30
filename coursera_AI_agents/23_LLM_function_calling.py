"""
Using LLM Function Calling for AI-Agent Interaction

One of the most challenging aspects of integrating AI agents with tool execution is ensuring that the model consistently produces structured output that can be parsed correctly.
To solve this, most LLMs offer function calling APIs that guarantee structured execution. Instead of treating function execution as a free-form text generation task, function calling APIs allow us to explicitly define the tools available to the model using JSON Schema. The model then decides when and how to call these functions, ensuring structured and predictable responses.

When using function calling, the model returns either:

A function call that includes the tool name and arguments as structured JSON.
A standard text response if the model decides a function is unnecessary.
This approach removes the need for manual prompt engineering to enforce structured output and allows the agent to focus on decision-making rather than syntax compliance.

Key Benefits of Function Calling APIs

Eliminates prompt engineering for structured responses – No need to force the model to output JSON manually.
Uses standardized JSON Schema – The same format used in API documentation applies seamlessly to AI interactions.
Allows mixed text and tool execution – The model can decide whether a tool is necessary or provide a natural response.
Simplifies parsing logic – Instead of handling inconsistent outputs, developers only check for tool_calls in the response.
Guarantees syntactically correct arguments – The model automatically ensures arguments match the expected parameter format.

Function calling APIs significantly improve the reliability of AI-agent interactions by enforcing structured execution. By defining tools with JSON Schema and letting the model determine when to use them, we build a more predictable and maintainable AI environment interface.
"""
import json
import os
from typing import List

from litellm import completion

def list_files() -> List[str]:
    """List files in the current directory."""
    return os.listdir(".")

def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"


tool_functions = {
    "list_files": list_files,
    "read_file": read_file
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    }
]

# Our rules are simplified since we don't have to worry about getting a specific output format
agent_rules = [{
    "role": "system",
    "content": """
You are an AI agent that can perform tasks by using available tools. 

If a user asks about files, documents, or content, first list the files before reading them.
"""
}]

user_task = input("What would you like me to do? ")

memory = [{"role": "user", "content": user_task}]

messages = agent_rules + memory

response = completion(
    model="openai/gpt-4o",
    messages=messages,
    tools=tools,
    max_tokens=1024
)

# Extract the tool call from the response, note we don't have to parse now!
tool = response.choices[0].message.tool_calls[0]
tool_name = tool.function.name
tool_args = json.loads(tool.function.arguments)
result = tool_functions[tool_name](**tool_args)

print(f"Tool Name: {tool_name}")
print(f"Tool Arguments: {tool_args}")
print(f"Result: {result}")