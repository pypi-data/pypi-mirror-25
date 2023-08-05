#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'bitex', 'gspread', 'oauth2client', 'coinbase',
]

proj_version='0.1.0'

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]

setup(
    name='cryptohands',
    version=proj_version,
    description="For making Crypto Pizza",
    long_description=readme + '\n\n' + history,
    author="Daniel Chaffelson",
    author_email='chaffelson@gmail.com',
    url='https://github.com/chaffelson/cryptohands',
    packages=find_packages(include=['cryptohands']),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'tox',
            'sphinx',
            'sphinx_rtd_theme',
            'bumpversion'
        ]
    },
    license="Apache Software License 2.0",
    download_url='https://github.com/Chaffelson/cryptohands/archive/' + proj_version + '.tar.gz',
    zip_safe=False,
    keywords=['cryptohands', 'bitcoin', 'ethereum', 'bitfinex', 'poloniex', 'bittrex', 'coinbase', 'api', 'wrapper'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
