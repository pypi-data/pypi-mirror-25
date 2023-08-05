import os

from hypothesis import strategies

users_names = strategies.just(os.environ['TMDb.User.Name'])
users_passwords = strategies.just(os.environ['TMDb.User.Password'])
