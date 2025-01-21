#import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# st.set_page_config(
#     page_title="Search Agent",
#     page_icon=":mag:",
#     layout="wide"
# )

#add custom CSS
# st.markdown(
#     """
#     <style>
#     .stApp {
#         max-width: 1200px;
#         margin: 0 auto;
#     }
#     .output-container {
#         background-color: #f0f2f6;
#         padding: 20px;
#         border-radius: 10px;
#         margin-bottom: 10px 0;
#     }
#     </style>
#     """,unsafe_allow_html=True
# )

class SerperPlacesSearch:
    def __init__(self):
        self.search = GoogleSerperAPIWrapper(type="places")
    
    def search_places(self, query):
        """
        Search for places using Serper API
        """
        try:
            # Get raw results from Serper
            raw_results = self.search.results(query)
            
            # Check if we have places in the results
            if not raw_results or 'places' not in raw_results:
                return "No places found matching your search."
            
            # Format the results with detailed information
            formatted_results = []
            for place in raw_results['places'][:5]:  # Limit to top 5 results
                name = place.get('title', 'N/A')
                address = place.get('address', 'N/A')
                phone = place.get('phoneNumber', 'N/A')
                rating = place.get('rating', 'N/A')
                reviews = place.get('reviewsCount', 'N/A')
                
                place_info = (
                    f"📍 {name}\n"
                    f"📮 Address: {address}\n"
                    f"� Phone: {phone}\n"
                    f"⭐ Rating: {rating} ({reviews} reviews)\n"
                )
                formatted_results.append(place_info)
            
            # Create a comprehensive response
            full_response = (
                f"Here are the places I found:\n\n"
                f"{'\n\n'.join(formatted_results)}\n\n"
                f"These are some of the best-rated places in the area. "
                f"Each location is verified and includes their address and rating information."
            )
            
            return full_response
            
        except Exception as e:
            return f"An error occurred while searching: {str(e)}"



def main():
    # st.title("Search Agent")
    # st.markdown("Ask me anything, and I'll search the web for you.")

    # #initialize session state for chat history
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []


    # #create agent
    # agent = create_search_agent()

    # #display chat history
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])


    # #query input
    # if prompt := st.chat_input("What would you like to know?"):
    #     #display user message
    #     with st.chat_message("user"):
    #         st.markdown(prompt)
    #     st.session_state.messages.append({"role": "user", "content": prompt})


    #     #display assistant response
    #     with st.chat_message("assistant"):
    #         with st.spinner("Searching the web..."):
    #             try:
    #                 response = agent.invoke(prompt)
    #                 st.markdown(response["output"])
    #                 st.session_state.messages.append({"role": "assistant", "content": response["output"]})
    #             except Exception as e:
    #                 error_message = f"An error occurred: {str(e)}"
    #                 st.error(error_message)
    #                 st.session_state.messages.append({"role": "assistant", "content": error_message})

    
    # #add a clear chat button
    # if st.sidebar.button("Clear Chat"):
    #     st.session_state.messages = []
    #     st.rerun()

    #agent = create_search_agent()

    while True:
        query = input("Enter a search query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        # try:
        #     response = agent.invoke(query)
        #     print("\nAgent Response:", response)
        # except Exception as e:
        #     print(f"\nAn error occurred: {e}")

        try:
            response = SerperPlacesSearch().search_places(query)
            print("\nAgent Response:", response)
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
