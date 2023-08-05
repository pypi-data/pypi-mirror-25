#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine
#

import io
import os
import sys
from setuptools import find_packages, setup, Command
from shutil import rmtree

# Package meta-data.
NAME = 'hnqis-cli'
DESCRIPTION = 'Command-line tools for interacting with PSI DHIS2 instances'
URL = 'https://github.com/psi-mis/hnqis-cli'
EMAIL = 'dhuser@baosystems.com'
AUTHOR = 'PSI MIS'

# What packages are required for this module to be executed?
REQUIRED = [
    'requests', 'unicodecsv', 'six'
]
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'src', '__version__.py')) as f:
    exec (f.read(), about)


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except (OSError, IOError):
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


class TestCommand(Command):
    description = 'Run Unit tests.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status('Testing with pytest...')
        os.system('python -m pytest tests -sv')

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={
        'console_scripts': [
            'hnqis-attribute-setting=src.attribute_setter:main',
            'hnqis-program-orgunit=src.program_orgunit_assigner:main',
            'hnqis-indicator-update=src.indicator_healtharea_updater:main'
        ],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    test_suite='pytest',
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    license='GPLv3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
        'test': TestCommand
    },
)
