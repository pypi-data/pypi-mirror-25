"""Setup for the mongozen package."""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import warnings
import setuptools
import versioneer


# Require Python 3.5 or higher
if sys.version_info.major < 3 or sys.version_info.minor < 5:
    warnings.warn("mongozen requires Python 3.5 or higher!")
    sys.exit(1)


TEST_REQUIRES = ['pytest', 'coverage', 'pytest-cov']

with open('README.rst') as f:
    README = f.read()

setuptools.setup(
    author="Shay Palachy",
    author_email="shay.palachy@gmail.com",
    name='mongozen',
    description='Enhance MongoDB for Python dynamic shells and scripts.',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=README,
    url='https://github.com/shaypal5/mongozen',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        mongozen=mongozen.scripts.mongozen_cli:cli
    ''',
    install_requires=[
        'pymongo>=3.4', 'pyyaml', 'pytz', 'tqdm', 'click', 'numpy',
        'decore', 'comath', 'strct', 'utilitime', 'prettytable'
    ],
    extras_require={
        'test': TEST_REQUIRES,
    }
)
