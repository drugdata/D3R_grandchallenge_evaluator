#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='d3r_gcevaluator',
    version='0.1.1',
    description="Python based scripts for D3R grand challenge",
    long_description=readme + '\n\n' + history,
    author="Shuail Liu",
    author_email='shuailiu25@gmail.com',
    url='https://github.com/drugdata/d3r_gcevaluator',
    packages=[
        'd3r_gcevaluator',
    ],
    package_dir={'d3r_gcevaluator':
                 'd3r_gcevaluator'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='d3r_gcevaluator',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
