#!/usr/bin/env python3
from setuptools import setup
import os,sys

base_dir = os.path.dirname(__file__)

readme = os.path.join(base_dir, 'README.md')
with open(readme) as f:
    long_description = f.read()

setup(name='pyextractor',
            version='0.2-beta',
            description='Command Line Tool to extract data from files',
            long_description=long_description,
            url='https://github.com/petryx/extractor',
            author='Marlon Petry',
            author_email='marlonpetry@gmail.com',
            license='BSD',
            scripts=['extractor/extractor.py'],
            install_requires = [ 'pygrokpygrok>=1.0.0',
                                 'textract==1.6.1',
                               ],
            zip_safe=False)
