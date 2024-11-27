"""
object representation of the positions on the physical chess board,
which is expanded for piece storage, due to the need of removing them
from game board, and fetching them back in crowning
8*8 for game board, plus 2 rows and 2 columns in the side gives
               STG-L A B C D E F G H STG-R
        STG-U      # # # # # # # # # #      STG-U
          8     #                       #     8
          7     #                       #     7
          6     #                       #     6
          5     #                       #     5
          4     #                       #     4
          3     #                       #     3
          2     #                       #     2
          1     #                       #     1
        STG-D      # # # # # # # # # #      STG-D
               STG-L A B C D E F G H STG-R

We encode the square positions into an 8 bit number unsigned,
as row and col have 10 values
both fit in 4 bits, with 4 bits for row and column.
the 4 least significant bits represent the row.
the 4 most significant bits represent the column.
"""

from __future__ import annotations

from dataclasses import dataclass

from hardware.interface import ENDIANNESS


@dataclass
class BoardPosition:
    """row and column representation of the board"""

    MAX_ROW = 9
    MAX_COL = 9

    row: int
    col: int

    def __post_init__(self):
        if self.row < 0 or self.row > BoardPosition.MAX_ROW:
            raise ValueError("invalid row")

        if self.col < 0 or self.col > BoardPosition.MAX_COL:
            raise ValueError("invalid col")

    @staticmethod
    def from_chess_encoding(position: str) -> BoardPosition:
        """from chess encoding constructs a BoardPosition"""

        if len(position) != 2:
            raise ValueError("board position expects 2 characters ")

        row = ord(position[0]) - ord("1") + 1
        col = ord(position[1]) - ord("a") + 1

        if not (
            (0 < row < BoardPosition.MAX_ROW) and (0 < col < BoardPosition.MAX_COL)
        ):
            raise ValueError("invalid chess encoding")

        return BoardPosition(row=row, col=col)

    def chess_encode(self) -> str:
        """
        encodes position into chess formatting string
        format: <column in lower case letter [a, h]><row in number [1, 8]>
        example: "e6"
        """

        invalid_squares = (0, BoardPosition.MAX_COL)
        if self.row in invalid_squares or self.col in invalid_squares:
            raise ValueError("chess encoding does not include storage squares")

        return f"{chr(ord('a')+self.col-1)}{chr(ord('0')+self.row)}"

    def human_readable(self) -> str:
        """human readable string, where STG means storage"""

        row: str | int
        if self.row == 0:
            row = "STG-L"
        elif self.row == BoardPosition.MAX_ROW:
            row = "STG-R"
        else:
            row = self.row

        col: str | int
        if self.col == 0:
            col = "STG-D"
        elif self.col == BoardPosition.MAX_COL:
            col = "STG-U"
        else:
            col = self.col

        return f"({row}, {col})"

    def hardware_encode(self) -> bytes:
        """encodes position to bytes"""

        return ((self.row << 4) | self.col).to_bytes(1, ENDIANNESS, signed=False)

    def __bytes__(self):
        return self.hardware_encode()
