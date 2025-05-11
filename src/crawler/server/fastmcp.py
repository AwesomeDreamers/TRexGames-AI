# 예시: src/mcp_crawler/server/fastmcp.py
import sys


class FastMCP:
    def __init__(self, name: str):
        self.name = name
        self.tools = []

    def tool(self):
        def decorator(func):
            self.tools.append(func)
            print(f"Tool registered: {func.__name__}", file=sys.stderr)
            return func
        return decorator

    def run(self):
        print(f" MCP development server running: {self.name}", file=sys.stderr)
        for tool in self.tools:
            print(f" - Tool: {tool.__name__}", file=sys.stderr)
