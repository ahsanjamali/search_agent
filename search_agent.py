from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_search_agent():
    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    # Initialize the search tool
    search_tool = DuckDuckGoSearchRun()

    # Initialize the agent
    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent

def main():
    agent = create_search_agent()

    while True:
        query = input("Enter a search query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        try:
            response = agent.invoke(query)
            print("\nAgent Response:", response["output"])
        except Exception as e:
            print(f"\nAn error occurred: {e}")
    
if __name__ == "__main__":
    main()
