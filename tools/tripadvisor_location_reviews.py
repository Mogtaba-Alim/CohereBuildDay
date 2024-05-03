

import requests
from langchain.tools import tool
from langchain_cohere.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
os.environ['COHERE_API_KEY'] = 'URKBopZalYu3WeoBZtmoFm66f3Cnuu7MkLWYyq6a'
os.environ['TRIPADVISOR_API'] = 'F1CDDCD88E044EE3B932AD4F6CEF96C2'

chat = ChatCohere(model='command-plus-r', temperature=0.3)
prompt = ChatPromptTemplate.from_template("""Summarize the ratings of the given location \n {ratings}""")


chain = prompt | chat | StrOutputParser()

def get_location_reviews(location_id):
    k = 30
    api_key = os.environ['TRIPADVISOR_API']
    url = f"https://api.content.tripadvisor.com/api/v1/location/%7Blocation_id%7D/reviews?language=en&limit={k}&key={api_key}"

    response = requests.get(url)

    if response.status_code==200:
        data = response.json()['data']
        if data and isinstance(data, list) and len(data) > 0:
            retrieved_ratings = []
            for i, review in enumerate(data):
                retrieved_ratings.append(
                    dict(
                        id=i, 
                        text=f"User Rating: {review.get('rating', '')} User Review: {review.get('text', '')}"
                        )
                )

            return chain.invoke(dict(ratings=retrieved_ratings))

        else:
            return 'No Reviews available for this location'
    else:
        return "Failed to retrieve data from the API"
@tool
def location_reviews(location_id) -> list:
    "This tool is only used to find ratings and reviews of given locations (indicated by the location_id). Do not use it for anything else."
    return get_location_reviews(location_id)