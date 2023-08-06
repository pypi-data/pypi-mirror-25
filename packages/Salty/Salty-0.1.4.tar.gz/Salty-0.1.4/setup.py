#!/usr/bin/env python
import sys
from setuptools import find_packages, setup


# versioning tools
exec(open('salty/version.py').read())

MIN_PYTHON = (3, 4)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


setup(
    name='Salty',
    version=__version__,
    description='Password management tool',
    author='Mark garcia Sastre',
    author_email='markcial@gmail.com',
    url='https://github.com/markcial/salty',
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['pytest', 'coverage'],
    install_requires=['pynacl'],
    entry_points={
       'console_scripts': [
           'salty = salty.__main__:main'
       ]
    }
)