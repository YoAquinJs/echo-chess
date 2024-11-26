"""
user input handler, parsing STT input into user commands
"""

import asyncio


def start_user_listener() -> None:
    """starts asynchronously listening to user commands"""

    asyncio.run(async_user_listener())


async def async_user_listener():
    """asynchronous user listener implementation"""
    raise NotImplementedError()
