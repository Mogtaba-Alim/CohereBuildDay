# LLM

from langchain.agents import AgentExecutor
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere.chat_models import ChatCohere

chat = ChatCohere(model="command-r-plus", temperature=0.3)

# Preamble
preamble = """You are a frinedly travel agent that assists customers find the best destination given their preferences and motivation for travelling 

First, you draft an itinerary based on the user message. you can use the search_tool for this task. 
Second, you look for "hotels", "attractions", and "restaurants", using the location_search tool. Return the location name and the address. 
Third, you look at location reviews using the location_id and the location_review tool. Provide a summary of the location_reviews per location

You are equipped with an location_search tool, a location_review_tool, and a search_tool. 

Ensure that your responses will have a daily itinerary breakdown. 
"""

tool_list = [location_search, location_reviews, search_tool]

prompt = ChatPromptTemplate.from_template("{input}")
agent = create_cohere_react_agent(
    llm=chat,
    tools=tool_list,
    prompt=prompt,
)