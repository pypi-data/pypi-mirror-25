import operator
from contextlib import suppress
from datetime import (datetime,
                      timedelta)
from itertools import chain
from typing import (Any,
                    Iterable,
                    Dict)

from aiohttp import ClientSession

from asynctmdb import requests
from asynctmdb.common import (DATE_FORMAT,
                              TIME_FORMAT,
                              DATE_TIME_FORMAT)
from asynctmdb.config import API_BASE_URL
from asynctmdb.utils import urljoin

MAX_TIME_RANGE_LENGTH = timedelta(days=14)
RELEASE_DATE_TIME_FORMAT = f'{DATE_FORMAT}T{TIME_FORMAT}.%fZ'
NOW_PLAYING_DATES_KEYS = ['minimum', 'maximum']


async def details(movie_id: int,
                  *,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  language: str = None,
                  session: ClientSession) -> Dict[str, Any]:
    method_url = base_method_url(api_base_url, movie_id)

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def account_states(movie_id: int,
                         *,
                         api_base_url: str = API_BASE_URL,
                         api_key: str,
                         session_id: str,
                         session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'account_states')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  session_id=session_id)
    return response


async def alternative_titles(movie_id: int,
                             *,
                             api_base_url: str = API_BASE_URL,
                             api_key: str,
                             country: str = None,
                             session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'alternative_titles')

    params = {}
    if country is not None:
        params['country'] = country

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def changes(movie_id: int,
                  *,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  start_date: datetime = None,
                  end_date: datetime = None,
                  page: int = None,
                  session: ClientSession,
                  format_string: str = DATE_TIME_FORMAT) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'changes')

    if start_date is not None and end_date is not None:
        if end_date - start_date > MAX_TIME_RANGE_LENGTH:
            err_msg = ('Invalid date range: '
                       'should be a range no longer '
                       f'than {MAX_TIME_RANGE_LENGTH.days} days.')
            raise ValueError(err_msg)

    params = {}
    if start_date is not None:
        params['start_date'] = start_date.strftime(format_string)
    if end_date is not None:
        params['end_date'] = end_date.strftime(format_string)
    if page is not None:
        params['page'] = page

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    normalize_changes(response,
                      format_string=format_string)
    return response


async def credits(movie_id: int,
                  *,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'credits')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key)
    return response


async def images(movie_id: int,
                 *,
                 api_base_url: str = API_BASE_URL,
                 api_key: str,
                 language: str = None,
                 session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'images')

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def keywords(movie_id: int,
                   *,
                   api_base_url: str = API_BASE_URL,
                   api_key: str,
                   session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'keywords')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key)
    return response


async def release_dates(movie_id: int,
                        *,
                        api_base_url: str = API_BASE_URL,
                        api_key: str,
                        session: ClientSession,
                        format_string: str = RELEASE_DATE_TIME_FORMAT
                        ) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'release_dates')
    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key)
    normalize_release_dates(response,
                            format_string=format_string)
    return response


async def videos(movie_id: int,
                 *,
                 api_base_url: str = API_BASE_URL,
                 api_key: str,
                 language: str = None,
                 session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'videos')

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def translations(movie_id: int,
                       *,
                       api_base_url: str = API_BASE_URL,
                       api_key: str,
                       session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'translations')

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key)
    return response


async def recommendations(movie_id: int,
                          *,
                          api_base_url: str = API_BASE_URL,
                          api_key: str,
                          language: str = None,
                          page: int = None,
                          session: ClientSession,
                          format_string: str = DATE_FORMAT) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'recommendations')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    normalize_recommendations(response,
                              format_string=format_string)
    return response


async def similar(movie_id: int,
                  *,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  language: str = None,
                  page: int = None,
                  session: ClientSession,
                  format_string: str = DATE_FORMAT) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'similar')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    normalize_similar(response,
                      format_string=format_string)
    return response


async def reviews(movie_id: int,
                  *,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  language: str = None,
                  page: int = None,
                  session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'reviews')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def lists(movie_id: int,
                *,
                api_base_url: str = API_BASE_URL,
                api_key: str,
                language: str = None,
                page: int = None,
                session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'lists')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def rate(movie_id: int,
               *,
               rating: float,
               api_base_url: str = API_BASE_URL,
               api_key: str,
               guest_session_id: str = None,
               session_id: str = None,
               session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'rating')

    params = {}
    if guest_session_id is not None:
        params['guest_session_id'] = guest_session_id
    if session_id is not None:
        params['session_id'] = session_id

    response = await requests.post(method_url=method_url,
                                   session=session,
                                   api_key=api_key,
                                   **params,
                                   json_body={'value': rating})
    return response


async def delete_rating(movie_id: int,
                        *,
                        api_base_url: str = API_BASE_URL,
                        api_key: str,
                        guest_session_id: str = None,
                        session_id: str = None,
                        session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'rating')

    params = {}
    if guest_session_id is not None:
        params['guest_session_id'] = guest_session_id
    if session_id is not None:
        params['session_id'] = session_id

    response = await requests.delete(method_url=method_url,
                                     session=session,
                                     api_key=api_key,
                                     **params)
    return response


async def latest(*,
                 api_base_url: str = API_BASE_URL,
                 api_key: str,
                 language: str = None,
                 session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(api_base_url, 'movie', 'latest')

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def now_playing(*,
                      api_base_url: str = API_BASE_URL,
                      api_key: str,
                      language: str = None,
                      page: int = None,
                      region: str = None,
                      session: ClientSession,
                      format_string: str = DATE_FORMAT,
                      dates_keys: Iterable[str] = NOW_PLAYING_DATES_KEYS
                      ) -> Dict[str, Any]:
    method_url = urljoin(api_base_url, 'movie', 'now_playing')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page
    if region is not None:
        params['region'] = region

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    normalize_now_playing(response,
                          dates_keys=dates_keys,
                          format_string=format_string)
    return response


async def popular(*,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  language: str = None,
                  page: int = None,
                  region: str = None,
                  session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(api_base_url, 'movie', 'popular')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page
    if region is not None:
        params['region'] = region

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def top_rated(*,
                    api_base_url: str = API_BASE_URL,
                    api_key: str,
                    language: str = None,
                    page: int = None,
                    region: str = None,
                    session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(api_base_url, 'movie', 'top_rated')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page
    if region is not None:
        params['region'] = region

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


async def upcoming(*,
                   api_base_url: str = API_BASE_URL,
                   api_key: str,
                   language: str = None,
                   page: int = None,
                   region: str = None,
                   session: ClientSession) -> Dict[str, Any]:
    method_url = urljoin(api_base_url, 'movie', 'upcoming')

    params = {}
    if language is not None:
        params['language'] = language
    if page is not None:
        params['page'] = page
    if region is not None:
        params['region'] = region

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response


def base_method_url(api_base_url: str,
                    movie_id: int) -> str:
    return urljoin(api_base_url, 'movie', str(movie_id))


items_record = operator.itemgetter('items')


def normalize_changes(response: Dict[str, Any],
                      *,
                      format_string: str) -> None:
    try:
        results = response['changes']
    except KeyError:
        return
    records = chain.from_iterable(map(items_record, results))
    for record in records:
        record['time'] = datetime.strptime(record['time'],
                                           format_string)


release_dates_record = operator.itemgetter('release_dates')


def normalize_release_dates(response: Dict[str, Any],
                            *,
                            format_string: str) -> None:
    try:
        results = response['results']
    except KeyError:
        return

    records = chain.from_iterable(map(release_dates_record, results))
    for record in records:
        record['release_date'] = datetime.strptime(record['release_date'],
                                                   format_string)


def normalize_recommendations(response: Dict[str, Any],
                              *,
                              format_string: str) -> None:
    try:
        results = response['results']
    except KeyError:
        return

    for result in results:
        with suppress(TypeError):
            result['release_date'] = (datetime.strptime(result['release_date'],
                                                        format_string)
                                      .date())


normalize_similar = normalize_recommendations


def normalize_now_playing(response: Dict[str, Any],
                          *,
                          format_string: str,
                          dates_keys: Iterable[str]
                          ) -> None:
    try:
        dates = response['dates']
    except KeyError:
        return

    for key in dates_keys:
        dates[key] = (datetime.strptime(dates[key],
                                        format_string)
                      .date())
