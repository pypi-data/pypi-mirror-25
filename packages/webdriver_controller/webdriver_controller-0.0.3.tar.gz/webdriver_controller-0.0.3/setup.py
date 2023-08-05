#!/usr/bin/env python3
from setuptools import setup
from setuptools import find_packages

import webdriver_controller

setup_args = {
    'name': 'webdriver_controller',
    'packages': find_packages(exclude=['tests']),
    'scripts': ['bin/webdriver_controller'],
    'version': webdriver_controller.__version__,
    'description': 'a tool manages local Selenium Webdriver installation',
    'long_description': '''
        A tool manages local Selenium Webdriver installation. It is inspired by Angular team's webdriver-manager package. Details on https://github.com/lcmtwn/webdriver_controller.
    ''',
    'author': 'lcmtwn',
    'author_email': 'lcmtwn@gmail.com',
    'url': 'https://github.com/lcmtwn/webdriver_controller',
    'classifiers': [
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing'
    ],
    'install_requires': [
        'aiohttp',
        'requests',
        'xmltodict'
    ]
}

setup(**setup_args)
