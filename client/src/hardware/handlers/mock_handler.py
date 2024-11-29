"""
hardware transmitter mock
"""

import random
from enum import Enum, auto
from queue import PriorityQueue

from hardware.command import AvailableHCommand, HardwareCommand
from hardware.comunication_handler import HardwareCommunicationHandler
from hardware.interface import HardwareCommandId, HardwareCommandResponse


class MockResponseMode(Enum):
    """behaviour of hardware response status from send_command"""

    SUCCEEDS = auto()
    FAILS = auto()
    UNDETERMINED = auto()


class HardwareCommunicationMockHandler(HardwareCommunicationHandler):
    """
    mock the hardware communication handler
    """

    def __init__(
        self,
        mock_response_mode: MockResponseMode,
        capabilities: set[type[HardwareCommand]] | None = None,
    ) -> None:
        self.mock_mode = mock_response_mode

        if capabilities is None:
            # default to all
            self.capabilities = {
                HardwareCommand.from_id(id) for id in HardwareCommandId
            }
        else:
            self.capabilities = capabilities

        self.sent_commands: PriorityQueue[HardwareCommand] = PriorityQueue()
        super().__init__()

    def setup(self) -> None:
        pass

    def cleanup(self) -> None:
        pass

    def _transmit_command(self, command: HardwareCommand) -> None:
        """send command synchronously"""
        self.sent_commands.put(command)

    def _response_listener(self) -> None:
        """listener to hardware responses synchronously"""
        while True:
            if self.sent_commands.empty():
                continue

            command = self.sent_commands.get()
            response: HardwareCommandResponse
            match self.mock_mode:
                case MockResponseMode.SUCCEEDS:
                    response = self.send_command_mock_ok(command)
                case MockResponseMode.FAILS:
                    response = self.send_command_mock_error(command)
                case MockResponseMode.UNDETERMINED:
                    response = self.send_command_mock_undetermined(command)

            self._recieve_response(response)

    def send_command_mock_ok(
        self, command: HardwareCommand
    ) -> HardwareCommandResponse:
        """sends command and always succeeds"""

        if isinstance(command, AvailableHCommand):
            if command.cmd in self.capabilities:
                return HardwareCommandResponse.AVAILABLE
            return HardwareCommandResponse.UNAVAILABLE

        return HardwareCommandResponse.EXECUTED

    def send_command_mock_error(
        self, _: HardwareCommand
    ) -> HardwareCommandResponse:
        """sends command and always fails"""

        return HardwareCommandResponse.HARDWARE_ERROR

    def send_command_mock_undetermined(
        self, command: HardwareCommand
    ) -> HardwareCommandResponse:
        """sends command and may succeed or fail"""

        if isinstance(command, AvailableHCommand):
            if random.random() < 0.5:
                return HardwareCommandResponse.HARDWARE_ERROR

            if command.__class__ in self.capabilities:
                return HardwareCommandResponse.AVAILABLE
            return HardwareCommandResponse.UNAVAILABLE

        return random.choice(
            [
                HardwareCommandResponse.EXECUTED,
                HardwareCommandResponse.SKIPPED,
                HardwareCommandResponse.HARDWARE_ERROR,
            ]
        )
