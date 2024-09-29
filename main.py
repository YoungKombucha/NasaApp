from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Access environment variables for each API key
apod_api_key = os.getenv('APOD_API_KEY')
neo_api_key = os.getenv('NEO_API_KEY')

# Check if the API keys were loaded correctly
if not apod_api_key or not neo_api_key:
    raise ValueError("API keys not found. Please check your .env file.")

# Example of loading both keys
print(f"Loaded APOD API key: {apod_api_key[:4]}...")
print(f"Loaded NEO API key: {neo_api_key[:4]}...")

#APOD API
def fetch_apod(api_key):
       url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
       response = requests.get(url)

       if response.status_code == 200:
            apod_data = response.json()
            print("Astronomy Picture of the Day:")
            print("Title:", apod_data['title'])
            print("Explanation:", apod_data['explanation'])
            print("URL:", apod_data['url'])
       else:
            print(f"Error fetching APOD data: {response.status_code}")

fetch_apod(apod_api_key)

#NEO API
def fetch_neo(api_key):
        today = datetime.today().strftime('%Y-%m-%d')
        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            neo_data = response.json()
            asteroids = neo_data['near_earth_objects'][today]
            print("Near-Earth Objects for {today}:")
            for asteroid in asteroids:
                print("Name:", asteroid['name'])
                print("Diameter (m):", asteroid['estimated_diameter']['meters']['estimated_diameter_max'])
                print("Potentially Hazardous:", asteroid['is_potentially_hazardous_asteroid'])
                print("Closest Approach Date:", asteroid['close_approach_data'][0]['close_approach_date'])
                print("Miss Distance (km):", asteroid['close_approach_data'][0]['miss_distance']['kilometers'])
            else:
                print(f"Error fetching NEO data: {response.status_code}")
fetch_neo(neo_api_key)

# Menu
def menu():
    print("Nasa API Application")
    print("1. Astronomy Picture of the Day")
    print("2. Near-Earth Objects")
    choice = input("Choose an option: ")
    if choice == '1':
        fetch_apod(apod_api_key)
    elif choice == '2':
        fetch_neo(neo_api_key)
    else:
        print("Invalid choice. Please try again.")
if __name__ == "__main__":
    menu()