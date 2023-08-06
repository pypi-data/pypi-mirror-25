#!/usr/bin/env python

import sys
from setuptools import setup

install_requires = [
    "catsql >= 0.4.1"
]

if sys.version_info[0] == 2:
    install_requires.append('unicodecsv')

setup(name="nanosql",
      version="0.1.1",
      author="Paul Fitzpatrick",
      author_email="paulfitz@alum.mit.edu",
      description="Edit a slice of a SQL database in nano",
      packages=['nanosql'],
      entry_points={
          "console_scripts": [
              "nanosql=nanosql.main:main"
          ]
      },
      install_requires=install_requires,
      url="https://github.com/paulfitz/nanosql"
)
