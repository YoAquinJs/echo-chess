"""
transmits commands to the hardware
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from hardware.interface import HardwareCommand


class HardwareTransmiter(ABC):
    """interface for hardware transmission"""

    _instance: HardwareTransmiter | None = None

    def __init__(self) -> None:
        if HardwareTransmiter._instance:
            raise RuntimeError("multiple transmitters where instantiated")

        HardwareTransmiter._instance = self
        self.setup()

    @classmethod
    def transmitter(cls) -> HardwareTransmiter:
        """transmitter getter"""

        if cls._instance is None:
            raise RuntimeError("no transmitter instantiated")

        return cls._instance

    @abstractmethod
    def setup(self) -> None:
        """setup the transmitter"""

    @abstractmethod
    async def send_command(self, cmd: HardwareCommand, args: str | None = None) -> None:
        """sends cmd to hardware with the given arguments"""
