"""
Voice-Chess Client

Configure via .env file in src/
"""

from dotenv import load_dotenv


def main():
    """program entry point"""

    if not load_dotenv():
        raise RuntimeError("no .env configuration file found")


if __name__ == "__main__":
    main()
