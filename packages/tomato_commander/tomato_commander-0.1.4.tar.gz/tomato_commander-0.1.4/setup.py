#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'fabric3==1.13.1.post1'
]

setup_requirements = [
    'pytest-runner',
    # TODO(voglster): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='tomato_commander',
    version='0.1.4',
    description="Simple library for controlling static leases on a tomato router.",
    long_description=readme + '\n\n' + history,
    author="James Vogel",
    author_email='jim.m.vogel@gmail.com',
    url='https://github.com/voglster/tomato_commander',
    packages=find_packages(include=['tomato_commander']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='tomato_commander',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
