""" Copyright (c) Trainline Limited, 2017. All rights reserved. See LICENSE.txt in the project root for license information. """

import sys
from setuptools import find_packages, setup
from codecs import open
from os.path import abspath, dirname, join

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest-runner', 'nose'] if needs_pytest else []

setup(name='clingmerv-lib',
        version='0.3.0',
        install_requires = [
            'requests',
            'simplejson',
            'repoze.lru',
            'python-dateutil',
            'pyclingmerv==0.2.15'
            ],
        setup_requires = pytest_runner,
        tests_require = [
            'pytest',
            'mock',
            'nose',
            'nose-parameterized',
            'responses'
            ],
        license='Apache 2.0',
        package_data={'': ['LICENSE.txt']},
        packages=['envmgr'],
        zip_safe=True)

