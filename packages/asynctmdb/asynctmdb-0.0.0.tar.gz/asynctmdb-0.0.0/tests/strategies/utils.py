from asyncio import (get_event_loop,
                     ensure_future)
from datetime import date

from aiohttp import ClientSession

from asynctmdb.methods import movies
from .api import (api_base_url,
                  api_key)


def load_max_movie_id() -> int:
    loop = get_event_loop()
    session = ClientSession(loop=loop)

    future = ensure_future(movies.latest(api_base_url=api_base_url,
                                         api_key=api_key,
                                         session=session))
    result = loop.run_until_complete(future)
    return result['id']


TMDB_FOUNDATION_DATE = date(year=2008,
                            month=1,
                            day=1)
