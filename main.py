from mcp import ClientSession, StdioServerParameters
# from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import json

# > npx @modelcontextprotocol/inspector \
#   uvx \
#   --directory ~/projects/servers/src/git \
#   mcp-server-git \
#   --repository ~/projects/zigpath

# TODO rather than hard code this use the same sort of json 
# config that the Anthropic tools use.
# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="uvx",  # Executable
    args=["--directory", "/Users/justinhj/projects/servers/src/git", "mcp-server-git"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

# Optional: create a sampling callback
# async def handle_sampling_message(
#     message: types.CreateMessageRequestParams,
# ) -> types.CreateMessageResult:
#     return types.CreateMessageResult(
#         role="assistant",
#         content=types.TextContent(
#             type="text",
#             text="Hello, world! from model",
#         ),
#         model="gpt-3.5-turbo",
#         stopReason="endTurn",
#     )

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=None
        ) as session:
            print("Session initializing...")
            # Initialize the connection
            await session.initialize()

            print("Session initialized.")

            # List available prompts
            # prompts = await session.list_prompts()

            # # Get a prompt
            # prompt = await session.get_prompt(
            #     "example-prompt", arguments={"arg1": "value"}
            # )

            # # List available resources
            # resources = await session.list_resources()

            # List available tools
            tools = await session.list_tools()

            print("Available Tools:")
            for tool in tools:
                print(f" - {tool}")
            # # Read a resource
            # content, mime_type = await session.read_resource("file://some/path")

            # Call a tool
            result = await session.call_tool("git_status", arguments={"repo_path": "/Users/justinhj/projects/converse"})
            print(f"Tool result - {result}")

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
