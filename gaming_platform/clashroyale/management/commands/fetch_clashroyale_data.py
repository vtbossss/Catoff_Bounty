from django.core.management.base import BaseCommand
from clashroyale.services.api_client import make_request
from clashroyale.models import Player, Clan, Leaderboard, Challenge, BattleLog, ClanWar
import urllib.parse

class Command(BaseCommand):
    help = "Fetch and store Clash Royale data for player stats, challenges, and real-time wagering"

    def add_arguments(self, parser):
        # Add player_tag argument to accept player tag as input
        parser.add_argument('player_tag', type=str, help="The player tag for which you want to fetch Clash Royale data")

    def handle(self, *args, **kwargs):
        # Retrieve the player_tag argument from the command
        player_tag = kwargs['player_tag']

        # URL-encode the player tag to ensure compatibility with API requirements
        encoded_player_tag = urllib.parse.quote(player_tag)
        
        # Helper function to process API responses
        def process_response(data, data_type):
            if isinstance(data, dict) and "items" in data:
                return data["items"]
            elif isinstance(data, dict):
                return [data]  # For endpoints that return a single object
            else:
                self.stdout.write(self.style.WARNING(f"No valid data found for {data_type}."))
                return []

        try:
            # 1. Fetch and store data for Players
            players_data = make_request(f"/players/{encoded_player_tag}")
            self.stdout.write(f"Players Data: {players_data}")
            if "tag" in players_data:
                Player.objects.update_or_create(
                    tag=players_data["tag"],
                    defaults={
                        "name": players_data["name"],
                        "level": players_data["expLevel"],
                        "trophies": players_data["trophies"],
                    },
                )
            else:
                self.stdout.write(self.style.WARNING("No player data found."))

            # 2. Fetch and store data for Clans (if player is in a clan)
            clan_tag = players_data.get("clan", {}).get("tag")
            if clan_tag:
                encoded_clan_tag = urllib.parse.quote(clan_tag)
                clans_data = make_request(f"/clans/{encoded_clan_tag}")
                self.stdout.write(f"Clans Data: {clans_data}")
                Clan.objects.update_or_create(
                    tag=clans_data["tag"],
                    defaults={
                        "name": clans_data["name"],
                        "description": clans_data.get("description", ""),
                        "badge_id": clans_data["badgeId"],
                        "clan_score": clans_data["clanScore"],
                        "members_count": clans_data["members"],
                    },
                )
            else:
                self.stdout.write(self.style.WARNING("Player is not part of a clan."))

            # 3. Fetch and store data for Leaderboards (replace location ID as required)
            leaderboard_data = make_request("/locations/global/rankings/players")
            self.stdout.write(f"Leaderboard Data: {leaderboard_data}")
            for leaderboard in process_response(leaderboard_data, "Leaderboards"):
                Leaderboard.objects.update_or_create(
                    leaderboard_id=leaderboard["tag"],
                    defaults={
                        "name": leaderboard["name"],
                        "clan_score": leaderboard.get("clanScore", 0),
                        "rank": leaderboard.get("rank", 0),
                    },
                )

            # 4. Fetch and store data for Challenges
            challenges_data = make_request("/challenges")
            self.stdout.write(f"Challenges Data: {challenges_data}")
            for challenge in process_response(challenges_data, "Challenges"):
                Challenge.objects.update_or_create(
                    challenge_id=challenge["id"],
                    defaults={
                        "name": challenge["title"],
                        "max_wins": challenge.get("maxWins", 0),
                        "reward": challenge.get("reward", ""),
                    },
                )

            # 5. Fetch and store data for Battle Logs
            battle_log_data = make_request(f"/players/{encoded_player_tag}/battlelog")
            self.stdout.write(f"Battle Log Data: {battle_log_data}")
            for battle in process_response(battle_log_data, "Battle Log"):
                BattleLog.objects.update_or_create(
                    battle_id=battle["battleTime"],
                    defaults={
                        "type": battle["type"],
                        "timestamp": battle["battleTime"],
                        "opponent_name": battle.get("opponent", {}).get("name", "Unknown"),
                    },
                )

            # 6. Fetch and store data for Clan War (if player is in a clan)
            if clan_tag:
                try:
                    clan_war_data = make_request(f"/clans/{encoded_clan_tag}/currentwar")
                    if "error" in clan_war_data and clan_war_data["error"] == "410":
                        self.stdout.write(self.style.WARNING("Clan is not currently in a war."))
                    else:
                        self.stdout.write(f"Clan War Data: {clan_war_data}")
                        ClanWar.objects.update_or_create(
                            war_id=clan_war_data["clan"]["tag"],
                            defaults={
                                "status": clan_war_data["state"],
                                "battle_count": clan_war_data.get("battlesPlayed", 0),
                                "wins": clan_war_data.get("wins", 0),
                            },
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error fetching Clan War data: {str(e)}"))
            else:
                self.stdout.write(self.style.WARNING("Clan war data cannot be fetched as player is not in a clan."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Data fetching and storage completed successfully."))
