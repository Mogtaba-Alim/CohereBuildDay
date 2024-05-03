import requests

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
        