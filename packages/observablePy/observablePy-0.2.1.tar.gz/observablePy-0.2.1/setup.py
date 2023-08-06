"""
Publish a new version:
Change version in package __init__ file
Change version in this setup file
pull __init__ and setup
Execute:
$ git tag X.Y.Z -m "Release X.Y.Z"
$ git push --tags
$ pip install --upgrade twine wheel
$ python setup.py sdist bdist_wheel --universal
$ twine upload dist/*
"""
import codecs
import os
import sys
from setuptools import setup, find_packages


NAME = 'observablePy'
GITHUB_NAME = 'ObservablePy'
VERSION = '0.2.1'
DOWNLOAD_URL = (
    'https://github.com/fredericklussier/' + GITHUB_NAME + '/' + VERSION
)


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, 'r', 'utf8') as f:
        return f.read()


setup(
    name=NAME,
    packages=[NAME],
    version=VERSION,
    description='Enable observable behavior.',
    long_description=read_file('ReadMe.rst'),
    license='MIT',
    author='Frederick Lussier',
    author_email='frederick.lussier@hotmail.com',
    url='https://github.com/fredericklussier/' + GITHUB_NAME,
    download_url=DOWNLOAD_URL,
    keywords=[
        'observable', 'observer', 'observer-pattern'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
    ],
)
