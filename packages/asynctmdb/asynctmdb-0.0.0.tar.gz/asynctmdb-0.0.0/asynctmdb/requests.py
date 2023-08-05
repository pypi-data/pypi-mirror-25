from functools import partial
from typing import (Any,
                    Callable,
                    Dict)

from aiohttp import ClientSession

from .types import AsyncContextManager


async def send(*,
               method: Callable[[ClientSession, str, Any],
                                AsyncContextManager],
               method_url: str,
               session: ClientSession,
               json_body: Dict[str, Any] = None,
               **params: Dict[str, str]
               ) -> Dict[str, Any]:
    async with method(session,
                      method_url,
                      json=json_body,
                      params=params) as response:
        response_json = await response.json()
        return response_json


get = partial(send,
              method=ClientSession.get)
post = partial(send,
               method=ClientSession.post)
delete = partial(send,
                 method=ClientSession.delete)
