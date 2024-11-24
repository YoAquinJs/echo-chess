"""
defines the interface between the client and the hardware
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from hardware.board_position import BoardPosition


class HardwareCommand(ABC):
    """hardware Command base class"""

    ENCODING = "ascii"
    ID_LENGTH = 3  # used for test assertion

    def serialize(self) -> bytes:
        """serializes the command for transmission"""

        cmd = self.__class__.command_id().encode(HardwareCommand.ENCODING)
        parameters = self._parameters()

        if parameters is None:
            return cmd
        return cmd + parameters

    @abstractmethod
    def _parameters(self) -> bytes | None:
        """serialize the parameters for the command"""

    @classmethod
    @abstractmethod
    def command_id(cls) -> str:
        """command keyword"""


@dataclass
class AvailableCommand(HardwareCommand):
    """
    returns OK when command is enabled, ERR otherwise
    serialized: AVL<cmd>
    """

    cmd: type[HardwareCommand]

    def _parameters(self) -> bytes | None:
        if self.cmd == AvailableCommand:
            return None
        return self.cmd.command_id().encode(HardwareCommand.ENCODING)

    @classmethod
    def command_id(cls) -> str:
        return "AVL"


@dataclass
class MovemenetCommand(HardwareCommand):
    """
    moves piece in origin to dest
    serialized: MOV<origin: EncodedPosition><dest: EncodedPosition>
    """

    origin: BoardPosition
    dest: BoardPosition

    def _parameters(self) -> bytes | None:
        return self.origin.encode() + self.dest.encode()

    @classmethod
    def command_id(cls) -> str:
        return "MOV"


@dataclass
class ClearCommand(HardwareCommand):
    """
    clears the movement queue
    serialized: CLR
    """

    def _parameters(self) -> bytes | None:
        return None

    @classmethod
    def command_id(cls) -> str:
        return "CLR"


@dataclass
class PrintCommand(HardwareCommand):
    """
    prints via hardware the content provided
    serialized: PTR<content: str>
    """

    content: str

    def _parameters(self) -> bytes | None:
        return self.content.encode(HardwareCommand.ENCODING)

    @classmethod
    def command_id(cls) -> str:
        return "PTR"


HARDWARE_COMMANDS: list[type[HardwareCommand]] = [
    AvailableCommand,
    MovemenetCommand,
    ClearCommand,
    PrintCommand,
]


class HardwareStatus(Enum):
    """
    represents status codes the hardware responds with, 1 byte long

    Possible Status
    OK: command received with no errors
    ERROR: command received with errors
    AVAILABLE: command available (only with AVL cmd)
    UNAVAILABLE: command unavailable (only with AVL cmd)
    """

    OK = 0
    ERROR = 1
    AVAILABLE = 3
    UNAVAILABLE = 4
