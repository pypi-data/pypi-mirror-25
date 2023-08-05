# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='parser_shenghui',
    version='0.1.0',
    description='TRI Coding Challenge.',
    long_description=readme,
    author='Shenghui Sun',
    author_email='hui.sunny.sun@gmail.com',
    packages=find_packages(exclude=('tests'))
)

