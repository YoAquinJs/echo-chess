"""
Shared interface with hardware for command, response and data specification
"""

from enum import Enum
from typing import Literal

# the board position specification is in the model.board_position module as
# board positions are shared among the system

# Based on the maximum expected movement queue (32, all pieces at once)
# plus a reasonable queue for other commands
MAX_COMMAND_QUEUE = 50

# size in bytes of command ids
HARDWARE_COMMAND_ID_SIZE = 1

# Further command specification such as arguments are kept in the
# hardware.command module

# encoding details
ENCODING = "ascii"
ENDIANNESS: Literal["big", "little"] = "big"


class HardwareCommandId(Enum):
    """
    Command Identifier Codes

    AVAILABLE           0x00
    MOVEMENT            0x01
    CLEAR_MOVS          0x02
    PRINT               0x0f
    """

    AVAILABLE = 0x00
    MOVEMENT = 0x01
    CLEAR_MOVS = 0x02
    PRINT = 0x0F


class HardwareCommandPriority(Enum):
    """
    Command Priority
    Priority is descendant

    AVAILABLE           0
    MOVEMENT            2
    CLEAR_MOVS          1
    PRINT               1
    """

    AVAILABLE = 0
    MOVEMENT = 2
    CLEAR_MOVS = 1
    PRINT = 1


class HardwareCommandTimeout(Enum):
    """
    Command Identifier Codes

    AVAILABLE           100
    MOVEMENT            4000
    CLEAR_MOVS          100
    PRINT               100
    """

    AVAILABLE = 100
    MOVEMENT = 4000
    CLEAR_MOVS = 100
    PRINT = 100


class HardwareCommandResponse(Enum):
    """
    Command Response Codes

        No errors
    EXECUTED            0x00
    SKIPPED             0x01
        Availability
    AVAILABLE           0x0A
    UNAVAILABLE         0x0B
        Error
    CLIENT_ERROR        0x10
    HARDWARE_ERROR      0x11
    """

    EXECUTED = 0x00
    SKIPPED = 0x01

    AVAILABLE = 0x0A
    UNAVAILABLE = 0x0B

    CLIENT_ERROR = 0x10
    HARDWARE_ERROR = 0x11
