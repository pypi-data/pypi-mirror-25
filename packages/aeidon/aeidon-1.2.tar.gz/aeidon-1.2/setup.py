#! /usr/bin/env python

from setuptools import setup

from aeidon import __version__

setup(name="aeidon",
      version=__version__,
      packages=["aeidon",],
      author="Osmo Salomaa",
      author_email="otsaloma@iki.fi",
      url="https://otsaloma.io/gaupol/",
      license="GPLv3",
      classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Topic :: Multimedia :: Video",
                   "Programming Language :: Python :: 3",]
      )

