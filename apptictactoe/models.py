from django.db import models

from apptictactoe.tictactoe.board import Board
from apptictactoe.tictactoe.game import Game
from apptictactoe.tictactoe.player import Player


# Create your models here.
class Player_Model(models.Model):
    symbol = models.CharField(max_length=1)


class Board_Model(models.Model):
    positions = models.CharField(max_length=9)


class Game_Model(models.Model):
    player_1 = models.ForeignKey(
        Player_Model, on_delete=models.CASCADE, related_name="player_1"
    )
    player_2 = models.ForeignKey(
        Player_Model, on_delete=models.CASCADE, related_name="player_2"
    )
    current_player = models.ForeignKey(
        Player_Model, on_delete=models.CASCADE, related_name="current_player"
    )
    board = models.ForeignKey(Board_Model, on_delete=models.CASCADE)

    def get_game(self) -> Game:
        """Creates a Game object initialized with the values
            stored in the database

        Returns:
            Game: A Game object created from the values in the
             database
        """

        board_model = getattr(self, "board")

        current_player_model = getattr(self, "current_player")
        current_player_symbol: str = getattr(current_player_model, "symbol")
        current_player = Player(current_player_symbol, current_player_model.id)

        player_1_model = getattr(self, "player_1")
        player_1_model_symbol: str = getattr(player_1_model, "symbol")
        player_1 = Player(player_1_model_symbol, player_1_model.id)

        player_2_model = getattr(self, "player_2")
        player_2_model_symbol: str = getattr(player_2_model, "symbol")
        player_2 = Player(player_2_model_symbol, player_2_model.id)

        board_model: Board_Model = getattr(self, "board")
        positions: str = getattr(board_model, "positions")
        game_board: Board = Board(positions)

        game = Game(
            board=game_board,
            players=[player_1, player_2],
            current_player=current_player,
        )
        return game

    def save_from_game(self, game: Game) -> None:
        """Updates the game model to match the values
            from the game parameter.

        Args:
            game (Game): Update the database to use the values from
             this game
        """
        self.current_player = Player_Model.objects.get(pk=game.current_player.id)
        self.board = Board_Model(
            positions=game.board.to_string(include_new_lines=False)
        )
        self.board.save()
        self.save()

    def get_other_player_id(self, my_player_id: int) -> int:
        """Gets id of other player in the game

        Args:
            my_player_id (int): _description_

        Raises:
            RuntimeWarning: when other player's id is not found

        Returns:
            int: id of other player
        """
        for player in [self.player_1, self.player_2]:
            if player.id != my_player_id:
                return player.id
        raise RuntimeWarning("Could not find id for other player")