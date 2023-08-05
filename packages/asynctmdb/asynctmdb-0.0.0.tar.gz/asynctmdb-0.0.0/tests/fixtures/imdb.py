from typing import (Any,
                    Dict)

import pytest

from asynctmdb import imdb
from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def imdb_id(movie_details: Dict[str, Any]) -> str:
    return movie_details['imdb_id']


@pytest.fixture(scope='session')
def non_existent_imdb_id() -> str:
    return imdb.title_id.from_int(0)


@pytest.fixture(scope='function')
def invalid_imdb_id() -> str:
    return example(strategies.invalid_imdb_ids)
