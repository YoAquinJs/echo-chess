"""
Defines the base classes and specific implementations for user commands.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
import logging

T = TypeVar("T")


class UserCmdArg(Generic[T], ABC):
    """Represents a voice command argument."""

    @classmethod
    @abstractmethod
    def parser(cls, data: str) -> T:
        """Parses speech received into a Python object."""


class UserCommand(ABC):
    """Abstracts user voice command details."""

    keyword: str 
    args: List[UserCmdArg]  

    @abstractmethod
    async def callback(self):
        """Executes the action associated with the command."""


class boardPositionArg(UserCmdArg[str]):
    """Parses chess positions like 'D5'."""

    @classmethod
    def parser(cls, data: str) -> str:
        if len(data) == 2 and data[0].isalpha() and data[1].isdigit():
            return data.upper() 
        raise ValueError(f"Invalid position format: {data}")


class MoveCommand(UserCommand):
    """Represents a chess move command."""

    keyword = "move"
    args = [boardPositionArg, boardPositionArg]  # Two board position arguments: start and end

    def __init__(self, data: str):
        """
        Initializes the MoveCommand by parsing the start and end positions.
        """
        if len(data) != 4:
            raise ValueError("Invalid move command format.")

        
        self.start = boardPositionArg.parser(data[:2]) 
        self.end = boardPositionArg.parser(data[2:])  

    async def callback(self):
        """
        Executes the move command by printing the move details.
        """
        print(f"Moving piece from {self.start} to {self.end}")

class StartGameCommand(UserCommand):
    """Represents a command to start the game."""

    keyword = "start" 

    args = []  

    async def callback(self):
        """Executes the start game command."""
        print("Starting the chess game...")

class GetTokenCommand(UserCommand):
    """Represents a command to get a token."""

    keyword = "get_token"  

    args = []  

    async def callback(self):
        """Executes the get token command."""
        print("Fetching the user token...")
        
def parse_command(text: str) -> UserCommand:
    """
    Parses the recognized text into a specific command.
    """
    logging.info("Parsing command: %s", text)

    if text.startswith("move"):
        return MoveCommand(text[4:].strip())  
    elif text.startswith("start"):
        return StartGameCommand()  
    elif text.startswith("get_token"):
        return GetTokenCommand()  
    else:
        raise ValueError(f"Unknown command: {text}")
    


