from functools import partial
from typing import (Any,
                    Dict)

from aiohttp import ClientSession

from asynctmdb import requests
from asynctmdb.config import API_BASE_URL
from asynctmdb.utils import urljoin

external_sources = {'imdb_id',
                    'freebase_mid', 'freebase_id',
                    'tvdb_id', 'tvrage_id'}


async def by_id(external_id: str,
                *,
                api_base_url: str = API_BASE_URL,
                api_key: str,
                language: str = None,
                external_source: str,
                session: ClientSession) -> Dict[str, Any]:
    """
    Search for objects by an external id (for instance, an IMDb ID).

    This method will search all objects (movies, TV shows and people)
    and return the results in a single response.

    The supported external sources for each object are as follows.

    +-------------+-----------+-----------+-----------+-----------+-----------+
    |             |Movies     |TV Shows   |TV Seasons |TV Episodes|People     |
    +=============+===========+===========+===========+===========+===========+
    |IMDb ID      |✓          |✓          |✗          |✓          |✓          |
    +-------------+-----------+-----------+-----------+-----------+-----------+
    |Freebase MID |✗          |✓          |✓          |✓          |✓          |
    +-------------+-----------+-----------+-----------+-----------+-----------+
    |Freebase ID  |✗          |✓          |✓          |✓          |✓          |
    +-------------+-----------+-----------+-----------+-----------+-----------+
    |TVDB ID      |✗          |✓          |✓          |✓          |✗          |
    +-------------+-----------+-----------+-----------+-----------+-----------+
    |TVRage ID    |✗          |✓          |✓          |✓          |✓          |
    +-------------+-----------+-----------+-----------+-----------+-----------+

    More info at :find:`TMDb docs <find-by-id>`.
    """
    method_url = urljoin(api_base_url, 'find', external_id)

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  external_source=external_source,
                                  **params)
    return response


by = {external_source: partial(by_id,
                               external_source=external_source)
      for external_source in external_sources}
