from contextlib import suppress
from datetime import datetime
from typing import (Any,
                    Dict)

from aiohttp import ClientSession

from asynctmdb.common import (DATE_FORMAT,
                              StatusCode)
from asynctmdb.config import API_BASE_URL
from asynctmdb.methods import find


async def movie(imdb_id: str,
                *,
                api_base_url: str = API_BASE_URL,
                api_key: str,
                language: str = None,
                session: ClientSession) -> Dict[str, Any]:
    params = {}
    if language is not None:
        params['language'] = language

    response = await find.by['imdb_id'](imdb_id,
                                        api_base_url=api_base_url,
                                        api_key=api_key,
                                        session=session,
                                        **params)
    try:
        records = response['movie_results']
    except KeyError as err:
        status_code = response['status_code']
        if status_code != StatusCode.RESOURCE_NOT_FOUND:
            return response
        err_msg = 'Invalid IMDb id: "{imdb_id}".'
        raise ValueError(err_msg) from err

    try:
        record, = records
    except ValueError as err:
        if records:
            err_msg = (f'Movie imdb id "{imdb_id}" is ambiguous: '
                       f'found {len(records)} records.')
        else:
            err_msg = ('No record found for movie with '
                       f'IMDb id "{imdb_id}".')
        raise ValueError(err_msg) from err
    else:
        normalize_movie(record)
        return record


def normalize_movie(record: Dict[str, Any],
                    *,
                    format_string: str = DATE_FORMAT) -> None:
    with suppress(TypeError):
        record['release_date'] = (datetime.strptime(record['release_date'],
                                                    format_string)
                                  .date())
