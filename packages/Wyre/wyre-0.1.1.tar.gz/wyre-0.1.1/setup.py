#!/usr/bin/env python

from distutils.core import setup

import wyre

setup(
    name='wyre',
    version=wyre.__version__,
    description='Lightweight dependency injection for pure OOP.',
    author='Abel André',
    author_email='abel.andre.87@gmail.com',
    url='https://gitlab.com/blndr/wyre',
    packages=['wyre'],
    keywords=[
        'dependency',
        'injection',
        'injector',
        'inject',
        'decorator',
        'dependency injection'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
