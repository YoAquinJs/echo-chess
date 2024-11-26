"""
handles user output, via the hardware transmitter and TTS
"""


def tts_user_feedback(content: str) -> None:
    """sends feedback to the user via text to speech"""

    raise NotImplementedError()


def hardware_user_feedback(content: str) -> None:
    """sends feedback to the user via hardware"""

    raise NotImplementedError()
