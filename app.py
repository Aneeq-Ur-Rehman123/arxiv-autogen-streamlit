from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio

# Load OpenAI key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("Using OpenAI key:", bool(api_key))

# Create client and assistant
client = OpenAIChatCompletionClient(model="gpt-4o", openai_api_key=api_key)
Assistant = AssistantAgent(
    name="Assistant",
    model_client=client,
    description="A basic first agent"
)

async def main():
    result = await Assistant.run(task="top 5 ai tools")
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())