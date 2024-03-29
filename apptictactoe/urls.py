from . import views

from django.urls import path


urlpatterns = [
    path("", views.index, name="index"),
    path(
        "make_move/<game_id>/<my_player_id>/<target_move_position>",
        views.make_move,
        name="tictactoe-make-move",
    ),
    path("join_game/<game_id>/<my_player_id>/", views.join_game, name="tictactoe-join-game"),
    path(
        "get_updates/<game_id>/<my_player_id>/", views.get_updates, name="tictactoe-get-updates"
    ),
    path("reset/<game_id>/", views.reset, name="tictactoe-reset")
]
