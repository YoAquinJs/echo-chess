import json
import logging

from config import load_config, setup_logging
from game_controller import game_loop
from serial_communication import close_serial, initialize_serial
from voice_detector import VoiceDetector


def main():
    setup_logging()
    config = load_config()
    model_path = config["MODEL_PATH"]
    sample_rate = config["SAMPLE_RATE"]
    serial_port = config["SERIAL_PORT"]
    baud_rate = config["BAUD_RATE"]

    detector = VoiceDetector(model_path, sample_rate)
    ser = initialize_serial(serial_port, baud_rate)

    try:
        game_loop(detector, ser)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        logging.info("Error: %s", {e})
    finally:
        if "ser" in locals() and ser is not None:
            close_serial(ser)


if __name__ == "__main__":
    main()
