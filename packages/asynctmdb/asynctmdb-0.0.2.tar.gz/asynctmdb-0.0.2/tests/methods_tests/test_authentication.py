from datetime import datetime

import pytest
from aiohttp import ClientSession

from asynctmdb.common import StatusCode
from asynctmdb.methods.authentication import (create_request_token,
                                              create_session,
                                              create_guest_session,
                                              validate_request_token)
from tests.utils import is_non_empty_hex_string


@pytest.mark.asyncio
async def test_create_request_token(api_base_url: str,
                                    api_key: str,
                                    invalid_api_key: str,
                                    current_date_time: datetime,
                                    session: ClientSession) -> None:
    valid_response = await create_request_token(
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)
    invalid_api_key_response = await create_request_token(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)

    succeed = valid_response['success']
    expiration_date_time = valid_response['expires_at']
    request_token = valid_response['request_token']
    invalid_api_key_status_code = invalid_api_key_response['status_code']

    assert isinstance(succeed, bool) and succeed
    assert expiration_date_time >= current_date_time
    assert is_non_empty_hex_string(request_token)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY


@pytest.mark.asyncio
async def test_validate_request_token(api_base_url: str,
                                      api_key: str,
                                      invalid_api_key: str,
                                      user_name: str,
                                      user_password: str,
                                      unvalidated_request_token: str,
                                      session: ClientSession) -> None:
    valid_response = await validate_request_token(
            api_base_url=api_base_url,
            api_key=api_key,
            username=user_name,
            password=user_password,
            request_token=unvalidated_request_token,
            session=session)
    invalid_api_key_response = await validate_request_token(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            username=user_name,
            password=user_password,
            request_token=unvalidated_request_token,
            session=session)

    succeed = valid_response['success']
    validated_request_token = valid_response['request_token']
    invalid_api_key_status_code = invalid_api_key_response['status_code']

    assert isinstance(succeed, bool) and succeed
    assert is_non_empty_hex_string(validated_request_token)
    assert validated_request_token == unvalidated_request_token
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY


@pytest.mark.asyncio
async def test_create_session(api_base_url: str,
                              api_key: str,
                              invalid_api_key: str,
                              user_name: str,
                              user_password: str,
                              unvalidated_request_token: str,
                              session: ClientSession) -> None:
    unvalidated_token_response = await create_session(
            api_base_url=api_base_url,
            api_key=api_key,
            request_token=unvalidated_request_token,
            session=session)
    response = await validate_request_token(
            api_base_url=api_base_url,
            api_key=api_key,
            username=user_name,
            password=user_password,
            request_token=unvalidated_request_token,
            session=session)
    validated_request_token = response['request_token']
    valid_response = await create_session(
            api_base_url=api_base_url,
            api_key=api_key,
            request_token=validated_request_token,
            session=session)
    invalid_api_key_response = await create_session(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            request_token=validated_request_token,
            session=session)

    succeed = valid_response['success']
    session_id = valid_response['session_id']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    unvalidated_token_status_code = unvalidated_token_response['status_code']

    assert isinstance(succeed, bool) and succeed
    assert is_non_empty_hex_string(session_id)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert unvalidated_token_status_code == StatusCode.SESSION_DENIED


@pytest.mark.asyncio
async def test_create_guest_session(api_base_url: str,
                                    api_key: str,
                                    invalid_api_key: str,
                                    session: ClientSession) -> None:
    valid_response = await create_guest_session(
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)
    invalid_api_key_response = await create_guest_session(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)

    succeed = valid_response['success']
    expiration_date_time = valid_response['expires_at']
    guest_session_id = valid_response['guest_session_id']
    invalid_api_key_status_code = invalid_api_key_response['status_code']

    assert succeed
    assert expiration_date_time >= datetime.utcnow()
    assert isinstance(guest_session_id, str)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
