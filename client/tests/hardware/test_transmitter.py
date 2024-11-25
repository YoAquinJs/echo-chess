"""test of the hardware via the mock class"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from hardware.interface import HARDWARE_COMMANDS, AvailableCommand
from hardware.mock_transmitter import MockHardwareTransmitter, MockResponseMode
from hardware.transmitter import HardwareCommand, HardwareTransmitter


@pytest.fixture()
def clean_transmitter_singleton() -> None:
    """sets transmitter singleton none for avoiding multiple instances error between tests"""

    HardwareTransmitter._instance = None


def test_transmitter_singleton(clean_transmitter_singleton) -> None:
    """assert transmitter singleton"""

    instance = MockHardwareTransmitter(MockResponseMode.SUCCEEDS)
    assert instance == HardwareTransmitter.transmitter()


def test_transmitter_fail_on_multiple_instances(clean_transmitter_singleton) -> None:
    """test exception raised upon multiple instances of transsmitter are attempted"""

    with pytest.raises(RuntimeError):
        MockHardwareTransmitter(MockResponseMode.SUCCEEDS)
        MockHardwareTransmitter(MockResponseMode.SUCCEEDS)


@given(st.sets(st.sampled_from(HARDWARE_COMMANDS)))
def test_fetch_available_commands(enabled_commands: set[type[HardwareCommand]]) -> None:
    """test the fetch of available commands"""

    if HardwareTransmitter.instantiated():
        HardwareTransmitter._instance = None

    MockHardwareTransmitter(MockResponseMode.SUCCEEDS, enabled_commands)
    available_commands = HardwareTransmitter.transmitter().available_commands

    if AvailableCommand not in enabled_commands:
        enabled_commands.clear()
    else:
        enabled_commands.remove(AvailableCommand)

    assert available_commands == enabled_commands
