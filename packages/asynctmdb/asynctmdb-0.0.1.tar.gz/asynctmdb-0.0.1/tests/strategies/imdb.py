import string

from hypothesis import strategies

invalid_imdb_ids_characters = strategies.sampled_from(
        sorted(set(string.printable) - {'t'}))
invalid_imdb_ids = strategies.text(alphabet=invalid_imdb_ids_characters)
