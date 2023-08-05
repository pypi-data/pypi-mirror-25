import operator
from datetime import (date,
                      datetime)
from itertools import chain
from typing import Set

import pytest
from aiohttp import ClientSession

from asynctmdb.common import StatusCode
from asynctmdb.methods import movies
from tests.utils import (is_positive_integer,
                         is_non_empty_string,
                         is_valid_paginated_record,
                         are_valid_results)


@pytest.mark.asyncio
async def test_movie_details(movie_id: int,
                             nonexistent_movie_id: int,
                             min_movie_id: int,
                             imdb_id: str,
                             api_base_url: str,
                             api_key: str,
                             invalid_api_key: str,
                             session: ClientSession) -> None:
    record = await movies.details(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)
    invalid_api_key_response = await movies.details(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.details(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    record_imdb_id = record['imdb_id']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert record_imdb_id == imdb_id
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_account_movie_states(movie_id: int,
                                    min_movie_id: int,
                                    api_base_url: str,
                                    api_key: str,
                                    invalid_api_key: str,
                                    session_id: str,
                                    invalid_session_id: str,
                                    session: ClientSession) -> None:
    record = await movies.account_states(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session_id=session_id,
            session=session)
    invalid_api_key_response = await movies.account_states(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session_id=session_id,
            session=session)
    invalid_session_response = await movies.account_states(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session_id=invalid_session_id,
            session=session)

    record_id = record['id']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    invalid_session_status_code = invalid_session_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert invalid_session_status_code == StatusCode.AUTHENTICATION_FAILED


@pytest.mark.asyncio
async def test_movie_alternative_titles(movie_id: int,
                                        nonexistent_movie_id: int,
                                        min_movie_id: int,
                                        api_base_url: str,
                                        api_key: str,
                                        invalid_api_key: str,
                                        session: ClientSession) -> None:
    record = await movies.alternative_titles(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)
    invalid_api_key_response = await movies.alternative_titles(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.alternative_titles(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    record_titles = map(operator.itemgetter('title'), record['titles'])
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert all(map(is_non_empty_string, record_titles))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_changes(movie_id: int,
                             nonexistent_movie_id: int,
                             movie_changes_start_date: datetime,
                             movie_changes_end_date: datetime,
                             page_number: int,
                             invalid_page_number: int,
                             api_base_url: str,
                             api_key: str,
                             invalid_api_key: str,
                             tmdb_foundation_date: date,
                             session: ClientSession) -> None:
    empty_interval_record = await movies.changes(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            start_date=datetime.max,
            end_date=datetime.min,
            page=page_number,
            session=session)
    nonexistent_movie_record = await movies.changes(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            start_date=movie_changes_start_date,
            end_date=movie_changes_end_date,
            page=page_number,
            session=session)
    record = await movies.changes(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            start_date=movie_changes_start_date,
            end_date=movie_changes_end_date,
            page=page_number,
            session=session)
    invalid_api_key_response = await movies.changes(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            start_date=movie_changes_start_date,
            end_date=movie_changes_end_date,
            page=page_number,
            session=session)
    invalid_page_response = await movies.changes(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            start_date=movie_changes_start_date,
            end_date=movie_changes_end_date,
            page=invalid_page_number,
            session=session)

    empty_interval_results = empty_interval_record['changes']
    nonexistent_movie_results = nonexistent_movie_record['changes']
    results = record['changes']
    items = chain.from_iterable(map(operator.itemgetter('items'),
                                    results))
    changes_times = map(operator.itemgetter('time'), items)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    invalid_page_status_code = invalid_page_response['status_code']

    assert isinstance(empty_interval_record, dict)
    assert isinstance(nonexistent_movie_record, dict)
    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert (isinstance(empty_interval_results, list) and
            not empty_interval_results)
    assert (isinstance(nonexistent_movie_results, list) and
            not nonexistent_movie_results)
    assert are_valid_results(results)
    assert all(isinstance(change_time, datetime) and
               change_time.date() > tmdb_foundation_date
               for change_time in changes_times)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert invalid_page_status_code == StatusCode.INVALID_PAGE


@pytest.mark.asyncio
async def test_movie_credits(movie_id: int,
                             nonexistent_movie_id: int,
                             min_movie_id: int,
                             api_base_url: str,
                             api_key: str,
                             invalid_api_key: str,
                             session: ClientSession) -> None:
    record = await movies.credits(movie_id,
                                  api_base_url=api_base_url,
                                  api_key=api_key,
                                  session=session)
    invalid_api_key_response = await movies.credits(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.credits(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    staff_records = record['cast'] + record['crew']
    staff_records_ids = map(operator.itemgetter('id'), staff_records)
    staff_records_names = map(operator.itemgetter('name'), staff_records)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert isinstance(staff_records, list)
    assert all(map(is_positive_integer, staff_records_ids))
    assert all(map(is_non_empty_string, staff_records_names))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_images(movie_id: int,
                            nonexistent_movie_id: int,
                            min_movie_id: int,
                            api_base_url: str,
                            api_key: str,
                            invalid_api_key: str,
                            session: ClientSession) -> None:
    record = await movies.images(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)
    invalid_api_key_response = await movies.images(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.images(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    results = record['backdrops']
    backdrops_records_heights = map(operator.itemgetter('height'),
                                    results)
    backdrops_records_widths = map(operator.itemgetter('width'),
                                   results)
    backdrops_records_files_paths = map(operator.itemgetter('file_path'),
                                        results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    assert all(map(is_positive_integer, backdrops_records_heights))
    assert all(map(is_positive_integer, backdrops_records_widths))
    assert all(map(is_non_empty_string, backdrops_records_files_paths))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_keywords(movie_id: int,
                              nonexistent_movie_id: int,
                              min_movie_id: int,
                              api_base_url: str,
                              api_key: str,
                              invalid_api_key: str,
                              session: ClientSession) -> None:
    record = await movies.keywords(movie_id,
                                   api_base_url=api_base_url,
                                   api_key=api_key,
                                   session=session)
    invalid_api_key_response = await movies.keywords(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.keywords(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    results = record['keywords']
    keywords_records_ids = map(operator.itemgetter('id'),
                               results)
    keywords_records_names = map(operator.itemgetter('name'),
                                 results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    assert all(map(is_positive_integer, keywords_records_ids))
    assert all(map(is_non_empty_string, keywords_records_names))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_release_dates(movie_id: int,
                                   nonexistent_movie_id: int,
                                   min_movie_id: int,
                                   min_movie_release_date: date,
                                   api_base_url: str,
                                   api_key: str,
                                   invalid_api_key: str,
                                   session: ClientSession) -> None:
    record = await movies.release_dates(movie_id,
                                        api_base_url=api_base_url,
                                        api_key=api_key,
                                        session=session)
    invalid_api_key_response = await movies.release_dates(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.release_dates(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    results = record['results']
    release_dates_records = chain.from_iterable(
            map(movies.release_dates_record, results))
    release_dates = map(operator.itemgetter('release_date'),
                        release_dates_records)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    assert all(min_movie_release_date <= release_date.date()
               for release_date in release_dates)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_videos(movie_id: int,
                            nonexistent_movie_id: int,
                            min_movie_id: int,
                            movie_videos_sites: Set[str],
                            api_base_url: str,
                            api_key: str,
                            invalid_api_key: str,
                            session: ClientSession) -> None:
    record = await movies.videos(movie_id,
                                 api_base_url=api_base_url,
                                 api_key=api_key,
                                 session=session)
    invalid_api_key_response = await movies.videos(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.videos(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    results = record['results']
    sites = map(operator.itemgetter('site'), results)
    sizes = map(operator.itemgetter('size'), results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    assert all(site in movie_videos_sites
               for site in sites)
    assert all(map(is_positive_integer, sizes))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_translations(movie_id: int,
                                  nonexistent_movie_id: int,
                                  min_movie_id: int,
                                  api_base_url: str,
                                  api_key: str,
                                  invalid_api_key: str,
                                  session: ClientSession) -> None:
    record = await movies.translations(movie_id,
                                       api_base_url=api_base_url,
                                       api_key=api_key,
                                       session=session)
    invalid_api_key_response = await movies.translations(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)
    nonexistent_movie_response = await movies.translations(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)

    record_id = record['id']
    results = record['translations']
    names = map(operator.itemgetter('name'), results)
    english_names = map(operator.itemgetter('english_name'),
                        results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    # there are cases with empty string ``name``,
    # e.g. ``movie_id`` 278035
    assert all(isinstance(name, str)
               for name in names)
    assert all(map(is_non_empty_string, english_names))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_movie_recommendations(movie_id: int,
                                     nonexistent_movie_id: int,
                                     page_number: int,
                                     invalid_page_number: int,
                                     min_movie_release_date: date,
                                     api_base_url: str,
                                     api_key: str,
                                     invalid_api_key: str,
                                     session: ClientSession) -> None:
    record = await movies.recommendations(movie_id,
                                          api_base_url=api_base_url,
                                          api_key=api_key,
                                          page=page_number,
                                          session=session)
    invalid_api_key_response = await movies.recommendations(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    nonexistent_movie_response = await movies.recommendations(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.recommendations(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    results = record['results']
    release_dates = map(operator.itemgetter('release_date'), results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']
    invalid_page_status_code = invalid_page_response['status_code']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert are_valid_results(results)
    assert all(release_date is None or
               isinstance(release_date, date) and
               release_date > min_movie_release_date
               for release_date in release_dates)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.INTERNAL_ERROR
    assert invalid_page_status_code == StatusCode.INVALID_PAGE


@pytest.mark.asyncio
async def test_similar_movies(movie_id: int,
                              nonexistent_movie_id: int,
                              page_number: int,
                              invalid_page_number: int,
                              min_movie_release_date: date,
                              api_base_url: str,
                              api_key: str,
                              invalid_api_key: str,
                              session: ClientSession) -> None:
    record = await movies.similar(movie_id,
                                  api_base_url=api_base_url,
                                  api_key=api_key,
                                  page=page_number,
                                  session=session)
    invalid_api_key_response = await movies.similar(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    nonexistent_movie_response = await movies.similar(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.similar(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    results = record['results']
    release_dates = map(operator.itemgetter('release_date'), results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']
    invalid_page_status_code = invalid_page_response['status_code']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert are_valid_results(results)
    assert all(release_date is None or
               isinstance(release_date, date) and
               release_date > min_movie_release_date
               for release_date in release_dates)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND
    assert invalid_page_status_code == StatusCode.INVALID_PAGE


@pytest.mark.asyncio
async def test_movie_reviews(movie_id: int,
                             nonexistent_movie_id: int,
                             min_movie_id: int,
                             page_number: int,
                             invalid_page_number: int,
                             api_base_url: str,
                             api_key: str,
                             invalid_api_key: str,
                             session: ClientSession) -> None:
    record = await movies.reviews(movie_id,
                                  api_base_url=api_base_url,
                                  api_key=api_key,
                                  page=page_number,
                                  session=session)
    invalid_api_key_response = await movies.reviews(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    nonexistent_movie_response = await movies.reviews(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.reviews(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    record_id = record['id']
    results = record['results']
    urls = map(operator.itemgetter('url'), results)
    reviews_ids = map(operator.itemgetter('id'), results)
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']
    invalid_page_status_code = invalid_page_response['status_code']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    assert all(url == 'https://www.themoviedb.org/review/{}'.format(review_id)
               for review_id, url in zip(reviews_ids, urls))
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND
    assert invalid_page_status_code == StatusCode.INVALID_PAGE


@pytest.mark.asyncio
async def test_movie_lists(movie_id: int,
                           nonexistent_movie_id: int,
                           min_movie_id: int,
                           page_number: int,
                           invalid_page_number: int,
                           api_base_url: str,
                           api_key: str,
                           invalid_api_key: str,
                           session: ClientSession) -> None:
    record = await movies.lists(movie_id,
                                api_base_url=api_base_url,
                                api_key=api_key,
                                page=page_number,
                                session=session)
    invalid_api_key_response = await movies.lists(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    nonexistent_movie_response = await movies.lists(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.lists(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    record_id = record['id']
    results = record['results']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']
    invalid_page_status_code = invalid_page_response['status_code']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert record_id == movie_id
    assert are_valid_results(results)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert nonexistent_movie_status_code == StatusCode.INTERNAL_ERROR
    assert invalid_page_status_code == StatusCode.INVALID_PAGE


@pytest.mark.asyncio
async def test_rate_movie(movie_id: int,
                          nonexistent_movie_id: int,
                          movie_rating: float,
                          guest_session_id: str,
                          invalid_session_id: str,
                          api_base_url: str,
                          api_key: str,
                          invalid_api_key: str,
                          session: ClientSession) -> None:
    valid_response = await movies.rate(
            movie_id,
            rating=movie_rating,
            api_base_url=api_base_url,
            api_key=api_key,
            guest_session_id=guest_session_id,
            session=session)
    invalid_api_key_response = await movies.rate(
            movie_id,
            rating=movie_rating,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            guest_session_id=guest_session_id,
            session=session)
    invalid_session_response = await movies.rate(
            movie_id,
            rating=movie_rating,
            api_base_url=api_base_url,
            api_key=api_key,
            session_id=invalid_session_id,
            session=session)
    nonexistent_movie_response = await movies.rate(
            nonexistent_movie_id,
            rating=movie_rating,
            api_base_url=api_base_url,
            api_key=api_key,
            guest_session_id=guest_session_id,
            session=session)

    valid_status_code = valid_response['status_code']
    invalid_session_status_code = invalid_session_response['status_code']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(valid_response, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert valid_status_code == StatusCode.SUCCESS
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert invalid_session_status_code == StatusCode.AUTHENTICATION_FAILED
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_rating(movie_id: int,
                             nonexistent_movie_id: int,
                             guest_session_id: str,
                             invalid_session_id: str,
                             api_base_url: str,
                             api_key: str,
                             invalid_api_key: str,
                             session: ClientSession) -> None:
    valid_response = await movies.delete_rating(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            guest_session_id=guest_session_id,
            session=session)
    invalid_api_key_response = await movies.delete_rating(
            movie_id,
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            guest_session_id=guest_session_id,
            session=session)
    invalid_session_response = await movies.delete_rating(
            movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            session_id=invalid_session_id,
            session=session)
    nonexistent_movie_response = await movies.delete_rating(
            nonexistent_movie_id,
            api_base_url=api_base_url,
            api_key=api_key,
            guest_session_id=guest_session_id,
            session=session)

    valid_status_code = valid_response['status_code']
    invalid_session_status_code = invalid_session_response['status_code']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    nonexistent_movie_status_code = nonexistent_movie_response['status_code']

    assert isinstance(valid_response, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(nonexistent_movie_response, dict)
    assert valid_status_code == StatusCode.SUCCESSFULLY_DELETED
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert invalid_session_status_code == StatusCode.AUTHENTICATION_FAILED
    assert nonexistent_movie_status_code == StatusCode.RESOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_latest_movie(min_movie_id: int,
                            api_base_url: str,
                            api_key: str,
                            invalid_api_key: str,
                            session: ClientSession) -> None:
    record = await movies.latest(
            api_base_url=api_base_url,
            api_key=api_key,
            session=session)
    invalid_api_key_response = await movies.latest(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            session=session)

    record_id = record['id']
    invalid_api_key_status_code = invalid_api_key_response['status_code']

    assert isinstance(record, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert is_positive_integer(record_id)
    assert record_id >= min_movie_id
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY


@pytest.mark.asyncio
async def test_now_playing_movies(page_number: int,
                                  invalid_page_number: int,
                                  api_base_url: str,
                                  api_key: str,
                                  invalid_api_key: str,
                                  session: ClientSession) -> None:
    record = await movies.now_playing(
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_api_key_response = await movies.now_playing(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.now_playing(
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    dates = record['dates']
    results = record['results']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    invalid_page_errors = invalid_page_response['errors']

    assert is_valid_paginated_record(record)
    assert isinstance(dates, dict)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert are_valid_results(results)
    assert all(isinstance(dates[key], date)
               for key in movies.NOW_PLAYING_DATES_KEYS)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert (isinstance(invalid_page_errors, list) and
            len(invalid_page_errors) == 1)


@pytest.mark.asyncio
async def test_popular_movies(page_number: int,
                              invalid_page_number: int,
                              api_base_url: str,
                              api_key: str,
                              invalid_api_key: str,
                              session: ClientSession) -> None:
    record = await movies.popular(
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_api_key_response = await movies.popular(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.popular(
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    results = record['results']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    invalid_page_errors = invalid_page_response['errors']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert are_valid_results(results)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert (isinstance(invalid_page_errors, list) and
            len(invalid_page_errors) == 1)


@pytest.mark.asyncio
async def test_top_rated_movies(page_number: int,
                                invalid_page_number: int,
                                api_base_url: str,
                                api_key: str,
                                invalid_api_key: str,
                                session: ClientSession) -> None:
    record = await movies.top_rated(
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_api_key_response = await movies.top_rated(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.top_rated(
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    results = record['results']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    invalid_page_errors = invalid_page_response['errors']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert are_valid_results(results)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert (isinstance(invalid_page_errors, list) and
            len(invalid_page_errors) == 1)


@pytest.mark.asyncio
async def test_upcoming_movies(page_number: int,
                               invalid_page_number: int,
                               api_base_url: str,
                               api_key: str,
                               invalid_api_key: str,
                               session: ClientSession) -> None:
    record = await movies.upcoming(
            api_base_url=api_base_url,
            api_key=api_key,
            page=page_number,
            session=session)
    invalid_api_key_response = await movies.upcoming(
            api_base_url=api_base_url,
            api_key=invalid_api_key,
            page=page_number,
            session=session)
    invalid_page_response = await movies.upcoming(
            api_base_url=api_base_url,
            api_key=api_key,
            page=invalid_page_number,
            session=session)

    results = record['results']
    invalid_api_key_status_code = invalid_api_key_response['status_code']
    invalid_page_errors = invalid_page_response['errors']

    assert is_valid_paginated_record(record)
    assert isinstance(invalid_api_key_response, dict)
    assert isinstance(invalid_page_response, dict)
    assert record['page'] == page_number
    assert are_valid_results(results)
    assert invalid_api_key_status_code == StatusCode.INVALID_API_KEY
    assert (isinstance(invalid_page_errors, list) and
            len(invalid_page_errors) == 1)
