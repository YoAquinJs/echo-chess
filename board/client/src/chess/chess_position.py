"""
represents client encoding of chess board positions,
extra squares are needed for storing captured pieces and access them in game,
that's why values range from [0, 9]
"""

from dataclasses import dataclass

MAX_ROW = 9
MAX_COL = 9


@dataclass
class ChessPosition:
    """chess position representation (row, col)"""

    row: int
    col: int

    def __post_init__(self):
        if self.row < 0 or self.row > MAX_ROW:
            raise ValueError("invalid row")
        if self.col < 0 or self.col > MAX_COL:
            raise ValueError("invalid col")

    def encode(self) -> bytes:
        """encodes position to bytes"""
        return bytes([self.row, self.col])

    def human_readable(self) -> str:
        """returns position human readable string, where STG means storage"""

        if self.row == 0:
            row = "STG-L"
        elif self.row == MAX_ROW:
            row = "STG-R"
        else:
            row = self.row

        if self.col == 0:
            col = "STG-D"
        elif self.col == MAX_COL:
            col = "STG-U"
        else:
            col = self.col

        return f"({row}, {col})"
