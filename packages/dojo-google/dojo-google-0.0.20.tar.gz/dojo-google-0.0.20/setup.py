#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='dojo-google',
    version='0.0.20',
    description='Dojo transforms using Google APIs.',
    author='Data Up',
    author_email='dojo@dataup.me',
    url='https://dojo.dataup.me/',
    packages=find_packages(exclude=['tests', '.cache', '.venv', '.git', 'dist']),
    install_requires=[
        'dojo',
        'google-api-python-client',
        'retrying'
    ]
)
