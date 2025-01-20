from django.db import models


# Documentation: The GameMode model stores details about different game modes in Clash Royale.
class GameMode(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)  # Game mode ID
    name = models.CharField(max_length=100)  # Game mode name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Game Mode"
        verbose_name_plural = "Game Modes"


# Documentation: The Prize model stores information about prizes for a specific challenge.
class Prize(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True)  # Prize type (e.g., "consumable")
    amount = models.PositiveIntegerField(blank=True, null=True)  # Prize amount
    consumable_name = models.CharField(max_length=100, blank=True, null=True)  # Name of the consumable prize
    challenge = models.ForeignKey(
        "Challenge", on_delete=models.CASCADE, related_name="prizes"
    )  # Associated challenge

    def __str__(self):
        if self.type and self.amount:
            return f"{self.amount}x {self.consumable_name or self.type}"
        return "No Prize"

    class Meta:
        verbose_name = "Prize"
        verbose_name_plural = "Prizes"


# Documentation: The Challenge model stores information about in-game challenges.
class Challenge(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)  # Unique challenge ID
    name = models.CharField(max_length=100)  # Challenge name
    description = models.TextField(blank=True, null=True)  # Challenge description
    start_time = models.DateTimeField(null=True, blank=True)  # Start time of the challenge
    end_time = models.DateTimeField(null=True, blank=True)  # End time of the challenge
    win_mode = models.CharField(max_length=50, blank=True, null=True)  # Win condition
    casual = models.BooleanField(default=False)  # Whether the challenge is casual
    max_losses = models.PositiveIntegerField()  # Maximum allowed losses
    max_wins = models.PositiveIntegerField()  # Maximum allowed wins
    game_mode = models.ForeignKey(
        GameMode, on_delete=models.SET_NULL, null=True, related_name="challenges"
    )  # Associated game mode
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_challenges"
    )  # Nested challenges (if any)
    icon_url = models.URLField(blank=True, null=True)  # URL for the challenge icon

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
        ordering = ["-start_time"]


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


# Documentation: The BattleLog model stores details of a player's battle history.
class BattleLog(models.Model):
    battle_id = models.CharField(max_length=255, unique=True)  # Unique battle ID
    type = models.CharField(max_length=50)  # Type of battle
    timestamp = models.DateTimeField()  # Timestamp of the battle
    arena = models.CharField(max_length=100, default="Unknown Arena")  # Arena where the battle took place
    game_mode = models.CharField(max_length=100, default="Unknown Mode")  # Game mode used in the battle
    player_tag = models.CharField(max_length=255)  # Player's tag
    player_name = models.CharField(max_length=255)  # Player's name
    starting_trophies = models.IntegerField(default=0)  # Starting trophies before the battle
    trophy_change = models.IntegerField(default=0)  # Change in trophies after the battle
    crowns = models.IntegerField(default=0)  # Number of crowns earned
    king_tower_hp = models.IntegerField(default=0)  # King's tower remaining HP
    princess_tower_hp = models.JSONField(null=True, blank=True)  # HP of princess towers (as a list)

    def __str__(self):
        return f"{self.player_name} battle log at {self.timestamp}"


