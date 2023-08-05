#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='dojo',
    version='0.0.41',
    description='A framework for building and running your data platform.',
    author='Data Up',
    author_email='dojo@dataup.me',
    url='https://www.dataup.me/',
    packages=find_packages(exclude=['tests', '.cache', '.venv', '.git', 'dist']),
    scripts=[],
    install_requires=[
        'pyyaml',
        'jsonschema',
        'cryptography',
        'python-dateutil',
        'click',
        'contextdecorator',
    ],
    entry_points='''
        [console_scripts]
        dojo=dojo.cli:cli
    ''',
)
