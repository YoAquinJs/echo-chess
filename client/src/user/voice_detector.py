"""
This module provides speech-to-text (STT) functionality for detecting and processing
voice commands using the Vosk library.
"""

import asyncio
import json
import logging
from typing import Tuple

import numpy as np
import pyaudio
import vosk

from config import setup_logging
from move_translations import correct_recognition, filter_move
from user_command import parse_command, UserCommand
from output import tts_user_feedback

setup_logging()

class UnavailableSTT(Exception):
    """Exception raised when speech-to-text is unavailable."""

class VoiceDetector:
    """
    Handles voice detection and speech-to-text conversion.
    """

    def __init__(self, model_path: str, sample_rate: int) -> None:
        """
        Initializes the Vosk model and audio stream.
        """
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.sample_rate = sample_rate
        self.model, self.recognizer = self.initialize_model(model_path, sample_rate)

    def initialize_model(self, model_path: str, sample_rate: int) -> Tuple[vosk.Model, vosk.KaldiRecognizer]:
        """
        Loads the Vosk model for speech recognition.
        """
        try:
            model = vosk.Model(model_path)
            recognizer = vosk.KaldiRecognizer(model, sample_rate)
            return model, recognizer
        except Exception as error:
            logging.error("Error initializing model: %s", error)
            raise UnavailableSTT("Speech recognition model is unavailable.") from error

    def initialize_stream(self) -> None:
        """
        Prepares the audio stream for capturing input.
        """
        if self.stream is None:
            try:
                audio_stream = self.p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=4096,
                )
            except OSError as e:
                logging.error("Failed to open audio stream: %s", e)
                raise UnavailableSTT from e

            try:
                self.stream = audio_stream
                self.stream.start_stream()
            except ValueError as e:
                logging.error("Failed to start audio stream: %s", e)
                raise UnavailableSTT from e

    def model_get_text(self) -> Tuple[bool, str]:
        """
        Captures and converts audio to text synchronously.
        """
        self.initialize_stream()
        detected, text = False, ""
        waiting_message_shown = False

        while True:
            data = self.stream.read(4096, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            if self.recognizer.AcceptWaveform(audio_data.tobytes()):
                result = self.recognizer.Result()
                text = json.loads(result).get("text", "").lower()

                if not text.strip():
                    continue

                
                command_chess = "chess"
                if command_chess in text:
                    detected = True
                    break

                print(f"raw command detected: {text}")
                text = correct_recognition(text)
                print(f"corrected command: {text} ")
                filtered_text = filter_move(text)
                print(f"filtered command: {text}")

                if len(filtered_text) >= 4:
                    detected = True
                    text = filtered_text
                    break
                else:
                    text = ""
            elif not waiting_message_shown:
                logging.info("Waiting for the command to start recording...")
                waiting_message_shown = True

        return detected, text

    async def model_get_text_async(self) -> Tuple[bool, str]:
        """
        Asynchronously captures audio and processes text.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.model_get_text)

async def user_cmd_listener(detector: VoiceDetector) -> None:
    """
    Listens for user commands asynchronously and logs recognized text.
    """
    try:
        detected, text = await detector.model_get_text_async()

        if not detected or not text:
            raise UnavailableSTT("No text recognized.")

        print(f"Recognized command: {text}")


        try:
            # Parse and execute the command
            command: UserCommand = parse_command(text)
            await command.callback()
        except ValueError as e:
            logging.warning("Failed to parse command: %s", e)
            await tts_user_feedback("Invalid command format. Please try again.")


    except UnavailableSTT as e:
        logging.error("STT unavailable: %s", e)

def user_cmd_parse(text: str) -> None:
    """
    Parses the recognized command text.
    """
    print(f"Parsed command: {text}")
