EMPTY = "-"


def row_and_column_to_key(row: int, column: int) -> str:
    """Convert string with row and column coordinates to string,
       i.e. row 0 and column 1 converts to '01'

    Args:
        row (int): _description_
        column (int): _description_

    Returns:
        str: _description_
    """
    return str(row) + str(column)


def key_to_row_and_column(key: str) -> tuple[int, int]:
    """Convert string with row and column coordinates to individual
       integers, i.e. '01' converts to row 0 and column 1

    Args:
        key (str): _description_

    Returns:
        tuple[int, int]: _description_
    """
    # TODO: error checking
    return int(key[0]), int(key[1])


class Board:
    def __init__(self, positions: str) -> None:
        """Constructor for Board class

        Args:
            positions str: Each character in the positions string
            represents the value of a position on the board.
            The first three characters represent the first row,
            the second three represent the second row,
            and the last three represent the bottom row.
            If positions is None, the board will initialize as blank.
        """
        self.width, self.height = 3, 3
        self.positions = {}

        if positions is not None and len(positions) > 0:
            row, col = 0, 0
            for position in positions:
                self.positions[row_and_column_to_key(row, col)] = position
                col = col + 1
                if col >= self.width:
                    col = 0
                    row = row + 1
        else:
            row, col = 0, 0
            for row in range(0, self.height):
                for col in range(0, self.width):
                    self.positions[row_and_column_to_key(row, col)] = EMPTY

    def is_position_valid(self, row: int, column: int) -> tuple[bool, str]:
        """Checks if position if on the board

        Args:
            row (int): The row of the position
            column (int): The column of the position

        Returns:
            tuple[bool, str]: Returns a tuple.  The first value in the tuple
             is a bool representing whether the position is valid or not.
             The second value contains a description of why the position is
             not valid.
        """
        problems = []
        if column < 0:
            problems.append("Column can not be less than zero.")
        if row < 0:
            problems.append("Row can not be less than zero.")
        if column >= self.width:
            problems.append(f"Column must be less than width ({self.width}).")
        if row >= self.height:
            problems.append(f"Row must be less than height ({self.height}).")
        if len(problems) > 0:
            return False, " ".join(problems)
        return True, None

    def is_free(self, row: int, column: int) -> bool:
        """Check if the position if available

        Args:
            row (int): Row of the position
            column (int): Column of the position

        Returns:
            bool: Whether or not the position is available
        """
        print(f"{self.positions[row_and_column_to_key(row, column)]=}")
        print(f"{row_and_column_to_key(row, column)=}")
        return self.positions[row_and_column_to_key(row, column)] == EMPTY

    def place(self, row: int, column: int, mark: str) -> None:
        """Places mark onto board

        Args:
            row (int): Row where mark should be placed
            column (int): Column where mark should be placed
            mark (str): The mark that should be placed, i.e. 'x'
        """
        self.positions[row_and_column_to_key(row, column)] = mark

    def get(self) -> dict[str, str]:
        """Getter for board's positions

        Returns:
            dict[str, str]: Dictionary of positions to values that represent the state
             of the board
        """
        return self.positions

    def to_string(self, include_new_lines: bool) -> str:
        """Returns a string representing the values on the board.

        Args:
            include_new_lines (bool): If true, newlines will be included after each row

        Returns:
            str: _description_
        """
        ret = ""
        for row in range(0, self.height):
            if row != 0 and include_new_lines:
                ret = ret + "\n"
            for col in range(0, self.width):
                ret = ret + self.positions[row_and_column_to_key(row, col)]
        return ret

    def __str__(self) -> str:
        return self.to_string(True)


# Sanity test
if __name__ == "__main__":
    board = Board(None)
    board.place(0, 0, "x")
    board.place(1, 1, "o")
    print(board)
