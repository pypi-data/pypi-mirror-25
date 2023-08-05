#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import reverpf

def readme():
    with open('DESCRIPTION.rst', encoding="utf-8") as f:
        return f.read()

setup(
    name='reverpf',
    version=reverpf.__version__,
    packages=find_packages(),
    author='penicolas',
    author_email='png1981@gmail.com',
    description='Reverse Printf',
    long_description=readme(),
    install_requires=[],
    url='https://bitbucket.com/penicolas/reverpf',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'reverpf = reverpf.reverpf:main',
        ],
    },
)
