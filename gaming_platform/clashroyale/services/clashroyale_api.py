import requests
from django.conf import settings

class ClashRoyaleAPI:
    BASE_URL = "https://api.clashroyale.com/v1"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.CLASH_ROYALE_API_TOKEN}"
        }

    def fetch_clan_info(self, clan_tag):
        url = f"{self.BASE_URL}/clans/{clan_tag}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching clan info: {response.text}")
        return response.json()
