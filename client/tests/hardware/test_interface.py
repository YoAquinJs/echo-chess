"""unit tests for the hardware.interface module"""

from hardware.interface import HARDWARE_COMMANDS, HardwareCommand


def test_command_id_length():
    """test that command identifiers are ID_LENGHT size"""

    for cmd in HARDWARE_COMMANDS:
        assert len(cmd.command_id()) == HardwareCommand.ID_LENGTH
