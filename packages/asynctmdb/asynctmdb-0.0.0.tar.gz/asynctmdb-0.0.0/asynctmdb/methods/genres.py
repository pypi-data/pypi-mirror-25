from typing import (Union,
                    Dict,
                    List)

from aiohttp import ClientSession

from asynctmdb import requests
from asynctmdb.utils import urljoin

GenresType = List[Dict[str, Union[int, str]]]


async def movie(*,
                api_base_url: str,
                api_key: str,
                language: str = None,
                session: ClientSession) -> GenresType:
    method_url = urljoin(base_method_url(api_base_url), 'movie/list')

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response['genres']


async def tv(*,
             api_base_url: str,
             api_key: str,
             language: str = None,
             session: ClientSession) -> GenresType:
    method_url = urljoin(base_method_url(api_base_url), 'tv/list')

    params = {}
    if language is not None:
        params['language'] = language

    response = await requests.get(method_url=method_url,
                                  session=session,
                                  api_key=api_key,
                                  **params)
    return response['genres']


def base_method_url(api_base_url: str) -> str:
    return urljoin(api_base_url, 'genre')
