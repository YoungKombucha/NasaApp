import os
import requests
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv

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
            return tabulate(table_data, headers=["Name", "Diameter (m)", "Potentially Hazardous", "Closest Approach Date", "Miss Distance (km)"])
        elif response.status_code == 403:
            print("Forbidden request. Check if the API key is valid and if you have the necessary permissions.")
            print("Response content:", response.content)
        else:
            print(f"Error fetching NEO data: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# GUI
def create_gui():
    global apod_image_label, neo_text

    root = tk.Tk()
    root.title("NASA API Application")

    # APOD Section
    apod_frame = ttk.LabelFrame(root, text="Astronomy Picture of the Day (APOD)")
    apod_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    apod_button = ttk.Button(apod_frame, text="Fetch APOD", command=lambda: display_apod(apod_api_key))
    apod_button.grid(row=0, column=0, padx=10, pady=10)

    apod_image_label = ttk.Label(apod_frame)
    apod_image_label.grid(row=1, column=0, padx=10, pady=10)

    # NEO Section
    neo_frame = ttk.LabelFrame(root, text="Near-Earth Objects (NEO)")
    neo_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    neo_button = ttk.Button(neo_frame, text="Fetch NEO", command=lambda: display_neo(neo_api_key))
    neo_button.grid(row=0, column=0, padx=10, pady=10)

    neo_text = tk.Text(neo_frame, wrap="word", height=10, width=80)
    neo_text.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()

def display_apod(api_key):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        apod_data = response.json()
        image_url = apod_data['url']
        image_response = requests.get(image_url)
        img = Image.open(BytesIO(image_response.content))
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)

        apod_image_label.config(image=img_tk)
        apod_image_label.image = img_tk  # Keep a reference to avoid garbage collection

        # Save the image locally
        save_image_locally(img, apod_data['title'])
    else:
        messagebox.showerror("Error", f"Failed to fetch APOD: {response.status_code}")

def display_neo(api_key):
    neo_data = fetch_neo(api_key)
    if neo_data:
        neo_text.delete(1.0, tk.END)
        neo_text.insert(tk.END, neo_data)

# Check if the API keys were loaded correctly
if not apod_api_key or not neo_api_key:
    raise ValueError("API keys not found. Please check your .env file.")

# Example of loading both keys
print(f"Loaded APOD API key: {apod_api_key[:4]}...")
print(f"Loaded NEO API key: {neo_api_key[:4]}...")

# Run the GUI
create_gui()