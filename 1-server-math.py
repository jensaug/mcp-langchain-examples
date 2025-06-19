from mcp.server.fastmcp import FastMCP

# Python stdio server implemented uing FastMCP with two MCP tools

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"Adding...")
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print(f"Multiplying...")
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")