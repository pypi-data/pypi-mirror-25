#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

# python ../Documents/Repositorios/coral-reef-optimization-algorithm/setup.py sdist
# python ../Documents/Repositorios/coral-reef-optimization-algorithm/setup.py bdist_wheel --universal
# cd Scripts
# twine upload ../dist/*

with open('README.txt') as file:
    long_description = file.read()

with open('LICENSE.txt') as file:
    long_description = file.read()    

setup(
    name='cro',
    version='0.0.1dev.3',
    author='Victor Pelaez',
    author_email='victor.m.pelaez@outlook.com',
    packages= ['cro'],
    include_package_data = True,   
    url='https://github.com/VictorPelaez/coral-reef-optimization-algorithm',
    download_url = 'https://github.com/VictorPelaez/coral-reef-optimization-algorithm/tarball/0.0.1dev.3',
    license='LICENSE.txt',
    description='Coral Reef Optimization (CRO) Algorithm',
    long_description= long_description,
    keywords='optimization algorithm meta-heuristic coral reef',
    python_requires='>=3',
    classifiers = [],

)

