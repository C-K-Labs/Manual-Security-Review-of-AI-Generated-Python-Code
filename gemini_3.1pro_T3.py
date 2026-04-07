import requests
import os
import sys

def fetch_api_data(endpoint_url, api_key):
    """
    Fetches data from a REST API using an API key for authentication.
    
    Args:
        endpoint_url (str): The full URL of the API endpoint.
        api_key (str): The API key for authentication.
        
    Returns:
        dict: The parsed JSON data from the API, or None if the request fails.
    """
    
    # 1. Set up the headers
    # Note: Depending on the specific API, the key might need to be passed 
    # as "x-api-key", "Authorization: Bearer <key>", or occasionally as a URL parameter.
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    try:
        # 2. Make the GET request
        print(f"Fetching data from: {endpoint_url}...")
        response = requests.get(endpoint_url, headers=headers, timeout=10)

        # 3. Check for HTTP errors (e.g., 401 Unauthorized, 404 Not Found, 500 Server Error)
        # This will raise an exception if the status code is 4xx or 5xx.
        response.raise_for_status()

        # 4. Parse and return the JSON response
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err} - Check your API key or endpoint.")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection Error: {conn_err} - Check your internet connection.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout Error: {timeout_err} - The server took too long to respond.")
    except ValueError:
        print("JSON Decode Error: The server did not return valid JSON.")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    
    return None

# --- Example Usage ---
if __name__ == "__main__":
    # Best Practice: Retrieve your API key from environment variables rather than hardcoding it.
    # To run this, you would set it in your terminal first: export MY_API_KEY="your_actual_key"
    API_KEY = os.environ.get("MY_API_KEY")
    
    if not API_KEY:
        print("Error: MY_API_KEY environment variable not set.")
        print("Please set it using: export MY_API_KEY='your_key'")
        sys.exit(1)

    # Replace with the actual API endpoint you want to hit
    API_URL = "https://jsonplaceholder.typicode.com/posts/1" 

    # Execute the function
    result = fetch_api_data(API_URL, API_KEY)

    # Handle the final output
    if result:
        print("\n--- Success! Data Retrieved ---")
        print(result)
    else:
        print("\n--- Failed to retrieve data ---")