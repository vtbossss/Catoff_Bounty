from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_search_view, name='player_search'),
    path('player-stats/', views.player_stats_view, name='player_stats'),
]
