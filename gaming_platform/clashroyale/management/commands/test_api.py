# clashroyale/management/commands/test_api.py

from django.core.management.base import BaseCommand
from clashroyale.services.api_client import make_request

class Command(BaseCommand):
    help = "Test Clash Royale API connectivity"

    def handle(self, *args, **kwargs):
        endpoint = "/cards"
        response = make_request(endpoint)

        if "error" in response:
            self.stdout.write(self.style.ERROR(f"Error: {response['error']}"))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully fetched cards:"))
            for card in response.get("items", []):
                self.stdout.write(f"- {card['name']}")
