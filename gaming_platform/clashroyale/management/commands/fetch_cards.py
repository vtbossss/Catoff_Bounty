# clashroyale/management/commands/fetch_cards.py

from django.core.management.base import BaseCommand
from clashroyale.services.api_client import make_request
from clashroyale.models import Card

class Command(BaseCommand):
    help = "Fetch and store Clash Royale card data"

    def handle(self, *args, **kwargs):
        endpoint = "/cards"
        response = make_request(endpoint)

        if "error" in response:
            self.stdout.write(self.style.ERROR(f"Error: {response['error']}"))
        else:
            cards = response.get("items", [])
            for card in cards:
                Card.objects.update_or_create(
                    id=card["id"],
                    defaults={
                        "name": card["name"],
                        "max_level": card["maxLevel"],
                        "icon_url": card["iconUrls"]["medium"],
                        "rarity": card["rarity"],
                        "card_type": card["type"],
                        "description": card["description"],
                    },
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully stored {len(cards)} cards."))
