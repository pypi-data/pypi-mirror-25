import os
import string

from hypothesis import strategies

from asynctmdb.utils import urljoin

api_base_url = urljoin(os.environ['API.BaseURL'],
                       os.environ['API.Version'])
api_key = os.environ['API.Key']

api_base_urls = strategies.just(api_base_url)
api_keys = strategies.just(api_key)
non_heximal_digits_characters = strategies.characters(
        blacklist_characters=string.hexdigits)
invalid_api_keys = strategies.text(alphabet=non_heximal_digits_characters)
