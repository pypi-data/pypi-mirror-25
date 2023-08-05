from datetime import datetime
from typing import (Any,
                    Union,
                    Dict)

from aiohttp import ClientSession

from asynctmdb import requests
from asynctmdb.common import DATE_TIME_FORMAT
from asynctmdb.config import API_BASE_URL
from asynctmdb.utils import urljoin


async def create_request_token(*,
                               api_base_url: str = API_BASE_URL,
                               api_key: str,
                               session: ClientSession,
                               date_time_format: str = DATE_TIME_FORMAT
                               ) -> Dict[str, Union[int, str, datetime]]:
    """
    Create a temporary request token
    that can be used to validate a TMDb user login.

    More details about how this works can be found
    :authentication:`here <how-do-i-generate-a-session-id>`.

    More info at :authentication:`TMDb docs <create-request-token>`.
    """
    method_url = urljoin(base_method_url(api_base_url),
                         'token',
                         'new')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key)
    normalize_response(response,
                       date_time_format=date_time_format)
    return response


async def create_session(*,
                         api_base_url: str = API_BASE_URL,
                         api_key: str,
                         request_token: str,
                         session: ClientSession
                         ) -> Dict[str, Union[int, str]]:
    """
    Create a fully valid session.

    This method can be used once a user has validated the request token.

    More details about how this works can be found
    :authentication:`here <how-do-i-generate-a-session-id>`.

    More info at :authentication:`TMDb docs <create-request-token>`.
    """
    method_url = urljoin(base_method_url(api_base_url),
                         'session',
                         'new')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  request_token=request_token)
    return response


async def validate_request_token(*,
                                 api_base_url: str = API_BASE_URL,
                                 api_key: str,
                                 username: str,
                                 password: str,
                                 request_token: str,
                                 session: ClientSession
                                 ) -> Dict[str, Union[int, str]]:
    """
    Validate a request token with username and password.

    **Caution**

    Please note, using this method is strongly discouraged.

    The preferred method of validating a request token is
    to have a user authenticate the request via the TMDb website.

    More details about how this works can be found
    :authentication:`here <how-do-i-generate-a-session-id>`.

    More info at :authentication:`TMDb docs <validate-request-token>`.
    """
    method_url = urljoin(base_method_url(api_base_url),
                         'token',
                         'validate_with_login')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  username=username,
                                  password=password,
                                  request_token=request_token)
    return response


async def create_guest_session(*,
                               api_base_url: str = API_BASE_URL,
                               api_key: str,
                               session: ClientSession,
                               date_time_format: str = DATE_TIME_FORMAT
                               ) -> Dict[str, Union[int, str, datetime]]:
    """
    Create a new guest session.

    Guest sessions are a type of session that will let a user rate movies
    and TV shows but not require them to have a TMDb user account.

    More information about user authentication can be found
    :authentication:`here <how-do-i-generate-a-session-id>`.

    Please note, there should be generated only a single guest session
    per user (or device) as you will be able to attach the ratings
    to a TMDb user account in the future.

    There is also IP limits in place so you should always make sure
    it's the end user doing the guest session actions.

    If a guest session is not used for the first time within 24 hours,
    it will be automatically deleted.

    More info at :authentication:`TMDb docs <create-guest-session>`.
    """
    method_url = urljoin(base_method_url(api_base_url),
                         'guest_session',
                         'new')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key)
    normalize_response(response,
                       date_time_format=date_time_format)
    return response


def base_method_url(api_base_url: str) -> str:
    return urljoin(api_base_url, 'authentication')


def normalize_response(response: Dict[str, Any],
                       *,
                       date_time_format: str) -> None:
    try:
        expiration_date_time_string = response['expires_at']
    except KeyError:
        return

    response['expires_at'] = datetime.strptime(expiration_date_time_string,
                                               date_time_format)
