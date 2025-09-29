# Import the OpenAI client for chat completions (special wrapper from autogen_ext)
from autogen_ext.models.openai import OpenAIChatCompletionClient  

# asyncio is required to run asynchronous (async/await) code in Python
import asyncio  

# Import AssistantAgent (our AI agent) from the new autogen package location
from autogen_agentchat.agents import AssistantAgent  

# Import message types that the agent can process (text + multimodal)
from autogen_agentchat.messages import TextMessage, MultiModalMessage  

# Import Image wrapper class from autogen_core (needed for multimodal image messages)
from autogen_core import Image as AGImage  

# Image processing libraries
from PIL import Image            # Pillow (PIL) handles images in Python
from io import BytesIO           # Helps convert raw bytes into image objects
import requests                  # Used to fetch an image from the internet  

# For reading environment variables (like API keys) securely
from dotenv import load_dotenv  
import os  

# Load values from the `.env` file into environment variables
load_dotenv()  

# Get the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")  

# Print True if API key is loaded successfully, False otherwise
print("Using OpenAI key :", bool(api_key))  

# Initialize the OpenAI client with model = gpt-4o (multimodal model)
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key)  

# Initialize an AssistantAgent that uses the OpenAI client
Assistant = AssistantAgent(
    name="Text_Agent",                         # Give the agent a name
    model_client=model_client,                 # Pass in the model client
    system_message="You are a helpful agent that can answer questions accurately."  
    # System message = instructions for how the AI should behave
)  

# ---------------- TEXT TASK -----------------
async def main():  
    # Ask the assistant a simple question (capital of Pakistan)
    result = await Assistant.run(task="capital of pakistan?")  

    # Loop through all returned messages from the agent
    for msg in result.messages:  
        # If the message comes from our Text_Agent, print the answer
        if msg.source == "Text_Agent":  
            print("Text Result:", msg.content)  

# ---------------- IMAGE DESCRIPTION TASK -----------------
async def test_multi_agent():  
    # Download an example image from the internet
    response = requests.get("https://picsum.photos/id/237/200/300")  

    # Open the image using Pillow (PIL)
    pil_image = Image.open(BytesIO(response.content))  

    # Convert PIL image into AGImage (Autogen’s format for images)
    ag_image = AGImage(pil_image)  

    # Build a multimodal message (text + image)
    multi_media_msg = MultiModalMessage(
        content=["Describe the image in detail", ag_image],  # Ask + provide image
        source="User"                                       # The sender is User
    )  

    # Send multimodal message to Assistant
    result = await Assistant.run(task=multi_media_msg)  

    # Loop through agent responses
    for msg in result.messages:  
        if msg.source == "Text_Agent":  
            # Print the detailed image description
            print("Image Description:", msg.content)  

# ---------------- RUN BOTH TASKS -----------------
if __name__ == "__main__":  
    # Run text-only question
    asyncio.run(main())  

    # Run image description question
    asyncio.run(test_multi_agent())  
