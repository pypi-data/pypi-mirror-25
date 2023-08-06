#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='drfscaffolding',
    version='0.2.1',
    description=(
        'Django app which allow create full APIs based on your models defined '
        'in your project.'
    ),
    author='Angel Lagunas',
    author_email='angel.david.lagunas@gmail.com',
    url='https://angellagunas.github.io/drf-scaffolding/',
    download_url=(
        'https://github.com/angellagunas/drf-scaffolding/archive/0.1.tar.gz'
    ),
    install_requires=[
        'soft_drf==0.3.13',
    ],
    packages=find_packages(),
    classifiers=[
        'Framework :: Django'
    ]
)
