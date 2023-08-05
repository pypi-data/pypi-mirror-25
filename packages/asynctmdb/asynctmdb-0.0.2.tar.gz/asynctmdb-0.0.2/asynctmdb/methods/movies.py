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
RELEASE_DATE_TIME_FORMAT = ('{date_format}T{time_format}.%fZ'
                            .format(date_format=DATE_FORMAT,
                                    time_format=TIME_FORMAT))
NOW_PLAYING_DATES_KEYS = ['minimum', 'maximum']


async def details(movie_id: int,
                  *,
                  api_base_url: str = API_BASE_URL,
                  api_key: str,
                  language: str = None,
                  append_to_response: str = None,
                  session: ClientSession) -> Dict[str, Any]:
    """
    Get the primary information about a movie.

    Supports ``append_to_response``.
    Read more about this :getting-started:`here <append-to-response>`.

    More info at :movies:`TMDb docs <get-movie-details>`.
    """
    method_url = base_method_url(api_base_url, movie_id)

    params = {}
    if language is not None:
        params['language'] = language
    if append_to_response is not None:
        params['append_to_response'] = append_to_response

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
    """
    Grab the following account states for a session:

      - Movie rating
      - If it belongs to your watchlist
      - If it belongs to your favourite list

    More info at :movies:`TMDb docs <get-movie-account-states>`.
    """
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
    """
    Get all of the alternative titles for a movie.

    More info at :movies:`TMDb docs <get-movie-alternative-titles>`.
    """
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
    """
    Get the changes for a movie.

    By default only the last 24 hours are returned.

    You can query up to 14 days in a single query by using the ``start_date``
    and ``end_date`` query parameters.

    More info at :movies:`TMDb docs <get-movie-changes>`.
    """
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'changes')

    if start_date is not None and end_date is not None:
        if end_date - start_date > MAX_TIME_RANGE_LENGTH:
            err_msg = ('Invalid date range: '
                       'should be a range no longer '
                       'than {days_count} days.'
                       .format(days_count=MAX_TIME_RANGE_LENGTH.days))
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
    """
    Get the cast and crew for a movie.

    More info at :movies:`TMDb docs <get-movie-credits>`.
    """
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
                 include_image_language: str = None,
                 session: ClientSession) -> Dict[str, Any]:
    """
    Get the images that belong to a movie.

    Querying images with a ``language`` parameter will filter the results.

    If you want to include a fallback language
    (especially useful for backdrops)
    you can use the ``include_image_language`` parameter.
    This should be a comma seperated value like so::

        include_image_language="en,null"

    More info at :movies:`TMDb docs <get-movie-images>`.
    """
    method_url = urljoin(base_method_url(api_base_url, movie_id),
                         'images')

    params = {}
    if language is not None:
        params['language'] = language
    if include_image_language is not None:
        params['include_image_language'] = include_image_language

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
    """
    Get the keywords that have been added to a movie.

    More info at :movies:`TMDb docs <get-movie-keywords>`.
    """
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
    """
    Get the release date along with the certification for a movie.

    Release dates support different types:

        1. Premiere
        2. Theatrical (limited)
        3. Theatrical
        4. Digital
        5. Physical
        6. TV

    More info at :movies:`TMDb docs <get-movie-release-dates>`.
    """
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
    """
    Get the videos that have been added to a movie.

    More info at :movies:`TMDb docs <get-movie-videos>`.
    """
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
    """
    Get a list of translations that have been created for a movie.

    More info at :movies:`TMDb docs <get-movie-translations>`.
    """
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
    """
    Get a list of recommended movies for a movie.

    More info at :movies:`TMDb docs <get-movie-recommendations>`.
    """
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
    """
    Get a list of similar movies.

    This is **not** the same as the "Recommendation" system
    you see on the website.

    These items are assembled by looking at keywords and genres.

    More info at :movies:`TMDb docs <get-similar-movies>`.
    """
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
    """
    Get the user reviews for a movie.

    More info at :movies:`TMDb docs <get-movie-reviews>`.
    """
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
    """
    Get a list of lists that this movie belongs to.

    More info at :movies:`TMDb docs <get-movie-lists>`.
    """
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
    """
    Rate a movie.

    A valid session or guest session ID is required.
    You can read more about how this works
    :authentication:`here <how-do-i-generate-a-session-id>`.

    More info at :movies:`TMDb docs <rate-movie>`.
    """
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
    """
    Remove your rating for a movie.

    A valid session or guest session ID is required.
    You can read more about how this works
    :authentication:`here <how-do-i-generate-a-session-id>`.

    More info at :movies:`TMDb docs <delete-movie-rating>`.
    """
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
    """
    Get the most newly created movie.

    This is a live response and will continuously change.

    More info at :movies:`TMDb docs <>`.
    """
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
    """
    Get a list of movies in theatres.

    This is a release type query that looks for all movies
    that have a release type of 2 or 3 within the specified date range.

    You can optionally specify a ``region`` parameter
    which will narrow the search to only look
    for theatrical release dates within the specified country.

    More info at :movies:`TMDb docs <get-now-playing>`.
    """
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
    """
    Get a list of the current popular movies on TMDb.

    This list updates daily.

    More info at :movies:`TMDb docs <get-popular-movies>`.
    """
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
    """
    Get the top rated movies on TMDb.

    More info at :movies:`TMDb docs <get-top-rated-movies>`.
    """
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
    """
    Get a list of upcoming movies in theatres.

    This is a release type query that looks for all movies
    that have a release type of 2 or 3 within the specified date range.

    You can optionally specify a region parameter
    which will narrow the search to only look for
    theatrical release dates within the specified country.

    More info at :movies:`TMDb docs <get-upcoming>`.
    """
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
