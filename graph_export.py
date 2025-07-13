import sys
import os
from langchain_google_genai import ChatGoogleGenerativeAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.agent import Agent
# Use Gemini (or switch to OpenAI if needed)
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

# Initialize your agent
agent = Agent(model)

# 👇 LangGraph Studio expects this variable
graph = agent.graph
