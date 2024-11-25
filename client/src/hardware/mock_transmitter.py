"""
hardware transmitter mock
"""

import random
from enum import Enum, auto

from hardware.interface import (
    HARDWARE_COMMANDS,
    STATUSES_WITHOUT_AVAILABILIY,
    AvailableCommand,
    HardwareCommand,
    HardwareStatus,
)
from hardware.transmitter import HardwareTransmitter


class MockResponseMode(Enum):
    """behaviour of hardware response status from send_command"""

    SUCCEEDS = auto()
    FAILS = auto()
    UNDETERMINED = auto()


class MockHardwareTransmitter(HardwareTransmitter):
    """
    mock the hardware transmitter, for mocking the hardware app-wide
    """

    def __init__(
        self,
        mock_response_mode: MockResponseMode,
        enabled_cmds: set[type[HardwareCommand]] = None,
    ) -> None:
        self.mock_mode = mock_response_mode
        self.enabled_commands = (
            HARDWARE_COMMANDS if enabled_cmds is None else enabled_cmds
        )
        super().__init__()

    def setup(self) -> None:
        pass

    def send_command(self, cmd: HardwareCommand) -> HardwareStatus:
        match self.mock_mode:
            case MockResponseMode.SUCCEEDS:
                return self.send_command_mock_ok(cmd)
            case MockResponseMode.FAILS:
                return self.send_command_mock_error(cmd)
            case MockResponseMode.UNDETERMINED:
                return self.send_command_mock_undetermined(cmd)

    def send_command_mock_ok(self, cmd: HardwareCommand) -> HardwareStatus:
        """sends command and always succeeds"""

        if isinstance(cmd, AvailableCommand):
            if cmd.cmd in self.enabled_commands:
                return HardwareStatus.AVAILABLE
            return HardwareStatus.UNAVAILABLE

        return HardwareStatus.OK

    def send_command_mock_error(self, _cmd: HardwareCommand) -> HardwareStatus:
        """sends command and always fails"""

        return HardwareStatus.ERROR

    def send_command_mock_undetermined(self, cmd: HardwareCommand) -> HardwareStatus:
        """sends command and may succeed or fail"""

        if isinstance(cmd, AvailableCommand):
            if random.random() < 0.5:
                return HardwareStatus.ERROR

            if cmd.cmd in self.enabled_commands:
                return HardwareStatus.AVAILABLE
            return HardwareStatus.UNAVAILABLE

        return random.choice(STATUSES_WITHOUT_AVAILABILIY)
