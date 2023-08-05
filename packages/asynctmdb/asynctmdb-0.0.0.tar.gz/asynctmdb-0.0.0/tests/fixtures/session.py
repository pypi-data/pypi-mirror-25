from asyncio import AbstractEventLoop
from typing import Generator

import pytest
from aiohttp import ClientSession


@pytest.fixture(scope='function')
def session(event_loop: AbstractEventLoop
            ) -> Generator[ClientSession, None, None]:
    with ClientSession(loop=event_loop) as result:
        yield result
