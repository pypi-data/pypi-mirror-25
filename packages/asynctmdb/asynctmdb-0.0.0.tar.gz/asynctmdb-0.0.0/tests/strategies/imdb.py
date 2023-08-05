import string

from hypothesis import strategies

invalid_imdb_ids_characters = strategies.characters(
        blacklist_characters='t' + string.digits)
invalid_imdb_ids = strategies.text(alphabet=invalid_imdb_ids_characters)
