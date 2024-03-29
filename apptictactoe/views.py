from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from apptictactoe.models import Board_Model, Game_Model, Player_Model

from apptictactoe.tictactoe import board
from apptictactoe.tictactoe.board import Board

STARTING_POSITIONS = "---------"


def index(request):
    board_model = Board_Model(positions=STARTING_POSITIONS)
    board_model.save()
    player_1_model = Player_Model(symbol="x")
    player_1_model.save()
    player_2_model = Player_Model(symbol="o")
    player_2_model.save()
    game_model = Game_Model(
        current_player=player_1_model,
        player_1=player_1_model,
        player_2=player_2_model,
        board=board_model,
    )
    game_model.save()
    return redirect(
        "tictactoe-join-game", game_id=game_model.id, my_player_id=player_1_model.id
    )


def make_move(request, game_id, my_player_id, target_move_position):
    if request.method == "POST":
        game_model = Game_Model.objects.get(pk=game_id)
        game = game_model.get_game()

        my_player_id = int(my_player_id)
        if game.current_player.id == my_player_id and not game.is_game_over():
            row, col = board.key_to_row_and_column(target_move_position)
            game.play_turn(row, col)
            game_model.save_from_game(game)

        response = {
            "tictactoe_positions": game.board.get(),
            "status": game.get_status(my_player_id),
        }
        return JsonResponse(response)


def join_game(request, game_id, my_player_id):
    print(f"{game_id=}")
    print(f"{my_player_id=}")
    my_player_id = int(my_player_id)
    game_model = Game_Model.objects.get(pk=game_id)
    game = game_model.get_game()
    my_player_model = Player_Model.objects.get(pk=my_player_id)
    # TODO: error handling and validation

    my_player_model_symbol: str = getattr(my_player_model, "symbol")
    other_player_id = game_model.get_other_player_id(my_player_id)

    context = {
        "symbol": my_player_model_symbol,
        "game_id": game_model.id,
        "my_player_id": my_player_model.id,
        "status": game.get_status(int(my_player_id)),
        "tictactoe_positions": game.board.get(),
        "link": request.build_absolute_uri(
            reverse(join_game, args=[game_id, other_player_id])
        ),
    }
    print(f"{game_id=}")
    return render(request, "index.html", context)


def get_updates(request, game_id, my_player_id):
    game_model = Game_Model.objects.get(pk=game_id)
    game = game_model.get_game()
    board_model = getattr(game_model, "board")
    tictactoe_board = Board(getattr(board_model, "positions"))

    response = {
        "tictactoe_positions": tictactoe_board.get(),
        "status": game.get_status(int(my_player_id)),
    }
    return JsonResponse(response)


def reset(request, game_id):
    game_model = Game_Model.objects.get(pk=game_id)
    board_model = getattr(game_model, "board")
    board_model.positions = STARTING_POSITIONS
    board_model.save()

    player_1_model = getattr(game_model, "player_1")
    game_model.current_player = player_1_model
    game_model.save()
