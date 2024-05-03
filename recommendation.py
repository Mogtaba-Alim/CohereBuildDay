import os
import cohere
from langchain_community.tools.tavily_search import TavilySearchResults


def get_city_list():
    COHERE_API_KEY='vgn4U23H3lwEB9GJR8taiBIZCUnmpKA6trYgUAbN'


    print("Let Your Feeling Fly! Answer the following questions and let us do the rest!")

    # Prompting the user to describe their desired experience, travel companions, and duration of travel
    experience = input("Describe the experience that you want to have: ")
    companions = input("Who are you taking with you: ")
    duration = input("For how long do you wish to travel: ")

    # Storing the responses in a text variable
    initial_answers = f"Experience: {experience}\nCompanions: {companions}\nDuration: {duration}"

    print("\nThank you! Your answers have been recorded.")
    print("Here are your responses:")
    print(initial_answers)

    co = cohere.Client(COHERE_API_KEY)


    # Define the initial chat history with the user's initial answers
    chat_history = [
        {"role": "USER", "message": "These are the experiences that a person wants to have."},
        {
            "role": "CHATBOT",
            "message": initial_answers,
        },
    ]

    # Ask the chatbot to suggest the top 3 countries
    message = "Can you suggest the top only 3 countries that would be a good fit for this experience? Return only the names of the 3 countries as a comma seperated list with nothing else."
    response = co.chat(
        chat_history=chat_history,
        message=message,
        # Optionally, you can perform a web search before answering the question.
        connectors=[{"id": "web-search"}],
    )

    # Assuming you have already extracted the API response and stored it in the 'response' variable

    # Extracting the list of three countries from the API response
    api_response = response.text
    countries_list = [country.strip() for country in api_response.split(',')]

    # Presenting the user with the prompt
    print("That looks like the making of a great trip! These are the top 3 destinations that will Fit Your Feelings:")
    for idx, country in enumerate(countries_list, 1):
        print(f"{idx}. {country}")

    # Prompting the user to select their desired destination
    selected_country = None
    while selected_country not in range(1, 4):
        try:
            selected_country = int(input("Please select a destination by entering the corresponding number (1-3): "))
            if selected_country not in range(1, 4):
                print("Invalid input. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Now you have the selected destination
    print(f"You have selected: {countries_list[selected_country - 1]}")


    # Define the chat history with the user's initial answers and selected country
    chat_history = [
        {"role": "USER", "message": initial_answers},
        {"role": "CHATBOT", "message": str(selected_country)}
    ]

    # Ask the chatbot to suggest a list of cities for each day of the trip
    message = f"Can you suggest a list of cities for each day of the trip in {selected_country}? Return only the list of cities that are in the country as a comma seperated list and nothing else"
    response = co.chat(
        chat_history=chat_history,
        message=message,
        # Optionally, you can perform a web search before answering the question.
        connectors=[{"id": "web-search"}],
    )

    # Extract the list of cities from the API response
    cities_list = response.text.split(',')

    unique_cities = list(set(cities_list))[:5]

    # Print the list of unique cities for each day of the trip
    print("Here is the list of cities for each day of your trip:")
    for idx, city in enumerate(unique_cities, 1):
        print(f"Day {idx}: {city}")

    return unique_cities, experience


# Describe the experience that you want to have: I want to have a romantic experience somewhere with a coast
# Who are you taking with you: My fiancé
# For how long do you wish to travel: 5 days