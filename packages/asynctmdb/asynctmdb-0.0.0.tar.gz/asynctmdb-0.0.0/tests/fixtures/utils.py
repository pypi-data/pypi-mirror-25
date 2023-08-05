from datetime import (date,
                      datetime)

import pytest

from tests import strategies


@pytest.fixture(scope='function')
def current_date_time() -> datetime:
    return datetime.utcnow()


@pytest.fixture(scope='session')
def tmdb_foundation_date() -> date:
    # TODO: find more accurate date
    return strategies.TMDB_FOUNDATION_DATE
