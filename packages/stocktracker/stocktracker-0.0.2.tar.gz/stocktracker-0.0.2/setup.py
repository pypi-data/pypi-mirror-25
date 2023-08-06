#!/usr/bin/env python2

from setuptools import setup

setup(
    name='stocktracker',
    version='0.0.2',
    description='stocktracker',
    author='Michael Giuffrida',
    author_email='michaelg@michaelg.us',
    url='https://github.com/mgiuffrida/stocktracker',
    license='MIT',
    packages=['stocktracker'],
    extras_require={
        'dev': [
            'pep8',
            'pylint',
        ]
    },
)
