import requests
import cohere

from sklearn.metrics.pairwise import cosine_similarity

import requests
from langchain.tools import tool


co = cohere.Client("URKBopZalYu3WeoBZtmoFm66f3Cnuu7MkLWYyq6a") 
api_key = "F1CDDCD88E044EE3B932AD4F6CEF96C2"

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

def string_to_query_string(s):
    # Replace spaces with '%20'
    query_string = s.replace(' ', '%20')
    return query_string


    
    # Get text embeddings
def get_embeddings(texts, model='embed-english-v3.0', input_type="search_document"):
    output = co.embed(
        model=model,
        input_type=input_type,
        texts=texts)
    return output.embeddings

def cosine_similarity(vector1, vector2):
    """
    Compute cosine similarity between two vectors.

    Args:
    vector1 (numpy array): The first vector.
    vector2 (numpy array): The second vector.

    Returns:
    float: Cosine similarity between the two vectors.
    """
    vector1 = np.squeeze(vector1)
    vector2 = np.squeeze(vector2)
    
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm1 * norm2)
    return similarity

def get_top_locations(query, location_name, category, num_results=3):
    # Fetch data from TripAdvisor API
    locations = get_locations(location_name, category)
    
    if locations:
        # Extract names of locations, descriptions, and ids
        location_data = locations['data']
        location_names = [item['name'] for item in location_data]
        location_ids = [item['location_id'] for item in location_data]
        embeddings = {}
        
        for name, loc_id in zip(location_names, location_ids):
            # Assuming each location name needs embedding
            embedding = get_embeddings([name])  # Pass a list with a single item
            embeddings[loc_id] = {'name': name, 'embedding': embedding}
        
        query_embedding = get_embeddings([query])
        similarities = {}
        for loc_id, loc_data in embeddings.items():
            embedding = loc_data['embedding']
            similarity = cosine_similarity(embedding, query_embedding)
            similarities[loc_id] = similarity
        
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Extract sorted location names and ids
        sorted_location_ids = [loc_id for loc_id, _ in sorted_similarities]
        sorted_location_names = [embeddings[loc_id]['name'] for loc_id in sorted_location_ids]
        
        # Return sorted location names and ids
        return sorted_location_names[:num_results], sorted_location_ids[:num_results]

        
    else:
        return None
    
@tool
def location_search(query, location_name, category) -> list:
    "This tool is only used to find locations on tripadvisor that falls in a specific `category` and `location_name` provided given a user `query`. Do not use it for anything else. `category` is any of the following: hotels, attractions, restaurants"
    return get_top_locations(query, location_name, category)
