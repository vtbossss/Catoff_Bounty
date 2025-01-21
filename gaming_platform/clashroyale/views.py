from django.shortcuts import render
from django.http import HttpResponse
import urllib.parse
from .services.api_client import make_request
from .services.verification import TrophyVerification, WinLossVerification, ChallengeVerification
from clashroyale.models import Player, Clan, Challenge, BattleLog, GameMode
import logging

# Set up logger for debugging and information purposes
logger = logging.getLogger(__name__)

def player_search_view(request):
    """
    Renders the player search form where the user can enter a player tag.
    """
    return render(request, "player_search.html")


def validate_player_tag(player_tag):
    """
    Validates the player tag format. A valid player tag should start with # and be between 8 to 12 characters long.
    """
    if not player_tag.startswith("#"):
        return False, "Player tag must start with #."
    if not (8 <= len(player_tag) <= 12):
        return False, "Player tag must be between 8 and 12 characters."
    if not player_tag[1:].isalnum():  # Check if the tag after "#" is alphanumeric
        return False, "Player tag can only contain alphanumeric characters."
    return True, None


def player_stats_view(request):
    """
    Fetches and displays player stats, challenges, battle logs, 
    and generates Zero-Knowledge Proofs based on the player's tag.
    """
    # Get the player tag from the request
    player_tag = request.GET.get("player_tag", "").strip()  # Ensure player_tag is stripped of whitespace
    if not player_tag:
        return render(request, "player_search.html", {"error": "Player tag is required!"})

    # Validate the player tag format
    is_valid, error_message = validate_player_tag(player_tag)
    if not is_valid:
        return render(request, "player_search.html", {"error": error_message})

    # URL-encode the player tag to ensure compatibility with API requirements
    encoded_player_tag = urllib.parse.quote(player_tag)

    try:
        # 1. Fetch and store player data
        player_data = make_request(f"/players/{encoded_player_tag}")
        if not player_data:
            logger.warning(f"Player data not found for tag: {player_tag}")
            return render(request, "player_search.html", {"error": "Player not found! Please check the tag."})

        # Store player data in the database (similar to the command)
        player, created = Player.objects.update_or_create(
            tag=player_data["tag"],
            defaults={
                "name": player_data["name"],
                "level": player_data["expLevel"],
                "trophies": player_data["trophies"],
            },
        )

        # Generate Zero-Knowledge Proofs for the player
        proofs = {
            "trophy_proof": TrophyVerification.generate_trophy_proof(player_tag, threshold=4000),
            "win_loss_proof": WinLossVerification.generate_win_loss_proof(player_tag, threshold=60.0),
        }
        logger.info(f"Generated proofs: {proofs}")

        # 2. Fetch and store clan data if the player is part of a clan
        clan_tag = player_data.get("clan", {}).get("tag")
        clan_data = None
        if clan_tag:
            encoded_clan_tag = urllib.parse.quote(clan_tag)
            clan_data = make_request(f"/clans/{encoded_clan_tag}")
            if clan_data:
                Clan.objects.update_or_create(
                    tag=clan_data["tag"],
                    defaults={
                        "name": clan_data["name"],
                        "description": clan_data.get("description", ""),
                        "badge_id": clan_data["badgeId"],
                        "clan_score": clan_data["clanScore"],
                        "members_count": clan_data["members"],
                    },
                )
                logger.info(f"Clan data stored successfully for clan tag: {clan_tag}")
            else:
                logger.warning(f"No clan data found for clan tag: {clan_tag}")

        # 3. Fetch and process challenges
        challenges_data = make_request("/challenges")
        challenge_proofs = []
        if challenges_data:
            for challenge_set in challenges_data:
                challenges = challenge_set.get("challenges", [])
                for challenge in challenges:
                    # Process and store challenge data
                    game_mode_data = challenge.get("gameMode", {})
                    game_mode, _ = GameMode.objects.get_or_create(
                        id=game_mode_data.get("id"),
                        defaults={"name": game_mode_data.get("name", "Unknown")},
                    )

                    challenge_obj, created = Challenge.objects.update_or_create(
                        id=challenge["id"],
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
                    # Generate ZKP for challenges
                    challenge_proof = ChallengeVerification.generate_challenge_proof(player_tag, challenge["id"])
                    challenge_proofs.append({
                        "challenge_id": challenge["id"],
                        "proof": challenge_proof,
                    })
                    logger.info(f"Challenge proof for {player_tag}: {challenge_proof}")

        # 4. Fetch and store battle log data
        battle_log_data = make_request(f"/players/{encoded_player_tag}/battlelog")
        if isinstance(battle_log_data, list) and battle_log_data:
            for battle in battle_log_data[:50]:  # Limit to top 50 battles
                battle_type = battle.get("type", "Unknown")
                battle_time = battle.get("battleTime", "")
                arena_name = battle.get("arena", {}).get("name", "Unknown Arena")
                game_mode_name = battle.get("gameMode", {}).get("name", "Unknown Mode")
                team = battle.get("team", [])

                if team:
                    player_data = team[0]  # First team member (current player)
                    BattleLog.objects.update_or_create(
                        battle_id=battle_time,
                        defaults={
                            "type": battle_type,
                            "timestamp": battle_time,
                            "arena": arena_name,
                            "game_mode": game_mode_name,
                            "player_tag": player_data.get("tag", ""),
                            "player_name": player_data.get("name", "Unknown"),
                            "starting_trophies": player_data.get("startingTrophies", 0),
                            "trophy_change": player_data.get("trophyChange", 0),
                            "crowns": player_data.get("crowns", 0),
                            "king_tower_hp": player_data.get("kingTowerHitPoints", 0),
                            "princess_tower_hp": player_data.get("princessTowersHitPoints", [0, 0]),
                        },
                    )
            logger.info("Battle logs processed successfully.")

        # Render the player stats template with fetched data and proofs
        return render(request, "player_stats.html", {
            "player": player_data,
            "clan": clan_data,  # Add clan data to context
            "proofs": proofs,
            "challenges": challenge_proofs,
            "battles": battle_log_data[:10],  # Display only top 10 battles
        })

    except Exception as e:
        # Handle any errors during the process
        logger.error(f"Error occurred while fetching data: {str(e)}")
        return render(request, "player_search.html", {"error": f"An error occurred: {str(e)}"})
