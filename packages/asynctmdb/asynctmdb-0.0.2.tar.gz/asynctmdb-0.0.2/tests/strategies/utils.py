from asyncio import (get_event_loop,
                     ensure_future)
from contextlib import closing
from datetime import date

from aiohttp import ClientSession

from asynctmdb.methods import movies

TMDB_FOUNDATION_DATE = date(year=2008,
                            month=1,
                            day=1)


def load_max_movie_id(api_base_url: str,
                      api_key: str) -> int:
    loop = get_event_loop()
    session = ClientSession(loop=loop)
    with closing(session):
        future = ensure_future(movies.latest(api_base_url=api_base_url,
                                             api_key=api_key,
                                             session=session))
        result = loop.run_until_complete(future)
    return result['id']
