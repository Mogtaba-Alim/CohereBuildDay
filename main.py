from recommendation import get_city_list
from tools.tripadvisor_location_search import get_top_locations
from tools.tripadvisor_location_reviews import get_location_reviews

cities, experience = get_city_list()
attractions = []
hotels = []
names = []
for city in cities:
    city_top_locations1 = get_top_locations(experience, city, "attractions")
    names.append(city_top_locations1[0])
    attractions.append(city_top_locations1[1])
    city_top_locations2 = get_top_locations(experience, city, "hotels")
    names.append(city_top_locations2[0])
    attractions.append(city_top_locations2[1])

locations = city_top_locations1 + city_top_locations2
print(locations)
# location_ids = sum(city_top_locations1[1] + city_top_locations2[1], [])
location_ids = [2464153, 182739, 4598748, 1674841, 2080716, 579048]
for loc_id in location_ids:
    print(get_location_reviews(loc_id))


