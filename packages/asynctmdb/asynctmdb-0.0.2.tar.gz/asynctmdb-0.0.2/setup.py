from setuptools import (setup,
                        find_packages)

import asynctmdb
from asynctmdb.config import PROJECT_NAME
from asynctmdb.utils import urljoin

project_base_url = 'https://github.com/lycantropos/asynctmdb'
setup(name=PROJECT_NAME,
      version=asynctmdb.__version__,
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=urljoin(project_base_url, 'archive/master.tar.gz'),
      description=asynctmdb.__doc__,
      long_description=open('README.rst').read(),
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: AsyncIO',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Internet :: WWW/HTTP',
      ],
      packages=find_packages(exclude=('tests',)),
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
