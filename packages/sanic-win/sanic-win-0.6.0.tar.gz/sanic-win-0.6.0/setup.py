"""
sanic-win
"""
import codecs
import os
import re
from distutils.errors import DistutilsPlatformError
from distutils.util import strtobool

from setuptools import setup


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        *paths
    )

    return codecs.open(path, mode, encoding)


with open_local(['sanic', '__init__.py'], encoding='latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


with open_local(['README.rst']) as rm:
    long_description = rm.read()

setup_kwargs = {
    'name': 'sanic-win',
    'version': version,
    'url': 'http://github.com/canfeit/sanic-win/',
    'license': 'MIT',
    'author': 'canfeit',
    'author_email': 'canfeit@qq.com',
    'description': (
        'A microframework based on uvloop, httptools, and learnings of flask'),
    'long_description': long_description,
    'packages': ['sanic'],
    'platforms': 'any',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
}

requirements = [
    'httptools>=0.0.9',
    'aiofiles>=0.3.0',
    'websockets>=3.2',
]

setup_kwargs['install_requires'] = requirements
setup(**setup_kwargs)
