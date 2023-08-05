from setuptools import (setup,
                        find_packages)

from asynctmdb.config import PROJECT_NAME

project_base_url = 'https://github.com/lycantropos/asynctmdb/'
setup(name=PROJECT_NAME,
      packages=find_packages(exclude=('tests',)),
      version='0.0.1',
      description='Asynchronous working with TMDB API.',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.tar.gz',
      install_requires=[
          'aiohttp>=2.2.5',  # asynchronous HTTP
      ],
      setup_requires=['pytest-runner>=2.11'],
      tests_require=[
          'pydevd>=1.0.0',  # debugging
          'pytest>=3.0.5',
          'pytest-asyncio>=0.6.0',  # "asyncio" support
          'pytest-cov>=2.4.0',  # coverage
          'hypothesis>=3.13.0',
      ])
