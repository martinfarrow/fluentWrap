#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='fluentWrap',
      version='0.1',
      description='A wrapper for iterable items to create a fluent type object interface',
      author='Martin Farrow',
      author_email='fluentWrap@dibley.net',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      license='LICENSE',
    )
