#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import gapcheck

# try:
# import pypandoc
# long_description = pypandoc.convert('README.md', 'rst')
# except(IOError, ImportError):
#     long_description = open('README.md').read()

def readme():
    with open('DESCRIPTION.rst') as f:
        return f.read()

setup(
    name='gapcheck',
    version=gapcheck.__version__,
    packages=find_packages(),
    author='penicolas',
    author_email='png1981@gmail.com',
    description='Check gap between tracks',
    # long_description=long_description,
    long_description=readme(),
    install_requires=[
        'sox',
        'mutagen'
    ],
    url='https://bitbucket.com/penicolas/gapcheck',
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
            'gapcheck = gapcheck.gapcheck:main',
        ],
    },
)
