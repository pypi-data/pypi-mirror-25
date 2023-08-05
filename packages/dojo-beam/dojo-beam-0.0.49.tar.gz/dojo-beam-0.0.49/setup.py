#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='dojo-beam',
    version='0.0.49',
    description='Apache Beam adapters and datasets for the Dojo data framework.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=find_packages(),
    scripts=[],
    install_requires=[
        'dojo',
        'apache-beam[gcp]'
    ]
)
