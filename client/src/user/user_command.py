"""
model for user voice command
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class UserCommandArg(ABC):
    """represents a voice command argument"""

    @classmethod
    @abstractmethod
    def parse(cls, data: str) -> Any:
        """parse speech received to python objects"""


class UserCommand(ABC):
    """represents a user voice command details"""

    keyword: str
    arguments: list[type[UserCommandArg]]

    def __init__(self, raw_input: str):
        self.args: list[Any] = []
        for word, arg in zip(raw_input.strip(" "), self.__class__.arguments):
            self.args.append(arg.parse(word))

    @abstractmethod
    async def callback(self):
        """command action"""
