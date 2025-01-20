from django.core.management.base import BaseCommand
from clashroyale.services.api_client import make_request
from clashroyale.models import Player, Clan, Challenge, BattleLog, GameMode, Prize
from clashroyale.services.verification import TrophyVerification, ChallengeVerification, WinLossVerification
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
                player, created = Player.objects.update_or_create(
                    tag=players_data["tag"],
                    defaults={
                        "name": players_data["name"],
                        "level": players_data["expLevel"],
                        "trophies": players_data["trophies"],
                    },
                )

                # Generate and log Trophy Proof
                trophy_proof = TrophyVerification.generate_trophy_proof(player_tag, threshold=4000)
                self.stdout.write(self.style.SUCCESS(f"Trophy proof for {player_tag}: {trophy_proof}"))
                
                # Generate and log Win-Loss Proof
                win_loss_proof = WinLossVerification.generate_win_loss_proof(player_tag, threshold=60.0)
                self.stdout.write(self.style.SUCCESS(f"Win/Loss proof for {player_tag}: {win_loss_proof}"))
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


            # 4. Fetch and store data for Challenges
            challenges_data = make_request("/challenges")
            self.stdout.write(f"Challenges Data: {challenges_data}")

            if not isinstance(challenges_data, list):
                self.stdout.write(self.style.WARNING("Challenges data is not in the expected format."))
                challenges_data = []

            for challenge_set in challenges_data:
                challenges = challenge_set.get("challenges", [])
                for challenge in challenges:
                    try:
                        # Process game mode
                        game_mode_data = challenge.get("gameMode", {})
                        game_mode, _ = GameMode.objects.get_or_create(
                            id=game_mode_data.get("id"),
                            defaults={"name": game_mode_data.get("name", "Unknown")},
                        )

                        # Process challenge
                        challenge_obj, created = Challenge.objects.update_or_create(
                            id=challenge["id"],  # Use 'id' instead of 'challenge_id'
                            defaults={
                                "name": challenge["name"],
                                "description": challenge.get("description", ""),
                                "win_mode": challenge.get("winMode", ""),
                                "casual": challenge.get("casual", False),
                                "max_losses": challenge.get("maxLosses", 0),
                                "max_wins": challenge.get("maxWins", 0),
                                "icon_url": challenge.get("iconUrl", ""),
                                "game_mode": game_mode,
                            },
                        )

                        # Process prizes
                        challenge_obj.prizes.all().delete()  # Clear old prizes to avoid duplicates
                        for prize in challenge.get("prizes", []):
                            Prize.objects.create(
                                challenge=challenge_obj,
                                type=prize.get("type"),
                                amount=prize.get("amount"),
                                consumable_name=prize.get("consumableName"),
                            )

                        action = "Created" if created else "Updated"
                        self.stdout.write(self.style.SUCCESS(f"{action} challenge: {challenge['name']}"))

                        # Generate and log Challenge Proof
                        challenge_proof = ChallengeVerification.generate_challenge_proof(player_tag, challenge["id"])
                        self.stdout.write(self.style.SUCCESS(f"Challenge proof for {player_tag} in challenge {challenge['name']}: {challenge_proof}"))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing challenge: {str(e)}"))

            # 5. Fetch and store data for Battle Logs
            battle_log_data = make_request(f"/players/{encoded_player_tag}/battlelog")
            self.stdout.write(f"Battle Log Data: {battle_log_data}")

            if isinstance(battle_log_data, list) and battle_log_data:
                for battle in battle_log_data[:50]:  # Limiting to the top 50 battles
                    # Extract necessary fields from the battle data
                    battle_type = battle.get("type", "Unknown")
                    battle_time = battle.get("battleTime", "")
                    arena_name = battle.get("arena", {}).get("name", "Unknown Arena")
                    game_mode_name = battle.get("gameMode", {}).get("name", "Unknown Mode")
                    team = battle.get("team", [])
                    
                    # Process the team data (assuming the team has only one player, the current player)
                    if team:
                        player_data = team[0]  # The first team member (your player)
                        player_tag = player_data.get("tag", "")
                        player_name = player_data.get("name", "Unknown")
                        trophy_change = player_data.get("trophyChange", 0)
                        crowns = player_data.get("crowns", 0)
                        king_tower_hp = player_data.get("kingTowerHitPoints", 0)
                        princess_tower_hp = player_data.get("princessTowersHitPoints", [0, 0])

                        # Create or update the BattleLog entry in the database
                        BattleLog.objects.update_or_create(
                            battle_id=battle_time,  # Use the battle time as a unique identifier
                            defaults={
                                "type": battle_type,
                                "timestamp": battle_time,
                                "arena": arena_name,
                                "game_mode": game_mode_name,
                                "player_tag": player_tag,
                                "player_name": player_name,
                                "starting_trophies": player_data.get("startingTrophies", 0),
                                "trophy_change": trophy_change,
                                "crowns": crowns,
                                "king_tower_hp": king_tower_hp,
                                "princess_tower_hp": princess_tower_hp,
                            },
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f"No team data for battle: {battle_time}"))
            else:
                self.stdout.write(self.style.WARNING("No valid battle log data found."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Data fetching and storage completed successfully."))
