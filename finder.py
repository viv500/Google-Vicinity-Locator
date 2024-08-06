import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import time  # Import the time module for adding delay

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
        messagebox.showerror("API Error", "Unable to fetch place details or invalid Place ID.")
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
    
    data = []
    next_page_token = None
    
    while True:
        if next_page_token:
            nearby_search_params['pagetoken'] = next_page_token
            time.sleep(2)  # Add delay to handle the token's validity time
        
        # Make the request to Nearby Search API
        nearby_search_response = requests.get(nearby_search_endpoint, params=nearby_search_params)
        nearby_places = nearby_search_response.json()
        
        # Check if the response contains results
        if 'results' not in nearby_places:
            break
        
        # Collect information about each place
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
        
        # Check if there's a next page token
        next_page_token = nearby_places.get('next_page_token')
        if not next_page_token:
            break
    
    # Generating a DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to an Excel file
    try:
        df.to_excel(excel_sheet, index=False)
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to save the Excel file: {e}")
        return
    
    return excel_sheet

def generate_report():
    api_key = os.getenv('GOOGLE_API_KEY')
    place_id = place_id_entry.get().strip()
    radius_str = radius_entry.get().strip()
    keyword = keyword_entry.get().strip()
    
    if not place_id:
        messagebox.showerror("Input Error", "Please fill in the Place ID.")
        return
    
    if not radius_str:
        messagebox.showerror("Input Error", "Please fill in the Radius.")
        return
    
    try:
        radius = int(radius_str)
    except ValueError:
        messagebox.showerror("Input Error", "Radius must be a number.")
        return
    
    # Get the user's Documents directory
    documents_dir = os.path.expanduser("~/Documents")
    
    # Open a file dialog to select the save location and filename, defaulting to the Documents directory
    file_path = filedialog.asksaveasfilename(
        initialdir=documents_dir,
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        title="Save Excel File As"
    )
    
    if not file_path:
        return  # User cancelled the file dialog
    
    # Call the function to generate the report
    result_file = get_nearby_places(api_key, place_id, radius, keyword, file_path)
    
    if result_file:
        messagebox.showinfo("Success", f"Data has been written to {result_file}")

# Create the main window
root = tk.Tk()
root.title("Nearby Places Finder")

# Create and place widgets
tk.Label(root, text="Place ID:").grid(row=0, column=0, padx=10, pady=10)
place_id_entry = tk.Entry(root)
place_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Radius (meters):").grid(row=1, column=0, padx=10, pady=10)
radius_entry = tk.Entry(root)
radius_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Keyword (optional):").grid(row=2, column=0, padx=10, pady=10)
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=2, column=1, padx=10, pady=10)

generate_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
