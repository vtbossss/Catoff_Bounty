from django.db import models

# Documentation: The Player model stores information about Clash Royale players.
class Player(models.Model):
    tag = models.CharField(max_length=50, unique=True)  # Unique identifier for the player
    name = models.CharField(max_length=100)  # Player's in-game name
    level = models.PositiveIntegerField()  # Player's experience level
    trophies = models.PositiveIntegerField()  # Number of trophies the player has

    def __str__(self):
        return f"{self.name} ({self.tag})"

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"


# Documentation: The Clan model stores details about in-game clans, which players can join.
class Clan(models.Model):
    tag = models.CharField(max_length=50, unique=True)  # Unique identifier for the clan
    name = models.CharField(max_length=100)  # Clan's name
    description = models.TextField(blank=True, null=True)  # Clan's description
    badge_id = models.PositiveIntegerField()  # Badge ID associated with the clan
    clan_score = models.PositiveIntegerField()  # Clan's score
    members_count = models.PositiveIntegerField()  # Number of members in the clan

    def __str__(self):
        return f"{self.name} ({self.tag})"

    class Meta:
        verbose_name = "Clan"
        verbose_name_plural = "Clans"


# Documentation: The Leaderboard model stores ranking information for players or clans.
class Leaderboard(models.Model):
    tag = models.CharField(max_length=50, unique=True)  # Unique identifier for the leaderboard entry
    name = models.CharField(max_length=100)  # Name of the player or clan in the leaderboard
    clan_score = models.PositiveIntegerField(blank=True, null=True)  # Clan score (if applicable)
    rank = models.PositiveIntegerField()  # Current rank in the leaderboard

    def __str__(self):
        return f"Leaderboard Entry: {self.name} (Rank: {self.rank})"

    class Meta:
        verbose_name = "Leaderboard"
        verbose_name_plural = "Leaderboards"


# Documentation: The Challenge model stores information about in-game challenges.
class Challenge(models.Model):
    challenge_id = models.CharField(max_length=50, unique=True)  # Unique identifier for the challenge
    name = models.CharField(max_length=100)  # Title of the challenge
    max_wins = models.PositiveIntegerField()  # Maximum wins in the challenge
    reward = models.CharField(max_length=100, blank=True, null=True)  # Reward details (if any)

    def __str__(self):
        return f"Challenge: {self.name} ({self.max_wins} Max Wins)"

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"


# Documentation: The BattleLog model stores details of a player's battle history.
class BattleLog(models.Model):
    battle_id = models.CharField(max_length=50, unique=True)  # Unique identifier for the battle
    type = models.CharField(max_length=50)  # Type of battle (e.g., 1v1, 2v2)
    timestamp = models.DateTimeField()  # Timestamp of the battle
    opponent_name = models.CharField(max_length=100)  # Opponent's name in the battle

    def __str__(self):
        return f"Battle: {self.type} vs {self.opponent_name} on {self.timestamp}"

    class Meta:
        verbose_name = "Battle Log"
        verbose_name_plural = "Battle Logs"


# Documentation: The ClanWar model stores information about clan wars.
class ClanWar(models.Model):
    war_id = models.CharField(max_length=50, unique=True)  # Unique identifier for the clan war
    status = models.CharField(max_length=50)  # Status of the war (e.g., "ongoing", "completed")
    battle_count = models.PositiveIntegerField()  # Total battles in the clan war
    wins = models.PositiveIntegerField()  # Number of wins in the clan war

    def __str__(self):
        return f"Clan War: {self.status} (Battles: {self.battle_count}, Wins: {self.wins})"

    class Meta:
        verbose_name = "Clan War"
        verbose_name_plural = "Clan Wars"
