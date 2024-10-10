## Setup Instructions

1. Clone the repository: `git clone https://github.com/your_username/NasaApp.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root of the project and add your API key:
    ```
    API_KEY=your_api_key_here
    ```
4. Run the application: `python app.py`
   
## Issues Encountered
1. issue with requests, had to install requests. 
2. **Issue**: Error 403 (Forbidden) when fetching APOD data.
   - **Description**: The APOD API returned a 403 error, indicating that the request was not authorized.
   - **Cause**: This error usually occurs when:
     1. The API key is missing or invalid.
     2. The API request exceeds the rate limit (too many requests in a short period).
     3. The API is being accessed from an unsupported location or network.
   - **Solution**: Investigate whether the API key is correctly loaded and valid, and ensure that the request is within the API's rate limits.
    - **Solved**: Issue was an invalid API key, simply generated a new key.
3. **Issue**: main displays information before any user request.
    -**Cause**: Unsure, maybe menu logic
    
   
