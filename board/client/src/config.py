import json
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config():
    with open("config.json", encoding="utf-8") as config_file:
        return json.load(config_file)
