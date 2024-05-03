import requests
from langchain.tools import tool
from tools.tripadvisor_location_search import get_top_locations

api_key = "F1CDDCD88E044EE3B932AD4F6CEF96C2"


def string_to_query_string(s):
    # Replace spaces with '%20'
    query_string = s.replace(' ', '%20')
    return 

def get_locations(location, category):
    formattedLocation = string_to_query_string(location)
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={api_key}&searchQuery={location}&category={category}&language=en"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return None

def get_location_reviews(location_id):
    k = 30
    api_key = os.environ['TRIPADVISOR_API']
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews?language=en&limit={k}&key={api_key}"

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
            return retrieved_ratings    

        else:
            return 'No Reviews available for this location'
    else:
        return "Failed to retrieve data from the API"
        

@tool
def location_search(city, category) -> list:
    "This tool is only used to find locations on tripadvisor that falls in a specific category and city provided.. Do not use it for anything else. `category` is any of the following: hotels, attractions, restaurants"
    return get_locations(city, category)


@tool
def location_reviews(location_id) -> list:
    "This tool is only used to find ratings and reviews of given locations (indicated by the location_id). Do not use it for anything else."
    return get_location_reviews(location_id)