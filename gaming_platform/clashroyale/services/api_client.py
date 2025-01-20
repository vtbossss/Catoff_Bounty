import requests
from .config import API_BASE_URL, HEADERS

def make_request(endpoint, params=None):
    """
    Make a request to the Clash Royale API.

    :param endpoint: API endpoint (e.g., "/players/{playerTag}").
    :param params: Query parameters for the request.
    :return: JSON response or error message.
    """
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        
        # Log the status code and response content for debugging purposes
        if not response.ok:
            print(f"Error {response.status_code}: {response.text}")
        
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        
        # Log the response headers to ensure it's JSON
        print(f"Response Headers: {response.headers}")
        
        # Attempt to parse the JSON response
        try:
            return response.json()
        except ValueError:
            print("Response is not in JSON format.")
            return {"error": "Response is not in JSON format."}
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}
