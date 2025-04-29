# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages.ai import AIMessage

import asyncio

model = ChatOllama(model="qwen3:8b")

server_params = StdioServerParameters(
    command="npx",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["@playwright/mcp@latest", "--headless"],
    env={"DISPLAY": ":1",
         }
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            for tool in tools:
                print(f"Tool name: {tool.name}")

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "Using google.com, find the best restaurant in San Francisco"})
            return agent_response

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    for message in result['messages']:
        if isinstance(message, AIMessage):
            print(message.content)