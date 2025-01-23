from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

#create the agent

memory = MemorySaver()
model = ChatOpenAI(model="gpt-3.5-turbo")
search = DuckDuckGoSearchRun()
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)


# Use the agent
config = {"configurable": {"thread_id": "abc123"}}

# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="Hi im Ahsan! and I live in sf")]}, config
# ):
#     print(chunk)
#     print("------")


# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
# ):
#     print(chunk)
#     print("------")


response = agent_executor.invoke(
    {"messages": [HumanMessage(content="Hi im Ahsan! and I want to get US updates.")]}, config
)
print(response["messages"][-1].content)

response = agent_executor.invoke(
    {"messages": [HumanMessage(content="Who is the president of the US?")]}, config
)
print(response["messages"][-1].content)
