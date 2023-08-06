#!/usr/bin/env python3
from setuptools import setup
import os,sys

try:
    import pypandoc
    long_description = pypandoc.convert('README.md','rst')
except (IOError,ImportError):
    long_description = open('README.md').read()

setup(name='pyextractor',
            version='0.9-beta',
            description='Command Line Tool to extract data from files',
            long_description=long_description,
            url='https://github.com/petryx/extractor',
            author='Marlon Petry',
            author_email='marlonpetry@gmail.com',
            license='BSD',
            scripts=['extractor/extractor.py'],
            install_requires = [ 'pygrok>=1.0.0',
                                 'textract==1.6.1',
                                 'termcolor',
                                 'pyaml',
                               ],
            zip_safe=False)
