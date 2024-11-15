import logging
import time

import serial

from config import setup_logging

setup_logging()


def initialize_serial(port, baud_rate, timeout=2):
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        time.sleep(timeout)  # Allow time for the connection to establish
        print(
            f"Serial connection initialized on port {port} with baud rate {baud_rate}"
        )
        return ser
    except serial.SerialException as e:
        logging.error("Error initializing serial connection: %s", {e})
        return None


def send_command(ser, command):
    if ser and ser.is_open:
        ser.write(command.encode())
        print(f"Sent command: {command}")
    else:
        print("Serial connection not open. Command not sent.")


def read_response(ser):
    if ser and ser.is_open and ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        print(f"Received response: {response}")
        return response
    return None


def close_serial(ser):
    if ser and ser.is_open:
        ser.close()
        print("Serial connection closed.")
