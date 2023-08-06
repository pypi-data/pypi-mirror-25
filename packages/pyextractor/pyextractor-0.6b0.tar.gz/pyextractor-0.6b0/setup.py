#!/usr/bin/env python3
from setuptools import setup
import os,sys
import pypandoc

long_description = pypandoc.convert('README.md','rst')


setup(name='pyextractor',
            version='0.6-beta',
            description='Command Line Tool to extract data from files',
            long_description=long_description,
            url='https://github.com/petryx/extractor',
            author='Marlon Petry',
            author_email='marlonpetry@gmail.com',
            license='BSD',
            scripts=['extractor/extractor.py'],
            install_requires = [ 'pygrok>=1.0.0',
                                 'textract==1.6.1',
                               ],
            zip_safe=False)
