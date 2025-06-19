# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages.ai import AIMessage

import asyncio

model = ChatOllama(model="qwen3:8b")

# The provided DuckDuckGo Python MCP server
server_params = StdioServerParameters(
    command="uvx",
    args=["ddg-mcp-server"]
)
#message = "Print information about the best restaurant in Göteborg, Sweden. Also print the address. Do your best, don't return links or ask any follw-up questions"
message = "Print information about the best restaurant in Göteborg, Sweden"

async def run_agent(message: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Print tools
            for index, tool in enumerate(tools):
                print(f"Tool {index} name: {tool.name}, description: {tool.description}")   

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": message})
            return agent_response

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent(message))
    for message in result['messages']:
        if isinstance(message, AIMessage):
            print(message.content)