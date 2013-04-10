# coding: utf8

from distutils.core import setup
import enc

long_description = open('README.rst', 'r').read()
description = 'Russian transliteration module'

setup(
        name='enc',
        version=enc.__version__,
        description=description,
        long_description=long_description,
        author=enc.__author__,
        author_email='vasnake@gmail.com',
        url='https://github.com/vasnake/transbot',
        license='GPL',
        classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',
        ],
        py_modules=['enc'],
)
