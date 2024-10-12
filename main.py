from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from tabulate import tabulate

# Load environment variables from the .env file
load_dotenv()

# Access environment variables for each API key
apod_api_key = os.getenv('APOD_API_KEY')
neo_api_key = os.getenv('NEO_API_KEY')

# APOD API
def fetch_apod(api_key):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    print(f"APOD API request URL: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        apod_data = response.json()
        print("Astronomy Picture of the Day:")
        print("Title:", apod_data['title'])
        print("Explanation:", apod_data['explanation'])
        print("URL:", apod_data['url'])

        # Display the image
        image_url = apod_data['url']
        image_response = requests.get(image_url)
        img = Image.open(BytesIO(image_response.content))
        img.show()

        # Save the image locally
        save_image_locally(img, apod_data['title'])
    elif response.status_code == 400:
        print("Bad request. Please check your API key and parameters.")
    elif response.status_code == 403:
        print("Forbidden request. Check if the API key is valid and if you have the necessary permissions.")
        print("Response content:", response.content)
    else:
        print(f"Error: Received unexpected status code {response.status_code}")

def save_image_locally(img, title):
    filename = f"{title.replace(' ', '_')}.jpg"
    img.save(filename)
    print(f"Image saved as {filename}")

# NEO API
def fetch_neo(api_key):
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}"
        print(f"NeoWs API request URL: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            neo_data = response.json()
            asteroids = neo_data['near_earth_objects'][today]

            print(f"Near-Earth Objects for {today}:")
            table_data = []
            for asteroid in asteroids:
                table_data.append([
                    asteroid['name'],
                    asteroid['estimated_diameter']['meters']['estimated_diameter_max'],
                    asteroid['is_potentially_hazardous_asteroid'],
                    asteroid['close_approach_data'][0]['close_approach_date'],
                    asteroid['close_approach_data'][0]['miss_distance']['kilometers']
                ])
            print(tabulate(table_data, headers=["Name", "Diameter (m)", "Potentially Hazardous", "Closest Approach Date", "Miss Distance (km)"]))
        elif response.status_code == 403:
            print("Forbidden request. Check if the API key is valid and if you have the necessary permissions.")
            print("Response content:", response.content)
        else:
            print(f"Error fetching NEO data: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Menu
def menu():
    while True:
        print("\nNasa API Application")
        print("1. Fetch Astronomy Picture of the Day (APOD)")
        print("2. Fetch Near-Earth Objects (NEO)")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            fetch_apod(apod_api_key)
        elif choice == '2':
            fetch_neo(neo_api_key)
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

# Check if the API keys were loaded correctly
if not apod_api_key or not neo_api_key:
    raise ValueError("API keys not found. Please check your .env file.")

# Example of loading both keys
print(f"Loaded APOD API key: {apod_api_key[:4]}...")
print(f"Loaded NEO API key: {neo_api_key[:4]}...")

# Run the menu
menu()