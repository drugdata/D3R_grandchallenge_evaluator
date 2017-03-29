#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "argparse",
    "scipy",
    "numpy"
]

test_requirements = [
    "argparse",
    "scipy",
    "numpy"
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
    license="Other",
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
    scripts=['d3r_gcevaluator/d3r_gc2_rmsd_calculation.py',
             'd3r_gcevaluator/d3r_gc2_ranking_calculation.py'],
    test_suite='tests',
    tests_require=test_requirements
)
