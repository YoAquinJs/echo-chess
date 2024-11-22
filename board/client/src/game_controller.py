import logging
import time

from config import setup_logging
from serial_communication import read_response, send_command
from tts import speak_message
from voice_detector import UnavailableSTT, user_cmd_listener

setup_logging()


def game_loop(detector, ser):
    while True:
        try:
            command_chess = "chess"
            text = detector.model_get_text()

            if text and command_chess in text:
                print("Chess command detected. Ready for your move.")
                speak_message("What is your next move?")
                time.sleep(0.3)

                user_cmd_listener(detector)

                if text:
                    send_command(ser, text)

                response = read_response(ser)
                if response:
                    print(f"Device response: {response}")

            else:
                print("Command not recognized. Waiting for 'chess'...")

        except UnavailableSTT:
            logging.error("Speech-to-text system is unavailable. Waiting to retry...")
            speak_message(
                "The speech recognition system is unavailable. Please check your microphone."
            )
            time.sleep(1)

        except (OSError, ValueError) as e:
            logging.error("System error: %s", {e})
            time.sleep(1)