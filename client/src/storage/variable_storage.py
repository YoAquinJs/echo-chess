"""handles persistent data storage"""

import inspect
import re
import sys
from importlib.metadata import metadata, version
from pathlib import Path
from typing import Any

# from appdirs import user_data_dir

APP_NAME = "voice-chess-client"

APP_VERSION = version(APP_NAME)
APP_METADATA = metadata(APP_NAME)


class VarsStorage:
    """static class for permanent storage utils"""

    VARS_FILENAME = "variables"
    VARS_SEPARATOR = " "

    data_dir: Path
    var_file: Path

    @classmethod
    def setup(cls) -> None:
        """asserts storage is available"""

        data_path: Path = Path(inspect.getfile(sys.modules["__main__"]))
        if not data_path.exists():
            raise RuntimeError("can't find source directory")

        cls.data_dir = data_path.parent
        cls.data_dir.mkdir(parents=True, exist_ok=True)

        cls.var_file = cls.data_dir / cls.VARS_FILENAME

    @classmethod
    def store(cls, key: str, value: Any) -> None:
        """stores key-value pair"""

        if " " in key or "\n" in key:
            raise ValueError(f"invalid key name: '{key}'")

        val_str = str(value)

        if "\n" in val_str:
            raise ValueError("value must not contain a new line")

        with open(cls.var_file, "a", encoding="UTF-8") as file:
            file.write(f"{key} {val_str}")

    @classmethod
    def get(cls, key: str) -> str | None:
        """retrieves key-value pair"""

        value: str | None = None
        with open(cls.var_file, "r", encoding="UTF-8") as file:
            for line in file:
                match = re.match(f"^{key} (.*)", line)
                if not match:
                    continue

                value = match.group(0) or None
                break

        return value
