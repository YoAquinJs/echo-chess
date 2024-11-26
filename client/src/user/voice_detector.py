import asyncio
import json
import logging

import numpy as np
import pyaudio
import vosk

# kep all imports relative to projects root
from stt_translations import correct_recognition


class UnavailableSTT(Exception):
    """Exception raised when speech-to-text is unavailable."""


class VoiceDetector:
    def __init__(self, model_path, sample_rate):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.sample_rate = sample_rate
        self.model, self.recognizer = self.initialize_model(model_path, sample_rate)

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

    async def model_get_text_async(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.model_get_text)


async def user_cmd_listener(detector):
    try:
        detected, text = await detector.model_get_text_async()

        if not detected or not text:
            raise UnavailableSTT("No text recognized.")

        print(f"Recognized command: {text}")

    except UnavailableSTT as e:
        logging.error("STT unavailable: %s", e)


def user_cmd_parse(text):
    print(f"Parsed command: {text}")
