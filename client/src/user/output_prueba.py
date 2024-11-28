"""
handles user output, via the hardware transmitter and TTS
"""
import asyncio
import logging
from tts import speak_message


async def tts_user_feedback(content: str) -> None:
    """
    Sends feedback to the user via text-to-speech asynchronously.
    Args:
        content (str): The message to convert to speech.
    """
    try:
        logging.info("Sending TTS feedback: %s", content)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, speak_message, content)
    except Exception as e:
        logging.error("Failed to send TTS feedback: %s", e)


def hardware_user_feedback(content: str) -> None:
    """
    Sends feedback to the user via hardware (not implemented yet).
    """
    logging.info("Hardware feedback requested but not implemented: %s", content)
    raise NotImplementedError("Hardware feedback is not implemented yet.")




