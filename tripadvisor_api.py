import requests

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