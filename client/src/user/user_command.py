"""
model for user voice command
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class UserCmdArg[T](ABC):
    """represents a voice command argument"""

    @classmethod
    @abstractmethod
    def parser(cls, data: str) -> T:
        """parse speech received to python objects"""


class UserCommand(ABC):
    """represents a user voice command details"""

    keyword: str
    args: tuple[UserCmdArg]

    @abstractmethod
    async def callback(self):
        """command action"""
