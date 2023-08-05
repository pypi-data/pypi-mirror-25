from asyncio import (AbstractEventLoop,
                     ensure_future)

import pytest
from aiohttp import ClientSession

from asynctmdb.methods.authentication import (
    create_request_token,
    create_session,
    validate_request_token,
    create_guest_session)
from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def user_name() -> str:
    return example(strategies.users_names)


@pytest.fixture(scope='function')
def user_password() -> str:
    return example(strategies.users_passwords)


@pytest.fixture(scope='function')
def unvalidated_request_token(api_base_url: str,
                              api_key: str,
                              session: ClientSession,
                              event_loop: AbstractEventLoop) -> str:
    future = ensure_future(create_request_token(
            api_base_url=api_base_url,
            api_key=api_key,
            session=session))
    response = event_loop.run_until_complete(future)
    return response['request_token']


@pytest.fixture(scope='function')
def guest_session_id(api_base_url: str,
                     api_key: str,
                     session: ClientSession,
                     event_loop: AbstractEventLoop) -> str:
    future = ensure_future(create_guest_session(
            api_base_url=api_base_url,
            api_key=api_key,
            session=session))
    response = event_loop.run_until_complete(future)
    return response['guest_session_id']


@pytest.fixture(scope='function')
def session_id(api_base_url: str,
               api_key: str,
               user_name: str,
               user_password: str,
               unvalidated_request_token: str,
               session: ClientSession,
               event_loop: AbstractEventLoop) -> str:
    future = ensure_future(validate_request_token(
            api_base_url=api_base_url,
            api_key=api_key,
            username=user_name,
            password=user_password,
            request_token=unvalidated_request_token,
            session=session))
    response = event_loop.run_until_complete(future)
    validated_request_token = response['request_token']
    future = ensure_future(create_session(
            api_base_url=api_base_url,
            api_key=api_key,
            request_token=validated_request_token,
            session=session))
    response = event_loop.run_until_complete(future)
    return response['session_id']


@pytest.fixture(scope='session')
def invalid_session_id() -> str:
    return ''
