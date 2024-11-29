"""
serial communication transmitter
"""

from __future__ import annotations

import os

from serial import Serial, SerialException

from hardware.command import HardwareCommand
from hardware.comunication_handler import HardwareCommunicationHandler
from hardware.interface import ENDIANNESS, HardwareCommandResponse

PORT_ENV = "ECHO_CHESS_SERIAL_PORT"
BAUDRATE_ENV = "ECHO_CHESS_SERIAL_BAUDRATE"


class HardwareCommunicationSerialHandler(HardwareCommunicationHandler):
    """serial hardware handler implementation using pyserial"""

    def setup(self) -> None:
        port = os.environ.get(PORT_ENV, None)
        if port is None:
            raise RuntimeError(f"missing {PORT_ENV}")

        try:
            baudrate_var = os.environ.get(BAUDRATE_ENV, None)
            if baudrate_var is None:
                raise RuntimeError(f"missing {BAUDRATE_ENV}")

            baudrate = int(baudrate_var)
        except ValueError as e:
            raise RuntimeError("invalid baud rate configured") from e

        try:
            self.serial = Serial(
                port=port,
                timeout=None,
                baudrate=baudrate,
                exclusive=True,  # ensures no other process interferes with the port
            )
        except SerialException as e:
            raise RuntimeError(f"unable to start serial com with '{port}'") from e
        except ValueError as e:
            raise RuntimeError("invalid environment variables configuration") from e

        self.port = self.serial.name

    def cleanup(self) -> None:
        if self.serial.is_open:
            self.serial.close()

    def _transmit_command(self, command: HardwareCommand) -> None:
        self.serial.write(command.serialize())

    def _response_listener(self) -> None:
        while True:
            hardware_response: bytes = self.serial.read(1)
            self._recieve_response(HardwareCommandResponse(hardware_response))
