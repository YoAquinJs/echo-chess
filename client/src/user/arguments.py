"""user commgnd arguments implementations"""

from model.board_position import BoardPosition
from user.user_command import UserCommandArg


class BoardPositionArg(UserCommandArg):
    """Chess board position user command argument"""

    @classmethod
    def parse(cls, data: str) -> BoardPosition:
        return BoardPosition.from_chess_encoding(data)
