#!/usr/bin/env python

import os
from distutils.core import setup
from setuptools import find_packages

__name__ = 'osc-plugin-clone'

setup(
    name = __name__,
    version = '20170913.0',
    author = 'Andrew Shadura',
    author_email = 'andrew.shadura@collabora.co.uk',
    url = 'https://gitlab.collabora.com/andrewsh/osc-plugin-clone',
    description = 'OSC plugin for cloning projects and forking distributions',
    license = 'GPL-2+',
    packages = find_packages(exclude=['*test*']),
    test_suite="tests",
    install_requires = ["osc >= 0.150"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools'
    ],
    data_files = [
        (os.path.join('lib', 'osc-plugins'), ['clone.py']),
    ]
)

