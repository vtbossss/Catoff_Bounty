# clashroyale/serializers.py

from rest_framework import serializers

from .models import Card,Clan, Player, Tournament, Location, Challenge, Leaderboard

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"



class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = "__all__"

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = "__all__"