"""
Deferred Hardware Command object to keep track of sent command state
"""

import asyncio
from dataclasses import dataclass, field
from typing import cast

from hardware.command import HardwareCommand
from hardware.errors import HardwareError
from hardware.interface import HardwareCommandResponse


@dataclass
class HardwareResponse:
    """tracks the state of a sent command"""

    command: HardwareCommand

    # pending for response
    _on_pending: asyncio.Event = field(
        default_factory=asyncio.Event, init=False
    )

    # received command response
    _on_recieve: asyncio.Event = field(
        default_factory=asyncio.Event, init=False
    )

    value: HardwareCommandResponse | None = field(default=None, init=False)

    async def wait(self):
        """
        Wait for response to be next in line, and for hardware to respond or
        timeout

        raises HardwareError if response times out
        """

        await self._on_pending.wait()

        try:
            await asyncio.wait_for(
                self._on_recieve.wait(), int(self.command.timeout)
            )

            self.value = cast(HardwareCommandResponse, self.value)
        except asyncio.TimeoutError as e:
            raise HardwareError("hardware response timed out") from e

        return self.value

    def pending(self):
        """mark response as next to be"""

        self._on_pending.set()

    def respond(self, response: HardwareCommandResponse):
        """receives response from hardware response handler and trigger event"""

        self._on_recieve.set()
        self.value = response

    def __lt__(self, other):
        return self.command.priority < other.command.priority
