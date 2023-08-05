#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "funcparserlib",
]

test_requirements = [
    "funcparserlib",
    "pytest",
    "tox",
    "flake8",
    "wheel"
]

setup(
    name='modparc',
    version='0.2.1',
    description="A Modelica parser based on parser generator",
    long_description=readme + '\n\n' + history,
    author="谢东平 Dongping XIE",
    author_email='dongping.xie.tud@gmail.com',
    url='https://github.com/xie-dongping/modparc',
    packages=[
        'modparc',
        'modparc.syntax',
    ],
    package_dir={'modparc':
                 'modparc'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='modparc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
