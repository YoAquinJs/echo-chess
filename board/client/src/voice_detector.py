import json
import logging

import numpy as np
import pyaudio
import vosk

from config import setup_logging
from move_translation import correct_recognition

setup_logging()


class UnavailableSTT(Exception):
    """Exception raised when speech-to-text is unavailable."""


class VoiceDetector:
    def __init__(self, model_path, sample_rate):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.model, self.recognizer = self.initialize_model(model_path, sample_rate)
        self.sample_rate = sample_rate

    def initialize_model(self, model_path, sample_rate):
        try:
            model = vosk.Model(model_path)
            recognizer = vosk.KaldiRecognizer(model, sample_rate)
            return model, recognizer
        except Exception as error:
            logging.error("Error initializing model: %s", error)
            raise UnavailableSTT("Speech recognition model is unavailable.") from error

    def initialize_stream(self):
        if self.stream is None:
            try:
                self.stream = self.p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=4096,
                )
                self.stream.start_stream()
            except Exception as e:
                logging.error("Failed to initialize audio stream: %s", e)
                raise UnavailableSTT("Microphone or audio input is unavailable.") from e
        return self.stream

    def model_get_text(self):
        audio_stream = self.initialize_stream()
        detected, text = False, ""
        waiting_message_shown = False

        while True:
            data = audio_stream.read(4096, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            if self.recognizer.AcceptWaveform(audio_data.tobytes()):
                result = self.recognizer.Result()
                text = json.loads(result).get("text", "").lower()

                text = correct_recognition(text)

                if len(text) < 3:
                    text = ""
                else:
                    detected = True
                    break
            elif not waiting_message_shown:
                print("Waiting for the command to start recording...")
                waiting_message_shown = True

        return detected, text


def user_cmd_listener(detector):
    try:
        text = detector.model_get_text()

        if not text:
            raise UnavailableSTT("No text recognized.")

        user_cmd_parse(text)

    except UnavailableSTT as e:
        logging.error("STT unavailable: %s", e)


def user_cmd_parse(text):
    print(f"Parsed command: {text}")
