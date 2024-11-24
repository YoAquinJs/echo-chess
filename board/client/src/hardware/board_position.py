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

from dataclasses import dataclass
from typing import Literal


@dataclass
class BoardPosition:
    """row and column representation of the board"""

    MAX_ROW = 9
    MAX_COL = 9

    row: int
    col: int

    ENDIANNESS: Literal["big", "little"] = "big"

    def __post_init__(self):
        if self.row < 0 or self.row > BoardPosition.MAX_ROW:
            raise ValueError("invalid row")

        if self.col < 0 or self.col > BoardPosition.MAX_COL:
            raise ValueError("invalid col")

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

    def encode(self) -> bytes:
        """encodes position to bytes"""
        return ((self.row << 4) | self.col).to_bytes(
            1, BoardPosition.ENDIANNESS, signed=False
        )

    def __bytes__(self):
        return self.encode()
