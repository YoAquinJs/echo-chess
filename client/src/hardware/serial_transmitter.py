"""
serial communication transmitter
"""

import os
from typing import Literal

from serial import Serial, SerialException

from hardware.interface import HardwareCommand, HardwareStatus
from hardware.transmitter import HardwareTransmitter


class SerialTransmitter(HardwareTransmitter):
    """serial transmitter implementation using pyserial"""

    # ENV variables
    PORT_ENV = "ECHO_CHESS_SERIAL_PORT"
    BAUDRATE_ENV = "ECHO_CHESS_SERIAL_BAUDRATE"
    TIMEOUT_ENV = "ECHO_CHESS_SERIAL_TIMEOUT"

    DEFAULT_TIMEOUT = 0.1  # 100ms

    RESPONSE_ENDIANESS: Literal["big", "little"] = "big"

    def setup(self) -> None:
        port = os.environ.get(SerialTransmitter.PORT_ENV, None)
        if port is None:
            raise RuntimeError(f"missing {SerialTransmitter.PORT_ENV}")

        try:
            baudrate_var = os.environ.get(SerialTransmitter.BAUDRATE_ENV, None)
            if baudrate_var is None:
                raise RuntimeError(f"missing {SerialTransmitter.BAUDRATE_ENV}")

            baudrate = int(baudrate_var)
        except ValueError as e:
            raise RuntimeError("invalid baud rate configured") from e

        try:
            timeout_var = os.environ.get(SerialTransmitter.TIMEOUT_ENV, None)
            if timeout_var is None:
                timeout = SerialTransmitter.DEFAULT_TIMEOUT
            else:
                timeout = float(timeout_var)
        except ValueError as e:
            raise RuntimeError("invalid serial timeout configured") from e

        try:
            self.serial = Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,  # timeout for hardware response
                exclusive=True,  # ensures no other process interferes with the port
            )
        except SerialException as e:
            raise RuntimeError(f"unable to start serial com with '{port}'") from e
        except ValueError as e:
            raise RuntimeError("invalid environment variables configuration") from e

        self.port = self.serial.name

    def send_command(self, cmd: HardwareCommand) -> HardwareStatus:
        self.serial.write(cmd.serialize())
        hardware_response: bytes = self.serial.read(1)

        if len(hardware_response) == 0:
            return HardwareStatus.ERROR

        return int.from_bytes(hardware_response, SerialTransmitter.RESPONSE_ENDIANESS)
