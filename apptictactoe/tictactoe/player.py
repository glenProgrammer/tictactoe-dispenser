import uuid


class Player:
    def __init__(self, mark, player_id) -> None:
        if player_id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = player_id
        self.mark = mark

    def get_move(self) -> tuple[int, int]:
        row = input("Choose row:")
        col = input("Choose column:")
        # TODO: validate
        return int(row), int(col)
