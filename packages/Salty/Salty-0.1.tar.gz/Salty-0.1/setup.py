#!/usr/bin/env python
import sys
from setuptools import find_packages, setup


MIN_PYTHON = (3, 4)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


setup(
    name='Salty',
    version='0.1',
    description='Password management tool',
    author='Mark garcia Sastre',
    author_email='markcial@gmail.com',
    url='https://github.com/markcial/salty',
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    install_requires=['pynacl'],
    entry_points={
       'console_scripts': [
           'salty = salty.__main__:main'
       ]
    }
)