"""
Specification for the shared hardware interface commands
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from hardware.interface import (
    ENCODING,
    ENDIANNESS,
    HARDWARE_COMMAND_ID_SIZE,
    HardwareCommandId,
    HardwareCommandPriority,
    HardwareCommandTimeout,
)
from model.board_position import BoardPosition


@dataclass
class HardwareCommand(ABC):
    """
    hardware Command Base Abstract Class
    """

    def __init__(self) -> None:
        self.id: HardwareCommandId
        self.priority: HardwareCommandPriority
        self.timeout: HardwareCommandTimeout

    def serialize(self) -> bytes:
        """serializes the command for transmission"""

        cmd = self.id.value.to_bytes(HARDWARE_COMMAND_ID_SIZE, ENDIANNESS)
        parameters = self.serialize_args()

        if parameters is None:
            return cmd
        return cmd + parameters

    @staticmethod
    def from_id(command_id: HardwareCommandId) -> type[HardwareCommand]:
        """map command id to hardware command class"""

        mapping = {
            HardwareCommandId.AVAILABLE: AvailableHCommand,
            HardwareCommandId.MOVEMENT: AvailableHCommand,
            HardwareCommandId.CLEAR_MOVS: AvailableHCommand,
            HardwareCommandId.PRINT: PrintHCommand,
        }

        return mapping[command_id]

    @abstractmethod
    def serialize_args(self) -> bytes | None:
        """serialize the arguments for the command"""


@dataclass
class AvailableHCommand(HardwareCommand):
    """
    Fetch whether hardware command is available from hardware or not
    """

    cmd: HardwareCommandId

    id: HardwareCommandId = field(default=HardwareCommandId.AVAILABLE)
    priority: HardwareCommandPriority = field(default=HardwareCommandPriority.AVAILABLE)
    timeout: HardwareCommandTimeout = field(default=HardwareCommandTimeout.AVAILABLE)

    def serialize_args(self) -> bytes | None:
        return self.cmd.value.to_bytes(HARDWARE_COMMAND_ID_SIZE, ENDIANNESS)


@dataclass
class MovemenetHCommand(HardwareCommand):
    """
    Moves piece from origin to destination
    """

    origin: BoardPosition
    dest: BoardPosition

    id: HardwareCommandId = field(default=HardwareCommandId.MOVEMENT)
    priority: HardwareCommandPriority = field(default=HardwareCommandPriority.MOVEMENT)
    timeout: HardwareCommandTimeout = field(default=HardwareCommandTimeout.MOVEMENT)

    def serialize_args(self) -> bytes | None:
        return self.origin.hardware_encode() + self.dest.hardware_encode()


@dataclass
class ClearMovementsHCommand(HardwareCommand):
    """
    Cancel all enqueued movements
    """

    id: HardwareCommandId = field(default=HardwareCommandId.CLEAR_MOVS)
    priority: HardwareCommandPriority = field(
        default=HardwareCommandPriority.CLEAR_MOVS
    )
    timeout: HardwareCommandTimeout = field(default=HardwareCommandTimeout.CLEAR_MOVS)

    def serialize_args(self) -> bytes | None:
        return None


@dataclass
class PrintHCommand(HardwareCommand):
    """
    Prints contents to hardware display
    """

    content: str

    id: HardwareCommandId = field(default=HardwareCommandId.PRINT)
    priority: HardwareCommandPriority = field(default=HardwareCommandPriority.PRINT)
    timeout: HardwareCommandTimeout = field(default=HardwareCommandTimeout.PRINT)

    def serialize_args(self) -> bytes | None:
        return self.content.encode(ENCODING)
