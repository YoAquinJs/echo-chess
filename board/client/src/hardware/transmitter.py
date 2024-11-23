"""
transmits commands to the hardware
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

    async def fetch_available_commands(self) -> None:
        """fetch available commands from hardware and cache that"""

        self.available_commands.clear()

        try:
            await self.send_command(AvailableCommand(AvailableCommand))
            self.available_commands.add(AvailableCommand)
        except HardwareError:
            return

        for command in HARDWARE_COMMANDS:
            if command == AvailableCommand:
                continue

            try:
                await self.send_command(AvailableCommand(command))
                self.available_commands.add(command)
            except HardwareError:
                return

    @abstractmethod
    def setup(self) -> None:
        """setup the transmitter"""

    @abstractmethod
    async def send_command(self, cmd: HardwareCommand) -> HardwareStatus:
        """
        sends cmd to hardware
        raises: HardwareError
        """
