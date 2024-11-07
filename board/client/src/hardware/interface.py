"""
defines the interface between the client and the hardware
"""

from enum import Enum


class HardwareCommand(Enum):
    """represents the command codes the hardware receives"""

    AVAILABLE = "AVL"
    CLEAR = "CLR"

    # ARGS origin: encoded_pos dest: encoded_pos
    MOVEMENT = "MOV"
    # ARGS content: str
    PRINT = "PTR"


class HardwareStatus(Enum):
    """represents status codes the hardware transmits"""

    OK = "O"
    ERR = "E"


class UnavailableHardware(Exception):
    """raise upon err or unknown status or timeout"""
