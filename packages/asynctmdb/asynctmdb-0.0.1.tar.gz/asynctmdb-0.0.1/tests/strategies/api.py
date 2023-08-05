import os
import string

from hypothesis import strategies

from asynctmdb.config import API_BASE_URL

api_key = os.environ['TMDb.API.Key']
api_base_urls = strategies.just(API_BASE_URL)
api_keys = strategies.just(api_key)
non_heximal_digits_characters = strategies.characters(
        blacklist_characters=string.hexdigits)
invalid_api_keys = strategies.text(alphabet=non_heximal_digits_characters)
