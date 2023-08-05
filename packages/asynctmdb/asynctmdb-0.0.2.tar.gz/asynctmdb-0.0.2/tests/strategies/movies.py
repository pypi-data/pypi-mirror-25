from datetime import (time,
                      datetime)
from typing import Iterator

from hypothesis import strategies

from tests.utils import example
from .api import (api_base_urls,
                  api_keys)
from .utils import (TMDB_FOUNDATION_DATE,
                    load_max_movie_id)

MIN_MOVIE_ID = 2
MAX_MOVIE_ID = load_max_movie_id(api_base_url=example(api_base_urls),
                                 api_key=example(api_keys))
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 1000


def ratings(min_movie_rating: float = 0.5,
            max_movie_rating: float = 10.,
            movie_rating_step: float = 0.5) -> Iterator[float]:
    rating = min_movie_rating
    while rating <= max_movie_rating:
        yield rating
        rating += movie_rating_step


movies_ids = strategies.integers(min_value=MIN_MOVIE_ID,
                                 max_value=MAX_MOVIE_ID)
nonexistent_movies_ids = (strategies.integers(max_value=MIN_MOVIE_ID - 1)
                          # we're expecting
                          # that there will be less
                          # than 1_000 new records in TMDb
                          # while tests session is running
                          | strategies.integers(min_value=MAX_MOVIE_ID + 1000))
movies_changes_date_times = strategies.datetimes(
        min_value=datetime.combine(TMDB_FOUNDATION_DATE, time()),
        max_value=datetime.utcnow())
movies_ratings = strategies.sampled_from(list(ratings()))
pages_numbers = strategies.integers(min_value=MIN_PAGE_NUMBER,
                                    max_value=MAX_PAGE_NUMBER)
invalid_pages_numbers = (strategies.integers(max_value=MIN_PAGE_NUMBER - 1)
                         | strategies.integers(min_value=MAX_PAGE_NUMBER + 1))
