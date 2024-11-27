import asyncio
import logging

from tts import speak_message
from voice_detector import UnavailableSTT, user_cmd_listener

# TODO rename every game name to user IO terminology, like input_loop
# remove prints as they pollute the program output


async def game_loop(detector):
    while True:
        try:
            command_chess = "chess"
            detected, text = await detector.model_get_text_async()

            if detected and command_chess in text:
                print("Chess command detected. Ready for your move.")
                speak_message("What is your next move?")
                await asyncio.sleep(0.3)  # TODO avoid magic numbers

                # Trigger del commando
                await user_cmd_listener(detector)

            else:
                print("Command not recognized. Waiting for 'chess'...")

        except UnavailableSTT:
            logging.error("Speech-to-text system is unavailable. Waiting to retry...")
            speak_message(
                "The speech recognition system is unavailable. Please check your microphone."
            )
            await asyncio.sleep(1)

        except (OSError, ValueError) as e:
            logging.error("System error: %s", {e})
            await asyncio.sleep(1)
