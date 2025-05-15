from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import asyncio
import os
from langchain_core.tools import tool
from dotenv import load_dotenv


async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    
    configuration_file = "server/weather.json"
    
    client = MCPClient.from_config_file(configuration_file)
    llm = ChatGroq(model="llama3-8b-8192")

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )
    
    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")
    
    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue
            
            print("\nAssistant: ", end="", flush=True)
            
            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")
        
    finally:
        if client and client.sessions:
            await client.close_all_sessions()
            

if __name__ =="__main__":
    asyncio.run(run_memory_chat())
