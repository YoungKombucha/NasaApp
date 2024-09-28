from dotenv import load_dotenv
import os
import requests

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