from django.db import models


# The GameMode model stores details about different game modes in Clash Royale.
class GameMode(models.Model):
    id = models.CharField(
        max_length=50, unique=True, primary_key=True, help_text="Unique identifier for the game mode"
    )
    name = models.CharField(max_length=100, help_text="Name of the game mode")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Game Mode"
        verbose_name_plural = "Game Modes"
        ordering = ["name"]


# The Prize model stores information about prizes for a specific challenge.
class Prize(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True, help_text="Type of prize (e.g., consumable)")
    amount = models.PositiveIntegerField(blank=True, null=True, help_text="Amount of the prize")
    consumable_name = models.CharField(
        max_length=100, blank=True, null=True, help_text="Name of the consumable prize"
    )
    challenge = models.ForeignKey(
        "Challenge",
        on_delete=models.CASCADE,
        related_name="prizes",
        help_text="Associated challenge for the prize",
    )

    def __str__(self):
        if self.type and self.amount:
            return f"{self.amount}x {self.consumable_name or self.type}"
        return "No Prize"

    class Meta:
        verbose_name = "Prize"
        verbose_name_plural = "Prizes"


# The Challenge model stores information about in-game challenges.
class Challenge(models.Model):
    id = models.CharField(
        max_length=50, unique=True, primary_key=True, help_text="Unique identifier for the challenge"
    )
    name = models.CharField(max_length=100, help_text="Name of the challenge")
    description = models.TextField(blank=True, null=True, help_text="Description of the challenge")
    start_time = models.DateTimeField(null=True, blank=True, help_text="Start time of the challenge")
    end_time = models.DateTimeField(null=True, blank=True, help_text="End time of the challenge")
    win_mode = models.CharField(max_length=50, blank=True, null=True, help_text="Win condition of the challenge")
    casual = models.BooleanField(default=False, help_text="Indicates if the challenge is casual")
    max_losses = models.PositiveIntegerField(help_text="Maximum losses allowed in the challenge")
    max_wins = models.PositiveIntegerField(help_text="Maximum wins allowed in the challenge")
    game_mode = models.ForeignKey(
        GameMode,
        on_delete=models.SET_NULL,
        null=True,
        related_name="challenges",
        help_text="Associated game mode for the challenge",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_challenges",
        help_text="Parent challenge if nested",
    )
    icon_url = models.URLField(blank=True, null=True, help_text="URL of the challenge icon")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
        ordering = ["-start_time"]


# The Player model stores information about Clash Royale players.
class Player(models.Model):
    tag = models.CharField(
        max_length=50, unique=True, db_index=True, help_text="Unique identifier for the player"
    )
    name = models.CharField(max_length=100, help_text="Player's in-game name")
    level = models.PositiveIntegerField(help_text="Player's experience level")
    trophies = models.PositiveIntegerField(help_text="Number of trophies the player has")

    def __str__(self):
        return f"{self.name} ({self.tag})"

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"


# The Clan model stores details about in-game clans, which players can join.
class Clan(models.Model):
    tag = models.CharField(
        max_length=50, unique=True, db_index=True, help_text="Unique identifier for the clan"
    )
    name = models.CharField(max_length=100, help_text="Name of the clan")
    description = models.TextField(blank=True, null=True, help_text="Description of the clan")
    badge_id = models.PositiveIntegerField(help_text="Badge ID associated with the clan")
    clan_score = models.PositiveIntegerField(help_text="Score of the clan")
    members_count = models.PositiveIntegerField(help_text="Number of members in the clan")

    def __str__(self):
        return f"{self.name} ({self.tag})"

    class Meta:
        verbose_name = "Clan"
        verbose_name_plural = "Clans"




# The BattleLog model stores details of a player's battle history.
class BattleLog(models.Model):
    battle_id = models.CharField(
        max_length=255, unique=True, db_index=True, help_text="Unique identifier for the battle"
    )
    type = models.CharField(max_length=50, help_text="Type of the battle")
    timestamp = models.DateTimeField(help_text="Timestamp of the battle")
    arena = models.CharField(
        max_length=100, default="Unknown Arena", help_text="Arena where the battle took place"
    )
    game_mode = models.CharField(
        max_length=100, default="Unknown Mode", help_text="Game mode used in the battle"
    )
    player_tag = models.CharField(
        max_length=255, db_index=True, help_text="Player's unique identifier (tag)"
    )
    player_name = models.CharField(max_length=255, help_text="Player's name in the battle")
    starting_trophies = models.IntegerField(default=0, help_text="Starting trophies before the battle")
    trophy_change = models.IntegerField(default=0, help_text="Change in trophies after the battle")
    crowns = models.IntegerField(default=0, help_text="Number of crowns earned")
    king_tower_hp = models.IntegerField(default=0, help_text="Remaining HP of the king's tower")
    princess_tower_hp = models.JSONField(
        null=True, blank=True, help_text="Remaining HP of the princess towers (as JSON)"
    )

    def __str__(self):
        return f"{self.player_name} battle log at {self.timestamp}"

    class Meta:
        verbose_name = "Battle Log"
        verbose_name_plural = "Battle Logs"
        ordering = ["-timestamp"]
