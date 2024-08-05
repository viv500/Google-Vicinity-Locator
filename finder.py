import requests
from dotenv import load_dotenv
import os
import pandas as pd

# Load the environment variables from the .env file
load_dotenv()

def get_nearby_places(api_key, place_id, radius, keyword, excel_sheet):
    # Endpoint for places API
    place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
    
    # JSONifying our details to provide to the API
    place_details_params = {
        'key': api_key,
        'place_id': place_id,
        'fields': 'geometry'
    }
    
    # Request to Google Places API
    place_details_response = requests.get(place_details_endpoint, params=place_details_params)
    place_details = place_details_response.json()
    
    if 'result' not in place_details or 'geometry' not in place_details['result']:
        print("Error: Unable to fetch place details or invalid Place ID.")
        return
    
    # Getting the latitude and longitude
    location = place_details['result']['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']
    
    # Endpoint for Nearby Search API call
    nearby_search_endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    # Set up parameters for Nearby Search
    nearby_search_params = {
        'key': api_key,
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'keyword': keyword if keyword and keyword != 'None' else ''
    }
    
    # Make the request to Nearby Search API
    nearby_search_response = requests.get(nearby_search_endpoint, params=nearby_search_params)
    nearby_places = nearby_search_response.json()
    
    # Check if the response contains results
    if 'results' not in nearby_places:
        print("Error: No results found or unable to fetch nearby places.")
        return
    
    # Collect information about each place
    data = []
    for place in nearby_places['results']:
        name = place.get('name', 'N/A')
        address = place.get('vicinity', 'N/A')
        place_id = place.get('place_id', 'N/A')
        types = place.get('types', [])
        rating = place.get('rating', 'N/A')
        
        data.append({
            'Name': name,
            'Address': address,
            'Place ID': place_id,
            'Types': ', '.join(types),
            'Rating': rating
        })
    
    # generating a dataframe
    df = pd.DataFrame(data)
    
    # Save the DataFrame to an Excel file
    df.to_excel(excel_sheet, index=False)
    print(f"Data has been written to {excel_sheet}")

# Example usage
place_id = 'ChIJUYmgCSSuEmsREh0wG5hVCQk'  # Replace with a valid Place ID
radius = 20  # Radius in meters
api_key = os.getenv('GOOGLE_API_KEY')
excel_sheet = 'nearby_places.xlsx'

# Call the function
get_nearby_places(api_key, place_id, radius, '', excel_sheet)
