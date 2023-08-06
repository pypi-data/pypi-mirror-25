#!/usr/bin/env python

"""Setup script for np."""

import setuptools
import os

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()
    
with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setuptools.setup(
    name="np",
    version='1.0.1',
    description="np = numpy++: numpy with added convenience functionality",
    url='https://github.com/k7hoven/np',
    author='Koos Zevenhoven',
    author_email='koos.zevenhoven@aalto.fi',
    packages=setuptools.find_packages(exclude = ('tests',)),
    long_description=(README + '\n' + CHANGES),
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    install_requires = REQUIREMENTS,
)

