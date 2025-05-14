from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/toggle_public/', views.toggle_public, name='toggle_public'),
    path('<int:game_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search_games, name='search_games'),
] 