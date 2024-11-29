"""
This module handles text-to-speech (TTS).
"""

import logging

import pyttsx3

logging.getLogger("comtypes").setLevel(logging.WARNING)


def speak_message(text: str) -> None:
    """
    Converts a text message to speech and plays it synchronously.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
