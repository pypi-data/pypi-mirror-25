from asyncio import (AbstractEventLoop,
                     ensure_future)
from datetime import (date,
                      datetime)
from typing import (Any,
                    Dict,
                    Set)

import pytest
from aiohttp import ClientSession

from asynctmdb.methods import movies
from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def movie_details(api_base_url: str,
                  api_key: str,
                  session: ClientSession,
                  event_loop: AbstractEventLoop) -> Dict[str, Any]:
    while True:
        movie_id = example(strategies.movies_ids)
        coroutine = movies.details(movie_id,
                                   api_base_url=api_base_url,
                                   api_key=api_key,
                                   session=session)
        future = ensure_future(coroutine)
        result = event_loop.run_until_complete(future)
        try:
            if not result['imdb_id']:
                continue
        except KeyError:
            continue

        return result


@pytest.fixture(scope='session')
def min_movie_id() -> int:
    return strategies.MIN_MOVIE_ID


@pytest.fixture(scope='function')
def movie_id(movie_details: Dict[str, Any]) -> int:
    return movie_details['id']


@pytest.fixture(scope='function')
def nonexistent_movie_id() -> int:
    return example(strategies.nonexistent_movies_ids)


@pytest.fixture(scope='session')
def min_movie_release_date() -> date:
    return date(year=1890, month=1, day=1)


@pytest.fixture(scope='session')
def movie_changes_start_date() -> datetime:
    return example(strategies.movies_changes_date_times)


@pytest.fixture(scope='session')
def movie_changes_end_date(movie_changes_start_date: datetime) -> datetime:
    return movie_changes_start_date + movies.MAX_TIME_RANGE_LENGTH


@pytest.fixture(scope='session')
def movie_videos_sites() -> Set[str]:
    return {'YouTube'}


@pytest.fixture(scope='function')
def page_number() -> int:
    return example(strategies.pages_numbers)


@pytest.fixture(scope='function')
def invalid_page_number() -> int:
    return example(strategies.invalid_pages_numbers)


@pytest.fixture(scope='function')
def movie_rating() -> float:
    return example(strategies.movies_ratings)
