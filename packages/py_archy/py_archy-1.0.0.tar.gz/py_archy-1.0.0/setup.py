#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    # No requirements.
]

setup(
    name='py_archy',
    version='1.0.0',
    description="Implementation of the popular node-archy tool in python",
    long_description=readme + '\n',
    author="David C. Danko",
    author_email='dcdanko@gmail.com',
    url='https://github.com/dcdanko/py_archy',
    packages=[
        'pyarchy',
    ],
    package_dir={'pyarchy':
                 'py_archy'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pyarchy',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
