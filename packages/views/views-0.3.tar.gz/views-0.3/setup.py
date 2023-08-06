#!/usr/bin/env python3

"""Setup script for the views module."""

import setuptools
import os

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()
    
setuptools.setup(
    name="views",
    version='0.3',
    description="views",
    url='https://github.com/k7hoven/views',
    author='Koos Zevenhoven',
    author_email='koos.zevenhoven@aalto.fi',
    packages=setuptools.find_packages(),
    py_modules=['views'],
    long_description=(README + '\n' + CHANGES),
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)

