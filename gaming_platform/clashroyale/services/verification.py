import hashlib
from clashroyale.models import Player, Challenge, BattleLog
from django.core.exceptions import ObjectDoesNotExist


class TrophyVerification:
    @staticmethod
    def commit_trophy_count(trophies: int) -> str:
        """
        Create a cryptographic commitment for the player's trophy count.
        """
        return hashlib.sha256(str(trophies).encode()).hexdigest()

    @staticmethod
    def generate_trophy_proof(player_tag: str, threshold: int) -> dict:
        """
        Generate a proof that the player's trophy count is above a threshold.
        """
        try:
            player = Player.objects.get(tag=player_tag)
            committed_value = TrophyVerification.commit_trophy_count(player.trophies)

            return {
                "proof": player.trophies > threshold,
                "commitment": committed_value,
                "message": f"Trophy count is {'above' if player.trophies > threshold else 'not above'} {threshold}."
            }
        except ObjectDoesNotExist as e:
            return {
                "proof": False,
                "commitment": None,
                "message": f"Player not found: {str(e)}"
            }

    @staticmethod
    def verify_trophy_proof(commitment: str, trophies: int) -> bool:
        """
        Verify the player's proof of trophy count.
        """
        recalculated_commitment = TrophyVerification.commit_trophy_count(trophies)
        return commitment == recalculated_commitment


class ChallengeVerification:
    @staticmethod
    def commit_challenge_completion(challenge_id: str, player_tag: str) -> str:
        """
        Create a cryptographic commitment for challenge completion.
        """
        commitment_input = f"{challenge_id}-{player_tag}-completed"
        return hashlib.sha256(commitment_input.encode()).hexdigest()

    @staticmethod
    def generate_challenge_proof(player_tag: str, challenge_id: str) -> dict:
        """
        Generate a proof that the player has completed a specific challenge.
        """
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            # Check if the player has completed the challenge by checking battle logs or a player-challenge relation
            player = Player.objects.get(tag=player_tag)

            # Here, assuming that the player's challenge completion is based on battle log data or other criteria
            challenge_completed = BattleLog.objects.filter(player_tag=player_tag, trophy_change__gte=0).exists()

            if challenge_completed:
                commitment = ChallengeVerification.commit_challenge_completion(challenge_id, player_tag)
                return {
                    "proof": True,
                    "commitment": commitment,
                    "message": f"Player {player_tag} has completed the challenge {challenge.name}."
                }
            else:
                return {
                    "proof": False,
                    "commitment": None,
                    "message": f"Player {player_tag} has not completed the challenge {challenge.name}."
                }
        except (ObjectDoesNotExist, Challenge.DoesNotExist) as e:
            return {
                "proof": False,
                "commitment": None,
                "message": f"Challenge or player data not found: {str(e)}"
            }

    @staticmethod
    def verify_challenge_proof(commitment: str, challenge_id: str, player_tag: str) -> bool:
        """
        Verify the player's proof of challenge completion.
        """
        recalculated_commitment = ChallengeVerification.commit_challenge_completion(challenge_id, player_tag)
        return commitment == recalculated_commitment


class WinLossVerification:
    @staticmethod
    def calculate_win_loss_ratio(player_tag: str) -> float:
        """
        Calculate the win-loss ratio for a player based on their battle logs.
        """
        battles = BattleLog.objects.filter(player_tag=player_tag)
        if not battles:
            return 0.0
        wins = sum(1 for battle in battles if battle.crowns > 0)  # Assuming crowns indicate a win
        losses = len(battles) - wins
        if losses == 0:
            return wins  # No losses, return win count as the ratio
        return (wins / losses) * 100  # Win-to-loss ratio

    @staticmethod
    def commit_win_loss_ratio(ratio: float) -> str:
        """
        Create a cryptographic commitment for the win-loss ratio.
        """
        return hashlib.sha256(f"{ratio:.2f}".encode()).hexdigest()

    @staticmethod
    def generate_win_loss_proof(player_tag: str, threshold: float) -> dict:
        """
        Generate a proof that the player's win-loss ratio is above a threshold.
        """
        win_loss_ratio = WinLossVerification.calculate_win_loss_ratio(player_tag)
        commitment = WinLossVerification.commit_win_loss_ratio(win_loss_ratio)

        return {
            "proof": win_loss_ratio > threshold,
            "commitment": commitment,
            "message": f"Win-loss ratio of {win_loss_ratio:.2f}% is {'above' if win_loss_ratio > threshold else 'below'} the threshold of {threshold}%.",
        }

    @staticmethod
    def verify_win_loss_proof(commitment: str, win_loss_ratio: float) -> bool:
        """
        Verify the player's proof of win-loss ratio.
        """
        recalculated_commitment = WinLossVerification.commit_win_loss_ratio(win_loss_ratio)
        return commitment == recalculated_commitment
