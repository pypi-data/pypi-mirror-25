from datetime import date

import pytest
from aiohttp import ClientSession

from asynctmdb import imdb
from asynctmdb.common import StatusCode
from tests.utils import is_positive_integer


@pytest.mark.asyncio
async def test_find_by_imdb_id(imdb_id: str,
                               invalid_imdb_id: str,
                               non_existent_imdb_id: str,
                               min_movie_id: int,
                               min_movie_release_date: date,
                               api_base_url: str,
                               api_key: str,
                               invalid_api_key: str,
                               session: ClientSession) -> None:
    record = await imdb.find.movie(imdb_id,
                                   api_base_url=api_base_url,
                                   api_key=api_key,
                                   session=session)
    invalid_api_key_response = await imdb.find.movie(
            imdb_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)

    record_id = record['id']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    release_date = record['release_date']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert (release_date is None or
            isinstance(release_date, date) and
            release_date >= min_movie_release_date)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY

    with pytest.raises(ValueError):
        await imdb.find.movie(invalid_imdb_id,
                              api_base_url=api_base_url,
                              api_key=api_key,
                              session=session)
    with pytest.raises(ValueError):
        await imdb.find.movie(non_existent_imdb_id,
                              api_base_url=api_base_url,
                              api_key=api_key,
                              session=session)
