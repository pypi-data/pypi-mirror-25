import operator

import pytest
from aiohttp import ClientSession

from asynctmdb.methods import genres
from tests.utils import (is_positive_integer,
                         is_non_empty_string)


@pytest.mark.asyncio
async def test_movie_genres(api_base_url: str,
                            api_key: str,
                            session: ClientSession) -> None:
    records = await genres.movie(api_base_url=api_base_url,
                                 api_key=api_key,
                                 session=session)

    records_count = len(records)
    records_ids = list(map(operator.itemgetter('id'), records))
    records_names = list(map(operator.itemgetter('name'), records))

    assert isinstance(records, list)
    assert all(map(is_positive_integer, records_ids))
    assert all(map(is_non_empty_string, records_names))

    assert len(set(records_ids)) == records_count
    assert len(set(records_names)) == records_count


@pytest.mark.asyncio
async def test_tv_genres(api_base_url: str,
                         api_key: str,
                         session: ClientSession) -> None:
    records = await genres.tv(api_base_url=api_base_url,
                              api_key=api_key,
                              session=session)

    records_count = len(records)
    records_ids = list(map(operator.itemgetter('id'), records))
    records_names = list(map(operator.itemgetter('name'), records))

    assert isinstance(records, list)
    assert all(map(is_positive_integer, records_ids))
    assert all(map(is_non_empty_string, records_names))

    assert len(set(records_ids)) == records_count
    assert len(set(records_names)) == records_count
