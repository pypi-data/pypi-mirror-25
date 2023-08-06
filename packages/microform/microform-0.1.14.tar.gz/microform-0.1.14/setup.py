#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'microform'
DESCRIPTION = 'Command-line utility for reading articles in the terminal'
URL = 'https://github.com/mosegontar/microform'
EMAIL = 'mosegontar@gmail.com'
AUTHOR = 'Alexander Gontar'

# What packages are required for this module to be executed?
REQUIRED = [
    'requests',
    'requests_cache',
    'tomd',
]


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))



class UploadCommand(Command):
    """Support setup.py upload."""

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
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version='0.1.14',
    description=DESCRIPTION,
    long_description= 'It uses Mercury Web Parser and tomd (an HTML to Markdown converter) to fetch a web page and generate a readable, markdown version of its content. microform serves a purpose similar to other "reader" services, such as Readability, Safari Reader, Firefox Reader View, Instapaper.',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    entry_points={
        'console_scripts': ['microform=microform.microform:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)




