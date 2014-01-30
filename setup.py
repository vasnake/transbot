#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright (c) Valentin Fedulov <vasnake@gmail.com>
# See COPYING for details.

from setuptools import setup

with open('README.rst', 'r') as infile:
    long_description = infile.read()

setup(
    name = 'translitbot',
    description = "XMPP chat bot for translit service",
    long_description = long_description,
    keywords = "XMPP GTalk chat bot translit",
    url = 'https://github.com/vasnake/transbot',
    download_url = 'https://github.com/vasnake/transbot/archive/master.zip',
    version = "0.1.2",
    license = 'GPLv3',
    author = "Valentin Fedulov",
    author_email='vasnake@gmail.com',
    packages = ['translitbot'],
    scripts = [],
    install_requires = ['dnspython', 'trans', 'xmpppy'],
    classifiers = [ # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: Freeware',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities'
    ],
    zip_safe = False
)
