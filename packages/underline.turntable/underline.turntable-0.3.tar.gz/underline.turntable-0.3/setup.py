#!/usr/bin/python3

from setuptools import setup, find_packages

setup(name = "underline.turntable",
      version = "0.3",
      description = "Speed and direction control of turntable.",

      author = "",
      author_email = "",
      maintainer = "Yeison Cardona",
      maintainer_email = "yeisoneng@gmail.com",

      url = "http://yeisoncardona.com",
      download_url = "",

      license = "GPLv3",
      keywords = "Raspberry Pi 3, Stepper motor",

      #list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Environment :: X11 Applications',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: System :: Hardware',
                   ],

                   packages = find_packages(),
      include_package_data = True,

      install_requires = ['RPi.GPIO',
                          ],
      #scripts = [
          #"cmd/command",
                 #],

      zip_safe = False,

      )
