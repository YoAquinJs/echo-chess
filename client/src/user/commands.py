"""user commands implementation"""

from user.arguments import BoardPositionArg
from user.user_command import UserCommand, UserCommandArg


class MoveUserCommand(UserCommand):
    """chesboard movement user command"""

    keyword: str = "move"
    arguments: list[type[UserCommandArg]] = [BoardPositionArg]

    async def callback(self):
        """command action"""
        raise NotImplementedError()
