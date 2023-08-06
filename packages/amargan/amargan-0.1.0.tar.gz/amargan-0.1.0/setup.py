#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#     __      ___ ___      __    _ __   __      __      ___
#   /'__`\  /' __` __`\  /'__`\ /\`'__/'_ `\  /'__`\  /' _ `\
#  /\ \L\.\_/\ \/\ \/\ \/\ \L\.\\ \ \/\ \L\ \/\ \L\.\_/\ \/\ \
#  \ \__/.\_\ \_\ \_\ \_\ \__/.\_\ \_\ \____ \ \__/.\_\ \_\ \_\
#   \/__/\/_/\/_/\/_/\/_/\/__/\/_/\/_/\/___L\ \/__/\/_/\/_/\/_/
#                                       /\____/
#                                       \_/__/

"""The setup script."""

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open(os.path.join(here, 'requirements', 'requirements.txt')) as rq_file:
    requirements = [i.strip() for i in rq_file.readlines()]

setup_requirements = [
    'nose',
]

with open(os.path.join(here, 'requirements', 'requirements-test.txt')) as rq_file:
    test_requirements = [i.strip() for i in rq_file.readlines()]
test_requirements.extend(
    [
        'nosetests',
        'nose-cov',
        'nose-parameterized',
    ]
)

setup(
    name='amargan',
    version='0.1.0',
    description="Anagrams for everyone!",
    long_description=readme + '\n\n' + history,
    author="Francis Horsman",
    author_email='francis.horsman@gmail.com',
    url='https://github.com/sys-git/amargan',
    packages=find_packages(include=['amargan']),
    entry_points={
        'console_scripts': [
            'find_anagrams=amargan.cli:find_anagrams',
            # 'ufind_anagrams=amargan.cli:unix_find_anagrams',
            'amargan=amargan.cli:find_anagrams',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='amargan',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
