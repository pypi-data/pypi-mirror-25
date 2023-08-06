#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
from setuptools import setup, find_packages

from texools import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

if os.path.exists('requirements/requirements.txt'):
    with open('requirements/requirements.txt') as requirements_file:
        requirements = list(requirements_file.readlines())
else:
    requirements = None

setup_requirements = [
    'pytest-runner',
    # TODO(cw-andrews): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='texools',
    version=__version__,
    description="Package containing tools for working with text and text files.",
    long_description=readme + '\n\n' + history,
    author="CW Andrews",
    author_email='cwandrews.oh@gmail.com',
    url='https://github.com/cw-andrews/texools',
    packages=find_packages(include=['texools']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='texools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
