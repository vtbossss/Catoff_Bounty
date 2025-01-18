# clashroyale/services/api_client.py

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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
