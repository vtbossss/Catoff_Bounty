# clashroyale/services/config.py
from django.conf import settings
API_BASE_URL = "https://api.clashroyale.com/v1"
API_TOKEN = settings.CLASH_ROYALE_API_TOKEN

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json",
}
