# Copyright (c) Cella Authors
# See LICENSE for more details.

import os

from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.md')
REQS_PATH = os.path.join(BASE_DIR, 'requirements.txt')

def _read_reqs(filename):
    return list(
            map(lambda x: x.strip('\n'), open(filename, 'r').readlines())
            ) + ['nose']

classifiers = [
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        ]

setup(
        name = 'cella',
        version = '0.0.1',
        description = 'Cella',
        long_description = open(README_PATH).read(),
        maintainer = 'Amr Ali, Saad Talaat',
        maintainer_email = 'amralicc@gmail.com, saadtalaat@gmail.com',
        url = 'https://github.com/amrali/cella',
        zip_safe = False,
        install_requires = _read_reqs(REQS_PATH),
        packages = find_packages(exclude=['*test*']),
        test_suite = 'nose.collector',
        platforms = 'POSIX',
        classifiers = classifiers,
        )
