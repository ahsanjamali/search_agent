import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Search Agent",
    page_icon=":mag:",
    layout="wide"
)

#add custom CSS
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .output-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px 0;
    }
    </style>
    """,unsafe_allow_html=True
)

@st.cache_resource
def create_search_agent():
    """Create and cache the search agent"""
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo"
    )

    search_tool = DuckDuckGoSearchRun()

    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent


def main():
    st.title("Search Agent")
    st.markdown("Ask me anything, and I'll search the web for you.")

    #initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


    #create agent
    agent = create_search_agent()

    #display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    #query input
    if prompt := st.chat_input("What would you like to know?"):
        #display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})


        #display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching the web..."):
                try:
                    response = agent.invoke(prompt)
                    st.markdown(response["output"])
                    st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

    
    #add a clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
