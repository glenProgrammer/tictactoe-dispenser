from .board import Board, row_and_column_to_key, EMPTY
from .player import Player


class Game:
    def __init__(
        self, board: Board, players: list[Player], current_player: Player
    ) -> None:
        """Constructor for Game.  If any arguments are omitted,
           an empty board will be generated and new players will be created

        Args:
            board (Board): The board the game will use
            players (list[Player]): List of 2 players who will play
            current_player (Player): The player whose turn it is
        """
        if board is None or players is None or current_player is None:
            self.board = Board(None)
            self.players = [Player("x", None), Player("o", None)]
            self.current_player = self.get_who_plays_first()
        else:
            self.board = board
            self.players = players
            self.current_player = current_player

    def _get_my_mark(self, player_id: int) -> str:
        for player in self.players:
            if player.id == player_id:
                return player.mark
        raise RuntimeWarning(f"Couldn't find mark for player with id {player_id}")

    def get_status(self, player_id: int) -> str:
        """Get status of player, i.e. if it's the player's turn,
           if the player won the game, etc.

        Args:
            player_id (int): Id of player whose status should be found

        Returns:
            str: A string that describes the player's status
        """
        # TODO: would this be more elegant with a switch statement?
        did_someone_win, winning_mark = self.detect_victory()
        if did_someone_win:
            my_mark = self._get_my_mark(player_id)
            if my_mark == winning_mark:
                return "You won the game!"
            else:
                return "You lost."
        if self.detect_stalemate():
            return "Stalemate"
        if self.current_player.id == int(player_id):
            return "It is your turn"
        return "Waiting for other player..."

    def play_turn(self, row: int, col: int) -> bool:
        print(self.current_player.mark + " turn.")
        print(row, col)
        row, col = (
            (row, col)
            if row is not None and col is not None
            else self.current_player.get_move()
        )
        print(row, col)
        is_valid, reason_not_valid = self.board.is_position_valid(row, col)
        if not is_valid:
            print(reason_not_valid)
            return
        if not self.board.is_free(row, col):
            print("That position is not free.")
            return
        self.board.place(row, col, self.current_player.mark)
        self.current_player = self.get_current_player()

    def get_current_player(self) -> Player:
        """Gets the player whose turn it is

        Returns:
            Player: Player whose turn it is
        """
        if self.players[0].id == self.current_player.id:
            return self.players[1]
        else:
            return self.players[0]

    def get_who_plays_first(self) -> Player:
        """Determines which player will mark first

        Returns:
            Player: The player who will mark first
        """
        return self.players[0]

    def is_game_over(self) -> bool:
        did_someone_win, _ = self.detect_victory()
        return did_someone_win or self.detect_stalemate()

    def display_board(self) -> None:
        print(self.board)

    def detect_stalemate(self) -> bool:
        paths_to_victory = self._get_paths_to_victory()
        for path_to_victory in paths_to_victory:
            marks = set()
            for position in path_to_victory:
                marks.add(self.board.positions.get(position))
            marks.discard(EMPTY)
            if len(marks) < 2:
                return False
        return True

    def _get_paths_to_victory(_) -> list[list[tuple[int, int]]]:
        paths_to_victory = []

        # row victories
        for row in range(0, 3):
            victory_path = []
            for col in range(0, 3):
                victory_path.append(row_and_column_to_key(row, col))
            paths_to_victory.append(victory_path)

        # column victories
        for col in range(0, 3):
            victory_path = []
            for row in range(0, 3):
                victory_path.append(row_and_column_to_key(row, col))
            paths_to_victory.append(victory_path)

        # diagonal victories
        victory_path = []
        for row, col in [(0, 0), (1, 1), (2, 2)]:
            victory_path.append(row_and_column_to_key(row, col))
        paths_to_victory.append(victory_path)
        victory_path = []
        for row, col in [(2, 0), (1, 1), (0, 2)]:
            victory_path.append(row_and_column_to_key(row, col))
        paths_to_victory.append(victory_path)

        return paths_to_victory

    def detect_victory(self) -> tuple[bool, Player]:
        paths_to_victory = self._get_paths_to_victory()

        for path_to_victory in paths_to_victory:
            first_value = self.board.positions.get(path_to_victory[0])
            if first_value != EMPTY:
                if all(
                    self.board.positions.get(position) == first_value
                    for position in path_to_victory[1::]
                ):
                    return True, first_value
        return False, None


# Sanity test
if __name__ == "__main__":
    tictactoe = Game(None, None, None)
    while not tictactoe.is_game_over():
        tictactoe.display_board()
        tictactoe.play_turn(None, None)
