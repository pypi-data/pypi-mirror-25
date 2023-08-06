#!/usr/bin/env python
# coding=utf-8
# :bc: Not importing unicode_literals because in Python 2 distutils,
# some values are expected to be byte strings.
from __future__ import absolute_import, division, print_function

from codecs import StreamReader, open

from setuptools import Extension, setup

##
# Load long description for PyPi.
with open('README.rst', 'r', 'utf-8') as f: # type: StreamReader
  long_description = f.read()

setup(
  name        = 'PyOTA-CCurl',
  description = 'C Curl extension for PyOTA',
  url         = 'https://github.com/todofixthis/pyota-ccurl',
  version     = '1.0.9',

  long_description = long_description,

  py_modules = ['pyota_ccurl'],
  ext_modules = [Extension('ccurl', ['src/ccurlmodule.c'])],

  entry_points = {
    'console_scripts': [
      'check_ccurl = pyota_ccurl:check_installation',
    ],
  },

  install_requires = ['pyota'],

  tests_require = ['nose'],
  test_suite    = 'test',
  test_loader   = 'nose.loader:TestLoader',

  license = 'MIT',

  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],

  keywords =
    'iota,tangle,iot,internet of things,api,library,cryptocurrency,'
    'balanced ternary',

  author        = 'Phoenix Zerin',
  author_email  = 'phx@phx.ph',
)
