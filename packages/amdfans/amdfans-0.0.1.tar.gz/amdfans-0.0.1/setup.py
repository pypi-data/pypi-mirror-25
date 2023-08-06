#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import amdfans

setup(
  name='amdfans',
  version='0.0.1',
  packages=find_packages(),
  author='Jorrin Pollard',
  author_email='me@jorrinpollard.com',
  description='Command-line program for setting AMD GPU fan speeds',
  url='https://github.com/jorrinpollard/amdfans',
  long_description='README at https://github.com/jorrinpollard/amdfans',
  license='MIT',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
  ],
  keywords=[
  ],
  install_requires=[
    'appdirs',
    'click',
    'ww',
  ],
  entry_points={
    'console_scripts': [
      'amdfans = amdfans.cli:main',
    ],
  },
)