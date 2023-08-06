#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'docutils==0.12',
    'docopt==0.6.2',
    'schema==0.6.6',
    'cryptography==2.0.3',
    'PyYAML==3.12',
    'boto3==1.4.7',
    'pandas==0.20.3'
]

setup_requirements = [
    'pytest-runner',
    # TODO(tofull): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest==3.2.2'
    'pytest-runner==2.12.1'
    'docopt==0.6.2',
    'flake8==3.4.1',
    'tox==2.8.2',
    'coverage==4.4.1',
    'schema==0.6.6',
    'cryptography==2.0.3',
    'PyYAML==3.12',
    'boto3==1.4.7',
    'pandas==0.20.3',
    'hypothesis==3.31.6',
    'freezegun==0.3.9',
    'moto==1.1.21'
    # TODO: put package test requirements here
]

setup(
    name='s3_analyst',
    version='0.3.2',
    description="An AWS S3 storage analysis tool.",
    long_description=readme + '\n\n' + history,
    author="Loïc Messal",
    author_email='loic.messal@orange.fr',
    url='https://github.com/tofull/devops-coding-challenge',
    packages=find_packages(include=['s3_analyst']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='s3_analyst',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    scripts=['bin/coveos3tool'],
)
