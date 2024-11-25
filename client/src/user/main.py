import asyncio
import json
import logging

from config import load_config, setup_logging
from game_controller import game_loop
from voice_detector import VoiceDetector


async def main_async():
    setup_logging()
    config = load_config()
    model_path = config["MODEL_PATH"]
    sample_rate = config["SAMPLE_RATE"]

    detector = VoiceDetector(model_path, sample_rate)

    try:
        await game_loop(detector)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        logging.info("Error: %s", {e})


if __name__ == "__main__":
    asyncio.run(main_async())
