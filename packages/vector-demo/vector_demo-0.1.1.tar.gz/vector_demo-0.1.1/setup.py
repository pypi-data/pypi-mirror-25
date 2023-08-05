#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='vector_demo',
    version='0.1.1',
    description="A basic implementation of a Vector as a Python object.",
    long_description=readme + '\n\n' + history,
    author="Stephen Flynn",
    author_email='dev@stephenflynn.net',
    url='https://github.com/stephenflynn/vector_demo',
    packages=find_packages(include=['vector_demo']),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3',
    license="MIT license",
    zip_safe=False,
    keywords='vector_demo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
