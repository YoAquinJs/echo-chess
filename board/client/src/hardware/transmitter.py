"""
interface for transmitting commands from client to hardware
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from hardware.interface import (
    HARDWARE_COMMANDS,
    AvailableCommand,
    HardwareCommand,
    HardwareStatus,
)


class HardwareError(Exception):
    """raise upon error, unknown response status or timeout from hardware"""

    def __init__(self, message: str, status: HardwareStatus):
        self.status = status
        super().__init__(message or status.value)


class HardwareTransmiter(ABC):
    """interface for hardware transmission"""

    _instance: HardwareTransmiter | None = None

    def __init__(self) -> None:
        if HardwareTransmiter._instance:
            raise RuntimeError("multiple transmitters where instantiated")

        HardwareTransmiter._instance = self

        self.setup()

        self.available_commands: set[type[HardwareCommand]]
        self.fetch_available_commands()

    @classmethod
    def transmitter(cls) -> HardwareTransmiter:
        """transmitter getter"""

        if cls._instance is None:
            raise RuntimeError("no transmitter initialized")

        return cls._instance

    def fetch_available_commands(self) -> None:
        """fetch available commands from hardware and cache them"""

        self.available_commands.clear()

        hardware_status = self.send_command(AvailableCommand(AvailableCommand))
        if hardware_status != HardwareStatus.AVAILABLE:
            return

        self.available_commands.add(AvailableCommand)
        for command in HARDWARE_COMMANDS:
            if command == AvailableCommand:
                continue

            hardware_status = self.send_command(AvailableCommand(command))
            if hardware_status == HardwareStatus.AVAILABLE:
                self.available_commands.add(command)

    @abstractmethod
    def setup(self) -> None:
        """setup the transmitter"""

    @abstractmethod
    def send_command(self, cmd: HardwareCommand) -> HardwareStatus:
        """sends cmd to hardware and returns status"""
