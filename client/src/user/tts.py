import logging

import pyttsx3

logging.getLogger("comtypes").setLevel(logging.WARNING)


def speak_message(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
