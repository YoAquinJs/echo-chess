"""
This module controls the main game loop.
It listens for user commands and interacts with 
the stt and tts components.
"""

import asyncio
import logging

from config import setup_logging
from output import tts_user_feedback
from voice_detector import UnavailableSTT, user_cmd_listener

setup_logging()



async def async_user_listener(detector) -> None:
    """
    asynchronous user listener implementation
    """
    while True:
        try:
            command_chess = "chess"
            detected, text = await detector.model_get_text_async()

            if detected and command_chess in text:
                print("Chess command detected. Ready for your move.")
                await tts_user_feedback("What is your next move?")
                await asyncio.sleep(0.3)

                await user_cmd_listener(detector)
            else:
                print("Command not recognized. Waiting for 'chess'...")

        except UnavailableSTT:
            logging.error("Speech-to-text system is unavailable. Waiting to retry...")
            await tts_user_feedback(
                "The speech recognition system is unavailable. Please check your microphone."
            )
            await asyncio.sleep(1)

        except (OSError, ValueError) as e:
            logging.error("System error: %s", {e})
            await asyncio.sleep(1)

def start_user_listener(detector) -> None:
    """Starts asynchronously listening to user commands."""
    asyncio.run(async_user_listener(detector))



