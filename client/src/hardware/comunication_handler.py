"""
interface for input/o commands from client to hardware
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod

from hardware.command import AvailableHCommand, HardwareCommand
from hardware.errors import HardwareError
from hardware.interface import (
    MAX_COMMAND_QUEUE,
    HardwareCommandId,
    HardwareCommandResponse,
)
from hardware.response import HardwareResponse


class HardwareCommunicationHandler(ABC):
    """
    Abstract Singleton interface for hardware IO operations
    """

    _instance: HardwareCommunicationHandler | None = None

    def __init__(self) -> None:
        if HardwareCommunicationHandler._instance is not None:
            raise RuntimeError("multiple handlers where instantiated")
        HardwareCommunicationHandler._instance = self

        self.capabilities: set[type[HardwareCommand]]

        # ensures command transmission is performed by a single coroutine
        self._transmission_lock = asyncio.Lock()

        # mirror of the hardware PQueue, synchronizes responses
        # queue size if max minus one because top of queue is _pending_response
        self._command_queue_mirror: asyncio.PriorityQueue[HardwareResponse] = (
            asyncio.PriorityQueue(maxsize=MAX_COMMAND_QUEUE - 1)
        )
        self._pending_response: HardwareResponse | None

        self.setup()
        asyncio.run(self._fetch_available_commands())

    @classmethod
    def instantiated(cls) -> bool:
        """whether instanced or not"""

        return cls._instance is not None

    @classmethod
    def instance(cls) -> HardwareCommunicationHandler:
        """instance singleton"""

        if cls._instance is None:
            raise RuntimeError("no hardware handler initialized")

        return cls._instance

    async def start_response_listener(self):
        """starts the response listener"""

        await asyncio.to_thread(self._response_listener)

    async def send_command(
        self, command: HardwareCommand
    ) -> HardwareCommandResponse | None:
        """sends command to hardware and awaits for its response or timeout"""

        response = HardwareResponse(command)

        # synchronizes command dispatch to be bounded at MAX_COMMAND_QUEUE
        await self._command_queue_mirror.put(response)
        if self._command_queue_mirror.qsize() == 1:
            self._get_next_pending()

        async with self._transmission_lock:
            await asyncio.to_thread(self._send_command, command)

        await response.wait()
        return response.value

    async def _recieve_response(
        self, command_response: HardwareCommandResponse
    ) -> None:
        """
        receives command from hardware, and updates handler queue state

        raises HardwareError on non expected received response
        """

        if self._pending_response is None:
            raise HardwareError("received non expected hardware response")

        self._pending_response.respond(command_response)
        self._get_next_pending()

    async def _fetch_available_commands(self) -> None:
        """fetch available commands from hardware and cache them"""

        self.capabilities = set()

        for command_id in HardwareCommandId:
            if command_id == HardwareCommandId.AVAILABLE:
                continue

            command_response = await self.send_command(AvailableHCommand(command_id))

            if command_response == HardwareCommandResponse.AVAILABLE:
                self.capabilities.add(HardwareCommand.from_id(command_id))

    def _get_next_pending(self) -> None:
        """pop from queue to pending response"""

        self._pending_response = self._command_queue_mirror.get_nowait()
        self._pending_response.pending()

    def __del__(self):
        """cleanup the transmitter"""

        self.cleanup()

    @abstractmethod
    def setup(self) -> None:
        """setup the transmitter"""

    @abstractmethod
    def cleanup(self) -> None:
        """cleans up the transmitter"""

    @abstractmethod
    def _send_command(self, command: HardwareCommand) -> None:
        """send command synchronously"""

    @abstractmethod
    def _response_listener(self) -> None:
        """listener to hardware responses synchronously"""
