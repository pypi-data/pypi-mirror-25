import os

from hypothesis import strategies

users_names = strategies.just(os.environ['TMDB_USER_NAME'])
users_passwords = strategies.just(os.environ['TMDB_USER_PASSWORD'])
