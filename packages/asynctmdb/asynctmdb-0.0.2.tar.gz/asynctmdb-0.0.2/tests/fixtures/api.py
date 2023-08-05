import pytest

from tests import strategies
from tests.utils import example


@pytest.fixture(scope='session')
def api_key() -> str:
    return example(strategies.api_keys)


@pytest.fixture(scope='session')
def invalid_api_key() -> str:
    return example(strategies.invalid_api_keys)


@pytest.fixture(scope='session')
def api_base_url() -> str:
    return example(strategies.api_base_urls)
