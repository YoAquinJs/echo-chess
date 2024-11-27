"""
Contain hardware errors
"""


class HardwareMisusedError(Exception):
    """
    raise on client misuse of hardware
        client error command response
        attempt to send on available command
    """


class HardwareError(Exception):
    """
    raise when hardware fails
        timeout
        hardware error command response
    """
