import requests
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

def get_nearby_places(api_key, place_id, radius):
    # Define the endpoint for Place Details API
    place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
    
    # Fetch Place Details to get the location coordinates
    place_details_params = {
        'key': api_key,
        'place_id': place_id,
        'fields': 'geometry'
    }
    
    place_details_response = requests.get(place_details_endpoint, params=place_details_params)
    place_details = place_details_response.json()
    
    if 'result' not in place_details or 'geometry' not in place_details['result']:
        print("Error: Unable to fetch place details or invalid Place ID.")
        return
    
    # Extract latitude and longitude
    location = place_details['result']['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']
    
    # Define the endpoint for Nearby Search API
    nearby_search_endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    # Set up parameters for Nearby Search
    nearby_search_params = {
        'key': api_key,
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'keyword': ''  # You can specify a keyword or leave it empty for all types of places
    }
    
    # Make the request to Nearby Search API
    nearby_search_response = requests.get(nearby_search_endpoint, params=nearby_search_params)
    nearby_places = nearby_search_response.json()
    
    # Check if the response contains results
    if 'results' not in nearby_places:
        print("Error: No results found or unable to fetch nearby places.")
        return
    
    # Print information about each place
    for place in nearby_places['results']:
        name = place.get('name', 'N/A')
        address = place.get('vicinity', 'N/A')
        place_id = place.get('place_id', 'N/A')
        types = place.get('types', [])
        rating = place.get('rating', 'N/A')
        
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Place ID: {place_id}")
        print(f"Types: {', '.join(types)}")
        print(f"Rating: {rating}")
        print("-" * 40)

# Example usage
place_id = 'ChIJUYmgCSSuEmsREh0wG5hVCQk'  # Replace with a valid Place ID
radius = 1500  # Radius in meters

# Retrieve the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Call the function with the API key, Place ID, and radius
get_nearby_places(api_key, place_id, radius)
